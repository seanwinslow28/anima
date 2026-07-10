import type {
  BeatSheet,
  RawRunState,
  RunError,
  RunStatus,
  RunSummary,
} from "../api/types";

/*
 * Fixtures shaped on the live daemon projection of real runs (captured
 * 2026-07-04 from server.state_view). Kept deliberately small; tests that need
 * a specific list override the MSW handler with these.
 */

export const runReviewFrame: RunSummary = {
  run_id: "2026-07-04-spark-forest",
  stage: "GENERATE",
  slug: "spark-forest",
  stub: false,
  updated_at: "2026-07-04T18:20:00.000000+00:00",
  next_action: {
    kind: "review_frame",
    frame: 3,
    hint: "next: review F03 candidate",
  },
};

export const runApprovePlan: RunSummary = {
  run_id: "2026-07-03-spark-tidepool",
  stage: "PLAN",
  slug: "spark-tidepool",
  stub: false,
  updated_at: "2026-07-03T14:02:00.000000+00:00",
  next_action: {
    kind: "approve_plan",
    hint: "next: --approve-plan",
  },
};

export const runDone: RunSummary = {
  run_id: "2026-06-21-spark-animatic-driven",
  stage: "DONE",
  slug: "spark-animatic",
  stub: false,
  updated_at: "2026-06-22T16:36:42.596295+00:00",
  next_action: {
    kind: "done",
    hint: "done: {'gif': '.../spark-animatic.gif'}",
  },
};

export const runStub: RunSummary = {
  run_id: "2026-07-01-spark-smoke",
  stage: "STORYBOARD",
  slug: "spark-smoke",
  stub: true,
  updated_at: "2026-07-01T09:00:00.000000+00:00",
  next_action: {
    kind: "approve_storyboard",
    hint: "next: --approve-storyboard",
  },
};

export const runErrorItem: RunError = {
  run_id: "2026-06-30-broken-run",
  stage: null,
  error: "unsupported schema_version 99",
};

export const statusReviewFrame: RunStatus = {
  run_id: "2026-07-04-spark-forest",
  stage: "GENERATE",
  stub: false,
  plan_status: "approved",
  next_action: {
    kind: "review_frame",
    frame: 3,
    hint: "next: review F03 candidate",
  },
  active_job: null,
  frames: [
    { n: 1, status: "approved", attempts: 1, hold: 4 },
    { n: 2, status: "approved", attempts: 2, hold: 2 },
    { n: 3, status: "generated", attempts: 1, hold: 2 },
    { n: 4, status: "pending", attempts: 0, hold: 2 },
    { n: 5, status: "pending", attempts: 0, hold: 2 },
  ],
  updated_at: "2026-07-04T18:20:00.000000+00:00",
};

/** An authoring run paused at the plan gate (U3 — the Plan gate's home state). */
export const statusApprovePlan: RunStatus = {
  run_id: "2026-07-03-spark-tidepool",
  stage: "PLAN",
  stub: false,
  plan_status: "draft",
  next_action: {
    kind: "approve_plan",
    hint: "next: --approve-plan",
  },
  active_job: null,
  frames: [],
  updated_at: "2026-07-03T14:02:00.000000+00:00",
};

/** An authoring run paused at the script gate (U4a — the Script gate's home state). */
export const statusApproveScript: RunStatus = {
  run_id: "2026-07-03-spark-tidepool",
  stage: "SCRIPT",
  stub: false,
  plan_status: "approved",
  next_action: {
    kind: "approve_script",
    hint: "next: --approve-script",
  },
  active_job: null,
  frames: [],
  updated_at: "2026-07-03T15:10:00.000000+00:00",
};

/** The plan gate while a job owns the run — the mutating control disables. */
export const statusApprovePlanBlocked: RunStatus = {
  ...statusApprovePlan,
  next_action: {
    kind: "approve_plan",
    hint: "next: --approve-plan",
    blocked_by_job: "job-owner",
  },
  active_job: { job_id: "job-owner", mutation_status: "running" },
};

/** A GENERATE run mid-fan: a job owns the run, Flo is drawing F04 (Slice 4). */
export const statusWorking: RunStatus = {
  run_id: "2026-07-04-spark-forest",
  stage: "GENERATE",
  stub: false,
  plan_status: "approved",
  next_action: {
    kind: "generating",
    frame: 4,
    hint: "working: generating F04",
    blocked_by_job: "job-7f3a",
  },
  active_job: { job_id: "job-7f3a", mutation_status: "running" },
  frames: [
    { n: 1, status: "approved", attempts: 1, hold: 4 },
    { n: 2, status: "approved", attempts: 2, hold: 2 },
    { n: 3, status: "approved", attempts: 1, hold: 2 },
    { n: 4, status: "pending", attempts: 0, hold: 2 },
    { n: 5, status: "pending", attempts: 0, hold: 2 },
  ],
  updated_at: "2026-07-04T18:25:00.000000+00:00",
};

