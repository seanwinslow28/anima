import type { RunError, RunStatus, RunSummary } from "../api/types";

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
  frames: [
    { n: 1, status: "approved", attempts: 1, hold: 4 },
    { n: 2, status: "approved", attempts: 2, hold: 2 },
    { n: 3, status: "generated", attempts: 1, hold: 2 },
    { n: 4, status: "pending", attempts: 0, hold: 2 },
    { n: 5, status: "pending", attempts: 0, hold: 2 },
  ],
  updated_at: "2026-07-04T18:20:00.000000+00:00",
};
