import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";

/**
 * The ⌘K command palette — U1 scaffold. STATIC nav targets only; run/stage/
 * action targets wire in as their screens land (U2a+). No network calls.
 *
 * A11y: modal dialog + the ARIA listbox pattern (the listbox is the single
 * focusable widget, options are its owned children — the one sanctioned
 * clickable that isn't a <button>/<a>). Focus is trapped on the listbox and
 * returned to the summoning element on close.
 */
const TARGETS = [
  { id: "palette-opt-dashboard", label: "Dashboard", to: "/" },
  { id: "palette-opt-system", label: "Design system", to: "/dev/system" },
] as const;

export function CommandPalette() {
  const [open, setOpen] = useState(false);
  const [active, setActive] = useState(0);
  const navigate = useNavigate();
  const listRef = useRef<HTMLUListElement>(null);
  const returnFocusRef = useRef<HTMLElement | null>(null);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        setOpen((wasOpen) => {
          if (!wasOpen) {
            returnFocusRef.current = document.activeElement as HTMLElement | null;
          }
          return !wasOpen;
        });
        setActive(0);
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  useEffect(() => {
    if (open) {
      listRef.current?.focus();
    } else {
      returnFocusRef.current?.focus();
      returnFocusRef.current = null;
    }
  }, [open]);

  if (!open) return null;

  const go = (target: (typeof TARGETS)[number]) => {
    setOpen(false);
    navigate(target.to);
  };

  const onListKeyDown = (e: React.KeyboardEvent) => {
    switch (e.key) {
      case "Escape":
        e.stopPropagation();
        setOpen(false);
        break;
      case "ArrowDown":
        e.preventDefault();
        setActive((a) => Math.min(a + 1, TARGETS.length - 1));
        break;
      case "ArrowUp":
        e.preventDefault();
        setActive((a) => Math.max(a - 1, 0));
        break;
      case "Enter":
        e.preventDefault();
        go(TARGETS[active]);
        break;
      case "Tab":
        // The listbox is the palette's only focus stop — trap.
        e.preventDefault();
        listRef.current?.focus();
        break;
    }
  };

  return (
    <div className="palette-backdrop" onClick={() => setOpen(false)}>
      <div
        role="dialog"
        aria-modal="true"
        aria-label="Command palette"
        className="palette"
        onClick={(e) => e.stopPropagation()}
      >
        <ul
          role="listbox"
          aria-label="Go to"
          tabIndex={0}
          ref={listRef}
          aria-activedescendant={TARGETS[active].id}
          onKeyDown={onListKeyDown}
          className="palette-list"
        >
          {TARGETS.map((target, i) => (
            <li
              key={target.id}
              id={target.id}
              role="option"
              aria-selected={i === active}
              className="palette-option"
              onClick={() => go(target)}
              onMouseEnter={() => setActive(i)}
            >
              {target.label}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
