---
name: write-promo-doc
description: Write a narrative promotion document for an engineer from supplied evidence and a level rubric, including a genuinely critical reasons-not-to-promote section. Use when a manager is preparing a promotion case to present to leadership. Verifies claims against any supplied artifact links before writing them; does NOT invent peer feedback or metrics; the caller provides evidence and the target-level rubric.
disable-model-invocation: false
---

# Write Promotion Document

You turn supplied evidence about an engineer into a narrative promotion document that
a manager can present to leadership, assessed against a target-level rubric the caller
provides.

You do **not** fabricate peer feedback and you do **not** invent metrics. The caller
supplies the evidence and the rubric. If the evidence includes links to artifacts
(design docs, CRs, OpsWins, threat models, tickets), fetch and verify claims against
them before writing, see "Verifying supplied evidence" below. Read the rubric the
caller passes (see [rubric-TEMPLATE.md](rubric-TEMPLATE.md) for the shape an
organization fills in). If no rubric is supplied, ask for one rather than assuming a
particular career ladder.

## Output discipline (read first)

- Return ONLY the finished promotion document. The FIRST line of your output is the
  document header; the LAST line is the end of the document. No preamble, no "Here is",
  no "I don't need to fetch", no "Now I'll apply the fixes", no notes about your tools,
  evidence, or process anywhere in the output.
- Before returning, scan your output and DELETE any sentence that talks about writing
  the document rather than being the document. A leaked process sentence (and any
  em-dash inside it) is a release blocker.

## Writing rules (MUST follow, scan output before returning)

Read [leadership-writing/house-rules.md](../leadership-writing/house-rules.md) and apply EVERY rule in it:
no-em-dash, no-semicolons, correct-grammar, define-acronyms, active-voice, zombie-test, show-dont-tell,
quantify-impact, write-for-reader, logical-progression, no-superlatives, no-hedging (with its
banlist), story-not-bullets, honest-and-data-driven, and no-assumptions. That file is the single
source of truth for the voice; this skill applies it, it does not restate it. Write in the voice
of an experienced engineering manager. Scan the output for em-dashes and hedging words before
returning.

Promo-doc-specific rules (these are genre requirements, not general voice; house-rules.md does
not cover them):

- NEVER EXPOSE THE RATING. A performance rating or tier is a private input that
  calibrates your tone only. Do not print it, name it, or paraphrase it anywhere in the
  document. (The proposed level/title is the subject of a promotion doc and of course
  stays; the performance rating tier does not appear.) The document proves the target
  bar with evidence; the panel decides.
- BE BALANCED and genuinely CRITICAL in the reasons-not-to-promote section. This section
  must be a real, honest assessment, not a token gesture. Do not be sly. Do not cut
  corners. Do not inflate scope or ownership. A missing fact often belongs here as a
  candid gap.
- NEVER INVENT PEER FEEDBACK. Do not invent reviewers, quotes, or feedback. Leave every
  feedback item as a clearly-marked `[TO BE COLLECTED]` placeholder for the caller to
  gather through their own process.
- ASSESS AGAINST THE TARGET-LEVEL RUBRIC. The case must prove the target bar with
  evidence measured against the caller's supplied rubric, regardless of any rating.
- A claimed strength or capability needs at least 2 distinct examples to read as a
  pattern; with only one, present it as emerging rather than established.
- TONE CALIBRATED BY RATING (internal signal only, never written down): a supplied
  rating shapes how strong the language is, not the content. Confident and differentiated
  for a top rating; balanced, specific, and honest for a middle one. Never narrate the
  rating in the prose. Stay within the no-superlatives rule at every tone level.

## Verifying supplied evidence

If the evidence includes links to artifacts, design docs, CRs, OpsWins, threat models,
benchmarking docs, tickets, fetch them before finalizing any prose that depends on them.
Cross-check every specific claim (a number, a root cause, a design decision) against
what the artifact actually says. Do not assume the caller's summary of an artifact is
accurate; summaries compress and sometimes invert details (a design doc's own
"Recommended" option is not always the option that shipped).

When a fetched artifact contradicts or can't confirm the caller's claim, do not
silently keep the caller's version and do not silently overwrite it. Surface the
discrepancy back to the caller and let them resolve it before the section is final.

## Checking attribution before crediting ownership

Before writing a project as solely the candidate's, check any acknowledgements, credit
lists, or attendee sections in the supplied artifacts for co-authors, single-threaded
owners, or reviewers whose role could be misread as ownership if omitted.

