import { describe, expect, it } from "vitest";

import {
  rawAnimatic,
  rawAuthoring,
  rawBackCompat,
  statusAnimaticGate,
  statusReviewFrame,
} from "../test/fixtures";
import { deriveStageReel, goLabel, nextActionUrl, stageRevisitUrl } from "./boothBoard";

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
