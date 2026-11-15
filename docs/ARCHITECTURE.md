# vstack architecture

This page explains **why** vstack is shaped the way it is. The README says how to use it,
[harness/README.md](../harness/README.md) says how each agent is invoked, and
[RULES.md](RULES.md) lists every rule with the check that enforces it.

- [1. The problem in one paragraph](#1-the-problem-in-one-paragraph)
- [2. Two repositories, by design](#2-two-repositories-by-design)
- [3. The layers](#3-the-layers)
- [4. One run, stage by stage](#4-one-run-stage-by-stage)
- [5. The graph and its invariants](#5-the-graph-and-its-invariants)
- [6. The privacy cut](#6-the-privacy-cut)
- [7. The same cell at four scales](#7-the-same-cell-at-four-scales)
- [8. Skills, not agents](#8-skills-not-agents)
- [9. What a harness must provide](#9-what-a-harness-must-provide)
- [10. Prior art](#10-prior-art)
- [11. Deliberate limits](#11-deliberate-limits)

## 1. The problem in one paragraph

A manager's writing is recurring, evidence-based and high-stakes: a weekly update to a director, a
talent card at review time, a promotion case. Each one means reading five systems, writing in a
voice the reader trusts, checking the draft, and placing it where the manager presses send. A
coding agent can do all of that, but left alone it will infer a status the evidence does not
support, invent a number that sounds right, skip the second check, and call the result done. vstack
exists to make that loop boring: one file per job, the same eight stages every time, checks that run
before the model is called and after it returns, and a human at the only exit.

## 2. Two repositories, by design

The rule: **verbs are public, nouns are private.** How to gather, diff, write, gate, land and
record is open and shared. Which tool, which document, which channel, which rubric, which rating
scale, which person is yours.

| | vstack (public) | instance (private) |
|---|---|---|
| Holds | engine, schemas, invariants, skills, harness adapters, evals, docs | tool map, org profile, graph, cells, fixtures, program context, company-specific skills, the pin |
| Names | no company, no product, no person, no internal host or id | everything the company calls things |
| Author | personal e-mail | work e-mail |
| Remote | GitHub | the company's git host only |
| Changes when | the loop, the voice or a harness changes | a program, a team or a schedule changes |

One repository cannot hold both halves. A public repository with one company file in it is a leak.
A private repository with the engine in it stops the engine being shared and pulls every harness
install behind the company firewall. Two repositories with a checked boundary is the smallest
arrangement that gives both. The boundary is enforced three ways, all in `scripts/check.sh`:

- `no-org`: a denylist of company terms, hosts and id shapes over every public file. The moment a
  term first appears in an instance file, it is added here in the same sitting.
- `identity`: every public commit by the personal e-mail, and `git config` set to it.
- `instance`: with `VSTACK_INSTANCE` set, the instance is outside this checkout, is not a remote of
  it, and has no public remote.

The instance pins the vstack commit it was last dry-run against in `vstack.lock`. The engine
warns when it runs from a different commit, so an upgrade is a deliberate step: dry-run every
cell, then move the pin.

## 3. The layers

```
 L4  harness   claude · codex · kiro · kirocrew     non-interactive flag, reads files by absolute path
 L3  skills    writers · critic · plumbing          public here, company-specific ones in the instance
 L2  engine    render · run · check · link · gen-*  bin/vstack, schema/
 L1  instance  tools · org profile · graph · cells   private repo, read at run time, never contained
 L0  state     runs/ · ledger/runs.jsonl · cache/   ~/.local/state/vstack
```

A layer talks only to its neighbours:

- The **harness** never reads the instance. It reads one rendered prompt whose absolute paths point
  into both repositories.
- A **skill** never reads a tool map. The prompt tells it which file to read next.
- The **engine** never contains a tool name. It reads them from the instance's `tools.json` and
  writes them into the prompt as `role -> server, tool`.
- **State** is plain files under one root. No daemon, no database, nothing to back up but a folder.

## 4. One run, stage by stage

```
trigger ─▶ pre-flight ─▶ render ─▶ [ gather ─▶ diff ─▶ write ─▶ gate ─▶ land ─▶ brief ─▶ record ] ─▶ contract ─▶ (second opinion)
            engine        engine    ─────────────────── the harness, from one prompt ──────────────────    engine        another harness
```

**Trigger.** A cron line from `vstack gen-cron`, a Kiro Crew job, or an event the instance wires
(a message, a mail, a tracker change). It runs `vstack run <cell> --harness <h> --instance <dir>`.

**Pre-flight (engine).** `check` on the graph and this cell. `verify-skills` on every skill the
cell needs, across the harness skill directories, against the lock. A drifted copy or a broken
invariant stops the run before any model call. This is the cheapest place to fail.

**Render (engine).** One prompt. Every `${config.x}` substituted, every source role resolved to a
real server and tool, every path absolute, the org profile inlined, the gate parameters filled in.
`--dry-run` swaps the sources for the cell's fixture. `--no-publish` keeps live sources but lands
the draft as a file and skips any role that would send a message even to corroborate. The prompt
opens with the rules that apply to every stage and a **Done means** list naming the files the run
must leave behind.

**Gather (harness).** Cache-first: if the cell's cached evidence is younger than `ttl_hours`,
reuse it. Otherwise call each role's tool with its `ref`. Read-only tools only. Keep facts as they
appear, record both values when sources disagree, never infer. Write `evidence.json` with a
`sources` list (role, status, item count) and a hash of the sorted items.

**Diff (harness).** Compare with the previous evidence and write what changed. A quiet week then
produces a short update instead of a re-narration.

**Write (harness).** Read `house-rules.md`, `rationalizations.md` and the writer skill, then produce
the document from the evidence alone. The first line after the title is
`Sources: used ...; unavailable ...` so a thin run is visible to the reader, never papered over.

**Gate (harness).** `validate-writing` in gate mode: every rule either passes with what it checked
named, or fails with the offending text quoted and a fix. Fix, re-run, at least two passes, at
most five, stop at zero blockers and zero majors. An unfixable blocker goes under Known Gaps. A
fix may never invent a fact.

**Land (harness).** The draft reaches the sink role: a compose box, a `[Draft]` document, a mail
draft. Never sent. This is the only write outside the run directory in the whole run.

**Brief (harness).** Three lines a busy reader decides from without opening the draft: what landed
with one status word, the one fact that needs attention with its source, where the draft is and
what to do (send, approve, nothing).

**Record (harness).** One line appended to the cell's ledger with the fields the cell names plus run
id, harness, flags and gate passes. One `result.json`. One reply line, `VSTACK_RESULT`.

**Contract (engine).** The engine reads the run directory back. Missing or malformed artifacts
(`evidence.json` without a sources list or hash, no `diff.md`, a draft without its `Sources:` line,
a gate report with too few passes, a brief that is not three lines, no `result.json`) turn the status
into `contract_unmet` and keep the model's claim beside it as `claimed_status`. The model's reply
is never the evidence; the files are.

**Second opinion (engine, optional).** With `gate.second_opinion` or `--second-opinion <harness>`,
a critic on a different agent reads the draft and the evidence cold, checks every number, date,
name and link, and writes `gate-second.md`. A finding counts only with the offending text quoted;
anything else is a note. Findings are recorded in `meta.json`. They never edit and never block,
because a critic that can block is a second writer.

After the run, `vstack retro --days N` reads the ledger back: runs per cell, contract misses, gate
passes, second-opinion findings and the Known Gaps that recur. Each recurring line is a missing
source, a missing rule or a missing check, in that order of preference, and the chosen enforcer is
recorded in [RULES.md](RULES.md).

## 5. The graph and its invariants

A cell is checked on its own, but the estate (every bot, every cell, every source) is checked as a
typed graph in `graph.json`, so a rule like "writers never fetch" holds across cells, not just
inside one.

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

| # | Invariant | Why |
|---|---|---|
| 1 | The graph is a DAG; the only shared mutable state is the append-only ledger | no two cells can wait on each other, and nothing is edited in place |
| 2 | W and G nodes have no edge to an S node | a writer that can fetch will fetch to fill a gap, and the gap is the finding |
| 3 | Every W has exactly one G before its D, `min_passes` at least 2 | the first fix introduces the second defect |
| 4 | Every D has a `records` edge; every cell has ledger fields | a landing nobody recorded cannot be audited or diffed next week |
| 5 | In the private component only D or L nodes have an edge outward; ledger fields never carry rating, candidate, promo, salary or feedback text | see section 6 |
| 6 | Every cell has a `dry_run_path` | every cell can be exercised with no side effects, on every harness, before it is trusted live |
| 7 | A writer reads at least `coverage.min_sources` (default 2) and every `coverage.require_roles` | one source is a copy, not an update; a required corroboration role cannot be quietly dropped |
| 8 | A run is complete when its artifacts pass the contract | the model's word is not evidence |

## 6. The privacy cut

People data (ratings, feedback, candidates, promotion arguments) lives in a separate connected
component of the graph, `hr` by default. Cells in it must name a private `workspace`. Only two
kinds of node may have an edge out of the component: a sink (the draft lands in a private folder a
human opens) and a ledger whose fields the check inspects by pattern. Sources, caches, writers,
gates and bots in the component never do. The result: a daily digest bot can read that a talent
card was drafted on a date, and nothing else.

## 7. The same cell at four scales

Each level's ledger is the next level's source:

| Scale | Unit | Trigger | Cache | Writer and gate | Sink | Ledger |
|---|---|---|---|---|---|---|
| section | one section of one document | evidence hash changed, or a reviewer comment | section files and a manifest | the document's skill, the critic | in-place patch | manifest provenance |
| document | one cell run | cron or event | `cache/<entity>/last-evidence.json` | write-* and the gate loop | a draft doc or message | `<cell>.jsonl` |
| bot | a memory partition hosting cells that share a cache | its crons and heartbeat | its workspace | the skills added to it | its dashboard and drafts | its ledger files |
| estate | the graph of bots | daily digest | the bots' ledgers | write-exec-update, validate-writing | one channel the owner reads | the asks ledger |

Two consequences. **Bot boundaries are cache boundaries**: two cells belong in one bot when they
read the same evidence, and a time-boxed effort over the same sources is a goal inside that bot, not
a new bot. **The per-entity cache is the payoff**: the weekly gather for 1:1 preparation is the
evidence a quarterly talent card needs, so the expensive document becomes a re-render over a warm
cache.

## 8. Skills, not agents

A skill is knowledge the running model loads into its context. An agent is a separate process with
its own context, prompt, tools and model. The house rules are 17 rules read by six writers and the
critic: as a skill they are one file, as agents they would be seven copies that drift. vstack uses an
agent only where it changes the model, the tool surface or the isolation boundary, which in
practice is the harness itself.

The writing skills do one thing: given evidence, produce a document in a consistent, honest voice.
They do not gather and they do not publish. Gathering and publishing touch company systems and
differ everywhere, so they stay in the instance's tool map and the engine's gather and land stages.
A new document type is a new skill directory with `SKILL.md` and `template.md`. A different ladder
or rating scale is an org-profile override, never a skill edit.

Every skill follows the open Agent Skills format (`name` equals the directory, lowercase-hyphen;
`description` says what it does and when to use it), so the same directory works on every harness
and `scripts/trigger-eval.py` can prove each description wins the prompts meant for it.

## 9. What a harness must provide

A non-interactive flag, a way to read a file by absolute path, and a skills directory. That is the
whole port. The four wired today take under fifteen lines each in `harness_cmd`:

| Harness | Non-interactive form | Skills directory |
|---|---|---|
| Claude Code | `claude -p`, prompt on stdin, tools limited to read, write, edit, glob, grep and three shell verbs | `~/.claude/skills` |
| Codex | `codex exec` in the run directory, workspace-write sandbox | `~/.codex/skills`, `~/.agents/skills` |
| Kiro CLI | `kiro-cli chat --no-interactive --trust-all-tools`, scoped through `--agent` | `~/.kiro/skills` |
| Kiro Crew | `kirocrew cron add`, a one-shot job the agent runs with its own MCP tools; the engine checks the run directory when it fills in | `~/.kiro/crew/skills` |

Nothing in vstack depends on a harness's plugin or marketplace format, which is why one cell runs on
all four unchanged.

## 10. Prior art

Several open skill collections for coding agents arrive at the same mechanisms independently. vstack
uses them where they fit a recurring writing job and names the source so a reader can compare:

| Practice | Also in | In vstack |
|---|---|---|
| a bounded critic loop with a hard round cap | gstack review rounds, Pocock software-factory brakes | gate `min_passes` 2, `max_passes` 5 |
| done means artifacts, not claims | gstack skill contracts, agent-skills verification gates, Superpowers verification-before-completion | the contract check after every run |
| a brief at the checkpoint, pushed as late as possible | Pocock loop-me | `brief.md`, the human's only required read |
| say which sources ran and which did not | Anthropic knowledge-work plugins (standalone vs connected) | the `Sources:` header |
| an independent critic on another model, findings only with proof | gstack outside review, pstack interrogate | `--second-opinion` |
| excuses with rebuttals and red flags, per skill | agent-skills anti-rationalization tables | `rationalizations.md` plus a Red flags section per writer |
| descriptions that route, proven by evals | agent-skills trigger evals, the Agent Skills spec | `trigger-eval.py` in `check.sh` |
| every rule paired with its enforcer, fixed at the highest level | pstack correct | `RULES.md`, `check.sh rules` |
| a retro that reads the ledger and asks for an enforcer | gstack retro, pstack reflect | `vstack retro` |
| read-only gather, one write at the sink | claude-quickstarts autonomous-coding security model | prompt stage 0 and the Claude tool allowlist |

Two things are specific to vstack: the privacy cut and the instance contract. They matter for one
person running automation inside a company, which is not the situation those collections address.

## 11. Deliberate limits

- **One model per run.** A cell runs on one harness invocation; there is no per-stage model tier.
  The second opinion is the one place a second model enters.
- **Cron and jobs, not events.** The schema has an `events` field and the prompt honours it, but
  `gen-cron` emits only clock triggers. Event wiring belongs to the instance and its harness.
- **No daemon.** State is files. If you want a dashboard, read `runs.jsonl`.
- **Drafts only.** No sink role sends. If a harness's tool can only send, it is not a sink.
