import type { ReactNode } from "react";

import "../../styles/gates.css";

/**
 * The reusable lit-page document-gate frame (U3; U4's three gates reuse it):
 * a cream --page sheet under the lamp in the dark booth, the gate title as
 * the screen's ONE h1, the artifact body as the page, an optional secondary
 * column, and the action bar. Density mandate: the artifact IS the page;
 * secondary panels (cost detail, provenance) reveal on intent inside the
 * aside — the primary content never timed-fades (D-B: you don't dim a page
 * you're reading).
 */
export function GateShell({
  stamp,
  title,
  byline,
  children,
  aside,
  actions,
}: {
  /** The mono corner stamp, e.g. "PLAN · REEL ONE". */
  stamp: string;
  /** The gate's h1. */
  title: string;
  /** Who authored the artifact, e.g. "authored by Maya · Opus". */
  byline?: string;
  /** The artifact body — rendered inside the lit page. */
  children: ReactNode;
  /** Secondary column (cost preview, slates). Optional. */
  aside?: ReactNode;
  /** The action bar — the one decision lives here. */
  actions: ReactNode;
}) {
  return (
    <section className="gate-screen" data-testid="gate-shell">
      <div className="gate-columns">
        <div className="gate-lampwrap">
          <article className="gate-page">
            <div className="gate-stamp">
              <span className="gate-mono">{stamp}</span>
            </div>
            <h1 className="gate-title">{title}</h1>
            {byline && <p className="gate-byline">{byline}</p>}
            <div className="gate-body">{children}</div>
          </article>
        </div>
        {aside && <aside className="gate-aside">{aside}</aside>}
      </div>
      <footer className="gate-actions">{actions}</footer>
    </section>
  );
}
