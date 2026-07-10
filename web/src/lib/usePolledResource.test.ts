import { renderHook, waitFor } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { usePolledResource } from "./usePolledResource";

/*
 * The generic interval-poll variant of useResource. Injected fetcher (no MSW
 * needed here — the api layer has its own tests): poll until the predicate
 * says terminal, then stop; idle while disabled; error stops the loop;
 * unmount/dep-change cleans up.
 */

const tick = { intervalMs: 5 };

describe("usePolledResource", () => {
  it("is idle while disabled and never calls the fetcher", async () => {
    const fetcher = vi.fn(() => Promise.resolve(1));
    const { result } = renderHook(() =>
      usePolledResource(fetcher, { ...tick, until: () => true, enabled: false }, []),
    );
    expect(result.current).toEqual({ status: "idle" });
    await new Promise((r) => setTimeout(r, 20));
    expect(fetcher).not.toHaveBeenCalled();
  });

  it("polls until the predicate is true, then stops", async () => {
    let n = 0;
    const fetcher = vi.fn(() => Promise.resolve(++n));
    const { result } = renderHook(() =>
      usePolledResource(fetcher, { ...tick, until: (v: number) => v >= 3 }, []),
    );
    await waitFor(() => {
      expect(result.current).toEqual({ status: "ready", data: 3 });
    });
    const calls = fetcher.mock.calls.length;
    await new Promise((r) => setTimeout(r, 30));
    expect(fetcher.mock.calls.length).toBe(calls); // terminal -> no more polls
  });

  it("surfaces each intermediate poll as ready data", async () => {
    let n = 0;
    const seen: number[] = [];
    const fetcher = () => Promise.resolve(++n);
    // record every render, not waitFor samples — the intermediate poll must render
    renderHook(() => {
      const res = usePolledResource(fetcher, { ...tick, until: (v: number) => v >= 2 }, []);
      if (res.status === "ready" && !seen.includes(res.data)) seen.push(res.data);
      return res;
    });
    await waitFor(() => expect(seen).toContain(2));
    expect(seen).toContain(1); // the running poll was visible, not swallowed
  });

  it("a rejected poll becomes the error state and stops the loop", async () => {
    const fetcher = vi.fn(() => Promise.reject(new Error("GET /jobs/x failed (404)")));
    const { result } = renderHook(() =>
      usePolledResource(fetcher, { ...tick, until: () => false }, []),
    );
    await waitFor(() => {
      expect(result.current.status).toBe("error");
    });
    const calls = fetcher.mock.calls.length;
    await new Promise((r) => setTimeout(r, 30));
    expect(fetcher.mock.calls.length).toBe(calls);
  });

  it("unmount stops the loop", async () => {
    const fetcher = vi.fn(() => Promise.resolve(0));
    const { unmount } = renderHook(() =>
      usePolledResource(fetcher, { ...tick, until: () => false }, []),
    );
    await waitFor(() => expect(fetcher).toHaveBeenCalled());
    unmount();
    const calls = fetcher.mock.calls.length;
    await new Promise((r) => setTimeout(r, 30));
    expect(fetcher.mock.calls.length).toBe(calls);
  });

  it("flipping enabled back off returns to idle", async () => {
    const fetcher = () => Promise.resolve(1);
    const { result, rerender } = renderHook(
      ({ enabled }: { enabled: boolean }) =>
        usePolledResource(fetcher, { ...tick, until: () => true, enabled }, []),
      { initialProps: { enabled: true } },
    );
    await waitFor(() => expect(result.current.status).toBe("ready"));
    rerender({ enabled: false });
    expect(result.current).toEqual({ status: "idle" });
  });

  it("a dep change restarts the poll against the new target", async () => {
    const fetcher = vi.fn((id: string) => Promise.resolve(id));
    const { result, rerender } = renderHook(
      ({ id }: { id: string }) =>
        usePolledResource(() => fetcher(id), { ...tick, until: () => true }, [id]),
      { initialProps: { id: "a" } },
    );
    await waitFor(() => expect(result.current).toEqual({ status: "ready", data: "a" }));
    rerender({ id: "b" });
    await waitFor(() => expect(result.current).toEqual({ status: "ready", data: "b" }));
  });
});
