import { Link } from "react-router-dom";

import type { ShotFrame, ShotSheet } from "../../api/types";
import { shotIntentLine } from "../../lib/shots";

/*
 * The slate stack (U4b) — Bea's draft shots.yaml as display-only slates in
 * the gate's aside: one slate per shot (cut · beat · hold, the clapper
 * header), the chain_from loop-return as a marker on its slate, and the
 * detail (intent line + cast tags) behind the density gate — revealed on
 * hover/focus like the plan gate's cost breakdown. NO cut / strike / reorder:
 * curation is G2 (deferred to v1c) and happens on disk; the beat number is a
 * REAL link back to the script gate, where the beat sheet lives.
 */

export function SlateStack({
  sheet,
  scriptHref,
}: {
  sheet: ShotSheet;
  /** The script gate's URL — each slate's beat number links back to it. */
  scriptHref: string;
}) {
  return (
    <section
      className="gate-slates"
      aria-label="The slate stack — the shot list, display only"
      tabIndex={0}
    >
      <div className="gate-slates-head">
        <span className="gate-lbl">The slate stack</span>
        <span className="gate-lbl gate-lbl--dim">
          {sheet.frames.length} cuts · curation lives on disk
        </span>
      </div>
      <ol className="slate-list">
        {sheet.frames.map((frame) => (
          <Slate key={frame.id} frame={frame} scriptHref={scriptHref} />
        ))}
      </ol>
    </section>
  );
}

const pad = (n: number) => String(n).padStart(2, "0");

function Slate({ frame, scriptHref }: { frame: ShotFrame; scriptHref: string }) {
  return (
    <li className="slate">
      <div className="slate-top">
        <span className="slate-clap" aria-hidden="true" />
        <span className="slate-field">
          <span className="gate-lbl">Cut</span>
          <b className="gate-mono">{pad(frame.id)}</b>
        </span>
        <span className="slate-field">
          <span className="gate-lbl">Beat</span>
          {frame.beat_id !== null ? (
            <Link
              className="slate-beatlink gate-mono"
              to={scriptHref}
              aria-label={`Beat ${frame.beat_id} — read it on the script gate`}
            >
              {pad(frame.beat_id)}
            </Link>
          ) : (
            <b className="gate-mono">—</b>
          )}
        </span>
        <span className="slate-field">
          <span className="gate-lbl">Hold</span>
          <b className="gate-mono">{frame.hold}</b>
        </span>
      </div>
      {frame.chain_from !== null && (
        <p className="slate-return gate-mono">
          ↩ returns to frame {frame.chain_from} — the loop closes here
        </p>
      )}
      {/* density gate: the slate detail arrives on intent (hover/focus) */}
      <div className="slate-detail" data-reveal>
        <p className="slate-intent">{shotIntentLine(frame.prompt)}</p>
        <span className="slate-cast">
          {frame.cast.map((name) => (
            <span key={name} className="slate-cast-tag gate-mono">
              {name}
            </span>
          ))}
        </span>
      </div>
    </li>
  );
}
