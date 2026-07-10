import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { http, HttpResponse } from "msw";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it } from "vitest";

import { StoryboardGate } from "./StoryboardGate";
import { RunProvider } from "../../lib/runContext";
import { ROUTER_FUTURE } from "../../test/render";
import { server } from "../../test/handlers";
import {
  shotsYaml,
  statusApproveStoryboard,
  storyboardMd,
} from "../../test/fixtures";
import {
  gateAccepted,
  gateBusy,
  gateError,
  JOB_ID,
  jobLifecycle,
  succeededJob,
  validationFailedJob,
} from "../../test/jobHandlers";

/*
 * The Storyboard gate (U4b) — Bea's board as the lit continuity report +
 * the display-only slate stack, and the honest read states: loading
 * skeleton, a 404 board (a back-compat run has none) as "no board for this
 * run", an unparseable shots.yaml as a read error (never a crash). The lock
 * flow (success / THE INVALID-LOCK state) is its own block.
 */

const RUN = "2026-07-03-spark-tidepool";

function artifactHandlers() {
  const hits = { storyboard: 0, shots: 0 };
  server.use(
    http.get(`/runs/${RUN}/artifacts/storyboard`, () => {
      hits.storyboard += 1;
      return HttpResponse.text(storyboardMd, {
        headers: { "Content-Type": "text/markdown; charset=utf-8" },
      });
    }),
    http.get(`/runs/${RUN}/artifacts/shots`, () => {
      hits.shots += 1;
      return HttpResponse.text(shotsYaml, {
        headers: { "Content-Type": "text/plain; charset=utf-8" },
      });
    }),
  );
  return hits;
}

function mountStoryboardGate(status = statusApproveStoryboard) {
  server.use(http.get("/runs/:id/status", () => HttpResponse.json(status)));
  return render(
    <MemoryRouter initialEntries={[`/runs/${RUN}/storyboard`]} future={ROUTER_FUTURE}>
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
          path="/runs/:id/storyboard"
          element={
            <RunProvider runId={RUN} pollIntervalMs={5}>
              <StoryboardGate pollIntervalMs={5} />
            </RunProvider>
          }
        />
        <Route
          path="/runs/:id/animatic"
          element={<div data-testid="animatic-screen" />}
        />
        <Route
          path="/runs/:id/script"
          element={<div data-testid="script-screen" />}
        />
        <Route
          path="/runs/:id/frames/:n"
          element={<div data-testid="eyegate-screen" />}
        />
      </Routes>
    </MemoryRouter>,
  );
}

export async function seeTheBoard() {
  await waitFor(() =>
    expect(screen.getByText(/Five cuts, one fixed camera/)).toBeInTheDocument(),
  );
}

