import { render } from "@testing-library/react";
import { describe, expect, test } from "vitest";

import { FilmGrain } from "./FilmGrain";

describe("FilmGrain", () => {
  test("renders a fixed grain overlay hidden from assistive tech", () => {
    const { container } = render(<FilmGrain />);
    const grain = container.firstElementChild!;
    expect(grain).toHaveAttribute("aria-hidden", "true");
    expect(grain).toHaveClass("ro-grain");
  });

  test("contains no content — it is texture, nothing else", () => {
    const { container } = render(<FilmGrain />);
    expect(container.textContent).toBe("");
  });
});
