import { describe, expect, it } from "vitest";

import {
  rawAnimatic,
  rawAuthoring,
  rawBackCompat,
  statusAnimaticGate,
  statusReviewFrame,
  statusWorking,
} from "../test/fixtures";
import {
  CREW,
  deriveSpend,
  deriveStageReel,
  framesToReel,
  goLabel,
  nextActionUrl,
  stageRevisitUrl,
} from "./boothBoard";

/*
 * U2b Task 2 — the run-shape-derived stage reel (red-team: never a fixed
 * 6-segment strip). The state.py fork map is canonical: SCRIPT/STORYBOARD
 * exist only on an authoring run (needs_storyboard), ANIMATIC only on the
 * authoring path — rendered "waived" when the run didn't opt in
 * (animatic_enabled false), absent entirely on back-compat.
 */

describe("deriveStageReel", () => {
  it("authoring run at GENERATE: six segments, waived animatic, CUT progress", () => {
    const reel = deriveStageReel(rawAuthoring, statusReviewFrame);
    expect(reel.map((s) => s.stage)).toEqual([
      "PLAN",
      "SCRIPT",
      "STORYBOARD",
      "ANIMATIC",
      "GENERATE",
      "ASSEMBLE",
    ]);
    expect(reel.map((s) => s.status)).toEqual([
      "done",
      "done",
      "done",
      "waived",
      "now",
      "upcoming",
    ]);
    // marks: printed / printed / locked (the board locks picture) / — / cut / —
    expect(reel[0].mark).toBe("PRINTED");
    expect(reel[2].mark).toBe("LOCKED");
    // 2 approved of 5 -> cut three is up
    expect(reel[4].mark).toBe("CUT 3/5");
    // the leader countdown: last segment reads 3 (8..3 on the six-segment reel)
    expect(reel.map((s) => s.n)).toEqual([8, 7, 6, 5, 4, 3]);
  });

  it("back-compat run: no SCRIPT / STORYBOARD / ANIMATIC segments at all", () => {
    const reel = deriveStageReel(rawBackCompat, statusReviewFrame);
    expect(reel.map((s) => s.stage)).toEqual(["PLAN", "GENERATE", "ASSEMBLE"]);
    // the countdown re-derives from the segment count (5..3), never fixed
    expect(reel.map((s) => s.n)).toEqual([5, 4, 3]);
  });

  it("animatic-enabled run at the placement gate: ANIMATIC is a real now-segment", () => {
    const reel = deriveStageReel(rawAnimatic, statusAnimaticGate);
    const animatic = reel.find((s) => s.stage === "ANIMATIC");
    expect(animatic?.status).toBe("now");
    expect(reel.find((s) => s.stage === "STORYBOARD")?.status).toBe("done");
    expect(reel.find((s) => s.stage === "GENERATE")?.status).toBe("upcoming");
  });

  it("a waived ANIMATIC stays waived even once the run is past it", () => {
    const reel = deriveStageReel(rawAuthoring, {
      ...statusReviewFrame,
      stage: "ASSEMBLE",
    });
    expect(reel.find((s) => s.stage === "ANIMATIC")?.status).toBe("waived");
    expect(reel.find((s) => s.stage === "GENERATE")?.status).toBe("done");
  });

  it("tolerates a pre-animatic run_state (no animatic_enabled key on disk)", () => {
    // Real payload shape: runs/2026-06-17-spark-authored-run predates the
    // 2026-06-18 animatic schema — the raw passthrough has NO animatic_enabled
    // (and load_state does not backfill). Missing must read as opted-out.
    // Typed WITHOUT a cast: RawRunState must admit the legacy shape.
    const legacy: import("../api/types").RawRunState = {
      run_id: "2026-06-17-spark-authored-run",
      slug: "spark-authored",
      stage: "DONE",
      stub: false,
      needs_storyboard: true,
      plan: { status: "approved", cost_estimate: null },
    };
    const reel = deriveStageReel(legacy, { stage: "DONE", frames: [] });
    expect(reel.find((s) => s.stage === "ANIMATIC")?.status).toBe("waived");
  });

  it("a DONE run reads every segment as done", () => {
    const reel = deriveStageReel(rawAuthoring, {
      ...statusReviewFrame,
      stage: "DONE",
    });
    expect(reel.every((s) => s.status === "done" || s.status === "waived")).toBe(
      true,
    );
    // DONE itself is not a segment — the reel ends at ASSEMBLE
    expect(reel.map((s) => s.stage)).not.toContain("DONE");
  });
});

