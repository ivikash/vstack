---
title: 0006 Adding a workflow
date: 2026-11-27
area: factory
realm: public
kind: note
tags: [meta, decision, factory]
status: accepted
---
# 0006 Adding a workflow

## Context
Goal stated by the owner 11/27/2026: every workflow carries a self-improvement loop (a correction to a landed doc becomes a contract rule without hand work, and every run measures itself against the previous one on cost, fill rate and how much he edited), every workflow and every decision has an ADR (public ones in the vstack repo, private ones in the private instance, both mirrored to the notes vault), existing behaviour is preserved unless he asks, and the loop runs hourly, daily, weekly, monthly, quarterly and yearly. The role guideline for the role guideline (pasted 11/27/2026) is the yardstick for what the factory should free him to do.
State read 11/27/2026: the engine already has per-run ledgers (runs.jsonl plus one per workflow with workflow-specific fields such as items_with_task_link, tbc_count, minutes_elapsed, tool_calls), a done-means contract check, `vstack retro` over the ledger, mistakes.md plus draft_contract regex per workflow, and the public repo keeps its own decisions.md (46 rows). Nothing re-reads a landed doc after the owner edits it, nothing compares a run with the previous one, nothing writes a contract rule from an edit, and no ADR files exist in either repo (the vault has 0001 to 0008 

## Decision
A fixed intake: `vstack new-workflow` asks the same short set every time (what document, who reads it, when it is due, which sources, where it lands, what it must never contain, one example of a good one), each with a recommended default drawn from the nearest existing workflow, then writes the workflow JSON, ADR 0001, mistakes.md, a sample and a dry run. The question set lives in `context/factory/intake.md` and is itself under the reflect loop

## Consequences
- A run that crosses the never line in the decision is a contract or check failure, not a judgement call.
- Reversing this means changing intake.md, new-workflow command together with every workflow that relies on it.
- Superseding this decision means a new ADR that names this one, never an edit here.

## Enforced by
intake.md, new-workflow command

## Source row
`context/factory/decisions.md` row 7, 11/27/2026
