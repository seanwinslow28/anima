import { http, HttpResponse } from "msw";
import { setupServer } from "msw/node";

import { runApprovePlan, runReviewFrame, statusReviewFrame } from "./fixtures";

/*
 * Default MSW handlers — a sane two-run list + one status. Tests override with
 * server.use(...) to exercise empty / error / 500 / other stages. No live
 * daemon ever runs in CI; the browser fetch is intercepted here.
 */
export const handlers = [
  http.get("/runs", () =>
    HttpResponse.json([runReviewFrame, runApprovePlan]),
  ),
  http.get("/runs/:id/status", () => HttpResponse.json(statusReviewFrame)),
];

export const server = setupServer(...handlers);
