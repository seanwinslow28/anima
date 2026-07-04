import { Link } from "react-router-dom";

import type { RunSummary } from "../api/types";
import { nextActionCta } from "../lib/nextAction";

/**
 * One run in the gallery: name (slug, Newsreader) + stage chip (mono) + the
 * load-bearing next-move CTA. The whole card is a real link to the run — it
 * leads with the verb of the next move, never a bare "in progress".
 */
export function RunCard({ run }: { run: RunSummary }) {
  const cta = nextActionCta(run.next_action);
  return (
    <Link
      to={`/runs/${run.run_id}`}
      className="runcard"
      aria-label={`Open run ${run.slug}`}
    >
      <div className="runcard-head">
        <span className="runcard-name">{run.slug}</span>
        <span className="stagechip">{run.stage}</span>
      </div>
      <div className="runcard-id">
        {run.run_id}
        {run.stub && <span className="stubtag"> · stub</span>}
      </div>
      <div className={`cta cta--${cta.tone}`}>
        <span className="cta-label">{cta.label}</span>
        {cta.tone === "act" && (
          <span className="cta-mark" aria-hidden="true">
            →
          </span>
        )}
        {cta.tone === "wait" && (
          <span className="cta-mark" aria-hidden="true">
            …
          </span>
        )}
      </div>
    </Link>
  );
}
