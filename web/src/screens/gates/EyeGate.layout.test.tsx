import { readFileSync } from "node:fs";

import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { BurnIn } from "../../reelone/BurnIn";

const eyeGateCss = readFileSync("src/styles/eyegate.css", "utf8");
const boothCss = readFileSync("src/booth/booth.css", "utf8");

function rule(css: string, selector: string) {
  const start = css.indexOf(`${selector} {`);
  expect(start, `${selector} exists`).toBeGreaterThan(-1);
  return css.slice(start, css.indexOf("}", start));
}

describe("EyeGate P1 structural layout contract", () => {
  it("completes the booth height chain with a flex-column stage", () => {
    const stage = rule(boothCss, ".booth-stage");
    expect(stage).toMatch(/display:\s*flex/);
    expect(stage).toMatch(/flex-direction:\s*column/);
  });

  it("does not let centered app screens shrink-wrap inside the flex shell", () => {
    expect(rule(boothCss, ".booth-stage > *")).toMatch(/width:\s*100%/);
  });

  it("lays the projected stage and Em rail out as in-flow grid columns", () => {
    const auditorium = rule(eyeGateCss, ".eg-stagewrap");
    const stageColumn = rule(eyeGateCss, ".eg-stagecol");
    const rail = rule(eyeGateCss, ".eg-rail");

    expect(auditorium).toMatch(/display:\s*grid/);
    expect(auditorium).toMatch(
      /grid-template-columns:\s*minmax\(0,\s*1fr\)\s+280px/,
    );
    expect(stageColumn).toMatch(/position:\s*relative/);
    expect(stageColumn).toMatch(/min-height:\s*0/);
    expect(rail).not.toMatch(/position:\s*absolute/);
  });

  it("keeps both burn-ins in one collision-proof row", () => {
    render(
      <div className="eg-burns" data-testid="burn-ins">
        <span className="eg-burn">
          <BurnIn segments={["F01", "TAKE 1", "HOLD 2"]} />
        </span>
        <span className="eg-burn">
          <BurnIn segments={["12 FPS", "NB2", "$0.07"]} />
        </span>
      </div>,
    );

    expect(screen.getByTestId("burn-ins").children).toHaveLength(2);
    const burns = rule(eyeGateCss, ".eg-burns");
    expect(burns).toMatch(/display:\s*flex/);
    expect(burns).toMatch(/justify-content:\s*space-between/);
    expect(rule(eyeGateCss, ".eg-burn")).toMatch(/text-overflow:\s*ellipsis/);
  });

  it("clamps the summoned cheat sheet to the narrow viewport", () => {
    expect(rule(eyeGateCss, ".eg-cheat")).toMatch(
      /width:\s*min\(340px,\s*92vw\)/,
    );
  });

  it("keeps the projection beam inside the padded narrow viewport", () => {
    expect(rule(eyeGateCss, ".eg-beam")).toMatch(
      /max-width:\s*calc\(100vw\s*-\s*40px\)/,
    );
  });

  it("keeps the wipe tag above the type floor and legible over frame art", () => {
    const wipeTag = rule(eyeGateCss, ".eg-wipe-tag");

    expect(wipeTag).toMatch(/font-size:\s*11px/);
    expect(wipeTag).toMatch(/text-shadow:/);
  });

  it("sizes the stage from the remaining vertical room at short viewports", () => {
    const eyeGateBooth = rule(boothCss, ".booth:has(.eg-screen)");
    const stage = rule(eyeGateCss, ".eg-stage");

    expect(eyeGateBooth).toMatch(/height:\s*100vh/);
    expect(eyeGateBooth).toMatch(/overflow:\s*hidden/);
    expect(stage).toMatch(/height:\s*min\(74vh,\s*100%\)/);
    expect(stage).toMatch(/max-width:\s*100%/);
    expect(stage).not.toMatch(/width:[^;]*74vh/);
  });
});
