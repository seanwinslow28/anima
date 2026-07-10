/*
 * The daemon contract, as TypeScript. Mirrors server/state_view.py +
 * server/jobs.py + server/routers/{gates,jobs}_router.py exactly (reads
 * verified against the live projection 2026-07-04; the job layer read from
 * the routers 2026-07-10):
 *   GET  /runs             -> RunListItem[]   (RunSummary | RunError)
 *   GET  /runs/{id}/status -> RunStatus
 *   GET  /runs/{id}        -> raw run_state.json (typed here as the
 *                             RawRunState partial — only the fields U2b reads)
 *   POST /runs/{id}/<gate> -> 202 {job_id} | 409 busy (dict detail) |
 *                             409 stale (STRING detail) | 404 | 422
 *   GET  /jobs/{job_id}    -> JobView
 */

/** next_action.kind is the navigation spine (state_view.next_action). */
export type NextActionKind =
  | "planning"
  | "approve_plan"
  | "scripting"
  | "approve_script"
  | "storyboarding"
  | "approve_storyboard"
  | "approve_animatic"
  | "generating"
  | "review_frame"
  | "assemble"
  | "done";

export interface NextAction {
  /** The machine token the UI routes and renders from. */
  kind: NextActionKind;
  /** The pipeline's own CLI "what to do next" string (verbose; not shown raw). */
  hint: string;
  /** Present only for review_frame / generating. */
  frame?: number;
  /** Present while a job owns the run — the mutating action is suppressed. */
  blocked_by_job?: string;
}

/** The job-layer overlay on /status while a job owns the run (Slice 4). */
export interface ActiveJob {
  job_id: string;
  mutation_status: string;
}

/** A readable run in the GET /runs list. */
export interface RunSummary {
  run_id: string;
  stage: string;
  slug: string;
  stub: boolean;
  updated_at: string | null;
  next_action: NextAction;
}

/** A run whose run_state.json couldn't be read — surfaced, never dropped. */
export interface RunError {
  run_id: string;
  stage: null;
  error: string;
}

export type RunListItem = RunSummary | RunError;

/** Narrow a list item to the error case (server sets stage:null + error). */
export function isRunError(item: RunListItem): item is RunError {
  return "error" in item;
}

export interface FrameState {
  n: number;
  status: string;
  attempts: number;
  hold: number | null;
}

/** GET /runs/{id}/status (status_view). */
export interface RunStatus {
  run_id: string;
  stage: string;
  stub: boolean;
  plan_status: string;
  next_action: NextAction;
  /** Always present in the projection; null when the run is idle. */
  active_job: ActiveJob | null;
  frames: FrameState[];
  updated_at: string | null;
}

/** One cost band as Maya's CostEstimatorNode emits it (all USD). */
export interface CostBand {
  low_usd: number;
  median_usd: number;
  high_usd: number;
  confidence?: string;
}

/** plan.cost_estimate — the overall band + the per-phase breakdown. */
export interface CostEstimate extends CostBand {
  by_phase: Record<string, CostBand>;
}

/**
 * GET /runs/{id} — the raw run_state.json passthrough, typed as the partial
 * U2b reads (pipeline/orchestration/state.py is the schema's source of
 * truth). needs_storyboard / animatic_enabled are the fork flags the
 * stage reel derives from; extra keys in the payload are ignored.
 */
export interface RawRunState {
  run_id: string;
  slug: string;
  stage: string;
  stub: boolean;
  /**
   * The fork flags are OPTIONAL: the raw endpoint is a passthrough and
   * load_state does not backfill, so a run authored before each flag's
   * schema landed simply lacks the key (verified live: the 2026-06-17 run
   * has no animatic_enabled). Missing reads as false — the back-compat /
   * opted-out semantics those runs actually had.
   */
  needs_storyboard?: boolean;
  animatic_enabled?: boolean;
  plan: {
    status: string;
    /** null until Maya drafts the plan ("estimate pending"). */
    cost_estimate: CostEstimate | null;
  };
}

/*
 * -- Sam's beat sheet (U4a): GET /runs/{id}/artifacts/beats --------------
 * beats.json as pipeline/orchestration/beats.py emits it (Beat/BeatSheet).
 * cast carries IR namespaces (`sean`, not the Bible folder key).
 */

export interface Beat {
  id: number;
  title: string;
  intent: string;
  emotional_beat: string;
  cast: string[];
  feel?: string | null;
  notes?: string | null;
}

export interface BeatSheet {
  slug: string;
  logline: string;
  beats: Beat[];
}

