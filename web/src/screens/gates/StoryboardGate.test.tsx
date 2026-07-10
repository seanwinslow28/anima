import { render, screen, waitFor } from "@testing-library/react";
import { http, HttpResponse } from "msw";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it } from "vitest";

import { StoryboardGate } from "./StoryboardGate";
import { RunProvider } from "../../lib/runContext";
import { ROUTER_FUTURE } from "../../test/render";
import { server } from "../../test/handlers";
import {
  shotsYaml,
  statusApproveStoryboard,
  storyboardMd,
} from "../../test/fixtures";

/*
 * The Storyboard gate (U4b) — Bea's board as the lit continuity report +
 * the display-only slate stack, and the honest read states: loading
 * skeleton, a 404 board (a back-compat run has none) as "no board for this
 * run", an unparseable shots.yaml as a read error (never a crash). The lock
 * flow (success / THE INVALID-LOCK state) is its own block.
 */

const RUN = "2026-07-03-spark-tidepool";

function artifactHandlers() {
  const hits = { storyboard: 0, shots: 0 };
  server.use(
    http.get(`/runs/${RUN}/artifacts/storyboard`, () => {
      hits.storyboard += 1;
      return HttpResponse.text(storyboardMd, {
        headers: { "Content-Type": "text/markdown; charset=utf-8" },
      });
    }),
    http.get(`/runs/${RUN}/artifacts/shots`, () => {
      hits.shots += 1;
      return HttpResponse.text(shotsYaml, {
        headers: { "Content-Type": "text/plain; charset=utf-8" },
      });
    }),
  );
  return hits;
}

function mountStoryboardGate(status = statusApproveStoryboard) {
  server.use(http.get("/runs/:id/status", () => HttpResponse.json(status)));
  return render(
    <MemoryRouter initialEntries={[`/runs/${RUN}/storyboard`]} future={ROUTER_FUTURE}>
      <Routes>
        <Route
          path="/runs/:id"
          element={
            <RunProvider runId={RUN} pollIntervalMs={5}>
              <div data-testid="overview-screen" />
            </RunProvider>
          }
        />
        <Route
          path="/runs/:id/storyboard"
          element={
            <RunProvider runId={RUN} pollIntervalMs={5}>
              <StoryboardGate pollIntervalMs={5} />
            </RunProvider>
          }
        />
        <Route
          path="/runs/:id/animatic"
          element={<div data-testid="animatic-screen" />}
        />
        <Route
          path="/runs/:id/script"
          element={<div data-testid="script-screen" />}
        />
      </Routes>
    </MemoryRouter>,
  );
}

export async function seeTheBoard() {
  await waitFor(() =>
    expect(screen.getByText(/Five cuts, one fixed camera/)).toBeInTheDocument(),
  );
}

describe("StoryboardGate — the read", () => {
  it("renders Bea's board as the lit continuity page, ONE h1, Bea's byline, the slug stamp", async () => {
    artifactHandlers();
    mountStoryboardGate();
    await seeTheBoard();
    // the report's voice made it to the page
    expect(screen.getByText(/his attention is the still point/)).toBeInTheDocument();
    // one h1 — the gate title (the board's own # heading demotes to h2)
    expect(screen.getAllByRole("heading", { level: 1 })).toHaveLength(1);
    expect(
      screen.getByRole("heading", { level: 1, name: /the board/i }),
    ).toBeInTheDocument();
    expect(screen.getByText(/boarded by Bea/i)).toBeInTheDocument();
    expect(screen.getByText(/STORYBOARD · SPARK-TIDEPOOL/)).toBeInTheDocument();
  });

  it("the slate stack rides the aside: one slate per shot + the loop-return marker", async () => {
    artifactHandlers();
    mountStoryboardGate();
    await seeTheBoard();
    expect(
      screen.getByRole("region", { name: /slate stack/i }),
    ).toBeInTheDocument();
    expect(screen.getByText(/returns to frame 1/i)).toBeInTheDocument();
    // the beat links are real links back to the script gate
    expect(
      screen.getAllByRole("link", { name: /beat 1 —/i })[0],
    ).toHaveAttribute("href", `/runs/${RUN}/script`);
  });

  it("shows the loading skeleton while the two artifacts are in flight", () => {
    artifactHandlers();
    mountStoryboardGate();
    expect(screen.getByTestId("gate-skeleton")).toBeInTheDocument();
  });

  it("fetches each artifact exactly once (the board is read, not polled)", async () => {
    const hits = artifactHandlers();
    mountStoryboardGate();
    await seeTheBoard();
    expect(hits.storyboard).toBe(1);
    expect(hits.shots).toBe(1);
  });

  it("a 404 board (back-compat run) reads as an honest 'no board for this run'", async () => {
    server.use(
      http.get(`/runs/${RUN}/artifacts/storyboard`, () =>
        HttpResponse.json(
          { detail: `no artifact 'storyboard' for run '${RUN}'` },
          { status: 404 },
        ),
      ),
      http.get(`/runs/${RUN}/artifacts/shots`, () =>
        HttpResponse.json(
          { detail: `no artifact 'shots' for run '${RUN}'` },
          { status: 404 },
        ),
      ),
    );
    mountStoryboardGate();
    await waitFor(() =>
      expect(screen.getByText(/no board for this run/i)).toBeInTheDocument(),
    );
    expect(screen.getByRole("button", { name: /retry/i })).toBeInTheDocument();
  });

  it("a non-404 artifact failure is the generic honest error with Retry", async () => {
    server.use(
      http.get(`/runs/${RUN}/artifacts/storyboard`, () =>
        HttpResponse.json({ detail: "boom" }, { status: 500 }),
      ),
      http.get(`/runs/${RUN}/artifacts/shots`, () =>
        HttpResponse.text(shotsYaml),
      ),
    );
    mountStoryboardGate();
    await waitFor(() =>
      expect(screen.getByText(/couldn't read the board/i)).toBeInTheDocument(),
    );
    expect(screen.getByRole("button", { name: /retry/i })).toBeInTheDocument();
  });

  it("an unparseable shots.yaml surfaces as the read error, never a crash", async () => {
    server.use(
      http.get(`/runs/${RUN}/artifacts/storyboard`, () =>
        HttpResponse.text(storyboardMd),
      ),
      http.get(`/runs/${RUN}/artifacts/shots`, () =>
        HttpResponse.text("frames: {}\nnot: [a, board"),
      ),
    );
    mountStoryboardGate();
    await waitFor(() =>
      expect(screen.getByText(/couldn't read the board/i)).toBeInTheDocument(),
    );
    expect(screen.getByRole("button", { name: /retry/i })).toBeInTheDocument();
  });
});
