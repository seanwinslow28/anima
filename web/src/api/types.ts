/*
 * The daemon read contract, as TypeScript. Mirrors server/state_view.py exactly
 * (verified against the live projection on real runs, 2026-07-04):
 *   GET /runs            -> RunListItem[]   (RunSummary | RunError)
 *   GET /runs/{id}/status -> RunStatus
 *   GET /runs/{id}       -> raw run_state.json (typed here as the RawRunState
 *                           partial — only the fields U2b reads)
 * All read-only; the POST/job types land with U3.
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
  needs_storyboard: boolean;
  animatic_enabled: boolean;
  plan: {
    status: string;
    /** null until Maya drafts the plan ("estimate pending"). */
    cost_estimate: CostEstimate | null;
  };
}