describe("StoryboardGate — the read", () => {
  it("renders Bea's board as the lit continuity page, ONE h1, Bea's byline, the slug stamp", async () => {
    artifactHandlers();
    mountStoryboardGate();
    await seeTheBoard();
    // the report's voice made it to the page
    expect(screen.getByText(/his attention is the still point/)).toBeInTheDocument();
    // one h1 — the gate title (the board's own # heading demotes to h2)
    expect(screen.getAllByRole("heading", { level: 1 })).toHaveLength(1);
    expect(
      screen.getByRole("heading", { level: 1, name: /the board/i }),
    ).toBeInTheDocument();
    expect(screen.getByText(/boarded by Bea/i)).toBeInTheDocument();
    expect(screen.getByText(/STORYBOARD · SPARK-TIDEPOOL/)).toBeInTheDocument();
  });

  it("the slate stack rides the aside: one slate per shot + the loop-return marker", async () => {
    artifactHandlers();
    mountStoryboardGate();
    await seeTheBoard();
    expect(
      screen.getByRole("region", { name: /slate stack/i }),
    ).toBeInTheDocument();
    expect(screen.getByText(/returns to frame 1/i)).toBeInTheDocument();
    // the beat links are real links back to the script gate
    expect(
      screen.getAllByRole("link", { name: /beat 1 —/i })[0],
    ).toHaveAttribute("href", `/runs/${RUN}/script`);
  });

  it("shows the loading skeleton while the two artifacts are in flight", () => {
    artifactHandlers();
    mountStoryboardGate();
    expect(screen.getByTestId("gate-skeleton")).toBeInTheDocument();
  });

  it("fetches each artifact exactly once (the board is read, not polled)", async () => {
    const hits = artifactHandlers();
    mountStoryboardGate();
    await seeTheBoard();
    expect(hits.storyboard).toBe(1);
    expect(hits.shots).toBe(1);
  });

  it("a 404 board (back-compat run) reads as an honest 'no board for this run'", async () => {
    server.use(
      http.get(`/runs/${RUN}/artifacts/storyboard`, () =>
        HttpResponse.json(
          { detail: `no artifact 'storyboard' for run '${RUN}'` },
          { status: 404 },
        ),
      ),
      http.get(`/runs/${RUN}/artifacts/shots`, () =>
        HttpResponse.json(
          { detail: `no artifact 'shots' for run '${RUN}'` },
          { status: 404 },
        ),
      ),
    );
    mountStoryboardGate();
    await waitFor(() =>
      expect(screen.getByText(/no board for this run/i)).toBeInTheDocument(),
    );
    expect(screen.getByRole("button", { name: /retry/i })).toBeInTheDocument();
  });

  it("a non-404 artifact failure is the generic honest error with Retry", async () => {
    server.use(
      http.get(`/runs/${RUN}/artifacts/storyboard`, () =>
        HttpResponse.json({ detail: "boom" }, { status: 500 }),
      ),
      http.get(`/runs/${RUN}/artifacts/shots`, () =>
        HttpResponse.text(shotsYaml),
      ),
    );
    mountStoryboardGate();
    await waitFor(() =>
      expect(screen.getByText(/couldn't read the board/i)).toBeInTheDocument(),
    );
    expect(screen.getByRole("button", { name: /retry/i })).toBeInTheDocument();
  });

  it("an unparseable shots.yaml surfaces as the read error, never a crash", async () => {
    server.use(
      http.get(`/runs/${RUN}/artifacts/storyboard`, () =>
        HttpResponse.text(storyboardMd),
      ),
      http.get(`/runs/${RUN}/artifacts/shots`, () =>
        HttpResponse.text("frames: {}\nnot: [a, board"),
      ),
    );
    mountStoryboardGate();
    await waitFor(() =>
      expect(screen.getByText(/couldn't read the board/i)).toBeInTheDocument(),
    );
    expect(screen.getByRole("button", { name: /retry/i })).toBeInTheDocument();
  });
});

const APPROVE = `/runs/${RUN}/storyboard/approve`;

/** Lock success, animatic fork: the run advances to the placement gate. */
const lockedToAnimatic = () =>
  succeededJob({
    logs: "approved: validated + locked=true on brief/shots.yaml\n",
    fresh_state: { stage: "ANIMATIC" },
    next_action: {
      kind: "approve_animatic",
      hint: "next: place roughs, then --approve-animatic",
    },
  });

/** Lock success, default fork: straight to GENERATE — frame 1 is up. */
const lockedToGenerate = () =>
  succeededJob({
    logs: "approved: validated + locked=true on brief/shots.yaml\n",
    fresh_state: { stage: "GENERATE" },
    next_action: {
      kind: "review_frame",
      frame: 1,
      hint: "next: review F01 candidate",
    },
  });

describe("StoryboardGate — Lock picture -> leader -> terminal (U3's hook, wired)", () => {
  it("lock runs the leader, then ADVANCES on the inline next_action to the animatic gate", async () => {
    artifactHandlers();
    mountStoryboardGate();
    server.use(gateAccepted(APPROVE), jobLifecycle(JOB_ID, lockedToAnimatic(), 3));
    await seeTheBoard();
    // the ONE decision (density gate: the board + one lock)
    const lock = screen.getByRole("button", { name: /lock picture/i });
    expect(lock).toBeEnabled();
    await userEvent.click(lock);
    // the shared ritual leader is the working state
    await waitFor(() => expect(screen.getByRole("status")).toBeInTheDocument());
    await waitFor(() =>
      expect(screen.getByTestId("animatic-screen")).toBeInTheDocument(),
    );
  });

  it("without animatic, lock advances to GENERATE's eye-gate on review_frame", async () => {
    artifactHandlers();
    mountStoryboardGate();
    server.use(gateAccepted(APPROVE), jobLifecycle(JOB_ID, lockedToGenerate(), 2));
    await seeTheBoard();
    await userEvent.click(screen.getByRole("button", { name: /lock picture/i }));
    await waitFor(() =>
      expect(screen.getByTestId("eyegate-screen")).toBeInTheDocument(),
    );
  });

  it("⌘⏎ locks (keyboard is a first-class hand)", async () => {
    artifactHandlers();
    mountStoryboardGate();
    server.use(gateAccepted(APPROVE), jobLifecycle(JOB_ID, lockedToAnimatic(), 2));
    await seeTheBoard();
    await userEvent.keyboard("{Meta>}{Enter}{/Meta}");
    await waitFor(() =>
      expect(screen.getByTestId("animatic-screen")).toBeInTheDocument(),
    );
  });

  it("THE INVALID-LOCK STATE: a refused lock names the gap AND the fix — calm, directive, no advance", async () => {
    const hits = artifactHandlers();
    mountStoryboardGate();
    server.use(gateAccepted(APPROVE), jobLifecycle(JOB_ID, validationFailedJob(), 1));
    await seeTheBoard();
    await userEvent.click(screen.getByRole("button", { name: /lock picture/i }));

    // a legitimate state, not a crash: "the board won't lock yet"
    await waitFor(() =>
      expect(screen.getByText(/board won't lock yet/i)).toBeInTheDocument(),
    );
    // the NAMED GAP — the daemon's re-validation reason, verbatim from job.logs
    expect(screen.getByText(/coverage gap: beat\(s\) \[3\]/)).toBeInTheDocument();
    // the FIX — directive: curation lives on disk, then re-lock
    expect(screen.getByText(/the fix lives on disk/i)).toBeInTheDocument();
    expect(screen.queryByTestId("animatic-screen")).toBeNull();
    // NOT the generic jammed-take framing — this state is its own thing
    expect(screen.queryByText(/jammed in the gate/i)).toBeNull();

    // the one recovery action re-reads the board fresh and re-arms the lock
    await userEvent.click(
      screen.getByRole("button", { name: /re-read the board/i }),
    );
    await waitFor(() =>
      expect(
        screen.getByRole("button", { name: /lock picture/i }),
      ).toBeInTheDocument(),
    );
    expect(hits.shots).toBe(2);
    expect(hits.storyboard).toBe(2);
  });

  it("a POST-level refusal (422) stays the DISTINCT generic error state, not invalid-lock", async () => {
    artifactHandlers();
    mountStoryboardGate();
    server.use(gateError(APPROVE, 422, "run_state.json is unloadable"));
    await seeTheBoard();
    await userEvent.click(screen.getByRole("button", { name: /lock picture/i }));
    await waitFor(() =>
      expect(screen.getByText(/the gate refused/i)).toBeInTheDocument(),
    );
    expect(screen.queryByText(/board won't lock yet/i)).toBeNull();
  });

  it("409-busy offers to watch the running job", async () => {
    artifactHandlers();
    mountStoryboardGate();
    server.use(gateBusy(APPROVE, "job-owner"));
    await seeTheBoard();
    await userEvent.click(screen.getByRole("button", { name: /lock picture/i }));
    await waitFor(() => expect(screen.getByText(/booth is busy/i)).toBeInTheDocument());
    expect(
      screen.getByRole("link", { name: /watch the running job/i }),
    ).toHaveAttribute("href", `/runs/${RUN}`);
  });

  it("blocked_by_job disables the lock (single-writer made visible)", async () => {
    server.use(
      http.get("/jobs/job-owner", () =>
        HttpResponse.json({
          ...succeededJob({ job_id: "job-owner" }),
          state: "running",
          rc: null,
        }),
      ),
    );
    artifactHandlers();
    mountStoryboardGate({
      ...statusApproveStoryboard,
      next_action: {
        kind: "approve_storyboard",
        hint: "next: --approve-storyboard",
        blocked_by_job: "job-owner",
      },
      active_job: { job_id: "job-owner", mutation_status: "running" },
    });
    await seeTheBoard();
    expect(
      screen.getByRole("button", { name: /lock picture/i }),
    ).toBeDisabled();
  });
});
