import { act, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { callIntercom, Intercom, INTERCOM_DISMISS_MS } from "./Intercom";

describe("Intercom", () => {
  afterEach(() => vi.useRealTimers());

  it("announces politely, remains readable for the full call, then auto-dismisses", () => {
    vi.useFakeTimers();
    render(<Intercom />);

    act(() => callIntercom("GO AGAIN — note sent as a correction. Flo re-shoots F04."));
    const line = screen.getByRole("status");
    expect(line).toHaveAttribute("aria-live", "polite");
    expect(line).toHaveTextContent("GO AGAIN");

    act(() => vi.advanceTimersByTime(INTERCOM_DISMISS_MS - 1));
    expect(line).toHaveTextContent("GO AGAIN");

    act(() => vi.advanceTimersByTime(1));
    expect(line).toBeEmptyDOMElement();
    expect(line).not.toHaveClass("ro-intercom--called");
  });
});
