---
title: 0017 Explicit subjects, bare known terms, no date after an identifier link, a unit after every span
date: 2026-11-27
area: factory
realm: public
kind: note
status: accepted
---

# 0017 Explicit subjects, bare known terms, no date after an identifier link, a unit after every span

## Context

The owner's second reading of the same document (ADR 0016 holds the first) named the principles behind the rulings: the Zen of Python. Explicit over implicit (a sentence that opens with `It`, `This` or `The service` hides its subject), flat over nested (`([REV-4821](url), shipped 10/28/2026)` appends a date to a link that carries its own, `(2,083 to 626)` leaves the reader to guess the unit), one obvious way (an acronym everyone knows, `CD`, `ADC`, is written bare and never expanded, yet writers kept producing `continuous deployment (CD)`).

## Decision

- `explicit_subject` ({subjects}): a prose sentence outside a list item, a table cell, a heading or a caption that opens with a listed subject fires `implicit-subject`. The default list is `It`, `This`, `The service`, `The system`. Bullets are exempt because a list item's subject is its lead.
- `identifier_link_no_date` ({labels}): an identifier link (default labels `[A-Z]{1,6}-\d+`, `[A-Z]\d{6,}`) followed in the same bracket or clause by a `MM/DD/YYYY` date fires `link-then-date`.
- `bracket_span_format` gains `bracket-span-no-unit`: a span `A to B` inside brackets whose second number is followed by no unit token (`%`, `x`, a word) fires.
- The Known terms table (`known_terms_source`) gains a `Write as` column. `bare_terms()` returns {bare form: long forms} for every filled row, and `bare-term-expanded` fires on a long form in prose or on `BARE (expansion)`. The owner adds a term with one row and the bare form in that column, no code change.
- `skills/leadership-writing/house-rules.md` opens with a Principles table: each Zen line, what it means for leadership writing, and the rule or check that enforces it.

`--selftest` covers each finding on the bad text, silence on the good text, the list and cell exemptions, and `bare_terms()` reading the column.

## Alternatives

A prompt line per principle: the owner's point was that the principles explain the rules, so the table in house-rules.md maps them and the checks enforce them. Hard-coding `CD` and `ADC`: the owner will add more, so the table column is the mechanism.

## Consequences

A document that hides its subject, trails a date after a link, drops a unit or expands a bare term fails the gate with the text named. The instance decides the subjects, the label shapes and the bare terms, the engine stays org-neutral.
