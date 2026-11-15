# vstack architecture

Two repositories, one contract between them. This page says what lives where and why, how a run
flows through, and the rules `vstack check` enforces. Operational detail per harness is in
[../harness/README.md](../harness/README.md), the instance layout in
[../instance-template/README.md](../instance-template/README.md).

## 1. Two repositories, by design

The rule: **verbs are public, nouns are private.** How to gather, diff, write, gate, land and
record is open. Which tool, which document, which channel, which rubric, which rating scale,
which person is yours.

| | vstack (public) | instance (private) |
|---|---|---|
| Holds | CLI, schemas, invariants, skills, harness adapters, evals, docs | tool map, org profile, graph, cells, fixtures, program context, company-specific skills, the pin |
| Names | no company, no product, no person, no internal host or id | everything the company calls things |
| Author | personal e-mail | work e-mail |
| Remote | GitHub | the company's git host only |
| Changes when | the loop, the voice or a harness changes | a program, a team or a schedule changes |

One repository cannot hold both halves without leaking: a public repo with company files in it
is a leak, a private repo with the engine in it stops the engine being shared. Two repositories
with a checked boundary is the smallest arrangement that gives both. The boundary is enforced
three ways: `scripts/check.sh no-org` (denylist over every public file), `scripts/check.sh
instance` (the instance is outside the checkout and has no public remote), and the author
e-mail check on both sides.

## 2. The layers

```
 L4  harness        claude · codex · kiro · kirocrew        non-interactive flag + absolute paths
 L3  skills         writers · critic · plumbing             public here, company-specific in the instance
 L2  engine         render · run · check · link · gen-*     bin/vstack, schema/
 L1  instance       tools · org profile · graph · cells      private repo, read at run time, never contained
 L0  state          runs/ · ledger/runs.jsonl · cache/      ~/.local/state/vstack
```

A layer talks only to its neighbours. The harness never reads the instance directly: it reads a
rendered prompt whose paths point into both. A skill never reads a tool map: the prompt tells it
which absolute file to read. The engine never contains a tool name: it reads them from L1.

## 3. A run, end to end

1. **trigger**: a cron line emitted by `vstack gen-cron`, a Kiro Crew job, or an event the
   instance wires (a message, a mail, a tracker change). The trigger runs
   `vstack run <cell> --harness <h> --instance <dir>`.
2. **pre-flight**: `check` on the graph and cell, `verify-skills` against the lock. A drifted
   skill copy or a broken invariant stops the run before any model call.
3. **render**: one prompt with the seven stages, every path absolute, every tool role resolved
   to a real server and tool from `tools.json`. `--dry-run` swaps the sources for the fixture.
   `--no-publish` skips any role that would send a message even to corroborate.
4. **gather**: the harness calls the tools the prompt names, cache-first, and writes
   `evidence.json` with a content hash. Writers never see a tool.
5. **diff**: the previous evidence is compared, so a quiet week produces a short update.
6. **write**: the writer skill turns evidence into a draft in the house voice. Nothing not in
   the evidence may appear.
7. **gate**: `validate-writing` scores the draft, the writer revises, at least two passes, at
   most five, stop at zero blockers.
8. **land**: the draft reaches a compose box or a `[Draft]` document. A human sends.
9. **brief**: three lines the human decides from without opening the draft: what landed, the one
   fact that needs attention with its source, where it is and what to do.
10. **record**: one ledger line, one `result.json`, the single reply line `VSTACK_RESULT`.
11. **contract**: the engine reads the run directory back. Missing or malformed artifacts turn
    the status into `contract_unmet` whatever the model claimed.
12. **second opinion** (optional, `gate.second_opinion` or `--second-opinion`): an independent
    critic on another harness evaluates the draft against the evidence and writes
    `gate-second.md`. A finding counts only with the offending text quoted. Findings are
    recorded in `meta.json`, never edit, never block.

`vstack retro --days 7` reads the ledger back: runs per cell, contract misses, gate passes,
second-opinion findings and recurring Known Gaps, and asks for an enforcer per recurring line.
[RULES.md](RULES.md) is where that enforcer is recorded.

## 4. The graph

`graph.json` types every node and edge in an instance so `vstack check` can enforce the
invariants over the whole estate, not one cell at a time.

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

Invariants:

1. Every wake is a DAG. The only shared mutable state is the append-only ledger.
2. Writers and gates never fetch. A W or G node with an edge to an S node fails.
3. Every writer has exactly one gate before its sink, with `min_passes` at least 2.
4. Every sink records. A D node with no `records` edge, or a cell with no ledger fields, fails.
5. The privacy cut: in the private component (`hr` by default) only a D or L node may have an
   edge outward, and ledger fields may not carry rating, candidate, promo, salary or feedback text.
6. Every cell has a `dry_run_path`, so it can run with no side effects.
7. A writer cell reads at least two sources, more when `coverage` says so. One source is a copy,
   not an update.
8. A run is complete when its artifacts pass the done-means contract, never on the model's word.

## 5. The same cell at four scales

Each level's ledger is the next level's source:

| Scale | Unit | Trigger | Cache | Writer and gate | Sink | Ledger |
|---|---|---|---|---|---|---|
| section | one section of one document | evidence hash changed, or a reviewer comment | section files and a manifest | the document's skill, the critic | in-place patch | manifest provenance |
| document | one cell run | cron or event | `cache/<entity>/last-evidence.json` | write-* and the gate loop | a draft doc or message | `<cell>.jsonl` |
| bot | a memory partition hosting cells that share a cache | its crons and heartbeat | its workspace | the skills added to it | its dashboard and drafts | its ledger files |
| estate | the graph of bots | daily digest | the bots' ledgers | write-exec-update, validate-writing | one channel the owner reads | the asks ledger |

Two consequences. Bot boundaries are cache boundaries: two cells belong in one bot when they read
the same evidence. And the per-entity cache is the payoff: the weekly gather for 1:1 preparation
is the evidence a quarterly talent card needs, so the expensive document becomes a re-render over
a warm cache.

## 6. Why the writing is skills, not agents

A skill is knowledge the running model loads. An agent is a separate process with its own
context. The house rules are 17 rules read by six writers and the critic: as a skill they are one
file, as agents they would be seven copies that drift. vstack uses an agent only where it changes
the model, the tool surface or the isolation boundary, which in practice is the harness itself.

The writing skills do one thing: given evidence, produce a document in a consistent, honest
voice. They do not gather and they do not publish. Gathering and publishing touch company
systems and differ everywhere, so they stay in the instance's tool map and in the engine's
gather and land stages. A new document type is a new skill directory with `SKILL.md` and
`template.md`. A different ladder or rating scale is an org-profile override, never a skill edit.

## 7. What a harness must provide

A non-interactive flag, a way to read a file by absolute path, and a skills directory. That is
the whole port. The four wired today each take under fifteen lines in `harness_cmd`.
