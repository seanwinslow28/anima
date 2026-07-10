import { renderHook, waitFor } from "@testing-library/react";
import { http, HttpResponse } from "msw";
import { act } from "react";
import { describe, expect, it } from "vitest";

import { useGateAction } from "./useGateAction";
import type { GateAction } from "../api/types";
import { server } from "../test/handlers";
import { statusReviewFrame } from "../test/fixtures";
import {
  cancelledJob,
  degradedJob,
  failedJob,
  gateAccepted,
  gateBusy,
  gateError,
  gateStale,
  JOB_ID,
  jobGone,
  jobLifecycle,
  succeededJob,
} from "../test/jobHandlers";

/*
 * The full job-flow contract (D-C) — every branch the DoD names. This hook is
 * the load-bearing shared unit U4/U5 reuse verbatim, so each branch has a
 * test: 202->poll->advanced · degraded (both shapes) · failed · cancelled ·
 * 409-busy · 409-stale · 422 · 404 (POST and poll) · the working phase ·
 * submit guard · reset.
 */

const RUN = "2026-07-03-spark-tidepool";
const APPROVE = `/runs/${RUN}/plan/approve`;
const action: GateAction = { method: "POST", path: APPROVE };

function hook() {
  return renderHook(() =>
    useGateAction(RUN, action, { pollIntervalMs: 5 }),
  );
}

describe("useGateAction — terminal outcomes", () => {
  it("202 -> poll -> full success -> ADVANCED on the inline next_action", async () => {
    server.use(gateAccepted(APPROVE), jobLifecycle(JOB_ID, succeededJob(), 2));
    const { result } = hook();
    expect(result.current.flow.phase).toBe("idle");
    act(() => result.current.submit());
    await waitFor(() => expect(result.current.flow.phase).toBe("advanced"));
    const flow = result.current.flow;
    if (flow.phase === "advanced") {
      // the INLINE next_action — no extra /status round-trip to navigate
      expect(flow.nextAction.kind).toBe("approve_script");
      expect(flow.job.rc).toBe(0);
    }
  });

  it("succeeded-but-degraded (rc 0 + load_error) -> degraded, NO advance", async () => {
    server.use(gateAccepted(APPROVE), jobLifecycle(JOB_ID, degradedJob(), 1));
    const { result } = hook();
    act(() => result.current.submit());
    await waitFor(() => expect(result.current.flow.phase).toBe("degraded"));
    const flow = result.current.flow;
    if (flow.phase === "degraded") {
      expect(flow.job.load_error).toContain("schema_version");
    }
  });

  it("succeeded-but-degraded (rc 0 + null fresh_state) -> degraded, NO advance", async () => {
    server.use(
      gateAccepted(APPROVE),
      jobLifecycle(
        JOB_ID,
        succeededJob({ fresh_state: null, next_action: null }),
        1,
      ),
    );
    const { result } = hook();
    act(() => result.current.submit());
    await waitFor(() => expect(result.current.flow.phase).toBe("degraded"));
  });

  it("failed (rc != 0) -> failed carrying rc + the logs tail", async () => {
    server.use(
      gateAccepted(APPROVE),
      jobLifecycle(JOB_ID, failedJob({ rc: 2, logs: "the gate refused: stage raced\n" }), 1),
    );
    const { result } = hook();
    act(() => result.current.submit());
    await waitFor(() => expect(result.current.flow.phase).toBe("failed"));
    const flow = result.current.flow;
    if (flow.phase === "failed") {
      expect(flow.job.rc).toBe(2);
      expect(flow.job.logs).toContain("stage raced");
    }
  });

  it("cancelled -> cancelled (the gate takes the run back)", async () => {
    server.use(gateAccepted(APPROVE), jobLifecycle(JOB_ID, cancelledJob(), 1));
    const { result } = hook();
    act(() => result.current.submit());
    await waitFor(() => expect(result.current.flow.phase).toBe("cancelled"));
  });
});

