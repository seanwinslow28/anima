import { readFileSync } from "node:fs";

import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { http, HttpResponse } from "msw";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it } from "vitest";

import { EyeGate } from "./EyeGate";
import { RunProvider } from "../../lib/runContext";
import { ROUTER_FUTURE } from "../../test/render";
import { server } from "../../test/handlers";
import { statusReviewFrame } from "../../test/fixtures";
import type { RunStatus } from "../../api/types";

/*
 * Onion-skin (U5c — the ghost layer): O ghosts the approved N-1 under the
 * candidate at low opacity, and — for a loop-return frame — frame 1 too,
 * read from chain_from in the shots artifact. THE TWO-REDS RULE: the ghost
 * renders cool/tungsten-dim, NEVER a lamp hue (print-green / hold-amber) —
 * one reserved warning hue on the stage.
 */

const RUN = "2026-07-04-spark-forest";

/** F04 under the eye with F01–F03 printed — the loop-return screening (the
 *  default shots.yaml fixture carries chain_from: 1 on frame 4). */
const statusF4LoopReturn: RunStatus = {
  ...statusReviewFrame,
  next_action: { kind: "review_frame", frame: 4, hint: "next: review F04" },
  frames: [
    { n: 1, status: "approved", attempts: 1, hold: 4 },
    { n: 2, status: "approved", attempts: 2, hold: 2 },
    { n: 3, status: "approved", attempts: 1, hold: 2 },
    { n: 4, status: "generated", attempts: 1, hold: 2 },
  ],
};

/** F01 under the eye — nothing printed before it, nothing to ghost. */
const statusNothingApproved: RunStatus = {
  ...statusReviewFrame,
  next_action: { kind: "review_frame", frame: 1, hint: "next: review F01" },
  frames: [
    { n: 1, status: "generated", attempts: 1, hold: 4 },
    { n: 2, status: "pending", attempts: 0, hold: 2 },
  ],
};

function mountEyeGate({
  frame = 3,
  status,
}: { frame?: number; status?: RunStatus } = {}) {
  if (status !== undefined) {
    server.use(http.get("/runs/:id/status", () => HttpResponse.json(status)));
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

const ghostImgs = () =>
  Array.from(
    document.querySelectorAll<HTMLImageElement>(".eg-onion .eg-ghost"),
  );

describe("EyeGate — onion-skin (O ghosts the approved N-1)", () => {
  it("O toggles a ghost of the approved previous frame under the candidate", async () => {
    mountEyeGate(); // F03: F02 is the approved N-1
    await seeTheStage();
    const region = stageRegion();
    region.focus();

    expect(document.querySelector(".eg-onion")).toBeNull();

    fireEvent.keyDown(region, { key: "o" });
    await waitFor(() => expect(ghostImgs()).toHaveLength(1));
    expect(ghostImgs()[0].src).toContain("/frames/2/image");

    fireEvent.keyDown(region, { key: "O" });
    expect(document.querySelector(".eg-onion")).toBeNull();
  });

  it("has a visible Ghost toolbar button that toggles the same layer", async () => {
    const user = userEvent.setup();
    mountEyeGate();
    await seeTheStage();

    const btn = screen.getByRole("button", { name: /ghost/i });
    expect(btn.tagName).toBe("BUTTON");
    expect(btn).toHaveAttribute("aria-pressed", "false");

    await user.click(btn);
    expect(btn).toHaveAttribute("aria-pressed", "true");
    await waitFor(() => expect(ghostImgs()).toHaveLength(1));

    await user.click(btn);
    expect(btn).toHaveAttribute("aria-pressed", "false");
    expect(document.querySelector(".eg-onion")).toBeNull();
  });

  it("a loop-return frame ghosts frame 1 too (chain_from via the shots artifact)", async () => {
    mountEyeGate({ frame: 4, status: statusF4LoopReturn });
    await seeTheStage();
    const region = stageRegion();
    region.focus();

    fireEvent.keyDown(region, { key: "o" });
    // the shots read is async — both ghosts settle: N-1 (F03) + chain_from (F01)
    await waitFor(() => expect(ghostImgs()).toHaveLength(2));
    const srcs = ghostImgs().map((img) => img.src);
    expect(srcs.some((s) => s.includes("/frames/3/image"))).toBe(true);
    expect(srcs.some((s) => s.includes("/frames/1/image"))).toBe(true);
  });

  it("dedupes when chain_from IS the approved N-1 (one ghost, never a double print)", async () => {
    // a board whose frame 2 chains from 1 — N-1 and the loop anchor coincide
    server.use(
      http.get("/runs/:id/artifacts/shots", () =>
        HttpResponse.text(
          [
            "slug: spark-forest",
            "frames:",
            "- id: 1",
            "  prompt: establishing",
            "  hold: 4",
            "- id: 2",
            "  prompt: 'Composition identical to frame 1.'",
            "  chain_from: 1",
          ].join("\n"),
          { headers: { "Content-Type": "text/plain; charset=utf-8" } },
        ),
      ),
    );
    const statusF2: RunStatus = {
      ...statusReviewFrame,
      next_action: { kind: "review_frame", frame: 2, hint: "next: review F02" },
      frames: [
        { n: 1, status: "approved", attempts: 1, hold: 4 },
        { n: 2, status: "generated", attempts: 1, hold: 2 },
      ],
    };
    mountEyeGate({ frame: 2, status: statusF2 });
    await seeTheStage();
    const region = stageRegion();
    region.focus();

    fireEvent.keyDown(region, { key: "o" });
    await waitFor(() => expect(ghostImgs()).toHaveLength(1));
    expect(ghostImgs()[0].src).toContain("/frames/1/image");
  });

  it("with nothing approved before the frame the button is disabled and O is a no-op", async () => {
    mountEyeGate({ frame: 1, status: statusNothingApproved });
    await seeTheStage();
    const region = stageRegion();
    region.focus();

    expect(screen.getByRole("button", { name: /ghost/i })).toBeDisabled();
    fireEvent.keyDown(region, { key: "o" });
    expect(document.querySelector(".eg-onion")).toBeNull();
  });

  it("the ghost layer is a judgment aid — aria-hidden, out of the reading order", async () => {
    mountEyeGate();
    await seeTheStage();
    const region = stageRegion();
    region.focus();

    fireEvent.keyDown(region, { key: "o" });
    await waitFor(() => expect(ghostImgs()).toHaveLength(1));
    const layer = document.querySelector(".eg-onion");
    expect(layer).toHaveAttribute("aria-hidden", "true");
  });
});

describe("the two-reds rule — the ghost never wears a lamp hue", () => {
  // vitest runs css:false, so the guard reads the stylesheet off disk (the
  // reelone.test.ts idiom; cwd-relative — a .tsx module's import.meta.url is
  // not file-scheme under the react transform): the .eg-ghost treatment must
  // be cool/desaturated and must never reach for the lamp tokens.
  const css = readFileSync("src/styles/eyegate.css", "utf8");

  it("the ghost rule is cool/desaturated and reserves the lamp hues", () => {
    const at = css.indexOf(".eg-ghost {");
    expect(at).toBeGreaterThan(-1);
    const rule = css.slice(at, css.indexOf("}", at));
    // cool: a real desaturating filter
    expect(rule).toMatch(/filter:/);
    expect(rule).toMatch(/saturate|grayscale/);
    // never a lamp hue: print-green / hold-amber / bakelite stay reserved
    expect(rule).not.toMatch(/--print|--hold|--bakelite/);
  });
});
