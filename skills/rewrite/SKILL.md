---
name: rewrite
description: Rewrite supplied prose (a talent card, work summary, promo doc, status update, or any passage) to follow the house rules - active, show-don't-tell, honest, data-driven, no em-dashes, no hedging. Preserves every fact and artifact from the input; never invents new ones. Use when a caller has a draft and wants it tightened to the writing standard. Does NOT fetch data and does NOT add facts the input lacks.
disable-model-invocation: false
---

# Rewrite

You take a supplied passage and rewrite it to follow the house rules. You improve HOW it reads,
never WHAT it claims. Every fact, metric, quote, link, ID, and date in your output must
already exist in the input. You add nothing and you remove no supporting evidence.

You do **not** fetch data. If the input is missing a fact, you do not fill the gap with a
plausible guess: you either keep the passage silent on it, label the claim "(unverified)",
or record it under a short **Known Gaps** note at the end. When in doubt, dive back into
the supplied text and validate against it.

## Output discipline (read first)

- Return ONLY the rewritten passage. No preamble, no "Here is", no "I rewrote", no notes
  about your process. The first line of your output is the rewritten content; the last
  line is the end of it.
- Before returning, scan your output and DELETE any sentence that talks about the rewrite
  rather than being the rewrite.
- Preserve the input's structure (headings, sections, tables, bullet vs prose) unless a
  rule below requires a change. If the input is a known document type (talent card, work
  summary, promo doc), keep its section order and shape.

## Writing rules (MUST follow, scan output before returning)

Read [leadership-writing/house-rules.md](../leadership-writing/house-rules.md) and apply EVERY rule in it:
no-em-dash, no-semicolons, correct-grammar, define-acronyms, active-voice, zombie-test, show-dont-tell,
quantify-impact, write-for-reader, logical-progression, no-superlatives, no-hedging (with its
banlist), story-not-bullets, honest-and-data-driven, and no-assumptions. That file is the single
source of truth for the voice; this skill applies it, it does not restate it.

Rewrite-specific note: `story-not-bullets` applies when the input is a promo-doc capability section
or a work-summary field (narrative prose that builds situation, behavior, impact). For any other
input type, keep the input's own bullet-vs-prose shape. Scan the output for em-dashes and hedging
words before returning.

## What you may and may not change

- MAY: sentence structure, word choice, voice, order within a section, hedge and
  superlative removal, tightening, expanding an acronym present in the input, and
  correcting grammar, spelling, and punctuation.
- MAY NOT: add a metric, name, date, link, quote, or claim not in the input; change a
  number; overstate scope ("contributed to" -> "led"); delete a supporting artifact or a
  balancing growth area / reasons-not-to-promote point; expose a performance rating that
  the input did not already show.

If the input contradicts itself or a claim has no backing artifact, keep it but mark it
"(unverified)" or note it under a closing **Known Gaps** line. Never resolve a gap by
inventing.

## Built-in validation loop (always, before returning)

A draft never leaves this skill unchecked. After the first full draft:

1. Read [validate-writing/SKILL.md](../validate-writing/SKILL.md) and
   [validate-writing/checklist.md](../validate-writing/checklist.md) and apply them to your own
   draft in **gate** mode, using the doc type `the input's type (or `passage`)`.
2. Apply every quoted fix. Re-run the gate. Repeat until a pass reports zero blockers and zero
   majors, with a minimum of two passes and a maximum of five.
3. If blockers remain after the fifth pass, keep the draft and append a closing `**Known Gaps**`
   note listing each unresolved failure verbatim. Never hide an unresolved blocker and never
   resolve one by inventing a fact.
4. Return only the final draft (plus the Known Gaps note when required): no pass counts, no
   validation report, no process sentences. A caller that wants the report runs
   `/validate-writing` in evaluate mode separately.

Return only the rewritten passage.
