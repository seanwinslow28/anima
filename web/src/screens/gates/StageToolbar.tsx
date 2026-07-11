/*
 * The stage action bar (U5b) — every eye-gate key's visible button (the a11y
 * discoverability contract; U5a's Run + take buttons live beside these in
 * the transport row). The decision pair (Print it / Go again) is primary;
 * the walk / keys / palette switches stay quiet.
 */

/** Summon U1's ⌘K palette — it listens on window; speak its language. */
function summonPalette() {
  window.dispatchEvent(
    new KeyboardEvent("keydown", { key: "k", metaKey: true, bubbles: true }),
  );
}

export function StageToolbar({
  canPrint,
  onPrint,
  canAgain,
  onAgain,
  prevN,
  nextN,
  onWalk,
  canGhost,
  onionOn,
  onToggleOnion,
  canDiff,
  diffOn,
  onToggleDiff,
  lightsOn,
  onToggleLights,
  cheatOpen,
  onToggleCheat,
}: {
  canPrint: boolean;
  onPrint: () => void;
  canAgain: boolean;
  onAgain: () => void;
  /** Adjacent reviewable frame numbers; null = a dead end (disabled). */
  prevN: number | null;
  nextN: number | null;
  onWalk: (n: number | null) => void;
  /** onion-skin (U5c): a ghost source exists (an approved prior / loop anchor) */
  canGhost: boolean;
  onionOn: boolean;
  onToggleOnion: () => void;
  /** diff-wipe (U5c): a comparator exists (another take / the approved prior) */
  canDiff: boolean;
  diffOn: boolean;
  onToggleDiff: () => void;
  /** lights-out (U5c): the frame alone — the toolbar itself goes with it */
  lightsOn: boolean;
  onToggleLights: () => void;
  cheatOpen: boolean;
  onToggleCheat: () => void;
}) {
  return (
    <>
      <div className="eg-decide" role="group" aria-label="The decision">
        <button
          type="button"
          className="eg-again ro-button ro-button--quiet"
          disabled={!canAgain}
          onClick={onAgain}
        >
          Go again <span className="eg-kx" aria-hidden="true">R</span>
        </button>
        <button
          type="button"
          className="eg-print ro-button ro-button--primary"
          disabled={!canPrint}
          onClick={onPrint}
        >
          Print it <span className="eg-kx" aria-hidden="true">⏎</span>
        </button>
      </div>
      <div className="eg-quiet" role="group" aria-label="Stage controls">
        <button
          type="button"
          className="eg-tsw"
          aria-label="Previous frame (↑)"
          disabled={prevN === null}
          onClick={() => onWalk(prevN)}
        >
          ↑
        </button>
        <button
          type="button"
          className="eg-tsw"
          aria-label="Next frame (↓)"
          disabled={nextN === null}
          onClick={() => onWalk(nextN)}
        >
          ↓
        </button>
        <button
          type="button"
          className="eg-tsw"
          aria-label="Ghost the prior print under the take (O)"
          aria-pressed={onionOn}
          disabled={!canGhost}
          onClick={onToggleOnion}
        >
          Ghost <span className="eg-kx" aria-hidden="true">O</span>
        </button>
        <button
          type="button"
          className="eg-tsw"
          aria-label="Compare takes with a wipe (D)"
          aria-pressed={diffOn}
          disabled={!canDiff}
          onClick={onToggleDiff}
        >
          Wipe <span className="eg-kx" aria-hidden="true">D</span>
        </button>
        <button
          type="button"
          className="eg-tsw"
          aria-label="House lights out, picture only (L)"
          aria-pressed={lightsOn}
          onClick={onToggleLights}
        >
          House lights <span className="eg-kx" aria-hidden="true">L</span>
        </button>
        <button
          type="button"
          className="eg-tsw"
          aria-label="Keys — the cheat-sheet (?)"
          aria-pressed={cheatOpen}
          onClick={onToggleCheat}
        >
          ? <span className="eg-kx" aria-hidden="true">KEYS</span>
        </button>
        <button
          type="button"
          className="eg-tsw"
          aria-label="Command palette (⌘K)"
          onClick={summonPalette}
        >
          ⌘K
        </button>
      </div>
    </>
  );
}
