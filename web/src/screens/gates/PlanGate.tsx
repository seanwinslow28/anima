import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { CostPreview } from "./CostPreview";
import { GateShell } from "./GateShell";
import { Markdown } from "./Markdown";
import { fetchArtifact, fetchRawState } from "../../api/client";
import { nextActionUrl } from "../../lib/boothBoard";
import { hasStageMovedPast } from "../../lib/gateStage";
import { useRun } from "../../lib/runContext";
import { useGateAction, type GateFlow } from "../../lib/useGateAction";
import { useResource } from "../../lib/useResource";
import { RitualLeader } from "../../reelone/RitualLeader";
import { callIntercom } from "../../reelone/Intercom";

/**
 * The Plan gate (/runs/:id/plan) — the simplest document gate, proving the
 * whole D-C flow: Maya's plan.md as the lit page, the cost preview
 * ("estimate, not a cap"), ONE primary action (Approve — print it, ⌘⏎) ->
 * 202 -> the ritual leader -> terminal -> advance on the INLINE
 * next_action. No send-back exists (G7 — not a daemon action); "not ready?"
 * is a CLI re-run on disk, then re-read.
 */
export function PlanGate({ pollIntervalMs }: { pollIntervalMs?: number }) {
  const { runId, status, refresh } = useRun();
  const navigate = useNavigate();
  const [nonce, setNonce] = useState(0);

  const plan = useResource(() => fetchArtifact(runId, "plan"), [runId, nonce]);
  const raw = useResource(() => fetchRawState(runId), [runId, nonce]);

  const { flow, submit, reset } = useGateAction(
    runId,
    { method: "POST", path: `/runs/${encodeURIComponent(runId)}/plan/approve` },
    { pollIntervalMs },
  );

  // the single-writer rule made visible: a job owns the run -> no approve
  const blockedBy =
    status.status === "ready"
      ? (status.data.next_action.blocked_by_job ?? null)
      : null;
  const archived =
    status.status === "ready" && hasStageMovedPast(status.data.stage, "PLAN");
  const canApprove = flow.phase === "idle" && blockedBy === null && !archived;

  // ADVANCE only on the full success shape — the hook already classified it;
  // the destination is the INLINE next_action (U1's URL scheme).
  useEffect(() => {
    if (flow.phase !== "advanced") return;
    callIntercom("PLAN PRINTED — criteria locked. Sam takes the next pass.");
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

  if (plan.status === "loading" || raw.status === "loading") {
    return (
      <section className="gate-screen" aria-hidden="true" data-testid="gate-skeleton">
        <div className="bb-sk bb-sk--hero ro-pulse" />
      </section>
    );
  }

  if (plan.status === "error" || raw.status === "error") {
    return (
      <section className="gate-screen">
        <div className="gate-notice gate-notice--error" role="alert">
          <h2>Couldn't read the plan</h2>
          <p>
            The booth couldn't pull this run's plan.md — it may not be drafted
            yet, or the daemon can't serve it.
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

  const slug = raw.data.slug;
  return (
    <GateShell
      stamp={`PLAN · ${slug.toUpperCase()}`}
      title="The plan"
      byline="authored by Maya · the planner"
      archiveMark={archived ? "PRINTED" : undefined}
      aside={<CostPreview estimate={raw.data.plan.cost_estimate} />}
      actions={archived ? undefined : (
        <PlanGateActions
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
      )}
    >
      <Markdown text={plan.data} />
    </GateShell>
  );
}

/** The action bar renders the gate's flow state — every branch honest. */
function PlanGateActions({
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
          <RitualLeader caption="PRINTING THE PLAN" />
          <p className="gate-hint">
            Maya's plan is going through the gate
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

    case "failed":
      return (
        <div className="gate-notice gate-notice--failed" role="alert">
          <h2>The take jammed in the gate — rc {flow.job.rc}</h2>
          <pre className="gate-logs">{flow.job.logs || "(no log output)"}</pre>
          <button type="button" className="gate-notice-act ro-button ro-button--primary" onClick={() => {
            reset();
            submit();
          }}>
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
                Approval locks the criteria and starts the print. Nothing burns
                compute until you approve. No send-back here — revise the brief
                on disk and re-plan from the CLI.
              </>
            )}
          </p>
        </>
      );
  }
}
