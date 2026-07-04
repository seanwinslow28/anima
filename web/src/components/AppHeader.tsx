import { Link } from "react-router-dom";

/**
 * The warm app bar: the anima wordmark (Newsreader, a real home link) and the
 * quiet studio tag. Reads like a studio masthead, not a console title bar.
 */
export function AppHeader() {
  return (
    <header className="appbar">
      <Link to="/" className="wordmark">
        anima
      </Link>
      <span className="studiotag">studio</span>
    </header>
  );
}