/*
 * -- Bea's shot list (U4b): GET /runs/{id}/artifacts/shots ----------------
 * shots.yaml served raw (text/plain) and parsed CLIENT-SIDE (lib/shots.ts —
 * G4: beat_id/chain_from live only in the YAML). Shape mirrors
 * pipeline/orchestration/shots.py (Shot/ShotList); display-only fields only —
 * validation stays the daemon's job at --approve-storyboard.
 */

export interface ShotFrame {
  id: number;
  /** IR namespaces; first = primary (Flo's folder key). */
  cast: string[];
  /** Em beat_description + T1 pose_description. */
  beat: string;
  /** Flo's generation prompt. */
  prompt: string;
  /** On-twos default (2) when the board doesn't say. */
  hold: number;
  /** Bea's beat->shot link; null on a pre-Bea board (the Spark original). */
  beat_id: number | null;
  /** The loop anchor — an earlier frame this one chains off (loop-return → 1). */
  chain_from: number | null;
}

export interface ShotSheet {
  slug: string;
  frames: ShotFrame[];
  /** The curation flag storyboard-approve flips; false on a draft board. */
  locked: boolean;
}

/*
 * -- The eye-gate reads (U5a): GET /runs/{id}/frames/{n}/candidates ---------
 * Shapes mirror server/artifacts.py candidates_view exactly: verdict data
 * rides through AS RECORDED (the daemon never re-derives a verdict).
 */

/** One staged patch proposal inside an Em verdict (displayed in U5a;
 *  prefilling the retry note is U5b). */
export interface EmProposedPatch {
  target: string;
  path: string;
  value: unknown;
  rationale: string;
}

/**
 * One Em (T2 vision critic) record — ONE per cast IR namespace, so an
 * attempt over a two-character frame carries two of these.
 */
export interface EmVerdict {
  frame: string;
  /** The IR namespace (`sean`), not the Bible folder key. */
  character: string;
  /** "pass" | "flag" | "human_review…" — open vocabulary, rendered as-is. */
  verdict: string;
  confidence: number | null;
  cites: string[];
  patches: number;
  proposed_patches: EmProposedPatch[];
  reasoning: string;
  notes: string;
}

/** One attempt of a frame, as /frames/{n}/candidates projects it. */
export interface CandidateAttempt {
  attempt: number;
  /** null when the fan recorded no candidate image (an honest state, not a bug). */
  image_url: string | null;
  status: "approved" | "generated" | "errored";
  t1: { verdict: string; fail_codes: string[] } | null;
  em: EmVerdict[];
  note: string | null;
  errored: string | null;
  ts: string | null;
}

/* -- the job layer (U3): POST gate -> 202 {job_id} -> poll GET /jobs/{id} -- */

/** Job lifecycle (server/jobs.py). Terminal = succeeded | failed | cancelled. */
export type JobState =
  | "pending"
  | "running"
  | "succeeded"
  | "failed"
  | "cancelled";

const TERMINAL_JOB_STATES: ReadonlySet<JobState> = new Set([
  "succeeded",
  "failed",
  "cancelled",
]);

/** Has the job left the pending/running loop? (server TERMINAL_STATES) */
export function isTerminalJobState(state: JobState): boolean {
  return TERMINAL_JOB_STATES.has(state);
}

/**
 * GET /jobs/{job_id} (jobs_router.job_view). succeeded ⇔ rc===0, but rc 0 can
 * still carry load_error / null fresh_state (the post-job state re-read
 * failed) — the DEGRADED success the hook must not auto-advance on.
 */
export interface JobView {
  job_id: string;
  run_id: string;
  state: JobState;
  rc: number | null;
  logs: string;
  /** The re-read run_state.json, handed back INLINE on terminal. */
  fresh_state: Record<string, unknown> | null;
  load_error: string | null;
  /** The post-job next_action, inline — advance on this, no /status round-trip. */
  next_action: NextAction | null;
}

/**
 * A mutating gate action, as a plain descriptor so one hook serves every
 * gate: U3 plan approve (no body), U4 script/storyboard/animatic approve
 * (no body), U5 frame approve (?attempt=K in the path) + retry ({note} body).
 */
export interface GateAction {
  method: "POST";
  /** The daemon path, e.g. /runs/{id}/plan/approve. */
  path: string;
  /** JSON body when the gate takes one (U5 retry {note}); omitted otherwise. */
  body?: unknown;
}

/**
 * The POST outcome, discriminated. THE TWO 409s ARE DISTINCT (red-team
 * blocker): busy carries a dict detail {active_job_id, reason} — offer to
 * watch that job; stale carries a PLAIN-STRING detail (stage mismatch — the
 * run already moved on) and there is NO job to watch.
 */
export type GateSubmitResult =
  | { kind: "accepted"; jobId: string }
  | { kind: "busy"; activeJobId: string; reason: string }
  | { kind: "stale"; detail: string }
  | { kind: "error"; status: number; detail: string };
