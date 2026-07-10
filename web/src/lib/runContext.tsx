import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useRef,
  useState,
  type ReactNode,
} from "react";

import { fetchJob, fetchStatus } from "../api/client";
import type { JobView, RunStatus } from "../api/types";
import { isTerminalJobState } from "../api/types";
import { usePolledResource, type PolledResource } from "./usePolledResource";
import { useResource, type Resource } from "./useResource";

/*
 * The run-scoped context (D-D: minimal, hand-rolled). One source of truth
 * per run for the overview + the active gate: the current /status read, a
 * refresh, and the live poll of the job that owns the run. When the watched
 * job goes terminal the provider re-reads /status once, so the booth board
 * advances on the REAL terminal signal (U3 closes U2b's static seam).
 */

export interface RunContextValue {
  runId: string;
  /** GET /runs/{id}/status — the projection the screens share. */
  status: Resource<RunStatus>;
  /** Re-read /status (a gate's terminal, a manual re-read). */
  refresh: () => void;
  /** Live poll of status.active_job's /jobs/{id}; idle when the run is idle. */
  activeJob: PolledResource<JobView>;
}

const RunContext = createContext<RunContextValue | null>(null);

export function RunProvider({
  runId,
  pollIntervalMs = 1000,
  children,
}: {
  runId: string;
  /** Test override — production stays at the ~1s cadence (D-C). */
  pollIntervalMs?: number;
  children: ReactNode;
}) {
  const [nonce, setNonce] = useState(0);
  const status = useResource(() => fetchStatus(runId), [runId, nonce]);
  const refresh = useCallback(() => setNonce((n) => n + 1), []);

  const activeJobId =
    status.status === "ready" ? (status.data.active_job?.job_id ?? null) : null;

  const activeJob = usePolledResource(
    () => fetchJob(activeJobId as string),
    {
      until: (job) => isTerminalJobState(job.state),
      intervalMs: pollIntervalMs,
      enabled: activeJobId !== null,
    },
    [activeJobId],
  );

  // One refresh per terminal job (belt: active_for already filters terminal
  // jobs server-side, so the re-read can't re-arm the same poll).
  const refreshedFor = useRef<string | null>(null);
  useEffect(() => {
    if (activeJob.status !== "ready") return;
    const job = activeJob.data;
    if (!isTerminalJobState(job.state)) return;
    if (refreshedFor.current === job.job_id) return;
    refreshedFor.current = job.job_id;
    refresh();
  }, [activeJob, refresh]);

  return (
    <RunContext.Provider value={{ runId, status, refresh, activeJob }}>
      {children}
    </RunContext.Provider>
  );
}

/** The run scope, or throw — a screen outside RunProvider is a wiring bug. */
export function useRun(): RunContextValue {
  const ctx = useContext(RunContext);
  if (ctx === null) {
    throw new Error("useRun must be used inside a RunProvider");
  }
  return ctx;
}

/**
 * The optional variant for shared hooks (useGateAction refreshes the run's
 * status on a job terminal when a scope is present, and stays usable
 * without one — e.g. in isolation tests).
 */
export function useRunRefresh(): (() => void) | null {
  return useContext(RunContext)?.refresh ?? null;
}
