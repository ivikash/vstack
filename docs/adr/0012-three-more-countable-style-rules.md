---
title: 0012 Three more countable style rules: the marker as a verb, unclosed brackets, a space before punctuation
date: 2026-11-27
area: factory
realm: public
kind: note
status: accepted
---

# 0012 Three more countable style rules: the marker as a verb, unclosed brackets, a space before punctuation

## Context

A third independent read of the landed documents on 11/27/2026 passed every one of them through the twelve rules of ADR 0010 and ADR 0011 at 0 findings and still failed seven on three shapes the checker did not count. The unproven-claim marker written as the sentence's verb ("every delta is TO BE CONFIRMED", "the root causes are (TO BE CONFIRMED)", "(organiser x, TO BE CONFIRMED still recurring)"). A title cut short inside a table cell, which left an opening bracket with no close and read as garbled text. A space before a colon in a calendar title copied into a cell.

## Decision

Three more rules. The lists stay in the instance's rules JSON, the engine holds the mechanism.

- `marker_not_after` -> `marker-as-predicate`: a bracketed `marker_exact` marker whose preceding word is on the list (the instance names "is", "are", "remains") is a finding, and so is a `marker_exact` text that stands outside its own brackets. The marker is a tag after a statement, the statement carries the verb. Link labels, quoted speech and verbatim-title cells are not read. Without `marker_not_after` the rule is off.
- `unclosed_brackets` -> `unclosed-bracket`: a table cell with more `[` than `]` or more `(` than `)` is a finding, once per cell. A closing bracket alone (`a) first, b) second`) and prose lines are not read.
- `space_before_punctuation` -> `space-before-punctuation`: a space between a word and one of the listed marks, followed by a space, a cell bar or the end of the line, is a finding in a cell and in prose. Code, URLs, quoted speech and the table alignment row are not read. A verbatim title is read: its words are someone else's, its spacing is the writer's to normalise.

`--selftest` carries a silent case and a still-fires case for each rule, and all fifteen rules fire on the bad text.

## Alternatives

A per-workflow contract regex for each shape: fixer 3's workflows already carry a space-before-punctuation regex, and the state ADR 0010 replaced was exactly that, one regex per workflow with no self-test. Reading the marker predicate through `marker-not-exact`: that rule reads only what is inside the brackets, the predicate shape is about what precedes them.

## Consequences

A writer that cuts a title to fit a cell, writes the marker as a verb or copies a calendar title with its stray space stops at `vstack check-run`. The predicate word list is the instance's, so a tense or verb it does not name passes until it adds the word.
