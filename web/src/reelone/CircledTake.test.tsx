import { render } from "@testing-library/react";
import { describe, expect, test } from "vitest";

import { CircledTake } from "./CircledTake";

// The approve flourish: a grease-pencil ellipse that draws itself around the
// printed take. Decorative — the verdict is carried by real text elsewhere.
describe("CircledTake", () => {
  test("renders a hidden-from-AT svg ellipse, undrawn by default", () => {
    const { container } = render(<CircledTake />);
    const svg = container.querySelector("svg")!;
    expect(svg).toHaveAttribute("aria-hidden", "true");
    expect(svg).toHaveClass("ro-circled");
    expect(svg).not.toHaveClass("on");
    expect(svg.querySelector("ellipse")).not.toBeNull();
  });

  test("on=true arms the circledraw animation", () => {
    const { container } = render(<CircledTake on />);
    expect(container.querySelector("svg")).toHaveClass("on");
  });
});
