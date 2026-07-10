import { fireEvent, screen } from "@testing-library/react";
import { Route, Routes } from "react-router-dom";
import { describe, expect, it } from "vitest";

import { renderApp } from "../test/render";
import { BoothShell } from "./BoothShell";
import { CommandPalette } from "./CommandPalette";

/** The palette next to a tiny route table so navigation is observable. */
function Harness() {
  return (
    <>
      <CommandPalette />
      <button>outside control</button>
      <Routes>
        <Route path="/" element={<p>home screen</p>} />
        <Route path="/dev/system" element={<p>system screen</p>} />
      </Routes>
    </>
  );
}

function openPalette() {
  fireEvent.keyDown(window, { key: "k", metaKey: true });
}

describe("CommandPalette", () => {
  it("is closed by default and opens on ⌘K as a labelled modal dialog", () => {
    renderApp(<Harness />);
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();

    openPalette();
    const dialog = screen.getByRole("dialog", { name: /command palette/i });
    expect(dialog).toHaveAttribute("aria-modal", "true");
  });

  it("opens on Ctrl+K too, and ⌘K toggles it closed again", () => {
    renderApp(<Harness />);
    fireEvent.keyDown(window, { key: "k", ctrlKey: true });
    expect(screen.getByRole("dialog")).toBeInTheDocument();

    openPalette();
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
  });

  it("lists the static nav targets in a listbox and traps focus on it", () => {
    renderApp(<Harness />);
    openPalette();

    const listbox = screen.getByRole("listbox");
    expect(document.activeElement).toBe(listbox);
    expect(screen.getByRole("option", { name: "Dashboard" })).toBeInTheDocument();
    expect(screen.getByRole("option", { name: "Design system" })).toBeInTheDocument();

    // Tab does not escape the dialog — the palette is the only focus stop.
    fireEvent.keyDown(listbox, { key: "Tab" });
    expect(document.activeElement).toBe(listbox);
  });

  it("arrow keys move the active option; Enter navigates and closes", () => {
    renderApp(<Harness />, { route: "/" });
    openPalette();

    const listbox = screen.getByRole("listbox");
    expect(screen.getByRole("option", { name: "Dashboard" })).toHaveAttribute(
      "aria-selected",
      "true",
    );

    fireEvent.keyDown(listbox, { key: "ArrowDown" });
    expect(screen.getByRole("option", { name: "Design system" })).toHaveAttribute(
      "aria-selected",
      "true",
    );

    fireEvent.keyDown(listbox, { key: "Enter" });
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
    expect(screen.getByText("system screen")).toBeInTheDocument();
  });

  it("clicking an option navigates and closes", () => {
    renderApp(<Harness />, { route: "/" });
    openPalette();

    fireEvent.click(screen.getByRole("option", { name: "Design system" }));
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
    expect(screen.getByText("system screen")).toBeInTheDocument();
  });

  it("Esc closes and returns focus to the previously focused element", () => {
    renderApp(<Harness />);
    const outside = screen.getByRole("button", { name: "outside control" });
    outside.focus();

    openPalette();
    expect(document.activeElement).not.toBe(outside);

    fireEvent.keyDown(screen.getByRole("listbox"), { key: "Escape" });
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
    expect(document.activeElement).toBe(outside);
  });

  it("is a shell capability: ⌘K opens it from inside the BoothShell", () => {
    renderApp(
      <BoothShell>
        <p>stage content</p>
      </BoothShell>,
    );
    openPalette();
    expect(screen.getByRole("dialog", { name: /command palette/i })).toBeInTheDocument();
  });
});
