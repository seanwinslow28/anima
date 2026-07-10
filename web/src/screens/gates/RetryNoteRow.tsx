import { useEffect, useRef, useState } from "react";

import type { EmVerdict } from "../../api/types";

/*
 * The retake note row (U5b) — AGAIN's editable correction. The note is
 * PREFILLED from Em's read of the shown take (accept her fix in a keystroke,
 * or edit); it rides the retry as {note} and lands in Flo's prompt as
 * CORRECTION:, so it should name the desired END-STATE, not the defect —
 * which is exactly what Em's proposed_patches values are.
 */

/**
 * Compose the shown take's Em records into the prefill: her proposed fixes
 * first (`value — rationale`, the end-state plus why), her non-pass
 * reasoning as the fallback when she flagged without proposing. A passing
 * take prefills nothing — and claims no attribution.
 */
export function composeEmNote(records: EmVerdict[]): {
  note: string;
  fromEm: boolean;
} {
  const fixes = records.flatMap((em) =>
    em.proposed_patches.map((p) =>
      p.rationale ? `${String(p.value)} — ${p.rationale}` : String(p.value),
    ),
  );
  if (fixes.length > 0) return { note: fixes.join("; "), fromEm: true };
  const flagged = records
    .filter((em) => em.verdict !== "pass" && em.reasoning.trim() !== "")
    .map((em) => em.reasoning.trim());
  if (flagged.length > 0) return { note: flagged.join("; "), fromEm: true };
  return { note: "", fromEm: false };
}

export function RetryNoteRow({
  prefill,
  fromEm,
  onSend,
  onCancel,
}: {
  prefill: string;
  fromEm: boolean;
  onSend: (note: string) => void;
  onCancel: () => void;
}) {
  const [note, setNote] = useState(prefill);
  const inputRef = useRef<HTMLInputElement>(null);
  useEffect(() => {
    inputRef.current?.focus();
    inputRef.current?.select();
  }, []);

  // the prefill is non-empty whenever Em flagged something; the empty case
  // is guarded anyway so a 422 (empty note) can never leave this row
  const canSend = note.trim().length > 0;
  const send = () => {
    if (canSend) onSend(note.trim());
  };

  return (
    <div className="eg-againrow">
      <label className="eg-lbl" htmlFor="eg-again-note">
        Go again — the note rides the retake
        {fromEm && " · prefilled from Em"}
      </label>
      <input
        id="eg-again-note"
        ref={inputRef}
        className="eg-mono"
        value={note}
        onChange={(e) => setNote(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            e.preventDefault();
            send();
          } else if (e.key === "Escape") {
            onCancel();
          }
        }}
        aria-label={fromEm ? "Retake note, prefilled from Em" : "Retake note"}
      />
      <button
        type="button"
        className="eg-again-send"
        aria-label="Send the retake"
        disabled={!canSend}
        onClick={send}
      >
        SEND
      </button>
      <button
        type="button"
        className="eg-tsw"
        aria-label="Cancel the retake (Esc)"
        onClick={onCancel}
      >
        ESC
      </button>
    </div>
  );
}
