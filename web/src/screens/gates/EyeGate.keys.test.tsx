import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { http, HttpResponse } from "msw";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it } from "vitest";

import { EyeGate } from "./EyeGate";
import { BoothShell } from "../../booth/BoothShell";
import { RunProvider } from "../../lib/runContext";
import { ROUTER_FUTURE } from "../../test/render";
import { server } from "../../test/handlers";
import { statusReviewFrame } from "../../test/fixtures";
import type { RunStatus } from "../../api/types";

/*
 * The eye-gate keyboard state machine (U5b) — the U5b key set over U5a's
 * focusable stage: ↑/↓ walk to the adjacent REVIEWABLE frame's screening,
 * ? toggles the cheat-sheet overlay (the discoverability backstop), ⌘K
 * summons U1's palette, and EVERY key has a visible stage-toolbar button
 * (the a11y contract). ⏎ print and R again are wired in their own tasks;
 * here the SM owns the keys and the buttons exist.
 */

const RUN = "2026-07-04-spark-forest";

/** statusReviewFrame with F04 flipped to generated (a reviewable next stop). */
const statusF4Reviewable: RunStatus = {
  ...statusReviewFrame,
  frames: statusReviewFrame.frames.map((f) =>
    f.n === 4 ? { ...f, status: "generated", attempts: 1 } : f,
  ),
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

describe("EyeGate — every key has a visible stage-toolbar button (a11y)", () => {
  it("shows real buttons for print, again, walk up/down, the cheat-sheet, and the palette", async () => {
    mountEyeGate();
    await seeTheStage();

    for (const name of [
      /print it/i,
      /go again/i,
      /previous frame/i,
      /next frame/i,
      /keys/i,
      /command palette/i,
      /run the loop/i, // U5a's — still present
    ]) {
      const btn = screen.getByRole("button", { name });
      expect(btn.tagName).toBe("BUTTON");
    }

    expect(screen.getByRole("button", { name: /print it/i })).toHaveClass(
      "ro-button",
      "ro-button--primary",
    );
    expect(screen.getByRole("button", { name: /go again/i })).toHaveClass(
      "ro-button",
      "ro-button--quiet",
    );
  });
});

describe("EyeGate — ? cheat-sheet (the discoverability backstop)", () => {
  it("? toggles an overlay listing every eye-gate key; Esc closes it", async () => {
    mountEyeGate();
    await seeTheStage();
    const region = stageRegion();
    region.focus();

    expect(screen.queryByRole("dialog", { name: /keys/i })).not.toBeInTheDocument();

    fireEvent.keyDown(region, { key: "?" });
    const sheet = screen.getByRole("dialog", { name: /keys/i });
    // every key of the shipped set is listed
    for (const key of ["⏎", "R", "SPACE", "1 2", "↑ ↓", "?", "⌘K"]) {
      expect(within(sheet).getByText(key)).toBeInTheDocument();
    }

    // ? again closes
    fireEvent.keyDown(region, { key: "?" });
    expect(screen.queryByRole("dialog", { name: /keys/i })).not.toBeInTheDocument();

    // Esc closes too
    fireEvent.keyDown(region, { key: "?" });
    expect(screen.getByRole("dialog", { name: /keys/i })).toBeInTheDocument();
    fireEvent.keyDown(region, { key: "Escape" });
    expect(screen.queryByRole("dialog", { name: /keys/i })).not.toBeInTheDocument();
  });

  it("the visible Keys button toggles the same overlay", async () => {
    const user = userEvent.setup();
    mountEyeGate();
    await seeTheStage();

    await user.click(screen.getByRole("button", { name: /keys/i }));
    expect(screen.getByRole("dialog", { name: /keys/i })).toBeInTheDocument();
    await user.click(screen.getByRole("button", { name: /^keys/i }));
    expect(screen.queryByRole("dialog", { name: /keys/i })).not.toBeInTheDocument();
  });
});

describe("EyeGate — ↑/↓ walk frames (reviewable stops only)", () => {
  it("↑ walks to the previous reviewable frame's screening", async () => {
    mountEyeGate();
    await seeTheStage();
    const region = stageRegion();
    region.focus();

    fireEvent.keyDown(region, { key: "ArrowUp" });
    await waitFor(() =>
      expect(
        screen.getByRole("heading", { level: 1, name: /F02/ }),
      ).toBeInTheDocument(),
    );
  });

  it("↓ is a no-op when every later frame is still pending (nothing to review)", async () => {
    mountEyeGate();
    await seeTheStage();
    const region = stageRegion();
    region.focus();

    fireEvent.keyDown(region, { key: "ArrowDown" });
    // stays on F03 — a pending frame is not a walkable stop
    expect(
      screen.getByRole("heading", { level: 1, name: /F03/ }),
    ).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /next frame/i })).toBeDisabled();
  });

  it("↓ walks to the next reviewable frame when one exists (skipping nothing reviewable is skipped)", async () => {
    mountEyeGate({ status: statusF4Reviewable });
    await seeTheStage();
    const region = stageRegion();
    region.focus();

    fireEvent.keyDown(region, { key: "ArrowDown" });
    await waitFor(() =>
      expect(
        screen.getByRole("heading", { level: 1, name: /F04/ }),
      ).toBeInTheDocument(),
    );
  });

  it("the visible walk buttons navigate too, and the dead end is disabled", async () => {
    const user = userEvent.setup();
    mountEyeGate();
    await seeTheStage();

    expect(screen.getByRole("button", { name: /next frame/i })).toBeDisabled();
    await user.click(screen.getByRole("button", { name: /previous frame/i }));
    await waitFor(() =>
      expect(
        screen.getByRole("heading", { level: 1, name: /F02/ }),
      ).toBeInTheDocument(),
    );
    // from F02 the walk back up hits F01
    expect(screen.getByRole("button", { name: /previous frame/i })).toBeEnabled();
  });
});

describe("EyeGate — ⌘K summons the palette (U1's, never swallowed)", () => {
  function mountInBooth() {
    return render(
      <MemoryRouter
        initialEntries={[`/runs/${RUN}/frames/3`]}
        future={ROUTER_FUTURE}
      >
        <BoothShell>
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
        </BoothShell>
      </MemoryRouter>,
    );
  }

  it("⌘K pressed on the stage region reaches the palette", async () => {
    mountInBooth();
    await seeTheStage();
    const region = stageRegion();
    region.focus();

    fireEvent.keyDown(region, { key: "k", metaKey: true });
    expect(
      screen.getByRole("dialog", { name: /command palette/i }),
    ).toBeInTheDocument();
  });

  it("the visible ⌘K button opens the palette", async () => {
    const user = userEvent.setup();
    mountInBooth();
    await seeTheStage();

    await user.click(screen.getByRole("button", { name: /command palette/i }));
    expect(
      screen.getByRole("dialog", { name: /command palette/i }),
    ).toBeInTheDocument();
  });
});
