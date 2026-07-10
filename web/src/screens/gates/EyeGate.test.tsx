import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { delay, http, HttpResponse } from "msw";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it } from "vitest";

import { EyeGate } from "./EyeGate";
import { RunProvider } from "../../lib/runContext";
import { ROUTER_FUTURE } from "../../test/render";
import { server } from "../../test/handlers";
import {
  candidatesEdge,
  candidatesFlagPass,
  candidatesTwoCast,
} from "../../test/fixtures";
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

describe("EyeGate — Em as a hand in the margin", () => {
  it("reads the shown take's verdict as a lamp before the words, and swaps with the take", async () => {
    const user = userEvent.setup();
    mountEyeGate();
    await seeTheStage();
    const rail = screen.getByRole("complementary", { name: /back row/i });

    // default take 2: Em passed — PRINT lamp, then the reasoning
    expect(
      within(rail).getByRole("img", { name: /verdict: print/i }),
    ).toBeInTheDocument();
    expect(within(rail).getByText("Ship.")).toBeInTheDocument();

    // take 1: the flag — HOLD lamp, the reasoning, the cite
    await user.click(screen.getByRole("button", { name: /take 1/i }));
    expect(
      within(rail).getByRole("img", { name: /verdict: hold/i }),
    ).toBeInTheDocument();
    expect(
      within(rail).getByText("line weight drifts on the arm"),
    ).toBeInTheDocument();
    expect(
      within(rail).getByText(/IR\.sean\.style\.line-weight/),
    ).toBeInTheDocument();
  });

  it("renders one card per cast namespace, with the proposed fix displayed", async () => {
    mountEyeGate({ candidates: candidatesTwoCast });
    await seeTheStage();
    const rail = screen.getByRole("complementary", { name: /back row/i });

    // two cards, named by IR namespace
    expect(
      within(rail).getByText("EM · back row · sean"),
    ).toBeInTheDocument();
    expect(
      within(rail).getByText("EM · back row · claude-mascot"),
    ).toBeInTheDocument();
    expect(
      within(rail).getByRole("img", { name: /verdict: print/i }),
    ).toBeInTheDocument();
    expect(
      within(rail).getByRole("img", { name: /verdict: hold/i }),
    ).toBeInTheDocument();

    // the proposed fix — displayed, attributed as hers to propose, yours to call
    expect(
      within(rail).getByText(/proposed — your call, not hers/i),
    ).toBeInTheDocument();
    expect(
      within(rail).getByText("the box-creature keeps exactly four legs"),
    ).toBeInTheDocument();
    expect(
      within(rail).getAllByText(/a fifth leg ghosts in on the near side/i).length,
    ).toBeGreaterThan(0);
    expect(
      within(rail).getByText(/IR\.claude-mascot\.anatomy\.leg-count-4/),
    ).toBeInTheDocument();
  });

  it("states her honest boundary in-context and announces the region; grease marks are decorative", async () => {
    mountEyeGate();
    await seeTheStage();
    const rail = screen.getByRole("complementary", { name: /back row/i });

    expect(rail).toHaveAttribute("aria-live", "polite");
    expect(
      within(rail).getByText(/she reads stills, not motion — the loop is yours/i),
    ).toBeInTheDocument();
    // every grease mark (the decorative margin strokes) is aria-hidden
    const marks = rail.querySelectorAll(".eg-grease");
    expect(marks.length).toBeGreaterThan(0);
    marks.forEach((m) => expect(m).toHaveAttribute("aria-hidden", "true"));
  });

  it("a take with no Em note says so honestly", async () => {
    mountEyeGate({ candidates: candidatesEdge });
    await seeTheStage();
    const rail = screen.getByRole("complementary", { name: /back row/i });
    expect(
      within(rail).getByText(/no note from the back row on this take/i),
    ).toBeInTheDocument();
  });
});

describe("EyeGate — the provenance line (client-composed, G8)", () => {
  it("credits the chain when Em has read the take", async () => {
    mountEyeGate();
    await seeTheStage();
    expect(
      screen.getByText("drawn by Flo (NB2) · read by Em · your call"),
    ).toBeInTheDocument();
  });

  it("drops 'read by Em' when the take carries no verdict — never invented", async () => {
    mountEyeGate({ candidates: candidatesEdge });
    await seeTheStage();
    expect(
      screen.getByText("drawn by Flo (NB2) · your call"),
    ).toBeInTheDocument();
    expect(screen.queryByText(/read by Em/)).not.toBeInTheDocument();
  });
});

describe("EyeGate — the filmstrip ledger", () => {
  it("shows the run's frames from /status: PRINT, ON SCREEN (ringed = the viewed frame), pending", async () => {
    mountEyeGate();
    await seeTheStage();
    const reel = screen.getByRole("list", { name: /reel/i });
    const cells = within(reel).getAllByRole("listitem");
    expect(cells).toHaveLength(5);

    expect(within(cells[0]).getByText("F01")).toBeInTheDocument();
    expect(within(cells[0]).getByText(/PRINT/)).toBeInTheDocument();
    expect(within(cells[1]).getByText(/PRINT/)).toBeInTheDocument();
    expect(within(cells[2]).getByText("F03")).toBeInTheDocument();
    expect(within(cells[2]).getByText(/ON SCREEN/)).toBeInTheDocument();
    // the ring follows the VIEWED frame
    expect(cells[2].className).toContain("ro-fcell--now");
    expect(cells[3].className).not.toContain("ro-fcell--now");
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
