import { useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";

import { GateShell } from "./GateShell";
import { nextActionUrl } from "../../lib/boothBoard";
import { useRun } from "../../lib/runContext";
import { useGateAction, type GateFlow } from "../../lib/useGateAction";
import { RitualLeader } from "../../reelone/RitualLeader";

import type { FrameState } from "../../api/types";

/**
 * The Animatic gate (/runs/:id/animatic — U4c): the THIN opt-in placement
 * gate (D-G). PHILOSOPHY's non-negotiable made a screen: the human pins
 * placement (where everyone stands, facing, scale) and timing (holds) BY
 * HAND before a frame is drawn. The daemon serves neither rough upload nor
 * display (G3) — roughs go on disk — so the page is an INSTRUCTION, not a
 * drop zone, and the gate's only data source is the shared /status read.
 * One decision, two roads: "Ingest & generate" and "Continue without
 * roughs" BOTH bind to POST /animatic/approve (skip = approve-empty — the
 * daemon ingests whatever is on disk and an empty dir proceeds with a
 * warning; it is never a second endpoint).
 */
export function AnimaticGate({ pollIntervalMs }: { pollIntervalMs?: number }) {
  const { runId, status, refresh } = useRun();
  const navigate = useNavigate();

  const { flow, submit, reset } = useGateAction(
    runId,
    { method: "POST", path: `/runs/${encodeURIComponent(runId)}/animatic/approve` },
    { pollIntervalMs },
  );

  // the single-writer rule made visible: a job owns the run -> both roads close
  const blockedBy =
    status.status === "ready"
      ? (status.data.next_action.blocked_by_job ?? null)
      : null;
  const canAct = flow.phase === "idle" && blockedBy === null;

  // ADVANCE only on the full success shape — the destination is the INLINE
  // next_action (review_frame F1 — the eye-gate, U5's route).
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

  // ⌘⏎ / Ctrl+⏎ ingests
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key !== "Enter" || !(e.metaKey || e.ctrlKey)) return;
      if (!canAct) return;
      e.preventDefault();
      submit();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [canAct, submit]);

  if (status.status === "loading") {
    return (
      <section className="gate-screen" aria-hidden="true" data-testid="gate-skeleton">
        <div className="bb-sk bb-sk--hero ro-pulse" />
      </section>
    );
  }

  if (status.status === "error") {
    return (
      <section className="gate-screen">
        <div className="gate-notice gate-notice--error" role="alert">
          <h2>Couldn't read the run</h2>
          <p>
            The booth couldn't pull this run's status — the daemon may be
            down, or the run unreadable.
          </p>
          <button type="button" className="gate-notice-act ro-button ro-button--primary" onClick={refresh}>
            Retry
          </button>
        </div>
      </section>
    );
  }

  return (
    <GateShell
      stamp="ANIMATIC · PLACEMENT"
      title="The placement pass"
      byline="drawn by hand · the human owns placement + timing"
      aside={<HoldsStrip frames={status.data.frames} />}
      actions={
        <AnimaticGateActions
          runId={runId}
          flow={flow}
          canAct={canAct}
          blockedBy={blockedBy}
          submit={() => submit()}
          refreshAndReset={() => {
            refresh();
            reset();
          }}
        />
      }
    >
      <p>
        The board is locked. Before a frame is drawn, pin the staging
        yourself — where each character stands, which way they face, their
        scale. One rough per frame you want to pin, dropped into
      </p>
      <p className="animatic-drop">
        <code className="gate-mono">{`runs/${runId}/animatic/`}</code>
      </p>
      <p>
        named by frame id — <code>F01.png</code>, <code>F02.png</code> … A
        stripped silhouette is enough (it reads cleaner than a colored rough,
        and the role-tag keeps its look out of the finished frame). Every
        frame is optional; timing rides an optional <code>holds.json</code>{" "}
        beside them.
      </p>
    </GateShell>
  );
}

