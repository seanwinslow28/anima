import type {
  FrameState,
  NextAction,
  NextActionKind,
  RawRunState,
  RunStatus,
} from "../api/types";
import type { FilmstripFrame } from "../reelone/Filmstrip";

/*
 * The booth board's pure derivations. The stage reel is RUN-SHAPE-DERIVED
 * (red-team rule: never a fixed 6-segment strip) from the state.py fork map:
 *   PLAN -> SCRIPT (authoring) | GENERATE (back-compat, brief carried shots.yaml)
 *   STORYBOARD -> ANIMATIC (opt-in) | GENERATE (default off)
 * So SCRIPT/STORYBOARD/ANIMATIC exist only when needs_storyboard; an
 * authoring run that didn't opt into the placement gate shows ANIMATIC as
 * "waived — holds carry timing" (the mockup's segment), never as a stage
 * the run will visit.
 */

/** Pipeline stage order (pipeline/orchestration/state.py STAGES). */
const STAGE_ORDER = [
  "PLAN",
  "SCRIPT",
  "STORYBOARD",
  "ANIMATIC",
  "GENERATE",
  "ASSEMBLE",
  "DONE",
] as const;

const STAGE_LABEL: Record<string, string> = {
  PLAN: "Plan",
  SCRIPT: "Script",
  STORYBOARD: "Board",
  ANIMATIC: "Animatic",
  GENERATE: "Generate",
  ASSEMBLE: "Assemble",
};

/** The station line under each segment name (constants — no invented data). */
const STAGE_WHO: Record<string, string> = {
  PLAN: "Maya · the plan",
  SCRIPT: "Sam · the script",
  STORYBOARD: "Bea · the board",
  ANIMATIC: "your roughs · placement",
  GENERATE: "Flo shoots · Em notes · you call",
  ASSEMBLE: "the splice · loop check",
};

export type SegmentStatus = "done" | "now" | "upcoming" | "waived";

export interface StageSegment {
  stage: string;
  label: string;
  /** the crew/station line under the name */
  who: string;
  /** leader countdown number — the last segment always reads 3 */
  n: number;
  status: SegmentStatus;
  /** the printed status corner: PRINTED / LOCKED / CUT k/n / NOW / — */
  mark: string;
}

function segmentMark(
  stage: string,
  status: SegmentStatus,
  frames: FrameState[],
): string {
  if (status === "done") return stage === "STORYBOARD" ? "LOCKED" : "PRINTED";
  if (status !== "now") return "—";
  if (stage === "GENERATE" && frames.length > 0) {
    const approved = frames.filter((f) => f.status === "approved").length;
    const cut = Math.min(approved + 1, frames.length);
    return `CUT ${cut}/${frames.length}`;
  }
  return "NOW";
}

/** Derive the reel of stages from the run's shape + current position. */
export function deriveStageReel(
  raw: Pick<RawRunState, "needs_storyboard" | "animatic_enabled">,
  status: Pick<RunStatus, "stage" | "frames">,
): StageSegment[] {
  const stages = STAGE_ORDER.filter((s) => {
    if (s === "DONE") return false; // the reel ends at ASSEMBLE
    if (!raw.needs_storyboard && (s === "SCRIPT" || s === "STORYBOARD" || s === "ANIMATIC")) {
      return false; // back-compat: PLAN -> GENERATE, the authoring block never exists
    }
    return true;
  });
  const cur = STAGE_ORDER.indexOf(status.stage as (typeof STAGE_ORDER)[number]);
  return stages.map((stage, i) => {
    const pos = STAGE_ORDER.indexOf(stage);
    let st: SegmentStatus =
      pos < cur ? "done" : pos === cur ? "now" : "upcoming";
    // opted-out placement gate: never visited, reads waived either side
    if (stage === "ANIMATIC" && !raw.animatic_enabled) st = "waived";
    return {
      stage,
      label: STAGE_LABEL[stage] ?? stage,
      who:
        st === "waived"
          ? "waived — holds carry timing"
          : STAGE_WHO[stage] ?? "",
      // count down like a film leader: first = N+2, last = 3
      n: stages.length + 2 - i,
      status: st,
      mark: segmentMark(stage, st, status.frames),
    };
  });
}

/**
 * The gate URL for a next_action, per U1's URL scheme. Kinds without a
 * screen (waits, assemble — auto-cascade in U3 — and done) return null:
 * the hero renders the move without a dead link.
 */
