---
name: write-work-summary
description: Write a structured Work Summary for an engineer from supplied evidence (projects, artifacts, metrics). Use when a manager wants to turn a body of work into a Summary / Timeline / Task / Challenges / Action / Result / Artifacts document for a performance or calibration review. Does NOT fetch data; the caller provides the evidence.
disable-model-invocation: false
---

# Write Work Summary

Read [leadership-writing/house-rules.md](../leadership-writing/house-rules.md) and
[leadership-writing/rationalizations.md](../leadership-writing/rationalizations.md) first and apply every rule in them.

You turn a supplied body of engineering work into a clean, structured Work Summary
for a manager to use in a performance or calibration review.

You do **not** fetch data. The caller provides the evidence (projects, metrics,
artifact links) in `$ARGUMENTS` or in the surrounding context. If no evidence is
provided, ask for it rather than inventing any.

## Output discipline (read first)

- Return ONLY the finished Work Summary. The FIRST line of your output is the document
  title/summary table; the LAST line is the end of the document. No preamble, no
  "Here is", no "I don't need to fetch", no "Now I'll apply the fixes", no notes about
  your tools, evidence, or process anywhere in the output.
- Before returning, scan your output and DELETE any sentence that talks about writing
  the summary rather than being the summary. A leaked process sentence (and any em-dash
  inside it) is a release blocker.

## Writing rules (MUST follow, scan output before returning)

Read [leadership-writing/house-rules.md](../leadership-writing/house-rules.md) and apply EVERY rule in it:
no-em-dash, no-semicolons, correct-grammar, define-acronyms, date-format, active-voice, zombie-test, show-dont-tell,
quantify-impact, plain-headings, write-for-reader, logical-progression, no-superlatives, no-hedging (with its
banlist), story-not-bullets, honest-and-data-driven, and no-assumptions. That file is the single
source of truth for the voice; this skill applies it, it does not restate it. Write in the voice
of an experienced engineering manager and attribute work precisely to the individual, distinguishing
"led" from "contributed to". Scan the output for em-dashes and hedging words before returning.

Work-summary-specific rules (not covered by house rules):

- RATING SUPPRESSION. A Work Summary presents work; it does not state, name, or
  paraphrase any performance rating or tier. If the caller supplies a rating, use it
  only to calibrate tone, never print it.
- If a number is a projection or load-test figure (not a realized production result),
  say so explicitly rather than presenting it as a realized production metric.

## Structure

Follow the structure in [template.md](template.md) exactly.

Write in NARRATIVE PARAGRAPHS, not bullet points. Leadership reads a story better than
a bullet dump, so each field (Summary, Timeline, Task, Challenges, Action, Result) is
prose. The only list in the document is Artifacts, which is a short set of links, plus
the summary table at the top.

Open the document with a SUMMARY TABLE before any detail section. Columns: Category,
Project Title, Project Summary, Impact, Collaborators. Category is one of
`[Ambiguity / Technical Complexity]`, `[Scope and Influence]`, `[Impact]`,
`[Operational Excellence]`, or `Known Gaps and Honest Assessment`. Sort the table rows
by the candidate's impact, highest first, and write the detail sections below in that
same order.

For each project the labeled fields run Summary, Timeline, Task, Challenges, Action,
Result, Artifacts, in that order, each written as a paragraph (Artifacts excepted). The
Task/Action/Result fields map to Situation -> Behavior -> Impact: keep Task brief, make
Action (what THIS person did) the substance, and quantify Result. Cover every period the
evidence spans. Include a `Known Gaps and Honest Assessment` section that candidly names
what is unproven or still developing.

If the caller provides a calibration sample (an example finished work summary), read it
first and match its structure and tone. It is calibration only; never copy its content.

## Built-in validation loop (always, before returning)

A draft never leaves this skill unchecked. After the first full draft:

1. Read [validate-writing/SKILL.md](../validate-writing/SKILL.md) and
   [validate-writing/checklist.md](../validate-writing/checklist.md) and apply them to your own
   draft in **gate** mode, using the doc type `work-summary`.
2. Apply every quoted fix. Re-run the gate. Repeat until a pass reports zero blockers and zero
   majors, with a minimum of two passes and a maximum of five.
3. If blockers remain after the fifth pass, keep the draft and append a closing `**Known Gaps**`
   note listing each unresolved failure verbatim. Never hide an unresolved blocker and never
   resolve one by inventing a fact.
4. Return only the final draft (plus the Known Gaps note when required): no pass counts, no
   validation report, no process sentences. A caller that wants the report runs
   `/validate-writing` in evaluate mode separately.

Return only the finished Work Summary in markdown.

## Red flags (this genre)

Stop and re-read the rule when you see yourself producing any of these, on top of the shared list:

- an artifact named with no link when the evidence has one
- a result sentence with no number when the evidence has one
- two projects merged into one paragraph to save space
