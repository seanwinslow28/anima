import { render, screen } from "@testing-library/react";
import { describe, expect, test } from "vitest";

import { Filmstrip, type FilmstripFrame } from "./Filmstrip";

const FRAMES: FilmstripFrame[] = [
  { id: 1, label: "F01", status: "printed", src: "/f1.png" },
  { id: 2, label: "F02", status: "printed", src: "/f2.png" },
  { id: 3, label: "F03", status: "working", now: true },
  { id: 4, label: "F04", status: "pending" },
];

describe("Filmstrip", () => {
  test("renders one cell per frame as a labelled list", () => {
    render(<Filmstrip frames={FRAMES} />);
    const strip = screen.getByRole("list", { name: "reel" });
    expect(strip).toHaveClass("ro-strip");
    expect(screen.getAllByRole("listitem")).toHaveLength(4);
  });

  test("a printed frame shows its image and the print mark", () => {
    render(<Filmstrip frames={FRAMES} />);
    const cell = screen.getAllByRole("listitem")[0];
    expect(cell.querySelector("img")).toHaveAttribute("src", "/f1.png");
    expect(cell.textContent).toContain("PRINT");
  });

  test("the working frame pulses and says who's on it", () => {
    render(<Filmstrip frames={FRAMES} />);
    const cell = screen.getAllByRole("listitem")[2];
    expect(cell.querySelector(".ro-pulse")).not.toBeNull();
    expect(cell.textContent).toContain("WORKING");
  });

  test("the current frame carries the tungsten ring", () => {
    render(<Filmstrip frames={FRAMES} />);
    const cells = screen.getAllByRole("listitem");
    expect(cells[2]).toHaveClass("ro-fcell--now");
    expect(cells[0]).not.toHaveClass("ro-fcell--now");
  });

  test("a frame without an image renders the dashed empty slot", () => {
    render(<Filmstrip frames={FRAMES} />);
    const cell = screen.getAllByRole("listitem")[3];
    expect(cell.querySelector("img")).toBeNull();
    expect(cell.querySelector(".ro-empty")).not.toBeNull();
  });
});
