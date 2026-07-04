import { screen } from "@testing-library/react";
import { http, HttpResponse } from "msw";
import { describe, expect, it } from "vitest";

import { nextActionCta } from "../lib/nextAction";
import { runApprovePlan, runReviewFrame } from "../test/fixtures";
import { server } from "../test/handlers";
import { renderApp } from "../test/render";
import { Dashboard } from "./Dashboard";

describe("Dashboard — happy path", () => {
  it("renders a card per run with its name, stage chip, and next-move CTA", async () => {
    server.use(
      http.get("/runs", () =>
        HttpResponse.json([runReviewFrame, runApprovePlan]),
      ),
    );

    renderApp(<Dashboard />);

    // Both run names (the slug, Newsreader headline).
    expect(await screen.findByText("spark-forest")).toBeInTheDocument();
    expect(screen.getByText("spark-tidepool")).toBeInTheDocument();

    // Stage chips (mono).
    expect(screen.getByText("GENERATE")).toBeInTheDocument();
    expect(screen.getByText("PLAN")).toBeInTheDocument();

    // The load-bearing part: each card leads with its next_action CTA verb, and
    // the text is exactly what the kind mapping produces.
    expect(
      screen.getByText(nextActionCta(runReviewFrame.next_action).label),
    ).toBeInTheDocument();
    expect(
      screen.getByText(nextActionCta(runApprovePlan.next_action).label),
    ).toBeInTheDocument();
  });

  it("shows two run cards for two runs", async () => {
    server.use(
      http.get("/runs", () =>
        HttpResponse.json([runReviewFrame, runApprovePlan]),
      ),
    );

    renderApp(<Dashboard />);

    const cards = await screen.findAllByRole("link", { name: /open run/i });
    expect(cards).toHaveLength(2);
  });
});
