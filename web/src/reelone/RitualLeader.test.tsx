import { render, screen } from "@testing-library/react";
import { act } from "react";
import { afterEach, describe, expect, test, vi } from "vitest";

import { RitualLeader } from "./RitualLeader";

// jsdom has no matchMedia; tests install one to drive the reduced path.
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

describe("RitualLeader — the job's working state", () => {
  test("is a ritual timer: the 3-2-1 loops and NEVER completes on its own", () => {
    vi.useFakeTimers({
      toFake: ["requestAnimationFrame", "cancelAnimationFrame", "performance"],
    });
    render(<RitualLeader caption="PRINTING" />);
    expect(screen.getByRole("status")).toBeInTheDocument();
    expect(screen.getByText("3")).toBeInTheDocument();

    // ride past a full 3-2-1 sweep (~2.1s) several times over — the leader
    // must still be up and counting (it re-arms; only the real terminal
    // signal, i.e. unmount by the flow, ends it).
    act(() => vi.advanceTimersByTime(2500));
    expect(screen.getByRole("status")).toBeInTheDocument();
    act(() => vi.advanceTimersByTime(5000));
    expect(screen.getByRole("status")).toBeInTheDocument();
    expect(screen.getByText(/[123]/)).toBeInTheDocument();
  });

  test("under prefers-reduced-motion it holds a still working dial (no busy remount loop)", () => {
    stubReducedMotion(true);
    render(<RitualLeader caption="PRINTING" />);
    const dial = screen.getByRole("status");
    expect(dial).toBeInTheDocument();
    expect(screen.getByText("PRINTING")).toBeInTheDocument();
  });
});
