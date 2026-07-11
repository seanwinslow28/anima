import "../../styles/eyegate.css";

import { useEffect, useLayoutEffect, useMemo, useRef, useState } from "react";
import { Link, useLocation, useNavigate, useParams } from "react-router-dom";

import { fetchArtifact, fetchCandidates, frameImageUrl } from "../../api/client";
import type {
  CandidateAttempt,
  FrameState,
  GateAction,
  RunStatus,
} from "../../api/types";
import { useHudOptional } from "../../booth/HudHost";
import { framesToReel, nextActionUrl } from "../../lib/boothBoard";
import { useImagePreload } from "../../lib/imagePreload";
import { parseShots } from "../../lib/shots";
import { useRun } from "../../lib/runContext";
import { useGateAction, type GateFlow } from "../../lib/useGateAction";
import { useResource } from "../../lib/useResource";
import { useRockLoop, type LoopEntry } from "../../lib/useRockLoop";
import { BurnIn } from "../../reelone/BurnIn";
import { CircledTake } from "../../reelone/CircledTake";
import { Filmstrip } from "../../reelone/Filmstrip";
import { callIntercom } from "../../reelone/Intercom";
import { RitualLeader } from "../../reelone/RitualLeader";
import { Timecode } from "../../reelone/Timecode";
import { CheatSheet } from "./CheatSheet";
import { EmReadout } from "./EmReadout";
import { DiffWipe, WipeControls, type WipeSource } from "./DiffWipe";
import { OnionSkin, type GhostSource } from "./OnionSkin";
import { composeEmNote, RetryNoteRow } from "./RetryNoteRow";
import { StageToolbar } from "./StageToolbar";

/*
 * The eye-gate (U5a + U5b) — the screening AND the decision. The stage is
 * the only bright object in the room: the current frame's shown take, lit,
 * alone; takes switch under it; Em reads from the margin. U5b adds the two
 * commits over U3's job flow: PRINT (⏎ — approve the shown take -> the
 * circled take -> the ritual leader -> cel-flip advance on the inline
 * next_action) and AGAIN (R — retry with Em's fix prefilled). Reads are all
 * client-side (D-E): /status through the run scope + GET
 * /frames/{n}/candidates + GET /frames/{n}/image?attempt=K as <img> srcs.
 * Onion/diff/lights are U5c.
 */

/** The G5 constants the burn-in + provenance lines are composed from. */
const FPS_LINE = "12 FPS";
const MODEL_LINE = "NB2";
const FRAME_COST_LINE = "$0.07";

const frameLabel = (n: number) => `F${String(n).padStart(2, "0")}`;

/** jsdom has no matchMedia; its absence reads as motion-allowed (U0 pattern). */
const reducedMotion = () =>
  typeof window.matchMedia === "function" &&
  window.matchMedia("(prefers-reduced-motion: reduce)").matches;

/** What Screening needs from the decision layer (owned by EyeGate — it must
 *  survive the run-scope /status re-read that unmounts Screening). */
interface DecisionGate {
  flow: GateFlow;
  decision: "print" | "again" | null;
  printTake: (attempt: number) => void;
  againNote: (note: string) => void;
  retryLast: () => void;
  backToGate: () => void;
}

