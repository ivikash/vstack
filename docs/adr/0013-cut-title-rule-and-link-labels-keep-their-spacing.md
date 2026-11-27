---
title: 0013 A cut title in a title cell is a finding, and a link label keeps its source's spacing
date: 2026-11-27
area: factory
realm: public
kind: note
status: accepted
---

# 0013 A cut title in a title cell is a finding, and a link label keeps its source's spacing

## Context

A fourth independent read of the landed documents on 11/27/2026 passed every one of them through the fifteen rules of ADR 0010 to 0012 at 0 findings and still failed the hub page on one shape: five decision titles in a table cut at the generator's cap, mid-word (`changes are active and relat`, `through the same mechanism as the ta`, `<ar`), one of them leaving a round bracket open inside a code span. The `unclosed-bracket` rule missed that one because the code stripper paired the cell's unclosed backtick with the backtick of the next cell's file name and hid the fragment between them. In the same pass a writer reported that `space-before-punctuation` fired inside a link label that quotes a task title verbatim (`Backfill Service :  Fix ...`), a title whose spacing belongs to the source the link points at.

## Decision

- `cut_title_lengths` -> `cut-title`: in a title cell (wholly bold, wholly a link, or a bold link) a title text that is exactly one of the listed lengths and ends in a letter or digit is a finding, and so is a title text that ends in an open `[`, `(` or `<` or leaves a `<` or a backtick unclosed. One finding per cell. A title of a listed length that ends in a closing bracket, a quote or a period is complete and does not count. Without `cut_title_lengths` the rule is off. Whether a title "ends mid-word" is not countable (a dictionary is not a rule), so the rule counts the two shapes a generator's cap leaves behind: the exact cap length and an opener with no close.
- `space-before-punctuation` no longer reads link labels. A label quotes its source's title verbatim and the link carries the reader to that source, so its spacing is the source's. A title cell that is not a link is still read: the writer copied it and owns its spacing.
- The code stripper never pairs backticks across a cell bar in a table row, so `unclosed-bracket` now counts the bracket a cut title leaves open inside a code span.

`--selftest` carries a silent case and a still-fires case for each change, and all sixteen rules fire on the bad text.

## Alternatives

Reading the generator's own guard as enough: the hub page generator refused an open bracket since ADR 0012 and still shipped the cut titles, because its guard had the same cross-cell backtick blind spot and no length check. Making the generator never cut (done, the title is the whole link label) without the rule: the next generator that cuts would ship the same shape. A dictionary check for a mid-word ending: not countable, and a title legitimately ending in an abbreviation would fail it.

## Consequences

A generator or writer that cuts a title to a cap stops at `vstack check-run` when the instance lists its caps. The list is the instance's, so a cap the instance does not name passes until it is added. A whole title that happens to be exactly a listed length and ends in a letter is a false positive the writer sees in the quote and can close with a period or a bracket, or the instance can drop that cap.
