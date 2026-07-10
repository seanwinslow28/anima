import { screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { renderApp } from "../test/render";
import { BoothShell } from "./BoothShell";

describe("BoothShell", () => {
  it("carries the .reelone class at its root so U0's scoped tokens apply", () => {
    // THE load-bearing U0→U1 thread: tokens are scoped to `.reelone`, not
    // :root — without this class on the shell root, the whole app renders
    // unstyled booth-wise.
    const { container } = renderApp(
      <BoothShell>
        <p>stage content</p>
      </BoothShell>,
    );
    const root = container.firstElementChild;
    expect(root).not.toBeNull();
    expect(root).toHaveClass("reelone");
  });

  it("renders the booth chrome: film grain, a banner landmark, and the stage <main>", () => {
    renderApp(
      <BoothShell>
        <p>stage content</p>
      </BoothShell>,
    );
    // Film grain is pure texture — present but hidden from assistive tech.
    expect(document.querySelector(".ro-grain")).not.toBeNull();
    expect(document.querySelector(".ro-grain")).toHaveAttribute("aria-hidden", "true");
    // Landmarks: <header> (app bar) + <main> (the stage).
    expect(screen.getByRole("banner")).toBeInTheDocument();
    expect(screen.getByRole("main")).toBeInTheDocument();
    // Routed children render inside the stage.
    expect(screen.getByRole("main")).toContainElement(screen.getByText("stage content"));
  });

  it("re-skins the wordmark: ANIMA home link with the screening-room sub", () => {
    renderApp(
      <BoothShell>
        <p>stage content</p>
      </BoothShell>,
    );
    const home = screen.getByRole("link", { name: /anima/i });
    expect(home).toHaveAttribute("href", "/");
    expect(screen.getByText(/screening room/i)).toBeInTheDocument();
  });
});
