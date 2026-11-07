---
name: score-gate
description: Run a draft through validate-writing in a fixed loop (minimum two passes, maximum five, stop at zero blockers and zero majors, optional coverage bar) and return the final draft plus a one-line result. Use when an automation needs the gate as a separate, auditable step rather than relying on the writer skill's built-in loop. Does not fetch and does not publish.
---

# Score gate

Input: a draft, its doc type, and the thresholds (`min_passes`, `max_passes`, optional
`coverage_bar`). Output: the final draft and a result block.

1. Read `../validate-writing/SKILL.md`, `../validate-writing/checklist.md` and
   `../leadership-writing/house-rules.md`.
2. Pass 1: evaluate the draft in gate mode for the given doc type. Record every failure as
   `rule -> offending text -> fix`, with severity.
3. Apply the fixes. A fix may tighten wording, correct structure or label a claim
   `(unverified)`. A fix may never add a fact that is not in the evidence.
4. Pass 2 is mandatory even when pass 1 was clean.
5. Repeat until a pass shows zero blockers and zero majors (and coverage at or above
   `coverage_bar` when one is set). Stop at `max_passes`. If failures remain, append a
   `**Known Gaps**` note to the draft listing them verbatim.
6. Return the draft, then exactly one line:
   `GATE passes=<n> blockers=<n> majors=<n> minors=<n> coverage=<pct or n/a> status=<pass|known_gaps>`

Never return the per-pass reports unless asked; the caller stores the last one.
