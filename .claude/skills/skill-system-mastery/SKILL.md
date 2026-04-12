---
name: skill-system-mastery
description: Claude Code skill creation and optimization assistant. Guides building effective SKILL.md files with proper YAML frontmatter, progressive disclosure, trigger phrase optimization, and reference file architecture. Use when creating a new skill, improving an existing skill description, debugging why a skill does not auto-load, or structuring a skill directory.
---

# Skill System Mastery

## Purpose

Create, debug, and optimize Claude Code skills that auto-load reliably and deliver domain expertise without wasting context tokens. Follow the progressive disclosure architecture: metadata triggers loading, SKILL.md provides workflow, and references/ holds deep content Claude reads only when needed.

## When to Use

- Creating a new skill from scratch (need the directory structure and SKILL.md template)
- Improving a skill description so it triggers more reliably on user prompts
- Debugging a skill that is not auto-loading when expected
- Deciding whether content belongs inline in SKILL.md or in references/
- Structuring a large skill with scripts, references, and assets
- Reviewing a skill for quality (token efficiency, completeness, section order)

## Examples

**Example 1: Creating a new skill**
```
User: "Create a skill for reviewing database migrations"
Claude: [Uses skill-system-mastery] Creates the directory structure:

db-migration-review/
  SKILL.md
  references/
    common-antipatterns.md

Generates SKILL.md with:
- Frontmatter: name + description with trigger phrases ("review migration", "check schema change", "audit SQL")
- Purpose, When to Use, Examples sections
- Domain content: migration review checklist, rollback verification, index analysis
- Success Criteria and Copy/Paste Ready sections
```

**Example 2: Debugging auto-load failure**
```
User: "My deploy-checker skill never fires when I ask about deployments"
Claude: [Uses skill-system-mastery] Checks:
1. Run /skills to verify discovery - is it listed?
2. Inspect YAML frontmatter syntax - missing closing ---?
3. Review description field - does it contain trigger phrases like "deploy", "release", "ship to production"?
4. Check directory name matches name field in frontmatter
Identifies: description says "Validates infrastructure" but lacks deployment trigger words. Rewrites description.
```

**Example 3: Optimizing token usage**
```
User: "My API integration skill is 400 lines and slowing things down"
Claude: [Uses skill-system-mastery] Applies progressive disclosure:
- Moves the 200-line endpoint reference table to references/api-endpoints.md
- Moves authentication flow details to references/auth-patterns.md
- Keeps core workflow (50 lines) and 2 inline examples in SKILL.md
- Adds "when to read" guidance: "For endpoint specifications, see references/api-endpoints.md"
Result: SKILL.md drops from 400 to 120 lines; references load only when needed.
```

## Skill Directory Structure

```
skill-name/
  SKILL.md              # REQUIRED - core logic and metadata
  scripts/              # OPTIONAL - executable code Claude runs via Bash
  references/           # OPTIONAL - docs Claude reads on demand via Read
  assets/               # OPTIONAL - templates/images used in output (not loaded into context)
```

## YAML Frontmatter Specification

Only two fields are required. The description is the single most important line in the entire skill.

```yaml
---
name: kebab-case-name
description: What this does AND when Claude should load it. Embed trigger phrases naturally.
---
```

| Field | Required | Purpose |
|-------|----------|---------|
| `name` | Yes | Kebab-case identifier. Must match the directory name. Doubles as /slash-command. |
| `description` | Yes | The ONLY field Claude reads to decide whether to load. Must include trigger phrases. |

### Writing Effective Descriptions

The description controls auto-loading. Claude reads it before every user turn and decides whether to load the full SKILL.md.

**Pattern**: `[What it does] + [When to use it with trigger phrases]`

Bad:
```yaml
description: Helps with databases.
```

Good:
```yaml
description: PostgreSQL query optimizer and schema reviewer. Use when analyzing slow queries, reviewing table schemas, checking index coverage, or debugging connection pool issues in Supabase or PostgreSQL databases.
```

**Optimization techniques:**
- Include the exact verbs users type: "create", "review", "debug", "fix", "generate"
- Include file extensions if relevant: ".tf", ".prisma", ".sql"
- Include tool/framework names: "Supabase", "Prisma", "Jira"
- Add negative constraints if needed: "Do NOT use for simple text edits"

### Claude Search Optimization (CSO)

**CRITICAL: Description = When to Use, NOT What the Skill Does.**

When a description summarizes the skill's workflow, Claude may follow the description instead of reading the full skill body. This creates a shortcut that bypasses important details.

```yaml
# BAD: Summarizes workflow - Claude takes shortcut
description: Use when executing plans - dispatches subagent per task with code review

# GOOD: Just triggering conditions, no workflow summary
description: Use when executing implementation plans with independent tasks
```

**Keyword coverage:** Include error messages, symptoms, synonyms, and tool names that users search for.

### Token Efficiency Targets

- Frequently-loaded skills: <200 words total
- Standard skills: <500 words
- Use cross-references instead of repeating content from other skills
- Reference `--help` for CLI flags instead of documenting them inline
- One excellent example beats three mediocre ones

## Progressive Disclosure Architecture

Three layers of information loading, each with increasing token cost:

