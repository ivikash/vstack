---
title: 0003 How the factory sees edits
date: 2026-11-27
area: factory
realm: public
kind: note
tags: [meta, decision, factory]
status: accepted
---
# 0003 How the factory sees edits

## Context
Goal stated by the owner 11/27/2026: every workflow carries a self-improvement loop (a correction to a landed doc becomes a contract rule without hand work, and every run measures itself against the previous one on cost, fill rate and how much he edited), every workflow and every decision has an ADR (public ones in the vstack repo, private ones in the private instance, both mirrored to the notes vault), existing behaviour is preserved unless he asks, and the loop runs hourly, daily, weekly, monthly, quarterly and yearly. The role guideline for the role guideline (pasted 11/27/2026) is the yardstick for what the factory should free him to do.
State read 11/27/2026: the engine already has per-run ledgers (runs.jsonl plus one per workflow with workflow-specific fields such as items_with_task_link, tbc_count, minutes_elapsed, tool_calls), a done-means contract check, `vstack retro` over the ledger, mistakes.md plus draft_contract regex per workflow, and the public repo keeps its own decisions.md (46 rows). Nothing re-reads a landed doc after the owner edits it, nothing compares a run with the previous one, nothing writes a contract rule from an edit, and no ADR files exist in either repo (the vault has 0001 to 0008 

## Decision
A `reflect` stage re-reads each landed landed document 24 hours and 7 days after landing, diffs it against the run's draft.md by block hash, classifies each change (wording, fact, structure, deletion). Wording and structure changes become candidate draft_contract rules in `context/<workflow>/proposals.md`, fact changes become mistakes.md rows, a section deleted three times stops being written. The Bot never edits a landed doc

## Consequences
- A run that crosses the never line in the decision is a contract or check failure, not a judgement call.
- Reversing this means changing engine stage 7, proposals.md per workflow together with every workflow that relies on it.
- Superseding this decision means a new ADR that names this one, never an edit here.

## Enforced by
engine stage 7, proposals.md per workflow

## Source row
`context/factory/decisions.md` row 1, 11/27/2026
