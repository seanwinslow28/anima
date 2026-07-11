import "../styles/boothboard.css";

import { useState } from "react";
import { Link, useParams } from "react-router-dom";

import { fetchRawState } from "../api/client";
import type { RawRunState, RunStatus } from "../api/types";
import {
  CREW,
  deriveSpend,
  deriveStageReel,
  FRAME_COST_USD,
  framesToReel,
  goLabel,
  nextActionUrl,
  phaseLabel,
  stageRevisitUrl,
  type StageSegment,
} from "../lib/boothBoard";
import { nextActionCta } from "../lib/nextAction";
import { useRun } from "../lib/runContext";
import { useResource } from "../lib/useResource";
import { BurnIn } from "../reelone/BurnIn";
import { Filmstrip } from "../reelone/Filmstrip";
import { RitualLeader } from "../reelone/RitualLeader";

/**
 * Screen 3 — the booth board: the run's home base as the projection booth
 * sees it. The /status read comes through the run scope (U3's runContext),
 * which LIVE-POLLS the job that owns the run and re-reads /status when it
 * goes terminal — the board advances on the real signal (U2b's static seam
 * is closed). The raw read (GET /runs/{id} — cost estimate + fork flags)
 * stays a local one-shot. Loading is a skeleton of the board, an unreadable
 * run is the couldn't-read state + one retry. Renders inside BoothShell
 * (inherits the `.reelone` token scope).
 */
export function RunOverview() {
  const { id = "" } = useParams();
  const { status, refresh } = useRun();
  // `nonce` re-runs the raw read on retry; the status read rides refresh().
  const [nonce, setNonce] = useState(0);
  const raw = useResource(() => fetchRawState(id), [id, nonce]);

  const reread = () => {
    refresh();
    setNonce((n) => n + 1);
  };

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
            className="bb-retry ro-button ro-button--primary"
            onClick={reread}
          >
            Retry
          </button>
        </div>
      </section>
    );
  }

  return (
    <BoothBoard
      runId={id}
      status={status.data}
      raw={raw.data}
      onReread={reread}
    />
  );
}

/** The ready board: the reel of stages + the now-screening hero. */
function BoothBoard({
  runId,
  status,
  raw,
  onReread,
}: {
  runId: string;
  status: RunStatus;
  raw: RawRunState;
  onReread: () => void;
}) {
  const segments = deriveStageReel(raw, status);
  return (
    <section className="bb-screen" data-testid="booth-board">
      <StageReel runId={runId} segments={segments} />
      <div className="bb-marquee">
        {status.active_job ? (
          <CrewWorking status={status} onReread={onReread} />
        ) : (
          <NowScreening runId={runId} status={status} />
        )}
        <BoxOffice status={status} raw={raw} />
      </div>
      <div className="bb-lower">
        <FrameReel runId={runId} status={status} slug={raw.slug} />
        <CrewStations />
      </div>
    </section>
  );
}

/**
 * The Working doctrine state, LIVE (U3): the run scope polls the owning
 * job's /jobs/{id} and re-reads /status on its terminal, so this leader
 * resolves on the real signal — the ritual timer, never a fake ETA. The
 * manual re-read stays as an escape hatch. No mutating affordance renders
 * while the job owns the run (blocked_by_job).
 */
function CrewWorking({
  status,
  onReread,
}: {
  status: RunStatus;
  onReread: () => void;
}) {
  const cta = nextActionCta(status.next_action);
  const line = cta.tone === "wait" ? cta.label : "The crew is on it";
  return (
    <section className="bb-now bb-now--working" aria-label="The crew is working">
      <span className="bb-eyebrow">
        In the booth · next_action: {status.next_action.kind}
      </span>
      <h1 className="bb-move" aria-live="polite">
        {line}…
      </h1>
      <RitualLeader caption="IN THE BOOTH" />
      <p className="bb-working-sub">
        Job <span className="bb-mono">{status.active_job?.job_id}</span> owns
        the run — the board advances when it wraps.
      </p>
      <button
        type="button"
        className="bb-retry ro-button ro-button--primary"
        onClick={onReread}
      >
        Re-read the booth
      </button>
    </section>
  );
}

