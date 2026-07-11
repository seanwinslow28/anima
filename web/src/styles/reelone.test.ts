import { readFileSync } from "node:fs";

import { describe, expect, test } from "vitest";

// The REEL ONE layers are plain CSS (vitest runs css:false, which stubs even
// ?raw CSS imports), so the guard reads them off disk: the exact mockup
// values are the contract — a drifted hex or a dropped keyframe is a real
// regression against the ratified look.
const read = (rel: string) =>
  readFileSync(new URL(rel, import.meta.url), "utf8");
const tokens = read("./reelone.tokens.css");
const motion = read("./reelone.motion.css");
const main = read("../main.tsx");
const cssSources = new Map([
  ["styles/gates.css", read("./gates.css")],
  ["reelone/reelone.css", read("../reelone/reelone.css")],
  ["styles/marquee.css", read("./marquee.css")],
  ["styles/eyegate.css", read("./eyegate.css")],
  ["screens/dev/systemsheet.css", read("../screens/dev/systemsheet.css")],
]);

describe("reelone.tokens.css", () => {
  test("carries the exact booth palette from the mockups", () => {
    for (const decl of [
      "--booth: #141018",
      "--booth2: #1D1722",
      "--booth3: #251E2B",
      "--line: #332A3C",
      "--tungsten: #E8B36A",
      "--tungsten-dim: #8A6F4D",
      "--screenlight: #FFF6E4",
      "--print: #7FA96B",
      "--hold: #D9A441",
      "--bakelite: #C24838",
      "--mute: #8F8798",
      "--text: #DDD5E0",
    ]) {
      expect(tokens).toContain(decl);
    }
  });

  test("names the lockdown palette additions on .reelone", () => {
    const reeloneBlock = tokens.match(/\.reelone\s*\{([\s\S]*?)\n\}/)?.[1] ?? "";
    for (const decl of [
      "--booth-deep: #0B080D",
      "--sprocket: #241D2C",
      "--on-tungsten: #101010",
      "--tungsten-bright: #F2C284",
    ]) {
      expect(reeloneBlock).toContain(decl);
    }
  });

  test("carries the lit continuity page set", () => {
    for (const decl of [
      "--page: #F7EFDC",
      "--page-ink: #2B2417",
      "--page-ink2: #57503F",
      "--page-rule: #C9BB98",
    ]) {
      expect(tokens).toContain(decl);
    }
  });

  test("ships the three type stacks (fallbacks, no licensed webfont)", () => {
    expect(tokens).toContain('"Futura", "Avenir Next", "Helvetica Neue"');
    expect(tokens).toContain('"SF Mono", Menlo, Consolas, monospace');
    expect(tokens).toContain("Georgia, serif");
  });

  test("scopes the booth to .reelone — never :root (v1a's --line stays warm)", () => {
    expect(tokens).toContain(".reelone");
    expect(tokens).not.toMatch(/:root\s*\{/);
  });
});

describe("REEL ONE CSS discipline", () => {
  test("keeps the seven named interface selectors at the 11px floor", () => {
    const selectors = [
      ["styles/gates.css", ".gate-approve small"],
      ["reelone/reelone.css", ".ro-fcell .ro-empty"],
      ["styles/marquee.css", ".mq-cta-mark--print"],
      ["reelone/reelone.css", ".ro-fcell .ro-cap"],
      ["styles/eyegate.css", ".eg-wipe-tag"],
      ["screens/dev/systemsheet.css", ".syssheet-sw"],
      ["screens/dev/systemsheet.css", ".syssheet button"],
    ] as const;

    for (const [file, selector] of selectors) {
      const source = cssSources.get(file) ?? "";
      const escaped = selector.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
      const rule =
        source.match(new RegExp(`${escaped}\\s*\\{([\\s\\S]*?)\\}`))?.[1] ?? "";
      const fontSize = Number(rule.match(/font-size:\s*([\d.]+)px/)?.[1]);
      expect(fontSize, `${file} ${selector}`).toBeGreaterThanOrEqual(11);
    }
  });

  test("uses the 900px responsive contract for gate columns", () => {
    const gates = cssSources.get("styles/gates.css") ?? "";
    expect(gates).toContain("@media (max-width: 900px)");
    expect(gates).not.toContain("@media (max-width: 960px)");
  });

  test("uses the reserved bakelite token for the failed flow-note border", () => {
    const eyeGate = cssSources.get("styles/eyegate.css") ?? "";
    expect(eyeGate).toMatch(
      /\.eg-flownote--failed\s*\{\s*border-color:\s*var\(--bakelite\);\s*\}/,
    );
  });
});

describe("reelone.motion.css", () => {
  test("defines the five REEL ONE keyframes", () => {
    for (const kf of [
      "@keyframes flicker",
      "@keyframes weave",
      "@keyframes circledraw",
      "@keyframes pulse",
      "@keyframes fade-through-black",
    ]) {
      expect(motion).toContain(kf);
    }
  });

  test("flicker is the ~1.5% print flicker, weave is sub-pixel", () => {
    expect(motion).toMatch(/flicker[\s\S]*?opacity:\s*\.986/);
    expect(motion).toMatch(/weave[\s\S]*?translate\(\.6px,\s*-\.4px\)/);
  });

  test("collapses under prefers-reduced-motion", () => {
    expect(motion).toContain("@media (prefers-reduced-motion: reduce)");
  });
});

describe("main.tsx wiring", () => {
  test("imports the reelone layers after tokens.css (extend, not replace)", () => {
    const tokensAt = main.indexOf("./styles/tokens.css");
    const roTokensAt = main.indexOf("./styles/reelone.tokens.css");
    const roMotionAt = main.indexOf("./styles/reelone.motion.css");
    expect(tokensAt).toBeGreaterThan(-1);
    expect(roTokensAt).toBeGreaterThan(tokensAt);
    expect(roMotionAt).toBeGreaterThan(roTokensAt);
  });
});
