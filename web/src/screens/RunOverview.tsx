import "../styles/boothboard.css";

import { useState } from "react";
import { useParams } from "react-router-dom";

import { fetchRawState, fetchStatus } from "../api/client";
import { useResource } from "../lib/useResource";

/**
 * Screen 3 — the booth board: the run's home base as the projection booth
 * sees it. Two one-shot daemon reads (GET /runs/{id}/status + GET /runs/{id}
 * raw — for the cost estimate and the fork flags); NO live polling (U3) and
 * NO gate POSTs (U3). Loading is a skeleton of the board, an unreadable run
 * is the couldn't-read state + one retry. Renders inside BoothShell
 * (inherits the `.reelone` token scope).
 */
export function RunOverview() {
  const { id = "" } = useParams();
  // `nonce` bumps on retry/refresh to re-run both reads (useResource deps).
  const [nonce, setNonce] = useState(0);
  const status = useResource(() => fetchStatus(id), [id, nonce]);
  const raw = useResource(() => fetchRawState(id), [id, nonce]);

  if (status.status === "loading" || raw.status === "loading") {
    return <BoardSkeleton />;
  }

  if (status.status === "error" || raw.status === "error") {
    return (
      <section className="bb-screen">
        <div className="bb-notice" role="alert">
          <h1 className="bb-notice-lead">Couldn't read this run.</h1>
          <p className="bb-notice-sub">
            The booth couldn't project <span className="bb-mono">{id}</span> —
            it may have moved, or its state file is unreadable.
          </p>
          <button
            type="button"
            className="bb-retry"
            onClick={() => setNonce((n) => n + 1)}
          >
            Retry
          </button>
        </div>
      </section>
    );
  }

  return (
    <section className="bb-screen" data-testid="booth-board">
      <p className="bb-mono">{raw.data.slug}</p>
    </section>
  );
}

/** Loading is a skeleton of the *board* — reel strip, hero, ledger shapes. */
function BoardSkeleton() {
  return (
    <section className="bb-screen" aria-hidden="true" data-testid="board-skeleton">
      <div className="bb-sk bb-sk--reel ro-pulse" />
      <div className="bb-sk-row">
        <div className="bb-sk bb-sk--hero ro-pulse" />
        <div className="bb-sk bb-sk--aside ro-pulse" />
      </div>
      <div className="bb-sk-row">
        <div className="bb-sk bb-sk--strip ro-pulse" />
        <div className="bb-sk bb-sk--aside ro-pulse" />
      </div>
    </section>
  );
}
