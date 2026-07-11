import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { http, HttpResponse } from "msw";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { afterEach, describe, expect, it, vi } from "vitest";

import { EyeGate } from "./EyeGate";
import { RunProvider } from "../../lib/runContext";
import { ROUTER_FUTURE } from "../../test/render";
import { server } from "../../test/handlers";
import { candidatesEdge, statusReviewFrame } from "../../test/fixtures";
import {
  failedJob,
  gateBusy,
  JOB_ID,
  jobLifecycle,
  succeededJob,
} from "../../test/jobHandlers";
import type { NextAction, RunStatus } from "../../api/types";

/*
 * PRINT (U5b) — ⏎ / the "Print it" button approves the SHOWN take through
 * U3's job flow: POST /frames/{n}/approve?attempt=K -> 202 -> the circled
 * take + the ritual leader (the working state) -> on the FULL success shape,
 * cel-flip advance to the frame the inline next_action names (the daemon
 * already skips approved frames). Reduced motion collapses the flip to a
 * soft crossfade — never a dead cut. Failure branches surface honestly.
 */

const RUN = "2026-07-04-spark-forest";
const APPROVE = `/runs/${RUN}/frames/3/approve`;

/**
 * The print-flow status: F03 under review, F04 ALREADY APPROVED, F05
 * generated — so the approve job's inline next_action (review_frame F05)
 * demonstrably skips the approved F04.
 */
const statusPrintFlow: RunStatus = {
  ...statusReviewFrame,
  frames: [
    { n: 1, status: "approved", attempts: 1, hold: 4 },
    { n: 2, status: "approved", attempts: 2, hold: 2 },
    { n: 3, status: "generated", attempts: 2, hold: 2 },
    { n: 4, status: "approved", attempts: 1, hold: 2 },
    { n: 5, status: "generated", attempts: 1, hold: 2 },
  ],
};

const nextReviewF05: NextAction = {
  kind: "review_frame",
  frame: 5,
  hint: "next: review F05 candidate",
};

function stubReducedMotion(matches: boolean) {
  vi.stubGlobal(
    "matchMedia",
    vi.fn().mockReturnValue({
      matches,
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
    }),
  );
}

afterEach(() => {
  vi.unstubAllGlobals();
});

/** Capture every approve POST's full URL; answer 202 {job_id}. */
function captureApprove(posted: string[]) {
  return http.post("/runs/:id/frames/:n/approve", ({ request }) => {
    posted.push(request.url);
    return HttpResponse.json({ job_id: JOB_ID }, { status: 202 });
  });
}

function mountEyeGate({ status = statusPrintFlow }: { status?: RunStatus } = {}) {
  server.use(http.get("/runs/:id/status", () => HttpResponse.json(status)));
  return render(
    <MemoryRouter initialEntries={[`/runs/${RUN}/frames/3`]} future={ROUTER_FUTURE}>
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
          path="/runs/:id/frames/:n"
          element={
            <RunProvider runId={RUN} pollIntervalMs={5}>
              <EyeGate pollIntervalMs={5} />
            </RunProvider>
          }
        />
      </Routes>
    </MemoryRouter>,
  );
}

async function seeTheStage() {
  await waitFor(() => expect(screen.getByTestId("stage")).toBeInTheDocument());
  return screen.getByTestId("stage");
}

function stageRegion() {
  return screen.getByRole("region", { name: /the stage/i });
}

