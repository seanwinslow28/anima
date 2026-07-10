import "./reelone.css";

/**
 * The fixed film-grain overlay — inline SVG turbulence at 5% opacity, no
 * external hosts. Pure texture: hidden from assistive tech, ignores pointers.
 */
export function FilmGrain() {
  return <div className="ro-grain" aria-hidden="true" />;
}
