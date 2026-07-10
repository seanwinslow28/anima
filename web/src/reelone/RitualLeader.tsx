import { useState } from "react";

import { Leader } from "./Leader";

import "./reelone.css";

/**
 * The job's working state: U0's Academy leader run as a RITUAL TIMER (D-C).
 * The 3-2-1 sweep re-arms every time it lands — it loops until the real
 * terminal signal unmounts it, so it can never "complete" ahead of the job
 * (it is not an ETA; the daemon offers no progress %). Under
 * prefers-reduced-motion the sweep would resolve instantly and remount
 * forever, so it holds a STILL working dial instead (announced, no motion).
 */
export function RitualLeader({ caption = "IN THE GATE" }: { caption?: string }) {
  const [cycle, setCycle] = useState(0);

  const reduced =
    typeof window.matchMedia === "function" &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (reduced) {
    return (
      <div className="ro-leader" role="status">
        <div className="ro-dial">
          <span className="ro-cross-v" aria-hidden="true" />
          <span className="ro-cross-h" aria-hidden="true" />
          <span className="ro-n">3</span>
          <span className="ro-cap">{caption}</span>
        </div>
      </div>
    );
  }

  // key remounts the Leader when a sweep lands -> the count re-arms.
  return (
    <Leader key={cycle} caption={caption} onDone={() => setCycle((c) => c + 1)} />
  );
}
