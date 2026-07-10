import { render, screen, waitFor, within } from "@testing-library/react";
import { http, HttpResponse } from "msw";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it } from "vitest";

import { AnimaticGate } from "./AnimaticGate";
import { RunProvider } from "../../lib/runContext";
import { ROUTER_FUTURE } from "../../test/render";
import { server } from "../../test/handlers";
import { statusAnimaticGate, statusAnimaticHolds } from "../../test/fixtures";
import type { RunStatus } from "../../api/types";

/*
 * The Animatic gate (U4c) — the THIN opt-in placement gate. No artifact read
 * exists (G3: roughs live on disk, the daemon serves neither upload nor
 * display), so the gate's ONLY data source is the shared /status read: the
 * placement instruction is the page, the holds strip is the aside, and the
 * one decision is POST /animatic/approve. This block covers the read states;
 * the ingest flow (both actions -> the SAME POST) is its own block.
 */

const RUN = "2026-06-21-spark-animatic-driven";

function mountAnimaticGate(status: RunStatus | (() => Response) = statusAnimaticHolds) {
  server.use(
    http.get(
      "/runs/:id/status",
      typeof status === "function" ? status : () => HttpResponse.json(status),
    ),
  );
  return render(
    <MemoryRouter initialEntries={[`/runs/${RUN}/animatic`]} future={ROUTER_FUTURE}>
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
          path="/runs/:id/animatic"
          element={
            <RunProvider runId={RUN} pollIntervalMs={5}>
              <AnimaticGate pollIntervalMs={5} />
            </RunProvider>
          }
        />
        <Route
          path="/runs/:id/frames/:n"
          element={<div data-testid="eyegate-screen" />}
        />
      </Routes>
    </MemoryRouter>,
  );
}

async function seeTheGate() {
  await waitFor(() =>
    expect(
      screen.getByRole("heading", { level: 1, name: /the placement pass/i }),
    ).toBeInTheDocument(),
  );
}

describe("AnimaticGate — the read (thin: /status is the only source)", () => {
  it("renders the placement page: ONE h1, the stamp, the byline, the drop-dir instruction (G3 — disk, not upload)", async () => {
    mountAnimaticGate();
    await seeTheGate();
    // one h1 — the gate title
    expect(screen.getAllByRole("heading", { level: 1 })).toHaveLength(1);
    expect(screen.getByText(/ANIMATIC · PLACEMENT/)).toBeInTheDocument();
    expect(screen.getByText(/drawn by hand/i)).toBeInTheDocument();
    // the instruction, not a drop zone: the REAL on-disk path + the naming form
    expect(screen.getByText(`runs/${RUN}/animatic/`)).toBeInTheDocument();
    expect(screen.getByText(/F01\.png/)).toBeInTheDocument();
    // a rough is enough — silhouette recommended, per-frame optional
    expect(screen.getByText(/silhouette/i)).toBeInTheDocument();
  });

  it("the holds strip renders one cell per frame from /status.frames[].hold", async () => {
    mountAnimaticGate(statusAnimaticHolds);
    await seeTheGate();
    const strip = screen.getByRole("region", { name: /holds/i });
    const cells = within(strip).getAllByRole("listitem");
    expect(cells).toHaveLength(4);
    expect(cells[0]).toHaveTextContent("F01");
    expect(cells[0]).toHaveTextContent("×4");
    expect(cells[3]).toHaveTextContent("×5");
    // the sidecar override note — holds.json on disk wins at ingest
    expect(within(strip).getByText(/holds\.json/)).toBeInTheDocument();
  });

  it("an empty frames read (the live ANIMATIC projection) is first-class: quiet board-holds line, both actions offered", async () => {
    mountAnimaticGate(statusAnimaticGate);
    await seeTheGate();
    // no broken strip — the honest quiet line instead
    expect(screen.queryAllByRole("listitem")).toHaveLength(0);
    expect(screen.getByText(/board's holds carry the timing/i)).toBeInTheDocument();
    // the gate never assumes roughs exist: the skip path is first-class
    expect(
      screen.getByRole("button", { name: /ingest & generate/i }),
    ).toBeEnabled();
    expect(
      screen.getByRole("button", { name: /continue without roughs/i }),
    ).toBeEnabled();
  });

  it("shows the loading skeleton while /status is in flight", () => {
    mountAnimaticGate();
    expect(screen.getByTestId("gate-skeleton")).toBeInTheDocument();
  });

  it("a failed /status read is the honest error, and Retry re-reads it", async () => {
    let calls = 0;
    mountAnimaticGate(() => {
      calls += 1;
      if (calls === 1) {
        return HttpResponse.json({ detail: "boom" }, { status: 500 });
      }
      return HttpResponse.json(statusAnimaticHolds);
    });
    await waitFor(() =>
      expect(screen.getByText(/couldn't read the run/i)).toBeInTheDocument(),
    );
    const { default: userEvent } = await import("@testing-library/user-event");
    await userEvent.click(screen.getByRole("button", { name: /retry/i }));
    await seeTheGate();
  });
});
