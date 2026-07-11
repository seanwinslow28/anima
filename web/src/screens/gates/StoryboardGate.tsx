import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { GateShell } from "./GateShell";
import { Markdown } from "./Markdown";
import { SlateStack } from "./SlateStack";
import { fetchArtifact } from "../../api/client";
import { nextActionUrl } from "../../lib/boothBoard";
import { hasStageMovedPast } from "../../lib/gateStage";
import { useRun } from "../../lib/runContext";
import { parseShots } from "../../lib/shots";
import { useGateAction, type GateFlow } from "../../lib/useGateAction";
import { useResource } from "../../lib/useResource";
import { RitualLeader } from "../../reelone/RitualLeader";

/**
 * The Storyboard gate (/runs/:id/storyboard — U4b): Bea's storyboard.md as
 * the lit continuity report — the page IS the screen — with her draft
 * shots.yaml parsed client-side (G4) into the display-only slate stack in
 * the aside. ONE action (Lock picture, ⌘⏎) rides U3's useGateAction; the
 * daemon's --approve-storyboard IS the curation gate (it re-validates
 * coverage / orphans / cast and REFUSES to lock a broken board), so a failed
 * lock job is not a crash — it is the legitimate "the board won't lock yet"
 * state, framed with the named gap and the fix. No in-UI curation (G2) and
 * no send-back (G7): both live on disk until their v1c deltas.
 */
export function StoryboardGate({ pollIntervalMs }: { pollIntervalMs?: number }) {
  const { runId, status, refresh } = useRun();
  const navigate = useNavigate();
  const [nonce, setNonce] = useState(0);

  const board = useResource(() => fetchArtifact(runId, "storyboard"), [runId, nonce]);
  const shots = useResource(
    () => fetchArtifact(runId, "shots").then(parseShots),
    [runId, nonce],
  );

  const { flow, submit, reset } = useGateAction(
    runId,
    { method: "POST", path: `/runs/${encodeURIComponent(runId)}/storyboard/approve` },
    { pollIntervalMs },
  );

  // the single-writer rule made visible: a job owns the run -> no lock
  const blockedBy =
    status.status === "ready"
      ? (status.data.next_action.blocked_by_job ?? null)
      : null;
  const archived =
    (shots.status === "ready" && shots.data.locked) ||
    (status.status === "ready" &&
      hasStageMovedPast(status.data.stage, "STORYBOARD"));
  const canLock = flow.phase === "idle" && blockedBy === null && !archived;

  // ADVANCE only on the full success shape — the destination is the INLINE
  // next_action (ANIMATIC when enabled, else GENERATE's eye-gate).
  useEffect(() => {
    if (flow.phase !== "advanced") return;
    navigate(
      nextActionUrl(runId, flow.nextAction) ?? `/runs/${encodeURIComponent(runId)}`,
    );
  }, [flow, navigate, runId]);

  // cancelled -> return to the gate
  useEffect(() => {
    if (flow.phase === "cancelled") reset();
  }, [flow, reset]);

  // ⌘⏎ / Ctrl+⏎ locks
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key !== "Enter" || !(e.metaKey || e.ctrlKey)) return;
      if (!canLock) return;
      e.preventDefault();
      submit();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [canLock, submit]);

  if (board.status === "loading" || shots.status === "loading") {
    return (
      <section className="gate-screen" aria-hidden="true" data-testid="gate-skeleton">
        <div className="bb-sk bb-sk--hero ro-pulse" />
      </section>
    );
  }

  if (board.status === "error" || shots.status === "error") {
    const noBoard =
      board.status === "error" && board.error.message.includes("(404)");
    return (
      <section className="gate-screen">
        <div className="gate-notice gate-notice--error" role="alert">
          <h2>{noBoard ? "No board for this run" : "Couldn't read the board"}</h2>
          <p>
            {noBoard ? (
              <>
                This run has no storyboard on disk — a back-compat run (the
                brief carried its own shots.yaml) goes straight from plan to
                generate and never visits this gate.
              </>
            ) : (
              <>
                The booth couldn't pull this run's board — the report or the
                shot list may not be authored yet, unreadable, or the daemon
                can't serve it.
              </>
            )}
          </p>
          <button
            type="button"
            className="gate-notice-act ro-button ro-button--primary"
            onClick={() => setNonce((n) => n + 1)}
          >
            Retry
          </button>
        </div>
      </section>
    );
  }

  const sheet = shots.data;
  return (
    <GateShell
      stamp={`STORYBOARD · ${sheet.slug.toUpperCase()}`}
      title="The board"
      byline="boarded by Bea · the storyboard artist"
      archiveMark={archived ? "LOCKED" : undefined}
      aside={
        <SlateStack
          sheet={sheet}
          scriptHref={`/runs/${encodeURIComponent(runId)}/script`}
        />
      }
      actions={archived ? undefined : (
        <StoryboardGateActions
          runId={runId}
          flow={flow}
          canLock={canLock}
          blockedBy={blockedBy}
          submit={() => submit()}
          refreshAndReset={() => {
            refresh();
            setNonce((n) => n + 1);
            reset();
          }}
        />
      )}
    >
      <Markdown text={board.data} />
    </GateShell>
  );
}

