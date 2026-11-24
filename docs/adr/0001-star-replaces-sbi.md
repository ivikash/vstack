# ADR 0001: STAR replaces SBI in the promotion document

Date: 2026-11-23. Status: accepted, amended the same day (D28, below).

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

## Amendment (D28, 2026-11-23)

The owner ruled that STAR is the skeleton the writer follows, never words the reader sees. The
bold `**Situation**`, `**Task**`, `**Action**` and `**Result**` lead-ins are removed from the
template, the skill, both fixtures and the lint. A story is the heading, the `**Headline**` line,
four unlabelled prose paragraphs in STAR order (the task paragraph ends with the `Ownership:`
sentence, the action paragraph with the altitude sentence) and the quote line. The lint counts
the paragraphs (`story-paragraphs`), fails a printed label (`no-star-labels`) and checks the
Ownership sentence (`ownership-line`). The order of the four paragraphs is a judgement rule,
`star-order` in checklist section H, which quotes the first sentence of the paragraph out of
place. The reasons-not-to-promote lead-ins (`**Pattern**` to `**Next**`) are unchanged. An
instance `draft_contract` that keyed on the four story lead-ins must drop those patterns.

Amended 2026-11-24 (round 4 shape, D59, D60, D62): the task paragraph no longer ends with an
`Ownership:` sentence, shared work is credited by function inside the paragraph and the ownership
audit's verdicts stay the gate, so the lint `ownership-line` is retired and a printed `Ownership:`
fails `no-star-labels`. The altitude sentence may be the counterfactual or a factual contrast naming
who else was engaged. The first paragraph opens with a bold `**Qn YYYY, <Project>:**` lead
(`story-lead`).
