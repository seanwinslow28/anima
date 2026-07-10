import { render, screen } from "@testing-library/react";
import { act } from "react";
import { afterEach, describe, expect, test, vi } from "vitest";

import { Leader } from "./Leader";

// jsdom has no matchMedia; the component treats "no matchMedia" as
// motion-allowed, and tests install one to drive the reduced path.
function stubReducedMotion(matches: boolean) {
  vi.stubGlobal(
    "matchMedia",
    vi.fn().mockReturnValue({ matches, addEventListener: vi.fn(), removeEventListener: vi.fn() }),
  );
}

afterEach(() => {
  vi.unstubAllGlobals();
  vi.useRealTimers();
});

describe("Leader", () => {
  test("renders the countdown dial starting at 3, announced as a working state", () => {
    render(<Leader onDone={() => {}} caption="NEXT PICTURE UP" />);
    const leader = screen.getByRole("status");
    expect(leader).toHaveClass("ro-leader");
    expect(screen.getByText("3")).toBeInTheDocument();
    expect(screen.getByText("NEXT PICTURE UP")).toBeInTheDocument();
  });

  test("sweeps 3-2-1 at ~700ms per count, then fires onDone once", () => {
    vi.useFakeTimers({
      toFake: ["requestAnimationFrame", "cancelAnimationFrame", "performance"],
    });
    const onDone = vi.fn();
    render(<Leader onDone={onDone} />);

    act(() => vi.advanceTimersByTime(750));
    expect(screen.getByText("2")).toBeInTheDocument();
    expect(onDone).not.toHaveBeenCalled();

    act(() => vi.advanceTimersByTime(700));
    expect(screen.getByText("1")).toBeInTheDocument();
    expect(onDone).not.toHaveBeenCalled();

    act(() => vi.advanceTimersByTime(750));
    expect(onDone).toHaveBeenCalledTimes(1);

    // the loop stops — no further frames re-fire it
    act(() => vi.advanceTimersByTime(3000));
    expect(onDone).toHaveBeenCalledTimes(1);
  });

  test("under prefers-reduced-motion it skips the sweep and resolves onDone", () => {
    stubReducedMotion(true);
    const onDone = vi.fn();
    render(<Leader onDone={onDone} />);
    expect(onDone).toHaveBeenCalledTimes(1);
  });
});
