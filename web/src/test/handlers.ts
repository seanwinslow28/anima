import { http, HttpResponse } from "msw";
import { setupServer } from "msw/node";

import {
  beatsFixture,
  candidatesFlagPass,
  rawAuthoring,
  runApprovePlan,
  runReviewFrame,
  scriptMd,
  shotsYaml,
  statusReviewFrame,
  storyboardMd,
} from "./fixtures";

/** A 1×1 PNG — the byte-serving /image endpoint's stand-in (U5a). */
export const TINY_PNG = Uint8Array.from(
  atob(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==",
  ),
  (c) => c.charCodeAt(0),
);

/*
 * Default MSW handlers — a sane two-run list, one status, one raw state.
 * Tests override with server.use(...) to exercise empty / error / 500 /
 * other stages. No live daemon ever runs in CI; the browser fetch is
 * intercepted here. (":id" matches one path segment, so /runs/:id never
 * swallows /runs/:id/status.)
 */
export const handlers = [
  http.get("/runs", () =>
    HttpResponse.json([runReviewFrame, runApprovePlan]),
  ),
  http.get("/runs/:id/status", () => HttpResponse.json(statusReviewFrame)),
  http.get("/runs/:id/artifacts/plan", () =>
    HttpResponse.text("# The plan\n\nA default plan for the booth.", {
      headers: { "Content-Type": "text/markdown; charset=utf-8" },
    }),
  ),
  http.get("/runs/:id/artifacts/script", () =>
    HttpResponse.text(scriptMd, {
      headers: { "Content-Type": "text/markdown; charset=utf-8" },
    }),
  ),
  http.get("/runs/:id/artifacts/beats", () => HttpResponse.json(beatsFixture)),
  http.get("/runs/:id/artifacts/storyboard", () =>
    HttpResponse.text(storyboardMd, {
      headers: { "Content-Type": "text/markdown; charset=utf-8" },
    }),
  ),
  http.get("/runs/:id/artifacts/shots", () =>
    HttpResponse.text(shotsYaml, {
      headers: { "Content-Type": "text/plain; charset=utf-8" },
    }),
  ),
  // U5a — the eye-gate's reads: frame candidates + the image bytes.
  http.get("/runs/:id/frames/:n/candidates", () =>
    HttpResponse.json(candidatesFlagPass),
  ),
  http.get("/runs/:id/frames/:n/image", () =>
    HttpResponse.arrayBuffer(TINY_PNG.buffer as ArrayBuffer, {
      headers: { "Content-Type": "image/png" },
    }),
  ),
  http.get("/runs/:id", () => HttpResponse.json(rawAuthoring)),
];

export const server = setupServer(...handlers);
