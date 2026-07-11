import "./reelone.css";

import { Link } from "react-router-dom";

export type FilmstripFrame = {
  id: string | number;
  /** the cell caption, e.g. "F03" */
  label: string;
  /** eye = a generated take waiting on the director (tungsten, no pulse) */
  status: "printed" | "working" | "eye" | "pending";
  /** override the default status word (e.g. "FLO DRAWING") — U2b additive */
  mark?: string;
  /** thumbnail — absent renders the dashed empty slot */
  src?: string;
  /** the current frame (tungsten ring) */
  now?: boolean;
  /** optional navigation target; only these cells earn hover warmth */
  href?: string;
};

const STATUS_MARK: Record<FilmstripFrame["status"], string> = {
  printed: "✓ PRINT",
  working: "● WORKING",
  eye: "YOUR CALL",
  pending: "",
};

const STATUS_CLASS: Record<FilmstripFrame["status"], string> = {
  printed: "ro-printed",
  working: "ro-working ro-pulse",
  eye: "ro-eye",
  pending: "",
};

/**
 * The reel ledger — one sprocketed cell per frame, status as a colored mark
 * in the cap row (print-green check, pulsing tungsten working dot, steady
 * tungsten eye), the current frame ringed. Presentational: the consumer
 * supplies the frames. Optional hover-skim hooks (U5c): a cell under the
 * mouse reports itself so the eye-gate can peek it on the stage.
 */
export function Filmstrip({
  frames,
  onPeek,
  onPeekEnd,
}: {
  frames: FilmstripFrame[];
  onPeek?: (id: FilmstripFrame["id"]) => void;
  onPeekEnd?: () => void;
}) {
  return (
    <ul className="ro-strip" aria-label="reel">
      {frames.map((f) => {
        const content = (
          <>
            {f.src ? (
              <img src={f.src} alt={`frame ${f.label}`} />
            ) : (
              <div className="ro-empty">{f.status === "working" ? "on the bench" : "not yet drawn"}</div>
            )}
            <div className="ro-cap">
              <span>{f.label}</span>
              {(f.status !== "pending" || f.mark) && (
                <span className={STATUS_CLASS[f.status]}>
                  {f.mark ?? STATUS_MARK[f.status]}
                </span>
              )}
            </div>
          </>
        );
        return (
          <li
            key={f.id}
            className={[
              "ro-fcell ro-sprocket",
              f.now ? "ro-fcell--now" : "",
              f.href ? "ro-fcell--linked" : "",
            ].filter(Boolean).join(" ")}
            onMouseEnter={onPeek ? () => onPeek(f.id) : undefined}
            onMouseLeave={onPeekEnd}
          >
            {f.href ? (
              <Link className="ro-fcell-hit" to={f.href}>{content}</Link>
            ) : (
              <div className="ro-fcell-hit">{content}</div>
            )}
          </li>
        );
      })}
    </ul>
  );
}
