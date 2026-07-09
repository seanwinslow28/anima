# v1b "Elevate" — three visual directions (Fable-5 exploration pass, 2026-07-09)

Deliverable of the [v1b Elevate exploration brief](../2026-07-09-v1b-elevate-exploration-brief.md):
three genuinely distinct visual directions for the v1b gate screens + eye-gate, each answering
"what room is Sean standing in when he keeps taste?" differently. **Open [`index.html`](index.html)**
(every page is self-contained — inline CSS/JS, data-URI assets; no network needed).

| Direction | The room | Eye-gate | Reading gate | Run overview | Dossier |
|---|---|---|---|---|---|
| **A · PEGBAR** | the production office | [light table](pegbar-eyegate.html) | [route sheet](pegbar-reading.html) | [day sheet](pegbar-overview.html) | [mood + rationale](pegbar-dossier.html) |
| **B · REEL ONE** | the screening room | [the screening](reelone-eyegate.html) | [continuity report](reelone-reading.html) | [booth board](reelone-overview.html) | [mood + rationale](reelone-dossier.html) |
| **C · ACCESSION** | the gallery | [viewing wall](accession-eyegate.html) | [exhibition checklist](accession-reading.html) | [exhibition floor](accession-overview.html) | [mood + rationale](accession-dossier.html) |

- **Real content throughout:** the mascot's hand-drawn keys (idle→look→alert) drive the rock/flip loop;
  the two-attempt Em story is verbatim from `tests/server/conftest.py::make_generate_run`
  ("line weight drifts on the arm" → flag → note → pass); the reading gates carry the real Spark board
  (5 beats / 5 shots, `chain_from: 1`).
- **Eye-gate keys (all directions):** ⏎ approve · R retry · Space rock the loop · O onion ·
  D diff-wipe · [ ] wipe line · L lights-out · 1/2 attempts · ↑↓ frames.
- **Daemon deltas:** A and B need none for v1b; C names one optional delta (D7 — persist the
  accession record server-side on approve).
- Mood imagery: Higgsfield soul_2 (9 renders, subscription credits). Reference research briefs
  (dailies tools / animation paperwork / museum UI) are summarized inside each dossier.
- This is a **divergent direction pass** — no production code. The chosen direction (or blend)
  feeds the separate v1b TDD build kickoff.