describe("nextActionUrl", () => {
  it("maps the gate kinds onto U1's URL scheme", () => {
    expect(nextActionUrl("run-1", { kind: "approve_plan", hint: "" })).toBe(
      "/runs/run-1/plan",
    );
    expect(nextActionUrl("run-1", { kind: "approve_script", hint: "" })).toBe(
      "/runs/run-1/script",
    );
    expect(
      nextActionUrl("run-1", { kind: "approve_storyboard", hint: "" }),
    ).toBe("/runs/run-1/storyboard");
    expect(
      nextActionUrl("run-1", { kind: "approve_animatic", hint: "" }),
    ).toBe("/runs/run-1/animatic");
    expect(
      nextActionUrl("run-1", { kind: "review_frame", frame: 3, hint: "" }),
    ).toBe("/runs/run-1/frames/3");
  });

  it("wait / terminal / U3-only kinds have no gate URL", () => {
    for (const kind of [
      "planning",
      "scripting",
      "generating",
      "assemble",
      "done",
    ] as const) {
      expect(nextActionUrl("run-1", { kind, frame: 4, hint: "" })).toBeNull();
    }
  });
});

describe("deriveSpend", () => {
  it("sums recorded attempts × the $0.07 G5 constant — a derived total, never a meter", () => {
    // 1 + 2 + 1 + 0 + 0 attempts
    expect(deriveSpend(statusReviewFrame.frames)).toEqual({
      attempts: 4,
      usd: 0.28,
    });
  });

  it("no attempts yet -> zero, not unknown", () => {
    expect(deriveSpend([])).toEqual({ attempts: 0, usd: 0 });
  });
});

describe("framesToReel", () => {
  it("maps approved->printed (with image), generated->eye ON SCREEN (ringed)", () => {
    const reel = framesToReel("run-1", statusReviewFrame);
    expect(reel).toHaveLength(5);
    expect(reel[0]).toMatchObject({
      label: "F01",
      status: "printed",
      src: "/runs/run-1/frames/1/image",
    });
    expect(reel[2]).toMatchObject({ label: "F03", status: "eye", now: true });
    // pending with no active job: queued, no image, no ring
    expect(reel[3]).toMatchObject({ status: "pending" });
    expect(reel[3].src).toBeUndefined();
  });

  it("the frame a live job is drawing pulses FLO DRAWING", () => {
    const reel = framesToReel("run-1", statusWorking);
    expect(reel[3]).toMatchObject({
      label: "F04",
      status: "working",
      mark: "FLO DRAWING",
      now: true,
    });
    // the other pending frame stays quietly queued
    expect(reel[4]).toMatchObject({ status: "pending" });
  });
});

describe("CREW", () => {
  it("is the seven-station constant map (stage->agent, client-side)", () => {
    expect(CREW.map((c) => c.agent)).toEqual([
      "Maya",
      "Sam",
      "Bea",
      "Cy",
      "Flo",
      "Em",
      "Mo",
    ]);
  });
});

describe("stageRevisitUrl / goLabel", () => {
  it("printed stages revisit their gate; assemble has no page", () => {
    expect(stageRevisitUrl("run-1", "PLAN")).toBe("/runs/run-1/plan");
    expect(stageRevisitUrl("run-1", "STORYBOARD")).toBe("/runs/run-1/storyboard");
    expect(stageRevisitUrl("run-1", "GENERATE")).toBe("/runs/run-1/frames/1");
    expect(stageRevisitUrl("run-1", "ASSEMBLE")).toBeNull();
  });

  it("the go-button reads as the booth's verb", () => {
    expect(goLabel("review_frame")).toBe("To the screening");
    expect(goLabel("approve_plan")).toBe("Read the plan");
    expect(goLabel("generating")).toBeNull();
  });
});
