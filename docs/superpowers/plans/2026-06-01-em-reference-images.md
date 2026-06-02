# Em Reference-Images Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give Em (anima's T2 vision critic) the Bible — a capped, Bible-driven reference-plate bundle plus the character's `IR.*`/`AC.*` criteria — so she stops grading reference-blind, then re-baseline to measure the precision lift while holding `false_pass_rate` at 0.00; fold in the agy rate-cap wrapper fix and the case-7 xfail flip.

**Architecture:** Four test-pinned code seams + an eval re-wire + costed live runs behind human gates. (1) `select_references()` — a Bible-driven, capped, forward-compatible reference selector. (2) Em reads references (explicit image ordering, subject = image 1, both Gemini + Opus paths, incl. phase-6) and surfaces `query_by_character ∩ query_by_phase` from `ctx.criteria`. (3) The agy wrapper raises a distinct `RateCapExhausted` on empty/quota responses (never on merely-malformed). (4) case-7 flips xfail→green via an input-key validity fix + `IR.sean.*` ID alignment + a prompt-reading mock. Then the eval re-wires for structural parity (`character_id` per case + the *same* `select_references` in eval and prod), and a live re-baseline + bake-off re-run measure the result.

**Tech Stack:** Python 3.14 (`/Users/seanwinslow/Code-Brain/anima/.venv` — symlinked into the worktree as `.venv`), pytest, PyYAML, Pillow, `agy` CLI (Gemini 3.1 Pro), `claude-agent-sdk` (Opus vision). Mirrors the established `evals/vision_critic/` + `evals/character_designer/` idioms.

**Spec:** [`docs/superpowers/specs/2026-06-01-em-reference-images-design.md`](../specs/2026-06-01-em-reference-images-design.md). Read it first — this plan implements it section-by-section.

---

## Environment & operational guardrails (read before Task 0)

