import { render, screen, within } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it } from "vitest";

import { SlateStack } from "./SlateStack";
import { parseShots } from "../../lib/shots";
import { shotsYaml } from "../../test/fixtures";
import { ROUTER_FUTURE } from "../../test/render";

/*
 * The slate stack (U4b) — shots.yaml parsed into DISPLAY-ONLY slates: one
 * slate per shot (cut number · beat link · hold · intent line · cast tags),
 * the chain_from loop-return as a marker on its slate. No cut / strike /
 * reorder — curation is G2, deferred; the stack carries NO buttons.
 */

const SCRIPT_HREF = "/runs/2026-07-03-spark-tidepool/script";

function mount(yaml = shotsYaml) {
  const sheet = parseShots(yaml);
  render(
    <MemoryRouter future={ROUTER_FUTURE}>
      <SlateStack sheet={sheet} scriptHref={SCRIPT_HREF} />
    </MemoryRouter>,
  );
  return sheet;
}

describe("SlateStack", () => {
  it("renders one slate per shot, as a semantic list", () => {
    mount();
    const stack = screen.getByRole("list");
    const slates = within(stack).getAllByRole("listitem");
    expect(slates).toHaveLength(4);
    // cut numbers, zero-padded like the booth's frame counters (cut + its
    // beat link can share digits — scope per slate)
    expect(within(slates[0]).getAllByText("01").length).toBeGreaterThan(0);
    expect(within(slates[3]).getAllByText("04").length).toBeGreaterThan(0);
  });

  it("each beat_id is a REAL link back to the script gate's beats", () => {
    mount();
    const beatLinks = screen.getAllByRole("link");
    expect(beatLinks).toHaveLength(4);
    for (const link of beatLinks) {
      expect(link).toHaveAttribute("href", SCRIPT_HREF);
    }
  });

  it("a frame without a beat_id gets no link, not a broken one", () => {
    mount("slug: s\nframes:\n- id: 1\n  cast: [sean]\n  beat: b\n  prompt: p\n");
    expect(screen.queryAllByRole("link")).toHaveLength(0);
  });

  it("the loop-return rides its slate: chain_from shows as 'returns to frame N'", () => {
    mount();
    const markers = screen.getAllByText(/returns to frame 1/i);
    expect(markers).toHaveLength(1);
  });

  it("slate detail: the one-line intent from the prompt + the cast tags", () => {
    mount();
    // establishing frame -> first sentence; edit frame -> the ONLY CHANGE delta
    expect(
      screen.getByText("Wide two-shot establishing frame."),
    ).toBeInTheDocument();
    expect(
      screen.getByText(/ONLY CHANGE: the mascot turns its head/),
    ).toBeInTheDocument();
    expect(screen.getAllByText("sean")).toHaveLength(4);
    expect(screen.getAllByText("claude-mascot")).toHaveLength(4);
    // holds read from the board (frame 1 holds 4; the default is 2)
    expect(screen.getByText("4")).toBeInTheDocument();
  });

  it("is DISPLAY-ONLY — no cut / strike / reorder controls (G2 deferred)", () => {
    mount();
    expect(screen.queryAllByRole("button")).toHaveLength(0);
  });
});
