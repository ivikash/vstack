---
name: write-promo-doc
description: Write a narrative promotion document for an engineer from supplied evidence and a level rubric, including a genuinely critical reasons-not-to-promote section. Use when a manager is preparing a promotion case to present to leadership. Verifies claims against any supplied artifact links before writing them; does NOT invent peer feedback or metrics; the caller provides evidence, the rubric and the target level.
disable-model-invocation: false
---

# Write Promotion Document

Read [leadership-writing/house-rules.md](../leadership-writing/house-rules.md) and
[leadership-writing/rationalizations.md](../leadership-writing/rationalizations.md) first and apply every rule in them.

You turn supplied evidence about an engineer into a narrative promotion document that a manager
can present to leadership, assessed against a target-level rubric the caller provides.

You do **not** fabricate peer feedback and you do **not** invent metrics. The caller supplies the
evidence, the rubric and the target level. If the evidence includes links to artifacts (design
docs, code reviews, recognition posts, threat models, tickets), fetch and verify claims against
them before writing, see "Verifying supplied evidence" below.

## Inputs, and when to refuse

- **rubric** (required): the caller's ladder language, in the shape of
  [rubric-TEMPLATE.md](rubric-TEMPLATE.md). Its dimensions become the story criteria.
- **target_level** (required): the proposed level or title.
- **evidence**: the gathered facts, with artifact links.
- **why_now.order**: a ranked list of keys the caller sets per candidate (workflow
  `config.why_now.order`, default `["impact", "ambiguity", "recency"]`). It decides the order of
  the Why now wins. You never choose this order yourself.
- optional: a rating (tone only, never printed), calibration samples, the glossary override.

Without a rubric or without a target_level, do not write. Return one line naming the missing
input and stop. A document written against a guessed ladder is worse than no document.

## Output discipline (read first)

- Return ONLY the finished promotion document. The FIRST line of your output is the document
  header, the LAST line is `Sources: used ...; unavailable ...`. No preamble, no "Here is", no
  notes about your tools, evidence or process anywhere in the output.
- Before returning, scan your output and DELETE any sentence that talks about writing the
  document rather than being the document. A leaked process sentence is a release blocker.

## Step 1: readiness assessment (before any prose)

After reading the rubric, write the readiness table as a stage document (`gap-analysis.md` in a
run directory, `<draft>.readiness.md` beside a fixture), never as a section of the promotion
document. One row per rubric criterion, columns Criterion, Evidence (linked), Met / Partly /
Not met, Gap. End it with one verdict line:

`Readiness: Ready | Ready with gaps | Not ready`

- **Not ready**: do not write the document. Return the readiness table and the gap list, and say
  which evidence would change the verdict.
- **Ready with gaps**: write the document and name every gap in Best reasons not to promote.
- **Ready**: write the document. Reasons not to promote still name real gaps.

## Writing rules (MUST follow, scan output before returning)

Read [leadership-writing/house-rules.md](../leadership-writing/house-rules.md) and apply EVERY rule in it:
no-em-dash, no-semicolons, correct-grammar, define-acronyms, active-voice, zombie-test, show-dont-tell,
quantify-impact, write-for-reader, logical-progression, no-superlatives, no-hedging (with its
banlist), story-not-bullets, honest-and-data-driven, and no-assumptions. That file is the single
source of truth for the voice. Write in the voice of an experienced engineering manager.

Promo-doc-specific rules (genre requirements, not general voice):

- NEVER EXPOSE THE RATING. A performance rating or tier is a private input that calibrates your
  tone only. Do not print it, name it, or paraphrase it anywhere in the document. The proposed
  level is the subject of the document and stays. The document proves the target bar with
  evidence, the panel decides.
- BE BALANCED and genuinely CRITICAL in the reasons-not-to-promote section. A real assessment,
  not a token gesture. Do not inflate scope or ownership. A missing fact often belongs here as a
  candid gap.
- NEVER INVENT PEER FEEDBACK. No invented reviewers, quotes or feedback. Every missing feedback
  item is `(TO BE COLLECTED)`, every missing quote is `(TO BE COLLECTED: quote from <role>)`.
