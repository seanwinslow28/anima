import { useCallback, useEffect, useRef, useState } from "react";

import { fetchJob, postGate } from "../api/client";
import type { GateAction, JobView, NextAction } from "../api/types";
import { isTerminalJobState } from "../api/types";
import { useRunRefresh } from "./runContext";
import { usePolledResource } from "./usePolledResource";

/*
 * The shared gate-action flow (D-C) — the load-bearing unit every mutating
 * surface reuses: the four document gates (U3/U4) and the eye-gate's
 * print/again (U5). POST the gate -> 202 {job_id} -> poll GET /jobs/{id}
 * (~1s) -> classify the terminal:
 *
 *   ADVANCED  only on the FULL success shape — state==="succeeded" &&
 *             rc===0 && !load_error && fresh_state && next_action — and the
 *             advance target is the INLINE next_action (no /status
 *             round-trip to navigate).
 *   DEGRADED  rc 0 but the post-job state re-read failed (load_error / null
 *             fresh_state): the take developed but the booth couldn't
 *             re-read it. Never auto-advance.
 *   FAILED    rc!=0 — surface rc + the logs tail honestly.
 *   CANCELLED back to the gate.
 *
 * The two 409s are DISTINCT (red-team blocker): busy (dict detail) carries
 * the owning job to watch; stale (string detail) means the run already moved
 * on — there is NO job to watch. Race-safety here is daemon-vs-daemon only
 * (the CLI is not locked out — fleet-ops' one-owner rule covers that).
 */

export type GateFlow =
  | { phase: "idle" }
  | { phase: "submitting" }
  | { phase: "working"; jobId: string; job: JobView | null }
  | { phase: "advanced"; job: JobView; nextAction: NextAction }
  | { phase: "degraded"; job: JobView }
  | { phase: "failed"; job: JobView }
  | { phase: "cancelled"; job: JobView }
  | { phase: "busy"; activeJobId: string; reason: string }
  | { phase: "stale"; detail: string }
  | { phase: "error"; detail: string; status?: number };

/** The terminal fork — exported for the one place a screen needs to re-derive. */
export function classifyTerminal(job: JobView): GateFlow {
  if (job.state === "cancelled") return { phase: "cancelled", job };
  if (job.state === "failed" || job.rc !== 0) return { phase: "failed", job };
  // succeeded && rc===0 — advance ONLY on the full shape
  if (!job.load_error && job.fresh_state && job.next_action) {
    return { phase: "advanced", job, nextAction: job.next_action };
  }
  return { phase: "degraded", job };
}

export function useGateAction(
  _runId: string,
  action: GateAction,
  opts?: { pollIntervalMs?: number },
): {
  flow: GateFlow;
  /** POST the gate (or a per-submit override — U5's retry note). */
  submit: (override?: GateAction) => void;
  /** Back to idle (cancelled/failed/stale -> the gate again). */
  reset: () => void;
} {
  const [flow, setFlow] = useState<GateFlow>({ phase: "idle" });
  const refreshRun = useRunRefresh();
  const pollIntervalMs = opts?.pollIntervalMs ?? 1000;

  // latest values without re-creating submit
  const actionRef = useRef(action);
  actionRef.current = action;
  const flowRef = useRef(flow);
  flowRef.current = flow;
  const alive = useRef(true);
  useEffect(() => {
    alive.current = true;
    return () => {
      alive.current = false;
    };
  }, []);

  const jobId = flow.phase === "working" ? flow.jobId : null;
  const polled = usePolledResource(
    () => fetchJob(jobId as string),
    {
      until: (job) => isTerminalJobState(job.state),
      intervalMs: pollIntervalMs,
      enabled: jobId !== null,
    },
    [jobId],
  );

  // fold each poll into the flow; classify on terminal
  useEffect(() => {
    if (jobId === null) return;
    if (polled.status === "error") {
      setFlow({ phase: "error", detail: polled.error.message });
      return;
    }
    if (polled.status !== "ready") return;
    const job = polled.data;
    if (!isTerminalJobState(job.state)) {
      setFlow({ phase: "working", jobId, job });
      return;
    }
    setFlow(classifyTerminal(job));
    // the run moved server-side — one shared /status re-read for the scope
    refreshRun?.();
  }, [polled, jobId, refreshRun]);

  const submit = useCallback(
    (override?: GateAction) => {
      const current = flowRef.current.phase;
      if (current === "submitting" || current === "working") return; // double-fire guard
      setFlow({ phase: "submitting" });
      postGate(override ?? actionRef.current).then(
        (result) => {
          if (!alive.current) return;
          switch (result.kind) {
            case "accepted":
              setFlow({ phase: "working", jobId: result.jobId, job: null });
              break;
            case "busy":
              setFlow({
                phase: "busy",
                activeJobId: result.activeJobId,
                reason: result.reason,
              });
              break;
            case "stale":
              setFlow({ phase: "stale", detail: result.detail });
              break;
            case "error":
              setFlow({
                phase: "error",
                status: result.status,
                detail: result.detail,
              });
              break;
          }
        },
        (error: unknown) => {
          if (!alive.current) return;
          setFlow({
            phase: "error",
            detail: error instanceof Error ? error.message : String(error),
          });
        },
      );
    },
    [],
  );

  const reset = useCallback(() => setFlow({ phase: "idle" }), []);

  return { flow, submit, reset };
}
