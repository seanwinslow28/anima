import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { http, HttpResponse } from "msw";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it } from "vitest";

import { EyeGate } from "./EyeGate";
import { RunProvider } from "../../lib/runContext";
import { ROUTER_FUTURE } from "../../test/render";
import { server } from "../../test/handlers";
import { candidatesFlagPass, candidatesTwoCast } from "../../test/fixtures";
import { JOB_ID, jobLifecycle, succeededJob } from "../../test/jobHandlers";
import type { CandidateAttempt } from "../../api/types";

/*
 * AGAIN (U5b) — R / the "Go again" button opens the retake note row,
 * PREFILLED from Em's read of the shown take (her proposed fix first, her
 * flagged reasoning as the fallback — attributed either way), auto-pausing
 * the loop. ⏎ in the row sends POST /frames/{n}/retry {note} through U3's
 * job flow (Flo re-shoots); Esc cancels and returns focus to the stage.
 * The prefill is non-empty whenever Em flagged something, but the empty
 * case is guarded anyway (never a 422).
 */

const RUN = "2026-07-04-spark-forest";

function mountEyeGate({
  candidates,
}: { candidates?: CandidateAttempt[] } = {}) {
  if (candidates !== undefined) {
    server.use(
      http.get("/runs/:id/frames/:n/candidates", () =>
        HttpResponse.json(candidates),
      ),
    );
  }
  return render(
    <MemoryRouter initialEntries={[`/runs/${RUN}/frames/3`]} future={ROUTER_FUTURE}>
      <Routes>
        <Route
          path="/runs/:id/frames/:n"
          element={
            <RunProvider runId={RUN} pollIntervalMs={5}>
              <EyeGate pollIntervalMs={5} />
            </RunProvider>
          }
        />
      </Routes>
    </MemoryRouter>,
  );
}

async function seeTheStage() {
  await waitFor(() => expect(screen.getByTestId("stage")).toBeInTheDocument());
  return screen.getByTestId("stage");
}

function stageRegion() {
  return screen.getByRole("region", { name: /the stage/i });
}

function noteInput() {
  return screen.getByRole("textbox", { name: /retake note/i });
}

describe("EyeGate — AGAIN opens the note row, prefilled from Em", () => {
  it("R opens the row with Em's proposed fix composed into the note, attributed, focused", async () => {
    mountEyeGate({ candidates: candidatesTwoCast });
    await seeTheStage();
    const region = stageRegion();
    region.focus();

    fireEvent.keyDown(region, { key: "r" });

    const input = noteInput();
    expect(input).toHaveValue(
      "the box-creature keeps exactly four legs — a fifth leg ghosts in on the near side",
    );
    expect(screen.getByText(/prefilled from Em/i)).toBeInTheDocument();
    expect(input).toHaveFocus();
  });

  it("falls back to Em's flagged reasoning when she proposed no patch", async () => {
    const user = userEvent.setup();
    mountEyeGate(); // candidatesFlagPass: take 1 flag (no patches), take 2 pass
    await seeTheStage();

    await user.click(screen.getByRole("button", { name: /take 1/i }));
    const region = stageRegion();
    region.focus();
    fireEvent.keyDown(region, { key: "r" });

    expect(noteInput()).toHaveValue("line weight drifts on the arm");
    expect(screen.getByText(/prefilled from Em/i)).toBeInTheDocument();
  });

  it("a passing take prefills nothing, claims no attribution, and can't send empty", async () => {
    const posted: unknown[] = [];
    server.use(
      http.post("/runs/:id/frames/:n/retry", async ({ request }) => {
        posted.push(await request.json());
        return HttpResponse.json({ job_id: JOB_ID }, { status: 202 });
      }),
    );
    mountEyeGate(); // default shown = take 2, Em said pass "Ship."
    await seeTheStage();
    const region = stageRegion();
    region.focus();

    fireEvent.keyDown(region, { key: "r" });
    const input = noteInput();
    expect(input).toHaveValue("");
    expect(screen.queryByText(/prefilled from Em/i)).not.toBeInTheDocument();
    expect(screen.getByRole("button", { name: /send the retake/i })).toBeDisabled();

    // ⏎ on the empty note never POSTs (the 422 guard)
    fireEvent.keyDown(input, { key: "Enter" });
    expect(posted).toHaveLength(0);
  });

  it("opening the row auto-pauses the loop", async () => {
    mountEyeGate();
    const stage = await seeTheStage();
    const region = stageRegion();
    region.focus();

    fireEvent.keyDown(region, { key: " " });
    expect(stage.className).toContain("eg-stage--running");

    fireEvent.keyDown(region, { key: "r" });
    expect(stage.className).not.toContain("eg-stage--running");
    expect(noteInput()).toBeInTheDocument();
  });

  it("Esc cancels the row and returns focus to the stage", async () => {
    mountEyeGate({ candidates: candidatesTwoCast });
    await seeTheStage();
    const region = stageRegion();
    region.focus();

    fireEvent.keyDown(region, { key: "r" });
    const input = noteInput();
    expect(input).toHaveFocus();

    fireEvent.keyDown(input, { key: "Escape" });
    expect(screen.queryByRole("textbox", { name: /retake note/i })).not.toBeInTheDocument();
    expect(region).toHaveFocus();
  });
});

