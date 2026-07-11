import { useState } from "react";

import "./systemsheet.css";
import { BurnIn } from "../../reelone/BurnIn";
import { CircledTake } from "../../reelone/CircledTake";
import { FilmGrain } from "../../reelone/FilmGrain";
import { Filmstrip, type FilmstripFrame } from "../../reelone/Filmstrip";
import { Lamp } from "../../reelone/Lamp";
import { Leader } from "../../reelone/Leader";
import { Timecode } from "../../reelone/Timecode";

// a 1×1 booth-toned png so printed cells show a thumbnail without assets
const THUMB =
  "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNka2r6DwAEXgH+2xBS9AAAAABJRU5ErkJggg==";

const SWATCHES: Array<[name: string, value: string, note: string, swatch?: string]> = [
  ["--booth", "#141018", "the room"],
  ["--booth2", "#1D1722", "raised surface"],
  ["--booth3", "#251E2B", "highest surface"],
  ["--booth-deep", "#0B080D", "stage + leader well"],
  ["--sprocket", "#241D2C", "film perforations"],
  ["--stage-edge", "#2B2333", "projector aperture"],
  ["--line", "#332A3C", "rules + borders"],
  ["--tungsten", "#E8B36A", "the practical / focus"],
  ["--tungsten-dim", "#8A6F4D", "dimmed practical"],
  ["--tungsten-bright", "#F2C284", "primary hover"],
  ["--screenlight", "#FFF6E4", "the lit frame"],
  ["--print", "#7FA96B", "lamp: approve"],
  ["--hold", "#D9A441", "lamp: Em holds"],
  ["--bakelite", "#C24838", "strike / fail only"],
  ["--text", "#DDD5E0", "body text"],
  ["--mute", "#8F8798", "secondary text"],
  ["--on-tungsten", "#101010", "text on the practical"],
  ["--tungsten-rgb", "232, 179, 106", "token-channel wash", "rgba(var(--tungsten-rgb), .35)"],
  ["--page", "#F7EFDC", "the lit page"],
  ["--page-ink", "#2B2417", "page body"],
  ["--page-ink2", "#57503F", "page secondary"],
  ["--page-rule", "#C9BB98", "page rules (decorative)"],
];

const REEL: FilmstripFrame[] = [
  { id: 1, label: "F01", status: "printed", src: THUMB },
  { id: 2, label: "F02", status: "printed", src: THUMB },
  { id: 3, label: "F03", status: "working", now: true },
  { id: 4, label: "F04", status: "pending" },
];

/**
 * The living token sheet — U0's demoable proof at /dev/system. A reference,
 * not a screen: it binds no run data and stays deliberately plain.
 */
export function SystemSheet() {
  const [leaderRun, setLeaderRun] = useState(0);
  const [leaderDone, setLeaderDone] = useState(false);

  return (
    <div className="reelone syssheet">
      <FilmGrain />
      <h1>REEL ONE — the design system</h1>
      <p className="syssheet-sub">
        the booth palette · type · lamps · motion — U0 reference sheet
      </p>

      <section>
        <h2>Palette</h2>
        <div className="syssheet-swatches">
          {SWATCHES.map(([name, value, note, swatch]) => (
            <div key={name} className="syssheet-sw">
              <i style={{ background: swatch ?? value }} />
              <span>
                {name} {value}
              </span>
              <small>{note}</small>
            </div>
          ))}
        </div>
      </section>

      <section>
        <h2>Button recipe</h2>
        <div className="syssheet-row">
          <button type="button" className="ro-button ro-button--primary">
            Primary action
          </button>
          <button type="button" className="ro-button ro-button--quiet">
            Quiet action
          </button>
          <button type="button" className="ro-button ro-button--danger">
            Danger action
          </button>
          <button type="button" className="ro-button ro-button--primary" disabled>
            Disabled
          </button>
        </div>
      </section>

      <section>
        <h2>Type</h2>
        <p className="syssheet-display">FUTURA TRACKED CAPS — 3 2 1</p>
        <p className="syssheet-mono">
          SF Mono — <Timecode frame={3} hold={2} /> ·{" "}
          <BurnIn segments={["12 FPS", "NB2", "$0.07"]} />
        </p>
        <p className="syssheet-page">
          Georgia, only on the lit continuity page — a sheet of paper in a dark
          booth.
        </p>
      </section>

      <section>
        <h2>Lamps</h2>
        <div className="syssheet-row">
          <Lamp verdict="print" />
          <Lamp verdict="hold" />
          <Lamp verdict="fail" />
          <Lamp verdict="hold" word="Em holds — stylus hand" />
        </div>
      </section>

      <section>
        <h2>The leader</h2>
        <div className="syssheet-stage">
          <Leader
            key={leaderRun}
            onDone={() => setLeaderDone(true)}
            caption="NEXT PICTURE UP"
          />
        </div>
        <div className="syssheet-row">
          <span className="syssheet-mono">
            {leaderDone ? "onDone fired ✓" : "counting down…"}
          </span>
          <button
            type="button"
            className="ro-button ro-button--quiet"
            onClick={() => {
              setLeaderDone(false);
              setLeaderRun((n) => n + 1);
            }}
          >
            run it again
          </button>
        </div>
      </section>

      <section>
        <h2>The circled take</h2>
        <div className="syssheet-row">
          <span className="syssheet-take">
            TAKE 2<CircledTake on />
          </span>
          <span className="syssheet-take">
            TAKE 1<CircledTake />
          </span>
        </div>
      </section>

      <section>
        <h2>The reel</h2>
        <Filmstrip frames={REEL} />
      </section>
    </div>
  );
}
