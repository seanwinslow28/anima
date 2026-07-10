import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { http, HttpResponse } from "msw";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it } from "vitest";

import { AnimaticGate } from "./AnimaticGate";
import { RunProvider } from "../../lib/runContext";
import { ROUTER_FUTURE } from "../../test/render";
import { server } from "../../test/handlers";
import { statusAnimaticGate, statusAnimaticHolds } from "../../test/fixtures";
import {
  gateBusy,
  JOB_ID,
  jobLifecycle,
  failedJob,
  succeededJob,
} from "../../test/jobHandlers";
import type { RunStatus } from "../../api/types";

/*
 * The Animatic gate (U4c) — the THIN opt-in placement gate. No artifact read
 * exists (G3: roughs live on disk, the daemon serves neither upload nor
 * display), so the gate's ONLY data source is the shared /status read: the
 * placement instruction is the page, the holds strip is the aside, and the
 * one decision is POST /animatic/approve. This block covers the read states;
 * the ingest flow (both actions -> the SAME POST) is its own block.
 */

const RUN = "2026-06-21-spark-animatic-driven";

function mountAnimaticGate(status: RunStatus | (() => Response) = statusAnimaticHolds) {
  server.use(
    http.get(
      "/runs/:id/status",
      typeof status === "function" ? status : () => HttpResponse.json(status),
    ),
  );
  return render(
    <MemoryRouter initialEntries={[`/runs/${RUN}/animatic`]} future={ROUTER_FUTURE}>
      <Routes>
        <Route
          path="/runs/:id"
          element={
            <RunProvider runId={RUN} pollIntervalMs={5}>
              <div data-testid="overview-screen" />
            </RunProvider>
          }
        />
        <Route
          path="/runs/:id/animatic"
          element={
            <RunProvider runId={RUN} pollIntervalMs={5}>
              <AnimaticGate pollIntervalMs={5} />
            </RunProvider>
          }
        />
        <Route
          path="/runs/:id/frames/:n"
          element={<div data-testid="eyegate-screen" />}
        />
      </Routes>
    </MemoryRouter>,
  );
}

async function seeTheGate() {
  await waitFor(() =>
    expect(
      screen.getByRole("heading", { level: 1, name: /the placement pass/i }),
    ).toBeInTheDocument(),
  );
}

