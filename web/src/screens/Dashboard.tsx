import { useState } from "react";

import { fetchRuns } from "../api/client";
import { isRunError, type RunError } from "../api/types";
import { RunCard } from "../components/RunCard";
import { CardGridSkeleton } from "../components/Skeleton";
import { useResource } from "../lib/useResource";

/**
 * Screen 1 — the run gallery and the resume point. Answers one question per
 * run: what's my next move here? Reads GET /runs and leads each card with its
 * next_action verb. Every doctrine state is built: loading (a skeleton of the
 * grid), empty (an invitation), error (what happened + the one recovery), and
 * the ready grid — where an unreadable run is surfaced as a card, never dropped.
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
        <div className="notice notice--error" role="alert">
          <p className="notice-lead">Couldn't reach the daemon.</p>
          <p className="notice-sub">
            Retry, or check that the daemon is running on 127.0.0.1:8000.
          </p>
          <button
            type="button"
            className="retry-btn"
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
        <div className="notice">
          <p className="notice-lead">No runs yet.</p>
          <p className="notice-sub">Start a short and the room opens.</p>
        </div>
        <div className="grid grid--pad">
          <NewProjectCard />
        </div>
      </Screen>
    );
  }

  return (
    <Screen>
      <div className="grid">
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
    <section className="screen">
      <h1 className="screen-title">Runs</h1>
      <p className="screen-sub">What's your next move?</p>
      {children}
    </section>
  );
}

/** An unreadable run — surfaced with its id + the recovery hint, never dropped. */
function UnreadableRunCard({ run }: { run: RunError }) {
  return (
    <div className="errcard">
      <div className="errcard-name">{run.run_id}</div>
      <div className="errcard-msg">Couldn't read this run.</div>
    </div>
  );
}

/** Inert placeholder — the brainstorm room lands in v1c. */
function NewProjectCard() {
  return (
    <button
      type="button"
      className="newcard"
      disabled
      aria-label="New project"
      title="The brainstorm room opens in v1c"
    >
      <span className="newcard-plus" aria-hidden="true">
        ＋
      </span>
      <span>New project</span>
      <span className="newcard-soon" aria-hidden="true">
        opens in v1c
      </span>
    </button>
  );
}
