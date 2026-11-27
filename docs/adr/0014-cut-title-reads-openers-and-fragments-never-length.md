---
title: 0014 cut-title reads openers and fragments, never length
date: 2026-11-27
area: factory
realm: public
kind: note
status: accepted
---

# 0014 cut-title reads openers and fragments, never length

Supersedes the length half of [0013](0013-cut-title-rule-and-link-labels-keep-their-spacing.md). The link-label exemption and the cell-by-cell code stripper of 0013 stand.

## Context

A fifth independent read of the landed documents on 11/27/2026 found four `cut-title` findings on titles that are whole and verbatim in their source: two bold roadmap titles of exactly 60 and 80 characters, a bold alarm name of exactly 60 characters, and a linked task title holding `<1hr`, where the `<` before a digit was read as an unclosed opener. The exact-length heuristic of 0013 was built for one generator's cap. That generator now refuses a cut title at its own source (its title cell is a bold link whose label is the whole title), so the heuristic had no true positive left to find and four false ones.

## Decision

- `cut_titles` (true) replaces `cut_title_lengths`. A title cell (wholly bold, wholly a link, or a bold link) is a finding, once per cell, only on a shape a whole title never has: the title ends in an open `[`, `(` or `<`, leaves a backtick unclosed, ends in a hyphen or a comma (a word or clause fragment), or holds a `<` followed by a letter with no `>` after it (`(TO BE COLLECTED: <ar`).
- A `<` followed by a digit, a space or `=` is a comparison (`last <1hr query`, `p99 < 50 ms`), never an opener.
- Length is never read. A whole title can be any length, and a generator that caps a title is refused at its own source, not by the checker.

`--selftest` carries the four quoted titles silent and six cut shapes firing.

## Alternatives

Keeping the length list and asking the writer to link every title of a listed length: that moves the false positive to the writer, who then edits a verbatim title's wrapper to satisfy a heuristic. A dictionary check for a mid-word ending: not countable, and a title legitimately ending in an abbreviation or an identifier would fail it.

## Consequences

A title cut at a cap that happens to end on a whole word (`... changes are active and`) is no longer a finding. The generator's own refusal and the writer's habit of copying a title whole are what prevent it. The rule catches the shapes a cut reliably leaves: an opener, a fragment marker, an unclosed code span.
