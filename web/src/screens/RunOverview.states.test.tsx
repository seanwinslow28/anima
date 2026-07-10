import { screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { delay, http, HttpResponse } from "msw";
import { Route, Routes } from "react-router-dom";
import { describe, expect, it } from "vitest";

import { statusReviewFrame, statusWorking } from "../test/fixtures";
import { server } from "../test/handlers";
import { renderApp } from "../test/render";
import { RunOverview } from "./RunOverview";

/*
 * U2b Task 1 — the two-read wiring (GET /runs/{id}/status + GET /runs/{id})
 * and the doctrine states that apply to a read-only board: loading (a
 * skeleton of the BOARD, not a spinner), error ("couldn't read this run" +
 * the one retry), ready. Working (static leader) is Task 4; busy/409 is a
 * POST concern (U3).
 */

const RUN_ID = "2026-07-04-spark-forest";

function renderOverview(id = RUN_ID) {
  return renderApp(
    <Routes>
      <Route path="/runs/:id" element={<RunOverview />} />
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

  it("renders the static Working state when a job owns the run — named agent, decorative leader, no action link", async () => {
    server.use(
      http.get(`/runs/:id/status`, () => HttpResponse.json(statusWorking)),
    );
    renderOverview();
    await screen.findByTestId("booth-board");
    // the one h1 is the working line, agent-named
    const headings = screen.getAllByRole("heading", { level: 1 });
    expect(headings).toHaveLength(1);
    expect(headings[0]).toHaveTextContent(/Flo is drawing F04/i);
    // the decorative leader — an image with an honest label, never a timer
    const leader = screen.getByTestId("static-leader");
    expect(leader).toHaveAttribute("role", "img");
    expect(leader).toHaveAccessibleName(/does not advance/i);
    // no mutating / stage affordance while the job owns the run
    expect(
      screen.queryByRole("link", { name: /to the screening/i }),
    ).not.toBeInTheDocument();
  });

  it("the working board is a single read — no polling, no self-advance", async () => {
    let statusReads = 0;
    server.use(
      http.get(`/runs/:id/status`, () => {
        statusReads += 1;
        return HttpResponse.json(statusWorking);
      }),
    );
    renderOverview();
    await screen.findByTestId("booth-board");
    expect(statusReads).toBe(1);
    // give any rogue interval/timeout a chance to fire — nothing may change
    await new Promise((r) => setTimeout(r, 120));
    expect(statusReads).toBe(1);
    expect(
      screen.getByRole("heading", { level: 1 }),
    ).toHaveTextContent(/Flo is drawing F04/i);
    expect(screen.getByTestId("static-leader")).toBeInTheDocument();
  });

  it("a manual re-read fetches /status again and moves the board", async () => {
    let calls = 0;
    server.use(
      http.get(`/runs/:id/status`, () => {
        calls += 1;
        return HttpResponse.json(calls === 1 ? statusWorking : statusReviewFrame);
      }),
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
