import { render, screen } from "@testing-library/react";
import { describe, expect, test } from "vitest";

import { Timecode } from "./Timecode";

describe("Timecode", () => {
  test("burns in the real formula, not a hardcoded offset", () => {
    render(<Timecode frame={3} hold={2} />);
    // 3 × 2 = 6 film frames @ 12fps
    const tc = screen.getByText("00:00:00+06");
    expect(tc).toHaveClass("ro-tc");
  });

  test("rolls over seconds like the lib it wraps", () => {
    render(<Timecode frame={7} hold={2} />);
    expect(screen.getByText("00:00:01+02")).toBeInTheDocument();
  });
});
