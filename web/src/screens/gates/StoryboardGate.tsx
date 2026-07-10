import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { GateShell } from "./GateShell";
import { Markdown } from "./Markdown";
import { SlateStack } from "./SlateStack";
import { fetchArtifact } from "../../api/client";
import { nextActionUrl } from "../../lib/boothBoard";
import { useRun } from "../../lib/runContext";
import { parseShots } from "../../lib/shots";
import { useGateAction } from "../../lib/useGateAction";
import { useResource } from "../../lib/useResource";

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
  const { runId, status } = useRun();
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
  const canLock = flow.phase === "idle" && blockedBy === null;

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
            className="gate-notice-act"
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
      aside={
        <SlateStack
          sheet={sheet}
          scriptHref={`/runs/${encodeURIComponent(runId)}/script`}
        />
      }
      actions={
        <button
          type="button"
          className="gate-approve"
          disabled={!canLock}
          onClick={() => submit()}
        >
          Lock picture
          <small>⌘⏎</small>
        </button>
      }
    >
      <Markdown text={board.data} />
    </GateShell>
  );
}
