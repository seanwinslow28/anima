import type { CostEstimate } from "../../api/types";
import { phaseLabel } from "../../lib/boothBoard";

/**
 * The box-office read on a gate: Maya's estimate band up front ("estimate,
 * not a cap" — D-H honesty), the by-phase breakdown + the house rule behind
 * the density gate (reveal on hover/focus, mirroring U2b's BoxOffice). A
 * null estimate reads as pending, never invented.
 */
export function CostPreview({ estimate }: { estimate: CostEstimate | null }) {
  return (
    <section className="gate-cost" aria-label="Box office — cost" tabIndex={0}>
      <div className="gate-cost-head">
        <span className="gate-lbl">Box office</span>
        <span className="gate-lbl gate-lbl--dim">estimate, not a cap</span>
      </div>
      {estimate ? (
        <p className="gate-cost-band gate-mono">
          est ${estimate.low_usd.toFixed(2)} – ${estimate.high_usd.toFixed(2)}{" "}
          · median ${estimate.median_usd.toFixed(2)}
        </p>
      ) : (
        <p className="gate-cost-band">
          estimate pending — Maya hasn't costed this plan yet
        </p>
      )}
      {/* density gate: the breakdown + the house rule arrive on intent */}
      <div className="gate-cost-detail" data-reveal>
        {estimate && (
          <table className="gate-cost-table">
            <tbody>
              {Object.entries(estimate.by_phase).map(([key, band]) => (
                <tr key={key}>
                  <td>{phaseLabel(key)}</td>
                  <td className="gate-mono">
                    ${band.low_usd.toFixed(2)} – ${band.high_usd.toFixed(2)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
        <p className="gate-cost-note">
          <b>Nothing burns compute until you approve.</b> Draft tier is the
          house default; pro screens only on your call or a critic pass.
        </p>
      </div>
    </section>
  );
}
