import { render, screen } from "@testing-library/react";
import { describe, expect, test } from "vitest";

import { BurnIn } from "./BurnIn";

// Cost as one burn-in line, never a panel: "12 FPS · NB2 · $0.07".
describe("BurnIn", () => {
  test("joins its segments with the interpunct", () => {
    render(<BurnIn segments={["12 FPS", "NB2", "$0.07"]} />);
    const line = screen.getByText("12 FPS · NB2 · $0.07");
    expect(line).toHaveClass("ro-burnin");
  });

  test("a single segment renders bare", () => {
    render(<BurnIn segments={["F03 · TAKE 2"]} />);
    expect(screen.getByText("F03 · TAKE 2")).toBeInTheDocument();
  });
});
