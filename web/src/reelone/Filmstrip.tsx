import "./reelone.css";

export type FilmstripFrame = {
  id: string | number;
  /** the cell caption, e.g. "F03" */
  label: string;
  status: "printed" | "working" | "pending";
  /** thumbnail — absent renders the dashed empty slot */
  src?: string;
  /** the current frame (tungsten ring) */
  now?: boolean;
};

const STATUS_MARK: Record<FilmstripFrame["status"], string> = {
  printed: "✓ PRINT",
  working: "● WORKING",
  pending: "",
};

/**
 * The reel ledger — one sprocketed cell per frame, status as a colored mark
 * in the cap row (print-green check, pulsing tungsten working dot), the
 * current frame ringed. Presentational: the consumer supplies the frames.
 */
export function Filmstrip({ frames }: { frames: FilmstripFrame[] }) {
  return (
    <ul className="ro-strip" aria-label="reel">
      {frames.map((f) => (
        <li
          key={f.id}
          className={f.now ? "ro-fcell ro-fcell--now" : "ro-fcell"}
        >
          {f.src ? (
            <img src={f.src} alt={`frame ${f.label}`} />
          ) : (
            <div className="ro-empty">{f.status === "working" ? "on the bench" : "not yet drawn"}</div>
          )}
          <div className="ro-cap">
            <span>{f.label}</span>
            {f.status !== "pending" && (
              <span
                className={
                  f.status === "printed" ? "ro-printed" : "ro-working ro-pulse"
                }
              >
                {STATUS_MARK[f.status]}
              </span>
            )}
          </div>
        </li>
      ))}
    </ul>
  );
}
