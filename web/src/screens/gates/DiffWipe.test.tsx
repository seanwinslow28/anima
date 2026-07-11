import { render, screen } from "@testing-library/react";
import { expect, it, vi } from "vitest";

import { WipeControls } from "./DiffWipe";

it("names the dominant side of the wipe for assistive technology", () => {
  render(
    <WipeControls
      options={[
        { key: "take-1", label: "TAKE 1", url: "/take-1.png" },
        { key: "take-2", label: "TAKE 2", url: "/take-2.png" },
      ]}
      selectedKey="take-2"
      onSelect={vi.fn()}
      wipe={62}
      onWipe={vi.fn()}
    />,
  );

  expect(screen.getByRole("slider", { name: /wipe position/i })).toHaveAttribute(
    "aria-valuetext",
    "62% — mostly TAKE 2",
  );
});
