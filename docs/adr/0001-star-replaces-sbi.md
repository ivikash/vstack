# ADR 0001: STAR replaces SBI in the promotion document

Date: 2026-11-23. Status: accepted.

## Context

The promotion writer told every story as Situation, Behavior, Impact. A senior reviewer rewrote
three stories in a real document into Situation, Task, Action, Result with a bold outcome line on
top, and marked the originals for opening with what the candidate did, for mixing the task into
the behaviour, and for burying the result. SBI has no place for who asked and what the candidate
owned, so ownership and the journey (what was tried, who was aligned) had nowhere to go and were
left out. The talent card keeps SBI, because a card has no room for a Task part.

## Decision

Every story in a promotion document is STAR under a bold Headline: `**Headline**` (outcome,
number, baseline), `**Situation**`, `**Task**` (with an `Ownership:` line), `**Action**` (the
journey, ending with the altitude sentence), `**Result**`, then one quote line. The lead-ins are
exact strings pinned in `skills/write-promo-doc/template.md` and checked by
`scripts/promo-lint.py`. `sbi-structure` in the checklist is scoped to talent-card and
work-summary.

## Consequences

- Hard to reverse: the lint, the checklist section H, both fixtures and any instance
  `draft_contract` key on the five lead-ins. Going back means changing all of them together.
- Surprising: two people-review genres now use two different story shapes on purpose.
- Trade-off accepted: a Task part adds 20 to 40 words per story against a 500-word cap. In return
  the ownership verdict and the journey have a fixed place a reviewer can find and a lint can
  count.
