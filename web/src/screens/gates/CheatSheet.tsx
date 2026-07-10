/*
 * The ? cheat-sheet (U5b; completed U5c) — the discoverability backstop. A
 * reference card over the stage listing every eye-gate key that exists today
 * — the COMPLETE v1b map. Not a modal: the stage keeps focus; ? or Esc puts
 * it away.
 */

const KEYS: ReadonlyArray<{ k: string; does: string }> = [
  { k: "⏎", does: "Print it — approve the shown take; the next picture comes up" },
  { k: "R", does: "Go again — send it back with a note (Em pre-fills)" },
  { k: "SPACE", does: "Run the loop (hold to rock, release to judge)" },
  { k: "1 2", does: "Switch takes" },
  { k: "↑ ↓", does: "Walk frames (reviewable stops only)" },
  { k: "O", does: "Ghost the previous print (and the loop anchor) under the take" },
  { k: "?", does: "This sheet" },
  { k: "⌘K", does: "Command palette" },
];

export function CheatSheet({ open }: { open: boolean }) {
  if (!open) return null;
  return (
    <div className="eg-cheat" role="dialog" aria-label="Keys">
      <p className="eg-lbl">The keys · ? or Esc puts this away</p>
      <dl className="eg-cheat-list">
        {KEYS.map(({ k, does }) => (
          <div key={k} className="eg-cheat-row">
            <dt>
              <kbd className="eg-kx">{k}</kbd>
            </dt>
            <dd>{does}</dd>
          </div>
        ))}
      </dl>
    </div>
  );
}
