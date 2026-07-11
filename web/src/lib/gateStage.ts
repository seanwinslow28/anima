const PIPELINE_STAGES = [
  "PLAN",
  "SCRIPT",
  "STORYBOARD",
  "ANIMATIC",
  "GENERATE",
  "ASSEMBLE",
  "DONE",
] as const;

/** Unknown stages fail open so the daemon's 409-stale contract stays the backstop. */
export function hasStageMovedPast(currentStage: string, gateStage: string): boolean {
  const current = PIPELINE_STAGES.indexOf(
    currentStage.toUpperCase() as (typeof PIPELINE_STAGES)[number],
  );
  const gate = PIPELINE_STAGES.indexOf(
    gateStage.toUpperCase() as (typeof PIPELINE_STAGES)[number],
  );
  return current >= 0 && gate >= 0 && current > gate;
}
