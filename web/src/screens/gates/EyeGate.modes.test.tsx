import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { http, HttpResponse } from "msw";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it } from "vitest";

import { EyeGate } from "./EyeGate";
import { RunProvider } from "../../lib/runContext";
import { ROUTER_FUTURE } from "../../test/render";
import { server } from "../../test/handlers";
import { candidatesFlagPass, statusReviewFrame } from "../../test/fixtures";
import type { CandidateAttempt, RunStatus } from "../../api/types";

/*
 * The U5c instrument modes beyond the ghost: diff-wipe (D, [/], the labelled
 * slider — attempt-vs-attempt or candidate-vs-approved-prior, NEVER the
 * Bible anchor, G9), lights-out (L — the frame alone on the dark stage), and
 * hover-skim (peek a reel cell on the stage without moving the reviewed
 * frame).
 */

const RUN = "2026-07-04-spark-forest";

/** F01 under the eye, one take, nothing approved — nothing to wipe against. */
const statusNothingToCompare: RunStatus = {
  ...statusReviewFrame,
  next_action: { kind: "review_frame", frame: 1, hint: "next: review F01" },
  frames: [
    { n: 1, status: "generated", attempts: 1, hold: 4 },
    { n: 2, status: "pending", attempts: 0, hold: 2 },
  ],
};

const oneAttempt: CandidateAttempt[] = [candidatesFlagPass[0]];

function mountEyeGate({
  frame = 3,
  status,
  candidates,
}: {
  frame?: number;
  status?: RunStatus;
  candidates?: CandidateAttempt[];
} = {}) {
  if (status !== undefined) {
    server.use(http.get("/runs/:id/status", () => HttpResponse.json(status)));
  }
  if (candidates !== undefined) {
    server.use(
      http.get("/runs/:id/frames/:n/candidates", () =>
        HttpResponse.json(candidates),
      ),
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

async function seeTheStage() {
  await waitFor(() => expect(screen.getByTestId("stage")).toBeInTheDocument());
  return screen.getByTestId("stage");
}

function stageRegion() {
  return screen.getByRole("region", { name: /the stage/i });
}

const wipeLayer = () => document.querySelector(".eg-wipe");
const wipeSlider = () =>
  screen.getByRole("slider", { name: /wipe position/i }) as HTMLInputElement;
const wipeImgs = () =>
  Array.from(document.querySelectorAll<HTMLImageElement>(".eg-wipe img"));

describe("EyeGate — diff-wipe (D compares two prints)", () => {
  it("D opens a wipe between the shown take and the other attempt, with a labelled slider; D closes it", async () => {
    mountEyeGate(); // F03: two attempts; shown = take 2 (latest)
    await seeTheStage();
    const region = stageRegion();
    region.focus();

    expect(wipeLayer()).toBeNull();

    fireEvent.keyDown(region, { key: "d" });
    expect(wipeLayer()).not.toBeNull();
    // both sides render: the shown take (attempt 2) vs the other (attempt 1)
    const srcs = wipeImgs().map((i) => i.src);
    expect(srcs.some((s) => s.includes("attempt=2"))).toBe(true);
    expect(srcs.some((s) => s.includes("attempt=1"))).toBe(true);
    // the wipe is ALSO a labelled slider (a11y — never mouse-only)
    expect(wipeSlider()).toBeInTheDocument();

    fireEvent.keyDown(region, { key: "D" });
    expect(wipeLayer()).toBeNull();
  });

  it("has a visible Wipe toolbar button that toggles the same layer", async () => {
    const user = userEvent.setup();
    mountEyeGate();
    await seeTheStage();

    const btn = screen.getByRole("button", { name: /wipe/i });
    expect(btn).toHaveAttribute("aria-pressed", "false");
    await user.click(btn);
    expect(btn).toHaveAttribute("aria-pressed", "true");
    expect(wipeLayer()).not.toBeNull();
    await user.click(btn);
    expect(wipeLayer()).toBeNull();
  });

  it("[ and ] drag the wipe line; the slider moves it too", async () => {
    mountEyeGate();
    await seeTheStage();
    const region = stageRegion();
    region.focus();

    fireEvent.keyDown(region, { key: "d" });
    expect(wipeSlider().value).toBe("50");

    fireEvent.keyDown(region, { key: "[" });
    expect(wipeSlider().value).toBe("46");
    fireEvent.keyDown(region, { key: "]" });
    fireEvent.keyDown(region, { key: "]" });
    expect(wipeSlider().value).toBe("54");

    // the slider is a real control, not a display — at 20 the over layer
    // clips to the left fifth (clip-path keeps both prints registered)
    fireEvent.change(wipeSlider(), { target: { value: "20" } });
    expect(wipeSlider().value).toBe("20");
    const over = document.querySelector<HTMLElement>(".eg-wipe-over");
    expect(over?.style.clipPath).toBe("inset(0 80% 0 0)");
  });

  it("can compare candidate-vs-approved-prior, and offers NO anchor path (G9)", async () => {
    const user = userEvent.setup();
    mountEyeGate(); // F03: F02 is the approved prior
    await seeTheStage();
    const region = stageRegion();
    region.focus();

    fireEvent.keyDown(region, { key: "d" });

    // the compare picker offers exactly: the other take + the approved prior
    const picker = screen.getByRole("group", { name: /compare against/i });
    const options = Array.from(picker.querySelectorAll("button")).map(
      (b) => b.textContent,
    );
    expect(options.join(" ")).toMatch(/take 1/i);
    expect(options.join(" ")).toMatch(/F02/i);
    expect(options.join(" ")).not.toMatch(/anchor|bible/i);

    await user.click(screen.getByRole("button", { name: /F02/i }));
    const srcs = wipeImgs().map((i) => i.src);
    expect(srcs.some((s) => s.includes("/frames/2/image"))).toBe(true);
    expect(srcs.some((s) => s.includes("attempt=2"))).toBe(true);
    // no image on the stage ever reads from the Bible tree
    expect(srcs.every((s) => !s.includes("characters"))).toBe(true);
  });

  it("with one take and nothing approved there is nothing to wipe — button disabled, D a no-op", async () => {
    mountEyeGate({
      frame: 1,
      status: statusNothingToCompare,
      candidates: oneAttempt,
    });
    await seeTheStage();
    const region = stageRegion();
    region.focus();

    expect(screen.getByRole("button", { name: /wipe/i })).toBeDisabled();
    fireEvent.keyDown(region, { key: "d" });
    expect(wipeLayer()).toBeNull();
  });
});

describe("EyeGate — lights-out (L: the frame alone)", () => {
  it("L drops ALL chrome — toolbar, Em, filmstrip, header — and L restores it", async () => {
    mountEyeGate();
    await seeTheStage();
    const region = stageRegion();
    region.focus();

    // chrome up
    expect(screen.getByRole("button", { name: /print it/i })).toBeInTheDocument();
    expect(screen.getByLabelText(/notes from the back row/i)).toBeInTheDocument();
    expect(document.querySelector(".ro-strip")).not.toBeNull();
    expect(document.querySelector(".eg-head")).not.toBeNull();

    fireEvent.keyDown(region, { key: "l" });
    // the frame alone on the dark stage
    expect(screen.getByTestId("stage")).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /print it/i })).toBeNull();
    expect(screen.queryByLabelText(/notes from the back row/i)).toBeNull();
    expect(document.querySelector(".ro-strip")).toBeNull();
    expect(document.querySelector(".eg-head")).toBeNull();

    fireEvent.keyDown(region, { key: "L" });
    expect(screen.getByRole("button", { name: /print it/i })).toBeInTheDocument();
    expect(document.querySelector(".ro-strip")).not.toBeNull();
  });

  it("has a visible House lights toolbar button", async () => {
    const user = userEvent.setup();
    mountEyeGate();
    await seeTheStage();

    const btn = screen.getByRole("button", { name: /house lights/i });
    expect(btn).toHaveAttribute("aria-pressed", "false");
    await user.click(btn);
    // chrome is gone — the toggle back is the L key (the one-key contract)
    expect(screen.queryByRole("button", { name: /house lights/i })).toBeNull();
    expect(document.querySelector(".eg-head")).toBeNull();
  });

  it("the loop still rocks with the lights out (the frame OR the running loop)", async () => {
    mountEyeGate();
    await seeTheStage();
    const region = stageRegion();
    region.focus();

    fireEvent.keyDown(region, { key: "l" });
    fireEvent.keyDown(region, { key: " " });
    expect(screen.getByTestId("stage").className).toContain("eg-stage--running");
    fireEvent.keyUp(region, { key: " " });
    expect(screen.getByTestId("stage").className).not.toContain(
      "eg-stage--running",
    );
  });
});

