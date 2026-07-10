import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { BeatsSheet } from "./BeatsSheet";
import type { BeatSheet } from "../../api/types";

/*
 * The beats sheet (U4a) — Sam's beats.json rendered as the structured sheet:
 * the logline, then each beat as an entry (id · title · intent · cast, with
 * emotional_beat / feel / notes as the detail line). A component over the
 * parsed JSON, not markdown.
 */

const sheet: BeatSheet = {
  slug: "the-spark-shared",
  logline:
    "Sean draws; the mascot notices and delights; everything settles back to the start.",
  beats: [
    {
      id: 1,
      title: "Establishing two-shot",
      intent: "Set the look, framing, and scale — the compositional anchor.",
      emotional_beat: "calm focus",
      cast: ["sean", "claude-mascot"],
      feel: "establishing — let it breathe",
      notes: "frame 5 returns here",
    },
    {
      id: 2,
      title: "The notice",
      intent: "The mascot perks up — the spark of catching the idea.",
      emotional_beat: "spark",
      cast: ["claude-mascot"],
    },
  ],
};

describe("BeatsSheet — the structured sheet", () => {
  it("renders the logline and every beat: id · title · intent · cast", () => {
    render(<BeatsSheet sheet={sheet} />);
    expect(
      screen.getByText(/Sean draws; the mascot notices and delights/),
    ).toBeInTheDocument();

    // the beats are a real list, one entry per beat
    expect(screen.getAllByRole("listitem")).toHaveLength(2);

    expect(screen.getByText("Establishing two-shot")).toBeInTheDocument();
    expect(
      screen.getByText(/Set the look, framing, and scale/),
    ).toBeInTheDocument();
    expect(screen.getByText("The notice")).toBeInTheDocument();

    // beat ids as visible marks
    expect(screen.getByText("01")).toBeInTheDocument();
    expect(screen.getByText("02")).toBeInTheDocument();

    // cast namespaces (beat 1 carries both, beat 2 only the mascot)
    expect(screen.getAllByText("sean")).toHaveLength(1);
    expect(screen.getAllByText("claude-mascot")).toHaveLength(2);
  });

  it("carries the detail line (emotional beat / feel / notes) when present, honestly absent otherwise", () => {
    render(<BeatsSheet sheet={sheet} />);
    // beat 1 has all three details
    expect(screen.getByText("calm focus")).toBeInTheDocument();
    expect(screen.getByText(/let it breathe/)).toBeInTheDocument();
    expect(screen.getByText(/frame 5 returns here/)).toBeInTheDocument();
    // beat 2 has only the emotional beat — no invented feel/notes
    expect(screen.getByText("spark")).toBeInTheDocument();
  });

  it("keeps the heading hierarchy under the gate's h1 (no h1 of its own)", () => {
    render(<BeatsSheet sheet={sheet} />);
    expect(screen.queryByRole("heading", { level: 1 })).toBeNull();
    // beat titles are headings so the sheet is navigable by landmark readers
    expect(
      screen.getByRole("heading", { name: /Establishing two-shot/ }),
    ).toBeInTheDocument();
  });
});
