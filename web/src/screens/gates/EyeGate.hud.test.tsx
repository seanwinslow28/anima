import { act, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { afterEach, describe, expect, it, vi } from "vitest";

import { EyeGate } from "./EyeGate";
import { HudHost, useHud } from "../../booth/HudHost";
import { RunProvider } from "../../lib/runContext";
import { ROUTER_FUTURE } from "../../test/render";

/*
 * The summonable HUD (U5c — the eye-gate's signature): the eye-gate opts
 * into U1's "full" dim level — idle ~3s and the booth chrome fades; the
 * frame is the only lit thing; any input wakes it. Reduced motion → no
 * timed fade at all (U1's contract, inherited). Plus the cheat-sheet
 * COMPLETE-map check and the focus-ownership polish (keys ignore typing
 * targets — including the wipe slider).
 */

const RUN = "2026-07-04-spark-forest";

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

/** Reports the provider's dim level (the U1 probe idiom). */
function Probe() {
  const { dimLevel } = useHud();
  return <div data-testid="probe" data-dim={dimLevel} />;
}

function mountInHud({ idleMs = 40 }: { idleMs?: number } = {}) {
  return render(
    <MemoryRouter
      initialEntries={[`/runs/${RUN}/frames/3`]}
      future={ROUTER_FUTURE}
    >
      <HudHost idleMs={idleMs}>
        <Probe />
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
      </HudHost>
    </MemoryRouter>,
  );
}

async function seeTheStage() {
  await waitFor(() => expect(screen.getByTestId("stage")).toBeInTheDocument());
  return screen.getByTestId("stage");
}

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("EyeGate — the summonable HUD (idle → the booth goes dark)", () => {
  it("declares the FULL dim level (reserved for the eye-gate since U1)", async () => {
    mountInHud();
    await seeTheStage();
    expect(screen.getByTestId("probe")).toHaveAttribute("data-dim", "full");
  });

  it("idles into the dark booth — chrome fades — and any input wakes it", async () => {
    mountInHud({ idleMs: 40 });
    await seeTheStage();
    const section = screen.getByTestId("eyegate");

    // idle past the threshold: the booth goes dark
    await waitFor(
      () => expect(section.className).toContain("eg-screen--idledark"),
      { timeout: 2000 },
    );

    // any input wakes the room
    fireEvent.keyDown(window, { key: "j" });
    expect(section.className).not.toContain("eg-screen--idledark");
  });

  it("under prefers-reduced-motion there is no timed fade at all", async () => {
    stubReducedMotion(true);
    mountInHud({ idleMs: 40 });
    await seeTheStage();
    const section = screen.getByTestId("eyegate");

    await new Promise((r) => setTimeout(r, 200));
    expect(section.className).not.toContain("eg-screen--idledark");
  });

  it("keeps the transport awake while the retry note is open", async () => {
    mountInHud({ idleMs: 40 });
    await seeTheStage();
    const section = screen.getByTestId("eyegate");
    const region = screen.getByRole("region", { name: /the stage/i });
    region.focus();

    fireEvent.keyDown(region, { key: "r" });
    expect(screen.getByRole("textbox", { name: /retake note/i })).toHaveFocus();

    await act(async () => {
      await new Promise((resolve) => setTimeout(resolve, 200));
    });
    expect(section.className).not.toContain("eg-screen--idledark");
  });
});

describe("EyeGate — the cheat-sheet lists the COMPLETE v1b key map", () => {
  it("every eye-gate key is on the sheet", async () => {
    mountInHud();
    await seeTheStage();
    const region = screen.getByRole("region", { name: /the stage/i });
    region.focus();

    fireEvent.keyDown(region, { key: "?" });
    const sheet = screen.getByRole("dialog", { name: /keys/i });
    for (const key of [
      "⏎",
      "R",
      "SPACE",
      "1 2",
      "↑ ↓",
      "O",
      "D",
      "[ ]",
      "L",
      "?",
      "⌘K",
    ]) {
      expect(within(sheet).getByText(key)).toBeInTheDocument();
    }
  });
});

describe("EyeGate — focus ownership (keys ignore typing targets)", () => {
  it("bracket keys pressed ON the wipe slider don't drag the wipe", async () => {
    mountInHud();
    await seeTheStage();
    const region = screen.getByRole("region", { name: /the stage/i });
    region.focus();

    fireEvent.keyDown(region, { key: "d" });
    const slider = screen.getByRole("slider", {
      name: /wipe position/i,
    }) as HTMLInputElement;
    expect(slider.value).toBe("50");

    fireEvent.keyDown(slider, { key: "[" });
    expect(slider.value).toBe("50");
  });

  it("mode letters typed into the retry note don't fire the modes", async () => {
    mountInHud();
    await seeTheStage();
    const region = screen.getByRole("region", { name: /the stage/i });
    region.focus();

    fireEvent.keyDown(region, { key: "r" }); // open the note
    const note = screen.getByRole("textbox");

    fireEvent.keyDown(note, { key: "o" });
    fireEvent.keyDown(note, { key: "l" });
    // no onion layer, no lights-out — the note owns the keys
    expect(document.querySelector(".eg-onion")).toBeNull();
    expect(document.querySelector(".eg-head")).not.toBeNull();
  });
});