/**
 * The action bar renders the gate's flow state — every branch honest. The
 * U4b-specific branch is `failed`: on this gate a failed approve job is the
 * daemon's curation gate REFUSING to lock a broken board (coverage / orphan /
 * cast conflict — the reason rides job.logs), so it renders as the legitimate
 * "the board won't lock yet" state — the named gap, then the fix — never as
 * a crash. The POST-level `error` branch (404/422) stays the generic refusal.
 */
function StoryboardGateActions({
  runId,
  flow,
  canLock,
  blockedBy,
  submit,
  refreshAndReset,
}: {
  runId: string;
  flow: GateFlow;
  canLock: boolean;
  blockedBy: string | null;
  submit: () => void;
  refreshAndReset: () => void;
}) {
  switch (flow.phase) {
    case "submitting":
    case "working":
      return (
        <div className="gate-working" data-testid="gate-working">
          <RitualLeader caption="LOCKING PICTURE" />
          <p className="gate-hint">
            The gate is re-reading the board — coverage, orphans, cast
            {flow.phase === "working" && (
              <>
                {" "}
                · job <span className="gate-mono">{flow.jobId}</span>
              </>
            )}
            . It locks only if the board holds.
          </p>
        </div>
      );

    case "busy":
      return (
        <div className="gate-notice gate-notice--busy" role="alert">
          <h2>The booth is busy</h2>
          <p>
            {flow.reason} · job{" "}
            <span className="gate-mono">{flow.activeJobId}</span> has the run.
          </p>
          <Link className="gate-notice-act ro-button ro-button--quiet" to={`/runs/${encodeURIComponent(runId)}`}>
            Watch the running job
          </Link>
        </div>
      );

    case "stale":
      return (
        <div className="gate-notice" role="alert">
          <h2>This run already moved on</h2>
          <p>{flow.detail}</p>
          <button type="button" className="gate-notice-act ro-button ro-button--primary" onClick={refreshAndReset}>
            Refresh the gate
          </button>
        </div>
      );

    // THE INVALID-LOCK STATE — the refused lock, framed as a state a
    // director legitimately hits, calm and directive.
    case "failed":
      return (
        <div className="gate-notice gate-notice--refused" role="alert">
          <h2>The board won't lock yet</h2>
          <p>The gate re-read the board and refused it. The gap, named:</p>
          <pre className="gate-logs">{flow.job.logs || "(no log output)"}</pre>
          <p>
            The fix lives on disk — curate shots.yaml there (add the missing
            shot, restore the dropped cast), then re-read and lock again.
          </p>
          <button type="button" className="gate-notice-act ro-button ro-button--primary" onClick={refreshAndReset}>
            Re-read the board
          </button>
        </div>
      );

    case "degraded":
      return (
        <div className="gate-notice gate-notice--error" role="alert">
          <h2>The board locked, but the booth couldn't re-read the run</h2>
          <p>
            The job finished (rc 0) yet the run's state wouldn't load
            {flow.job.load_error && (
              <>
                : <span className="gate-mono">{flow.job.load_error}</span>
              </>
            )}
            . Refresh before touching anything.
          </p>
          <button type="button" className="gate-notice-act ro-button ro-button--primary" onClick={refreshAndReset}>
            Refresh
          </button>
        </div>
      );

    case "error":
      return (
        <div className="gate-notice gate-notice--error" role="alert">
          <h2>The gate refused{flow.status ? ` (${flow.status})` : ""}</h2>
          <p>{flow.detail}</p>
          <button type="button" className="gate-notice-act ro-button ro-button--primary" onClick={refreshAndReset}>
            Back to the gate
          </button>
        </div>
      );

    // idle, advanced (navigating away), cancelled (resetting)
    default:
      return (
        <>
          <button
            type="button"
            className="gate-approve ro-button ro-button--primary"
            disabled={!canLock}
            onClick={submit}
          >
            Lock picture
            <small>⌘⏎</small>
          </button>
          <p className="gate-hint">
            {blockedBy ? (
              <>
                Job <span className="gate-mono">{blockedBy}</span> owns this run —
                the gate unlocks when it wraps.
              </>
            ) : (
              <>
                Locking re-validates the board and writes locked: true into
                shots.yaml — then it's the camera's. Slates are the shot list;
                curation happens on disk, not here.
              </>
            )}
          </p>
        </>
      );
  }
}
