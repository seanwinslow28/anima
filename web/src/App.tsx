import { Route, Routes } from "react-router-dom";

import { AppHeader } from "./components/AppHeader";
import { Dashboard } from "./screens/Dashboard";
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
        </Routes>
      </main>
    </div>
  );
}