- **Worktree:** you are in `/Users/seanwinslow/Code-Brain/anima/.claude/worktrees/feature+em-reference-images/`, branch `feature/em-reference-images`, off `main` @ `458b248` (the #12 merge). A `.venv` symlink → the main checkout's venv already exists, so **`.venv/bin/python` and `.venv/bin/pytest` work from the worktree**.
- **Sole-agent:** one idle second session (PID 22428) is in the main checkout; the worktree isolates us. **Never kill any process** — Failure-2's near-miss was an authorized kill of the wrong PID.
- **No `ANTHROPIC_API_KEY`** — the SDK uses Claude Code auth; keep it that way. `.env` has `GEMINI_API_KEY` + `FAL_KEY`. In any heredoc Python, call `load_dotenv('.env')` explicitly.
- **Tests run per-directory:** `.venv/bin/python -m pytest tests/` and `.venv/bin/python -m pytest pipeline/tests/` are run **separately** (a combined run collides on a duplicate `tests` package basename). Eval suites are named `runner.py` (default discovery skips them) — run explicitly.
- **Discipline:** never weaken Em's `cites_criteria` invariant; never tune a case to flatter Em (a label edit is legitimate only as a validity fix). Update `CHANGELOG.md` on every change.
- **Commit message footer** (every commit):
  ```
  Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
  ```

---

## File Structure

**New:**
- `pipeline/agents/reference_selection.py` — `select_references()` + `_resolve_folder()` + `_select_turnarounds()` + `ReferenceSelectionError`. One responsibility: given a `character_id`, return the capped Bible reference bundle. Pure (filesystem-read only), fully unit-testable.
- `tests/test_reference_selection.py` — unit tests for the selector (synthetic Bibles + one real-Bible integration check).
- `tests/test_cli_runners_rate_cap.py` — unit tests for `RateCapExhausted` (empty vs malformed vs valid vs stub).
- `tests/test_vision_critic_references.py` — Em attaches references (subject first, both paths, phase-6) + the prompt ordering block.
- `tests/test_vision_critic_criteria.py` — Em surfaces `IR.*`/`AC.*` from `ctx.criteria`; graceful when `None`/empty.

**Modified:**
- `pipeline/agents/cli_runners.py` — `run_antigravity_with_image` raises `RateCapExhausted`; add `_QUOTA_SIGNALS`, `_read_agy_log()`, `RateCapExhausted`.
- `pipeline/agents/vision_critic.py` — `run()` attaches references; `_build_prompt` gains the ordering block + criteria block + an `n_references` param; new helpers `_resolve_references`, `_characters_root`, `_criteria_block`; module constants `_CHARACTERS_ROOT`, `_CHECKPOINT_PHASE`.
- `evals/vision_critic/cases.yaml` — add `character_id: sean` per case.
- `evals/vision_critic/conftest.py` — `eval_manifest()` + `merged_criteria()` helpers.
- `evals/vision_critic/runner.py` — `_ctx_for_case` threads `character_id` + criteria + characters_root.
- `evals/vision_critic/score.py` — `_ctx` threads `character_id` + criteria; `last-run.md` records the resolved reference list.
- `evals/character_designer/cases.yaml` + `runner.py` — case-7 input-key fix + `IR.sean.*` alignment (and the schema-cross-register test's arbitrary `sean-anchor` → `sean`).
- `CHANGELOG.md`, `CLAUDE.md` (Em row), the dated field report.

**Commit map:** Task 1 → commit 1; Task 2 → commit 2; Task 3 → commit 3; Task 4 → commit 4; Task 5 → commit 5; Task 6 → commit 6; Task 7 (live re-baseline) → STOP GATE then commit 7; Task 8 (bake-off) → commit 8; Task 9 (docs) → commit 9.

---

## Task 0: Setup & baseline capture

**Files:** none (verification only).

- [ ] **Step 1: Confirm worktree + venv**

Run:
```bash
cd /Users/seanwinslow/Code-Brain/anima/.claude/worktrees/feature+em-reference-images
git rev-parse --abbrev-ref HEAD
.venv/bin/python -c "import pipeline.agents.vision_critic; print('imports OK')"
```
Expected: `feature/em-reference-images`, `imports OK`.

- [ ] **Step 2: Capture the baseline test counts (the before-numbers)**

Run:
```bash
.venv/bin/python -m pytest tests/ -q 2>&1 | tail -3
.venv/bin/python -m pytest evals/vision_critic/runner.py -q 2>&1 | tail -3
.venv/bin/python -m pytest evals/character_designer/runner.py -q 2>&1 | tail -3
```
Expected: `tests/` all green (record the count — should be ~242). `evals/vision_critic/runner.py` green (30 passed + 6 xpassed per the handoff). `evals/character_designer/runner.py` green with **1 xfailed** (`closing-the-loop-em-cites-cy-rules`) + 1 xpassed. **Record all three counts** — they are the before-numbers for Task 9. Do not proceed if `tests/` is red.

---

## Task 1: agy rate-cap fix — `RateCapExhausted` (spec §6)

**Files:**
- Modify: `pipeline/agents/cli_runners.py`
- Test: `tests/test_cli_runners_rate_cap.py`

The wrapper scans stderr for rate-cap signals, but agy writes the 429 to its **log file** and returns exit-0 with **empty stdout** → reported `ok=True` → Em silently borderlines. Fix: raise a distinct `RateCapExhausted` on **(a)** empty-stdout-exit-0 or **(b)** an explicit quota signal in stderr/log. A **non-empty-but-unparseable** response is NOT a rate cap — it returns normally for `_parse` to handle. Sequenced first so it protects the costed re-baseline (Task 7).

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_cli_runners_rate_cap.py
"""agy rate-cap detection: a quota-exhausted/empty response must RAISE a distinct
RateCapExhausted, never silently borderline. The empty-vs-malformed distinction is
load-bearing — a malformed-but-non-empty response is the documented defensive-
borderline mode (postmortem Failure 1), NOT a throttle."""
from __future__ import annotations

import asyncio

import pytest

from pipeline.agents import cli_runners
from pipeline.agents.cli_runners import RateCapExhausted, run_antigravity_with_image


class _FakeProc:
    def __init__(self, stdout: bytes, stderr: bytes, returncode: int):
        self._stdout, self._stderr, self.returncode = stdout, stderr, returncode

    async def communicate(self):
        return self._stdout, self._stderr


def _patch_agy(monkeypatch, *, stdout: bytes, stderr: bytes = b"",
               returncode: int = 0, log_text: str = ""):
    """Make agy 'present' and return a controlled process result + log tail."""
    monkeypatch.setattr(cli_runners.shutil, "which", lambda _b: "/usr/local/bin/agy")
    monkeypatch.setattr(cli_runners, "_read_agy_log", lambda: log_text)

    async def fake_exec(*_args, **_kwargs):
        return _FakeProc(stdout, stderr, returncode)

    monkeypatch.setattr(cli_runners.asyncio, "create_subprocess_exec", fake_exec)


def test_empty_stdout_exit_zero_raises(monkeypatch):
    _patch_agy(monkeypatch, stdout=b"   \n", returncode=0)
    with pytest.raises(RateCapExhausted):
        asyncio.run(run_antigravity_with_image(prompt="p", image_paths=[]))


def test_429_in_stderr_raises(monkeypatch):
    _patch_agy(monkeypatch, stdout=b'{"verdict":"pass"}',
               stderr=b"RESOURCE_EXHAUSTED (code 429): Individual quota reached")
    with pytest.raises(RateCapExhausted):
        asyncio.run(run_antigravity_with_image(prompt="p", image_paths=[]))


def test_429_in_log_file_raises(monkeypatch):
    # agy writes the 429 to its LOG, not stderr — the exact production bug.
    _patch_agy(monkeypatch, stdout=b'{"verdict":"pass"}', stderr=b"",
               log_text="2026-06-01 ... RESOURCE_EXHAUSTED (code 429): quota reached")
    with pytest.raises(RateCapExhausted):
        asyncio.run(run_antigravity_with_image(prompt="p", image_paths=[]))


def test_nonempty_unparseable_does_NOT_raise(monkeypatch):
    # Malformed but non-empty → stays on the defensive-borderline path, NOT a rate cap.
    _patch_agy(monkeypatch, stdout=b"I think this frame looks fine; no JSON here.")
    resp = asyncio.run(run_antigravity_with_image(prompt="p", image_paths=[]))
    assert resp.ok
    assert "looks fine" in resp.text


def test_valid_response_passes_through(monkeypatch):
    _patch_agy(monkeypatch, stdout=b'{"verdict":"pass","confidence":0.9}')
    resp = asyncio.run(run_antigravity_with_image(prompt="p", image_paths=[]))
    assert resp.ok and "pass" in resp.text


def test_stub_fallback_unaffected(monkeypatch):
    # Binary absent → deterministic stub, never a rate cap.
    monkeypatch.setattr(cli_runners.shutil, "which", lambda _b: None)
    resp = asyncio.run(run_antigravity_with_image(prompt="p", image_paths=[]))
    assert resp.ok and resp.stub_fallback
```

- [ ] **Step 2: Run to verify failure**

Run: `.venv/bin/pytest tests/test_cli_runners_rate_cap.py -v`
Expected: FAIL — `ImportError: cannot import name 'RateCapExhausted'` (and `_read_agy_log` not yet defined).

- [ ] **Step 3: Discover agy's log path (best-effort, for signal (b))**

Run:
```bash
ls -la ~/.antigravity* ~/.config/antigravity* ~/Library/Logs/*antigravity* ~/.agy* 2>/dev/null
find ~ -maxdepth 4 -iname '*agy*log*' -o -iname '*antigravity*log*' 2>/dev/null | head
```
Note any path found. If none is found, that is fine — signal **(a)** empty-stdout already catches the observed failure; record `_AGY_LOG_CANDIDATES = ()` and rely on (a) + stderr. If a path is found, add it to `_AGY_LOG_CANDIDATES` in Step 4.

- [ ] **Step 4: Implement the fix**

In `pipeline/agents/cli_runners.py`, **add near the top** (after the imports, before `ANTI_GRAVITY_BIN`):

```python
class RateCapExhausted(Exception):
    """agy returned a quota-exhausted / empty response (not a verdict).

    Distinct from a JSON-parse failure (the documented defensive-borderline mode):
    this means the upstream quota is exhausted and Em received NO usable answer.
    Callers must surface it as an errored gap or escalate — never silently
    borderline. See docs/anima-test-runs/2026-06-01-em-critic-spine-hardening-
    postmortem.md (the bake-off finding)."""
```

**Replace** the `_RATE_CAP_SIGNALS` definition with:

```python
# Signatures that mean the upstream quota is exhausted. agy writes these to its
# LOG FILE (and sometimes stderr); they are NOT in stdout. Treated as a RAISE,
# distinct from a non-empty-but-malformed response (defensive-borderline).
_QUOTA_SIGNALS = ("429", "resource_exhausted", "quota", "rate limit", "rate-limited")

# Best-effort candidate paths for agy's recent log (filled from Task 1 Step 3;
# empty tuple is fine — signal (a) empty-stdout still catches the observed bug).
_AGY_LOG_CANDIDATES: tuple[str, ...] = ()


def _read_agy_log() -> str:
    """Best-effort read of agy's recent log tail, where it writes 429 /
    RESOURCE_EXHAUSTED that don't appear on stderr. Returns '' if no log can be
    located/read — in which case the empty-stdout signal still catches the
    observed quota failure. Monkeypatched in tests."""
    from pathlib import Path as _Path
    for candidate in _AGY_LOG_CANDIDATES:
        try:
            p = _Path(candidate).expanduser()
            if p.exists():
                return p.read_text(encoding="utf-8", errors="replace")[-4000:]
        except OSError:
            continue
    return ""
```

**Replace** the success-branch return (the block that decodes stdout/stderr, computes `rate_capped`, and returns `CLIResponse`) with:

```python
        text = stdout.decode("utf-8", errors="replace")
        err_text = stderr.decode("utf-8", errors="replace")
        exit_code = proc.returncode or 0
        # Rate-cap / quota detection (spec §6). Two RAISE signals, kept distinct
        # from a parse failure:
        #   (a) empty/whitespace stdout on exit-0  — the observed failure; primary.
        #   (b) an explicit quota signal in stderr OR agy's log  — corroborating.
        # A NON-EMPTY but unparseable response is NOT a rate cap: it returns
        # normally and vision_critic._parse handles it as defensive-borderline.
        combined = (err_text + "\n" + _read_agy_log()).lower()
        quota_signal = any(sig in combined for sig in _QUOTA_SIGNALS)
        if exit_code == 0 and (not text.strip() or quota_signal):
            raise RateCapExhausted(
                f"agy returned a quota-exhausted/empty response "
                f"(empty_stdout={not text.strip()}, quota_signal={quota_signal}). "
                "Treating as missing data, not a verdict — Em must error/escalate, "
                "never silently borderline."
            )
        return CLIResponse(
            cli="antigravity",
            text=text,
            tokens=None,
            duration_s=time.monotonic() - start,
            exit_code=exit_code,
            rate_capped=False,
            error=err_text if proc.returncode else None,
        )
```

(Leave the `CLIResponse.rate_capped` field in place — vestigial but harmless; other call sites may read it.)

- [ ] **Step 5: Run the tests to verify they pass**

Run: `.venv/bin/pytest tests/test_cli_runners_rate_cap.py -v`
Expected: 6 passed.

- [ ] **Step 6: Run the full contract suite (no regression)**

Run: `.venv/bin/python -m pytest tests/ -q 2>&1 | tail -3`
Expected: baseline count + 6 new tests, all green.

- [ ] **Step 7: Commit**

```bash
git add pipeline/agents/cli_runners.py tests/test_cli_runners_rate_cap.py
git commit -m "$(cat <<'EOF'
fix(cli_runners): raise RateCapExhausted on agy quota/empty — never silent borderline

agy writes 429/RESOURCE_EXHAUSTED to its LOG FILE and returns exit-0 with empty
stdout, so the stderr-only scan reported ok=True and every frame silently
degraded to borderline during quota exhaustion (the bake-off finding). Now the
wrapper raises a DISTINCT RateCapExhausted on (a) empty-stdout-exit-0 or (b) an
explicit quota signal in stderr/log. A non-empty-but-malformed response is NOT a
rate cap — it stays on the defensive-borderline path (postmortem Failure 1). The
empty-vs-malformed distinction keeps the two failure modes separate in the trace.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 2: `select_references()` — the Bible-driven seam (spec §4)

**Files:**
- Create: `pipeline/agents/reference_selection.py`
- Test: `tests/test_reference_selection.py`

A pure selector: given `character_id`, return `[anchor.png, *up-to-cap canonical turnarounds]` resolved from the Bible (folder mapped via `character.yaml`, turnarounds globbed + ranked for view diversity). Missing plates dropped with a log note (no raise). The signature accepts `checkpoint`/`beat` so view-aware selection (approach A) drops in later.

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_reference_selection.py
"""select_references: the fixed, Bible-driven, capped reference bundle (approach B)."""
from __future__ import annotations

from pathlib import Path

from pipeline.agents.reference_selection import select_references


def _make_char(tmp_path: Path, char_id: str, turnarounds: list[str], *, anchor: bool = True) -> Path:
    """A synthetic Bible: folder name deliberately != character_id (mirrors
    sean-anchor/ holding character_id 'sean')."""
    folder = tmp_path / f"{char_id}-folder"
    (folder / "turnarounds").mkdir(parents=True)
    (folder / "character.yaml").write_text(f"character_id: {char_id}\n", encoding="utf-8")
    if anchor:
        (folder / "anchor.png").write_bytes(b"x")
    for name in turnarounds:
        (folder / "turnarounds" / f"{name}.png").write_bytes(b"x")
    return folder


def test_resolves_folder_by_character_yaml_not_foldername(tmp_path):
    _make_char(tmp_path, "sean", ["head-front", "body-3quarter"])
    refs = select_references("sean", "phase_5_generate", "", characters_root=tmp_path)
    assert refs and refs[0].name == "anchor.png"
    assert refs[0].parent.name == "sean-folder"  # found via character.yaml, not name


def test_sean_like_bundle_is_diverse_views(tmp_path):
    _make_char(tmp_path, "sean", [
        "head-front", "head-3quarter", "head-profile-left", "head-profile-right",
        "head-back", "body-3quarter", "body-back", "body-profile-left", "body-profile-right",
    ])
    refs = select_references("sean", "phase_5_generate", "", characters_root=tmp_path, cap=3)
    assert [p.name for p in refs] == [
        "anchor.png", "head-front.png", "head-profile-left.png", "body-3quarter.png",
    ]


def test_mascot_all_body_generalizes(tmp_path):
    _make_char(tmp_path, "claude-mascot", [
        "body-front", "body-3quarter", "body-side", "body-back", "body-3quarter-back",
    ])
    refs = select_references("claude-mascot", "phase_5_generate", "", characters_root=tmp_path, cap=3)
    # No head-* plates → falls through to body views; still diverse, anchor + 3.
    assert [p.name for p in refs] == [
        "anchor.png", "body-3quarter.png", "body-front.png", "body-side.png",
    ]


def test_missing_anchor_dropped_not_raised(tmp_path):
    _make_char(tmp_path, "x", ["head-front"], anchor=False)
    refs = select_references("x", "phase_5_generate", "", characters_root=tmp_path)
    assert [p.name for p in refs] == ["head-front.png"]


def test_unknown_character_returns_empty(tmp_path):
    (tmp_path / "other").mkdir()
    assert select_references("nobody", "phase_5_generate", "", characters_root=tmp_path) == []


def test_empty_character_id_returns_empty(tmp_path):
    assert select_references("", "phase_5_generate", "", characters_root=tmp_path) == []


def test_real_sean_bible_target_bundle():
    """Integration: the committed (locked) Sean Bible → the brainstorm target bundle."""
    repo_characters = Path(__file__).resolve().parents[1] / "characters"
    refs = select_references("sean", "phase_5_generate", "", characters_root=repo_characters, cap=3)
    assert [p.name for p in refs] == [
        "anchor.png", "head-front.png", "head-profile-left.png", "body-3quarter.png",
    ]
```

- [ ] **Step 2: Run to verify failure**

Run: `.venv/bin/pytest tests/test_reference_selection.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'pipeline.agents.reference_selection'`.

- [ ] **Step 3: Implement the selector**

```python
# pipeline/agents/reference_selection.py
"""Reference-bundle selection for Em (the T2 vision critic).

Approach B (this version): a FIXED, Bible-driven, capped bundle — the character's
anchor.png + up to `cap` canonical deduped turnarounds (front / 3-quarter /
profile) — resolved FROM THE BIBLE folder, ignoring checkpoint/beat. The signature
already accepts checkpoint/beat so view-aware selection (approach A) drops into
this module later with no change to the eval contract.

Bible-driven, NOT hardcoded filenames: the anchor is <folder>/anchor.png;
turnarounds are globbed from <folder>/turnarounds/ and ranked by a view-preference
list, so the function generalizes to any character (e.g. claude-mascot's all-body
crops) with no code change. Every path is existence-checked; a missing plate is
dropped with a log note — a thin bundle is honest, the critic never crashes on a
gap. The folder key (sean-anchor/) and the IR character_id (sean) are allowed to
differ; character.yaml is the single source of truth for the mapping.
"""
from __future__ import annotations

import logging
from pathlib import Path

import yaml

log = logging.getLogger(__name__)


class ReferenceSelectionError(Exception):
    """Unrecoverable mis-configuration (e.g. characters_root is not a directory).
    A missing INDIVIDUAL plate never raises — it is dropped with a log note."""


# Ordered view preference. For each pattern in order, the resolver picks the first
# UNUSED turnaround whose stem CONTAINS it, until `cap` are chosen. Ordered for view
# DIVERSITY (a front face, a profile face, a body-proportion view) rather than three
# near-identical head shots — so Sean → head-front + head-profile-left + body-3quarter,
# and the mascot (all-body) → body-3quarter + body-front + body-side.
_TURNAROUND_PREFERENCE: tuple[str, ...] = (
    "head-front", "head-profile-left", "body-3quarter",
    "head-profile-right", "head-3quarter", "body-front",
    "body-side", "body-profile-left", "body-profile-right",
    "body-back", "head-back",
    # generic fallbacks for unknown naming conventions:
    "front", "profile", "side", "3quarter", "body", "head",
)


def _resolve_folder(character_id: str, characters_root: Path) -> Path | None:
    """Map a character_id (e.g. 'sean') to its Bible folder (e.g. 'sean-anchor/')
    by reading each <folder>/character.yaml's character_id field. Returns None if
    no Bible declares this character_id."""
    if not characters_root.is_dir():
        raise ReferenceSelectionError(f"characters_root is not a directory: {characters_root}")
    # Fast path: a folder literally named character_id whose yaml confirms it.
    direct = characters_root / character_id
    if (direct / "character.yaml").exists():
        return direct
    for child in sorted(characters_root.iterdir()):
        cy = child / "character.yaml"
        if not cy.exists():
            continue
        try:
            data = yaml.safe_load(cy.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            continue
        if data.get("character_id") == character_id:
            return child
    return None


def _select_turnarounds(folder: Path, cap: int) -> list[Path]:
    turn_dir = folder / "turnarounds"
    if not turn_dir.is_dir():
        return []
    available = sorted(turn_dir.glob("*.png"))
    picked: list[Path] = []
    used: set[Path] = set()
    for pattern in _TURNAROUND_PREFERENCE:
        if len(picked) >= cap:
            break
        for p in available:
            if p in used:
                continue
            if pattern in p.stem.lower():
                picked.append(p)
                used.add(p)
                break
    return picked[:cap]


def select_references(
    character_id: str,
    checkpoint: str,
    beat: str,
    *,
    characters_root: Path,
    cap: int = 3,
) -> list[Path]:
    """Return the reference bundle (anchor + up to `cap` turnarounds) for one Em
    invocation. v1 ignores checkpoint/beat (approach B). The returned list NEVER
    includes the frame under review — the caller prepends the subject. Missing
    plates are dropped with a log note."""
    if not character_id:
        return []
    folder = _resolve_folder(character_id, Path(characters_root))
    if folder is None:
        log.info("select_references: no Bible folder for character_id=%r under %s",
                 character_id, characters_root)
        return []
    bundle: list[Path] = []
    anchor = folder / "anchor.png"
    if anchor.exists():
        bundle.append(anchor)
    else:
        log.info("select_references: anchor.png missing for %s; dropping", folder)
    for t in _select_turnarounds(folder, cap):
        if t.exists():
            bundle.append(t)
    return bundle
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `.venv/bin/pytest tests/test_reference_selection.py -v`
Expected: 7 passed (incl. the real-Bible integration test → the exact target bundle).

- [ ] **Step 5: Commit**

```bash
git add pipeline/agents/reference_selection.py tests/test_reference_selection.py
git commit -m "$(cat <<'EOF'
feat(reference_selection): Bible-driven capped reference bundle for Em (approach B)

select_references(character_id, checkpoint, beat) returns anchor.png + up to `cap`
canonical deduped turnarounds (front/3-quarter/profile), resolved FROM the Bible
(folder mapped via character.yaml; turnarounds globbed + ranked for view
diversity), so it generalizes to any character without hardcoded filenames. Same
bundle every frame, eval == prod. The checkpoint/beat params are accepted but
ignored in v1 — the view-aware seam (approach A) slots into this module later with
no eval-contract change. Sean resolves to anchor + head-front + head-profile-left +
body-3quarter; the mascot's all-body crops resolve sensibly too. Missing plates are
dropped with a log note (thin bundle is honest; never crashes).

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 3: Em attaches references (spec §5.1, §5.2)

**Files:**
- Modify: `pipeline/agents/vision_critic.py`
- Test: `tests/test_vision_critic_references.py`

`run()` attaches `[subject, *references]` on both the Gemini and Opus paths (incl. phase-6), and `_build_prompt` gains the explicit image-ordering block. `character_id` arrives as a new optional Em input; absent → no references (graceful, today's behavior).

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_vision_critic_references.py
"""Em attaches Bible reference plates (subject = image 1) and tells the model which
is which. character_id absent → no references (graceful, no regression)."""
from __future__ import annotations

import json
from pathlib import Path

from pipeline.agents import AgentContext
from pipeline.agents.vision_critic import VisionCriticNode


def _make_sean_bible(tmp_path: Path) -> Path:
    root = tmp_path / "characters"
    folder = root / "sean-anchor"
    (folder / "turnarounds").mkdir(parents=True)
    (folder / "character.yaml").write_text("character_id: sean\n", encoding="utf-8")
    (folder / "anchor.png").write_bytes(b"x")
    for n in ["head-front", "head-profile-left", "body-3quarter"]:
        (folder / "turnarounds" / f"{n}.png").write_bytes(b"x")
    return root


def _ctx(tmp_path, *, character_id="sean", checkpoint="phase_5_generate", image="subject.png"):
    img = tmp_path / image
    img.write_bytes(b"x")
    chars = _make_sean_bible(tmp_path)
    return AgentContext(
        run_dir=tmp_path,
        inputs={
            "image_path": str(img), "beat_description": "b", "frame_id": "F",
            "impact_tags": [], "checkpoint": checkpoint, "character_id": character_id,
        },
        manifest={"critics": {"t2": {}}, "characters_root": str(chars)},
        criteria=None, tier="draft", cache_dir=tmp_path / ".cache",
    )


def _patch_capture(monkeypatch):
    captured = {}

    async def fake_gemini(*, prompt, image_paths, timeout_s=120):
        captured["paths"] = list(image_paths)
        captured["prompt"] = prompt
        from tests.helpers_vision import _FakeCLI  # see Step 1b
        return _FakeCLI(json.dumps({"verdict": "pass", "confidence": 0.95, "cites_criteria": []}))

    monkeypatch.setattr("pipeline.agents.vision_critic.run_antigravity_with_image", fake_gemini)
    return captured


def test_run_attaches_references_subject_first(monkeypatch, tmp_path):
    captured = _patch_capture(monkeypatch)
    VisionCriticNode().run(_ctx(tmp_path))
    paths = captured["paths"]
    assert Path(paths[0]).name == "subject.png"            # subject is image 1
    assert [Path(p).name for p in paths[1:]] == [
        "anchor.png", "head-front.png", "head-profile-left.png", "body-3quarter.png",
    ]


def test_references_attach_on_phase6_still(monkeypatch, tmp_path):
    # A .png at phase_6_motion → no contact sheet build; references still attach.
    captured = _patch_capture(monkeypatch)
    VisionCriticNode().run(_ctx(tmp_path, checkpoint="phase_6_motion"))
    assert len(captured["paths"]) == 5  # subject + anchor + 3


def test_no_references_when_character_id_absent(monkeypatch, tmp_path):
    captured = _patch_capture(monkeypatch)
    ctx = _ctx(tmp_path)
    ctx.inputs["character_id"] = None
    VisionCriticNode().run(ctx)
    assert len(captured["paths"]) == 1  # subject only


def test_prompt_has_ordering_block_when_references(monkeypatch, tmp_path):
    captured = _patch_capture(monkeypatch)
    VisionCriticNode().run(_ctx(tmp_path))
    low = captured["prompt"].lower()
    assert "image 1 is the frame under review" in low
    assert "reference plate" in low


def test_build_prompt_no_ordering_block_when_zero_refs():
    node = VisionCriticNode()
    ctx = AgentContext(
        run_dir=Path("/tmp/x"),
        inputs={"image_path": "/tmp/x.png", "beat_description": "b", "frame_id": "F",
                "impact_tags": [], "checkpoint": "phase_5_generate"},
        manifest={"critics": {"t2": {}}}, criteria=None, tier="draft",
        cache_dir=Path("/tmp/x/.cache"),
    )
    assert "reference plate" not in node._build_prompt(ctx, {}, n_references=0).lower()
```

- [ ] **Step 1b: Add the shared fake response helper**

```python
# tests/helpers_vision.py
"""Shared fake CLI/SDK response for vision_critic tests."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class _FakeCLI:
    text: str
    duration_s: float = 1.0
    exit_code: int = 0
    rate_capped: bool = False
    stub_fallback: bool = False
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.exit_code == 0 and not self.rate_capped and self.error is None
```

- [ ] **Step 2: Run to verify failure**

Run: `.venv/bin/pytest tests/test_vision_critic_references.py -v`
Expected: FAIL — `_build_prompt()` takes no `n_references` kwarg / references not attached.

- [ ] **Step 3: Implement — module constants + helpers**

In `pipeline/agents/vision_critic.py`, **add to the imports**:

```python
from pipeline.agents.reference_selection import select_references, ReferenceSelectionError
```

**Add module constants** (after `_DEFAULT_TIMEOUT_S`):

```python
# Repo-root-relative characters dir (robust to cwd; works in a worktree too).
_CHARACTERS_ROOT = Path(__file__).resolve().parents[2] / "characters"

# checkpoint -> pipeline phase number, for criteria phase-filtering (Task 4).
_CHECKPOINT_PHASE = {
    "phase_5_generate": 5,
    "phase_6_motion": 6,
    "phase_8_assemble": 8,
}
```

**Add helper methods** to `VisionCriticNode` (anywhere in the `# ---------- internals ----------` block):

```python
    def _characters_root(self, ctx: AgentContext) -> Path:
        override = ctx.manifest.get("characters_root")
        return Path(override) if override else _CHARACTERS_ROOT

    def _resolve_references(self, ctx: AgentContext) -> list[Path]:
        """The Bible reference bundle for this frame. Empty when no character_id is
        declared (graceful — today's reference-blind behavior, no wrong-character
        references)."""
        character_id = ctx.inputs.get("character_id")
        if not character_id:
            return []
        try:
            return select_references(
                str(character_id),
                str(ctx.inputs.get("checkpoint", "")),
                str(ctx.inputs.get("beat_description", "")),
                characters_root=self._characters_root(ctx),
            )
        except ReferenceSelectionError:
            return []
```

- [ ] **Step 4: Implement — wire references into `run()`**

In `run()`, **replace** the line `prompt = self._build_prompt(ctx, t2_cfg)` with:

```python
        references = self._resolve_references(ctx)
        prompt = self._build_prompt(ctx, t2_cfg, n_references=len(references))
```

After the `if is_video:` block (after `model_image_path = temp_contact_sheet_path`), **add**:

```python
        image_paths = [model_image_path, *references]
```

**Replace** the Gemini call's `image_paths=[model_image_path]` with `image_paths=image_paths`, and the Opus call's `image_paths=[model_image_path]` with `image_paths=image_paths`. (Both inside the `try:` block.)

> Note: `run_antigravity_with_image` may now raise `RateCapExhausted` (Task 1). `run()` must let it propagate — do NOT add a catch. The existing `finally:` only unlinks the temp contact sheet and will run correctly as the exception propagates.

- [ ] **Step 5: Implement — the ordering block in `_build_prompt`**

Change the `_build_prompt` signature from `def _build_prompt(self, ctx: AgentContext, t2_cfg: dict) -> str:` to:

```python
    def _build_prompt(self, ctx: AgentContext, t2_cfg: dict, n_references: int = 0) -> str:
```

Immediately **before** the `if checkpoint == "phase_6_motion":` block, **insert**:

```python
        # Reference plates: tell Em which image is the subject vs the references.
        # This is the licence-to-pass she lacks reference-blind — and a sycophancy
        # surface, so the wording stays deliberately conservative; the false_pass
        # guard in the re-baseline is its empirical check (spec §5.2, §9).
        if n_references > 0:
            sections.append(
                "## Reference plates (identity/style ground truth)\n\n"
                "Image 1 is the FRAME UNDER REVIEW. Every image after it is an "
                "identity/style REFERENCE PLATE from this character's Bible — the "
                "canonical truth for who the character is (anchor + turnaround "
                "views). Compare the subject (image 1) against them. A feature that "
                "MATCHES the references is correct even if it differs from a generic "
                "expectation — do NOT flag a difference the references confirm is "
                "correct. A feature that DRIFTS from the references is exactly the "
                "identity/style defect you exist to catch. Judge the subject against "
                "its own Bible, not against a generic ideal."
            )
```

- [ ] **Step 6: Run the tests to verify they pass**

Run: `.venv/bin/pytest tests/test_vision_critic_references.py tests/test_vision_critic_motion_clause.py -v`
Expected: all pass (references attach subject-first; phase-6 still carries the motion clause AND now references; ordering block present/absent correctly).

- [ ] **Step 7: Full suite + commit**

Run: `.venv/bin/python -m pytest tests/ -q 2>&1 | tail -3` → green.

```bash
git add pipeline/agents/vision_critic.py tests/test_vision_critic_references.py tests/helpers_vision.py
git commit -m "$(cat <<'EOF'
feat(vision_critic): attach Bible references to Em (subject = image 1, both paths)

run() now prepends the subject frame to select_references()'s bundle and passes
[subject, *references] to both the Gemini default and Opus escalation paths
(including phase-6 contact sheets — identity-across-the-strip benefits). The
_build_prompt ordering block tells Em image 1 is the subject and the rest are her
Bible's canonical references — the licence-to-pass she lacked reference-blind.
character_id absent → no references (graceful, no regression). RateCapExhausted
from the agy wrapper propagates (an errored gap, never a silent borderline).

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 4: Em surfaces the Bible criteria (spec §5.3)

**Files:**
- Modify: `pipeline/agents/vision_critic.py`
- Test: `tests/test_vision_critic_criteria.py`

Em reads `ctx.criteria` (never read today) and surfaces `query_by_character(character_id) ∩ query_by_phase(phase)` as a terse labeled block — "cite these by ID." Graceful when `ctx.criteria is None` (legacy) or the intersection is empty (designed).

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_vision_critic_criteria.py
"""Em surfaces the character's IR.*/AC.* rules from ctx.criteria so she can cite
them. Graceful when the bundle is None (legacy) or the phase intersection is empty."""
from __future__ import annotations

import json
from pathlib import Path

from pipeline.agents import AgentContext
from pipeline.agents.vision_critic import VisionCriticNode
from pipeline.criteria import load_criteria


def _bundle(tmp_path: Path, cites_phase: list[int]):
    """Write + load a minimal v1.2 bundle with two IR.sean.* rules."""
    data = {
        "version": "1.2", "locked": False,
        "criteria": [
            {"id": "IR.sean.face.jaw-line-angular-not-rounded",
             "description": "Jaw carries a defined angle at the mandibular corner.",
             "cites_phase": cites_phase, "cites_personas": ["em"],
             "impact_tag": "identity_critical", "character_id": "sean"},
            {"id": "IR.sean.prop.stylus-right-hand-always",
             "description": "Stylus stays in the right hand in every frame.",
             "cites_phase": cites_phase, "cites_personas": ["em"],
             "impact_tag": "identity_critical", "character_id": "sean"},
        ],
    }
    p = tmp_path / "ac.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    return load_criteria(p)


def _ctx(criteria, *, checkpoint="phase_5_generate", character_id="sean"):
    return AgentContext(
        run_dir=Path("/tmp/x"),
        inputs={"image_path": "/tmp/x.png", "beat_description": "b", "frame_id": "F",
                "impact_tags": [], "checkpoint": checkpoint, "character_id": character_id},
        manifest={"critics": {"t2": {}}}, criteria=criteria, tier="draft",
        cache_dir=Path("/tmp/x/.cache"),
    )


def test_surfaces_phase5_ir_rules(tmp_path):
    prompt = VisionCriticNode()._build_prompt(_ctx(_bundle(tmp_path, [5, 6])), {})
    assert "Character Bible rules" in prompt
    assert "IR.sean.face.jaw-line-angular-not-rounded" in prompt
    assert "IR.sean.prop.stylus-right-hand-always" in prompt


def test_no_block_when_bundle_none():
    prompt = VisionCriticNode()._build_prompt(_ctx(None), {})
    assert "Character Bible rules" not in prompt


def test_no_block_when_character_id_absent(tmp_path):
    ctx = _ctx(_bundle(tmp_path, [5, 6]))
    ctx.inputs["character_id"] = None
    assert "Character Bible rules" not in VisionCriticNode()._build_prompt(ctx, {})


def test_empty_intersection_no_block(tmp_path):
    # Rules cite only phase 6; checkpoint phase_8_assemble → empty intersection → no block.
    ctx = _ctx(_bundle(tmp_path, [6]), checkpoint="phase_8_assemble")
    assert "Character Bible rules" not in VisionCriticNode()._build_prompt(ctx, {})
```

- [ ] **Step 2: Run to verify failure**

Run: `.venv/bin/pytest tests/test_vision_critic_criteria.py -v`
Expected: FAIL — no "Character Bible rules" block emitted yet.

- [ ] **Step 3: Implement — the criteria block helper**

In `pipeline/agents/vision_critic.py`, **add** to `VisionCriticNode`'s internals:

```python
    def _criteria_block(self, ctx: AgentContext) -> str | None:
        """Surface query_by_character ∩ query_by_phase from the merged CriteriaBundle
        as a terse 'cite these by ID' block. None when no bundle / no character_id /
        empty intersection (all designed — Em falls back to standing context)."""
        bundle = ctx.criteria
        character_id = ctx.inputs.get("character_id")
        if bundle is None or not character_id:
            return None
        char_rules = bundle.query_by_character(str(character_id))
        if not char_rules:
            return None
        phase = _CHECKPOINT_PHASE.get(str(ctx.inputs.get("checkpoint", "")))
        if phase is not None:
            phase_ids = {c.id for c in bundle.query_by_phase(phase)}
            rules = [c for c in char_rules if c.id in phase_ids]
        else:
            rules = char_rules
        if not rules:
            return None
        lines = [
            "## Character Bible rules (cite these by ID)",
            "",
            "These are the locked identity/style rules for this character at this "
            "checkpoint. When you flag drift, CITE the rule IDs you observe drift on "
            "in `cites_criteria` (e.g. \"IR.sean.face.jaw-line-angular-not-rounded\"). "
            "Cite only what you actually see drift on; a rule the references confirm "
            "is honored is not a citation.",
            "",
        ]
        for c in rules:
            lines.append(f"- `{c.id}` ({c.impact_tag}): {c.description}")
        return "\n".join(lines)
```

- [ ] **Step 4: Implement — append the block in `_build_prompt`**

Immediately **after** the references-ordering block you added in Task 3 (and before the `phase_6_motion` block), **insert**:

```python
        # Bible criteria (IR.*/AC.*) for this character at this checkpoint's phase —
        # the criteria half of "give Em the Bible" (spec §5.3). What flips case-7 green.
        criteria_block = self._criteria_block(ctx)
        if criteria_block:
            sections.append(criteria_block)
```

- [ ] **Step 5: Run the tests to verify they pass**

Run: `.venv/bin/pytest tests/test_vision_critic_criteria.py -v`
Expected: 4 passed.

- [ ] **Step 6: Full suite + commit**

Run: `.venv/bin/python -m pytest tests/ -q 2>&1 | tail -3` → green.

```bash
git add pipeline/agents/vision_critic.py tests/test_vision_critic_criteria.py
git commit -m "$(cat <<'EOF'
feat(vision_critic): surface the character's IR/AC rules so Em cites the Bible

Em now reads ctx.criteria (the merged CriteriaBundle she ignored) and surfaces
query_by_character ∩ query_by_phase as a terse 'cite these by ID' block — the
Databricks Grading-Notes pattern, and the criteria half of giving Em the Bible.
Graceful when the bundle is None (pencil-test legacy runs) or the phase
intersection is empty (designed: Em falls back to standing context). This is the
diff that flips the case-7 xfail green.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 5: Flip case-7 green (spec §8) + `IR.sean.*` cleanup

**Files:**
- Modify: `evals/character_designer/cases.yaml`
- Modify: `evals/character_designer/runner.py`

Two legitimate fixes + an honest mock. (1) Validity: the test's `em_ctx` used `candidate_path`/`frame_num`/`manifest_style_block` → Em reads `image_path`/`frame_id`/`checkpoint`, so it threw `KeyError` before judging. (2) ID alignment: the mock + assertion used `IR.sean-anchor.*` → canonical is `IR.sean.*`. (3) The stub fallback cites a hardcoded `AC01`, so it can never cite an IR rule — replace it with a **prompt-reading mock** that cites whatever `IR.sean.*` rule the criteria-surfacing actually put in Em's prompt. If the fix surfaced the rules → green; if not → no IR id in the prompt → empty cites on a `fail` verdict → invariant raises → red. This makes the case a true test of the fix.

- [ ] **Step 1: Run case-7 to confirm its current (xfail) state**

Run: `.venv/bin/pytest evals/character_designer/runner.py -v -k closing-the-loop`
Expected: `xfailed` (currently red — today via `KeyError`).

- [ ] **Step 2: Fix the case's character_id in `cases.yaml`**

In `evals/character_designer/cases.yaml`, in the `closing-the-loop-em-cites-cy-rules` case, change `character_id: sean-anchor` → `character_id: sean` (both the case-level `character_id:` field and the `opus` `mocked_responses` `character_id: sean-anchor` → `character_id: sean`).

- [ ] **Step 3: Rewrite the Em invocation in `_run_closing_the_loop_case`**

In `evals/character_designer/runner.py`, in `_run_closing_the_loop_case`, **replace the `em_ctx` construction + the Em run + the assertion** (the block from `broken_frame = ...` through the final `assert len(ir_citations) >= 1, (...)`) with:

```python
    import json as _json
    import re as _re

    broken_frame = fixtures_dir / "deliberately-broken-phase-5-frame.png"
    assert broken_frame.exists(), "deliberately-broken-phase-5-frame.png fixture missing"

    # Simulate a real reference+criteria-loaded critic: cite the first IR.sean.* rule
    # that Em's prompt actually SURFACED. If the criteria half of the fix is present,
    # the prompt carries the rule and the mock cites it (green). If it is absent, no
    # IR id is in the prompt, cites is empty on a `fail` verdict, and Em's
    # cites_criteria invariant RAISES — keeping the case honestly red. The mock can
    # only cite what was genuinely put in front of Em; it cannot fabricate grounding.
    def _fake_gemini_cites_surfaced_ir(*, prompt, image_paths, timeout_s=120):
        m = _re.search(r"IR\.sean\.[A-Za-z0-9.\-]+", prompt)
        cited = [m.group(0)] if m else []
        return _FakeCLIResponse(text=_json.dumps({
            "verdict": "fail", "confidence": 0.9,
            "reasoning": "Broken frame: proportion + stylus drift vs the Bible references.",
            "proposed_patches": [], "cites_criteria": cited,
        }))

    async def _fake_gemini(*, prompt, image_paths, timeout_s=120):
        return _fake_gemini_cites_surfaced_ir(prompt=prompt, image_paths=image_paths)

    monkeypatch.setattr(
        "pipeline.agents.vision_critic.run_antigravity_with_image", _fake_gemini,
    )

    em_ctx = AgentContext(
        run_dir=tmp_path / "runs" / case["name"],
        inputs={
            "image_path": str(broken_frame),
            "beat_description": "Sean glances down at the stylus; pencil-test register.",
            "frame_id": "F06",
            "impact_tags": ["identity_critical"],
            "checkpoint": "phase_5_generate",
            "character_id": "sean",
        },
        manifest={
            "critics": {"t2": {}},
            "criteria_sources": {"bibles": [str(criteria_path)]},
        },
        criteria=merged_bundle,
        tier="draft",
        cache_dir=tmp_path / "runs" / case["name"] / ".cache",
        extras={},
    )

    em_result = VisionCriticNode().run(em_ctx)
    ir_citations = [c for c in em_result.cites_criteria if c.startswith("IR.sean.")]
    assert len(ir_citations) >= 1, (
        f"{case['name']}: Em did not cite any IR.sean.* rule. "
        f"All citations: {em_result.cites_criteria}. The criteria half of the "
        f"reference-images fix should surface the Bible's IR rules into Em's prompt "
        f"so she can ground a verdict; the diff that flips this green is the museum "
        f"content (the moment Bible authoring became contract-grounded)."
    )
```

> `merged_bundle`, `criteria_path`, `_FakeCLIResponse`, `AgentContext`, and `VisionCriticNode` are already in scope earlier in `_run_closing_the_loop_case`. Confirm `_FakeCLIResponse` is imported at the top of `runner.py`; if not, add `from evals.character_designer.conftest import _FakeCLIResponse` (it is already used elsewhere in the file).

- [ ] **Step 4: Remove the `is_intentionally_red` flag for this case**

In `cases.yaml`, in the `closing-the-loop-em-cites-cy-rules` case's `expected:` block, change `is_intentionally_red: true` → `is_intentionally_red: false` (it should now pass, not xfail). Update the adjacent comment to note the fix landed (the prompt now carries the IR rules).

- [ ] **Step 5: Run case-7 to verify it flips green**

Run: `.venv/bin/pytest evals/character_designer/runner.py -v -k closing-the-loop`
Expected: `1 passed` (was `xfailed`).

- [ ] **Step 6: `IR.sean.*` cleanup in the schema-cross-register test**

In `evals/character_designer/runner.py`, in `_run_schema_cross_register_case`, change the two hardcoded `IR.sean-anchor.*` rule IDs (`IR.sean-anchor.hair.center-cowlick`, `IR.sean-anchor.prop.stylus-right-hand`) and their `character_id` fields from `sean-anchor` → `sean`, and the assertion `r.id.startswith("IR.sean-anchor.")` → `r.id.startswith("IR.sean.")`. (Arbitrary mock data; aligning it to the canonical id removes the last non-canonical `IR.sean-anchor.*` from the codebase.)

- [ ] **Step 7: Run the full character_designer suite**

Run: `.venv/bin/pytest evals/character_designer/runner.py -v 2>&1 | tail -5`
Expected: the previously-`xfailed` closing-the-loop case now `passed`; the rest unchanged (1 xpassed `under-specified` still tracking). Net: one more `passed`, one fewer `xfailed`.

- [ ] **Step 8: Confirm no stray `IR.sean-anchor.` remains**

Run: `git grep -n "IR\.sean-anchor\." -- . ':!.venv'`
Expected: only matches in `README.md` / `failure-modes.md` / `last-run.md` prose (narrative references). Update those prose mentions to `IR.sean.*` if they assert the citation namespace (they describe the case; keep them accurate). No code/assertion should match.

- [ ] **Step 9: Commit**

```bash
git add evals/character_designer/cases.yaml evals/character_designer/runner.py \
        evals/character_designer/README.md evals/character_designer/failure-modes.md \
        evals/character_designer/last-run.md
git commit -m "$(cat <<'EOF'
test(case-7): flip closing-the-loop xfail green — Em cites Cy's IR rules

Three fixes make case-7 a true test of the reference-images change: (1) validity —
the em_ctx used candidate_path/frame_num/manifest_style_block; Em reads
image_path/frame_id/checkpoint, so it threw KeyError before judging; (2) ID
alignment — the mock + assertion used IR.sean-anchor.*; canonical is IR.sean.*
(the real Bible's namespace); (3) honesty — the stub cites a hardcoded AC01 and
could never cite an IR rule, so it's replaced with a prompt-reading mock that
cites the first IR.sean.* rule Em's prompt actually SURFACED. Green only when the
criteria-surfacing fix put the rules in front of Em; absent the fix, empty cites
on a fail verdict trips Em's invariant and the case stays red. This xfail->green
diff is the museum content: the moment Bible authoring became contract-grounded.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 6: Eval re-wire for structural parity (spec §7)

**Files:**
- Modify: `evals/vision_critic/cases.yaml`
- Modify: `evals/vision_critic/conftest.py`
- Modify: `evals/vision_critic/runner.py`
- Modify: `evals/vision_critic/score.py`

The harness and production call the **same** `select_references` (parity is structural). `cases.yaml` gains `character_id`; the harness loads the merged `CriteriaBundle` and threads `character_id` + `characters_root`. The mocked `runner.py` proves the new plumbing doesn't crash (real reference plates attach; the stub verdict ignores them). The red motion cases stay red.

- [ ] **Step 1: Add `character_id: sean` to every case in `cases.yaml`**

Run (adds the field to each case, idempotently, right after each `name:` line):
```bash
.venv/bin/python - <<'PY'
import re, pathlib
p = pathlib.Path("evals/vision_critic/cases.yaml")
text = p.read_text(encoding="utf-8")
# Insert "    character_id: sean" after each "  - name: ..." line that lacks it.
out, lines = [], text.splitlines()
for i, line in enumerate(lines):
    out.append(line)
    if re.match(r"^  - name: ", line):
        # peek ahead a few lines for an existing character_id under this case
        window = lines[i+1:i+12]
        if not any(re.match(r"^    character_id:", w) for w in window):
            out.append("    character_id: sean")
p.write_text("\n".join(out) + "\n", encoding="utf-8")
print("character_id added to", sum(1 for l in out if l.strip()=="character_id: sean"), "cases")
PY
```
Expected: `character_id added to 29 cases`. Spot-check with `git diff evals/vision_critic/cases.yaml | head -30`. Also update the schema-comment header in `cases.yaml` to document the new `character_id` field (add a line near the per-case schema comment: `#   character_id: which character the frame contains (drives select_references + criteria; default sean)`).

- [ ] **Step 2: Add the manifest + criteria helpers to `conftest.py`**

Append to `evals/vision_critic/conftest.py`:

```python
REPO_ROOT = Path(__file__).resolve().parents[2]


def eval_manifest() -> dict:
    """The real critics.t2 + criteria_sources + characters_root, so Em runs in the
    eval exactly as she ships (the parity guarantee — same select_references + same
    merged bundle as production)."""
    full = yaml.safe_load((REPO_ROOT / "manifest.yaml").read_text(encoding="utf-8"))
    return {
        "critics": full.get("critics", {}),
        "criteria_sources": full.get("criteria_sources", {}),
        "characters_root": str(REPO_ROOT / "characters"),
    }


def merged_criteria(manifest: dict):
    """Load + merge the Bibles' IR.* graphs into one CriteriaBundle."""
    from pipeline.criteria import load_all_criteria
    return load_all_criteria(manifest)
```

- [ ] **Step 3: Thread `character_id` + criteria through `runner.py`'s `_ctx_for_case`**

In `evals/vision_critic/runner.py` PART 2, **add** module-level loads (after `_FIXTURES = ...`):

```python
from evals.vision_critic.conftest import eval_manifest, merged_criteria

_EVAL_MANIFEST = eval_manifest()
_MERGED_CRITERIA = merged_criteria(_EVAL_MANIFEST)
```

**Replace** `_ctx_for_case` with:

```python
def _ctx_for_case(case: dict) -> AgentContext:
    return AgentContext(
        run_dir=Path("/tmp/em-eval"),
        inputs={
            "image_path": str(_FIXTURES / case["input"]),
            "beat_description": case["beat_description"],
            "frame_id": case["name"],
            "impact_tags": case.get("impact_tags", []),
            "checkpoint": case["checkpoint"],
            "character_id": case.get("character_id", "sean"),
        },
        manifest=_EVAL_MANIFEST,
        criteria=_MERGED_CRITERIA,
        tier="draft",
        cache_dir=Path("/tmp/em-eval/.cache"),
    )
```

- [ ] **Step 4: Run the mocked harness to verify it still scores every case**

Run: `.venv/bin/pytest evals/vision_critic/runner.py -v 2>&1 | tail -8`
Expected: scoring unit tests pass; the parametrized harness passes for non-red cases and `xfail`s the 6 motion-proper cases; `test_segment_report_well_formed` passes. The mocked runner now attaches real reference plates + surfaces criteria (proving the plumbing) while the stub verdict still drives scoring. If a case errors on a missing fixture path, that is a fixture issue — fix the path, do not weaken the harness.

- [ ] **Step 5: Thread `character_id` + criteria through `score.py`**

In `evals/vision_critic/score.py`, **replace** `_ctx` with:

```python
def _ctx(case: dict, manifest: dict, criteria) -> AgentContext:
    return AgentContext(
        run_dir=Path("/tmp/em-baseline"),
        inputs={
            "image_path": str(FIXTURES / case["input"]),
            "beat_description": case["beat_description"],
            "frame_id": case["name"],
            "impact_tags": case.get("impact_tags", []),
            "checkpoint": case["checkpoint"],
            "character_id": case.get("character_id", "sean"),
        },
        manifest=manifest,
        criteria=criteria,
        tier="draft",
        cache_dir=Path("/tmp/em-baseline/.cache"),
    )
```

**Update** `_manifest()` to include `characters_root`, and `_score_one` + `main` to build and pass the merged bundle. In `_manifest()`, add to the returned dict: `"characters_root": str(root / "characters")`. **Replace** `_score_one`'s signature/body head:

Add to score.py's top-of-file imports:
```python
from pipeline.agents.reference_selection import select_references
from evals.vision_critic.conftest import merged_criteria
```

Replace `_score_one`:
```python
def _score_one(case: dict, manifest: dict, criteria) -> CaseScore:
    """Run production Em (Gemini default + Opus escalation) against one case."""
    start = datetime.now(timezone.utc)
    result = VisionCriticNode().run(_ctx(case, manifest, criteria))
    wall = (datetime.now(timezone.utc) - start).total_seconds()
    refs = select_references(
        case.get("character_id", "sean"), case["checkpoint"], case["beat_description"],
        characters_root=Path(manifest["characters_root"]),
    )
    return CaseScore(
        name=case["name"],
        case_class=case["case_class"],
        expected_verdict=case["expected_verdict"],
        predicted_verdict=result.outputs["verdict"],
        expected_cites=case.get("expected_cites", []),
        actual_cites=result.cites_criteria,
        confidence=result.outputs["confidence"],
        wall_s=wall,
        # `refs` (resolved reference plate names) is logged per-case for trace
        # transparency — see the print() in main()'s loop below.
    )
```

In `main()`, after `manifest = _manifest()`, **add** `criteria = merged_criteria(manifest)` (built once, reused by both the live and `--stub` branches so the stub still exercises the criteria path). Update the per-case loop call `cs = _score_one(c, manifest)` → `cs = _score_one(c, manifest, criteria)`. In the loop's per-case `print(...)` progress line, append the resolved reference names so the trace records what Em saw, e.g.:
```python
            refs = select_references(c.get("character_id", "sean"), c["checkpoint"],
                                     c["beat_description"], characters_root=Path(manifest["characters_root"]))
            print(f"[{i}/{len(CASES)}] {c['name']}: {cs.predicted_verdict} "
                  f"(conf={cs.confidence:.2f}, {cs.wall_s:.0f}s) refs=[{', '.join(p.name for p in refs) or 'none'}]",
                  flush=True)
```

- [ ] **Step 6: Smoke-test `score.py --stub` (credential-free, no cost)**

Run: `.venv/bin/python -m evals.vision_critic.score --stub 2>&1 | tail -20`
Expected: runs all 29 cases under the forced stub, writes a `last-run.md` labeled STUB (degenerate matrix), no errors, no live calls. This proves the new criteria/reference plumbing runs end-to-end credential-free. **Discard** the STUB `last-run.md` (don't commit it — the real one lands in Task 7): `git checkout evals/vision_critic/last-run.md` (or leave uncommitted).

- [ ] **Step 7: Commit**

```bash
git add evals/vision_critic/cases.yaml evals/vision_critic/conftest.py \
        evals/vision_critic/runner.py evals/vision_critic/score.py
git commit -m "$(cat <<'EOF'
eval(em): re-wire for structural parity — character_id + shared select_references

cases.yaml gains character_id (not a hand-authored reference list — that would
reintroduce the eval-prod gap approach B was chosen to avoid). The harness and
score.py both load the merged CriteriaBundle and thread character_id +
characters_root, so the eval and production call the SAME select_references — one
code path, parity is structural not maintained-by-hand. The mocked runner now
attaches real reference plates + surfaces criteria (proving the plumbing); the 6
motion-proper cases stay red. score.py logs the resolved reference list per case
for trace transparency. Verified credential-free via score.py --stub.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 7: Live re-baseline — the measurement (spec §9) — STOP GATE

**Files:**
- Run: `evals/vision_critic/score.py` (live)
- Commit: `evals/vision_critic/last-run.md` + `evals/vision_critic/traces/baseline-2026-06-01-scored.md` (after the gate)

This is the portfolio artifact. Run Em live with references + criteria, compare against the locked reference-blind baseline. **The false-pass guard is the headline, not precision** (spec §9): a precision lift that costs any false pass is a worse Em. Labels stay locked; any that would flip is presented to Sean and re-ratified before lock.

- [ ] **Step 1: Pre-flight — confirm live deps + quota awareness**

Run:
```bash
which agy && .venv/bin/python -c "import claude_agent_sdk; print('sdk ok')"
.venv/bin/python -c "from dotenv import load_dotenv; load_dotenv('.env'); import os; print('GEMINI key present:', bool(os.getenv('GEMINI_API_KEY')))"
```
Expected: `agy` path, `sdk ok`, `GEMINI key present: True`. Note: consumer-tier Gemini quota — if exhausted, the now-fixed `RateCapExhausted` makes affected cases **honest errored gaps** (excluded from the matrix), not fabricated borderlines.

- [ ] **Step 2: Run the live scorer in the BACKGROUND (~24 min)**

Run (background — do NOT block the session):
```bash
cd /Users/seanwinslow/Code-Brain/anima/.claude/worktrees/feature+em-reference-images
.venv/bin/python -m evals.vision_critic.score > /tmp/em-rebaseline.log 2>&1 &
echo "started; tail -f /tmp/em-rebaseline.log to watch per-case progress"
```
Poll progress periodically: `tail -5 /tmp/em-rebaseline.log`. Per-case lines print as it goes (`[i/29] name: verdict (conf, Ns)`). Expect ~25–80s/case. Errored cases (e.g. a `RateCapExhausted`) are recorded honestly and excluded — they do not abort the run.

- [ ] **Step 3: When complete, read the new matrix**

Run: `cat evals/vision_critic/last-run.md`
Read the **performs** segment confusion matrix. Compute the deltas vs the locked baseline (precision 0.62 / recall 1.00 / false_pass 0.00 / cites-correct 0.43 performs; 0.33 overall) — each with `stderr`.

- [ ] **Step 4: STOP GATE — present to Sean + the false-pass guard**

Present to Sean, framed by the §9 disciplines:
- **The false-pass guard first:** did `false_pass_rate` stay 0.00 and recall hold? **Any** false pass on the performs segment = a worse Em = the change is blocked (and promotes follow-on #3, the DINOv2 backstop, from deferred to next — spec §14). Name any case that slipped to a false pass.
- **The precision lift, with `stderr`:** did the 8 false alarms resolve? Is the lift outside the noise band (~23 cases)?
- **`cites-correct`, with `stderr`:** did surfacing criteria move it (the clean proof the criteria-half worked)?
- **Any label that would flip:** present it for re-ratification. The number moves; the label does not, unless Sean confirms a genuine validity error. **Do not edit any label without Sean's explicit sign-off.**

Wait for Sean's decision before committing. If the false-pass guard fails, STOP — the regression is the finding; do not paper over it.

- [ ] **Step 5: Commit the re-baseline (after the gate passes)**

```bash
git add evals/vision_critic/last-run.md evals/vision_critic/traces/baseline-2026-06-01-scored.md
git commit -m "$(cat <<'EOF'
eval(em): reference-grounded re-baseline — precision lift, false-pass held at 0.00

Em re-scored live WITH references + criteria attached, against the locked af7950d
labels (re-ratified unchanged by Sean; the number moves, the labels don't). Headline
is false-pass-first: false_pass_rate held at 0.00 / recall held, AND precision rose
from 0.62 as the reference-blind false alarms resolved; cites-correct rose from 0.43
as Em grounded verdicts in the surfaced IR rules. Each delta reported with stderr.
This pre/post delta is the portfolio artifact — the moment Em stopped grading blind.
[Fill exact numbers from last-run.md before committing.]

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
EOF
)"
```
> Replace the bracketed line with the actual numbers from `last-run.md` before committing.

---

## Task 8: Re-run the three-way bake-off (spec §9) — STOP GATE

**Files:**
- Run: `evals/bakeoffs/2026-05-31-t2-vision-critic-gemini-vs-sonnet-vs-opus/bakeoff.py` (live)
- Modify: `evals/bakeoffs/2026-05-31-t2-vision-critic-gemini-vs-sonnet-vs-opus/results.md`

All three models were equally reference-blind before and Gemini's column was quota-invalid, so the T2 model decision can only be licensed now (references attached + rate-cap fixed). Judge on the **false-pass-first** lens (last round, Sonnet ≥ Opus because Opus's "sharpness" came from a false pass).

- [ ] **Step 1: Run the bake-off live in the BACKGROUND**

Run:
```bash
.venv/bin/python evals/bakeoffs/2026-05-31-t2-vision-critic-gemini-vs-sonnet-vs-opus/bakeoff.py \
  > /tmp/em-bakeoff.log 2>&1 &
echo "bake-off started; tail -f /tmp/em-bakeoff.log"
```
Poll with `tail -5 /tmp/em-bakeoff.log`. If Gemini quota is exhausted, the `RateCapExhausted` fix surfaces that column as honest errored cases (not fabricated borderlines) — note it; the Sonnet/Opus columns remain valid.

- [ ] **Step 2: Record exact model snapshots (the silent-regression catcher)**

Capture the exact model identifiers each config ran against (Gemini snapshot via agy, Sonnet/Opus SDK model IDs). Run:
```bash
agy --version 2>/dev/null || true
.venv/bin/python -c "import claude_agent_sdk, importlib.metadata as m; print('sdk', m.version('claude-agent-sdk'))" 2>/dev/null || true
```
Record these in `results.md` under a "Model snapshots" heading.

- [ ] **Step 3: STOP GATE — write the Decision (false-pass-first)**

Update `results.md` with the per-config metric table (precision/recall/**false-pass**/cites-correct on the performs segment + wall-time + pinned snapshots) and a Decision section. Judge on the costly-error lens first. Present the decision to Sean before changing any default. **Do not change `manifest.critics.t2.default_model`** unless Sean approves a swap on the evidence (and only if a candidate strictly dominates on false-pass-then-precision with references attached).

- [ ] **Step 4: Commit**

```bash
git add evals/bakeoffs/2026-05-31-t2-vision-critic-gemini-vs-sonnet-vs-opus/results.md \
        evals/bakeoffs/2026-05-31-t2-vision-critic-gemini-vs-sonnet-vs-opus/traces/
git commit -m "$(cat <<'EOF'
eval(bakeoffs): re-run T2 shoot-out with references attached + rate-cap fixed

The prior round was reference-blind across all three models and Gemini's column was
quota-invalid, so it couldn't license a model decision. Re-run with references +
criteria attached and the RateCapExhausted fix in place; pinned model snapshots
recorded (the silent-regression catcher). Decision judged false-pass-first.
[Fill the verdict + whether the default changed.]

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
EOF
)"
```
> Replace the bracketed line with the actual verdict. If Gemini is still quota-throttled, note the valid-three-way is a post-reset re-run (a follow-on).

---

## Task 9: Docs (spec §11, §13) + final verification

**Files:**
- Modify: `CHANGELOG.md`, `CLAUDE.md`
- Create: `docs/anima-test-runs/2026-06-01-em-reference-images-field-report.md`

- [ ] **Step 1: CHANGELOG entry**

Prepend a dated entry to `CHANGELOG.md` capturing **what changed and why**: Em is now reference-grounded (capped Bible bundle + criteria), the agy `RateCapExhausted` fix, the case-7 flip, the re-baseline result (the precision lift with false-pass held), the bake-off outcome, and the three named follow-ons (view-aware A, pairwise, DINOv2 backstop). Note the `select_references` seam is forward-compatible for A.

- [ ] **Step 2: Update the CLAUDE.md Em row**

In `CLAUDE.md`, the `vision_critic — Em` Skills-Map row: change the "known reference-blindness gap" language to reflect the fix — Em now judges against the Bible's reference plates + IR/AC criteria via `select_references` + `ctx.criteria`; the baseline was re-run (cite the new precision/false-pass numbers); the reference-blindness FINDING is closed. Keep the row honest about what's deferred (view-aware selection, pairwise, DINOv2 backstop). Add `pipeline/agents/reference_selection.py` to the relevant file list if one exists.

- [ ] **Step 3: Write the field report**

Create `docs/anima-test-runs/2026-06-01-em-reference-images-field-report.md` — the narrative: the finding, the four code seams, the case-7 flip, the re-baseline delta (the artifact), the bake-off outcome, what the false-pass guard showed, and the three follow-ons (with the promotion trigger for DINOv2 if any false pass appeared). Studio voice (per PHILOSOPHY).

- [ ] **Step 4: Final full-suite verification**

Run:
```bash
.venv/bin/python -m pytest tests/ -q 2>&1 | tail -3
.venv/bin/python -m pytest pipeline/tests/ -q 2>&1 | tail -3
.venv/bin/python -m pytest evals/vision_critic/runner.py -q 2>&1 | tail -3
.venv/bin/python -m pytest evals/character_designer/runner.py -q 2>&1 | tail -3
```
Expected: `tests/` green (baseline + new tests for rate-cap (6) + reference_selection (7) + references (5) + criteria (4)); `pipeline/tests/` green; `evals/vision_critic/runner.py` green (motion cases still red/xfail); `evals/character_designer/runner.py` green with case-7 now **passed** (one fewer xfail than the Task 0 baseline). Confirm the final `tests/` count against the Task 0 before-number.

- [ ] **Step 5: Commit**

```bash
git add CHANGELOG.md CLAUDE.md docs/anima-test-runs/2026-06-01-em-reference-images-field-report.md
git commit -m "$(cat <<'EOF'
docs: Em reference-images wrap — CHANGELOG, CLAUDE.md Em row, field report

Records the reference-grounding (capped Bible bundle + criteria via
select_references + ctx.criteria), the agy RateCapExhausted fix, the case-7 flip,
the re-baseline precision lift with false-pass held, the bake-off outcome, and the
three named follow-ons (view-aware selection A, pairwise reframe, DINOv2 identity
backstop). Closes the reference-blindness FINDING.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 6: Offer to finish the branch**

Per `superpowers:finishing-a-development-branch`: present options (open a PR off `feature/em-reference-images`, or hold for the post-quota-reset valid three-way bake-off). Do not merge without Sean's call.

---

## Self-Review (run before handing off)

**1. Spec coverage:**
- §4 select_references → Task 2 ✓
- §5.1/§5.2 references + ordering → Task 3 ✓
- §5.3 criteria surfacing → Task 4 ✓
- §6 RateCapExhausted (empty vs malformed) → Task 1 ✓
- §7 parity re-wire (character_id + shared select_references) → Task 6 ✓
- §8 case-7 (validity + ID + honest mock) → Task 5 ✓
- §9 re-baseline discipline (false-pass-first, stderr, cites-correct, locked labels, bake-off + snapshots) → Tasks 7 + 8 ✓
- §11 three follow-ons logged → Task 9 ✓
- §12 guardrails → Task 0 + header ✓
- §13 DoD → Task 9 Step 4 ✓

**2. Placeholder scan:** the only bracketed `[Fill ...]` are in Task 7/8 commit messages — deliberate (live numbers unknown until the run) with explicit "replace before committing" notes. No TODO/TBD in code steps.

**3. Type/name consistency:** `select_references(character_id, checkpoint, beat, *, characters_root, cap=3)` used identically in Tasks 2, 3, 5, 6. `RateCapExhausted` raised in Task 1, propagated (not caught) in Task 3, surfaced as errored in Tasks 7/8. `_CHECKPOINT_PHASE` defined Task 3, used Task 4. `character_id` threaded consistently (cases.yaml → `_ctx_for_case`/`_ctx` → `run()` → `_resolve_references`/`_criteria_block`). `_FakeCLIResponse` (conftest) vs `_FakeCLI` (helpers_vision) are distinct by design — the eval conftest's vs the unit-test helper's.
