---
title: 0018 A workflow switches a style rule key for its own drafts, and a bracket span carries its unit on both numbers
date: 2026-11-27
area: factory
realm: public
kind: note
status: accepted
---

# 0018 A workflow switches a style rule key for its own drafts, and a bracket span carries its unit on both numbers

## Context

The owner's fourth reading of one document produced two rulings about shapes rather than facts. First, `(2,083 to 626 µs)` leaves the first number bare: the unit belongs on both, `(2,083 µs to 626 µs)`, `(14% to 7%)`. Second, inside a document whose year a dated line has already established (a tracker row read on MM/DD/YYYY, or the first dated sentence), later dates read better as MM/DD. That second ruling conflicts with the house rule that every date is MM/DD/YYYY, and it is scoped: the owner asked for it in one kind's body, not everywhere. The only per-workflow switch the checker had was `style_exempt` (ADR 0015), which takes whole lines out of every check, too coarse for a rule that should still read those lines.

## Decision

- `bracket_span_format` gains `bracket-span-first-unit`: a span `A to B unit` inside brackets whose first number carries no unit token fires. Date windows and label ranges stay excluded as before.
- `scripts/style-check.py` gains `--option key=value`, which sets one rules JSON key for that run. A workflow lists its switches under `draft_contract.style_options` as `{key: value, why}`. `vstack check-run`, `vstack record` and `vstack style-check --workflow` pass them, `vstack check` requires the `why` and refuses a key that is not a rules key shape, the schema types the object, and the rendered prompt shows the switches to the writer.
- The first such key, `date_year_once`: when on, `date_without_year` stops counting MM/DD dates after the first line that carried a full MM/DD/YYYY. A short date above any full date still counts. Off by default, so the house rule is unchanged for every other kind.

`--selftest` covers the first-unit finding, the both-units pass, the switch on and off, and the short-date-first case.

## Alternatives

Loosening `date_without_year` in the instance rules JSON: every kind would lose the check. A `style_exempt` line pattern for dated sentences: those lines would lose every other check too. Writing the ruling as an instruction: the fourth review was the fourth time an instruction had not held.

## Consequences

A scoped owner ruling that conflicts with a house rule has a mechanism: a per-workflow key with a recorded why, visible in the workflow file, the prompt and `vstack check`. The conflict itself is the instance's to record and the owner's to settle; the engine carries both settings.
