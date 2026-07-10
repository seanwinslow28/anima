import { Outlet, Route, Routes, useParams } from "react-router-dom";

import { BoothShell } from "./booth/BoothShell";
import { RunProvider } from "./lib/runContext";
import { Dashboard } from "./screens/Dashboard";
import { SystemSheet } from "./screens/dev/SystemSheet";
import { AnimaticGate } from "./screens/gates/AnimaticGate";
import { EyeGate } from "./screens/gates/EyeGate";
import { PlanGate } from "./screens/gates/PlanGate";
import { ScriptGate } from "./screens/gates/ScriptGate";
import { StoryboardGate } from "./screens/gates/StoryboardGate";
import { RunOverview } from "./screens/RunOverview";

/**
 * The single-window shell: the booth (U1's BoothShell — chrome, film grain,
 * the `.reelone` token scope) around the routed stage.
 *
 * URL scheme (decided in U1 — downstream units bind these; each gate route
 * lands WITH its own unit, pointing at a real screen — no placeholders):
 *
 *   /                        Dashboard — the marquee            (v1a, re-skin U2a)
 *   /runs/:id                Run overview — the booth board     (U2b)
 *   /runs/:id/plan           Plan gate — the read               (U3)
 *   /runs/:id/script         Script gate — the read             (U4a)
 *   /runs/:id/storyboard     Storyboard gate — the continuity   (U4b)
 *   /runs/:id/animatic       Animatic gate — placement, opt-in  (U4c; absent
 *                            from the stepper when !animatic_enabled)
 *   /runs/:id/frames/:n      Eye-gate — the screening           (U5)
 *   /dev/system              REEL ONE living token sheet        (U0)
 *
 * Everything under /runs/:id sits in one RunProvider (U3's runContext), so
 * the overview and the active gate share a single /status source of truth
 * plus the live poll of the job that owns the run.
 */
export default function App() {
  return (
    <BoothShell>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/runs/:id" element={<RunScope />}>
          <Route index element={<RunOverview />} />
          <Route path="plan" element={<PlanGate />} />
          <Route path="script" element={<ScriptGate />} />
          <Route path="storyboard" element={<StoryboardGate />} />
          <Route path="animatic" element={<AnimaticGate />} />
          {/* U5: the eye-gate — the screening */}
          <Route path="frames/:n" element={<EyeGate />} />
        </Route>
        {/* U0 dev-only reference: the REEL ONE living token sheet */}
        <Route path="/dev/system" element={<SystemSheet />} />
      </Routes>
    </BoothShell>
  );
}

/** The layout route binding the URL's run id to the run-scoped context. */
function RunScope() {
  const { id = "" } = useParams();
  return (
    <RunProvider runId={id}>
      <Outlet />
    </RunProvider>
  );
}
