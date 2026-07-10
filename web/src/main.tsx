// Self-hosted fonts (so the eventual offline desktop shell works) — the two-font
// rule: Newsreader 400/500 + JetBrains Mono 400. No third family, ever.
import "@fontsource/newsreader/400.css";
import "@fontsource/newsreader/500.css";
import "@fontsource/jetbrains-mono/400.css";
import "./styles/tokens.css";
// The REEL ONE layer (v1b) EXTENDS the warm tokens — booth palette scoped to
// .reelone surfaces, so v1a screens are untouched until each re-skin slice.
import "./styles/reelone.tokens.css";
import "./styles/reelone.motion.css";
import "./styles/app.css";

import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";

import App from "./App";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <BrowserRouter
      future={{ v7_startTransition: true, v7_relativeSplatPath: true }}
    >
      <App />
    </BrowserRouter>
  </StrictMode>,
);