describe("AnimaticGate — the read (thin: /status is the only source)", () => {
  it("renders the placement page: ONE h1, the stamp, the byline, the drop-dir instruction (G3 — disk, not upload)", async () => {
    mountAnimaticGate();
    await seeTheGate();
    // one h1 — the gate title
    expect(screen.getAllByRole("heading", { level: 1 })).toHaveLength(1);
    expect(screen.getByText(/ANIMATIC · PLACEMENT/)).toBeInTheDocument();
    expect(screen.getByText(/drawn by hand/i)).toBeInTheDocument();
    // the instruction, not a drop zone: the REAL on-disk path + the naming form
    expect(screen.getByText(`runs/${RUN}/animatic/`)).toBeInTheDocument();
    expect(screen.getByText(/F01\.png/)).toBeInTheDocument();
    // a rough is enough — silhouette recommended, per-frame optional
    expect(screen.getByText(/silhouette/i)).toBeInTheDocument();
  });

  it("the holds strip renders one cell per frame from /status.frames[].hold", async () => {
    mountAnimaticGate(statusAnimaticHolds);
    await seeTheGate();
    const strip = screen.getByRole("region", { name: /holds/i });
    const cells = within(strip).getAllByRole("listitem");
    expect(cells).toHaveLength(4);
    expect(cells[0]).toHaveTextContent("F01");
    expect(cells[0]).toHaveTextContent("×4");
    expect(cells[3]).toHaveTextContent("×5");
    // the sidecar override note — holds.json on disk wins at ingest
    expect(within(strip).getByText(/holds\.json/)).toBeInTheDocument();
  });

  it("an empty frames read (the live ANIMATIC projection) is first-class: quiet board-holds line, both actions offered", async () => {
    mountAnimaticGate(statusAnimaticGate);
    await seeTheGate();
    // no broken strip — the honest quiet line instead
    expect(screen.queryAllByRole("listitem")).toHaveLength(0);
    expect(screen.getByText(/board's holds carry the timing/i)).toBeInTheDocument();
    // the gate never assumes roughs exist: the skip path is first-class
    expect(
      screen.getByRole("button", { name: /ingest & generate/i }),
    ).toBeEnabled();
    expect(
      screen.getByRole("button", { name: /continue without roughs/i }),
    ).toBeEnabled();
  });

  it("shows the loading skeleton while /status is in flight", () => {
    mountAnimaticGate();
    expect(screen.getByTestId("gate-skeleton")).toBeInTheDocument();
  });

  it("a failed /status read is the honest error, and Retry re-reads it", async () => {
    let calls = 0;
    mountAnimaticGate(() => {
      calls += 1;
      if (calls === 1) {
        return HttpResponse.json({ detail: "boom" }, { status: 500 });
      }
      return HttpResponse.json(statusAnimaticHolds);
    });
    await waitFor(() =>
      expect(screen.getByText(/couldn't read the run/i)).toBeInTheDocument(),
    );
    await userEvent.click(screen.getByRole("button", { name: /retry/i }));
    await seeTheGate();
  });
});

const APPROVE = `/runs/${RUN}/animatic/approve`;

/** Ingest success: --approve-animatic ingested the roughs and fanned frame 1. */
const ingested = () =>
  succeededJob({
    logs:
      "animatic approved — ingested 4 placement rough(s) + 1 hold override(s); " +
      "entering GENERATE\n",
    fresh_state: { stage: "GENERATE" },
    next_action: {
      kind: "review_frame",
      frame: 1,
      hint: "next: review F01 candidate",
    },
  });

/**
 * The daemon's ingest REFUSAL (rc 2): a rough that names a frame not in the
 * board — the named gap rides job.logs verbatim (wording from
 * pipeline/orchestration/animatic_stage.py approve_animatic_gate).
 */
const ingestRefused = () =>
  failedJob({
    logs:
      "error: animatic ingest failed: animatic rough F07.png names frame 7, " +
      "which is not in the board (frames: [1, 2, 3, 4])\n" +
      `  fix the roughs/sidecar in runs/${RUN}/animatic and re-run --approve-animatic.\n`,
  });

describe("AnimaticGate — ingest & skip (both roads through the SAME POST)", () => {
  it("Ingest & generate runs the leader, then ADVANCES on the inline next_action to the eye-gate", async () => {
    mountAnimaticGate();
    server.use(
      http.post(APPROVE, () =>
        HttpResponse.json({ job_id: JOB_ID }, { status: 202 }),
      ),
      jobLifecycle(JOB_ID, ingested(), 3),
    );
    await seeTheGate();
    await userEvent.click(
      screen.getByRole("button", { name: /ingest & generate/i }),
    );
    // the shared ritual leader is the working state
    await waitFor(() => expect(screen.getByRole("status")).toBeInTheDocument());
    await waitFor(() =>
      expect(screen.getByTestId("eyegate-screen")).toBeInTheDocument(),
    );
  });

  it("Continue without roughs binds to the SAME POST — skip is approve-empty, never a second endpoint", async () => {
    mountAnimaticGate(statusAnimaticGate);
    let approvePosts = 0;
    server.use(
      http.post(APPROVE, () => {
        approvePosts += 1;
        return HttpResponse.json({ job_id: JOB_ID }, { status: 202 });
      }),
      jobLifecycle(
        JOB_ID,
        ingested(), // rc 0 either way — an empty dir proceeds with a warning
        1,
      ),
    );
    await seeTheGate();
    await userEvent.click(
      screen.getByRole("button", { name: /continue without roughs/i }),
    );
    await waitFor(() =>
      expect(screen.getByTestId("eyegate-screen")).toBeInTheDocument(),
    );
    expect(approvePosts).toBe(1);
  });

  it("⌘⏎ ingests (keyboard is a first-class hand)", async () => {
    mountAnimaticGate();
    server.use(
      http.post(APPROVE, () =>
        HttpResponse.json({ job_id: JOB_ID }, { status: 202 }),
      ),
      jobLifecycle(JOB_ID, ingested(), 2),
    );
    await seeTheGate();
    await userEvent.keyboard("{Meta>}{Enter}{/Meta}");
    await waitFor(() =>
      expect(screen.getByTestId("eyegate-screen")).toBeInTheDocument(),
    );
  });

  it("a refused ingest names the gap AND the fix — calm, on-disk, no advance", async () => {
    mountAnimaticGate();
    server.use(
      http.post(APPROVE, () =>
        HttpResponse.json({ job_id: JOB_ID }, { status: 202 }),
      ),
      jobLifecycle(JOB_ID, ingestRefused(), 1),
    );
    await seeTheGate();
    await userEvent.click(
      screen.getByRole("button", { name: /ingest & generate/i }),
    );
    // a legitimate state, not a crash
    await waitFor(() =>
      expect(screen.getByText(/roughs won't ingest yet/i)).toBeInTheDocument(),
    );
    // the NAMED GAP — the daemon's refusal, verbatim from job.logs
    expect(
      screen.getByText(/F07\.png names frame 7/),
    ).toBeInTheDocument();
    // the FIX — directive: the pass lives on disk
    expect(screen.getByText(/the fix lives on disk/i)).toBeInTheDocument();
    expect(screen.queryByTestId("eyegate-screen")).toBeNull();

    // the one recovery action re-arms the gate
    await userEvent.click(
      screen.getByRole("button", { name: /back to the placement gate/i }),
    );
    await waitFor(() =>
      expect(
        screen.getByRole("button", { name: /ingest & generate/i }),
      ).toBeInTheDocument(),
    );
  });

  it("409-busy offers to watch the running job", async () => {
    mountAnimaticGate();
    server.use(gateBusy(APPROVE, "job-owner"));
    await seeTheGate();
    await userEvent.click(
      screen.getByRole("button", { name: /ingest & generate/i }),
    );
    await waitFor(() =>
      expect(screen.getByText(/booth is busy/i)).toBeInTheDocument(),
    );
    expect(
      screen.getByRole("link", { name: /watch the running job/i }),
    ).toHaveAttribute("href", `/runs/${RUN}`);
  });

  it("blocked_by_job disables BOTH roads (single-writer made visible)", async () => {
    server.use(
      http.get("/jobs/job-owner", () =>
        HttpResponse.json({
          ...succeededJob({ job_id: "job-owner" }),
          state: "running",
          rc: null,
        }),
      ),
    );
    mountAnimaticGate({
      ...statusAnimaticGate,
      next_action: {
        kind: "approve_animatic",
        hint: "next: place roughs, then --approve-animatic",
        blocked_by_job: "job-owner",
      },
      active_job: { job_id: "job-owner", mutation_status: "running" },
    });
    await seeTheGate();
    expect(
      screen.getByRole("button", { name: /ingest & generate/i }),
    ).toBeDisabled();
    expect(
      screen.getByRole("button", { name: /continue without roughs/i }),
    ).toBeDisabled();
  });
});
