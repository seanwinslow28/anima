import { screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { delay, http, HttpResponse } from "msw";
import { Route, Routes } from "react-router-dom";
import { describe, expect, it } from "vitest";

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
