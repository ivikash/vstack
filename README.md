<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo/vstack-logo-dark.svg">
    <img src="assets/logo/vstack-logo.svg" alt="vstack" width="560">
  </picture>
</p>

**Run a manager's recurring writing work on any coding agent, with proof it was done right.**

A weekly leadership update, a daily program status, a talent card, a work summary, a promotion
document: each is the same job. Gather evidence from the systems that hold it, write in a fixed
voice, check the draft against a checklist, put it where a human presses send, record what
happened. vstack turns that job into a file (a **workflow**), runs it on the coding agent you already
have (Claude Code, Codex, Kiro CLI or Kiro Crew), and refuses to call it done until the artifacts
prove it.

Everything that names your company lives in a second, private repository called the **instance**.
vstack reads it at run time and never contains it, and a check fails if the line is crossed.

- [Five words](#five-words)
- [What you get](#what-you-get)
- [How a run works](#how-a-run-works)
- [Install in ten minutes](#install-in-ten-minutes)
- [Write your first workflow](#write-your-first-workflow)
- [Run it, by hand and on a schedule](#run-it-by-hand-and-on-a-schedule)
- [What a finished run looks like](#what-a-finished-run-looks-like)
- [The skills](#the-skills)
- [The rules, and what enforces them](#the-rules-and-what-enforces-them)
- [Commands](#commands)
- [Layout](#layout)
- [Troubleshooting](#troubleshooting)
- [Design notes](#design-notes)

## Five words

| Word | Means |
|---|---|
| **workflow** | one recurring document as one JSON file: trigger, sources, writer, gate, sink, ledger. `workflows/weekly-update.json` is a workflow. Everything vstack does, it does to a workflow |
| **instance** | the private folder (and repository) that holds your company's facts: which tools, which documents, which channels, which people. vstack reads it, never contains it |
| **connector** | a capability name a workflow asks for (`chat.search`, `docs.read`). The instance's `connectors.json` binds each connector to a real MCP server and tool, so workflows never name tools |
| **harness** | the coding agent that runs the prompt: Claude Code, Codex, Kiro CLI or Kiro Crew |
| **run** | one execution of one workflow: a directory of artifacts under `~/.local/state/vstack/runs/` and one ledger line |

Three more words appear once you are inside: a **glossary** is your company's vocabulary the writers
substitute, **context** is the standing inputs a workflow reads every time (template contracts,
rules, rubrics), and a **brief** is the three lines you read instead of the draft.

`example/` is a complete instance for a made-up company. Copy it to start yours; the checks also
use it as the proof that the invariants hold on a real layout.

Everything in vstack is one of three kinds of thing, and the sections below follow that order:
**Define** (what should happen every time, in the instance), **Run** (what happened this time, on
disk), **Check** (what refuses a bad definition or a bad run, in the engine).

## What you get

| Piece | What it does | Where |
|---|---|---|
| **engine** | one Python file, no dependencies. Renders a workflow into a prompt, runs it on a harness, verifies the run directory, keeps a ledger, prints schedules and agent templates | `bin/vstack` |
| **skills** | the writers (executive update, talent card, work summary, promotion doc), the critic (`validate-writing`), the rewriters, and two plumbing skills. Plain markdown in the open [Agent Skills](https://agentskills.io/specification) format | `skills/` |
| **harness adapters** | how each of the four agents is invoked non-interactively and where it reads skills from | `harness/README.md`, `harness_cmd` in the engine |
| **example instance** | a complete instance for a made-up company: connectors, glossary, one workflow with its sample evidence. Copy it to start yours | `example/` |
| **evals and checks** | a nine-group check script, a routing eval for the skills, sample evidence with expected outcomes | `scripts/`, `evals/` |

## How a run works

```
   your private instance                 vstack (this repository)               your harness
   ─────────────────────                 ────────────────────────               ────────────
   workflows/weekly-update.json ─┐
   connectors.json               ├─▶ vstack run <workflow> --harness claude ─▶ one prompt, absolute paths
   glossary.md                   │       │                                      │
   context/, *.sample.json      ─┘       │ pre-flight: invariants,               ▼
                                     │ skill copies match the lock    claude -p / codex exec /
                                     │                                kiro-cli chat / kirocrew cron
                                     ▼                                   │
                        ~/.local/state/vstack/runs/<workflow>/<harness>-<id>/│
                           evidence.json  diff.md  draft.md  gate.md  brief.md  result.json
                                     │                                   │
                                     │ contract check: are the files there and well-formed?
                                     ▼
                        ledger/runs.jsonl  (one line per run, append-only)
                                     │
                                     ▼
                        a DRAFT in a compose box or a [Draft] document. A human presses send.
```

The prompt the harness runs has eight stages. Every workflow is this loop:

| Stage | What happens | Leaves behind |
|---|---|---|
| 1 gather | call the tools the workflow's **connectors** bind to, cache-first. Read-only | `evidence.json` with a `sources` list and a content hash |
| 2 diff | compare with the previous run's evidence | `diff.md` |
| 3 write | the writer skill turns evidence into a draft in the house voice. The first line says which sources were used and which were unavailable | `draft.md` |
| 4 gate | `validate-writing` scores the draft, the writer fixes every quoted failure, at least 2 and at most 5 passes. `gate.extra_checklists` adds the instance's own rule files (a house writing style) as further scored rules, and `gate-policy.json` in the instance can make them mandatory for every writer. `gate-policy.json required_style_rules` names a rules JSON for `scripts/style-check.py`, the countable half of that style (sentence length, weasel words, unexpanded acronyms, dates, URL labels, semicolons, em-dashes, hedge words, marker form, a marker used as a verb, comparatives without a number, from-X-to-Y spans without the relative change, unclosed brackets in a cell, a space before punctuation outside a link label, a title cell ending in an opener or a fragment): the writer runs `vstack style-check` inside the loop and `check-run` marks any finding unmet | `gate.md`, first line `passes: N` |
| 5 land | the draft goes to the sink: a compose box, a `[Draft]` document. Never sent | the landed path or id |
| 5b brief | three lines a busy reader decides from without opening the draft | `brief.md` |
| 6 record | `vstack record`: one result file, one scorecard, one ledger line | `result.json`, `scorecard.json`, a line in `runs.jsonl` |
| 7 reflect | 24 h and 7 d later, `vstack reflect` reads the landed document back and diffs it against the draft. Wording and structure edits become proposed contract rules, fact edits become mistakes rows, a section deleted three times stops being written. The same proposal twice is applied | `reflect-24h.json`, `reflect-7d.json`, `owner_edit_ratio` in the scorecard |
| contract | the engine reads the run directory back. Anything missing or malformed marks the run `contract_unmet`, whatever the model claimed | `meta.json` |

Two optional extras: `--second-opinion <harness>` runs an independent critic on another agent and
records its quoted findings (never edits, never blocks), and `vstack retro` reads the ledger back
weekly and lists what keeps going wrong.

## Define: install and write your first workflow

### Install in ten minutes

You need Python 3.9 or newer, git, and at least one of: Claude Code, Codex CLI, Kiro CLI, Kiro Crew.

**1. Clone and make every harness read the same skills.**

```bash
git clone https://github.com/ivikash/vstack ~/github/vstack
V=~/github/vstack/bin/vstack

$V link-skills --canonical ~/github/vstack/skills \
   --targets ~/.claude/skills ~/.codex/skills ~/.agents/skills ~/.kiro/skills ~/.kiro/crew/skills \
   --skills leadership-writing write-exec-update write-talent-card write-work-summary write-promo-doc \
            validate-writing rewrite rewrite-and-validate score-gate gather-evidence
```

Each harness directory now holds symlinks into this checkout. A `git pull` here updates all of
them; an existing real copy is moved aside, not deleted (`~/.local/state/vstack/skill-backups`).
Pass only the target directories for the harnesses you have.

**2. Create your instance from the example.** A private repository, committed with your work
e-mail, hosted only on your company's git server.

```bash
cp -r ~/github/vstack/example ~/work/my-instance
cd ~/work/my-instance && git init && git config user.email you@your-company.example
export VSTACK_INSTANCE=~/work/my-instance        # or pass --instance DIR on every command
```

Then edit, in this order:

| File | Change |
|---|---|
| `connectors.json` | bind each **connector** (`docs.read`, `chat.search`, `chat.draft`, ...) to the MCP server and tool your harness has. This is the only file that names real tools |
| `mcp-servers.json` | the servers those tools come from. `vstack gen-mcp --servers mcp-servers.json --target claude` prints the block for each harness's config |
| `glossary.md` | your company's words: what principles are called, the rating scale, level names. Only the keys you change |
| `workflows/program-update.json` | rename, set the `config` values (document id, channel, project), keep the connectors |
| `workflows/program-update.sample.json` | made-up evidence for dry runs. Real section names, invented values |

**3. Prove the definition is sound.** No model call, under a second.

```bash
$V check                      # invariants over workflows/
$V map                        # the estate derived from them: sources, writers, gates, sinks, ledgers, bots
cd ~/github/vstack && scripts/check.sh    # the public repo's own checks, including that your instance is private
```

**4. Dry run.** Sample evidence in, files out, nothing published, on whichever harness you have.

```bash
$V run ~/work/my-instance/workflows/program-update.json --harness claude --dry-run
#                                                    --harness codex | kiro | kirocrew | print
```

Which harness value is which: `claude`, `codex` and `kiro` run the prompt in a subprocess and wait.
`kirocrew` is the cron-worker path: it registers a one-shot scheduled job on the host and returns
`"status": "scheduled"`, so it is for live runs only. A `--dry-run` or `--no-publish` run on
`kirocrew` renders the prompt and registers nothing (`"status": "rendered"`). For a hand-driven
run on any host use `print` (or `vstack render`), follow the prompt yourself, then `vstack record`.

The command prints `meta.json` when the harness returns. Look for `"status": "ok"` or
`"known_gaps"` and `"contract": {"met": true}`. The run directory it names holds every artifact.

### Write your first workflow

A workflow is one JSON file. This is the example instance's workflow with a comment on each field:

```jsonc
{
  "id": "program-update",                 // lowercase-hyphen; names the run dir and ledger
  "kind": "writer",                       // writer | consumer | collector
  "component": "program",                 // partition; "hr" is the private one by default
  "trigger": {"cron": "29 8 * * 1-5", "timezone": "UTC", "events": []},
  "bot": "ProgramStatus",                 // the Kiro Crew bot that hosts it (bound on the Schedule page)
  "sources": [                            // connectors, never tool names; bound through connectors.json
    {"connector": "docs.read",   "ref": "${config.statusDocId}", "notes": "latest dated entries"},
    {"connector": "tasks.list",  "ref": "${config.taskProject}", "notes": "owner, due, status, last comment"},
    {"connector": "mail.search", "ref": "${config.meetingSummaryQuery}", "notes": "last ${config.lookbackDays} days"},
    {"connector": "chat.search", "ref": "${config.discussChannel}", "notes": "status and blockers"}
  ],
  "coverage": {"min_sources": 3},         // check fails a writer that reads fewer sources
  "cache": {"key": "program/${config.program}", "ttl_hours": 20},
  "writer": {"skill": "write-exec-update"},
  "gate": {"skill": "validate-writing", "doc_type": "exec-update",
           "min_passes": 2, "max_passes": 5, "coverage_bar": 85,
           "second_opinion": "codex"},    // optional independent critic
  "sink": {"connector": "chat.draft", "ref": "${config.postChannel}", "dry_run_path": "update.md"},
  "ledger": {"file": "program-update.jsonl",
             "fields": ["program", "overall_status", "red_sections", "green_by_dates", "open_action_items", "posted_to"]},
                                          // sample evidence: program-update.sample.json beside this file, by default
  "config": {"program": "Project Lantern", "statusDocId": "doc-0000", "taskProject": "project-0000",
             "meetingSummaryQuery": "\"Meeting summary\" Lantern", "discussChannel": "#lantern",
             "postChannel": "#lantern-leadership", "lookbackDays": 14}
}
```

Rules of thumb:

- **Connectors, not tools.** `chat.search` in the workflow, `slack-mcp / search` in `connectors.json`.
  Change the tool once, every workflow follows.
- **`${config.x}`** is substituted anywhere in the workflow, so ids and channels live in one block.
- **Three sources or more.** One source is a copy. Add a corroboration connector when your chat tool
  has an assistant you can ask, and put it in `coverage.require_connectors` so the check insists on it.
- **The sink is always a draft.** `chat.draft`, `docs.write` to a `[Draft]`, `mail.draft`. A connector
  that sends is a bug.
- **A private workflow** (`component: "hr"`) must name a `workspace`, and its ledger fields may not
  carry ratings, candidates or feedback text. `vstack check` refuses otherwise.

Full field reference: `schema/workflow.schema.json`. Validate with `$V check`.

## Run: by hand and on a schedule

```bash
# by hand, live: gathers from real sources, lands a draft, you press send
$V run <workflow> --harness claude

# live gather and gate, but the draft stays a file (for a first look at real evidence)
$V run <workflow> --harness claude --no-publish

# with an independent critic on another agent; findings land in meta.json
$V run <workflow> --harness claude --second-opinion codex

# see the prompt a harness would get, without running anything
$V render <workflow> --harness kiro

# standing schedule: one line per workflow with a trigger
$V gen-cron --harness claude     # crontab lines (workflows from $VSTACK_INSTANCE)
$V gen-cron --harness kirocrew   # kirocrew cron add commands, with the bot to bind each to

# a Kiro CLI agent template whose tool surface is exactly connectors.json
$V gen-agent --harness kiro > ~/.kiro/agents/vstack-runner.json

# weekly: what happened, what keeps going wrong
$V retro --days 7
```

On a schedule, the cron line calls `vstack run` directly. For Kiro Crew, the job's message tells
the agent to render the workflow with its shell and follow the printed prompt, so every wake gets a
fresh run directory and the agent's own MCP tools do the gathering.

### What a finished run looks like

```
~/.local/state/vstack/runs/program-update/claude-20261115-094200-c0b4fc/
  prompt.md         the exact prompt the harness received
  command.txt       the exact command
  evidence.json     {"gathered_at", "sources": [{"connector","status","items"}], "items": [...], "evidence_hash"}
  diff.md           what changed since the previous run
  draft.md          line 1 title, line 2 "Sources: used ...; unavailable ...", then the document
  gate.md           "passes: 2" then the last pass report, every rule with what it checked
  brief.md          three lines: what landed, the one fact to look at with its source, where and what to do
  update.md         the landed copy (dry run and no-publish) or the landed id/URL
  result.json       {"status": "ok" | "known_gaps" | "failed", "gate_passes": 2, "draft", "brief", "landed"}
  gate-second.md    (with --second-opinion) "findings: N" then each finding with the offending text quoted
  meta.json         run id, harness, timings, result, contract {met, unmet[]}, second_opinion
  stdout.log        what the harness printed
~/.local/state/vstack/ledger/runs.jsonl       one line per run, append-only
~/.local/state/vstack/cache/<key>/last-evidence.json
~/.local/state/vstack/retro/<date>.md         written by vstack retro
```

A brief from a real dry run, so you know the register:

```
PRISM daily exec update (dry run, 11/07 sample data): RED.
Ingestion is RED with no recovery date because the sources give two Hub cut-over targets, 11/05 and 11/19, and the owner owes one date by 11/10 (fixture, test data).
Draft at .../prism-update.md. Reader action: nothing (dry run, not posted).
```

## The skills

All under `skills/`, one directory each, linked into every harness. The writers never fetch and
never publish: they turn evidence into a document and nothing else.

| Skill | Use when | Reads |
|---|---|---|
| `write-exec-update` | a status update for executives: overall line, one block per workstream (RED/YELLOW/GREEN, Green-by when RED), milestones, risks, action items, Known Gaps | `format.md` |
| `write-talent-card` | a per-person talent-review card: rating rationale and key deliverables sections | `template.md` |
| `write-work-summary` | a structured work summary: timeline, task, challenges, action, result, artifacts | `template.md` |
| `write-promo-doc` | a narrative promotion document against a level rubric, with a real Reasons Not To Promote section | `template.md`, `rubric-TEMPLATE.md` |
| `validate-writing` | the gate. `gate` mode returns pass or fail with every failure quoted and a fix; `evaluate` mode returns a scored report. Never rewrites | `checklist.md` |
| `rewrite` | tighten supplied prose to the house rules, every fact and link preserved, nothing added | |
| `rewrite-and-validate` | the same, then loop through the gate until it passes, at least two passes | |
| `score-gate` | run any draft through the gate in a fixed loop and return the final draft plus a one-line result | |
| `gather-evidence` | the gather stage: cache-first, by connector, one `evidence.json`, never prose | |
| `leadership-writing` | not invoked. Holds `house-rules.md` (the voice: 17 rules, 4 of them mechanical blockers), `glossary.md` (neutral defaults) and `rationalizations.md` (12 excuses with their rebuttals, 7 red flags). Every writer and the critic read all three first | |

The voice in one paragraph: lead with the point and the fact behind it, active voice, no
superlatives, no hedging, no em-dashes or semicolons, every claim tied to an artifact in the
evidence, every missing fact labelled `(unverified)` or listed under Known Gaps, never invented.

## Check: the rules, and what enforces them

A rule nothing enforces is a wish. [docs/RULES.md](docs/RULES.md) pairs every rule with its check.
The checks, in the order they run:

| `scripts/check.sh` group | Fails when |
|---|---|
| identity | a commit here is not by the personal e-mail, or `git config user.email` is wrong |
| no-org | any public file carries a company term, internal host, ticket, chat, doc or account id |
| schemas | a JSON file does not parse, or the example instance breaks an invariant |
| frontmatter | a skill's `name` is not its directory name in lowercase-hyphen, or a description is empty or over 1024 characters |
| loop | a writer skill lacks the gate loop (min 2, max 5, reads house-rules) |
| glossary | a skill references a glossary key that is not defined |
| triggers | a skill's description does not win its own prompts in `evals/triggers.json` (36 cases, no model) |
| rules | `docs/RULES.md` names a check or subcommand that does not exist |
| instance | with `VSTACK_INSTANCE` set: the instance is inside this checkout, is a remote of it, or has a public remote |

And `vstack check` over an instance:

1. Writers and gates never fetch: a writer receives `evidence.json` and nothing else.
2. Every writer has exactly one gate before its sink, `min_passes` at least 2.
3. Every sink records: a workflow with no ledger fields fails.
4. The privacy cut: a private workflow names a private workspace, and its ledger fields may not
   carry rating, candidate, promo, salary or feedback text.
5. Every workflow has a `dry_run_path`, so it can run with no side effects.
6. A writer reads at least two sources, more when `coverage` says so.
7. Every source is a connector name, never a tool name.

And after every run, the **contract**: `evidence.json` with sources and hash, `diff.md`, `draft.md`
with its `Sources:` line, `gate.md` with enough passes, a three-line `brief.md`, `result.json`.

## Commands

| Command | Does |
|---|---|
| `vstack render <workflow> [--harness h]` | print the prompt, run nothing |
| `vstack run <workflow> --harness h [--dry-run] [--no-publish] [--second-opinion h2] [--agent a] [--model m]` | pre-flight, render, execute, contract check, ledger line |
| `vstack check [--instance d]` | invariants over the workflows, including the document budget: a document-writing sink names `document: {kind: rolling, title}` or `{kind: per_event, event}` and the instance's `documents.json` lists it |
| `vstack map [--instance d] [--json]` | the estate derived from the workflows: sources, writers, gates, sinks, ledgers, bots |
| `vstack check-run <run-dir>` | contract check on an existing run directory |
| `vstack verify-skills --dirs ... --skills ...` | every named skill present and identical in every harness dir |
| `vstack link-skills --canonical d --targets ... --skills ...` | symlink the canonical skills into each harness dir |
| `vstack gen-cron --harness h [--instance d]` | crontab lines, or `kirocrew cron add` commands with the bot to bind to |
| `vstack gen-agent --harness kiro [--instance d]` | a Kiro CLI agent template whose tool surface is exactly `connectors.json` |
| `vstack gen-mcp --servers f --target h` | the MCP server block for one harness |
| `vstack retro [--days n] [--trend-runs k]` | per-workflow runs, contract misses, gate passes, a scorecard trend table, flags for a field worse two runs in a row, recurring Known Gaps |
| `vstack record <run-dir> [--workflow f]` | stage 6 for any harness path: meta.json, `scorecard.json`, one `runs.jsonl` line (idempotent by run id). The rendered prompt tells the worker to run it, so an asynchronous run is counted too |
| `vstack reflect <run-dir> --age 24h\|7d [--render]` | stage 7: `--render` prints the worker prompt that reads the landed document back into `landed-<age>.md`, then the engine diffs it against draft.md by block, classifies each change (wording, fact, structure, deletion), writes `reflect-<age>.json`, fills `owner_edit_ratio`, and files proposals, mistakes and deletion counts in the instance context |
| `vstack reflect --due` | every landed run 24 h or 7 d old that has no reflect of that age yet, one `<run-dir> --age <age>` per line |

Every command accepts `--instance DIR` or reads `$VSTACK_INSTANCE` and fills `--connectors`,
`--glossary` and `--workflows` from it. State lives under `~/.local/state/vstack`.

## Layout

```
bin/vstack               the CLI, one file, standard library only
schema/                  workflow, connectors, ledger (JSON Schema)
skills/                  one canonical copy of every skill
harness/README.md        the four harnesses: exact command, skills dir, what a run leaves behind
example/                 a complete instance for a made-up company: README, connectors.json, glossary.md, mcp-servers.json, workflows/ with sample evidence, vstack.lock
evals/                   triggers.json, fixtures/ (synthetic evidence packs the skill evals read), results/
scripts/check.sh         the nine check groups
scripts/trigger-eval.py  the routing eval
docs/ARCHITECTURE.md     why two repos, the layers, the run, the derived map, the scales
docs/RULES.md            every rule and its enforcer
```

## Troubleshooting

| Symptom | Cause and fix |
|---|---|
| `pre-flight failed (skills)` | a harness dir has a stale copy or is missing a skill. `vstack link-skills ...` again, then `vstack verify-skills` |
| `pre-flight failed (invariants)` | the workflow breaks a rule. `vstack check` prints each one |
| `"status": "contract_unmet"` with `"claimed_status": "ok"` | the model said done but a file is missing or malformed. `meta.json` lists which; `vstack check-run <dir>` repeats it |
| `warning: instance pins vstack X, this checkout is Y` | you updated vstack. Dry run every workflow once, then write the new short SHA into the instance's `vstack.lock` |
| draft says `Sources: ... unavailable chat.search` | the connector is unbound in `connectors.json`, or the tool returned nothing. Fix the binding or the `ref`, never the draft |
| Kiro CLI denies a tool | kiro-cli 3.x denies any tool not named in `--trust-tools`; run under the `vstack-runner` template from `vstack gen-agent`, or let the adapter pass `--trust-all-tools` |
| a `kirocrew` run shows `"status": "scheduled"` | correct: the job runs asynchronously. Its run dir fills in when it finishes; `vstack check-run` on it then |
| a `kirocrew` run shows `"status": "rendered"` | you passed `--dry-run` or `--no-publish`: nothing was scheduled. Run the prompt by hand, then `vstack record` |
| `vstack record` again after a fix still reads the old verdict | it no longer does: one line per run id in `runs.jsonl`, the latest record replaces the earlier one |
| a worktree run reads the main checkout's files | write `${instance}` instead of an absolute instance path in `config` and `record.post_record`; it expands to the directory that holds the workflow's `workflows/` dir (or `--instance`) |
| `check.sh no-org` fails on your own text | the word is on the denylist for a reason. Rephrase in the public repo; the term belongs in the instance |

## Design notes

Why two repositories, what each layer owns, the derived map, the privacy cut and the same
workflow at four scales: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md). Recorded test runs:
[evals/results/](evals/results/).

## License

MIT.
