# ADR 0002: two markers, round brackets, spelled exactly

Date: 2026-11-23. Status: accepted.

## Context

The promotion skill used three conventions for an unresolved fact: `[TO BE COLLECTED]` in the
feedback table, `` `TODO: ...` `` code spans inside prose, and the house-rules `(unverified)`
label. A reviewer's rewrites added a fourth, square-bracket placeholders such as `[date]` and
`[N accounts]`. Four forms cannot be counted, and a model picking any of them was never wrong, so
nothing failed when a draft shipped with twelve open placeholders.

## Decision

A promotion document has exactly two markers, both in round brackets: `(TO BE COLLECTED)` or
`(TO BE COLLECTED: <what>)` when the data does not exist yet, and `(TO BE CONFIRMED)` at the end
of a sentence whose number or source is unconfirmed. Every square-bracket form, `TODO`, `TBD`,
`TBC` and `(unverified)` fails `markers-consistent` in the lint and the checklist. The lint
reports the count of each marker so a reviewer sees how much is still open. Exec-update keeps
`(unverified)`, which is a different genre with a different reader.

## Consequences

- Hard to reverse: the two strings are pinned in the template, the lint, the checklist, the
  glossary and the fixtures. The talent card still uses `[TO BE COLLECTED: feedback text]`, so
  the two genres diverge on purpose.
- Surprising: round brackets were chosen over square because square brackets collide with
  markdown link syntax and with the reviewer's own placeholder habit, so a lint cannot tell a
  marker from a broken link.
- Trade-off accepted: a writer loses the granular `TODO: confirm which option shipped` note. The
  same information goes into `(TO BE COLLECTED: which option shipped)`, which the lint can count.
