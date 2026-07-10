import { useCallback, useEffect, useRef, useState } from "react";

/*
 * The rock/flip loop (U5a — the eye-gate's sacred act): hold to run the
 * frame's loop context at 12fps STEPPED (83ms, the flat-cadence step — never
 * an ease), release to freeze back on the take and judge. You judge animation
 * in motion, never as a still. Under prefers-reduced-motion the run collapses
 * to a single hand-step per press — the flip-book turned by hand.
 */

/** One cel of the loop context: an approved neighbor, or the shown take. */
export interface LoopEntry {
  n: number;
  hold: number | null;
  url: string;
}

const STEP_MS = 83; // 1000/12, the pipeline's frame rate, stepped

function reducedMotion(): boolean {
  // jsdom has no matchMedia; its absence reads as motion-allowed (U0 pattern)
  return (
    typeof window.matchMedia === "function" &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches
  );
}

/**
 * Drive the loop over `entries` (frame order), `currentIndex` = the frame
 * under review. `playhead` is the cel on screen — null means frozen on the
 * shown take (the resting state).
 */
export function useRockLoop(entries: LoopEntry[], currentIndex: number) {
  const [playIdx, setPlayIdx] = useState<number | null>(null);
  const [running, setRunning] = useState(false);
  const timer = useRef<ReturnType<typeof setInterval> | null>(null);

  const clear = () => {
    if (timer.current !== null) {
      clearInterval(timer.current);
      timer.current = null;
    }
  };

  const start = useCallback(() => {
    if (entries.length < 2) return; // nothing to rock against
    if (reducedMotion()) {
      // a single hand-step that STAYS — release must not erase it
      setPlayIdx((prev) => ((prev ?? currentIndex) + 1) % entries.length);
      return;
    }
    if (timer.current !== null) return; // already rocking (key repeat)
    setRunning(true);
    setPlayIdx(currentIndex);
    timer.current = setInterval(() => {
      setPlayIdx((prev) => ((prev ?? currentIndex) + 1) % entries.length);
    }, STEP_MS);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [entries, currentIndex]);

  const stop = useCallback(() => {
    if (reducedMotion()) return; // a step is not a run; nothing to release
    clear();
    setRunning(false);
    setPlayIdx(null); // freeze on the shown take
  }, []);

  // the loop context changed (take switch, a frame approved): reset cold
  const key = entries.map((e) => e.url).join("\n");
  useEffect(() => {
    clear();
    setRunning(false);
    setPlayIdx(null);
  }, [key]);

  useEffect(() => clear, []); // unmount

  const playhead =
    playIdx === null ? null : (entries[playIdx] ?? null);

  return { running, playhead, start, stop };
}
