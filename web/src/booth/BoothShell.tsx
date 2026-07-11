import "./booth.css";

import type { ReactNode } from "react";

import { AppHeader } from "../components/AppHeader";
import { FilmGrain } from "../reelone/FilmGrain";
import { Intercom } from "../reelone/Intercom";
import { CommandPalette } from "./CommandPalette";
import { HudHost, useHud } from "./HudHost";

/**
 * The fading HUD layer. ONLY shell chrome lives inside it — a screen's
 * primary content is never a child of .booth-hud (the D-B hard rule: the
 * room disappears, the work never does).
 */
function BoothChrome() {
  const { chromeHidden } = useHud();
  return (
    <div className={chromeHidden ? "booth-hud booth-hud--idle" : "booth-hud"}>
      <AppHeader />
    </div>
  );
}

/**
 * The room. Wraps every routed screen in the booth chrome: U0's `.reelone`
 * token scope (load-bearing — tokens are scoped to `.reelone`, NOT :root),
 * the film-grain overlay, the summonable-HUD provider, the app bar, and the
 * <main> stage the router renders into.
 */
export function BoothShell({ children }: { children: ReactNode }) {
  return (
    <div className="reelone booth">
      <FilmGrain />
      <HudHost>
        <BoothChrome />
        <main className="booth-stage">{children}</main>
        <Intercom />
        {/* Summoned UI, not idle chrome — lives outside .booth-hud. */}
        <CommandPalette />
      </HudHost>
    </div>
  );
}
