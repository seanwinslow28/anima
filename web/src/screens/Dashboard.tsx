import "../styles/marquee.css";

import { useState } from "react";

import { fetchRuns } from "../api/client";
import { isRunError, type RunError } from "../api/types";
import { RunCard } from "../components/RunCard";
import { CardGridSkeleton } from "../components/Skeleton";
import { useResource } from "../lib/useResource";

/**
 * Screen 1 — the marquee: the run list as the screening room's front of
 * house. Answers one question per run: what's my next move here? Reads
 * GET /runs and leads each booth card with its next_action verb. Every
 * doctrine state is built: loading (a skeleton of the marquee), empty (an
 * invitation), error (what happened + the one recovery), and the ready
 * grid — where an unreadable run is surfaced as a card, never dropped.
 * Renders inside BoothShell, which provides the `.reelone` token scope.
 */
export function Dashboard() {
  // `nonce` bumps on retry to re-run the same fetch (useResource watches deps).
  const [nonce, setNonce] = useState(0);
  const runs = useResource(fetchRuns, [nonce]);

  if (runs.status === "loading") {
    return (
      <Screen>
        <CardGridSkeleton />
      </Screen>
    );
  }

  if (runs.status === "error") {
    return (
      <Screen>
        <div className="mq-notice mq-notice--error" role="alert">
          <p className="mq-notice-lead">Couldn't reach the daemon.</p>
          <p className="mq-notice-sub">
            Retry, or check that the daemon is running on 127.0.0.1:8000.
          </p>
          <button
            type="button"
            className="mq-retry ro-button ro-button--primary"
            onClick={() => setNonce((n) => n + 1)}
          >
            Retry
          </button>
        </div>
      </Screen>
    );
  }

  if (runs.data.length === 0) {
    return (
      <Screen>
        <div className="mq-notice">
          <p className="mq-notice-lead">No runs yet.</p>
          <p className="mq-notice-sub">Bring a spark and the room opens.</p>
        </div>
        <div className="mq-grid mq-grid--pad">
          <NewProjectCard />
        </div>
      </Screen>
    );
  }

  return (
    <Screen>
      <div className="mq-grid">
        {runs.data.map((item) =>
          isRunError(item) ? (
            <UnreadableRunCard key={item.run_id} run={item} />
          ) : (
            <RunCard key={item.run_id} run={item} />
          ),
        )}
        <NewProjectCard />
      </div>
    </Screen>
  );
}

function Screen({ children }: { children: React.ReactNode }) {
  return (
    <section className="mq-screen">
      <h1 className="mq-title">Runs</h1>
      <p className="mq-sub">What's your next move?</p>
      {children}
    </section>
  );
}

/** An unreadable run — a booth errcard with its id, never dropped. */
function UnreadableRunCard({ run }: { run: RunError }) {
  return (
    <div className="mq-err">
      <div className="mq-err-id">{run.run_id}</div>
      <div className="mq-err-msg">Couldn't read this run.</div>
    </div>
  );
}

/** Inert placeholder — the brainstorm room lands in v1c. */
function NewProjectCard() {
  return (
    <div className="mq-new" title="The brainstorm room opens in v1c">
      <span className="mq-new-plus" aria-hidden="true">
        ＋
      </span>
      <span>New project</span>
      <span className="mq-new-soon" aria-hidden="true">
        opens in v1c
      </span>
    </div>
  );
}
