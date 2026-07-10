import "./reelone.css";
import { TC } from "../lib/timecode";

/** The timecode burn-in — frame × hold @ 12fps, mono, screenlight-dim. */
export function Timecode({
  frame,
  hold,
  fps,
}: {
  frame: number;
  hold: number;
  fps?: number;
}) {
  return <span className="ro-tc">{TC(frame, hold, fps)}</span>;
}
