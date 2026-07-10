import type { EmVerdict } from "../../api/types";
import { Lamp, type LampVerdict } from "../../reelone/Lamp";

/*
 * Em as a hand in the margin (U5a) — the read-out beside the frame. Four
 * fixed slots per cast namespace: verdict (a <Lamp> BEFORE the words),
 * reasoning, the proposed fix (displayed here; prefilling the retry note is
 * U5b), and cites — rendering the /candidates Em payload as-is. Her honest
 * boundary is stated in-context: she reads stills, not motion.
 */

/** Map Em's open verdict vocabulary onto the reserved lamp hues. */
export function lampForVerdict(verdict: string): {
  lamp: LampVerdict;
  word: string;
} {
  if (verdict === "pass") return { lamp: "print", word: "PRINT" };
  if (verdict === "flag") return { lamp: "hold", word: "HOLD" };
  // human_review… and anything else Em says: the reserved warning hue,
  // her own word spelled out
  return { lamp: "fail", word: verdict.replace(/_/g, " ").toUpperCase() };
}

/** A grease-pencil margin stroke — pure decoration, hidden from the reader. */
function GreaseMark() {
  return (
    <svg
      className="eg-grease"
      aria-hidden="true"
      viewBox="0 0 46 8"
      focusable="false"
    >
      <path
        d="M2 5 C 12 2, 30 8, 44 3"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.4"
        strokeLinecap="round"
      />
    </svg>
  );
}

/** The margin rail: one card per cast namespace + the boundary line. */
export function EmReadout({ records }: { records: EmVerdict[] }) {
  return (
    <aside
      className="eg-rail"
      aria-label="Notes from the back row"
      aria-live="polite"
    >
      {records.length === 0 ? (
        <p className="eg-nonote">No note from the back row on this take.</p>
      ) : (
        records.map((em) => <EmCard key={em.character} em={em} />)
      )}
      <p className="eg-bound">
        She reads stills, not motion — the loop is yours.
      </p>
    </aside>
  );
}

function EmCard({ em }: { em: EmVerdict }) {
  const { lamp, word } = lampForVerdict(em.verdict);
  return (
    <article className="eg-note">
      <div className="eg-note-head">
        <span className="eg-lbl">EM · back row · {em.character}</span>
        <GreaseMark />
      </div>
      <div className="eg-note-verdict">
        <Lamp verdict={lamp} word={word} />
      </div>
      <p className="eg-note-reason">{em.reasoning}</p>
      {em.proposed_patches.length > 0 && (
        <div className="eg-fix">
          <span className="eg-lbl">Proposed — your call, not hers</span>
          {em.proposed_patches.map((p, i) => (
            <div key={i} className="eg-fix-patch">
              <q>{String(p.value)}</q>
              <span className="eg-fix-meta eg-mono">
                {p.target}:{p.path}
              </span>
              <span className="eg-fix-why">{p.rationale}</span>
            </div>
          ))}
        </div>
      )}
      {em.cites.length > 0 && (
        <p className="eg-cite">
          cites <b>{em.cites.join(", ")}</b>
        </p>
      )}
    </article>
  );
}