/** The box office — estimate truthfully, spend as a labelled derivation (D-H). */
function BoxOffice({ status, raw }: { status: RunStatus; raw: RawRunState }) {
  const ce = raw.plan.cost_estimate;
  const spend = deriveSpend(status.frames);
  return (
    <aside className="bb-boxoffice" aria-label="Box office — cost" tabIndex={0}>
      <div className="bb-bo-head">
        <span className="bb-lbl">Box office</span>
        <span className="bb-lbl bb-lbl--dim">estimate, not a cap</span>
      </div>
      <div className="bb-stub">
        <p className="bb-bo-spent bb-mono" data-testid="derived-spend">
          ≈ ${spend.usd.toFixed(2)} drawn
          <span className="bb-bo-how">
            {" "}
            · derived: {spend.attempts} take{spend.attempts === 1 ? "" : "s"} ×
            ${FRAME_COST_USD.toFixed(2)}
          </span>
        </p>
        {ce ? (
          <p className="bb-bo-est bb-mono">
            est ${ce.low_usd.toFixed(2)} – ${ce.high_usd.toFixed(2)} · median $
            {ce.median_usd.toFixed(2)}
          </p>
        ) : (
          <p className="bb-bo-est">
            estimate pending — Maya hasn't costed this plan yet
          </p>
        )}
      </div>
      {/* density gate: the breakdown + house rules arrive on intent */}
      <div className="bb-bo-detail" data-reveal>
        {ce && (
          <table className="bb-bo-table">
            <tbody>
              {Object.entries(ce.by_phase).map(([key, band]) => (
                <tr key={key}>
                  <td>{phaseLabel(key)}</td>
                  <td className="bb-mono">
                    ${band.low_usd.toFixed(2)} – ${band.high_usd.toFixed(2)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
        <p className="bb-bo-note">
          <b>Nothing burns compute until you approve.</b> Draft tier is the
          house default; pro screens only on your call or a critic pass.
        </p>
        <BurnIn segments={["12 FPS", "NB2", `$${FRAME_COST_USD.toFixed(2)} / frame`]} />
      </div>
    </aside>
  );
}

/** The mini frame-reel — the run's cuts as a filmstrip ledger. */
function FrameReel({
  runId,
  status,
  slug,
}: {
  runId: string;
  status: RunStatus;
  slug: string;
}) {
  if (status.frames.length === 0) {
    return (
      <div className="bb-reelbox">
        <span className="bb-lbl">Reel — {slug}</span>
        <p className="bb-reel-empty">No cuts on the reel yet.</p>
      </div>
    );
  }
  return (
    <div className="bb-reelbox">
      <span className="bb-lbl">
        Reel — {status.frames.length} cut{status.frames.length === 1 ? "" : "s"}{" "}
        · {slug}
      </span>
      <Filmstrip frames={framesToReel(runId, status)} />
    </div>
  );
}

/** The crew stations — the constant map, revealed on intent. */
function CrewStations() {
  return (
    <aside className="bb-crew" aria-label="The crew tonight" tabIndex={0}>
      <span className="bb-lbl">The crew tonight</span>
      <p className="bb-crew-whisper bb-mono">seven stations · focus to call roll</p>
      <ul className="bb-crew-list" data-reveal>
        {CREW.map((c) => (
          <li key={c.agent}>
            <b>{c.agent}</b>
            <span>{c.station}</span>
          </li>
        ))}
      </ul>
    </aside>
  );
}

/** The leader strip — one sprocketed segment per derived stage. */
function StageReel({
  runId,
  segments,
}: {
  runId: string;
  segments: StageSegment[];
}) {
  return (
    <nav aria-label="pipeline stages">
      <ol className="bb-leaderstrip">
        {segments.map((seg) => {
          const href =
            seg.status === "done" ? stageRevisitUrl(runId, seg.stage) : null;
          const inner = (
            <>
              <span className="bb-seg-n" aria-hidden="true">
                {seg.n}
              </span>
              <span className="bb-seg-nm">{seg.label}</span>
              <span className="bb-seg-who">{seg.who}</span>
              <span className="bb-seg-st">{seg.mark}</span>
            </>
          );
          return (
            <li
              key={seg.stage}
              className={`bb-seg ro-sprocket bb-seg--${seg.status}`}
              aria-current={seg.status === "now" ? "step" : undefined}
            >
              {href ? (
                // a printed stage is a revisit affordance — a real link
                <Link className="bb-seg-hit" to={href}>
                  {inner}
                </Link>
              ) : (
                <div className="bb-seg-hit">{inner}</div>
              )}
            </li>
          );
        })}
      </ol>
    </nav>
  );
}

/** The hero: the one move, front and centre (h1 = the CTA spine's words). */
function NowScreening({ runId, status }: { runId: string; status: RunStatus }) {
  const cta = nextActionCta(status.next_action);
  const url = nextActionUrl(runId, status.next_action);
  const verb = goLabel(status.next_action.kind);
  const frame = status.next_action.frame;
  return (
    <section className="bb-now" aria-label="Your next move">
      <span className="bb-eyebrow">
        Now screening · next_action: {status.next_action.kind}
      </span>
      <h1 className="bb-move">{cta.label}</h1>
      {url && verb && (
        <Link className="bb-go ro-button ro-button--primary" to={url}>
          {verb}
          {frame != null && (
            <small>F{String(frame).padStart(2, "0")} · ⏎</small>
          )}
        </Link>
      )}
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
