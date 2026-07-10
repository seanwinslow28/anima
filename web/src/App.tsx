import { Route, Routes } from "react-router-dom";

import { BoothShell } from "./booth/BoothShell";
import { Dashboard } from "./screens/Dashboard";
import { SystemSheet } from "./screens/dev/SystemSheet";
import { RunOverview } from "./screens/RunOverview";

/**
 * The single-window shell: the booth (U1's BoothShell — chrome, film grain,
 * the `.reelone` token scope) around the routed stage.
 *
 * URL scheme (decided in U1 — downstream units bind these; each gate route
 * lands WITH its own unit, pointing at a real screen — no placeholders):
 *
 *   /                        Dashboard — the marquee            (v1a, re-skin U2a)
 *   /runs/:id                Run overview — the booth board     (stub, built U2b)
 *   /runs/:id/plan           Plan gate — the read               (U3)
 *   /runs/:id/script         Script gate — the read             (U4a)
 *   /runs/:id/storyboard     Storyboard gate — the continuity   (U4b)
 *   /runs/:id/animatic       Animatic gate — placement, opt-in  (U4c; absent
 *                            from the stepper when !animatic_enabled)
 *   /runs/:id/frames/:n      Eye-gate — the screening           (U5)
 *   /dev/system              REEL ONE living token sheet        (U0)
 */
export default function App() {
  return (
    <BoothShell>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/runs/:id" element={<RunOverview />} />
        {/* U0 dev-only reference: the REEL ONE living token sheet */}
        <Route path="/dev/system" element={<SystemSheet />} />
      </Routes>
    </BoothShell>
  );
}
