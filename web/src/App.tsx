import { Route, Routes } from "react-router-dom";

import { AppHeader } from "./components/AppHeader";
import { Dashboard } from "./screens/Dashboard";
import { SystemSheet } from "./screens/dev/SystemSheet";
import { RunOverview } from "./screens/RunOverview";

/**
 * The single-window shell: warm header over a <main> stage, with client-side
 * routing between the Dashboard (run gallery) and a Run overview.
 */
export default function App() {
  return (
    <div className="app">
      <AppHeader />
      <main className="main">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/runs/:id" element={<RunOverview />} />
          {/* U0 dev-only reference: the REEL ONE living token sheet */}
          <Route path="/dev/system" element={<SystemSheet />} />
        </Routes>
      </main>
    </div>
  );
}