/** An authoring run paused at the animatic placement gate. */
export const statusAnimaticGate: RunStatus = {
  run_id: "2026-06-21-spark-animatic-driven",
  stage: "ANIMATIC",
  stub: false,
  plan_status: "approved",
  next_action: {
    kind: "approve_animatic",
    hint: "next: place roughs, then --approve-animatic",
  },
  active_job: null,
  frames: [],
  updated_at: "2026-06-21T12:00:00.000000+00:00",
};

/*
 * The script/beats artifact fixture pair (U4a — the Script gate's two reads).
 * scriptMd is screenplay-register markdown the way Sam emits it (scene
 * heading, action lines, indented dialogue — markdown renders the indent as
 * a code block, which the screenplay CSS restyles as the dialogue column).
 */

export const scriptMd = `INT. THE STUDIO — NIGHT

Sean draws. The mascot watches from his shoulder, box-head tilted.

    SEAN
    There you are.

The line lands on the page and the little creature lights up.
`;

/** Sam's beat sheet, shaped on pipeline/orchestration/beats.py. */
export const beatsFixture: BeatSheet = {
  slug: "spark-tidepool",
  logline:
    "Sean draws; the mascot notices and delights; everything settles back to the start.",
  beats: [
    {
      id: 1,
      title: "Establishing two-shot",
      intent: "Set the look, framing, and scale — the anchor the loop returns to.",
      emotional_beat: "calm focus",
      cast: ["sean", "claude-mascot"],
      feel: "establishing — let it breathe",
      notes: "the closing beat returns here",
    },
    {
      id: 2,
      title: "The notice",
      intent: "The mascot perks up — the spark of catching the idea.",
      emotional_beat: "spark",
      cast: ["claude-mascot"],
    },
  ],
};

/*
 * Raw run-state fixtures (GET /runs/{id} — the passthrough of run_state.json).
 * Typed as the RawRunState partial; shapes captured from a real authored run
 * (2026-06-21-spark-animatic-driven) — cost_estimate is Maya's real band.
 */

/** Authoring run (Sam→Bea), animatic waived, plan costed. */
export const rawAuthoring: RawRunState = {
  run_id: "2026-07-04-spark-forest",
  slug: "spark-forest",
  stage: "GENERATE",
  stub: false,
  needs_storyboard: true,
  animatic_enabled: false,
  plan: {
    status: "approved",
    cost_estimate: {
      low_usd: 0.35,
      median_usd: 0.93,
      high_usd: 2.25,
      by_phase: {
        phase_2: { low_usd: 0, median_usd: 0, high_usd: 0 },
        phase_5: { low_usd: 0.35, median_usd: 0.93, high_usd: 2.25, confidence: "full" },
        phase_6: { low_usd: 0, median_usd: 0, high_usd: 0 },
        phase_8: { low_usd: 0, median_usd: 0, high_usd: 0 },
      },
    },
  },
};

/** Back-compat run (brief carried shots.yaml — no SCRIPT/STORYBOARD ever). */
export const rawBackCompat: RawRunState = {
  run_id: "2026-07-04-spark-forest",
  slug: "spark-forest",
  stage: "GENERATE",
  stub: false,
  needs_storyboard: false,
  animatic_enabled: false,
  plan: {
    status: "approved",
    cost_estimate: {
      low_usd: 0.35,
      median_usd: 0.93,
      high_usd: 2.25,
      by_phase: {
        phase_5: { low_usd: 0.35, median_usd: 0.93, high_usd: 2.25, confidence: "full" },
      },
    },
  },
};

/**
 * Animatic-enabled authoring run. cost_estimate null exercises the
 * pre-draft "estimate pending" path (the field is null until Maya drafts).
 */
export const rawAnimatic: RawRunState = {
  run_id: "2026-06-21-spark-animatic-driven",
  slug: "spark-animatic",
  stage: "ANIMATIC",
  stub: false,
  needs_storyboard: true,
  animatic_enabled: true,
  plan: { status: "approved", cost_estimate: null },
};