export function EyeGate({ pollIntervalMs }: { pollIntervalMs?: number } = {}) {
  const { n = "" } = useParams();
  const frameN = Number(n);
  const { runId, status, refresh } = useRun();
  const navigate = useNavigate();
  const [nonce, setNonce] = useState(0);
  const candidates = useResource(
    () => fetchCandidates(runId, frameN),
    [runId, frameN, nonce],
  );

  const reload = () => {
    refresh();
    setNonce((x) => x + 1);
  };

  // The shots artifact — read ONLY for chain_from (the loop anchor, U5c
  // onion). A soft read: an unreadable/absent board costs the loop-return
  // ghost, never the screening (the .catch collapses it to null).
  const shots = useResource(
    () =>
      fetchArtifact(runId, "shots")
        .then(parseShots)
        .catch(() => null),
    [runId],
  );
  const chainFrom =
    shots.status === "ready" && shots.data !== null
      ? (shots.data.frames.find((f) => f.id === frameN)?.chain_from ?? null)
      : null;

  // -- the decision layer (U5b): print/again through U3's job flow --------
  // One useGateAction serves both commits (the single-writer run allows one
  // job at a time anyway); `decision` remembers which one is in flight for
  // the veil caption and the terminal handling. It lives HERE, not in
  // Screening: the hook's terminal refreshRun() flips the run-scope /status
  // resource through loading, which swaps Screening for the skeleton — the
  // flow must survive that unmount.
  const frameBase = `/runs/${encodeURIComponent(runId)}/frames/${frameN}`;
  const { flow, submit, reset } = useGateAction(
    runId,
    { method: "POST", path: `${frameBase}/approve` },
    { pollIntervalMs },
  );
  const [decision, setDecision] = useState<"print" | "again" | null>(null);
  const lastAction = useRef<GateAction | null>(null);
  const pendingIntercom = useRef<string | null>(null);
  const lastStatus = useRef<RunStatus | null>(null);

  const dispatch = (mode: "print" | "again", action: GateAction) => {
    setDecision(mode);
    lastAction.current = action;
    submit(action);
  };

  // walking to another frame abandons this frame's decision state
  useEffect(() => {
    setDecision(null);
    reset();
  }, [frameN, reset]);

  // ADVANCE only on the full success shape — the destination is the INLINE
  // next_action. A re-shoot landing back on THIS frame re-reads the takes
  // instead of navigating; assemble/done route to the overview. Consumed
  // exactly once (the effect re-fires when frameN flips mid-advance).
  const consumedAdvance = useRef(false);
  useEffect(() => {
    if (flow.phase !== "advanced") {
      consumedAdvance.current = false;
      return;
    }
    if (consumedAdvance.current) return;
    consumedAdvance.current = true;
    if (pendingIntercom.current !== null) {
      callIntercom(pendingIntercom.current);
      pendingIntercom.current = null;
    }
    const na = flow.nextAction;
    if (na.kind === "review_frame" && na.frame === frameN) {
      setDecision(null);
      reset();
      setNonce((x) => x + 1);
      return;
    }
    navigate(
      nextActionUrl(runId, na) ?? `/runs/${encodeURIComponent(runId)}`,
      { state: { celFlip: true } },
    );
  }, [flow, frameN, runId, navigate, reset]);

  // cancelled -> back to the gate
  useEffect(() => {
    if (flow.phase === "cancelled") {
      setDecision(null);
      reset();
    }
  }, [flow, reset]);

  const gate: DecisionGate = {
    flow,
    decision,
    printTake: (attempt) => {
      pendingIntercom.current = `${frameLabel(frameN)} TAKE ${attempt} — PRINTED. ${FRAME_COST_LINE} to the ledger.`;
      dispatch("print", {
        method: "POST",
        path: `${frameBase}/approve?attempt=${attempt}`,
      });
    },
    againNote: (note) => {
      pendingIntercom.current = `GO AGAIN — note sent as a correction. Flo re-shoots ${frameLabel(frameN)}.`;
      dispatch("again", {
        method: "POST",
        path: `${frameBase}/retry`,
        body: { note },
      });
    },
    retryLast: () => {
      if (lastAction.current) submit(lastAction.current);
    },
    backToGate: () => {
      setDecision(null);
      reset();
      reload();
    },
  };

  // Keep the last ready /status so the run-scope re-read (fired on every job
  // terminal) never blanks the lit stage back to the skeleton mid-decision —
  // the projection updates in place; the skeleton is for the FIRST read only.
  if (status.status === "ready") lastStatus.current = status.data;
  const statusData =
    status.status === "ready" ? status.data : lastStatus.current;

  if (
    candidates.status === "loading" ||
    (status.status === "loading" && statusData === null)
  ) {
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
          <button type="button" className="eg-retry ro-button ro-button--primary" onClick={reload}>
            Retry
          </button>
        </div>
      </section>
    );
  }

  // statusData is non-null past the gates above (loading requires it null;
  // error returned); the assertion keeps the narrowing local.
  const runStatus = statusData as RunStatus;
  const frameState = runStatus.frames.find((f) => f.n === frameN) ?? null;
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
      status={runStatus}
      attempts={candidates.data}
      chainFrom={chainFrom}
      gate={gate}
    />
  );
}

