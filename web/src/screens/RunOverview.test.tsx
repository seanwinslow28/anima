import { screen, within } from "@testing-library/react";
import { http, HttpResponse } from "msw";
import { Route, Routes } from "react-router-dom";
import { describe, expect, it } from "vitest";

import {
  rawAnimatic,
  rawBackCompat,
  statusAnimaticGate,
} from "../test/fixtures";
import { RunProvider } from "../lib/runContext";
import { server } from "../test/handlers";
import { renderApp } from "../test/render";
import { RunOverview } from "./RunOverview";

/*
 * U2b — the booth board's content: the reel of stages (run-shape-derived,
 * revisitable), the now-screening hero (one h1 = the move, one primary
 * action on U1's URL scheme). Default handlers serve an authoring run
 * (rawAuthoring + statusReviewFrame: GENERATE, F03 waiting on the eye).
 * Since U3 the board reads /status through the run scope (RunProvider).
 */

const RUN_ID = "2026-07-04-spark-forest";

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
    expect(go).toHaveClass("bb-go", "ro-button", "ro-button--primary");
  });

  it("names the machine token in the eyebrow (now screening · next_action)", async () => {
    renderOverview();
    await screen.findByTestId("booth-board");
    expect(screen.getByText(/now screening/i)).toHaveTextContent(
      /review_frame/,
    );
  });

  it("shows the estimate truthfully — the band, never a cap", async () => {
    renderOverview();
    await screen.findByTestId("booth-board");
    const bo = screen.getByRole("complementary", { name: /box office/i });
    expect(bo).toHaveTextContent(/estimate, not a cap/i);
    expect(bo).toHaveTextContent("$0.35");
    expect(bo).toHaveTextContent("$0.93");
    expect(bo).toHaveTextContent("$2.25");
  });

  it("labels the spend as a derived running total (≈ … drawn), never a live meter", async () => {
    renderOverview();
    await screen.findByTestId("booth-board");
    const spend = screen.getByTestId("derived-spend");
    // 4 recorded attempts × $0.07
    expect(spend).toHaveTextContent("≈");
    expect(spend).toHaveTextContent("$0.28");
    expect(spend).toHaveTextContent(/drawn/i);
    expect(spend).toHaveTextContent(/derived/i);
  });

  it("a plan not yet costed reads estimate pending, not $0", async () => {
    server.use(
      http.get("/runs/:id", () => HttpResponse.json(rawAnimatic)),
      http.get("/runs/:id/status", () =>
        HttpResponse.json(statusAnimaticGate),
      ),
    );
    renderOverview("2026-06-21-spark-animatic-driven");
    await screen.findByTestId("booth-board");
    const bo = screen.getByRole("complementary", { name: /box office/i });
    expect(bo).toHaveTextContent(/estimate pending/i);
  });

  it("keeps the by-phase detail behind the density gate (on-intent reveal)", async () => {
    renderOverview();
    await screen.findByTestId("booth-board");
    const bo = screen.getByRole("complementary", { name: /box office/i });
    // keyboard-reachable reveal region; detail present in the DOM for AT
    expect(bo).toHaveAttribute("tabindex", "0");
    const detail = bo.querySelector("[data-reveal]");
    expect(detail).not.toBeNull();
    expect(detail).toHaveTextContent(/generate/i);
  });

  it("staffs the crew stations behind the same on-intent reveal", async () => {
    renderOverview();
    await screen.findByTestId("booth-board");
    const crew = screen.getByRole("complementary", { name: /crew/i });
    expect(crew).toHaveAttribute("tabindex", "0");
    const list = crew.querySelector("[data-reveal]");
    expect(list).not.toBeNull();
    for (const agent of ["Maya", "Sam", "Bea", "Cy", "Flo", "Em", "Mo"]) {
      expect(crew).toHaveTextContent(agent);
    }
  });

  it("leaves a quiet crew whisper at rest while the full roll stays on intent", async () => {
    renderOverview();
    await screen.findByTestId("booth-board");
    const crew = screen.getByRole("complementary", { name: /crew/i });
    const whisper = within(crew).getByText(/seven stations · focus to call roll/i);
    expect(whisper.closest("[data-reveal]")).toBeNull();
  });

  it("renders the mini frame-reel: printed takes, the take on screen, queued cuts", async () => {
    renderOverview();
    await screen.findByTestId("booth-board");
    const strip = screen.getByRole("list", { name: "reel" });
    const cells = within(strip).getAllByRole("listitem");
    expect(cells).toHaveLength(5);
    expect(cells[0].textContent).toContain("PRINT");
    expect(cells[2].textContent).toContain("YOUR CALL");
    expect(cells[2].querySelector("img")).toHaveAttribute(
      "src",
      `/runs/${RUN_ID}/frames/3/image`,
    );
    expect(cells[4].querySelector(".ro-empty")).not.toBeNull();
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
