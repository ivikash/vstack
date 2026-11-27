---
title: 0011 Four more countable style rules: hedges, marker form, comparatives, spans
date: 2026-11-27
area: factory
realm: public
kind: note
status: accepted
---

# 0011 Four more countable style rules: hedges, marker form, comparatives, spans

## Context

ADR 0010 put the countable half of a writing style in `scripts/style-check.py`. An independent read of 55 landed documents on 11/27/2026 found every one at 0 findings and still failed 15 of them on a shape the checker did not count: a hedge word ("likely") standing in for the unproven-claim marker. The same read listed markers with a reason inside their brackets, comparatives with no number behind them, and absolute numbers written before the relative change.

## Decision

Four more rules, each with its list or pattern in the instance's rules JSON and nothing specific in the engine.

- `hedge_words` -> `hedge-word`: a listed word or phrase outside a marker (`(TO BE ...)` or `[TO BE ...]`), quoted speech, code, a link label and a verbatim-title table cell is a finding.
- `marker_exact` -> `marker-not-exact`: a bracketed marker whose text is one of the listed markers followed by anything else inside the brackets is a finding. Another marker word is not read.
- `comparatives` -> `comparative-without-number`: a listed word in a prose sentence or a prose table cell that holds no digit is a finding. Sentences split as the sentence-length rule splits them, a list item is its own sentence, every link is one word, quoted speech is blanked.
- `numeric_span_needs_relative` -> `span-without-relative`: `from <number>[ unit] to <number>` whose sentence or cell holds none of the relative patterns before it is a finding. The default patterns are a percentage (`\d%`) and a multiplier (`\dx`), the instance may give its own list. A number followed by `/`, `:` or a letter is a date, a clock time or an identifier (`1Q`), not a span, and `from 2026 to 2027` is a period.

`--selftest` carries a silent case and a still-fires case for each rule, and all twelve rules fire on the bad text.

## Alternatives

Adding the hedge words to the weasel list: the weasel rule keeps prose link labels and does not blank markers, so the two rules differ in what they exempt, and a hedge inside a marker would count. A per-workflow regex in each instance contract: the state ADR 0010 replaced.

## Consequences

A draft that writes "likely", "(TO BE CONFIRMED which date)", "fewer calls" with no number or "fell from 16 min to 5 min" with no percentage first stops at `vstack check-run`. The comparative list is the instance's: a word such as "more" is as strict as the instance wants it, and the instance drops it from its JSON when it costs more than it catches.