describe("EyeGate — hover-skim (peek a reel cell without moving the frame)", () => {
  it("hovering an approved cell peeks that frame on the stage; leaving restores the take", async () => {
    mountEyeGate(); // F03 under review; F01/F02 printed
    await seeTheStage();

    const stageImg = () =>
      document.querySelector<HTMLImageElement>(".eg-img img");
    expect(stageImg()?.src).toContain("attempt=2");

    const cellF1 = screen.getByText("F01").closest("li");
    expect(cellF1).not.toBeNull();
    fireEvent.mouseEnter(cellF1 as HTMLElement);

    // the peek rides the stage…
    expect(stageImg()?.src).toContain("/frames/1/image");
    // …but the reviewed frame does NOT move
    expect(
      screen.getByRole("heading", { level: 1, name: /F03/ }),
    ).toBeInTheDocument();

    fireEvent.mouseLeave(cellF1 as HTMLElement);
    expect(stageImg()?.src).toContain("attempt=2");
  });

  it("a pending cell has nothing to peek — hover leaves the stage alone", async () => {
    mountEyeGate();
    await seeTheStage();

    const stageImg = () =>
      document.querySelector<HTMLImageElement>(".eg-img img");
    const cellF4 = screen.getByText("F04").closest("li");
    fireEvent.mouseEnter(cellF4 as HTMLElement);
    expect(stageImg()?.src).toContain("attempt=2");
  });
});
