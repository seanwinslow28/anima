import { useEffect, useState } from "react";

/** A one-shot async read: loading -> ready | error. Shared by both screens. */
export type Resource<T> =
  | { status: "loading" }
  | { status: "error"; error: Error }
  | { status: "ready"; data: T };

/**
 * Run `fetcher` when `deps` change, tracking loading/ready/error. `nonce` (bumped
 * by a retry) re-runs the same fetch. Stale results are dropped on unmount /
 * dep-change so a slow response can't overwrite a newer one.
 */
export function useResource<T>(
  fetcher: () => Promise<T>,
  deps: readonly unknown[],
): Resource<T> {
  const [state, setState] = useState<Resource<T>>({ status: "loading" });

  useEffect(() => {
    let alive = true;
    setState({ status: "loading" });
    fetcher().then(
      (data) => alive && setState({ status: "ready", data }),
      (error: unknown) =>
        alive &&
        setState({
          status: "error",
          error: error instanceof Error ? error : new Error(String(error)),
        }),
    );
    return () => {
      alive = false;
    };
    // fetcher is re-created each render; deps are the real trigger.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);

  return state;
}
