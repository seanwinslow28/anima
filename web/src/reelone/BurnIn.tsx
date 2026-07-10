import "./reelone.css";

/**
 * The model+cost burn-in — one mono line ("12 FPS · NB2 · $0.07"), never a
 * panel (the density mandate: numbers you can stand behind, shown small).
 */
export function BurnIn({ segments }: { segments: string[] }) {
  return <span className="ro-burnin">{segments.join(" · ")}</span>;
}
