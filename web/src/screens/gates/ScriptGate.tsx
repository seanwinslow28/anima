import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { BeatsSheet } from "./BeatsSheet";
import { GateShell } from "./GateShell";
import { Markdown } from "./Markdown";
import { fetchArtifact, fetchArtifactJson } from "../../api/client";
import type { BeatSheet } from "../../api/types";
import { nextActionUrl } from "../../lib/boothBoard";
import { useRun } from "../../lib/runContext";
import { useGateAction, type GateFlow } from "../../lib/useGateAction";
import { useResource } from "../../lib/useResource";
import { RitualLeader } from "../../reelone/RitualLeader";

/**
 * The Script gate (/runs/:id/script — U4a): Sam's script.md as the
 * screenplay lit page, with the INSTANT Script ⇄ Beats toggle — both
 * artifacts are fetched once and the toggle is pure client view state, no
 * reload. ONE action (Approve — print it, ⌘⏎) rides U3's useGateAction. No
 * send-back (G7); "not ready?" is a CLI re-run on disk, then re-read. A
 * back-compat run never routes here (U2b omits the segment); reached
 * directly, the 404 script reads as an honest "no script for this run".
 */
export function ScriptGate({ pollIntervalMs }: { pollIntervalMs?: number }) {
  const { runId, status, refresh } = useRun();
  const navigate = useNavigate();
  const [nonce, setNonce] = useState(0);
  const [view, setView] = useState<"script" | "beats">("script");

  const script = useResource(() => fetchArtifact(runId, "script"), [runId, nonce]);
  const beats = useResource(
    () => fetchArtifactJson<BeatSheet>(runId, "beats"),
    [runId, nonce],
  );

  const { flow, submit, reset } = useGateAction(
    runId,
    { method: "POST", path: `/runs/${encodeURIComponent(runId)}/script/approve` },
    { pollIntervalMs },
  );

  // the single-writer rule made visible: a job owns the run -> no approve
  const blockedBy =
    status.status === "ready"
      ? (status.data.next_action.blocked_by_job ?? null)
      : null;
  const canApprove = flow.phase === "idle" && blockedBy === null;

  // ADVANCE only on the full success shape — the hook already classified it;
  // the destination is the INLINE next_action (U1's URL scheme).
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

  // ⌘⏎ / Ctrl+⏎ approves
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key !== "Enter" || !(e.metaKey || e.ctrlKey)) return;
      if (!canApprove) return;
      e.preventDefault();
      submit();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [canApprove, submit]);

  if (script.status === "loading" || beats.status === "loading") {
    return (
      <section className="gate-screen" aria-hidden="true" data-testid="gate-skeleton">
        <div className="bb-sk bb-sk--hero ro-pulse" />
      </section>
    );
  }

  if (script.status === "error" || beats.status === "error") {
    const noScript =
      script.status === "error" && script.error.message.includes("(404)");
    return (
      <section className="gate-screen">
        <div className="gate-notice gate-notice--error" role="alert">
          <h2>{noScript ? "No script for this run" : "Couldn't read the script"}</h2>
          <p>
            {noScript ? (
              <>
                This run has no script on disk — a back-compat run (the brief
                carried its own shots.yaml) goes straight from plan to
                generate and never visits this gate.
              </>
            ) : (
              <>
                The booth couldn't pull this run's script — it may not be
                authored yet, or the daemon can't serve it.
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

  const sheet = beats.data;
  return (
    <GateShell
      stamp={`SCRIPT · ${sheet.slug.toUpperCase()}`}
      title="The script"
      byline="authored by Sam · the scriptwriter"
      actions={
        <ScriptGateActions
          runId={runId}
          flow={flow}
          canApprove={canApprove}
          blockedBy={blockedBy}
          submit={() => submit()}
          reset={reset}
          refreshAndReset={() => {
            refresh();
            setNonce((n) => n + 1);
            reset();
          }}
        />
      }
    >
      <div className="gate-viewtoggle" aria-label="Script or beats view">
        <button
          type="button"
          className="gate-viewbtn"
          aria-pressed={view === "script"}
          onClick={() => setView("script")}
        >
          Script
        </button>
        <button
          type="button"
          className="gate-viewbtn"
          aria-pressed={view === "beats"}
          onClick={() => setView("beats")}
        >
          Beats
        </button>
      </div>
      {view === "script" ? (
        <div className="gate-screenplay">
          <Markdown text={script.data} />
        </div>
      ) : (
        <BeatsSheet sheet={sheet} />
      )}
    </GateShell>
  );
}

/** The action bar renders the gate's flow state — every branch honest. */
function ScriptGateActions({
  runId,
  flow,
  canApprove,
  blockedBy,
  submit,
  reset,
  refreshAndReset,
}: {
  runId: string;
  flow: GateFlow;
  canApprove: boolean;
  blockedBy: string | null;
  submit: () => void;
  reset: () => void;
  refreshAndReset: () => void;
}) {
  switch (flow.phase) {
    case "submitting":
    case "working":
      return (
        <div className="gate-working" data-testid="gate-working">
          <RitualLeader caption="PRINTING THE SCRIPT" />
          <p className="gate-hint">
            Sam's script is going through the gate
            {flow.phase === "working" && (
              <>
                {" "}
                · job <span className="gate-mono">{flow.jobId}</span>
              </>
            )}
            . The count holds until the take is really through.
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
          <Link className="gate-notice-act" to={`/runs/${encodeURIComponent(runId)}`}>
            Watch the running job
          </Link>
        </div>
      );

    case "stale":
      return (
        <div className="gate-notice" role="alert">
          <h2>This run already moved on</h2>
          <p>{flow.detail}</p>
          <button type="button" className="gate-notice-act" onClick={refreshAndReset}>
            Refresh the gate
          </button>
        </div>
      );

    case "failed":
      return (
        <div className="gate-notice gate-notice--failed" role="alert">
          <h2>The take jammed in the gate — rc {flow.job.rc}</h2>
          <pre className="gate-logs">{flow.job.logs || "(no log output)"}</pre>
          <button
            type="button"
            className="gate-notice-act"
            onClick={() => {
              reset();
              submit();
            }}
          >
            Retry
          </button>
        </div>
      );

    case "degraded":
      return (
        <div className="gate-notice gate-notice--error" role="alert">
          <h2>The take developed, but the booth couldn't re-read it</h2>
          <p>
            The job finished (rc 0) yet the run's state wouldn't load
            {flow.job.load_error && (
              <>
                : <span className="gate-mono">{flow.job.load_error}</span>
              </>
            )}
            . Refresh before touching anything.
          </p>
          <button type="button" className="gate-notice-act" onClick={refreshAndReset}>
            Refresh
          </button>
        </div>
      );

    case "error":
      return (
        <div className="gate-notice gate-notice--error" role="alert">
          <h2>The gate refused{flow.status ? ` (${flow.status})` : ""}</h2>
          <p>{flow.detail}</p>
          <button type="button" className="gate-notice-act" onClick={refreshAndReset}>
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
            className="gate-approve"
            disabled={!canApprove}
            onClick={submit}
          >
            Approve — print it
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
                Approval locks the beat sheet and hands the run to Bea for the
                board. No send-back here — revise the script on disk and re-run
                from the CLI.
              </>
            )}
          </p>
        </>
      );
  }
}
