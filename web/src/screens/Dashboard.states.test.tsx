import { screen, waitForElementToBeRemoved } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { http, HttpResponse } from "msw";
import { describe, expect, it } from "vitest";

import { runErrorItem, runReviewFrame } from "../test/fixtures";
import { server } from "../test/handlers";
import { renderApp } from "../test/render";
import { Dashboard } from "./Dashboard";

describe("Dashboard — states", () => {
  it("shows the empty invitation (and the new-project card) when there are no runs", async () => {
    server.use(http.get("/runs", () => HttpResponse.json([])));

    renderApp(<Dashboard />);

    expect(await screen.findByText(/no runs yet/i)).toBeInTheDocument();
    // The inert new-project placeholder is present (brainstorm room is v1c).
    expect(
      screen.getByRole("button", { name: /new project/i }),
    ).toBeInTheDocument();
  });

  it("shows a skeleton of the gallery while loading", () => {
    // First synchronous render is the loading state (the fetch resolves later).
    renderApp(<Dashboard />);
    expect(screen.getByTestId("dashboard-skeleton")).toBeInTheDocument();
  });

  it("shows an error with a working retry when the list can't be read", async () => {
    let hits = 0;
    server.use(
      http.get("/runs", () => {
        hits += 1;
        // Fail first, then succeed once retried.
        return hits === 1
          ? new HttpResponse(null, { status: 500 })
          : HttpResponse.json([runReviewFrame]);
      }),
    );

    renderApp(<Dashboard />);

    expect(await screen.findByText(/couldn't reach the daemon/i)).toBeInTheDocument();
    const retry = screen.getByRole("button", { name: /retry/i });

    await userEvent.click(retry);

    // Recovery: the run now renders.
    expect(await screen.findByText("spark-forest")).toBeInTheDocument();
    expect(screen.queryByText(/couldn't reach the daemon/i)).not.toBeInTheDocument();
  });

  it("surfaces an unreadable run as a 'couldn't read this run' card, never dropped", async () => {
    server.use(
      http.get("/runs", () => HttpResponse.json([runReviewFrame, runErrorItem])),
    );

    renderApp(<Dashboard />);

    // The good run still renders...
    expect(await screen.findByText("spark-forest")).toBeInTheDocument();
    // ...and the broken one is surfaced with its id + the recovery hint.
    expect(screen.getByText(/couldn't read this run/i)).toBeInTheDocument();
    expect(screen.getByText(runErrorItem.run_id)).toBeInTheDocument();
  });

  it("clears the skeleton once runs load", async () => {
    server.use(http.get("/runs", () => HttpResponse.json([runReviewFrame])));
    renderApp(<Dashboard />);
    await waitForElementToBeRemoved(() => screen.queryByTestId("dashboard-skeleton"));
    expect(screen.getByText("spark-forest")).toBeInTheDocument();
  });
});