- ASSESS AGAINST THE TARGET-LEVEL RUBRIC. The case proves the target bar with evidence measured
  against the caller's rubric, regardless of any rating.
- A claimed strength needs at least 2 distinct examples to read as a pattern. With one, present
  it as emerging.
- TONE CALIBRATED BY RATING (internal signal only, never written down): a supplied rating shapes
  how strong the language is, not the content. Stay within no-superlatives at every tone level.

## Two markers, round brackets, identical everywhere

- `(TO BE COLLECTED)` or `(TO BE COLLECTED: <what>)`: the data does not exist yet (a quote not
  yet asked for, a feedback row, an adoption count nobody has measured).
- `(TO BE CONFIRMED)` at the end of the sentence: the data exists but the number or its source
  is unconfirmed.

No other form. No square brackets, no `TODO` code spans, no `TBD`, no `(unverified)` in this
genre. Resolve every marker you can before the section is called final, and leave the rest
visible: a marker is a fact about the evidence, not a flaw in the writing.

## Verifying supplied evidence

If the evidence includes links to artifacts, fetch them before finalising any prose that depends
on them. Cross-check every specific claim (a number, a root cause, a design decision) against
what the artifact says. Summaries compress and sometimes invert details (a design doc's own
"Recommended" option is not always the option that shipped). When a fetched artifact contradicts
or cannot confirm the caller's claim, do not silently keep either version. Surface the
discrepancy to the caller and mark the sentence `(TO BE CONFIRMED)` until they resolve it.

## Checking attribution before crediting ownership

Before writing a project as the candidate's, check acknowledgements, credit lists and attendee
sections in the supplied artifacts for co-authors, a `roles.senior_technical_owner` who set
direction, or reviewers whose role could be misread as ownership. Every story's task paragraph
(the second) ends with one `Ownership:` sentence naming what the candidate originated, executed
and operated. An
ownership verb in a story (led, owned, drove, architected, designed, end-to-end) must be backed by
that line and by the ownership audit's verdict (SUPPORTED, PARTIALLY SUPPORTED, UNSUPPORTED).
With shared ownership, write the qualified version: "executed the implementation and rollout
under <name>'s direction as `roles.senior_technical_owner`". When in doubt, ask the caller.

## Generating questions for the candidate

When a claim cannot be verified from supplied artifacts and the caller does not have the answer,
produce a short list of plain-language questions the caller can forward to the candidate ("Which
of the three options did we ship, and why?"), not "the panel will ask X". Mark the sentence in
the draft `(TO BE CONFIRMED)` meanwhile.

## Structure

Follow [template.md](template.md). Its "Shapes the lint keys on" block holds the exact strings
`scripts/promo-lint.py` checks. Two readers, two sections:

- **Why now?** is for a VP. Three bold wins in the order `why_now.order` gives, each carrying its
  story's Headline number, under 550 words, no unglossed internal codename.
- **Evidence** is for the panel. One `### <Project>: <Criterion>` story per project. STAR is the
  skeleton you follow, never words the reader sees: the only bold lead-in in a story is
  `**Headline**`. Four unlabelled prose paragraphs follow it, in this order:

  - **Headline**: the glossary term. Bold first line, the outcome, at least one number and the
    baseline or comparator it beat. Never the project name alone, never what the candidate did.
  - Paragraph 1, situation: the customer or stakeholder, what was broken or undefined, why it
    mattered now, and the criterion's marker (Ambiguity: what was undefined and from whose view.
    Problem Complexity: why the cause was not obvious or who else owned the code). Its last
    sentence is the candidate's first move, in an action verb.
  - Paragraph 2, task: what the candidate owned, who asked. Its last sentence is the
    `Ownership: originated ..., executed ..., operated ...` sentence, not a labelled line.
  - Paragraph 3, action: the journey, candidate-led action verbs: what was tried or ruled out, why
    no off-the-shelf path worked, who they reached out to or aligned, every artifact linked on its
    identifier at the claim it supports. Its last sentence is the altitude test: why a strong
    engineer one level below could not have done it.
  - Paragraph 4, result: dated, numbers, adoption, reuse by others.
  - One quote line, verbatim with name and role, or `(TO BE COLLECTED: quote from <role>)`.

  No `**Situation**`, `**Task**`, `**Action**` or `**Result**` label anywhere. The lint fails a
  printed label and a story with fewer than four paragraphs, the gate's `star-order` rule fails a
  paragraph that is out of order, quoting its first sentence.

