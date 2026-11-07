# manager-ops-kernel

The plumbing that runs a manager's recurring writing work on any agent harness, with the writing
itself kept in skills and the company-specific parts kept in files you own.

Pair it with [Leadership-Writing-Skills](https://github.com/ivikash/Leadership-Writing-Skills)
(the writers and the critic) and a private repository holding your organisation's tool map, org
profile, rubrics and cell instances.

## Why "kernel"

In an operating system the kernel is the small fixed part that schedules work, isolates processes
and talks to devices through drivers, while every application is written against the kernel's
interface and knows nothing about the hardware. This repository plays the same role for manager
automation:

| Operating system | This kernel |
|---|---|
| process | a **cell**: one unit of automation (`cells/*.json`) |
| scheduler | `kernel run` on a cron, a Bot heartbeat, or by hand |
| device driver | `tools.json`: maps a capability role (`docs.read`) to a real MCP tool |
| memory protection | the **privacy cut**: a private component whose only exits are drafts and sanitised ledger lines |
| syscall interface | the seven stages every cell runs: trigger, gather, diff, write, gate, land, record |
| user space | the skills that write and check, and the harness (Claude Code, Codex, Kiro CLI, Kiro Crew) |

Change the harness, the tools or the company and the cells do not change.

## What is in here

```
bin/kernel            one CLI: render, run, check, verify-skills, link-skills, gen-cron, gen-mcp
schema/               JSON Schemas for cell, graph, tools and ledger files
cells/example/        a program status update cell (synthetic config)
graph/example.graph.json   typed nodes and edges the invariants are checked against
tools/tools.example.json   role -> MCP tool map, generic names
fixtures/             synthetic evidence for dry runs
skills/               plumbing skills: gather-evidence, score-gate
docs/ARCHITECTURE.md  layers, invariants, the fractal
scripts/check.sh      repository invariants (author e-mail, no company terms, schemas parse)
```

## The seven stages

Every cell, at every scale, is the same loop:

```
trigger -> gather (cache-first, hashed) -> diff -> write (skill) -> gate (critic loop) -> land (draft for one click) -> record (ledger line)
```

`kernel render` turns a cell into one prompt with those stages spelled out and absolute paths
filled in. `kernel run` executes that prompt on the harness you name and records the outcome.

## Invariants `kernel check` enforces

1. Every wake is a DAG. The only shared mutable state is the ledger, and it is append-only.
2. Writers and gates never fetch. A writer node with an edge to a source fails.
3. Every writer has exactly one gate before its sink. A writer cell without a `gate` fails.
   `min_passes` is at least 2.
4. Every sink records. A cell with no ledger fields fails.
5. Privacy cut. A cell in the private component (default `hr`) must name a private workspace, and
   its ledger may not carry rating, candidate, promo, compensation or feedback-text fields. In the
   graph, only sink (D) and ledger (L) nodes may have an edge out of the private component.
6. Every cell is runnable without side effects: `sink.dry_run_path` is required.

## Run a cell

```bash
# see the prompt, no model call
bin/kernel render cells/example/program-update.json --tools tools/tools.example.json --dry-run

# dry run (fixture in, files out, nothing published) on each harness
bin/kernel run cells/example/program-update.json --harness claude   --tools tools/tools.example.json --dry-run
bin/kernel run cells/example/program-update.json --harness codex    --tools tools/tools.example.json --dry-run
bin/kernel run cells/example/program-update.json --harness kiro     --tools tools/tools.example.json --dry-run
bin/kernel run cells/example/program-update.json --harness kirocrew --tools tools/tools.example.json --dry-run --agent <bot>

# live: add --org-profile and your private tools.json, drop --dry-run
```

Each run leaves `prompt.md`, `evidence.json`, `diff.md`, `draft.md`, `gate.md`, `result.json`,
`stdout.log` and `meta.json` under `~/.local/state/kernel/runs/<cell>/<harness>-<run id>/` and
appends one line to `~/.local/state/kernel/ledger/runs.jsonl`.

## Harness notes

| Harness | How `kernel run` invokes it | Scheduling |
|---|---|---|
| Claude Code | `claude -p --permission-mode acceptEdits --allowedTools Read Write ...` | OS cron (`kernel gen-cron --harness claude`) |
| Codex | `codex exec -C <run dir> -s workspace-write` | OS cron |
| Kiro CLI | `kiro-cli chat --no-interactive --trust-tools=fs_read,fs_write,execute_bash` | OS cron |
| Kiro Crew | `kirocrew cron add ... --at "in 1 minute" --agent <bot>` (runs on the Bot's memory and workspace) | native cron bound to a Bot (`kernel gen-cron --harness kirocrew`) |

Skills are read from `~/.agents/skills` by default (what `npx skills add` writes). Run
`kernel link-skills` once so every harness skill directory is a symlink to that one place, and
`kernel verify-skills` before each run to prove the copies match.

## Keep it generic

`scripts/check.sh` refuses commits that name a company, an internal host, a ticket or channel id,
or use a non-public author e-mail. Those belong in your private repository: `tools.<org>.json`,
`org-profile.<org>.md`, `cells/<org>/*.json`, `graph.<org>.json`.

MIT licensed.
