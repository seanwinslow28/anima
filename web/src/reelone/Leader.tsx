import { useEffect, useRef, useState } from "react";

import "./reelone.css";

/**
 * The Academy leader — the 3-2-1 clock-sweep countdown that IS the working
 * state (never a spinner). rAF drives a conic --sweep through 360° per count
 * (~700ms each, the mockup's cadence), then fires onDone; every job's
 * working state reuses this. Under prefers-reduced-motion the sweep is
 * skipped and onDone resolves immediately (the a11y contract).
 */
export function Leader({
  onDone,
  caption = "NEXT PICTURE UP",
  counts = 3,
}: {
  onDone: () => void;
  caption?: string;
  counts?: number;
}) {
  const [n, setN] = useState(counts);
  const dialRef = useRef<HTMLDivElement>(null);
  // keep the latest callback without restarting the sweep on re-render
  const doneRef = useRef(onDone);
  doneRef.current = onDone;

  useEffect(() => {
    const reduced =
      typeof window.matchMedia === "function" &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduced) {
      doneRef.current();
      return;
    }

    let raf = 0;
    let t0: number | null = null;
    let count = counts;
    const sweep = (ts: number) => {
      if (t0 === null) t0 = ts;
      const p = (ts - t0) / 700;
      if (p >= 1) {
        t0 = ts;
        count -= 1;
        if (count < 1) {
          dialRef.current?.style.setProperty("--sweep", "0deg");
          doneRef.current();
          return;
        }
        setN(count);
      }
      dialRef.current?.style.setProperty("--sweep", `${(p % 1) * 360}deg`);
      raf = requestAnimationFrame(sweep);
    };
    raf = requestAnimationFrame(sweep);
    return () => cancelAnimationFrame(raf);
  }, [counts]);

  return (
    <div className="ro-leader" role="status">
      <div className="ro-dial" ref={dialRef}>
        <span className="ro-cross-v" aria-hidden="true" />
        <span className="ro-cross-h" aria-hidden="true" />
        <span className="ro-n">{n}</span>
        <span className="ro-cap">{caption}</span>
      </div>
    </div>
  );
}
