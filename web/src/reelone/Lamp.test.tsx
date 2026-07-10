import { render, screen } from "@testing-library/react";
import { describe, expect, test } from "vitest";

import { Lamp } from "./Lamp";

// The lamp is a lit signal BEFORE a word: the semantic hue arrives ahead of
// the text. PRINT = approve (green), HOLD = Em's amber, FAIL = bakelite.
describe("Lamp", () => {
  test("print verdict lights the print lamp with the word", () => {
    render(<Lamp verdict="print" />);
    const lamp = screen.getByRole("img", { name: "verdict: print" });
    expect(lamp).toHaveClass("ro-lamp", "ro-lamp--print");
    expect(lamp).toHaveTextContent("PRINT");
  });

  test("hold verdict lights the hold lamp", () => {
    render(<Lamp verdict="hold" />);
    const lamp = screen.getByRole("img", { name: "verdict: hold" });
    expect(lamp).toHaveClass("ro-lamp--hold");
    expect(lamp).toHaveTextContent("HOLD");
  });

  test("fail verdict lights the fail lamp", () => {
    render(<Lamp verdict="fail" />);
    const lamp = screen.getByRole("img", { name: "verdict: fail" });
    expect(lamp).toHaveClass("ro-lamp--fail");
    expect(lamp).toHaveTextContent("FAIL");
  });

  test("a custom word replaces the default text but keeps the semantics", () => {
    render(<Lamp verdict="hold" word="Em holds" />);
    const lamp = screen.getByRole("img", { name: "verdict: hold" });
    expect(lamp).toHaveTextContent("Em holds");
  });
});
