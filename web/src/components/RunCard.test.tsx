import { screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import type { RunSummary } from "../api/types";
import { nextActionCta } from "../lib/nextAction";
import { runDone, runReviewFrame, runStub } from "../test/fixtures";
import { renderApp } from "../test/render";
import { RunCard } from "./RunCard";

/** A crew-working run (wait tone) — Flo mid-draw. */
const runGenerating: RunSummary = {
  ...runReviewFrame,
  next_action: { kind: "generating", frame: 4, hint: "generating F04" },
};

describe("RunCard — the marquee card", () => {
  it("is a real link to the run, carrying the booth card class", () => {
    renderApp(<RunCard run={runReviewFrame} />);

    const card = screen.getByRole("link", { name: /open run spark-forest/i });
    expect(card).toHaveAttribute("href", "/runs/2026-07-04-spark-forest");
    expect(card).toHaveClass("mq-card", "ro-sprocket");
  });

  it("leads with slug (display) + stage (mono chip) + the one move", () => {
    renderApp(<RunCard run={runReviewFrame} />);

    expect(screen.getByText("spark-forest")).toHaveClass("mq-name");
    expect(screen.getByText("GENERATE")).toHaveClass("mq-stage");
    // The CTA copy is nextActionCta's, unchanged — only the dressing is new.
    const cta = nextActionCta(runReviewFrame.next_action);
    expect(screen.getByText(cta.label).closest(".mq-cta")).toHaveClass(
      "mq-cta--act",
    );
  });

  it("act tone reaches for it — the tungsten arrow mark", () => {
    renderApp(<RunCard run={runReviewFrame} />);

    const cta = screen
      .getByText(nextActionCta(runReviewFrame.next_action).label)
      .closest(".mq-cta")!;
    const mark = cta.querySelector(".mq-cta-mark");
    expect(mark).toHaveTextContent("→");
    expect(mark).toHaveAttribute("aria-hidden", "true");
  });

  it("wait tone shows the crew working — a pulse that respects reduced motion", () => {
    renderApp(<RunCard run={runGenerating} />);

    const cta = screen
      .getByText(nextActionCta(runGenerating.next_action).label)
      .closest(".mq-cta")!;
    expect(cta).toHaveClass("mq-cta--wait");
    // The pulsing mark rides the ro-pulse primitive (reduced-motion-guarded).
    expect(cta.querySelector(".mq-cta-mark")).toHaveClass("ro-pulse");
  });

  it("done tone reads as printed — the print-lamp mark", () => {
    renderApp(<RunCard run={runDone} />);

    const cta = screen
      .getByText(nextActionCta(runDone.next_action).label)
      .closest(".mq-cta")!;
    expect(cta).toHaveClass("mq-cta--done");
    const mark = cta.querySelector(".mq-cta-mark");
    expect(mark).toBeInTheDocument();
    expect(mark).toHaveAttribute("aria-hidden", "true");
  });

  it("keeps the secondary layer (id, stub, updated date) quiet in the meta row", () => {
    renderApp(<RunCard run={runStub} />);

    const meta = screen.getByText(runStub.run_id).closest(".mq-meta")!;
    expect(meta).toHaveTextContent("stub");
    // updated_at surfaces as its date, mono and on intent — never shouted.
    expect(meta).toHaveTextContent("2026-07-01");
  });

  it("renders without a date when updated_at is null", () => {
    const undated: RunSummary = { ...runReviewFrame, updated_at: null };
    renderApp(<RunCard run={undated} />);

    expect(
      screen.getByText(undated.run_id).closest(".mq-meta"),
    ).toBeInTheDocument();
  });
});
