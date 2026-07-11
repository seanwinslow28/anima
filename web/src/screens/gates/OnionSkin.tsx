/*
 * The onion-skin ghost layer (U5c — "O"): the approved N-1 (and, on a
 * loop-return, the chain_from anchor) rendered over the candidate at low
 * opacity so the eye judges whether the character HOLDS and the loop closes.
 * THE TWO-REDS RULE: the ghost treatment (eyegate.css .eg-ghost) is
 * cool/tungsten-dim — never print-green or hold-amber; the stage keeps one
 * reserved warning hue and the lamp semantics stay unambiguous. A judgment
 * aid, not content: the whole layer is aria-hidden.
 */

export interface GhostSource {
  n: number;
  url: string;
  /** the corner tag — "N-1" for the previous print, "LOOP" for the anchor */
  role: "N-1" | "LOOP";
}

const pad = (n: number) => `F${String(n).padStart(2, "0")}`;

export function OnionSkin({ ghosts }: { ghosts: GhostSource[] }) {
  if (ghosts.length === 0) return null;
  return (
    <div className="eg-onion" aria-hidden="true" data-testid="onion">
      {ghosts.map((g) => (
        <div key={g.n} className="eg-ghostcell">
          <img className="eg-ghost" src={g.url} alt="" />
          <span className="eg-ghost-tag">
            {g.role} · {pad(g.n)}
          </span>
        </div>
      ))}
    </div>
  );
}
