import { useEffect, useState } from "react";

/*
 * The eye-gate's image preloader (U5a cross-slice DoD). Every loop frame and
 * every take is primed through one browser <img> fetch and then cached at
 * module level, so the rock swaps between already-decoded images — never a
 * flicker-load, never a per-frame fetch mid-run. A url that 404s resolves
 * "error" (the honest state's signal), it never throws.
 */

export type PreloadStatus = "loading" | "ok" | "error";

/** The slice of HTMLImageElement the preloader drives (jsdom's Image never
 *  fires events, so tests inject a controllable stand-in). */
export interface PreloadImageLike {
  src: string;
  onload: (() => void) | null;
  onerror: (() => void) | null;
}

let imageFactory: (() => PreloadImageLike) | null = null;

export function setImageFactoryForTests(
  factory: (() => PreloadImageLike) | null,
): void {
  imageFactory = factory;
}

const cache = new Map<string, Promise<"ok" | "error">>();

export function resetPreloadCacheForTests(): void {
  cache.clear();
}

/** Prime one url. Cached: the same url never fetches twice. */
export function preloadImage(url: string): Promise<"ok" | "error"> {
  let pending = cache.get(url);
  if (!pending) {
    pending = new Promise((resolve) => {
      // HTMLImageElement's handler signatures are wider; the preloader only
      // ever assigns zero-arg closures, so the narrow view is safe.
      const img: PreloadImageLike = imageFactory
        ? imageFactory()
        : (new Image() as unknown as PreloadImageLike);
      img.onload = () => resolve("ok");
      img.onerror = () => resolve("error");
      img.src = url;
    });
    cache.set(url, pending);
  }
  return pending;
}

/**
 * Prime a set of urls and track each one's status. Absent key = not yet
 * requested; "loading" until the browser answers.
 */
export function useImagePreload(urls: string[]): Record<string, PreloadStatus> {
  const [statuses, setStatuses] = useState<Record<string, PreloadStatus>>({});
  const key = urls.join("\n");

  useEffect(() => {
    let alive = true;
    for (const url of urls) {
      setStatuses((prev) =>
        url in prev ? prev : { ...prev, [url]: "loading" },
      );
      void preloadImage(url).then((s) => {
        if (!alive) return;
        setStatuses((prev) => (prev[url] === s ? prev : { ...prev, [url]: s }));
      });
    }
    return () => {
      alive = false;
    };
    // the joined key is the real trigger (a fresh array each render is fine)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [key]);

  return statuses;
}
