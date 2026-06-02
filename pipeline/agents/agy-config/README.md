# anima + `agy` MCP overhead (operational incident #2)

**Finding (2026-06-02, verified against `agy --help` on Sean's v1.0.2):** the `agy`
flag surface has **no per-invocation config or MCP control flag** — no `--config`,
`--config-dir`, `--mcp-config`, `--allowed-mcp-server-names`, or `--extensions`. The
full surface is `--add-dir`, `-p/--print/--prompt`, `--prompt-interactive/-i`,
`--continue/-c`, `--conversation`, `--dangerously-skip-permissions`, `--sandbox`,
`--log-file`, `--print-timeout`, plus subcommands (`plugin`/`plugins`, `install`,
`update`, `changelog`, `help`).

**Consequence:** the surgical "point anima's `agy` calls at an isolated empty MCP
config" approach (the original Option A) is **not achievable** — there is no flag or
documented env var to redirect agy's config. The empty `mcp_config.json` beside this
README is retained only as a ready artifact *if* a future agy release adds a
config-dir override; it is **not** wired into `cli_runners.py` (no flag to wire).

## What MCP loading actually costs here

Local cold-start latency + extra `uvx`/`npx` child processes (the "Pencil,
notebooklm" spawns) contending with the asyncio child-watcher — **not** Gemini token
quota. So this is a latency/stability nuisance for the deferred eval run, not a
money or quota issue. It is the lowest-stakes of the three incidents.

## The available levers (both GLOBAL — affect interactive agy + IDE)

1. **`agy plugin disable <name>`** — managed, reversible (`agy plugin enable <name>`).
   List first: `agy plugin list`.
2. **`"disabled": true`** per server in `~/.gemini/config/mcp_config.json` (documented
   per-server field).

## Recommended use — scope it in TIME, not space

Because there's no anima-only scope, wrap a costed run with a disable/enable toggle
instead of permanently changing Sean's interactive setup:

```bash
agy plugin list                       # capture current state
agy plugin disable <heavy-server>     # e.g. the notebooklm / Pencil servers
# … run the deferred Em re-baseline …
agy plugin enable <heavy-server>      # restore interactive setup
```

Verify with `agy plugin list` (note: this v1.0.2 has **no** `agy inspect` subcommand).
Alternatively, if the latency is tolerable, do nothing — the `RateCapExhausted` guard
already handles the real (quota) risk, and MCP startup only lengthens the run.
