# vstack architecture

Two repositories, one contract between them. This page says what lives where and why, and how a
run flows through. The kernel internals are in [kernel-architecture.md](kernel-architecture.md),
the writing discipline in [writing-architecture.md](writing-architecture.md).

## 1. Two repositories, by design

| | vstack (public) | instance (private) |
|---|---|---|
| Holds | CLI, schemas, invariants, public skills, harness adapters, evals, docs | tool map, org profile, graph, cells, fixtures, program context, company-specific skills, the pin |
| Names | no company, no product, no person, no internal host or id | everything the company calls things |
| Author | personal e-mail | work e-mail |
| Remote | GitHub | the company's git host only |
| Changes when | the loop, the voice or a harness changes | a program, a team or a schedule changes |

One repository cannot hold both halves without leaking: a public repo with company files in it
is a leak, a private repo with the kernel in it stops the kernel being shared. Two repositories
with a checked boundary is the smallest arrangement that gives both. The boundary is enforced
three ways: `scripts/check.sh no-org` (denylist over every public file), `scripts/check.sh
instance` (the instance is outside the checkout and has no public remote), and the author
e-mail check on both sides.

## 2. The layers

```
 L4  harness        claude · codex · kiro · kirocrew        (harness/README.md)
 L3  skills         writers · critic · plumbing             (skills/, instance/skills/)
 L2  kernel         render · run · check · link · gen-*     (bin/vstack, schema/)
 L1  instance       tools · org profile · graph · cells      (private repo)
 L0  state          runs/ · ledger/runs.jsonl · cache/      (~/.local/state/vstack)
```

A layer talks only to its neighbours. The harness never reads the instance directly: it reads a
rendered prompt whose paths point into both. A skill never reads a tool map: the prompt tells it
which absolute file to read. The kernel never contains a tool name: it reads them from L1.

## 3. A run, end to end

1. **trigger**: a cron line emitted by `vstack gen-cron`, a Kiro Crew job, or an event the
   instance wires (a message, a mail, a tracker change). The trigger runs
   `vstack run <cell> --harness <h> --tools <instance>/tools.json --org-profile <instance>/org-profile.md`.
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
9. **record**: one ledger line, one `result.json`, the single reply line `KERNEL_RESULT`.

## 4. Why skills are files and not agents

A skill is knowledge the running model loads. An agent is a separate process with its own
context. The house rules are 17 rules read by six writers and the critic: as a skill they are one
file, as agents they would be seven copies that drift. vstack uses an agent only where it changes
the model, the tool surface or the isolation boundary, which in practice is the harness itself.

## 5. What a harness must provide

A non-interactive flag, a way to read a file by absolute path, and a skills directory. That is
the whole port. The four wired today each take under fifteen lines in `harness_cmd`.

## 6. Where the practices come from

The loop shape matches what the public skill packs converged on in 2026: trigger, checkpoint
pushed late, brief instead of raw output, deterministic checks before a model review, a bounded
review loop, an append-only ledger, and fresh context per run with state in files. vstack's
additions are the privacy cut and the instance contract, which none of the packs needed because
none of them were written for one person inside a company.
