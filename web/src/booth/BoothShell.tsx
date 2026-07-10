import "./booth.css";

import type { ReactNode } from "react";

import { AppHeader } from "../components/AppHeader";
import { FilmGrain } from "../reelone/FilmGrain";

/**
 * The room. Wraps every routed screen in the booth chrome: U0's `.reelone`
 * token scope (load-bearing — tokens are scoped to `.reelone`, NOT :root),
 * the film-grain overlay, the app bar, and the <main> stage the router
 * renders into.
 */
export function BoothShell({ children }: { children: ReactNode }) {
  return (
    <div className="reelone booth">
      <FilmGrain />
      <AppHeader />
      <main className="booth-stage">{children}</main>
    </div>
  );
}
