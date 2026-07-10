import { Link } from "react-router-dom";

/**
 * The booth app bar: the ANIMA wordmark in screenlight (tracked caps, the
 * SMPTE-leader face) over the tungsten-dim "screening room" sub. A real home
 * link — the projectionist can always walk back to the marquee.
 */
export function AppHeader() {
  return (
    <header className="booth-appbar">
      <Link to="/" className="booth-wordmark">
        ANIMA
        <small>screening room</small>
      </Link>
    </header>
  );
}
