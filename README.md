# vstack

One repository for a manager's recurring writing work on any coding agent: the scheduler and
plumbing (the **engine**), the writers and the critic (the **skills**), the adapters for four
harnesses, and the evals that keep all of it honest. Everything that names a company lives in a
second, private repository called the **instance**, which vstack reads at run time and never contains.

vstack merges two earlier repositories, one of them with its history: the engine (the CLI, schemas,
invariants) and `Leadership-Writing-Skills` (house rules, writers, validator).

```
                 instance (private, your company's words)        vstack (this repo, public)
                 ─────────────────────────────────────────       ──────────────────────────
  cron / event ─▶ cells/*.json  ──┐                               bin/vstack  render · run · check
                 tools.json      ├──▶  vstack run <cell> ─────▶   seven stages, one prompt
                 org-profile.md  │     --instance <path>          skills/   writers, critic, plumbing
                 context/        │     --harness claude|codex|    harness/  how each agent is invoked
                 fixtures/      ─┘              kiro|kirocrew     schema/   cell, graph, tools, ledger
                                                   │              evals/    fixtures and structural checks
                                                   ▼
                 ~/.local/state/vstack/runs/<cell>/<run>/   evidence · diff · draft · gate · result
                 ~/.local/state/vstack/ledger/runs.jsonl    one appended line per run
                                                   │
                                                   ▼
                 a DRAFT in a compose box or a [Draft] document. A human presses send.
```

## The seven stages

Every cell, at every scale, is the same loop. `vstack render` spells it out as one prompt with
absolute paths filled in, `vstack run` executes it on the harness you name.

```
trigger -> gather (cache-first, hashed) -> diff -> write (skill) -> gate (critic loop) -> land (draft) -> record (ledger)
```

## Invariants `vstack check` enforces

1. Every wake is a DAG. The only shared mutable state is the append-only ledger.
2. Writers and gates never fetch. A writer node with an edge to a source fails.
3. Every writer has exactly one gate before its sink, with at least two passes.
4. Every sink records. A cell with no ledger fields fails.
5. A private component (people, HR) records only dates, ids and counts.

## Layout

```
bin/vstack             the CLI
schema/                JSON Schemas: cell, graph, tools, ledger
skills/                one canonical copy of every public skill, linked into each harness
  leadership-writing/    house-rules.md (the voice), org-profile.md (neutral defaults)
  write-exec-update/ write-talent-card/ write-work-summary/ write-promo-doc/
  validate-writing/ rewrite/ rewrite-and-validate/ score-gate/
  gather-evidence/
harness/README.md      how claude, codex, kiro and kirocrew are invoked and where they read skills
instance-template/     copy into a private repo: tools.json, org-profile.md, mcp-servers.json,
                       graph.json, cells/, fixtures/, vstack.lock
evals/                 synthetic fixtures, expected outcomes, and what check.sh verifies
scripts/check.sh       identity, no-org denylist, schemas, frontmatter, loop, profile, instance
docs/ARCHITECTURE.md   the two-repo split, layers, run flow, graph types, invariants
```

## Quick start

```bash
git clone https://github.com/ivikash/vstack ~/github/vstack
V=~/github/vstack/bin/vstack

# 1. make every harness read the same skills
$V link-skills --canonical ~/github/vstack/skills \
   --targets ~/.claude/skills ~/.codex/skills ~/.agents/skills ~/.kiro/skills ~/.kiro/crew/skills \
   --skills leadership-writing write-exec-update validate-writing score-gate gather-evidence

# 2. create your instance from the template (a private repository, your work e-mail)
cp -r ~/github/vstack/instance-template ~/work/my-instance && cd ~/work/my-instance && git init
export VSTACK_INSTANCE=~/work/my-instance     # or pass --instance on every command

# 3. prove the estate is sound (no model call)
$V check

# 4. dry run a cell on any harness: fixture in, files out, nothing published
$V run ~/work/my-instance/cells/program-update.json --harness claude --dry-run
#  --harness codex | kiro | kirocrew

# 5. live: same command without --dry-run. The draft lands in a compose box; you press send.
#    standing schedule: $V gen-cron --cells ~/work/my-instance/cells --harness claude
```

## Checks before every commit

`scripts/check.sh` runs in seconds and needs no model. With `VSTACK_INSTANCE=<path>` it also
proves the instance is outside this repository and has no public remote.

## License

MIT. The skills contain no organisation-specific names, tools or systems, and the denylist in
`scripts/check.sh` keeps it that way.
