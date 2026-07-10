import type {
  BeatSheet,
  CandidateAttempt,
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

/**
 * An authoring run paused at the animatic placement gate. frames: [] is the
 * DAEMON-TRUE shape at stage ANIMATIC today (verified against
 * server/state_view.py + generate_stage.py 2026-07-10): frame_order/holds
 * populate in enter_generate, which runs AFTER --approve-animatic — so the
 * live projection carries no frames at this gate. The gate must treat the
 * empty strip as first-class, not broken.
 */
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

/**
 * The animatic gate WITH the board's frames + holds on /status — the plan's
 * intended binding (U4c: holds ride /status.frames[].hold). Forward-looking:
 * the strip lights the moment the projection carries frames at ANIMATIC; the
 * shape itself is exactly what /status serves from GENERATE onward.
 */
export const statusAnimaticHolds: RunStatus = {
  ...statusAnimaticGate,
  frames: [
    { n: 1, status: "pending", attempts: 0, hold: 4 },
    { n: 2, status: "pending", attempts: 0, hold: 2 },
    { n: 3, status: "pending", attempts: 0, hold: 2 },
    { n: 4, status: "pending", attempts: 0, hold: 5 },
  ],
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

/** An authoring run paused at the storyboard curation gate (U4b). */
export const statusApproveStoryboard: RunStatus = {
  run_id: "2026-07-03-spark-tidepool",
  stage: "STORYBOARD",
  stub: false,
  plan_status: "approved",
  next_action: {
    kind: "approve_storyboard",
    hint: "next: --approve-storyboard",
  },
  active_job: null,
  frames: [],
  updated_at: "2026-07-03T16:40:00.000000+00:00",
};

/*
 * The storyboard/shots artifact fixture pair (U4b — the Storyboard gate's two
 * reads). storyboardMd is Bea's continuity report the way she emits it (studio
 * voice, read like a report); shotsYaml is her draft board shaped EXACTLY on
 * pipeline/orchestration/shots.py — beat_id on every frame (the beat→shot
 * link), the Slice-A prompt discipline (F01 full establishing, F02+ terse
 * "Same … ONLY CHANGE:" edits), and the Slice-B loop anchor (chain_from: 1 on
 * the closing frame).
 */

export const storyboardMd = `# The board, read aloud

Five cuts, one fixed camera. The room does the acting for us.

Sean never looks up. That's the spine of the piece — his attention is the
still point, and everything that moves, moves on the shoulder.

Cut five is not a near-match, it is a **match**: composition identical to cut
one, chained from it, so when the reel loops there is no seam.
`;

export const shotsYaml = `slug: spark-tidepool
frames:
- id: 1
  cast: [sean, claude-mascot]
  beat: 'Establishing two-shot: Sean draws, the mascot perched on his shoulder, idle.'
  prompt: Wide two-shot establishing frame. A young man seated three-quarter at a
    drawing desk, stylus in his RIGHT hand; a terracotta box-creature perched on
    his shoulder, idle. Pencil test key drawing on cream paper.
  beat_id: 1
  hold: 4
- id: 2
  cast: [sean, claude-mascot]
  beat: 'The notice: the mascot turns its head to look down at the drawing.'
  prompt: 'Same two-shot, same framing and identities. ONLY CHANGE: the mascot
    turns its head to LOOK down at the drawing, curious.'
  beat_id: 2
- id: 3
  cast: [sean, claude-mascot]
  beat: 'The delight: the mascot reacts with small, genuine delight.'
  prompt: 'Same two-shot. ONLY CHANGE: the mascot reacts with small, genuine
    DELIGHT at the drawing — a quiet beat, not a gag.'
  beat_id: 3
- id: 4
  cast: [sean, claude-mascot]
  beat: 'The settle: composition identical to frame 1 so the loop closes.'
  prompt: 'Composition identical to frame 1. The mascot eases back to its idle
    perched pose; the drawing hand returns to its start position.'
  beat_id: 4
  chain_from: 1
`;

/*
 * The eye-gate's /frames/{n}/candidates fixtures (U5a). Shaped EXACTLY on
 * server/artifacts.py candidates_view over tests/server/conftest.py's
 * make_generate_run — the verbatim flag→pass two-attempt Em story (attempt 1
 * flag "line weight drifts on the arm" cites IR.sean.style.line-weight →
 * attempt 2 pass "Ship.", carrying the retry note). Frame 3 of the
 * statusReviewFrame run, under review: neither attempt approved.
 */

const F3_IMG = "/runs/2026-07-04-spark-forest/frames/3/image";

export const candidatesFlagPass: CandidateAttempt[] = [
  {
    attempt: 1,
    image_url: `${F3_IMG}?attempt=1`,
    status: "generated",
    t1: { verdict: "needs_vision_review", fail_codes: [] },
    em: [
      {
        frame: "SPARK_F03",
        character: "sean",
        verdict: "flag",
        confidence: 0.8,
        cites: ["IR.sean.style.line-weight"],
        patches: 0,
        proposed_patches: [],
        reasoning: "line weight drifts on the arm",
        notes: "em@phase_5_generate frame=SPARK_F03 (gemini)",
      },
    ],
    note: null,
    errored: null,
    ts: "2026-07-04T00:00:00+00:00",
  },
  {
    attempt: 2,
    image_url: `${F3_IMG}?attempt=2`,
    status: "generated",
    t1: { verdict: "needs_vision_review", fail_codes: [] },
    em: [
      {
        frame: "SPARK_F03",
        character: "sean",
        verdict: "pass",
        confidence: 1.0,
        cites: [],
        patches: 0,
        proposed_patches: [],
        reasoning: "Ship.",
        notes: "em@phase_5_generate frame=SPARK_F03 (gemini)",
      },
    ],
    note: "hold the line weight from the anchor",
    errored: null,
    ts: "2026-07-04T00:05:00+00:00",
  },
];

/**
 * Two cast namespaces on one attempt (the >1 em record case — one verdict per
 * IR namespace) + a real proposed_patches entry (the fix slot's data). The
 * mascot flags with a proposed fix; sean passes.
 */
export const candidatesTwoCast: CandidateAttempt[] = [
  {
    attempt: 1,
    image_url: `${F3_IMG}?attempt=1`,
    status: "generated",
    t1: { verdict: "needs_vision_review", fail_codes: [] },
    em: [
      {
        frame: "SPARK_F03",
        character: "sean",
        verdict: "pass",
        confidence: 0.95,
        cites: [],
        patches: 0,
        proposed_patches: [],
        reasoning: "Holds from the anchor.",
        notes: "em@phase_5_generate frame=SPARK_F03 (gemini)",
      },
      {
        frame: "SPARK_F03",
        character: "claude-mascot",
        verdict: "flag",
        confidence: 0.7,
        cites: ["IR.claude-mascot.anatomy.leg-count-4"],
        patches: 1,
        proposed_patches: [
          {
            target: "frame_prompt",
            path: "prompt",
            value: "the box-creature keeps exactly four legs",
            rationale: "a fifth leg ghosts in on the near side",
          },
        ],
        reasoning: "a fifth leg ghosts in on the near side",
        notes: "em@phase_5_generate frame=SPARK_F03 (gemini)",
      },
    ],
    note: null,
    errored: null,
    ts: "2026-07-04T00:00:00+00:00",
  },
];

/**
 * The honest-state edges: a take whose image never landed (image_url null)
 * and an errored fan (status "errored" + the recorded error). Neither may
 * render a broken <img>.
 */
export const candidatesEdge: CandidateAttempt[] = [
  {
    attempt: 1,
    image_url: null,
    status: "generated",
    t1: null,
    em: [],
    note: null,
    errored: null,
    ts: "2026-07-04T00:00:00+00:00",
  },
  {
    attempt: 2,
    image_url: null,
    status: "errored",
    t1: null,
    em: [],
    note: null,
    errored: "NB2 transport timed out",
    ts: "2026-07-04T00:05:00+00:00",
  },
];

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
