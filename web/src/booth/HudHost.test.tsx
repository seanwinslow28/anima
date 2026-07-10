import { fireEvent, render, screen } from "@testing-library/react";
import { act } from "react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { renderApp } from "../test/render";
import { BoothShell } from "./BoothShell";
import { HudHost, useDimLevel, useHud } from "./HudHost";

// jsdom has no matchMedia; the provider treats "no matchMedia" as
// motion-allowed, and tests install one to drive the reduced path
// (the U0 Leader pattern).
function stubReducedMotion(matches: boolean) {
  vi.stubGlobal(
    "matchMedia",
    vi.fn().mockReturnValue({ matches, addEventListener: vi.fn(), removeEventListener: vi.fn() }),
  );
}

/** A chrome consumer that reports the provider's state. */
function Probe() {
  const { chromeHidden, dimLevel } = useHud();
  return <div data-testid="probe" data-hidden={chromeHidden} data-dim={dimLevel} />;
}

afterEach(() => {
  vi.unstubAllGlobals();
  vi.useRealTimers();
});

describe("HudHost idle-wake", () => {
  it("hides the chrome after ~3s idle and wakes it on mousemove", () => {
    vi.useFakeTimers();
    render(
      <HudHost>
        <Probe />
      </HudHost>,
    );
    const probe = screen.getByTestId("probe");
    expect(probe).toHaveAttribute("data-hidden", "false");

    act(() => vi.advanceTimersByTime(3000));
    expect(probe).toHaveAttribute("data-hidden", "true");

    act(() => {
      fireEvent.mouseMove(window);
    });
    expect(probe).toHaveAttribute("data-hidden", "false");
  });

  it("wakes on keydown too, and re-idles after another idle period", () => {
    vi.useFakeTimers();
    render(
      <HudHost>
        <Probe />
      </HudHost>,
    );
    const probe = screen.getByTestId("probe");

    act(() => vi.advanceTimersByTime(3000));
    expect(probe).toHaveAttribute("data-hidden", "true");

    act(() => {
      fireEvent.keyDown(window, { key: "j" });
    });
    expect(probe).toHaveAttribute("data-hidden", "false");

    act(() => vi.advanceTimersByTime(3000));
    expect(probe).toHaveAttribute("data-hidden", "true");
  });

  it("under prefers-reduced-motion the chrome never times out", () => {
    stubReducedMotion(true);
    vi.useFakeTimers();
    render(
      <HudHost>
        <Probe />
      </HudHost>,
    );
    const probe = screen.getByTestId("probe");

    act(() => vi.advanceTimersByTime(10000));
    expect(probe).toHaveAttribute("data-hidden", "false");
  });
});

describe("HudHost dim-level api", () => {
  it("defaults to the density level", () => {
    render(
      <HudHost>
        <Probe />
      </HudHost>,
    );
    expect(screen.getByTestId("probe")).toHaveAttribute("data-dim", "density");
  });

  it("a screen can declare full (reserved for the eye-gate) and it releases on unmount", () => {
    function FullDimScreen() {
      useDimLevel("full");
      return <p>the stage</p>;
    }
    const { rerender } = render(
      <HudHost>
        <Probe />
        <FullDimScreen />
      </HudHost>,
    );
    expect(screen.getByTestId("probe")).toHaveAttribute("data-dim", "full");

    rerender(
      <HudHost>
        <Probe />
      </HudHost>,
    );
    expect(screen.getByTestId("probe")).toHaveAttribute("data-dim", "density");
  });
});

describe("BoothShell under the HUD", () => {
  it("fades only the shell chrome on idle — never the stage's primary content", () => {
    vi.useFakeTimers();
    renderApp(
      <BoothShell>
        <p>primary content</p>
      </BoothShell>,
    );

    act(() => vi.advanceTimersByTime(3000));

    // The app bar sits inside the fading HUD layer…
    const banner = screen.getByRole("banner");
    expect(banner.closest(".booth-hud")).toHaveClass("booth-hud--idle");
    // …the <main> stage does not: the room disappears, the work never does.
    const main = screen.getByRole("main");
    expect(main.closest(".booth-hud")).toBeNull();

    act(() => {
      fireEvent.mouseMove(window);
    });
    expect(banner.closest(".booth-hud")).not.toHaveClass("booth-hud--idle");
  });
});
