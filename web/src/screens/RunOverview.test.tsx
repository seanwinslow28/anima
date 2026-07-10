import { screen, within } from "@testing-library/react";
import { http, HttpResponse } from "msw";
import { Route, Routes } from "react-router-dom";
import { describe, expect, it } from "vitest";

import {
  rawAnimatic,
  rawBackCompat,
  statusAnimaticGate,
} from "../test/fixtures";
import { server } from "../test/handlers";
import { renderApp } from "../test/render";
import { RunOverview } from "./RunOverview";

/*
 * U2b — the booth board's content: the reel of stages (run-shape-derived,
 * revisitable), the now-screening hero (one h1 = the move, one primary
 * action on U1's URL scheme). Default handlers serve an authoring run
 * (rawAuthoring + statusReviewFrame: GENERATE, F03 waiting on the eye).
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

describe("RunOverview — the reel of stages", () => {
  it("renders the pipeline-stages landmark with the authoring run's six segments", async () => {
    renderOverview();
    const nav = await screen.findByRole("navigation", {
      name: /pipeline stages/i,
    });
    const items = within(nav).getAllByRole("listitem");
    expect(items).toHaveLength(6);
    expect(nav).toHaveTextContent("Plan");
    expect(nav).toHaveTextContent("Script");
    expect(nav).toHaveTextContent("Board");
    expect(nav).toHaveTextContent("Animatic");
    expect(nav).toHaveTextContent("Generate");
    expect(nav).toHaveTextContent("Assemble");
  });

  it("marks the current stage aria-current=step and the board LOCKED", async () => {
    renderOverview();
    const nav = await screen.findByRole("navigation", {
      name: /pipeline stages/i,
    });
    const now = nav.querySelector('[aria-current="step"]');
    expect(now).toHaveTextContent("Generate");
    expect(now).toHaveTextContent("CUT 3/5");
    expect(nav).toHaveTextContent("LOCKED");
    expect(nav).toHaveTextContent(/waived/i);
  });

  it("a printed stage is a real revisit link to its gate", async () => {
    renderOverview();
    const nav = await screen.findByRole("navigation", {
      name: /pipeline stages/i,
    });
    const plan = within(nav).getByRole("link", { name: /plan/i });
    expect(plan).toHaveAttribute("href", `/runs/${RUN_ID}/plan`);
  });

  it("derives the back-compat reel: no Script / Board / Animatic segments", async () => {
    server.use(http.get("/runs/:id", () => HttpResponse.json(rawBackCompat)));
    renderOverview();
    const nav = await screen.findByRole("navigation", {
      name: /pipeline stages/i,
    });
    expect(within(nav).getAllByRole("listitem")).toHaveLength(3);
    expect(nav).not.toHaveTextContent("Script");
    expect(nav).not.toHaveTextContent("Board");
    expect(nav).not.toHaveTextContent("Animatic");
  });

  it("an animatic-enabled run shows ANIMATIC as the current gate", async () => {
    server.use(
      http.get("/runs/:id", () => HttpResponse.json(rawAnimatic)),
      http.get("/runs/:id/status", () =>
        HttpResponse.json(statusAnimaticGate),
      ),
    );
    renderOverview("2026-06-21-spark-animatic-driven");
    const nav = await screen.findByRole("navigation", {
      name: /pipeline stages/i,
    });
    const now = nav.querySelector('[aria-current="step"]');
    expect(now).toHaveTextContent("Animatic");
  });
});

describe("RunOverview — the now-screening hero", () => {
  it("leads with one h1 = the move, and one primary action to the gate URL", async () => {
    renderOverview();
    await screen.findByTestId("booth-board");
    const headings = screen.getAllByRole("heading", { level: 1 });
    expect(headings).toHaveLength(1);
    expect(headings[0]).toHaveTextContent(/F03 waiting on your eye/i);
    const go = screen.getByRole("link", { name: /to the screening/i });
    expect(go).toHaveAttribute("href", `/runs/${RUN_ID}/frames/3`);
  });

  it("names the machine token in the eyebrow (now screening · next_action)", async () => {
    renderOverview();
    await screen.findByTestId("booth-board");
    expect(screen.getByText(/now screening/i)).toHaveTextContent(
      /review_frame/,
    );
  });

  it("an act kind with no screen yet (assemble) renders the move without a dead link", async () => {
    server.use(
      http.get("/runs/:id/status", () =>
        HttpResponse.json({
          run_id: RUN_ID,
          stage: "ASSEMBLE",
          stub: false,
          plan_status: "approved",
          next_action: { kind: "assemble", hint: "next: --assemble" },
          active_job: null,
          frames: [],
          updated_at: null,
        }),
      ),
    );
    renderOverview();
    await screen.findByTestId("booth-board");
    expect(
      screen.getByRole("heading", { level: 1, name: /ready to assemble/i }),
    ).toBeInTheDocument();
    expect(
      screen.queryByRole("link", { name: /to the screening/i }),
    ).not.toBeInTheDocument();
  });
});
