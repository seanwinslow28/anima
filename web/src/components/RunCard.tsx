import "../styles/marquee.css";

import { Link } from "react-router-dom";

import type { RunSummary } from "../api/types";
import { nextActionCta } from "../lib/nextAction";

/**
 * One run on the marquee: a booth card — slug (display face, screenlit) +
 * stage (mono chip) + the load-bearing next-move CTA, its tone mapped onto
 * the booth's light (act = tungsten reach, wait = crew working, done =
 * printed). The whole card is a real link to the run. Secondary facts (id,
 * stub, updated date) live in the quiet meta row and arrive on intent —
 * the density gate: default state is the art and the one decision.
 */
export function RunCard({ run }: { run: RunSummary }) {
  const cta = nextActionCta(run.next_action);
  return (
    <Link
      to={`/runs/${run.run_id}`}
      className="mq-card ro-sprocket"
      aria-label={`Open run ${run.slug}`}
    >
      <div className="mq-head">
        <span className="mq-name">{run.slug}</span>
        <span className="mq-stage">{run.stage}</span>
      </div>
      <div className={`mq-cta mq-cta--${cta.tone}`}>
        <span className="mq-cta-label">{cta.label}</span>
        {cta.tone === "act" && (
          <span className="mq-cta-mark" aria-hidden="true">
            →
          </span>
        )}
        {cta.tone === "wait" && (
          <span className="mq-cta-mark ro-pulse" aria-hidden="true">
            …
          </span>
        )}
        {cta.tone === "done" && (
          <span className="mq-cta-mark mq-cta-mark--print" aria-hidden="true">
            ●
          </span>
        )}
      </div>
      <div className="mq-meta">
        <span className="mq-meta-id">{run.run_id}</span>
        {run.stub && <span className="mq-meta-stub">stub</span>}
        {run.updated_at && (
          <span className="mq-meta-date">{run.updated_at.slice(0, 10)}</span>
        )}
      </div>
    </Link>
  );
}
