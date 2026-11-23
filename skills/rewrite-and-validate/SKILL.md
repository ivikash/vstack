---
name: rewrite-and-validate
description: Rewrite supplied prose to follow the house rules, then self-validate it against the writing checklist and re-rewrite until it passes, at least two passes. Use when a caller has a draft and wants it tightened to the writing standard with proof it passed the gate. Preserves every fact and artifact; adds none.
disable-model-invocation: false
---

# Rewrite And Validate

Read [leadership-writing/house-rules.md](../leadership-writing/house-rules.md) and
[leadership-writing/rationalizations.md](../leadership-writing/rationalizations.md) first and apply every rule in them.

You rewrite a supplied passage to follow the house rules and then prove it clears the bar by
validating it, fixing what you find, and validating again. You run the
validate -> fix loop a **minimum of two times** and do not return the draft until a
validation pass finds zero blocker or major failures.

The writing standard is identical to [/rewrite](../rewrite/SKILL.md). Read and apply that
skill's writing rules verbatim. This skill adds the validation loop on top.

You do **not** fetch data. Every fact, metric, quote, link, ID, and date in your output
must already exist in the input. You add nothing. If a fact is missing you label it
"(unverified)", omit it, or record it under a closing **Known Gaps** note; you never fill
a gap with a plausible guess.

## Writing rules (MUST follow, identical to /rewrite)

Read [leadership-writing/house-rules.md](../leadership-writing/house-rules.md) and apply EVERY rule in it:
no-em-dash, no-semicolons, correct-grammar, define-acronyms, active-voice, zombie-test, show-dont-tell,
quantify-impact, plain-headings, write-for-reader, logical-progression, no-superlatives, no-hedging (with its
banlist), story-not-bullets, honest-and-data-driven, and no-assumptions. That file is the single
source of truth for the voice; this skill applies it, it does not restate it. The standard is
identical to [/rewrite](../rewrite/SKILL.md); this skill adds the validation loop on top.

You MAY change wording, voice, order, and tightness. You MAY NOT add a fact not in the
input, change a number, overstate scope, delete a balancing growth area /
reasons-not-to-promote point, or expose a rating the input did not already show.

## The loop (this is what this skill adds)

Run these steps in order. Do all of it silently; the caller sees only the final draft.

1. **Rewrite.** Produce a first rewrite following the writing rules above.
2. **Validate (pass 1).** Check the draft against every relevant rule below (the same
   checklist [/validate-writing](../validate-writing/checklist.md) enforces). If the
   validate-writing skill is available, invoke it in `gate` mode with the same doc type
   and the input as evidence; otherwise run the checks yourself. Record each failure as
   `rule -> exact offending text -> concrete fix` with a severity (blocker / major / minor).
3. **Fix.** Apply every fix from pass 1. Fixes may only tighten wording or correct a rule
   violation; a fix may never invent a fact to satisfy a rule. If a rule can only be
   satisfied with data the input lacks (for example a required metric), label it
   "(unverified)" or move it to Known Gaps rather than inventing.
4. **Validate (pass 2).** Re-check the fixed draft the same way. This second pass is
   mandatory even if pass 1 was clean: you always validate at least twice.
5. **Repeat** steps 3-4 until a validation pass reports zero blocker and zero major
   failures. Minor-only failures may remain if fixing them would require inventing data;
   note those under Known Gaps. Cap the loop at 5 total passes; if blockers or majors
   still remain at the cap, return the best draft and append a short
   `**Known Gaps**` note listing the unresolved failures verbatim. Never hide an
   unresolved blocker.

## Validation checklist (the gate each pass applies)

Each pass applies the checklist [/validate-writing](../validate-writing/checklist.md)
enforces, which is the operational form of every rule in
[leadership-writing/house-rules.md](../leadership-writing/house-rules.md). A pass fails a rule on at
least one concrete, locatable violation; do not invent violations to seem thorough. Group
failures by severity so the loop knows when to stop:

- **Integrity (blocker):** the house-rules honesty and no-em-dash rules, plus the
  document-integrity gates from the checklist (no fabricated metric / quote / link / ID /
  date; projections and test-only figures labeled, not shown as realized results;
  placeholders left as placeholders; no rating the input did not already show; scope
  attributed honestly).
- **Structure (blocker):** the document keeps the sections and order its type requires,
  and any required balancing section (talent-card Growth Areas, promo-doc reasons not to
  promote) is present, specific, and non-empty.
- **Writing quality (major):** the house-rules writing rules (active-voice, zombie-test,
  show-dont-tell, logical-progression, write-for-reader, no-hedging, no-superlatives,
  define-acronyms, story-not-bullets) all satisfied.
- **Polish (minor):** no section is a wall of text; specifics beat generic praise; the
  correct-grammar rule holds (no grammar, spelling, punctuation, agreement, or tense
  errors remain).

## Output discipline

- Return ONLY the final validated draft. No preamble, no validation report, no pass
  counts, no "Here is". The first line is the content; the last line is the end of it
  (or the `**Known Gaps**` note when one is required).
- Before returning, scan the output one last time for em-dashes and leaked process
  sentences and delete them.

Return only the final validated passage.

## Red flags (this genre)

Stop and re-read the rule when you see yourself producing any of these, on top of the shared list:

- returning after one pass
- a Known Gaps note dropped because the rewrite looked clean
- a validation report pasted into the returned prose