A project appears in full once. Every other mention is one sentence with a cross-reference.
At most 2 full stories per criterion, further projects under it in one sentence each. A story
stays under 500 words, quote excluded. A shortened story keeps every link the longer one had.

Principles are cited the way the glossary ([leadership-writing/glossary.md](../leadership-writing/glossary.md))
says: when `principles.cite_per_statement` is `false` (the default), close each criterion with
one line `<principles.name> demonstrated: X, Y`. When `true`, one principle in bold brackets at
the end of the statement it supports. Cite only principles in `principles.list` when a list is
supplied.

**Best reasons not to promote**: five parts per reason with the template's lead-ins (Pattern with
two positive examples, Gap with one dated example of who pointed it out, Also seen by, Does not
block with evidence, Next with a plan). Every gap a feedback provider states is addressed by one
reason. An aspiration is not a reason. Headings in plain words. No reason may contradict a story
(a gap "does not propose initiatives" beside a story that says "proposed and drove" is a blocker).

If the caller provides calibration samples, read them first and match their structure and tone.
They are calibration only, never copy their content.

## Self-check before finalising a section

- Unexplained internal codenames or team names: gloss in one clause or generalise.
- Artifact labels that overclaim (a three-option one-pager is not a "design document").
- Transition sentences that restate structure without a new fact. Cut them.
- The same story with the same numbers under two headings. Cross-reference the first.
- Unsupported scope or superlative claims. Cut the adjective and let the facts stand.
- Run `scripts/promo-lint.py` on the draft when a shell is available. It prints one line per
  countable failure, longest story first.

## Built-in validation loop (always, before returning)

A draft never leaves this skill unchecked. After the first full draft:

1. Read [validate-writing/SKILL.md](../validate-writing/SKILL.md) and
   [validate-writing/checklist.md](../validate-writing/checklist.md) and apply them to your own
   draft in **gate** mode, using the doc type `promo-doc` (section H holds the promo-doc rules).
2. Apply every quoted fix. Re-run the gate. Repeat until a pass reports zero blockers and zero
   majors, with a minimum of two passes and a maximum of five.
3. If blockers remain after the fifth pass, keep the draft and append a closing `**Known Gaps**`
   note listing each unresolved failure verbatim. Never hide an unresolved blocker and never
   resolve one by inventing a fact.
4. Return only the final draft (plus the Known Gaps note when required): no pass counts, no
   validation report, no process sentences. A caller that wants the report runs
   `/validate-writing` in evaluate mode separately.

## Optional output: discussion cheat sheet

On request, also produce a companion table from the same evidence: one row per project, columns
for criterion, what makes this the target level and not the level below, what was the ambiguity,
what was the complexity, each a complete speakable sentence with its numbers embedded. For a live
calibration discussion, not a replacement for the document.

Return only the finished promotion document in markdown.

## Red flags (this genre)

Stop and re-read the rule when you see yourself producing any of these, on top of the shared list:

- a story that opens with what the candidate did instead of the Situation
- a Headline with no number, or a number with nothing it is compared against
- a reason not to promote with no named, dated example
- a story filed under a criterion its Situation does not carry the marker for
- a Reasons Not To Promote section that only restates strengths, or lists an aspiration as a gap
- a claim with no code review, document or ticket linked beside it
- a peer quote that is not verbatim from the evidence
- a Why now ordered by time when `why_now.order` does not start with recency
- a square bracket or `TODO` where a round-bracket marker belongs
- a promotion document written with no readiness verdict, or against a `Not ready` verdict
