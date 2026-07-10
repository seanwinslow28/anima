import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { delay, http, HttpResponse } from "msw";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it } from "vitest";

import { EyeGate } from "./EyeGate";
import { RunProvider } from "../../lib/runContext";
import { ROUTER_FUTURE } from "../../test/render";
import { server } from "../../test/handlers";
import { candidatesEdge, candidatesFlagPass } from "../../test/fixtures";
import type { CandidateAttempt, RunStatus } from "../../api/types";

/*
 * The eye-gate (U5a) — the stage: the lit frame, take switching, the burn-ins,
 * and the honest states (a take that never developed is a card, never a broken
 * <img>). All reads: /status through the run scope + /frames/{n}/candidates.
 */

const RUN = "2026-07-04-spark-forest";

function mountEyeGate({
  frame = 3,
  candidates,
  status,
}: {
  frame?: number;
  candidates?: CandidateAttempt[] | (() => Response);
  status?: RunStatus;
} = {}) {
  if (candidates !== undefined) {
    server.use(
      http.get(
        "/runs/:id/frames/:n/candidates",
        typeof candidates === "function"
          ? candidates
          : () => HttpResponse.json(candidates),
      ),
    );
  }
  if (status !== undefined) {
    server.use(
      http.get("/runs/:id/status", () => HttpResponse.json(status)),
    );
  }
  return render(
    <MemoryRouter
      initialEntries={[`/runs/${RUN}/frames/${frame}`]}
      future={ROUTER_FUTURE}
    >
      <Routes>
        <Route
          path="/runs/:id/frames/:n"
          element={
            <RunProvider runId={RUN} pollIntervalMs={5}>
              <EyeGate />
            </RunProvider>
          }
        />
      </Routes>
    </MemoryRouter>,
  );
}

/** The lit stage (the <figure> the frame projects in). */
async function seeTheStage() {
  await waitFor(() =>
    expect(screen.getByTestId("stage")).toBeInTheDocument(),
  );
  return screen.getByTestId("stage");
}

describe("EyeGate — the stage (the lit frame)", () => {
  it("projects the shown take: the image, the burn-ins, the timecode, one h1", async () => {
    mountEyeGate();
    const stage = await seeTheStage();

    // default shown take = the latest attempt (2) when none is approved
    const img = within(stage).getByRole("img", { name: /F03.*take 2/i });
    expect(img).toHaveAttribute("src", expect.stringContaining("attempt=2"));

    // burn-in left: frame · take · hold (hold 2 from /status.frames)
    expect(screen.getByText("F03 · TAKE 2 · HOLD 2")).toBeInTheDocument();
    // burn-in right: the G5 constant line
    expect(screen.getByText("12 FPS · NB2 · $0.07")).toBeInTheDocument();
    // timecode = frame_index × hold @ 12fps -> (3-1)×2 = +04
    expect(screen.getByText("00:00:00+04")).toBeInTheDocument();

    // one h1 on the screen
    const h1s = screen.getAllByRole("heading", { level: 1 });
    expect(h1s).toHaveLength(1);
    expect(h1s[0]).toHaveTextContent(/F03/);
  });

  it("approved frames default to the approved take, not the latest", async () => {
    const approvedFirst: CandidateAttempt[] = [
      { ...candidatesFlagPass[0], status: "approved" },
      candidatesFlagPass[1],
    ];
    mountEyeGate({ candidates: approvedFirst });
    const stage = await seeTheStage();
    const img = within(stage).getByRole("img", { name: /take 1/i });
    expect(img).toHaveAttribute("src", expect.stringContaining("attempt=1"));
  });
});

describe("EyeGate — take switching (click; keys are the loop task)", () => {
  it("clicking a take swaps the stage image and the burn-in", async () => {
    const user = userEvent.setup();
    mountEyeGate();
    const stage = await seeTheStage();

    const take1 = screen.getByRole("button", { name: /take 1/i });
    const take2 = screen.getByRole("button", { name: /take 2/i });
    expect(take2).toHaveAttribute("aria-pressed", "true");

    await user.click(take1);

    expect(take1).toHaveAttribute("aria-pressed", "true");
    expect(take2).toHaveAttribute("aria-pressed", "false");
    expect(within(stage).getByRole("img", { name: /take 1/i })).toHaveAttribute(
      "src",
      expect.stringContaining("attempt=1"),
    );
    expect(screen.getByText("F03 · TAKE 1 · HOLD 2")).toBeInTheDocument();
  });
});

describe("EyeGate — honest image states (never a broken <img>)", () => {
  it("an errored fan renders the honest card + the recorded error, no <img>", async () => {
    mountEyeGate({ candidates: candidatesEdge });
    const stage = await seeTheStage();

    // default shown = latest attempt (2), which errored
    expect(
      within(stage).getByText(/this take didn't develop/i),
    ).toBeInTheDocument();
    expect(within(stage).getByText(/NB2 transport timed out/i)).toBeInTheDocument();
    expect(within(stage).queryByRole("img")).not.toBeInTheDocument();
  });

  it("a take with no image (null image_url) renders the honest card", async () => {
    const user = userEvent.setup();
    mountEyeGate({ candidates: candidatesEdge });
    const stage = await seeTheStage();

    await user.click(screen.getByRole("button", { name: /take 1/i }));

    expect(
      within(stage).getByText(/this take didn't develop/i),
    ).toBeInTheDocument();
    expect(within(stage).queryByRole("img")).not.toBeInTheDocument();
  });

  it("a stage image that 404s flips to the honest card (onError)", async () => {
    mountEyeGate();
    const stage = await seeTheStage();

    fireEvent.error(within(stage).getByRole("img", { name: /take 2/i }));

    expect(
      within(stage).getByText(/this take didn't develop/i),
    ).toBeInTheDocument();
    expect(within(stage).queryByRole("img")).not.toBeInTheDocument();
  });
});

describe("EyeGate — the doctrine states", () => {
  it("loading: a lit-frame skeleton while the candidates read is in flight", async () => {
    mountEyeGate({
      candidates: (() => delay("infinite")) as unknown as () => Response,
    });
    await waitFor(() =>
      expect(screen.getByTestId("eyegate-skeleton")).toBeInTheDocument(),
    );
  });

  it("error: a candidates 404 is the couldn't-screen state with one retry", async () => {
    const user = userEvent.setup();
    mountEyeGate({
      candidates: () =>
        HttpResponse.json({ detail: "no frame" }, { status: 404 }),
    });
    await waitFor(() =>
      expect(screen.getByRole("alert")).toHaveTextContent(/couldn't screen/i),
    );
    expect(screen.queryByTestId("stage")).not.toBeInTheDocument();

    // the retry re-runs the read; restore the default handler first
    server.resetHandlers();
    await user.click(screen.getByRole("button", { name: /retry/i }));
    await seeTheStage();
  });

  it("working: a frame still generating reads 'Flo is drawing', with the ritual leader", async () => {
    mountEyeGate({ frame: 4, candidates: [] });
    await waitFor(() =>
      expect(screen.getByText(/Flo is drawing F04/i)).toBeInTheDocument(),
    );
    // the decorative non-advancing leader (the ritual timer)
    expect(screen.getByRole("status")).toBeInTheDocument();
    expect(screen.queryByTestId("stage")).not.toBeInTheDocument();
  });
});
