import "./reelone.css";

/**
 * The approve flourish — a grease-pencil ellipse drawn around the printed
 * take (stroke-dashoffset → 0 via the circledraw keyframe; `forwards` keeps
 * it drawn, and reduced-motion collapses the draw to instant). Position it
 * inside a relatively-positioned take cell; `on` arms the draw. Decorative:
 * hidden from AT — the verdict is real text elsewhere.
 */
export function CircledTake({ on = false }: { on?: boolean }) {
  return (
    <svg
      className={on ? "ro-circled on" : "ro-circled"}
      aria-hidden="true"
      viewBox="0 0 100 44"
      preserveAspectRatio="none"
    >
      <ellipse cx="50" cy="22" rx="47" ry="19" />
    </svg>
  );
}
