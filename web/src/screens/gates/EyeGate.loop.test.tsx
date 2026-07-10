import { act, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { afterEach, describe, expect, it, vi } from "vitest";

import { EyeGate } from "./EyeGate";
import {
  resetPreloadCacheForTests,
  setImageFactoryForTests,
  type PreloadImageLike,
} from "../../lib/imagePreload";
import { RunProvider } from "../../lib/runContext";
import { ROUTER_FUTURE } from "../../test/render";

/*
 * The rock/flip loop (U5a — the philosophy-honoring core): hold Space and the
 * frame's loop context runs at 12fps STEPPED (83ms), the shown take riding in
 * its own slot; release freezes back on the take. Reduced motion collapses
 * the run to a single hand-step. The stage owns the keys (a focusable region;
 * typing targets are ignored) and every loop frame is preloaded first.
 *
 * Loop context from /status (statusReviewFrame): F01 approved (hold 4),
 * F02 approved (hold 2), F03 = the frame under review -> the loop is
 * [F01, F02, F03-as-the-shown-take].
 */

const RUN = "2026-07-04-spark-forest";

/** Auto-loading fake images: preload resolves "ok" for every url, recorded. */
function stubAutoLoadImages(): string[] {
  const srcs: string[] = [];
  setImageFactoryForTests(() => {
    const img: PreloadImageLike = {
      set src(url: string) {
        srcs.push(url);
        queueMicrotask(() => img.onload?.());
      },
      onload: null,
      onerror: null,
    } as unknown as PreloadImageLike;
    return img;
  });
  return srcs;
}

function stubReducedMotion(matches: boolean) {
  vi.stubGlobal(
    "matchMedia",
    vi.fn().mockReturnValue({
      matches,
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
    }),
  );
}

afterEach(() => {
  vi.unstubAllGlobals();
  vi.useRealTimers();
  setImageFactoryForTests(null);
  resetPreloadCacheForTests();
});

function mountEyeGate() {
  return render(
    <MemoryRouter initialEntries={[`/runs/${RUN}/frames/3`]} future={ROUTER_FUTURE}>
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

/** The focusable stage region that owns the keyboard. */
function stageRegion() {
  return screen.getByRole("region", { name: /the stage/i });
}

const stageImgSrc = () =>
  within(screen.getByTestId("stage")).getByRole("img").getAttribute("src");

describe("EyeGate — preload (the cross-slice image DoD)", () => {
  it("primes the loop neighbors and every take before the rock", async () => {
    const srcs = stubAutoLoadImages();
    mountEyeGate();
    await seeTheStage();

    await waitFor(() => {
      expect(srcs).toEqual(
        expect.arrayContaining([
          `/runs/${RUN}/frames/1/image`,
          `/runs/${RUN}/frames/2/image`,
          `/runs/${RUN}/frames/3/image?attempt=1`,
          `/runs/${RUN}/frames/3/image?attempt=2`,
        ]),
      );
    });
  });
});

describe("EyeGate — rock/flip (hold Space to run, release to judge)", () => {
  it("rocks the loop at 12fps stepped with the shown take in its slot, and freezes on release", async () => {
    stubAutoLoadImages();
    mountEyeGate();
    const stage = await seeTheStage();
    const region = stageRegion();
    expect(region).toHaveAttribute("tabindex", "0");
    region.focus();

    vi.useFakeTimers();
    fireEvent.keyDown(region, { key: " " });

    // the gate weave breathes while the loop runs
    expect(stage.className).toContain("eg-stage--running");

    // 83ms per step: F01 -> F02 -> the shown take in F03's slot -> wraps
    act(() => vi.advanceTimersByTime(83));
    expect(stageImgSrc()).toBe(`/runs/${RUN}/frames/1/image`);
    // the timecode follows the playhead: F01 = frame 0 × hold 4 -> +00
    expect(screen.getByText("00:00:00+00")).toBeInTheDocument();

    act(() => vi.advanceTimersByTime(83));
    expect(stageImgSrc()).toBe(`/runs/${RUN}/frames/2/image`);

    act(() => vi.advanceTimersByTime(83));
    expect(stageImgSrc()).toBe(`/runs/${RUN}/frames/3/image?attempt=2`);

    act(() => vi.advanceTimersByTime(83));
    expect(stageImgSrc()).toBe(`/runs/${RUN}/frames/1/image`);

    // release: freeze back on the shown take, weave off
    fireEvent.keyUp(region, { key: " " });
    expect(stageImgSrc()).toBe(`/runs/${RUN}/frames/3/image?attempt=2`);
    expect(stage.className).not.toContain("eg-stage--running");
    expect(screen.getByText("00:00:00+04")).toBeInTheDocument();
  });

  it("rocks THIS candidate: a switched take rides the loop's F03 slot", async () => {
    stubAutoLoadImages();
    const user = userEvent.setup();
    mountEyeGate();
    await seeTheStage();

    await user.click(screen.getByRole("button", { name: /take 1/i }));

    const region = stageRegion();
    region.focus();
    vi.useFakeTimers();
    fireEvent.keyDown(region, { key: " " });
    act(() => vi.advanceTimersByTime(83 * 3));
    expect(stageImgSrc()).toBe(`/runs/${RUN}/frames/3/image?attempt=1`);
  });

  it("reduced motion: Space is a single hand-step, never a run", async () => {
    stubReducedMotion(true);
    stubAutoLoadImages();
    mountEyeGate();
    const stage = await seeTheStage();
    const region = stageRegion();
    region.focus();

    fireEvent.keyDown(region, { key: " " });
    // one step, immediately — and no run, no weave
    expect(stageImgSrc()).toBe(`/runs/${RUN}/frames/1/image`);
    expect(stage.className).not.toContain("eg-stage--running");

    // release does not snap back — the step is the affordance
    fireEvent.keyUp(region, { key: " " });
    expect(stageImgSrc()).toBe(`/runs/${RUN}/frames/1/image`);

    // the next press steps again
    fireEvent.keyDown(region, { key: " " });
    expect(stageImgSrc()).toBe(`/runs/${RUN}/frames/2/image`);
  });
});

describe("EyeGate — the keyboard infra (U5a owns Space + 1/2)", () => {
  it("keys fire only when the stage owns them: outside events and typing targets are ignored", async () => {
    stubAutoLoadImages();
    mountEyeGate();
    const stage = await seeTheStage();

    // an event outside the stage region never starts the loop
    fireEvent.keyDown(document.body, { key: " " });
    expect(stage.className).not.toContain("eg-stage--running");

    // a typing target inside the region is ignored (the infra U5b's note rides on)
    const input = document.createElement("input");
    stageRegion().appendChild(input);
    fireEvent.keyDown(input, { key: " " });
    expect(stage.className).not.toContain("eg-stage--running");
  });

  it("number keys switch takes; the Run button is the visible Space", async () => {
    stubAutoLoadImages();
    mountEyeGate();
    const stage = await seeTheStage();
    const region = stageRegion();
    region.focus();

    fireEvent.keyDown(region, { key: "1" });
    expect(screen.getByRole("button", { name: /take 1/i })).toHaveAttribute(
      "aria-pressed",
      "true",
    );
    expect(stageImgSrc()).toBe(`/runs/${RUN}/frames/3/image?attempt=1`);
    fireEvent.keyDown(region, { key: "2" });
    expect(stageImgSrc()).toBe(`/runs/${RUN}/frames/3/image?attempt=2`);

    // the visible button: press-and-hold semantics
    const run = screen.getByRole("button", { name: /run the loop/i });
    expect(run).toHaveAttribute("aria-pressed", "false");
    fireEvent.mouseDown(run);
    expect(stage.className).toContain("eg-stage--running");
    expect(run).toHaveAttribute("aria-pressed", "true");
    fireEvent.mouseUp(run);
    expect(stage.className).not.toContain("eg-stage--running");
  });
});
