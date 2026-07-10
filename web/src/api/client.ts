import type {
  GateAction,
  GateSubmitResult,
  JobView,
  RawRunState,
  RunListItem,
  RunStatus,
} from "./types";

/*
 * The daemon client. Same-origin in dev (Vite proxies /runs + /jobs -> the
 * daemon sidecar), so paths are relative. Reads: a non-2xx or network failure
 * throws; screens catch it and render the one recovery action (states
 * doctrine). The gate POST is different — its non-2xx statuses ARE the
 * contract (202 / 409-busy / 409-stale / 404 / 422), so postGate returns a
 * discriminated result instead of throwing.
 */

async function getJson<T>(url: string): Promise<T> {
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`GET ${url} failed (${res.status})`);
  }
  return (await res.json()) as T;
}

/** GET /runs — every run, newest first (error items included, never dropped). */
export function fetchRuns(): Promise<RunListItem[]> {
  return getJson<RunListItem[]>("/runs");
}

/** GET /runs/{id}/status — one run's projected status. */
export function fetchStatus(id: string): Promise<RunStatus> {
  return getJson<RunStatus>(`/runs/${encodeURIComponent(id)}/status`);
}

/**
 * GET /runs/{id} — the raw run_state.json passthrough. U2b reads it for
 * plan.cost_estimate + the fork flags (needs_storyboard / animatic_enabled)
 * that shape the stage reel.
 */
export function fetchRawState(id: string): Promise<RawRunState> {
  return getJson<RawRunState>(`/runs/${encodeURIComponent(id)}`);
}

/** GET /jobs/{job_id} — one poll of a job's lifecycle view. 404 throws. */
export function fetchJob(jobId: string): Promise<JobView> {
  return getJson<JobView>(`/jobs/${encodeURIComponent(jobId)}`);
}

/**
 * GET /runs/{id}/artifacts/{kind} — an artifact's text (plan.md is
 * text/markdown; U4 reads script/beats/storyboard/shots the same way).
 */
export async function fetchArtifact(runId: string, kind: string): Promise<string> {
  const url = `/runs/${encodeURIComponent(runId)}/artifacts/${encodeURIComponent(kind)}`;
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`GET ${url} failed (${res.status})`);
  }
  return res.text();
}

/** FastAPI error bodies are {detail}; detail may not be a string (Pydantic 422). */
async function readDetail(res: Response): Promise<unknown> {
  try {
    const body = (await res.json()) as { detail?: unknown };
    return body.detail ?? `${res.status} ${res.statusText}`;
  } catch {
    return `${res.status} ${res.statusText}`;
  }
}

/**
 * POST a gate action. Every daemon-shaped outcome comes back as a
 * discriminated GateSubmitResult — THE TWO 409s ARE DISTINCT: a dict detail
 * carrying active_job_id is BUSY (offer to watch that job); a plain-string
 * detail is STALE (stage mismatch — there is no job to watch). Only a
 * network-level failure rejects.
 */
export async function postGate(action: GateAction): Promise<GateSubmitResult> {
  const res = await fetch(action.path, {
    method: action.method,
    ...(action.body !== undefined
      ? {
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(action.body),
        }
      : {}),
  });

  if (res.status === 202) {
    const body = (await res.json()) as { job_id: string };
    return { kind: "accepted", jobId: body.job_id };
  }

  const detail = await readDetail(res);

  if (res.status === 409) {
    if (
      typeof detail === "object" &&
      detail !== null &&
      "active_job_id" in detail
    ) {
      const busy = detail as { active_job_id: string; reason?: string };
      return {
        kind: "busy",
        activeJobId: busy.active_job_id,
        reason: busy.reason ?? "a job already owns this run",
      };
    }
    return { kind: "stale", detail: String(detail) };
  }

  return {
    kind: "error",
    status: res.status,
    detail: typeof detail === "string" ? detail : JSON.stringify(detail),
  };
}
