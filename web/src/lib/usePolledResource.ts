import { useEffect, useRef, useState } from "react";

import type { Resource } from "./useResource";

/** useResource's shape + "idle" for a poll that isn't switched on. */
export type PolledResource<T> = { status: "idle" } | Resource<T>;

/**
 * The interval-poll variant of useResource (D-D: extend the hand-rolled
 * spine, no data library). Runs `fetcher` immediately, then again every
 * `intervalMs` until `until(data)` says terminal — a setTimeout chain, so
 * polls never overlap. Every intermediate poll surfaces as ready data (the
 * working state renders from it). A rejected poll becomes the error state
 * and stops the loop. Cleanup on unmount / dep-change / enabled-flip; stale
 * responses are dropped.
 */
export function usePolledResource<T>(
  fetcher: () => Promise<T>,
  {
    until,
    intervalMs = 1000,
    enabled = true,
  }: {
    until: (data: T) => boolean;
    intervalMs?: number;
    enabled?: boolean;
  },
  deps: readonly unknown[],
): PolledResource<T> {
  const [state, setState] = useState<PolledResource<T>>(
    enabled ? { status: "loading" } : { status: "idle" },
  );
  // latest callbacks without restarting the loop on re-render
  const fetcherRef = useRef(fetcher);
  fetcherRef.current = fetcher;
  const untilRef = useRef(until);
  untilRef.current = until;

  useEffect(() => {
    if (!enabled) {
      setState({ status: "idle" });
      return;
    }
    let alive = true;
    let timer: ReturnType<typeof setTimeout> | null = null;
    setState({ status: "loading" });

    const tick = () => {
      fetcherRef.current().then(
        (data) => {
          if (!alive) return;
          setState({ status: "ready", data });
          if (!untilRef.current(data)) {
            timer = setTimeout(tick, intervalMs);
          }
        },
        (error: unknown) => {
          if (!alive) return;
          setState({
            status: "error",
            error: error instanceof Error ? error : new Error(String(error)),
          });
        },
      );
    };
    tick();

    return () => {
      alive = false;
      if (timer !== null) clearTimeout(timer);
    };
    // deps are the poll target's identity; fetcher/until ride the refs.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [enabled, intervalMs, ...deps]);

  return state;
}
