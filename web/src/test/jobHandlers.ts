import { http, HttpResponse } from "msw";

import type { JobView, NextAction } from "../api/types";

/*
 * The reusable job-lifecycle MSW seam (U3) — the template U4/U5 import.
 *
 * Two halves, mirroring the daemon's two surfaces:
 *   1. POST gate handlers  — gateAccepted / gateBusy / gateStale / gateError
 *      (the four response shapes of server/routers/gates_router.py; the two
 *      409s are DISTINCT — busy is a dict detail, stale a plain string).
 *   2. GET /jobs/:id       — jobSequence (poll k returns views[k], last view
 *      repeats) with jobLifecycle sugar (N running polls, then the terminal).
 *
 * JobView factories build the terminal shapes the DoD names: succeededJob
 * (full success), degradedJob (rc 0 + load_error / null fresh_state),
 * failedJob (rc!=0 + logs), cancelledJob.
 */

export const JOB_ID = "job-msw-0001";

export const nextActionApproveScript: NextAction = {
  kind: "approve_script",
  hint: "next: --approve-script",
};

/** A JobView with sane running defaults; override any field. */
export function jobView(overrides: Partial<JobView> = {}): JobView {
  return {
    job_id: JOB_ID,
    run_id: "2026-07-03-spark-tidepool",
    state: "running",
    rc: null,
    logs: "",
    fresh_state: null,
    load_error: null,
    next_action: null,
    ...overrides,
  };
}

/** Full success: rc 0, fresh_state + next_action handed back inline. */
export function succeededJob(overrides: Partial<JobView> = {}): JobView {
  return jobView({
    state: "succeeded",
    rc: 0,
    logs: "plan approved\n",
    fresh_state: { stage: "SCRIPT" },
    next_action: nextActionApproveScript,
    ...overrides,
  });
}

/** Degraded success: the job ran (rc 0) but the state re-read failed. */
export function degradedJob(overrides: Partial<JobView> = {}): JobView {
  return jobView({
    state: "succeeded",
    rc: 0,
    logs: "plan approved\n",
    fresh_state: null,
    next_action: null,
    load_error: "unsupported schema_version 99",
    ...overrides,
  });
}

/** Honest failure: rc != 0 + the logs tail. */
export function failedJob(overrides: Partial<JobView> = {}): JobView {
  return jobView({
    state: "failed",
    rc: 2,
    logs: "stage precheck raced: run is at stage 'SCRIPT'\n",
    ...overrides,
  });
}

export function cancelledJob(overrides: Partial<JobView> = {}): JobView {
  return jobView({ state: "cancelled", rc: null, ...overrides });
}

/**
 * The storyboard curation gate's REFUSAL (U4b's invalid-lock state): the
 * approve job fails (rc!=0) because --approve-storyboard re-validated the
 * board and refused to lock it — the named gap rides job.logs verbatim
 * (wording from pipeline/cli/storyboard.py approve_storyboard +
 * storyboard_validate's coverage message).
 */
export function validationFailedJob(overrides: Partial<JobView> = {}): JobView {
  return jobView({
    state: "failed",
    rc: 2,
    logs:
      "error: curation gate failed — not locking brief/shots.yaml:\n" +
      "  coverage gap: beat(s) [3] are boarded by no shot (no frame carries " +
      "their beat_id) — every beat needs a shot\n",
    ...overrides,
  });
}

/* -- GET /jobs/:id ---------------------------------------------------- */

/**
 * Poll k answers views[k]; the last view repeats forever (a terminal job
 * stays terminal). The primitive under jobLifecycle — use directly for
 * odd sequences (e.g. pending -> running -> failed).
 */
export function jobSequence(jobId: string, views: JobView[]) {
  let poll = 0;
  return http.get(`/jobs/${jobId}`, () => {
    const view = views[Math.min(poll, views.length - 1)];
    poll += 1;
    return HttpResponse.json(view);
  });
}

/** `runningPolls` running answers, then `terminal` forever. */
export function jobLifecycle(
  jobId: string,
  terminal: JobView,
  runningPolls = 1,
) {
  const running = Array.from({ length: runningPolls }, () =>
    jobView({ job_id: jobId }),
  );
  return jobSequence(jobId, [...running, { ...terminal, job_id: jobId }]);
}

/** GET /jobs/:id -> 404 (daemon restarted — the registry is process-lifetime). */
export function jobGone(jobId: string) {
  return http.get(`/jobs/${jobId}`, () =>
    HttpResponse.json({ detail: `no job '${jobId}'` }, { status: 404 }),
  );
}

/* -- POST gate -------------------------------------------------------- */

/** 202 {job_id} — the slot is reserved, the worker is dispatched. */
export function gateAccepted(path: string, jobId = JOB_ID) {
  return http.post(path, () =>
    HttpResponse.json({ job_id: jobId }, { status: 202 }),
  );
}

/** 409 BUSY — detail is a DICT {active_job_id, reason}. */
export function gateBusy(path: string, activeJobId = JOB_ID) {
  return http.post(path, () =>
    HttpResponse.json(
      {
        detail: {
          active_job_id: activeJobId,
          reason: "a job already owns this run",
        },
      },
      { status: 409 },
    ),
  );
}

/** 409 STALE — detail is a PLAIN STRING (stage mismatch; no job to watch). */
export function gateStale(
  path: string,
  detail = "run is at stage 'SCRIPT', not 'PLAN' (this gate's stage)",
) {
  return http.post(path, () =>
    HttpResponse.json({ detail }, { status: 409 }),
  );
}

/** POST -> 404 (run gone) or 422 (unloadable state / bad note). */
export function gateError(path: string, status: 404 | 422, detail: string) {
  return http.post(path, () => HttpResponse.json({ detail }, { status }));
}
