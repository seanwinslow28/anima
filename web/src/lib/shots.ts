import { load } from "js-yaml";

import type { ShotFrame, ShotSheet } from "../api/types";

/*
 * The client-side shots.yaml parser (U4b; U5c's chain_from read reuses it).
 * The daemon serves the artifact raw (text/plain — G4), so the client parses
 * it for DISPLAY: the slate stack + the loop-return marker. Deliberately NOT
 * a re-implementation of load_shots' validation (coverage/conflict/ascending
 * ids are the daemon's job at --approve-storyboard) — this only refuses what
 * it cannot render. A throw surfaces as the artifact read's error state.
 */

export function parseShots(text: string): ShotSheet {
  const raw = load(text);
  if (typeof raw !== "object" || raw === null) {
    throw new Error("shots.yaml: not a mapping");
  }
  const doc = raw as Record<string, unknown>;

  const slug = doc.slug;
  if (typeof slug !== "string" || slug === "") {
    throw new Error("shots.yaml: missing slug");
  }
  if (!Array.isArray(doc.frames) || doc.frames.length === 0) {
    throw new Error("shots.yaml: frames must be a non-empty list");
  }

  const frames = doc.frames.map((entry, i): ShotFrame => {
    if (typeof entry !== "object" || entry === null) {
      throw new Error(`shots.yaml frames[${i}]: not a mapping`);
    }
    const f = entry as Record<string, unknown>;
    if (typeof f.id !== "number") {
      throw new Error(`shots.yaml frames[${i}]: missing id`);
    }
    return {
      id: f.id,
      cast: Array.isArray(f.cast) ? f.cast.map(String) : [],
      beat: typeof f.beat === "string" ? f.beat : "",
      prompt: typeof f.prompt === "string" ? f.prompt : "",
      hold: typeof f.hold === "number" ? f.hold : 2,
      beat_id: typeof f.beat_id === "number" ? f.beat_id : null,
      chain_from: typeof f.chain_from === "number" ? f.chain_from : null,
    };
  });

  return { slug, frames, locked: doc.locked === true };
}

/**
 * The slate's one-line intent, from the prompt. An edit frame's meaning lives
 * in its delta (Bea's Slice-A "Same … ONLY CHANGE: <delta>" discipline), so
 * from ONLY CHANGE: on when present; an establishing frame reads as its first
 * sentence.
 */
export function shotIntentLine(prompt: string): string {
  const at = prompt.indexOf("ONLY CHANGE:");
  const from = at >= 0 ? prompt.slice(at) : prompt;
  const dot = from.indexOf(". ");
  const line = dot >= 0 ? from.slice(0, dot + 1) : from;
  return line.trim();
}