describe("useGateAction — POST outcomes", () => {
  it("409-busy (dict detail) -> busy with the active job to watch", async () => {
    server.use(gateBusy(APPROVE, "job-owner"));
    const { result } = hook();
    act(() => result.current.submit());
    await waitFor(() => expect(result.current.flow.phase).toBe("busy"));
    const flow = result.current.flow;
    if (flow.phase === "busy") {
      expect(flow.activeJobId).toBe("job-owner");
      expect(flow.reason).toBe("a job already owns this run");
    }
  });

  it("409-stale (string detail) -> stale, NOT busy — there is no job to watch", async () => {
    server.use(gateStale(APPROVE));
    const { result } = hook();
    act(() => result.current.submit());
    await waitFor(() => expect(result.current.flow.phase).toBe("stale"));
    const flow = result.current.flow;
    if (flow.phase === "stale") {
      expect(flow.detail).toContain("stage");
    }
  });

  it("422 -> error with the reason", async () => {
    server.use(gateError(APPROVE, 422, "could not load run state"));
    const { result } = hook();
    act(() => result.current.submit());
    await waitFor(() => expect(result.current.flow.phase).toBe("error"));
    const flow = result.current.flow;
    if (flow.phase === "error") {
      expect(flow.status).toBe(422);
      expect(flow.detail).toContain("could not load");
    }
  });

  it("404 (run gone) -> error", async () => {
    server.use(gateError(APPROVE, 404, `no run '${RUN}'`));
    const { result } = hook();
    act(() => result.current.submit());
    await waitFor(() => expect(result.current.flow.phase).toBe("error"));
  });

  it("a poll 404 (job gone — daemon restarted) -> error, poll stops", async () => {
    server.use(gateAccepted(APPROVE, "job-lost"), jobGone("job-lost"));
    const { result } = hook();
    act(() => result.current.submit());
    await waitFor(() => expect(result.current.flow.phase).toBe("error"));
  });
});

describe("useGateAction — the working phase + controls", () => {
  it("renders WORKING (with the polled job) while the job runs", async () => {
    // a job that never terminates during the test window
    server.use(
      gateAccepted(APPROVE),
      http.get(`/jobs/${JOB_ID}`, () =>
        HttpResponse.json({ ...succeededJob(), state: "running", rc: null }),
      ),
    );
    const { result } = hook();
    act(() => result.current.submit());
    await waitFor(() => {
      const flow = result.current.flow;
      expect(flow.phase).toBe("working");
      if (flow.phase === "working") {
        expect(flow.jobId).toBe(JOB_ID);
        expect(flow.job?.state).toBe("running");
      }
    });
  });

  it("submit is a no-op while already submitting/working (double-fire guard)", async () => {
    let posts = 0;
    server.use(
      http.post(APPROVE, () => {
        posts += 1;
        return HttpResponse.json({ job_id: JOB_ID }, { status: 202 });
      }),
      http.get(`/jobs/${JOB_ID}`, () =>
        HttpResponse.json({ ...succeededJob(), state: "running", rc: null }),
      ),
    );
    const { result } = hook();
    act(() => result.current.submit());
    await waitFor(() => expect(result.current.flow.phase).toBe("working"));
    act(() => result.current.submit());
    await new Promise((r) => setTimeout(r, 20));
    expect(posts).toBe(1);
  });

  it("reset returns the flow to idle (cancelled/failed -> back to the gate)", async () => {
    server.use(gateAccepted(APPROVE), jobLifecycle(JOB_ID, failedJob(), 1));
    const { result } = hook();
    act(() => result.current.submit());
    await waitFor(() => expect(result.current.flow.phase).toBe("failed"));
    act(() => result.current.reset());
    expect(result.current.flow.phase).toBe("idle");
  });

  it("submit(override) posts the override action (U5's per-submit retry note)", async () => {
    let body: unknown = null;
    const RETRY = `/runs/${RUN}/frames/3/retry`;
    server.use(
      http.post(RETRY, async ({ request }) => {
        body = await request.json();
        return HttpResponse.json({ job_id: JOB_ID }, { status: 202 });
      }),
      jobLifecycle(JOB_ID, succeededJob(), 1),
    );
    const { result } = hook();
    act(() =>
      result.current.submit({
        method: "POST",
        path: RETRY,
        body: { note: "looser wrist on the follow-through" },
      }),
    );
    await waitFor(() => expect(result.current.flow.phase).toBe("advanced"));
    expect(body).toEqual({ note: "looser wrist on the follow-through" });
  });
});

describe("useGateAction — runContext glue", () => {
  it("a terminal job re-reads the run's /status when inside a RunProvider", async () => {
    const { RunProvider } = await import("./runContext");
    let statusReads = 0;
    server.use(
      http.get(`/runs/:id/status`, () => {
        statusReads += 1;
        return HttpResponse.json(statusReviewFrame);
      }),
      gateAccepted(APPROVE),
      jobLifecycle(JOB_ID, succeededJob(), 1),
    );
    const { result } = renderHook(
      () => useGateAction(RUN, action, { pollIntervalMs: 5 }),
      {
        wrapper: ({ children }) => (
          <RunProvider runId={RUN} pollIntervalMs={5}>
            {children}
          </RunProvider>
        ),
      },
    );
    await waitFor(() => expect(statusReads).toBe(1));
    act(() => result.current.submit());
    await waitFor(() => expect(result.current.flow.phase).toBe("advanced"));
    await waitFor(() => expect(statusReads).toBeGreaterThanOrEqual(2));
  });
});
