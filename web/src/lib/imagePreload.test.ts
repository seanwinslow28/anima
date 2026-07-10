import { afterEach, describe, expect, it, vi } from "vitest";

import {
  preloadImage,
  resetPreloadCacheForTests,
  setImageFactoryForTests,
  type PreloadImageLike,
} from "./imagePreload";

/*
 * The eye-gate's image preloader (U5a cross-slice DoD): every loop frame and
 * every take is primed ONCE — the rock never flicker-loads, and a repeat
 * request rides the cache instead of a new fetch.
 */

/** A controllable Image stand-in (jsdom's Image never fires events). */
function makeFakeImages() {
  const created: Array<PreloadImageLike & { fire: (ev: "load" | "error") => void }> = [];
  setImageFactoryForTests(() => {
    const img = {
      src: "",
      onload: null as (() => void) | null,
      onerror: null as (() => void) | null,
      fire(ev: "load" | "error") {
        (ev === "load" ? img.onload : img.onerror)?.();
      },
    };
    created.push(img);
    return img;
  });
  return created;
}

afterEach(() => {
  setImageFactoryForTests(null);
  resetPreloadCacheForTests();
  vi.restoreAllMocks();
});

describe("preloadImage", () => {
  it("resolves ok on load and error on a 404 — the honest split", async () => {
    const imgs = makeFakeImages();

    const okP = preloadImage("/runs/r/frames/1/image");
    const badP = preloadImage("/runs/r/frames/9/image");
    expect(imgs.map((i) => i.src)).toEqual([
      "/runs/r/frames/1/image",
      "/runs/r/frames/9/image",
    ]);

    imgs[0].fire("load");
    imgs[1].fire("error");
    await expect(okP).resolves.toBe("ok");
    await expect(badP).resolves.toBe("error");
  });

  it("caches per url — a second request never creates a second fetch", async () => {
    const imgs = makeFakeImages();

    const first = preloadImage("/runs/r/frames/1/image");
    const second = preloadImage("/runs/r/frames/1/image");

    expect(imgs).toHaveLength(1);
    expect(second).toBe(first);

    imgs[0].fire("load");
    await expect(second).resolves.toBe("ok");
  });
});
