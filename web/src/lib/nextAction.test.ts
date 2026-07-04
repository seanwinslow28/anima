import { describe, expect, it } from "vitest";

import type { NextAction } from "../api/types";
import { nextActionCta } from "./nextAction";

const na = (over: Partial<NextAction>): NextAction => ({
  kind: "done",
  hint: "",
  ...over,
});

describe("nextActionCta — the CTA spine (kind -> human move)", () => {
  it("maps a plan gate to an actionable 'Plan ready'", () => {
    const cta = nextActionCta(na({ kind: "approve_plan" }));
    expect(cta.label).toBe("Plan ready");
    expect(cta.tone).toBe("act");
  });

  it("names the frame and the eye for review_frame, zero-padded", () => {
    const cta = nextActionCta(na({ kind: "review_frame", frame: 3 }));
    expect(cta.label).toBe("F03 waiting on your eye");
    expect(cta.tone).toBe("act");
  });

  it("names the agent for a working stage (planning -> Maya)", () => {
    const cta = nextActionCta(na({ kind: "planning" }));
    expect(cta.label).toBe("Maya is planning");
    expect(cta.tone).toBe("wait");
  });

  it("names Flo and the frame while generating", () => {
    const cta = nextActionCta(na({ kind: "generating", frame: 4 }));
    expect(cta.label).toBe("Flo is drawing F04");
    expect(cta.tone).toBe("wait");
  });

  it("maps assemble to 'Ready to assemble'", () => {
    const cta = nextActionCta(na({ kind: "assemble" }));
    expect(cta.label).toBe("Ready to assemble");
    expect(cta.tone).toBe("act");
  });

  it("maps done to a quiet terminal 'Done'", () => {
    const cta = nextActionCta(na({ kind: "done" }));
    expect(cta.label).toBe("Done");
    expect(cta.tone).toBe("done");
  });

  it("covers every authoring gate + working stage with a specific verb", () => {
    expect(nextActionCta(na({ kind: "scripting" })).label).toBe("Sam is drafting");
    expect(nextActionCta(na({ kind: "approve_script" })).label).toBe("Script ready");
    expect(nextActionCta(na({ kind: "storyboarding" })).label).toBe("Bea is drafting");
    expect(nextActionCta(na({ kind: "approve_storyboard" })).label).toBe(
      "Board ready",
    );
    expect(nextActionCta(na({ kind: "approve_animatic" })).label).toBe(
      "Place the roughs",
    );
  });

  it("degrades safely if the frame is missing on a frame kind", () => {
    const cta = nextActionCta(na({ kind: "review_frame" }));
    expect(cta.label).toBe("A frame waiting on your eye");
    expect(cta.tone).toBe("act");
  });

  it("degrades safely on an unknown kind", () => {
    // The daemon could add a kind before the UI knows it; never crash.
    const cta = nextActionCta(na({ kind: "brainstorming" as NextAction["kind"] }));
    expect(cta.label).toBe("Open run");
    expect(cta.tone).toBe("act");
  });
});
