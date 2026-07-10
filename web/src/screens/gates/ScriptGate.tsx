import { useState } from "react";

import { BeatsSheet } from "./BeatsSheet";
import { GateShell } from "./GateShell";
import { Markdown } from "./Markdown";
import { fetchArtifact, fetchArtifactJson } from "../../api/client";
import type { BeatSheet } from "../../api/types";
import { useRun } from "../../lib/runContext";
import { useResource } from "../../lib/useResource";

/**
 * The Script gate (/runs/:id/script — U4a): Sam's script.md as the
 * screenplay lit page, with the INSTANT Script ⇄ Beats toggle — both
 * artifacts are fetched once and the toggle is pure client view state, no
 * reload. ONE action (Approve — print it, ⌘⏎) rides U3's useGateAction. No
 * send-back (G7); "not ready?" is a CLI re-run on disk, then re-read. A
 * back-compat run never routes here (U2b omits the segment); reached
 * directly, the 404 script reads as an honest "no script for this run".
 */
export function ScriptGate({ pollIntervalMs: _pollIntervalMs }: { pollIntervalMs?: number }) {
  const { runId } = useRun();
  const [nonce, setNonce] = useState(0);
  const [view, setView] = useState<"script" | "beats">("script");

  const script = useResource(() => fetchArtifact(runId, "script"), [runId, nonce]);
  const beats = useResource(
    () => fetchArtifactJson<BeatSheet>(runId, "beats"),
    [runId, nonce],
  );

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
      actions={null}
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
