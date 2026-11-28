---
title: 0019 The intake command exists: `vstack new-workflow` is built, decision 7 is no longer a record without a mechanism
date: 2026-11-28
area: factory
realm: public
kind: note
tags: [meta, decision, factory]
status: accepted
---
# 0019 The intake command exists: `vstack new-workflow` is built, decision 7 is no longer a record without a mechanism

## Context
Goal stated by the owner 11/27/2026: every workflow carries a self-improvement loop (a correction to a landed doc becomes a contract rule without hand work, and every run measures itself against the previous one on cost, fill rate and how much he edited), every workflow and every decision has an ADR (public ones in the vstack repo, private ones in the private instance, both mirrored to the notes vault), existing behaviour is preserved unless he asks, and the loop runs hourly, daily, weekly, monthly, quarterly and yearly. The role guideline for the role guideline (pasted 11/27/2026) is the yardstick for what the factory should free him to do.
State read 11/27/2026: the engine already has per-run ledgers (runs.jsonl plus one per workflow with workflow-specific fields such as items_with_task_link, tbc_count, minutes_elapsed, tool_calls), a done-means contract check, `vstack retro` over the ledger, mistakes.md plus draft_contract regex per workflow, and the public repo keeps its own decisions.md (46 rows). Nothing re-reads a landed doc after the owner edits it, nothing compares a run with the previous one, nothing writes a contract rule from an edit, and no ADR files exist in either repo (the vault has 0001 to 0008 

## Decision
Engine commit on `promo-doc` (11/28/2026, parity report Needs a build 1): `vstack new-workflow <id> --instance d` asks the seven questions decision 7 lists (what document, who reads it, when due, which sources, where it lands, what it must never contain, one example of a good one), each defaulting from the nearest existing workflow (`--like`, else the id sharing the most words), and writes `workflows/<id>.json`, `workflows/<id>.sample.json`, `context/<id>/mistakes.md`, `context/<id>/example.md` and `adr/<id>/0001-why-it-exists-and-what-it-must-never-do.md` in the shape `gen-adr.py` expects, then runs `vstack check` with the new file inside the instance and a dry run (`render --dry-run --harness print`). Non-interactive through `--answers file.json`, `--set key=value` or `--defaults`, `--out dir` for a scratch intake checked through a symlink view of the instance. Never overwrites, refuses a never rule that is not a regex. The question set in prose is `context/factory/intake.md` with the defaults rule and one worked example (hiring-pipeline, dry run 11/28/2026 into scratch, invariants PASS). The parity report counted eight questions, decision 7 lists seven, the seven stand and the workflow id is the argument

## Consequences
- A run that crosses the never line in the decision is a contract or check failure, not a judgement call.
- Reversing this means changing `vstack new-workflow`, `scripts/engine-selftest.py` new-workflow behaviour (seven keys in order, five files, dry run, check on the view, no overwrite, bad regex refused, `--defaults` takes all seven), `context/factory/intake.md` together with every workflow that relies on it.
- Superseding this decision means a new ADR that names this one, never an edit here.

## Enforced by
`vstack new-workflow`, `scripts/engine-selftest.py` new-workflow behaviour (seven keys in order, five files, dry run, check on the view, no overwrite, bad regex refused, `--defaults` takes all seven), `context/factory/intake.md`

## Source row
`context/factory/decisions.md` row 85, 11/28/2026
