/*
 * The daemon read contract, as TypeScript. Mirrors server/state_view.py exactly
 * (verified against the live projection on real runs, 2026-07-04):
 *   GET /runs            -> RunListItem[]   (RunSummary | RunError)
 *   GET /runs/{id}/status -> RunStatus
 * These are the only two endpoints v1a consumes; both are read-only.
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
  frames: FrameState[];
  updated_at: string | null;
}
