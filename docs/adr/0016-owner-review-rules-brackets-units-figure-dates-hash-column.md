---
title: 0016 Four countable rules from an owner's document review: bracket spans, quantity units, figure dates, the # column
date: 2026-11-27
area: factory
realm: public
kind: note
status: accepted
---

# 0016 Four countable rules from an owner's document review: bracket spans, quantity units, figure dates, the # column

## Context

The owner read one landed document end to end and returned eleven rulings. Seven were about that document's facts and wording and belong to the instance. Four were about shapes any document can carry and that a model repeats unless a check counts them:

- a span inside brackets written as prose, `(from about 2,080 to about 630 microseconds)`, where the owner reads `(~2,080 to ~630 µs)`
- a quantity verb with no unit, `pays 70% less`, where the reader cannot tell less time, less money or fewer calls
- a sentence that cites a figure and repeats the date the figure already draws as its change line, `fell 70% after the 11/07/2026 deployment (Figure 1)`
- a table whose first column is not `#`, so a reviewer cannot name a row

Each had been written as an instruction before. The instruction was ignored in six documents of the same kind on the same day.

## Decision

`scripts/style-check.py` gains four rules, each off until the instance's style rules JSON names it:

- `bracket_span_format` (true): inside `( ... )` on a prose line, `from <digit>` fires `bracket-span-from` and `about|around|roughly <digit>` fires `bracket-span-about`. Link labels and quoted text are not read.
- `quantity_unit` ({verbs, units}): a sentence holding a listed verb and a digit and none of the listed units fires `quantity-without-unit`. The verbs and units are the instance's, the engine ships none.
- `figure_sentence_no_date` (true or {exempt_prefixes}): a sentence holding `Figure <n>` and a `MM/DD/YYYY` date fires `figure-sentence-date`. Lines starting with the exempt prefixes (`*Figure`, `The window runs`, `Same window as` by default) are the caption and the window sentence, which keep the date.
- `table_first_header_hash` (true): the first header cell of every table is `#`, else `table-no-hash-column`.

`--selftest` covers each rule firing on the bad text and silent on the good text. A workflow that wants one of them without switching it on for every writer carries the same regex in `draft_contract.must_not_match`, which is how the instance landed the `#` column on five kinds whose other sibling kinds pin a header without it.

## Alternatives

Writing the rulings into the prompt again: that is where they were. One instance-only contract regex per kind: the first three are house style, not kind shape, and belong beside the other countable rules so every writer and the reflect step see them. Switching `table_first_header_hash` on in the shared JSON: it would fail every landed document of the kinds that pin a different header, so the instance chose the contract route for that one.

## Consequences

A document that repeats one of the four shapes fails the gate with the finding naming the text, and the reflect step can propose the rule to a kind that lacks it. The engine stays org-neutral: the unit list, the verb list and the exempt prefixes are the instance's words.
