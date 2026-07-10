import { screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { delay, http, HttpResponse } from "msw";
import { Route, Routes } from "react-router-dom";
import { describe, expect, it } from "vitest";

import { RunProvider } from "../lib/runContext";
import { statusReviewFrame, statusWorking } from "../test/fixtures";
import { server } from "../test/handlers";
import { succeededJob } from "../test/jobHandlers";
import { renderApp } from "../test/render";
import { RunOverview } from "./RunOverview";

/*
 * U2b Task 1 wired the two reads (GET /runs/{id}/status via the run scope +
 * GET /runs/{id}) and the doctrine states: loading (a skeleton of the
 * BOARD, not a spinner), error ("couldn't read this run" + the one retry),
 * ready. U3 closed the static Working seam: the board now LIVE-POLLS the
 * owning job through runContext and advances on the real terminal.
 */

const RUN_ID = "2026-07-04-spark-forest";

/** A job that stays running for the whole test (the provider polls it). */
function runningJob(jobId: string) {
  return http.get(`/jobs/${jobId}`, () =>
    HttpResponse.json({
      ...succeededJob({ job_id: jobId }),
      state: "running",
      rc: null,
    }),
  );
}

function renderOverview(id = RUN_ID) {
  return renderApp(
    <Routes>
      <Route
        path="/runs/:id"
        element={
          <RunProvider runId={id} pollIntervalMs={5}>
            <RunOverview />
          </RunProvider>
        }
      />
    </Routes>,
    { route: `/runs/${id}` },
  );
}

describe("RunOverview states", () => {
  it("shows a skeleton of the board while the reads are in flight", async () => {
    server.use(
      http.get(`/runs/:id/status`, async () => {
        await delay(60);
        return HttpResponse.json(null, { status: 404 });
      }),
      http.get(`/runs/:id`, async () => {
        await delay(60);
        return HttpResponse.json(null, { status: 404 });
      }),
    );
    renderOverview();
    expect(screen.getByTestId("board-skeleton")).toBeInTheDocument();
  });

  it("renders the board once both reads land", async () => {
    renderOverview();
    expect(await screen.findByTestId("booth-board")).toBeInTheDocument();
    expect(screen.queryByTestId("board-skeleton")).not.toBeInTheDocument();
  });

  it("renders the couldn't-read state + one retry when the status read 404s", async () => {
    server.use(
      http.get(`/runs/:id/status`, () =>
        HttpResponse.json({ detail: "no run" }, { status: 404 }),
      ),
    );
    renderOverview("nope");
    expect(
      await screen.findByText(/couldn't read this run/i),
    ).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /retry/i })).toBeInTheDocument();
    expect(screen.queryByTestId("booth-board")).not.toBeInTheDocument();
  });

  it("renders the couldn't-read state when the raw state read 422s", async () => {
    server.use(
      http.get(`/runs/:id`, () =>
        HttpResponse.json({ detail: "malformed run_state.json" }, { status: 422 }),
      ),
    );
    renderOverview();
    expect(
      await screen.findByText(/couldn't read this run/i),
    ).toBeInTheDocument();
  });

  it("renders the Working state when a job owns the run — named agent, the ritual leader, no action link", async () => {
    server.use(
      http.get(`/runs/:id/status`, () => HttpResponse.json(statusWorking)),
      runningJob("job-7f3a"),
    );
    renderOverview();
    await screen.findByTestId("booth-board");
    // the one h1 is the working line, agent-named
    const headings = screen.getAllByRole("heading", { level: 1 });
    expect(headings).toHaveLength(1);
    expect(headings[0]).toHaveTextContent(/Flo is drawing F04/i);
    // the ritual leader — an announced working state, never a fake ETA
    expect(screen.getByRole("status")).toBeInTheDocument();
    // no mutating / stage affordance while the job owns the run
    expect(
      screen.queryByRole("link", { name: /to the screening/i }),
    ).not.toBeInTheDocument();
  });

  it("the working board LIVE-POLLS the owning job and advances on the real terminal (the U2b static seam is closed)", async () => {
    let statusReads = 0;
    let jobPolls = 0;
    server.use(
      http.get(`/runs/:id/status`, () => {
        statusReads += 1;
        return HttpResponse.json(statusReads === 1 ? statusWorking : statusReviewFrame);
      }),
      http.get(`/jobs/job-7f3a`, () => {
        jobPolls += 1;
        return HttpResponse.json(
          jobPolls < 3
            ? { ...succeededJob({ job_id: "job-7f3a" }), state: "running", rc: null }
            : succeededJob({ job_id: "job-7f3a" }),
        );
      }),
    );
    renderOverview();
    await screen.findByTestId("booth-board");
    // NO clicks: the leader resolves on the job's real terminal and the
    // board re-reads /status on its own.
    expect(
      await screen.findByRole("heading", {
        level: 1,
        name: /F03 waiting on your eye/i,
      }),
    ).toBeInTheDocument();
    expect(jobPolls).toBeGreaterThanOrEqual(3);
    expect(statusReads).toBe(2);
  });

  it("a manual re-read still fetches /status again and moves the board", async () => {
    let calls = 0;
    server.use(
      http.get(`/runs/:id/status`, () => {
        calls += 1;
        return HttpResponse.json(calls === 1 ? statusWorking : statusReviewFrame);
      }),
      runningJob("job-7f3a"),
    );
    renderOverview();
    await screen.findByTestId("booth-board");
    const reread = screen.getByRole("button", { name: /re-read/i });
    await userEvent.click(reread);
    expect(
      await screen.findByRole("heading", {
        level: 1,
        name: /F03 waiting on your eye/i,
      }),
    ).toBeInTheDocument();
    expect(calls).toBe(2);
  });

  it("retry re-reads both endpoints and recovers", async () => {
    server.use(
      http.get(
        `/runs/:id/status`,
        () => HttpResponse.json({ detail: "boom" }, { status: 500 }),
        { once: true },
      ),
    );
    renderOverview();
    const retry = await screen.findByRole("button", { name: /retry/i });
    await userEvent.click(retry);
    await waitFor(() =>
      expect(screen.getByTestId("booth-board")).toBeInTheDocument(),
    );
  });
});
