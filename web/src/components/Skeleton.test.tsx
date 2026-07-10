import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { CardGridSkeleton } from "./Skeleton";

describe("CardGridSkeleton — a skeleton of the marquee, not a spinner", () => {
  it("renders booth-card-shaped placeholders, hidden from the a11y tree", () => {
    render(<CardGridSkeleton count={4} />);

    const grid = screen.getByTestId("dashboard-skeleton");
    expect(grid).toHaveAttribute("aria-hidden", "true");
    expect(grid.querySelectorAll(".mq-card.mq-card--skeleton")).toHaveLength(4);
  });

  it("pulses via the ro-pulse primitive so reduced motion stills it", () => {
    render(<CardGridSkeleton count={1} />);

    const lines = screen
      .getByTestId("dashboard-skeleton")
      .querySelectorAll(".mq-sk");
    expect(lines.length).toBeGreaterThan(0);
    for (const line of lines) {
      expect(line).toHaveClass("ro-pulse");
    }
  });
});
