import { screen } from "@testing-library/react";
import { describe, expect, test, vi } from "vitest";

import App from "../../App";
import { renderApp } from "../../test/render";

// The living token sheet — U0's demoable proof, mounted at /dev/system.
// A reference, not a screen: it binds no run data.
describe("/dev/system", () => {
  test("mounts the system sheet inside the booth scope", () => {
    renderApp(<App />, { route: "/dev/system" });
    expect(
      screen.getByRole("heading", { level: 1, name: /reel one/i }),
    ).toBeInTheDocument();
    expect(document.querySelector(".reelone")).not.toBeNull();
  });

  test("renders the palette swatches, the lamps, and a live leader", () => {
    vi.stubGlobal(
      "matchMedia",
      vi.fn().mockReturnValue({ matches: false, addEventListener: vi.fn(), removeEventListener: vi.fn() }),
    );
    renderApp(<App />, { route: "/dev/system" });
    // palette
    expect(screen.getByText(/--booth #141018/)).toBeInTheDocument();
    expect(screen.getByText(/--tungsten #E8B36A/)).toBeInTheDocument();
    // lamps
    expect(screen.getByRole("img", { name: "verdict: print" })).toBeInTheDocument();
    // two hold lamps: the default word + the custom-word variant
    expect(screen.getAllByRole("img", { name: "verdict: hold" })).toHaveLength(2);
    expect(screen.getByRole("img", { name: "verdict: fail" })).toBeInTheDocument();
    // the live leader (working state) + the reel
    expect(
      screen.getAllByRole("status").find((node) => node.classList.contains("ro-leader")),
    ).toHaveClass("ro-leader");
    expect(screen.getByRole("list", { name: "reel" })).toBeInTheDocument();
    vi.unstubAllGlobals();
  });

  test("renders the P3a token additions, rgb mechanism, and button recipe", () => {
    renderApp(<App />, { route: "/dev/system" });

    for (const token of [
      "--booth-deep #0B080D",
      "--sprocket #241D2C",
      "--on-tungsten #101010",
      "--tungsten-bright #F2C284",
      "--stage-edge #2B2333",
      "--tungsten-rgb 232, 179, 106",
    ]) {
      expect(screen.getByText(new RegExp(token))).toBeInTheDocument();
    }

    expect(screen.getByRole("button", { name: "Primary action" })).toHaveClass(
      "ro-button",
      "ro-button--primary",
    );
    expect(screen.getByRole("button", { name: "Quiet action" })).toHaveClass(
      "ro-button",
      "ro-button--quiet",
    );
    expect(screen.getByRole("button", { name: "Danger action" })).toHaveClass(
      "ro-button",
      "ro-button--danger",
    );
  });
});
