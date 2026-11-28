---
title: 0020 Reflect scores the span the run wrote and one spelling of an emphasised link
date: 2026-11-28
area: factory
realm: public
kind: note
tags: [meta, decision, factory]
status: accepted
---
# 0020 Reflect scores the span the run wrote and one spelling of an emphasised link

## Context
Stage 7 (`vstack reflect`, ADR 0003) reads a landed document back 24 h and 7 d after landing, diffs it against the run's draft.md by block and turns the owner's edits into contract proposals, mistakes rows and deletion counts. The first scheduled pass over 51 landings on 11/28/2026 scored text the owner never touched:

- On a rolling document the draft side ran from the section heading to the end of the draft, so the per-document About block, which the run never writes, counted as two deletions in a scan workflow, and two rerecorded runs each brought deletions.json to 2 of the 3 that make the writer stop a section. The read-back side was whatever the worker wrote: a whole-document read-back of the daily people report (title, status table, the previous run's section, the About block) scored 15 structure changes and an owner edit ratio of 0.74 on a section the owner had not opened.
- The document store returns `**[x](u)**` as `[**x**](u)`. The block pairing key stripped the bold markers, so an untouched row paired, but a row with one real edit went on to classification, the proposed regex, the edit ratio and the filed before and after text with the raw spelling on each side. 20 of the 88 regexes proposed in that pass were the link markup of a task title, and 24 were auto-applied as `must_not_match` rules because the rerecorded run pairs repeated the same regex. The worker of that run reverted them by hand.

## Decision
- `reflect_span(draft, landed, heading)` fixes the span on both sides. Draft: from the section heading (the first `## ` line) to the end, cut before a same-level frame heading (`About`, `About this document`, the heading REFLECT_PROMPT already names as the end of a section). Read-back: from the heading whose text equals the section heading, cut before the first heading at the section's level or above whose text is a frame heading or no heading of the draft span (the previous run's section, the document title). Sub-headings the store demotes still match by text. `reflect-<age>.json` records `span` with the blocks cut on each side.
- `canon_markup(text)` rewrites an emphasised link with the markers inside the label (`[**x**](u)`, `[*x*](u)`, `[_x_](u)`, `[***x***](u)`, a label with brackets of its own) to the writers' marker-outside form, on both sides, before `reflect_diff` splits into blocks. The read-backs of 11/28/2026 held 420 bold links in the inside form and no italic or nested one, the italic and nested markers ride on the same regex.
- `vstack reflect --dry-run` prints the diff and what the filing would do (proposals, mistakes, deletions, the proposed regexes) and writes nothing: no `reflect-<age>.json`, no scorecard, no ledger line, no instance file.

## Consequences
- A reflect on a rolling document can take the whole document as its read-back, the worker's cut is no longer load-bearing.
- A same-level heading the owner adds inside a section ends the read-back span early and the rest of the section counts as deleted. Named as a limit in the code, to be lifted when a reflect shows one.
- The proposals, mistakes rows and auto-applied rules filed from the fix-wave patches of 11/27/2026 (dates given a year, glosses added to landed documents by a script, not by the owner) are a separate class: the engine cannot tell a script's patch from the owner's edit, the instance's ledger-follows-the-live-document decision covers it.
- Reversing this means changing `reflect_span`, `canon_markup`, the reflect-span and reflect-markup behaviours of `scripts/engine-selftest.py` and REFLECT_PROMPT together.
- Superseding this decision means a new ADR that names this one, never an edit here.

## Enforced by
`scripts/engine-selftest.py` reflect-span (a two-section fixture: whole-document read-back with the previous run's section and an owner-edited About gives 0 changes, no proposal, no deletion count, `span` 4 and 8) and reflect-markup (the exact pair alone is 0 changes, beside a real wording edit in the same row the proposed regex names the removed words and carries no marker, before and after agree on the spelling, `--dry-run` writes nothing), run by `scripts/check.sh engine`. Both were red on the engine before this commit (ratio 1.0, 6 structure and 1 mistakes row on the fixture, a regex built from the link markup).

## Source row
`decisions.md` row dated 2026-11-28 (reflect span and link spelling), and the private instance's `context/factory/decisions.md` row 91, 11/28/2026