export function nextActionUrl(runId: string, na: NextAction): string | null {
  const base = `/runs/${encodeURIComponent(runId)}`;
  switch (na.kind) {
    case "approve_plan":
      return `${base}/plan`;
    case "approve_script":
      return `${base}/script`;
    case "approve_storyboard":
      return `${base}/storyboard`;
    case "approve_animatic":
      return `${base}/animatic`;
    case "review_frame":
      return na.frame != null ? `${base}/frames/${na.frame}` : null;
    default:
      return null;
  }
}

/** Where a printed segment revisits. ASSEMBLE has no page (the cut is the loop). */
export function stageRevisitUrl(runId: string, stage: string): string | null {
  const base = `/runs/${encodeURIComponent(runId)}`;
  switch (stage) {
    case "PLAN":
      return `${base}/plan`;
    case "SCRIPT":
      return `${base}/script`;
    case "STORYBOARD":
      return `${base}/storyboard`;
    case "ANIMATIC":
      return `${base}/animatic`;
    case "GENERATE":
      return `${base}/frames/1`;
    default:
      return null;
  }
}

/** The G5 per-frame NB2 constant the derived spend rides on (USD). */
export const FRAME_COST_USD = 0.07;

/**
 * The client-derived "spent so far": Σ recorded attempts × $0.07. A derived
 * running total (D-H honesty) — the daemon keeps no spend accumulator, so
 * this is labelled "≈ … drawn", never rendered as a live meter.
 */
export function deriveSpend(frames: FrameState[]): {
  attempts: number;
  usd: number;
} {
  const attempts = frames.reduce((sum, f) => sum + f.attempts, 0);
  // integer cents — 4 × 0.07 must read 0.28, not 0.28000000000000004
  return { attempts, usd: (attempts * 7) / 100 };
}

/** Human names for Maya's by_phase cost keys (fallback: prettified key). */
export function phaseLabel(key: string): string {
  const names: Record<string, string> = {
    phase_0: "Plan",
    phase_2: "Bible",
    phase_5: "Generate",
    phase_6: "Motion",
    phase_8: "Assemble",
  };
  return names[key] ?? key.replace("phase_", "Phase ");
}

/**
 * The mini frame-reel: status.frames -> <Filmstrip> cells. approved = PRINT
 * (image served), generated = ON SCREEN (the take waiting on the director,
 * ringed), the frame a live job is drawing = FLO DRAWING (pulse), the rest
 * queue quietly. The loop-return arrow needs chain_from (G4) — omitted here,
 * an eye-gate concern.
 */
export function framesToReel(
  runId: string,
  status: Pick<RunStatus, "frames" | "next_action" | "active_job">,
): FilmstripFrame[] {
  const na = status.next_action;
  const base = `/runs/${encodeURIComponent(runId)}/frames`;
  return status.frames.map((f) => {
    const label = `F${String(f.n).padStart(2, "0")}`;
    if (f.status === "approved") {
      return { id: f.n, label, status: "printed" as const, src: `${base}/${f.n}/image` };
    }
    if (f.status === "generated") {
      return {
        id: f.n,
        label,
        status: "eye" as const,
        src: `${base}/${f.n}/image`,
        now: na.kind === "review_frame" && na.frame === f.n,
      };
    }
    const drawing =
      status.active_job != null &&
      na.kind === "generating" &&
      na.frame === f.n;
    return drawing
      ? { id: f.n, label, status: "working" as const, mark: "FLO DRAWING", now: true }
      : { id: f.n, label, status: "pending" as const };
  });
}

/**
 * The crew stations — a client-side constant map (stage -> agent), the whole
 * fleet on the board. Revealed on intent (hover/focus), never permanent.
 */
export const CREW: ReadonlyArray<{ agent: string; station: string }> = [
  { agent: "Maya", station: "plan" },
  { agent: "Sam", station: "script" },
  { agent: "Bea", station: "board" },
  { agent: "Cy", station: "bible" },
  { agent: "Flo", station: "frames" },
  { agent: "Em", station: "critic" },
  { agent: "Mo", station: "docent" },
];

/** The go-button verb per next_action kind (null = no primary action). */
export function goLabel(kind: NextActionKind | string): string | null {
  switch (kind) {
    case "approve_plan":
      return "Read the plan";
    case "approve_script":
      return "Read the script";
    case "approve_storyboard":
      return "Review the board";
    case "approve_animatic":
      return "Place the roughs";
    case "review_frame":
      return "To the screening";
    default:
      return null;
  }
}
