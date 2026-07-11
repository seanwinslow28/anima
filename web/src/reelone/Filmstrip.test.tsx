import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, test } from "vitest";

import { Filmstrip, type FilmstripFrame } from "./Filmstrip";
import { ROUTER_FUTURE } from "../test/render";

const FRAMES: FilmstripFrame[] = [
  { id: 1, label: "F01", status: "printed", src: "/f1.png", href: "/frames/1" },
  { id: 2, label: "F02", status: "printed", src: "/f2.png" },
  { id: 3, label: "F03", status: "working", now: true },
  { id: 4, label: "F04", status: "pending" },
];

describe("Filmstrip", () => {
  const renderStrip = (frames = FRAMES) =>
    render(
      <MemoryRouter future={ROUTER_FUTURE}>
        <Filmstrip frames={frames} />
      </MemoryRouter>,
    );

  test("renders one cell per frame as a labelled list", () => {
    renderStrip();
    const strip = screen.getByRole("list", { name: "reel" });
    expect(strip).toHaveClass("ro-strip");
    const cells = screen.getAllByRole("listitem");
    expect(cells).toHaveLength(4);
    cells.forEach((cell) => expect(cell).toHaveClass("ro-sprocket"));
  });

  test("a printed frame shows its image and the print mark", () => {
    renderStrip();
    const cell = screen.getAllByRole("listitem")[0];
    expect(cell).toHaveClass("ro-fcell--linked");
    expect(screen.getByRole("link", { name: /F01/i })).toHaveAttribute(
      "href",
      "/frames/1",
    );
    expect(cell.querySelector("img")).toHaveAttribute("src", "/f1.png");
    expect(cell.textContent).toContain("PRINT");
  });

  test("the working frame pulses and says who's on it", () => {
    renderStrip();
    const cell = screen.getAllByRole("listitem")[2];
    expect(cell.querySelector(".ro-pulse")).not.toBeNull();
    expect(cell.textContent).toContain("WORKING");
  });

  test("the current frame carries the tungsten ring", () => {
    renderStrip();
    const cells = screen.getAllByRole("listitem");
    expect(cells[2]).toHaveClass("ro-fcell--now");
    expect(cells[0]).not.toHaveClass("ro-fcell--now");
  });

  test("a frame without an image renders the dashed empty slot", () => {
    renderStrip();
    const cell = screen.getAllByRole("listitem")[3];
    expect(cell.querySelector("img")).toBeNull();
    expect(cell.querySelector(".ro-empty")).not.toBeNull();
  });

  // U2b additive extension — the eye status (a generated take waiting on the
  // director, tungsten, no pulse) and a per-frame mark override.
  test("an eye frame reads YOUR CALL in tungsten without pulsing", () => {
    renderStrip([{ id: 3, label: "F03", status: "eye", src: "/f3.png", now: true }]);
    const cell = screen.getAllByRole("listitem")[0];
    expect(cell.textContent).toContain("YOUR CALL");
    expect(cell.querySelector(".ro-eye")).not.toBeNull();
    expect(cell.querySelector(".ro-pulse")).toBeNull();
  });

  test("a mark override replaces the default status word", () => {
    renderStrip([{ id: 4, label: "F04", status: "working", mark: "FLO DRAWING" }]);
    const cell = screen.getAllByRole("listitem")[0];
    expect(cell.textContent).toContain("FLO DRAWING");
    expect(cell.textContent).not.toContain("● WORKING");
    expect(cell.querySelector(".ro-pulse")).not.toBeNull();
  });
});
