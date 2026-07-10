import "../../styles/eyegate.css";

import { useState } from "react";
import { useParams } from "react-router-dom";

import { fetchCandidates } from "../../api/client";
import type { CandidateAttempt, FrameState, RunStatus } from "../../api/types";
import { framesToReel } from "../../lib/boothBoard";
import { useRun } from "../../lib/runContext";
import { useResource } from "../../lib/useResource";
import { BurnIn } from "../../reelone/BurnIn";
import { Filmstrip } from "../../reelone/Filmstrip";
import { RitualLeader } from "../../reelone/RitualLeader";
import { Timecode } from "../../reelone/Timecode";
import { EmReadout } from "./EmReadout";

/*
 * The eye-gate (U5a) — the screening. The stage is the only bright object in
 * the room: the current frame's shown take, lit, alone; takes switch under
 * it; Em reads from the margin. All client-side over the daemon's reads
 * (D-E): /status through the run scope + GET /frames/{n}/candidates +
 * GET /frames/{n}/image?attempt=K as <img> srcs. Print/retry (the POSTs)
 * are U5b; onion/diff/lights are U5c.
 */

/** The G5 constants the burn-in + provenance lines are composed from. */
const FPS_LINE = "12 FPS";
const MODEL_LINE = "NB2";
const FRAME_COST_LINE = "$0.07";

const frameLabel = (n: number) => `F${String(n).padStart(2, "0")}`;

export function EyeGate() {
  const { n = "" } = useParams();
  const frameN = Number(n);
  const { runId, status, refresh } = useRun();
  const [nonce, setNonce] = useState(0);
  const candidates = useResource(
    () => fetchCandidates(runId, frameN),
    [runId, frameN, nonce],
  );

  const retry = () => {
    refresh();
    setNonce((x) => x + 1);
  };

  if (status.status === "loading" || candidates.status === "loading") {
    return <StageSkeleton />;
  }

  if (status.status === "error" || candidates.status === "error") {
    return (
      <section className="eg-screen">
        <div className="eg-notice" role="alert">
          <h1 className="eg-notice-lead">Couldn't screen this frame.</h1>
          <p className="eg-notice-sub">
            The booth couldn't project {frameLabel(frameN)} of{" "}
            <span className="eg-mono">{runId}</span> — it may not be on this
            reel, or its candidates are unreadable.
          </p>
          <button type="button" className="eg-retry" onClick={retry}>
            Retry
          </button>
        </div>
      </section>
    );
  }

  const frameState =
    status.data.frames.find((f) => f.n === frameN) ?? null;
  const stillDrawing =
    frameState !== null &&
    frameState.status !== "approved" &&
    frameState.status !== "generated";

  if (candidates.data.length === 0 || stillDrawing) {
    return (
      <section className="eg-screen eg-screen--working">
        <h1 className="eg-working-lead">Flo is drawing {frameLabel(frameN)}</h1>
        <div className="eg-working-leader">
          <RitualLeader caption="FLO IS DRAWING" />
        </div>
        <p className="eg-working-sub">
          The booth will call when the print is up.
        </p>
      </section>
    );
  }

  return (
    <Screening
      key={frameN}
      runId={runId}
      frameN={frameN}
      frameState={frameState}
      status={status.data}
      attempts={candidates.data}
    />
  );
}

/** The ready state: the lit stage + Em's margin + takes + the reel. */
function Screening({
  runId,
  frameN,
  frameState,
  status,
  attempts,
}: {
  runId: string;
  frameN: number;
  frameState: FrameState | null;
  status: RunStatus;
  attempts: CandidateAttempt[];
}) {
  const label = frameLabel(frameN);
  const hold = frameState?.hold ?? 2;
  // default shown take: the approved one if the frame has one, else the latest
  const defaultShown =
    attempts.find((a) => a.status === "approved")?.attempt ??
    attempts[attempts.length - 1].attempt;
  const [shown, setShown] = useState(defaultShown);
  // takes whose <img> 404ed — flipped to the honest card, never left broken
  const [broken, setBroken] = useState<ReadonlySet<number>>(new Set());

  const attempt =
    attempts.find((a) => a.attempt === shown) ?? attempts[attempts.length - 1];
  const showable =
    attempt.image_url !== null &&
    attempt.status !== "errored" &&
    !broken.has(attempt.attempt);

  // the reel ledger: the run's frames, ringed on the VIEWED frame
  const reelFrames = framesToReel(runId, status).map((f) => ({
    ...f,
    now: f.id === frameN,
  }));

  return (
    <section className="eg-screen" data-testid="eyegate">
      <header className="eg-head">
        <h1 className="eg-h1">{label} · the screening</h1>
        <Timecode frame={frameN - 1} hold={hold} />
      </header>

      <div className="eg-stagewrap">
        <div className="eg-beam" aria-hidden="true" />
        <figure
          className="eg-stage"
          data-testid="stage"
          aria-label={`${label} take ${attempt.attempt}, projected`}
        >
          {showable ? (
            <div className="eg-img eg-img--lit">
              <img
                src={attempt.image_url as string}
                alt={`${label} take ${attempt.attempt} — the candidate on screen`}
                onError={() =>
                  setBroken((prev) => new Set(prev).add(attempt.attempt))
                }
              />
            </div>
          ) : (
            <div className="eg-nodevelop">
              <p className="eg-nodevelop-lead">This take didn't develop.</p>
              {attempt.errored && (
                <p className="eg-nodevelop-why eg-mono">{attempt.errored}</p>
              )}
              <p className="eg-nodevelop-sub">
                No image landed for take {attempt.attempt} — pick another take,
                or send it again once the retake gate lands.
              </p>
            </div>
          )}
          <span className="eg-burn eg-burn--l">
            <BurnIn segments={[label, `TAKE ${attempt.attempt}`, `HOLD ${hold}`]} />
          </span>
          <span className="eg-burn eg-burn--r">
            <BurnIn segments={[FPS_LINE, MODEL_LINE, FRAME_COST_LINE]} />
          </span>
        </figure>
        <EmReadout records={attempt.em} />
      </div>

      <div className="eg-transport">
        <div className="eg-row">
          <div className="eg-takes" role="group" aria-label="Takes">
            {attempts.map((a) => (
              <button
                key={a.attempt}
                type="button"
                aria-pressed={a.attempt === shown}
                onClick={() => setShown(a.attempt)}
              >
                TAKE {a.attempt}
              </button>
            ))}
          </div>
          {/* the provenance line — composed from constants + the verdict (G8) */}
          <p className="eg-prov">
            {attempt.em.length > 0
              ? "drawn by Flo (NB2) · read by Em · your call"
              : "drawn by Flo (NB2) · your call"}
          </p>
        </div>
        <div className="eg-strip">
          <Filmstrip frames={reelFrames} />
        </div>
      </div>
    </section>
  );
}

/** Loading is a skeleton of the stage — the lit frame's shape, dimmed. */
function StageSkeleton() {
  return (
    <section
      className="eg-screen"
      aria-hidden="true"
      data-testid="eyegate-skeleton"
    >
      <div className="eg-sk eg-sk--stage ro-pulse" />
      <div className="eg-sk eg-sk--transport ro-pulse" />
    </section>
  );
}
