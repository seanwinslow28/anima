import type { Beat, BeatSheet } from "../../api/types";

/**
 * The beats sheet (U4a) — Sam's beats.json as the structured sheet on the
 * lit page: the logline up top, then each beat as one entry (id · title ·
 * intent · cast, with the emotional beat / feel / notes as the detail line).
 * A component over the parsed JSON, not markdown. No h1 of its own — the
 * GateShell's gate title is the screen's one h1.
 */
export function BeatsSheet({ sheet }: { sheet: BeatSheet }) {
  return (
    <div className="beats-sheet">
      <p className="beats-logline">{sheet.logline}</p>
      <ol className="beats-list">
        {sheet.beats.map((beat) => (
          <BeatEntry key={beat.id} beat={beat} />
        ))}
      </ol>
    </div>
  );
}

function BeatEntry({ beat }: { beat: Beat }) {
  return (
    <li className="beats-entry">
      <div className="beats-head">
        <span className="beats-id gate-mono" aria-hidden="true">
          {String(beat.id).padStart(2, "0")}
        </span>
        <h2 className="beats-title">{beat.title}</h2>
        <span className="beats-emotion">{beat.emotional_beat}</span>
      </div>
      <p className="beats-intent">{beat.intent}</p>
      <div className="beats-detail">
        <span className="beats-cast">
          {beat.cast.map((name) => (
            <span key={name} className="beats-cast-tag gate-mono">
              {name}
            </span>
          ))}
        </span>
        {beat.feel && <span className="beats-feel">{beat.feel}</span>}
        {beat.notes && <span className="beats-notes">{beat.notes}</span>}
      </div>
    </li>
  );
}
