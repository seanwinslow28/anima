import { Route, Routes } from "react-router-dom";

import { BoothShell } from "./booth/BoothShell";
import { Dashboard } from "./screens/Dashboard";
import { SystemSheet } from "./screens/dev/SystemSheet";
import { RunOverview } from "./screens/RunOverview";

/**
 * The single-window shell: the booth (U1's BoothShell — chrome, film grain,
 * the `.reelone` token scope) around the routed stage.
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