describe("EyeGate — PRINT (⏎ approves the shown take, then the next picture comes up)", () => {
  it("keeps the two primary decisions discoverable with their 11px whisper copy", async () => {
    mountEyeGate();
    await seeTheStage();

    expect(screen.getByText("⏎ · circle the take")).toHaveClass("ro-whisper");
    expect(screen.getByText("R · the note rides along")).toHaveClass("ro-whisper");
  });

  it("calls the booth intercom with the printed take and its ledger cost on success", async () => {
    const calls: string[] = [];
    const hear = (event: Event) =>
      calls.push((event as CustomEvent<{ message: string }>).detail.message);
    window.addEventListener("reelone:intercom", hear);
    server.use(
      captureApprove([]),
      jobLifecycle(JOB_ID, succeededJob({ next_action: nextReviewF05 }), 2),
    );
    mountEyeGate();
    await seeTheStage();

    fireEvent.keyDown(stageRegion(), { key: "Enter" });

    await waitFor(() =>
      expect(calls).toContain(
        "F03 TAKE 2 — PRINTED. $0.07 to the ledger.",
      ),
    );
    window.removeEventListener("reelone:intercom", hear);
  });

  it("⏎ POSTs approve?attempt=<shown>, circles the take, runs the leader, and cel-flip advances to the inline next_action (skipping the approved F04)", async () => {
    const posted: string[] = [];
    server.use(
      captureApprove(posted),
      jobLifecycle(JOB_ID, succeededJob({ next_action: nextReviewF05 }), 2),
    );
    mountEyeGate();
    const stage = await seeTheStage();
    // no arrival flourish on a plain mount — the flip belongs to the advance
    expect(stage.className).not.toContain("eg-stage--arrive");

    const region = stageRegion();
    region.focus();
    fireEvent.keyDown(region, { key: "Enter" });

    // the circle draws on the shown take (take 2) while the job runs
    const take2 = screen.getByRole("button", { name: /take 2/i });
    await waitFor(() =>
      expect(take2.querySelector(".ro-circled.on")).toBeInTheDocument(),
    );
    // the ritual leader is the working state
    expect(screen.getByTestId("gate-working")).toBeInTheDocument();

    // the POST carried the shown take as the attempt query param
    await waitFor(() => expect(posted).toHaveLength(1));
    expect(posted[0]).toContain("/frames/3/approve?attempt=2");

    // terminal: advance to F05 (the inline next_action — F04 approved, skipped)
    await waitFor(() =>
      expect(
        screen.getByRole("heading", { level: 1, name: /F05/ }),
      ).toBeInTheDocument(),
    );
    // the next picture arrives through the cel-flip (fade-through-black)
    expect(screen.getByTestId("stage").className).toContain("eg-stage--arrive");
  });

  it("the visible Print it button drives the same flow, following a switched take", async () => {
    const user = userEvent.setup();
    const posted: string[] = [];
    server.use(
      captureApprove(posted),
      jobLifecycle(JOB_ID, succeededJob({ next_action: nextReviewF05 })),
    );
    mountEyeGate();
    await seeTheStage();

    await user.click(screen.getByRole("button", { name: /take 1/i }));
    await user.click(screen.getByRole("button", { name: /print it/i }));

    await waitFor(() => expect(posted).toHaveLength(1));
    expect(posted[0]).toContain("/frames/3/approve?attempt=1");
  });

  it("reduced motion: the advance is a soft crossfade, never a dead cut", async () => {
    stubReducedMotion(true);
    server.use(
      captureApprove([]),
      jobLifecycle(JOB_ID, succeededJob({ next_action: nextReviewF05 })),
    );
    mountEyeGate();
    await seeTheStage();

    const region = stageRegion();
    region.focus();
    fireEvent.keyDown(region, { key: "Enter" });

    await waitFor(() =>
      expect(
        screen.getByRole("heading", { level: 1, name: /F05/ }),
      ).toBeInTheDocument(),
    );
    const stage = screen.getByTestId("stage");
    expect(stage.className).toContain("eg-stage--arrive-soft");
    expect(stage.className).not.toMatch(/eg-stage--arrive(?!-soft)/);
  });

  it("an assemble next_action routes to the run overview (the cut is the loop's page)", async () => {
    server.use(
      captureApprove([]),
      jobLifecycle(
        JOB_ID,
        succeededJob({
          next_action: { kind: "assemble", hint: "next: --assemble" },
        }),
      ),
    );
    mountEyeGate();
    await seeTheStage();

    const region = stageRegion();
    region.focus();
    fireEvent.keyDown(region, { key: "Enter" });

    await waitFor(() =>
      expect(screen.getByTestId("overview-screen")).toBeInTheDocument(),
    );
  });

  it("a failed print shows rc + the log tail honestly, with a retry", async () => {
    const posted: string[] = [];
    server.use(
      captureApprove(posted),
      jobLifecycle(JOB_ID, failedJob({ logs: "flock held: frame gate raced\n" })),
    );
    mountEyeGate();
    await seeTheStage();

    const region = stageRegion();
    region.focus();
    fireEvent.keyDown(region, { key: "Enter" });

    const alert = await screen.findByRole("alert");
    expect(alert).toHaveTextContent(/rc 2/);
    expect(alert).toHaveTextContent(/flock held: frame gate raced/);
    // still on F03 — a failed print never advances
    expect(screen.getByRole("heading", { level: 1, name: /F03/ })).toBeInTheDocument();

    // the one recovery action re-submits the same print
    const user = userEvent.setup();
    await user.click(within(alert).getByRole("button", { name: /retry/i }));
    await waitFor(() => expect(posted).toHaveLength(2));
  });

  it("a 409-busy run surfaces the owning job and offers to watch it", async () => {
    server.use(gateBusy(APPROVE, "job-owner-7f3a"));
    mountEyeGate();
    await seeTheStage();

    const region = stageRegion();
    region.focus();
    fireEvent.keyDown(region, { key: "Enter" });

    const alert = await screen.findByRole("alert");
    expect(alert).toHaveTextContent(/busy/i);
    expect(alert).toHaveTextContent(/job-owner-7f3a/);
    const watch = within(alert).getByRole("link", { name: /watch/i });
    expect(watch).toHaveAttribute("href", `/runs/${RUN}`);
  });

  it("blocked_by_job disables the print (single-writer made visible) and ⏎ is inert", async () => {
    const posted: string[] = [];
    const blocked: RunStatus = {
      ...statusPrintFlow,
      next_action: {
        ...statusPrintFlow.next_action,
        blocked_by_job: "job-owner",
      },
      active_job: { job_id: "job-owner", mutation_status: "running" },
    };
    server.use(
      captureApprove(posted),
      http.get("/jobs/job-owner", () =>
        HttpResponse.json({
          ...succeededJob({ job_id: "job-owner" }),
          state: "running",
          rc: null,
        }),
      ),
    );
    mountEyeGate({ status: blocked });
    await seeTheStage();

    expect(screen.getByRole("button", { name: /print it/i })).toBeDisabled();
    const region = stageRegion();
    region.focus();
    fireEvent.keyDown(region, { key: "Enter" });
    expect(posted).toHaveLength(0);
  });

  it("a take that never developed can't be printed", async () => {
    server.use(
      http.get("/runs/:id/frames/:n/candidates", () =>
        HttpResponse.json(candidatesEdge),
      ),
    );
    mountEyeGate();
    await waitFor(() =>
      expect(screen.getByText(/this take didn't develop/i)).toBeInTheDocument(),
    );
    expect(screen.getByRole("button", { name: /print it/i })).toBeDisabled();
  });
});