| Level | What Loads | Token Cost | Strategy |
|-------|-----------|-----------|----------|
| 1. Metadata | name + description only | ~50-100 | Dense trigger phrases, no implementation details |
| 2. Instructions | Full SKILL.md body | 1k-5k | Core workflow, decision trees, 2-3 inline examples |
| 3. Resources | references/ and scripts/ | Variable | Loaded only when Claude decides it needs them |

### When to Use references/ vs Inline

- **Inline in SKILL.md**: Content under 50 lines OR critical for every execution
- **references/ file**: Conditional content (e.g., "if using React"), lookup tables over 50 lines, pattern libraries with 3+ code examples, configuration templates

In SKILL.md, always tell Claude when to read each reference:
```markdown
For the complete list of API endpoints, see references/api-endpoints.md.
For authentication flow patterns, see references/auth-patterns.md when the user mentions OAuth or JWT.
```

## Mandatory Section Order

Every SKILL.md must follow this exact order. Do not add or remove sections.

1. YAML frontmatter (name + description)
2. `# Skill Title`
3. `## Purpose` - one paragraph, imperative form
4. `## When to Use` - bullet list of specific trigger situations
5. `## Examples` - 2-3 user/Claude dialog exchanges
6. `## [Domain Content]` - the bulk (60-150 lines), organized by task
7. `## Success Criteria` - testable yes/no checklist
8. `## Copy/Paste Ready` - 3-5 natural language trigger phrases

## TDD for Skills

Apply RED-GREEN-REFACTOR to skill creation to ensure the skill actually changes Claude's behavior:

### 1. RED: Baseline Without Skill
Test what Claude does without the skill loaded. Use a subagent so your main context stays clean:

```
Launch a subagent WITHOUT the skill loaded.
Give it the exact prompt a user would type.
Record Claude's default behavior — this is your baseline.
```

### 2. GREEN: Write the Skill
Write the SKILL.md following the mandatory section order. Then test again:

```
Launch a subagent WITH the skill loaded.
Give it the same prompt.
Compare behavior to baseline — the skill should produce measurably different output.
```

If behavior is identical, the skill is not triggering or not providing actionable instructions.

### 3. REFACTOR: Close Loopholes
Test with pressure scenarios — prompts where Claude might rationalize skipping the skill's guidance:

```
"This is a simple case, just do it quickly"
"Skip the checklist, I trust you"
"We're in a hurry, just make it work"
```

If Claude bypasses the skill under pressure, add explicit loophole closers (see Rationalization Prevention below).

## Rationalization Prevention

For discipline-enforcing skills (verification, checklists, review gates), Claude will rationalize skipping steps under perceived time pressure. Counter this with explicit patterns:

### Loophole Closers
Add a `<HARD-GATE>` block for non-negotiable steps:

```markdown
<HARD-GATE>
Do NOT skip verification even if the fix seems obvious.
"Simple" bugs are where unexamined assumptions cause the most damage.
This applies to EVERY fix regardless of perceived simplicity.
</HARD-GATE>
```

### Common Rationalizations to Block

| Rationalization | Why It Fails | Counter |
|----------------|-------------|---------|
| "This is too simple to need X" | Simple cases are where assumptions hide | "Especially for simple cases" |
| "I already verified mentally" | Mental verification has no evidence trail | "Show the output" |
| "The user is in a hurry" | Rushing causes rework that wastes more time | "Fast is slow without verification" |
| "I just need to change one line" | One-line changes cause cascading failures | "Run the full check" |
| "The tests passed before" | Prior state is not current state | "Run tests NOW" |

### Red Flags in Skill Output
If Claude's output contains these phrases, the skill's discipline gates are being bypassed:
- "Since this is straightforward..." (skipping verification)
- "I'm confident that..." (substituting assertion for evidence)
- "Based on my earlier check..." (stale verification)
- "This should work because..." (reasoning instead of testing)

## Debugging Skills

If a skill is not firing or behaving incorrectly:

1. **Check discovery**: Run `/skills` to see if it appears in the loaded list
2. **Verify YAML**: Ensure frontmatter has opening and closing `---` with valid syntax
3. **Force invocation**: Type `/skill-name` to test manual trigger
4. **Inspect description**: If manual works but auto does not, the description lacks trigger phrases
5. **Check directory name**: Must match the `name` field exactly
6. **Run debug mode**: `claude --debug` shows skill triggering decisions in logs

## Component Selection Guide

| Need | Use | Why |
|------|-----|-----|
| Teach Claude HOW to do something | **Skill** | Injects procedural knowledge into context |
| FORCE something to happen every time | **Hook** | Deterministic shell execution, not probabilistic |
| Offload heavy cognitive work | **Agent** | Isolated context prevents pollution |
| Quick user-triggered action | **Command** | Slash-command shortcut |

## Success Criteria

- [ ] SKILL.md has valid YAML frontmatter with name and description
- [ ] Description embeds trigger phrases naturally (not a keyword list)
- [ ] Directory name matches the name field in frontmatter
- [ ] Section order follows the mandatory template exactly
- [ ] Content under 500 lines total; references used for large tables
- [ ] Every reference file has "when to read" guidance in SKILL.md
- [ ] Imperative form throughout (not "This skill does X")

## Copy/Paste Ready

```
"Create a new skill for [topic]"
"Improve this skill's description so it triggers better"
"Why isn't my skill auto-loading?"
"Write a SKILL.md for [workflow]"
"Help me structure a skill with reference files"
```
