import { screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import App from "./App";
import { renderApp } from "./test/render";

describe("app shell", () => {
  it("renders the whole app inside the .reelone booth (the U0→U1 token thread)", () => {
    const { container } = renderApp(<App />, { route: "/" });
    // Every screen must sit under the `.reelone` scope or U0's tokens
    // (scoped to `.reelone`, not :root) never apply.
    expect(container.firstElementChild).toHaveClass("reelone");
  });

  it("renders the ANIMA wordmark home link and the shell landmarks", () => {
    renderApp(<App />, { route: "/" });

    // The wordmark is a real navigation control (a11y contract), home is "/".
    const home = screen.getByRole("link", { name: /anima/i });
    expect(home).toHaveAttribute("href", "/");
    expect(screen.getByText(/screening room/i)).toBeInTheDocument();
    // Landmarks: one <header> app bar + one <main> stage per screen.
    expect(screen.getByRole("banner")).toBeInTheDocument();
    expect(screen.getByRole("main")).toBeInTheDocument();
  });

  it("routes the Dashboard onto the stage at /", () => {
    renderApp(<App />, { route: "/" });
    expect(screen.getByRole("main")).toContainElement(
      screen.getByRole("heading", { level: 1 }),
    );
  });

  it("keeps /dev/system rendering inside the booth", () => {
    renderApp(<App />, { route: "/dev/system" });
    expect(screen.getByRole("main")).toContainElement(
      screen.getByRole("heading", { level: 1, name: /reel one/i }),
    );
  });
});
