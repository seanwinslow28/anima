import "./reelone.css";

export type LampVerdict = "print" | "hold" | "fail";

const DEFAULT_WORD: Record<LampVerdict, string> = {
  print: "PRINT",
  hold: "HOLD",
  fail: "FAIL",
};

/**
 * A lit signal BEFORE a word. The lamp hue is semantic and reserved:
 * print = approve (green), hold = Em's amber, fail = bakelite. The verdict
 * is announced via aria-label so the color is never the only carrier.
 */
export function Lamp({ verdict, word }: { verdict: LampVerdict; word?: string }) {
  return (
    <span
      className={`ro-lamp ro-lamp--${verdict}`}
      role="img"
      aria-label={`verdict: ${verdict}`}
    >
      <i className="ro-lamp-dot" />
      {word ?? DEFAULT_WORD[verdict]}
    </span>
  );
}
