import { describe, expect, it } from "vitest";

import { parseShots, shotIntentLine } from "./shots";
import { shotsYaml } from "../test/fixtures";

/*
 * The client-side shots.yaml parser (U4b — G4: chain_from/beat_id live only
 * in the raw YAML artifact, so the client parses it). Display-only: the shape
 * mirrors pipeline/orchestration/shots.py (Shot/ShotList), the VALIDATION
 * stays the daemon's job — the parser only refuses what it cannot render.
 */

describe("parseShots", () => {
  it("parses the board fixture into the shots.py shape", () => {
    const sheet = parseShots(shotsYaml);
    expect(sheet.slug).toBe("spark-tidepool");
    expect(sheet.locked).toBe(false);
    expect(sheet.frames).toHaveLength(4);

    const first = sheet.frames[0];
    expect(first.id).toBe(1);
    expect(first.cast).toEqual(["sean", "claude-mascot"]);
    expect(first.beat_id).toBe(1);
    expect(first.hold).toBe(4);
    expect(first.chain_from).toBeNull();
    expect(first.prompt).toMatch(/^Wide two-shot establishing frame\./);
  });

  it("defaults hold to 2 (on-twos) and beat_id/chain_from to null when absent", () => {
    const sheet = parseShots(shotsYaml);
    expect(sheet.frames[1].hold).toBe(2);
    expect(sheet.frames[1].chain_from).toBeNull();
    const bare = parseShots(
      "slug: s\nframes:\n- id: 1\n  cast: [sean]\n  beat: b\n  prompt: p\n",
    );
    expect(bare.frames[0].beat_id).toBeNull();
    expect(bare.frames[0].chain_from).toBeNull();
    expect(bare.frames[0].hold).toBe(2);
  });

  it("carries the loop anchor: chain_from on the closing frame", () => {
    const sheet = parseShots(shotsYaml);
    expect(sheet.frames[3].chain_from).toBe(1);
  });

  it("reads a locked board's flag", () => {
    const sheet = parseShots(
      "slug: s\nlocked: true\nframes:\n- id: 1\n  cast: [sean]\n  beat: b\n  prompt: p\n",
    );
    expect(sheet.locked).toBe(true);
  });

  it("throws on malformed YAML and on a board it cannot render", () => {
    expect(() => parseShots(": : not yaml : :")).toThrow();
    // no frames — nothing to slate
    expect(() => parseShots("slug: s\n")).toThrow(/frames/);
    // a frame without an id — the slate has no cut number
    expect(() =>
      parseShots("slug: s\nframes:\n- cast: [sean]\n  prompt: p\n"),
    ).toThrow(/id/);
  });
});

describe("shotIntentLine", () => {
  it("is the prompt's first sentence for an establishing frame", () => {
    expect(
      shotIntentLine("Wide two-shot establishing frame. A young man seated."),
    ).toBe("Wide two-shot establishing frame.");
  });

  it("is the delta for a Slice-A edit frame (from ONLY CHANGE: on)", () => {
    expect(
      shotIntentLine(
        "Same two-shot, same framing. ONLY CHANGE: the mascot turns its head to LOOK down. Pencil test key drawing.",
      ),
    ).toBe("ONLY CHANGE: the mascot turns its head to LOOK down.");
  });

  it("returns the whole prompt when there is no sentence break", () => {
    expect(shotIntentLine("one unbroken line")).toBe("one unbroken line");
  });
});