/** The ready state: the lit stage + Em's margin + takes + the decision. */
function Screening({
  runId,
  frameN,
  frameState,
  status,
  attempts,
  chainFrom,
  gate,
}: {
  runId: string;
  frameN: number;
  frameState: FrameState | null;
  status: RunStatus;
  attempts: CandidateAttempt[];
  /** the loop anchor from the shots artifact (null: not a loop-return) */
  chainFrom: number | null;
  gate: DecisionGate;
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

  // -- hover-skim (U5c): a reel cell under the mouse PEEKS that frame on the
  //    stage without moving the reviewed frame (the FCP skimmer; the
  //    keyboard equivalent is the ↑↓ walk). Only a frame with a print to
  //    serve peeks; leaving restores the take. ----------------------------
  const [peekN, setPeekN] = useState<number | null>(null);
  const peek = (id: string | number) => {
    const f = status.frames.find((x) => x.n === Number(id));
    if (
      f &&
      f.n !== frameN &&
      (f.status === "approved" || f.status === "generated")
    ) {
      setPeekN(f.n);
    }
  };
  const peekEnd = () => setPeekN(null);
  const peekUrl = peekN !== null ? frameImageUrl(runId, peekN) : null;

  // the cel on screen: the playhead while rocking, else the peek, else the
  // shown take
  const cel = loop.playhead;
  const celUrl =
    cel?.url ?? peekUrl ?? (showable ? attempt.image_url : null);

  // -- onion-skin (U5c "O"): ghost the approved N-1 under the candidate,
  //    plus the chain_from anchor on a loop-return (deduped when they
  //    coincide). Sources exist only where a print actually exists — the
  //    ghost is always a real approved frame, never the Bible anchor (G9). --
  const [onion, setOnion] = useState(false);
  const ghosts = useMemo(() => {
    const out: GhostSource[] = [];
    const priorApproved = status.frames
      .filter((f) => f.status === "approved" && f.n < frameN)
      .reduce<number | null>((best, f) => (best === null || f.n > best ? f.n : best), null);
    if (priorApproved !== null) {
      out.push({
        n: priorApproved,
        url: frameImageUrl(runId, priorApproved),
        role: "N-1",
      });
    }
    if (
      chainFrom !== null &&
      chainFrom !== priorApproved &&
      status.frames.some((f) => f.n === chainFrom && f.status === "approved")
    ) {
      out.push({ n: chainFrom, url: frameImageUrl(runId, chainFrom), role: "LOOP" });
    }
    return out;
  }, [status.frames, frameN, chainFrom, runId]);
  const canGhost = showable && ghosts.length > 0;
  const toggleOnion = () => {
    if (canGhost) setOnion((o) => !o);
  };

  // -- diff-wipe (U5c "D"): compare the shown take against another attempt
  //    or the approved prior — the two comparators the daemon actually
  //    serves. The Bible anchor is NOT one (G9): no anchor path exists. ----
  const [diff, setDiff] = useState(false);
  const [wipe, setWipe] = useState(50);
  const [compareKey, setCompareKey] = useState<string | null>(null);
  const compareOptions = useMemo(() => {
    const opts: WipeSource[] = [];
    for (const a of attempts) {
      if (
        a.attempt !== attempt.attempt &&
        a.image_url !== null &&
        a.status !== "errored" &&
        !broken.has(a.attempt)
      ) {
        opts.push({
          key: `take-${a.attempt}`,
          label: `TAKE ${a.attempt}`,
          url: a.image_url,
        });
      }
    }
    const prior = ghosts.find((g) => g.role === "N-1");
    if (prior) {
      opts.push({
        key: "prior",
        label: `${frameLabel(prior.n)} PRINT`,
        url: prior.url,
      });
    }
    return opts;
  }, [attempts, attempt.attempt, broken, ghosts]);
  const canDiff = showable && compareOptions.length > 0;
  const compare =
    compareOptions.find((o) => o.key === compareKey) ?? compareOptions[0] ?? null;
  const toggleDiff = () => {
    if (canDiff) setDiff((d) => !d);
  };
  const dragWipe = (delta: number) => {
    if (diff && canDiff) setWipe((w) => Math.max(0, Math.min(100, w + delta)));
  };

  // -- lights-out (U5c "L"): ALL chrome drops — the frame (or the running
  //    loop) alone on the dark stage; L again restores. A decision terminal
  //    still surfaces (honesty beats ritual). -----------------------------
  const [lights, setLights] = useState(false);

  // -- the summonable HUD (U5c — the signature): the eye-gate opts into
  //    U1's "full" dim level; idle ~3s and the booth chrome fades to almost
  //    nothing, any input wakes it. The frame and the decision are the only
  //    permanent things. HudHost already honors reduced motion (no timed
  //    fade); bare mounts (unit tests) have no HUD and never dim. ---------
  const hud = useHudOptional();
  const declareDim = hud?.declareDimLevel;
  const releaseDim = hud?.releaseDimLevel;
  useLayoutEffect(() => {
    if (!declareDim || !releaseDim) return;
    declareDim("full");
    return releaseDim;
  }, [declareDim, releaseDim]);
  const boothDark =
    (hud?.chromeHidden ?? false) && hud?.dimLevel === "full";

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

  // -- the decision layer's view of THIS screening ------------------------
  const { flow, decision } = gate;
  // the single-writer rule made visible: a job owns the run -> no commits
  const blockedBy = status.next_action.blocked_by_job ?? null;
  const gateIdle = flow.phase === "idle";
  const canPrint = showable && gateIdle && blockedBy === null;
  const canAgain = gateIdle && blockedBy === null;
  const print = () => {
    if (!canPrint) return;
    gate.printTake(attempt.attempt);
  };

  // AGAIN: the note row, prefilled from Em's read of the SHOWN take.
  // Opening it pauses the loop — you write with the picture still.
  const [againOpen, setAgainOpen] = useState(false);
  const emNote = composeEmNote(attempt.em);
  const openAgain = () => {
    if (!canAgain) return;
    loop.stop();
    setAgainOpen(true);
  };
  const cancelAgain = () => {
    setAgainOpen(false);
    regionRef.current?.focus();
  };
  const sendAgain = (note: string) => {
    setAgainOpen(false);
    gate.againNote(note);
  };

  const jobRunning = flow.phase === "submitting" || flow.phase === "working";
  // the circled take: the grease-pencil flourish on the take being printed
  const circledTake =
    decision === "print" && (jobRunning || flow.phase === "advanced")
      ? attempt.attempt
      : null;
  const noticeUp =
    flow.phase === "failed" ||
    flow.phase === "busy" ||
    flow.phase === "stale" ||
    flow.phase === "degraded" ||
    flow.phase === "error";

  // the cel-flip arrival: this screening was navigated to by a print — the
  // next picture comes up through black (reduced motion: a soft crossfade,
  // never a dead cut)
  const location = useLocation();
  const celFlip =
    (location.state as { celFlip?: boolean } | null)?.celFlip === true;

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
    if (e.key === "Enter") {
      e.preventDefault();
      print();
      return;
    }
    if (e.key === "r" || e.key === "R") {
      e.preventDefault();
      openAgain();
      return;
    }
    if (e.key === "o" || e.key === "O") {
      toggleOnion();
      return;
    }
    if (e.key === "d" || e.key === "D") {
      toggleDiff();
      return;
    }
    if (e.key === "[") {
      dragWipe(-4);
      return;
    }
    if (e.key === "]") {
      dragWipe(4);
      return;
    }
    if (e.key === "l" || e.key === "L") {
      setLights((v) => !v);
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

  // the diff wipe rides the stage only while the stage is at rest on the
  // shown take (never over the rocking loop or a peek)
  const diffOn =
    diff && canDiff && compare !== null && cel === null && peekN === null;

  // idle-dark never swallows a decision terminal — honesty beats ritual
  const idleDark = boothDark && !noticeUp && !jobRunning && !againOpen;

  return (
    <section
      className={[
        "eg-screen",
        lights ? "eg-screen--lights" : "",
        idleDark ? "eg-screen--idledark" : "",
      ]
        .filter(Boolean)
        .join(" ")}
      data-testid="eyegate"
      role="region"
      aria-label={`${label} — the stage. Hold Space to run the loop; number keys switch takes.`}
      tabIndex={0}
      ref={regionRef as React.RefObject<HTMLElement & HTMLDivElement>}
      onKeyDown={onKeyDown}
      onKeyUp={onKeyUp}
    >
      {!lights && (
        <header className="eg-head">
          <h1 className="eg-h1">{label} · the screening</h1>
          <Timecode
            frame={(cel?.n ?? frameN) - 1}
            hold={cel ? (cel.hold ?? 2) : hold}
          />
        </header>
      )}

      <div className="eg-stagewrap">
        <div className="eg-stagecol">
          <div className="eg-beam" aria-hidden="true" />
          <figure
            className={[
              "eg-stage",
              loop.running ? "eg-stage--running" : "",
              celFlip
                ? reducedMotion()
                  ? "eg-stage--arrive-soft"
                  : "eg-stage--arrive"
                : "",
            ]
              .filter(Boolean)
              .join(" ")}
            data-testid="stage"
            aria-label={`${label} take ${attempt.attempt}, projected`}
          >
            {diffOn && attempt.image_url !== null ? (
              <DiffWipe
                base={{
                  key: "base",
                  label: `TAKE ${attempt.attempt}`,
                  url: attempt.image_url,
                }}
                compare={compare}
                wipe={wipe}
              />
            ) : celUrl !== null ? (
              <div className={loop.running ? "eg-img eg-img--lit ro-weave" : "eg-img eg-img--lit"}>
                <img
                  className="ro-flicker"
                  src={celUrl}
                  alt={
                    cel && cel.n !== frameN
                      ? `${frameLabel(cel.n)} — rocking the loop`
                      : peekN !== null
                        ? `${frameLabel(peekN)} — peeking the reel`
                        : `${label} take ${attempt.attempt} — the candidate on screen`
                  }
                  onError={
                    cel || peekN !== null
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
            {onion && canGhost && loop.playhead === null && peekN === null && (
              <OnionSkin ghosts={ghosts} />
            )}
            <div className="eg-burns">
              <span className="eg-burn">
                <BurnIn segments={[label, `TAKE ${attempt.attempt}`, `HOLD ${hold}`]} />
              </span>
              <span className="eg-burn">
                <BurnIn segments={[FPS_LINE, MODEL_LINE, FRAME_COST_LINE]} />
              </span>
            </div>
          </figure>
          {!lights && <CheatSheet open={cheatOpen} />}
          {jobRunning && (
            <div className="eg-jobveil" data-testid="gate-working">
              <div className="eg-jobveil-dial">
                <RitualLeader
                  caption={decision === "again" ? "FLO RE-SHOOTS" : "PRINTING"}
                />
              </div>
              <p className="eg-jobveil-sub">
                {decision === "again"
                  ? `Flo re-shoots ${label} — the note rides the retake`
                  : `Printing ${label} take ${attempt.attempt} — the count holds until it's really through`}
                {flow.phase === "working" && (
                  <>
                    {" "}
                    · job <span className="eg-mono">{flow.jobId}</span>
                  </>
                )}
              </p>
            </div>
          )}
        </div>
        {!lights && <EmReadout records={attempt.em} />}
      </div>

      {(!lights || noticeUp) && (
      <div className="eg-transport">
        {diffOn && (
          <WipeControls
            options={compareOptions}
            selectedKey={compare.key}
            onSelect={setCompareKey}
            wipe={wipe}
            onWipe={setWipe}
          />
        )}
        {againOpen && !noticeUp && !jobRunning && (
          <RetryNoteRow
            key={attempt.attempt}
            prefill={emNote.note}
            fromEm={emNote.fromEm}
            onSend={sendAgain}
            onCancel={cancelAgain}
          />
        )}
        {noticeUp ? (
          <DecisionNotice
            flow={flow}
            runId={runId}
            onRetry={gate.retryLast}
            onBack={gate.backToGate}
          />
        ) : (
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
                  <CircledTake on={circledTake === a.attempt} />
                </button>
              ))}
            </div>
            <StageToolbar
              canPrint={canPrint}
              onPrint={print}
              canAgain={canAgain}
              onAgain={openAgain}
              prevN={prevN}
              nextN={nextN}
              onWalk={walk}
              canGhost={canGhost}
              onionOn={onion}
              onToggleOnion={toggleOnion}
              canDiff={canDiff}
              diffOn={diff}
              onToggleDiff={toggleDiff}
              lightsOn={lights}
              onToggleLights={() => setLights((v) => !v)}
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
        )}
        <div className="eg-strip">
          <Filmstrip frames={reelFrames} onPeek={peek} onPeekEnd={peekEnd} />
        </div>
      </div>
      )}
    </section>
  );
}

/**
 * The decision's non-happy terminals, each honest with ONE recovery action
 * (the states doctrine; branch semantics from U3's classified GateFlow).
 */
function DecisionNotice({
  flow,
  runId,
  onRetry,
  onBack,
}: {
  flow: GateFlow;
  runId: string;
  onRetry: () => void;
  onBack: () => void;
}) {
  switch (flow.phase) {
    case "failed":
      return (
        <div className="eg-flownote eg-flownote--failed" role="alert">
          <p className="eg-flownote-lead">
            The take jammed in the gate — rc {flow.job.rc}
          </p>
          <pre className="eg-logs">{flow.job.logs || "(no log output)"}</pre>
          <button type="button" className="eg-flownote-act ro-button ro-button--primary" onClick={onRetry}>
            Retry
          </button>
        </div>
      );

    case "busy":
      return (
        <div className="eg-flownote eg-flownote--busy" role="alert">
          <p className="eg-flownote-lead">The booth is busy</p>
          <p className="eg-flownote-sub">
            {flow.reason} · job{" "}
            <span className="eg-mono">{flow.activeJobId}</span> has the run.
          </p>
          <Link
            className="eg-flownote-act ro-button ro-button--quiet"
            to={`/runs/${encodeURIComponent(runId)}`}
          >
            Watch the running job
          </Link>
        </div>
      );

    case "stale":
      return (
        <div className="eg-flownote" role="alert">
          <p className="eg-flownote-lead">This run already moved on</p>
          <p className="eg-flownote-sub">{flow.detail}</p>
          <button type="button" className="eg-flownote-act ro-button ro-button--primary" onClick={onBack}>
            Refresh the screening
          </button>
        </div>
      );

    case "degraded":
      return (
        <div className="eg-flownote eg-flownote--failed" role="alert">
          <p className="eg-flownote-lead">
            The take went through, but the booth couldn't re-read the run
          </p>
          <p className="eg-flownote-sub">
            The job finished (rc 0) yet the run's state wouldn't load
            {flow.job.load_error && (
              <>
                : <span className="eg-mono">{flow.job.load_error}</span>
              </>
            )}
            . Refresh before touching anything.
          </p>
          <button type="button" className="eg-flownote-act ro-button ro-button--primary" onClick={onBack}>
            Refresh
          </button>
        </div>
      );

    case "error":
      return (
        <div className="eg-flownote eg-flownote--failed" role="alert">
          <p className="eg-flownote-lead">
            The gate refused{flow.status ? ` (${flow.status})` : ""}
          </p>
          <p className="eg-flownote-sub">{flow.detail}</p>
          <button type="button" className="eg-flownote-act ro-button ro-button--primary" onClick={onBack}>
            Back to the screening
          </button>
        </div>
      );

    default:
      return null;
  }
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