describe("EyeGate — AGAIN sends the retake through the job layer", () => {
  it("⏎ in the row POSTs retry {note}, veils the stage with FLO RE-SHOOTS, and the re-shot take comes up", async () => {
    const posted: unknown[] = [];
    let retried = false;
    const thirdTake: CandidateAttempt = {
      ...candidatesFlagPass[1],
      attempt: 3,
      image_url: `/runs/${RUN}/frames/3/image?attempt=3`,
      note: "hold the line weight from the anchor; tighter arm",
    };
    server.use(
      http.get("/runs/:id/frames/:n/candidates", () =>
        HttpResponse.json(
          retried ? [...candidatesFlagPass, thirdTake] : candidatesFlagPass,
        ),
      ),
      http.post("/runs/:id/frames/:n/retry", async ({ request }) => {
        posted.push(await request.json());
        retried = true;
        return HttpResponse.json({ job_id: JOB_ID }, { status: 202 });
      }),
      jobLifecycle(
        JOB_ID,
        succeededJob({
          next_action: { kind: "review_frame", frame: 3, hint: "next: review F03" },
        }),
        2,
      ),
    );
    const user = userEvent.setup();
    mountEyeGate();
    await seeTheStage();

    // take 1 carries the flag — its reasoning seeds the note
    await user.click(screen.getByRole("button", { name: /take 1/i }));
    const region = stageRegion();
    region.focus();
    fireEvent.keyDown(region, { key: "r" });

    const input = noteInput();
    await user.type(input, "; tighter arm");
    fireEvent.keyDown(input, { key: "Enter" });

    // the working veil names the re-shoot
    await waitFor(() =>
      expect(screen.getByTestId("gate-working")).toBeInTheDocument(),
    );
    expect(screen.getByText(/FLO RE-SHOOTS/)).toBeInTheDocument();

    // the POST carried the note as {note}
    await waitFor(() => expect(posted).toHaveLength(1));
    expect(posted[0]).toEqual({
      note: "line weight drifts on the arm; tighter arm",
    });

    // terminal (review_frame, SAME frame) -> the takes re-read; take 3 is up
    await waitFor(() =>
      expect(screen.getByRole("button", { name: /take 3/i })).toBeInTheDocument(),
    );
  });

  it("the visible Go again + SEND buttons drive the same flow", async () => {
    const posted: unknown[] = [];
    server.use(
      http.post("/runs/:id/frames/:n/retry", async ({ request }) => {
        posted.push(await request.json());
        return HttpResponse.json({ job_id: JOB_ID }, { status: 202 });
      }),
      jobLifecycle(
        JOB_ID,
        succeededJob({
          next_action: { kind: "review_frame", frame: 3, hint: "next: review F03" },
        }),
      ),
    );
    const user = userEvent.setup();
    mountEyeGate({ candidates: candidatesTwoCast });
    await seeTheStage();

    await user.click(screen.getByRole("button", { name: /go again/i }));
    await user.click(screen.getByRole("button", { name: /send the retake/i }));

    await waitFor(() => expect(posted).toHaveLength(1));
    expect(posted[0]).toEqual({
      note:
        "the box-creature keeps exactly four legs — a fifth leg ghosts in on the near side",
    });
  });

  it("the loop still rocks after a cancelled note (Space keeps working)", async () => {
    mountEyeGate();
    const stage = await seeTheStage();
    const region = stageRegion();
    region.focus();

    fireEvent.keyDown(region, { key: "r" });
    fireEvent.keyDown(noteInput(), { key: "Escape" });

    fireEvent.keyDown(region, { key: " " });
    expect(stage.className).toContain("eg-stage--running");
    fireEvent.keyUp(region, { key: " " });
    expect(stage.className).not.toContain("eg-stage--running");
  });
});
