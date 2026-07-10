import { http, HttpResponse } from "msw";
import { setupServer } from "msw/node";

import {
  beatsFixture,
  rawAuthoring,
  runApprovePlan,
  runReviewFrame,
  scriptMd,
  statusReviewFrame,
} from "./fixtures";

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
  http.get("/runs/:id", () => HttpResponse.json(rawAuthoring)),
];

export const server = setupServer(...handlers);
