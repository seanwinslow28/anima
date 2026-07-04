import { defineConfig, type UserConfig } from "vite";
import react from "@vitejs/plugin-react";

// The daemon runs as a sidecar on 127.0.0.1:8000. In dev, Vite proxies the
// read endpoints to it so the browser talks same-origin (no CORS, no server/
// edit). Production (the desktop shell) will point at the same local daemon.
const DAEMON = "http://127.0.0.1:8000";

// `test` is Vitest config, read at runtime from this file. We keep Vite's own
// defineConfig (so the react() plugin type matches the top-level Vite, not
// Vitest's nested copy) and cast to UserConfig to carry the extra `test` key —
// the canonical dual-Vite workaround.
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/runs": DAEMON,
      "/health": DAEMON,
      "/jobs": DAEMON,
    },
  },
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: ["./src/test/setup.ts"],
    css: false,
  },
} as UserConfig);
