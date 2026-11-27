---
title: 0007 Every writing workflow loops
date: 2026-11-27
area: factory
realm: public
kind: note
tags: [meta, decision, factory]
status: accepted
---
# 0007 Every writing workflow loops

## Context
Goal stated by the owner 11/27/2026: every workflow carries a self-improvement loop (a correction to a landed doc becomes a contract rule without hand work, and every run measures itself against the previous one on cost, fill rate and how much he edited), every workflow and every decision has an ADR (public ones in the vstack repo, private ones in the private instance, both mirrored to the notes vault), existing behaviour is preserved unless he asks, and the loop runs hourly, daily, weekly, monthly, quarterly and yearly. The role guideline for the role guideline (pasted 11/27/2026) is the yardstick for what the factory should free him to do.
State read 11/27/2026: the engine already has per-run ledgers (runs.jsonl plus one per workflow with workflow-specific fields such as items_with_task_link, tbc_count, minutes_elapsed, tool_calls), a done-means contract check, `vstack retro` over the ledger, mistakes.md plus draft_contract regex per workflow, and the public repo keeps its own decisions.md (46 rows). Nothing re-reads a landed doc after the owner edits it, nothing compares a run with the previous one, nothing writes a contract rule from an edit, and no ADR files exist in either repo (the vault has 0001 to 0008 

## Decision
No document lands after one pass. Every writer runs draft, validate (house rules, the company writing style, template contract, numbers against sources), rewrite, at least two passes and at most five, and stops only at zero blockers. Anything the run cannot know (the journey behind an outcome, who decided what, why a date moved) is written as (TO BE CONFIRMED) and raised as an ask (decision 17), never guessed. This applies to incident write-ups, incident reviews, ops write-ups, retros, the daily people report, program updates and every future workflow

## Consequences
- A run that crosses the never line in the decision is a contract or check failure, not a judgement call.
- Reversing this means changing gate min_passes 2 max 5 on every workflow, `vstack check` fails a writer with no gate together with every workflow that relies on it.
- Superseding this decision means a new ADR that names this one, never an edit here.

## Enforced by
gate min_passes 2 max 5 on every workflow, `vstack check` fails a writer with no gate

## Source row
`context/factory/decisions.md` row 19, 11/27/2026
