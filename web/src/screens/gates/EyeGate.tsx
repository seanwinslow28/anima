import "../../styles/eyegate.css";

import { useEffect, useMemo, useRef, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import { fetchCandidates, frameImageUrl } from "../../api/client";
import type { CandidateAttempt, FrameState, RunStatus } from "../../api/types";
import { framesToReel } from "../../lib/boothBoard";
import { useImagePreload } from "../../lib/imagePreload";
import { useRun } from "../../lib/runContext";
import { useResource } from "../../lib/useResource";
import { useRockLoop, type LoopEntry } from "../../lib/useRockLoop";
import { BurnIn } from "../../reelone/BurnIn";
import { Filmstrip } from "../../reelone/Filmstrip";
import { RitualLeader } from "../../reelone/RitualLeader";
import { Timecode } from "../../reelone/Timecode";
import { CheatSheet } from "./CheatSheet";
import { EmReadout } from "./EmReadout";
import { StageToolbar } from "./StageToolbar";

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

  // -- the cross-slice image DoD: prime every take + every loop neighbor,
  //    so the rock swaps decoded images, never flicker-loads --------------
  const preloadUrls = useMemo(() => {
    const urls = attempts
      .map((a) => a.image_url)
      .filter((u): u is string => u !== null);
    for (const f of status.frames) {
      if (f.status === "approved" && f.n !== frameN) {
        urls.push(frameImageUrl(runId, f.n));
      }
    }
    return urls;
  }, [attempts, status.frames, frameN, runId]);
  const preload = useImagePreload(preloadUrls);

  // -- the loop context: the approved neighbors in frame order, with the
  //    SHOWN take riding the current frame's slot (judge THIS candidate in
  //    motion). A neighbor whose image failed to load is skipped honestly. --
  const loopEntries = useMemo(() => {
    const out: LoopEntry[] = [];
    for (const f of [...status.frames].sort((a, b) => a.n - b.n)) {
      if (f.n === frameN) {
        if (showable && attempt.image_url !== null) {
          out.push({ n: f.n, hold: f.hold, url: attempt.image_url });
        }
      } else if (f.status === "approved") {
        const url = frameImageUrl(runId, f.n);
        if (preload[url] !== "error") out.push({ n: f.n, hold: f.hold, url });
      }
    }
    return out;
  }, [status.frames, frameN, showable, attempt.image_url, runId, preload]);
  const currentIndex = loopEntries.findIndex((e) => e.n === frameN);
  const loop = useRockLoop(loopEntries, Math.max(currentIndex, 0));
  const canRock = showable && currentIndex >= 0 && loopEntries.length >= 2;

  // the cel on screen: the playhead while rocking, else the shown take
  const cel = loop.playhead;
  const celUrl = cel ? cel.url : showable ? attempt.image_url : null;

  // -- ↑/↓ walk frames: the adjacent REVIEWABLE stops (a pending frame has
  //    nothing to screen — the walk skips it) -----------------------------
  const navigate = useNavigate();
  const reviewable = status.frames
    .filter((f) => f.status === "approved" || f.status === "generated")
    .map((f) => f.n)
    .sort((a, b) => a - b);
  const prevN = [...reviewable].reverse().find((m) => m < frameN) ?? null;
  const nextN = reviewable.find((m) => m > frameN) ?? null;
  const walk = (m: number | null) => {
    if (m !== null) {
      navigate(`/runs/${encodeURIComponent(runId)}/frames/${m}`);
    }
  };

  // the ? cheat-sheet — the discoverability backstop
  const [cheatOpen, setCheatOpen] = useState(false);

  // -- keyboard focus ownership: the stage region owns the eye-gate keys;
  //    typing targets are ignored (the retry note rides on this) ----------
  const regionRef = useRef<HTMLElement>(null);
  useEffect(() => {
    regionRef.current?.focus();
  }, []);

  const isTypingTarget = (t: EventTarget | null) => {
    const tag = (t as HTMLElement | null)?.tagName;
    return tag === "INPUT" || tag === "TEXTAREA";
  };
  const onKeyDown = (e: React.KeyboardEvent) => {
    if (isTypingTarget(e.target)) return;
    if (e.metaKey || e.ctrlKey) return; // ⌘K etc. belong to the shell
    if (e.key === " ") {
      e.preventDefault();
      if (!e.repeat && canRock) loop.start();
      return;
    }
    if (e.key === "ArrowUp") {
      e.preventDefault();
      walk(prevN);
      return;
    }
    if (e.key === "ArrowDown") {
      e.preventDefault();
      walk(nextN);
      return;
    }
    if (e.key === "?") {
      setCheatOpen((o) => !o);
      return;
    }
    if (e.key === "Escape") {
      setCheatOpen(false);
      return;
    }
    if (/^[1-9]$/.test(e.key)) {
      const take = attempts.find((a) => a.attempt === Number(e.key));
      if (take) setShown(take.attempt);
    }
  };
  const onKeyUp = (e: React.KeyboardEvent) => {
    if (isTypingTarget(e.target)) return;
    if (e.key === " ") loop.stop();
  };

  return (
    <section
      className="eg-screen"
      data-testid="eyegate"
      role="region"
      aria-label={`${label} — the stage. Hold Space to run the loop; number keys switch takes.`}
      tabIndex={0}
      ref={regionRef as React.RefObject<HTMLElement & HTMLDivElement>}
      onKeyDown={onKeyDown}
      onKeyUp={onKeyUp}
    >
      <header className="eg-head">
        <h1 className="eg-h1">{label} · the screening</h1>
        <Timecode
          frame={(cel?.n ?? frameN) - 1}
          hold={cel ? (cel.hold ?? 2) : hold}
        />
      </header>

      <div className="eg-stagewrap">
        <div className="eg-beam" aria-hidden="true" />
        <figure
          className={
            loop.running ? "eg-stage eg-stage--running" : "eg-stage"
          }
          data-testid="stage"
          aria-label={`${label} take ${attempt.attempt}, projected`}
        >
          {celUrl !== null ? (
            <div className="eg-img eg-img--lit">
              <img
                src={celUrl}
                alt={
                  cel && cel.n !== frameN
                    ? `${frameLabel(cel.n)} — rocking the loop`
                    : `${label} take ${attempt.attempt} — the candidate on screen`
                }
                onError={
                  cel
                    ? undefined
                    : () =>
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
        <CheatSheet open={cheatOpen} />
      </div>

      <div className="eg-transport">
        <div className="eg-row">
          {/* the visible Space (a11y discoverability): hold to rock */}
          <button
            type="button"
            className="eg-tsw"
            aria-pressed={loop.running}
            aria-label="Run the loop (hold Space)"
            disabled={!canRock}
            onMouseDown={() => canRock && loop.start()}
            onMouseUp={loop.stop}
            onMouseLeave={loop.stop}
          >
            Run <span className="eg-kx" aria-hidden="true">SPACE</span>
          </button>
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
          <StageToolbar
            canPrint={showable}
            onPrint={() => {}}
            canAgain={true}
            onAgain={() => {}}
            prevN={prevN}
            nextN={nextN}
            onWalk={walk}
            cheatOpen={cheatOpen}
            onToggleCheat={() => setCheatOpen((o) => !o)}
          />
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