/**
 * The holds strip — the pacing that drives ASSEMBLE, read from
 * /status.frames[].hold. The empty shape is FIRST-CLASS: today's daemon
 * serves frames: [] at stage ANIMATIC (frame_order populates in
 * enter_generate, after this gate), so the quiet board-holds line is what a
 * live run shows; the strip lights the moment the projection carries frames.
 */
function HoldsStrip({ frames }: { frames: FrameState[] }) {
  return (
    <section className="gate-holds" aria-label="The holds">
      <h2 className="gate-lbl">The holds</h2>
      {frames.length > 0 ? (
        <ul className="holds-strip">
          {frames.map((f) => (
            <li key={f.n} className="holds-cell">
              <span className="holds-frame gate-mono">
                F{String(f.n).padStart(2, "0")}
              </span>
              <span className="holds-count">×{f.hold ?? 2}</span>
            </li>
          ))}
        </ul>
      ) : (
        <p className="holds-note">
          The board's holds carry the timing through to assemble.
        </p>
      )}
      <p className="holds-note">
        A <code className="gate-mono">holds.json</code> beside the roughs
        overrides them at ingest.
      </p>
    </section>
  );
}

/**
 * The action bar renders the gate's flow state — every branch honest. The
 * U4c-specific branch is `failed`: --approve-animatic REFUSING a bad drop
 * (a rough naming a frame not in the board, a malformed holds.json — the
 * reason rides job.logs verbatim), framed as the legitimate "the roughs
 * won't ingest yet" state — the named gap, then the on-disk fix. An EMPTY
 * dir is NOT a failure: the daemon proceeds with a warning (the skip road).
 */
function AnimaticGateActions({
  runId,
  flow,
  canAct,
  blockedBy,
  submit,
  refreshAndReset,
}: {
  runId: string;
  flow: GateFlow;
  canAct: boolean;
  blockedBy: string | null;
  submit: () => void;
  refreshAndReset: () => void;
}) {
  switch (flow.phase) {
    case "submitting":
    case "working":
      return (
        <div className="gate-working" data-testid="gate-working">
          <RitualLeader caption="INGESTING PLACEMENT" />
          <p className="gate-hint">
            The gate is reading the roughs off disk — placement pins ride
            into generate, holds into assemble
            {flow.phase === "working" && (
              <>
                {" "}
                · job <span className="gate-mono">{flow.jobId}</span>
              </>
            )}
            .
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

    // THE REFUSED-INGEST STATE — a bad drop, named and fixable on disk.
    case "failed":
      return (
        <div className="gate-notice gate-notice--refused" role="alert">
          <h2>The roughs won't ingest yet</h2>
          <p>The gate read the drop directory and refused it. The gap, named:</p>
          <pre className="gate-logs">{flow.job.logs || "(no log output)"}</pre>
          <p>
            The fix lives on disk — rename or remove the offending rough, or
            repair holds.json, then ingest again. (No roughs at all is fine:
            that road proceeds with a warning.)
          </p>
          <button type="button" className="gate-notice-act ro-button ro-button--primary" onClick={refreshAndReset}>
            Back to the placement gate
          </button>
        </div>
      );

    case "degraded":
      return (
        <div className="gate-notice gate-notice--error" role="alert">
          <h2>The roughs ingested, but the booth couldn't re-read the run</h2>
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
            disabled={!canAct}
            onClick={submit}
          >
            Ingest &amp; generate
            <small>⌘⏎</small>
          </button>
          <button
            type="button"
            className="gate-secondary ro-button ro-button--quiet"
            disabled={!canAct}
            onClick={submit}
          >
            Continue without roughs
          </button>
          <p className="gate-hint">
            {blockedBy ? (
              <>
                Job <span className="gate-mono">{blockedBy}</span> owns this run —
                the gate unlocks when it wraps.
              </>
            ) : (
              <>
                Both roads go through the same gate — ingest reads whatever is
                on disk; nothing there means the pass is waived and the
                board's holds carry through.
              </>
            )}
          </p>
        </>
      );
  }
}
