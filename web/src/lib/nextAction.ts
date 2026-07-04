import type { NextAction } from "../api/types";

/**
 * The CTA spine. Turns the daemon's next_action into the one human move a card
 * or hero leads with — the load-bearing "what's my next move?" the whole UI is
 * organized around. Strings track the spec's microcopy library + working-state
 * doctrine (agent-named while working, verb-first when it's your move).
 */
export interface Cta {
  /** The accessible words (no arrow/ellipsis — the view adds the affordance). */
  label: string;
  /** act = your move (teal, →) · wait = crew working (muted, …) · done = terminal. */
  tone: "act" | "wait" | "done";
}

/** Frame number as the pipeline names it: F03, F12. */
function frameLabel(frame: number | undefined): string | null {
  if (frame == null) return null;
  return "F" + String(frame).padStart(2, "0");
}

export function nextActionCta(na: NextAction): Cta {
  const f = frameLabel(na.frame);
  switch (na.kind) {
    case "planning":
      return { label: "Maya is planning", tone: "wait" };
    case "approve_plan":
      return { label: "Plan ready", tone: "act" };
    case "scripting":
      return { label: "Sam is drafting", tone: "wait" };
    case "approve_script":
      return { label: "Script ready", tone: "act" };
    case "storyboarding":
      return { label: "Bea is drafting", tone: "wait" };
    case "approve_storyboard":
      return { label: "Board ready", tone: "act" };
    case "approve_animatic":
      return { label: "Place the roughs", tone: "act" };
    case "generating":
      return { label: f ? `Flo is drawing ${f}` : "Flo is drawing", tone: "wait" };
    case "review_frame":
      return {
        label: f ? `${f} waiting on your eye` : "A frame waiting on your eye",
        tone: "act",
      };
    case "assemble":
      return { label: "Ready to assemble", tone: "act" };
    case "done":
      return { label: "Done", tone: "done" };
    default:
      // A kind the UI doesn't know yet — route to the run, never crash.
      return { label: "Open run", tone: "act" };
  }
}
