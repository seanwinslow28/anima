import { describe, expect, test } from "vitest";

import { TC } from "./timecode";

// Timecode = frame_index × hold @ 12fps, rendered "HH:MM:SS+FF" (the burn-in
// format from the REEL ONE mockups; FF is the frames field, base fps).
describe("TC", () => {
  test("frame 0 is zero timecode", () => {
    expect(TC(0, 2)).toBe("00:00:00+00");
  });

  test("frames accumulate in the +FF field before a full second", () => {
    // hold 2 → each board frame advances 2 film frames (the mockup's +00/+02/+04)
    expect(TC(1, 2)).toBe("00:00:00+02");
    expect(TC(2, 2)).toBe("00:00:00+04");
  });

  test("12 film frames roll over into one second at the default 12fps", () => {
    expect(TC(6, 2)).toBe("00:00:01+00");
    expect(TC(7, 2)).toBe("00:00:01+02");
  });

  test("seconds roll into minutes and minutes into hours", () => {
    // 60s × 12fps = 720 film frames → hold 1, index 720
    expect(TC(720, 1)).toBe("00:01:00+00");
    // 3600s × 12fps = 43200 film frames
    expect(TC(43200, 1)).toBe("01:00:00+00");
  });

  test("every field zero-pads to two digits", () => {
    // 500 film frames = 41s + 8 frames
    expect(TC(100, 5)).toBe("00:00:41+08");
  });

  test("fps is overridable", () => {
    // 24 film frames @ 24fps = exactly one second
    expect(TC(24, 1, 24)).toBe("00:00:01+00");
    expect(TC(25, 1, 24)).toBe("00:00:01+01");
  });
});
