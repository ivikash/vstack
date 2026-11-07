# Architecture

## Layers and the public / private line

The rule: **verbs are public, nouns are private.** How to gather, diff, write, gate, land and
record is open. Which tool, which document, which channel, which rubric, which rating scale,
which person is yours.

```
L4  RUNNERS           claude -p | codex exec | kiro-cli chat --no-interactive | kirocrew cron (Bot)     public
L3  ORCHESTRATION     graph.json, cells/*.json, kernel check, kernel gen-cron                           public schema, private instances
L2  STATE             evidence cache + manifest (content hashes), ledger/*.jsonl (append-only)         public schema, private data
L1  SKILLS            leadership-writing, write-*, validate-writing, gather-evidence, score-gate       public
                      org-profile.<org>.md, rubrics, confidentiality rules                             private
L0  TOOLS             tools.<org>.json: role -> MCP server + tool; one file generates every harness's MCP config   private
```

## Node and edge types

| Node | Meaning |
|---|---|
| S | source, a system of record, read-only |
| C | cache, content-addressed evidence per entity |
| W | writer, a pure skill, no I/O |
| G | gate, a pure critic |
| D | draft sink, where output waits for one human click |
| L | ledger, append-only outcome record |
| B | bot, a memory partition that hosts cells |

Edges: `reads` (S or L to C or W), `writes` (C to W), `gates` (W to G), `lands` (G to D),
`records` (D to L), `delegates` (B to B).

## The fractal

The same seven-stage cell repeats at four scales, and each level's ledger is the next level's
source:

| Scale | Unit | Trigger | Cache | Writer and gate | Sink | Ledger |
|---|---|---|---|---|---|---|
| section | one section of one document | evidence hash changed, or a reviewer comment | section files and a manifest | the document's skill, the critic | in-place patch | manifest provenance |
| document | one cell run | cron or event | `data/<entity>/evidence.json` | write-* and the gate loop | a draft doc or message | `<cell>.jsonl` |
| bot | a memory partition hosting cells that share a cache | its crons and heartbeat | its workspace | the skills added to it | its dashboard and drafts | its ledger files |
| crew | the graph of bots | daily digest | the bots' ledgers | write-exec-update, validate-writing | one channel the owner reads | the asks ledger |

Two consequences:

- **Bot boundaries are cache boundaries.** Two cells belong in one bot when they read the same
  evidence. A time-boxed effort with the same sources as an existing bot is a goal inside that bot,
  not a new bot.
- **The per-entity cache is the payoff.** A weekly gather for 1:1 preparation is the same
  evidence a quarterly talent card needs. The expensive document becomes a re-render over a cache
  that is already warm.

## Portability

Three things are the same on every harness: SKILL.md files (the open Agent Skills format), MCP
tools, and plain files. Everything harness-specific is in `bin/kernel`'s `harness_cmd`, about ten
lines per harness. A new harness is a new branch there and a row in the README table.

## What a private repository holds

```
tools.<org>.json          roles -> real MCP servers and tools
org-profile.<org>.md      principles, rating labels, level names, role names
rubrics/*.md              level guidelines passed to writers at run time
cells/<org>/*.json        cell instances with real ids and channels in config
graph.<org>.json          the instance graph kernel check validates
mcp-servers.json          one list that kernel gen-mcp turns into each harness's config
```

Commits there use the organisation e-mail; commits here and in the skills repository use a
personal one. Both are enforced by `scripts/check.sh` in the pre-commit hook.
