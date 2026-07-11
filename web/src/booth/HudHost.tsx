import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react";

/**
 * Per-screen dim level (D-B). "density" is the default everywhere: the shell
 * chrome may fade on idle, a screen's primary content NEVER does. "full" is
 * RESERVED for the eye-gate (U5) — U1 ships the mechanism only; nothing
 * renders full-dark yet.
 */
export type DimLevel = "density" | "full";

interface HudContextValue {
  /** True once the room has gone idle — only shell chrome may act on this. */
  chromeHidden: boolean;
  dimLevel: DimLevel;
  declareDimLevel: (level: DimLevel) => void;
  releaseDimLevel: () => void;
}

const HudContext = createContext<HudContextValue | null>(null);

const WAKE_EVENTS = ["mousemove", "keydown", "pointerdown"] as const;

/**
 * The summonable-HUD / idle-wake provider — the room disappears. Idle ~3s
 * fades the shell chrome; any input wakes it. Under prefers-reduced-motion
 * there is no timed fade at all: the chrome stays visible (a11y contract).
 */
export function HudHost({
  children,
  idleMs = 3000,
}: {
  children: ReactNode;
  idleMs?: number;
}) {
  const [chromeHidden, setChromeHidden] = useState(false);
  const [dimLevel, setDimLevel] = useState<DimLevel>("density");

  useEffect(() => {
    // jsdom has no matchMedia; treat its absence as motion-allowed.
    const reduce =
      typeof window.matchMedia === "function" &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduce) return;

    let idleTimer: ReturnType<typeof setTimeout>;
    const wake = () => {
      setChromeHidden(false);
      clearTimeout(idleTimer);
      idleTimer = setTimeout(() => setChromeHidden(true), idleMs);
    };
    WAKE_EVENTS.forEach((ev) => window.addEventListener(ev, wake));
    wake();
    return () => {
      clearTimeout(idleTimer);
      WAKE_EVENTS.forEach((ev) => window.removeEventListener(ev, wake));
    };
  }, [idleMs]);

  const declareDimLevel = useCallback((level: DimLevel) => setDimLevel(level), []);
  const releaseDimLevel = useCallback(() => setDimLevel("density"), []);

  return (
    <HudContext.Provider value={{ chromeHidden, dimLevel, declareDimLevel, releaseDimLevel }}>
      {children}
    </HudContext.Provider>
  );
}

/** Shell-chrome consumer hook: is the room idle, and at what dim level. */
export function useHud(): HudContextValue {
  const ctx = useContext(HudContext);
  if (!ctx) throw new Error("useHud must be used inside <HudHost>");
  return ctx;
}

/**
 * The tolerant consumer (U5c): a screen that reacts to the HUD when the
 * booth is around it but renders fine bare (unit tests mount screens without
 * the shell). Null outside a <HudHost>.
 */
export function useHudOptional(): HudContextValue | null {
  return useContext(HudContext);
}

/**
 * Screen-side declaration: `useDimLevel("full")` opts a screen into the
 * eye-gate's full idle-dark (U5); calling it with no argument just reads the
 * current level. The declaration releases back to "density" on unmount.
 */
export function useDimLevel(level?: DimLevel): DimLevel {
  const { dimLevel, declareDimLevel, releaseDimLevel } = useHud();
  useEffect(() => {
    if (!level) return;
    declareDimLevel(level);
    return releaseDimLevel;
  }, [level, declareDimLevel, releaseDimLevel]);
  return dimLevel;
}
