import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { CostPreview } from "./CostPreview";
import { GateShell } from "./GateShell";
import { Markdown } from "./Markdown";
import { rawAuthoring } from "../../test/fixtures";

describe("GateShell — the reusable lit-page document-gate frame", () => {
  function shell() {
    return render(
      <GateShell
        stamp="PLAN · REEL ONE"
        title="The plan"
        byline="authored by Maya · Opus"
        aside={<div data-testid="aside-slot">secondary</div>}
        actions={<button type="button">Approve — print it</button>}
      >
        <p>Maya's prose.</p>
      </GateShell>,
    );
  }

  it("renders the gate title as the page's ONE h1", () => {
    shell();
    const h1s = screen.getAllByRole("heading", { level: 1 });
    expect(h1s).toHaveLength(1);
    expect(h1s[0]).toHaveTextContent("The plan");
  });

  it("renders the stamp head, byline, artifact body, aside and action bar", () => {
    shell();
    expect(screen.getByText("PLAN · REEL ONE")).toBeInTheDocument();
    expect(screen.getByText(/authored by Maya/)).toBeInTheDocument();
    expect(screen.getByText("Maya's prose.")).toBeInTheDocument();
    expect(screen.getByTestId("aside-slot")).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: /approve — print it/i }),
    ).toBeInTheDocument();
  });

  it("the artifact is the page — the lit sheet is an article the body sits in", () => {
    shell();
    const article = screen.getByRole("article");
    expect(article).toHaveClass("gate-page");
    expect(article).toHaveTextContent("Maya's prose.");
  });
});

describe("Markdown — the lit page renders prose, not a <pre> dump", () => {
  it("renders headings/lists/gfm-tables as elements", () => {
    const { container } = render(
      <Markdown
        text={"# Plan\n\n- one frame\n\n| phase | cost |\n| --- | --- |\n| generate | $0.35 |"}
      />,
    );
    expect(container.querySelector("ul li")).toHaveTextContent("one frame");
    expect(container.querySelector("table td")).toHaveTextContent("generate");
    expect(container.querySelector("pre")).toBeNull();
  });

  it("demotes the document's headings so the shell keeps the only h1", () => {
    const { container } = render(<Markdown text={"# Plan\n\n## Frames"} />);
    expect(container.querySelector("h1")).toBeNull();
    expect(container.querySelector("h2")).toHaveTextContent("Plan");
    expect(container.querySelector("h3")).toHaveTextContent("Frames");
  });
});

describe("CostPreview — the box-office read on a gate", () => {
  it("shows the band + the honesty label, with by-phase detail on intent", () => {
    render(<CostPreview estimate={rawAuthoring.plan.cost_estimate} />);
    expect(screen.getByText(/estimate, not a cap/i)).toBeInTheDocument();
    expect(screen.getByText(/est \$0\.35 – \$2\.25 · median \$0\.93/)).toBeInTheDocument();
    // the by-phase breakdown + house rule live behind the density gate
    expect(screen.getByText("Generate")).toBeInTheDocument();
    expect(screen.getByText(/nothing burns compute until you approve/i)).toBeInTheDocument();
    const detail = screen.getByText(/nothing burns compute/i).closest("[data-reveal]");
    expect(detail).not.toBeNull();
  });

  it("a null estimate reads as pending, never invented", () => {
    render(<CostPreview estimate={null} />);
    expect(screen.getByText(/estimate pending/i)).toBeInTheDocument();
  });
});
