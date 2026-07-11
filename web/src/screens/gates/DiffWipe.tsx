/*
 * The diff-wipe (U5c — "D"): a wipe between two prints — the shown take
 * against another attempt, or against the approved prior frame (both served
 * by the daemon; the "face morphed through the tween" catch). The Bible
 * anchor is NOT a comparator — it isn't served (D-E, G9), and no anchor
 * path exists here by construction. The over layer clips with clip-path so
 * both prints stay registered; [ / ] drag the wipe line and the wipe is
 * ALSO a labelled slider (a11y — never mouse-only).
 */

export interface WipeSource {
  key: string;
  label: string;
  url: string;
}

/** The stage overlay: comparator on the left of the line, the take on the right. */
export function DiffWipe({
  base,
  compare,
  wipe,
}: {
  /** the shown take — the right side */
  base: WipeSource;
  /** the picked comparator — the left side */
  compare: WipeSource;
  /** wipe position, 0–100 (% from the left) */
  wipe: number;
}) {
  return (
    <div className="eg-wipe" data-testid="wipe">
      <div className="eg-wipe-under">
        <img src={base.url} alt={`${base.label} — right of the wipe`} />
      </div>
      <div
        className="eg-wipe-over"
        style={{ clipPath: `inset(0 ${100 - wipe}% 0 0)` }}
      >
        <img src={compare.url} alt={`${compare.label} — left of the wipe`} />
      </div>
      <div
        className="eg-wipe-line"
        style={{ left: `${wipe}%` }}
        aria-hidden="true"
      >
        <span className="eg-wipe-tag">
          {compare.label} ◂ ▸ {base.label}
        </span>
      </div>
    </div>
  );
}

/** The wipe's controls (transport-side): the labelled slider + the picker. */
export function WipeControls({
  options,
  selectedKey,
  onSelect,
  wipe,
  onWipe,
}: {
  options: WipeSource[];
  selectedKey: string;
  onSelect: (key: string) => void;
  wipe: number;
  onWipe: (value: number) => void;
}) {
  const selectedLabel =
    options.find((option) => option.key === selectedKey)?.label ?? "comparison";
  const wipeMeaning =
    wipe === 50
      ? "even split"
      : wipe > 50
        ? `mostly ${selectedLabel}`
        : "mostly the shown take";

  return (
    <div className="eg-wiperow">
      <div className="eg-wipe-pick" role="group" aria-label="Compare against">
        {options.map((o) => (
          <button
            key={o.key}
            type="button"
            className="eg-tsw"
            aria-pressed={o.key === selectedKey}
            onClick={() => onSelect(o.key)}
          >
            {o.label}
          </button>
        ))}
      </div>
      <label className="eg-lbl" htmlFor="eg-wipe-slider">
        Wipe position
      </label>
      <input
        id="eg-wipe-slider"
        type="range"
        min={0}
        max={100}
        value={wipe}
        aria-valuetext={`${wipe}% — ${wipeMeaning}`}
        onChange={(e) => onWipe(Number(e.target.value))}
      />
      <span className="eg-kx" aria-hidden="true">
        [ ]
      </span>
    </div>
  );
}
