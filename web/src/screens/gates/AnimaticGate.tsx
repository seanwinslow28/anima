import { GateShell } from "./GateShell";
import { useRun } from "../../lib/runContext";

import type { FrameState } from "../../api/types";

/**
 * The Animatic gate (/runs/:id/animatic — U4c): the THIN opt-in placement
 * gate (D-G). PHILOSOPHY's non-negotiable made a screen: the human pins
 * placement (where everyone stands, facing, scale) and timing (holds) BY
 * HAND before a frame is drawn. The daemon serves neither rough upload nor
 * display (G3) — roughs go on disk — so the page is an INSTRUCTION, not a
 * drop zone, and the gate's only data source is the shared /status read.
 * One decision: POST /animatic/approve ingests whatever roughs are on disk;
 * an empty dir proceeds with a warning — "Continue without roughs" binds to
 * the SAME endpoint (skip = approve-empty, never a second route).
 */
export function AnimaticGate(_props: { pollIntervalMs?: number }) {
  const { runId, status, refresh } = useRun();

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
          <button type="button" className="gate-notice-act" onClick={refresh}>
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
        <>
          <button type="button" className="gate-approve">
            Ingest &amp; generate
            <small>⌘⏎</small>
          </button>
          <button type="button" className="gate-secondary">
            Continue without roughs
          </button>
        </>
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