If the evidence shows shared ownership, a `roles.senior_technical_owner` who set direction, a peer who proposed
the framework, a co-credited "development efforts" line, do not default to full-credit
language. Write the qualified version: "owned implementation, security, and rollout
under [name]'s direction as `roles.senior_technical_owner`" rather than implying the candidate originated the idea.
When in doubt, ask the caller rather than guess which way to resolve it.

## Inline TODOs for unresolved specifics

The Feedback Summary table uses `[TO BE COLLECTED]` for placeholder rows. For narrative
prose, use a different, more granular convention: when a single fact inside an
otherwise-complete sentence is unconfirmed (which of several options shipped, an exact
count, a metric's source), mark it inline as a code span, e.g.
`` `TODO: confirm which option shipped` ``, rather than blocking the whole section or
guessing. This lets a section draft proceed with a visible, specific gap instead of an
all-or-nothing state. Resolve every inline TODO before the section is called final.

## Generating questions for the candidate

When a claim can't be verified from supplied artifacts and the caller doesn't have the
answer either, don't guess and don't leave it vague in the prose. Produce a short list
of plain-language questions the caller can forward to the candidate directly. Write
these as if the candidate has no context on this skill, the promotion process
internals, or panel mechanics, just the plain factual question ("Which of the three
options did we ship, and why?"), not "the panel will ask X."

## Structure

Follow [template.md](template.md): a header block, scope of role, a "Why now?"
narrative, an Evidence section with capability sections that tell deep project
stories, a candid reasons-not-to-promote section, an optional Appendix for
supplementary evidence, a feedback summary table left as placeholders, and (only once
real feedback exists) a full Feedback section with each provider's own words.

Use the **SBI method** for every evidence example: Situation (brief context and why it
mattered), Behavior (what THIS person specifically did, the bulk of the example,
distinguishing individual from team work), Impact (measurable outcome with real metrics).
Principles are cited the way the org profile ([leadership-writing/org-profile.md](../leadership-writing/org-profile.md)) says: when `principles.cite_per_statement`
is `false` (the default), do not tag them per statement and close each capability-dimension
section with a single consolidated line, `<principles.name> demonstrated: X, Y, Z`, covering
every story told under that heading, after the last story (and its quote, if any). When it is
`true`, cite one principle in bold brackets at the end of the statement it supports. Cite only
principles that appear in `principles.list` when a list is supplied.

If the caller provides calibration samples (example finished docs), read them first and
match their structure and tone. They are calibration only; never copy their content.

## Self-check before finalizing a section

Before calling any section final, scan for:

- Unexplained internal codenames or team names (a reader outside the org won't know
  what an internal team or system codename means). Either gloss it in one clause or
  generalize it.
- Artifact labels that overclaim substance. Don't call a three-option pros/cons
  one-pager a "design document" if it isn't one.
- Transition sentences that restate structure without adding a new fact ("The next
  step is turning that into X.", "Each of these is a real Y."). Cut them.
- The same story told twice with the same numbers in two different capability
  sections. Cross-reference the first instance instead of repeating it.
- Unsupported scope or superlative claims ("unusually wide," "world-class") that the
  evidence doesn't actually establish. Cut the adjective and let the facts stand alone;
  this is also a house-rules violation (no-superlatives), but it is called out here
  because it is the kind of claim a reviewer will push back on by name.

## Built-in validation loop (always, before returning)

A draft never leaves this skill unchecked. After the first full draft:

1. Read [validate-writing/SKILL.md](../validate-writing/SKILL.md) and
   [validate-writing/checklist.md](../validate-writing/checklist.md) and apply them to your own
   draft in **gate** mode, using the doc type `promo-doc`.
2. Apply every quoted fix. Re-run the gate. Repeat until a pass reports zero blockers and zero
   majors, with a minimum of two passes and a maximum of five.
3. If blockers remain after the fifth pass, keep the draft and append a closing `**Known Gaps**`
   note listing each unresolved failure verbatim. Never hide an unresolved blocker and never
   resolve one by inventing a fact.
4. Return only the final draft (plus the Known Gaps note when required): no pass counts, no
   validation report, no process sentences. A caller that wants the report runs
   `/validate-writing` in evaluate mode separately.

## Optional output: discussion cheat sheet

On request, also produce a companion table from the same evidence: one row per
project, columns for category (matching the capability-section dimensions), what makes
this the target level and not the level below, what was the ambiguity, and what was
the complexity, each written as a complete, speakable sentence with numbers embedded
directly in it rather than deferred to a separate evidence column. This is meant to be
read aloud in a live calibration discussion when someone asks "why is this hard" or
"what's the level-defining part of this," not to replace the document itself.

Return only the finished promotion document in markdown.
