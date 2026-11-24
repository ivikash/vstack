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
- **scope_file** (required, run config): the per-team scope file. It holds one "current level"
  paragraph and one "next level" paragraph per level pair, keyed by `target_level`. The next-level
  paragraph differs per pair (the step to a senior level adds delivery through others, more
  complex systems and more design than the step before it). `## Scope of Role` is copied from it.
- **candidate-facts** (required, per-candidate decisions file): the prior roles with their months,
  the date the current level started, the months in level, and the candidate's pronoun (she, he or
  they), which the lint's `candidate-subject-share` reads through `PROMO_LINT_CANDIDATE_PRONOUN`.
  See "Candidate facts".
- **story-ranking** (required, per-candidate decisions file): a table with columns project, rank,
  one line on why it matters, written by the owner. See "The owner ranks the stories".
- **evidence**: the gathered facts, with artifact links.
- **why_now.order**: a ranked list of keys the caller sets per candidate (workflow
  `config.why_now.order`, default `["impact", "ambiguity", "recency"]`). Since D53 it is a
  tie-breaker only, between projects the `story-ranking` table gives the same rank. You never
  choose an order yourself.
- optional: a rating (tone only, never printed), calibration samples, the glossary override.

Without a rubric or without a target_level, do not write. Return one line naming the missing
input and stop. A document written against a guessed ladder is worse than no document.

Without the scope file, without a level pair in it for `target_level`, or without the
`story-ranking` table, the run STOPS before any prose: write `questions.md` in the run directory
asking the owner for the missing input (for the ranking, list every candidate project with its
evidence strength: the numbers the evidence holds, the markers it would need, the code review
count) and write no draft. The next run reads the answers from the scope file and the decisions
file, never from the chat.

## Output discipline (read first)

- Return ONLY the finished promotion document. The FIRST line of your output is the document
  header, the LAST line is `Sources used: ... Sources unavailable: ...` (no semicolon). No preamble,
  no "Here is", no notes about your tools, evidence or process anywhere in the output.
- Before returning, scan your output and DELETE any sentence that talks about writing the
  document rather than being the document. A leaked process sentence is a release blocker: the
  lint rule `no-process-leak` fails the body on "earlier draft", "evidence pull", "reviewer of
  the", "readiness row", "in the order <x>, then", "told once below" and "working copy". The run
  brief, the frontmatter and the Sources line are exempt, nothing else is.

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
no-em-dash, no-semicolons, correct-grammar, define-acronyms, date-format, active-voice, zombie-test, show-dont-tell,
quantify-impact (relative figure first, absolutes in round brackets), plain-headings, write-for-reader, logical-progression, no-superlatives, no-hedging (with its
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

## Scope of Role is about the team and the level (scope-no-candidate)

`## Scope of Role` describes the team (what it owns, its scale) and what the PROPOSED level is
expected to be on this team. It never describes the candidate: no name, no alias, no hire or join
date, no "joined" or "hired", no prior team. Those facts live in the header block and in the
stories. The text is the two paragraphs the scope file holds for the level pair, copied, not
rewritten per candidate. The lint's `scope-no-candidate` fails the section on the candidate's name
(from the title and the Employee Name line, plus the alias the instance sets through
`PROMO_LINT_CANDIDATE_ALIAS`), a hire or join word, or a prior-team sentence.

## Candidate facts (candidate-facts, tenure-months)

The `candidate-facts` block in the per-candidate decisions file is an owner input: the prior roles
with their months, the date the current level started, the months in level, and the pronoun the
document uses for the candidate (the instance workflow passes it to the lint as
`PROMO_LINT_CANDIDATE_PRONOUN`, without it the lint takes the commonest of she, he, they in the
stories). A fact the block
does not hold prints as a TODO row for the owner in the run brief and as `(TO BE CONFIRMED)` at the
end of the sentence that needs it. It is never inferred from a people-directory page or a hire
date, and never invented. Two consequences:

- The review-count window and any "in N months as a <title>" clause run from the date the
  current level started, not from the hire date. A candidate hired at one level and promoted
  since has a shorter window than their tenure on the team.
- Tenure prints in months, never in days. The header's `Time in Current Level` is a month count,
  and so is every tenure figure in Why now. The lint's `tenure-months` fails a day count in either
  place.

## The owner ranks the stories (owner-ranked-stories)

Story importance is the owner's call, never the config order and never yours. The
`story-ranking` table in the per-candidate decisions file (project, rank, one line on why it
matters) decides the order of the Why now wins and which story is told first under each criterion.
`why_now.order` breaks ties between projects of equal rank, nothing more. When the table is
missing, stop and write `questions.md` as "Inputs, and when to refuse" says. The gate's
`owner-ranked-stories` rule fails a Why now order or a first story that departs from the table.

## Why now is one paragraph for the VP (why-now-one-paragraph, why-now-opener, why-now-no-list, why-now-rollup)

Write Why now last, from the finished stories, as ONE paragraph under 550 words with no bullet, no
sub-heading, no link, no criterion in brackets and no marker. Procedure:

1. Sentence one: the months in level from the `candidate-facts` block and the prior roles in one
   clause ("Dana has 26 months in level as an Engineer II after 14 months as an Engineer I on the
   same team"). Never the review counts, those open the review-process story.
2. Sentence two: how many initiatives, listed with each project name in bold, in the order the
   `story-ranking` table gives (D53, `why_now.order` breaks ties). You never pick the order.
3. One sentence per ranked project, three at most, each opening "On **Project**," with two or
   three of the candidate's verbs from that story's action paragraph and ending on the story's
   Headline number with its baseline, relative first (D51). Bold the number, not the sentence.
4. One sentence on operations (incidents root-caused, on-call scopes with a one-clause gloss
   each), one on people (who the candidate onboarded or mentored, with the number that landed).
5. One closing sentence that rolls up in counts (projects, services, teams, regions, months), not
   in trait words. "Across these 3 initiatives she shipped in 2 teams' codebases and 4 services in
   26 months", never "a consistent ability to".

A project with no story is not named in Why now, it goes to the Appendix (D14). No sentence names
more than three projects. The candidate is the grammatical subject of every sentence. The lint's
`why-now-one-paragraph` fails a second paragraph, a bullet, a sub-heading, a link, a bracketed
criterion, a bold span over six words with no digit, and a bold project name with no numbered
sentence. `why-now-opener` fails a first sentence with no month count, with a review count or with
a trait word. The gate's `why-now-no-list` and `why-now-rollup` read the rest.

## Show, don't tell (no-trait-words, obstacle-first, figure-has-verb, reuse-named, candidate-subject-share)

The house rule `show-dont-tell` lists the seven techniques, the house rule `no-superlatives` holds
the denylist of trait words and claim phrases, and the lint's `no-trait-words` reads that list from
`house-rules.md` at run time, so there is one list. In a story:

- Open the situation paragraph with the bold lead `**Qn YYYY, <Project>:**` (lint `story-lead`),
  then the obstacle in concrete nouns before the candidate's first verb: what did not exist, who
  else owned the code. The lint's `obstacle-first` warns when no absence construction precedes
  the candidate's first sentence.
- Open action sentences on the candidate's name or pronoun and a verb. The lint's
  `candidate-subject-share` warns when fewer than 60 percent of action sentences do, quoting the
  rest.
- Name the technique per component instead of an adjective about depth. Never deep, thorough,
  rigorous, robust, strong, consistent, impressive, instrumental, "ability to", "well beyond",
  "was responsible for", "owned quality", or demonstrat- followed by a trait. The lint fails each
  one, quoting the sentence. The D24 altitude form "A strong <level> would have" is the one
  exemption.
- Put each result figure in the sentence with the verb that produced it (`figure-has-verb`
  warns on a numbered sentence with no verb) and end the result paragraph on who uses the work now,
  a named team or builder, or on the exact sentence "No reuse by others is on record."
  (`reuse-named` warns otherwise, "stakeholders" is not a name).

## Relative first, dates MM/DD/YYYY, no markers in Why now (relative-first, date-format, why-now-no-markers)

Where a Headline or a Why now sentence carries both a relative figure (a percentage, an x-factor,
"N times") and the absolute numbers, the relative comes first and the absolutes follow in round
brackets: "cut credential-fetch failures by 99.7% (from 4,200 a day to 11 a day)". The house rule
`quantify-impact` carries the same line for every genre, the lint's `relative-first` fails the
other order and absolutes left outside the brackets.

Dates in body text are MM/DD/YYYY (house rule `date-format`). A YYYY-MM-DD anywhere outside a URL,
a link target or the frontmatter fails the lint's `date-format`. A quarter label (`Q3 2026`) in a
story lead is not a date and passes (D52 amended by D62).

Why now carries no marker. A figure the evidence does not hold is left out of Why now and told in
its story with `(TO BE CONFIRMED)` or `(TO BE COLLECTED: <what>)`. The lint's `why-now-no-markers`
fails a Why now sentence with either marker.

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
direction, or reviewers whose role could be misread as ownership. An ownership verb in a story
(led, owned, drove, architected, designed, end-to-end) must be backed by the ownership audit's
verdict (SUPPORTED, PARTIALLY SUPPORTED, UNSUPPORTED). No `Ownership:` sentence is printed (D59,
the printed line was a label the reader sees, the same class D28 removed). With shared ownership,
credit the other party by function in the same sentence as the candidate's act, in the task
paragraph: "shipped the Identity team's half with that team's senior owner as reviewer, who then
ran the rollout on their fleet". Never as a subtraction ("under <name>'s design, with the core
authored by another builder"), which belongs only in Best reasons not to promote (house rule
`credit-inline`). The ownership audit stays the gate (D21). When in doubt, ask the caller.

## Task-tracker dates and other builders' fixes (asana-date-role)

Every task-tracker date in a result paragraph is the task's completion date. Never the created
date, never the due date: a created date tells the reader when the work was noticed, a due date
when it was hoped for, and only the completion date tells them when the candidate delivered. When
a task's code fix is another builder's change, the story does not credit the candidate with the
fix. It gets a row in the ownership audit naming that builder and the verdict, and the sentence
says what the candidate did (found it, scoped it, reviewed it). The gate's `asana-date-role` rule
fails the sentence otherwise.

An ordering word between two tool-stamped events (before, after, then, once) is used only when the
stamps agree with the order the sentence claims. A comment stamped three minutes after the task's
completion does not support "verified before closing". When the stamps disagree or sit within
minutes of each other, the two events share one clause with no order ("verified in production the
day she closed the task"). The gate's `ordering-words-stamped` rule fails the sentence otherwise.

## Roles given to other people (role-words-held, asked-for-by-audited)

A role word on another person in a story (senior builder, principal engineer, product manager,
bar raiser) is a claim like any other. It is backed by a people-directory row in the evidence or
an artifact that names the role (an acknowledgement, a review record, a design-doc field).
Otherwise write the plain word "builder" or end the sentence `(TO BE CONFIRMED)`. The ownership
audit covers the candidate's verbs, not the roles the draft gives to others, so check these
separately. The lint warns on a story paragraph that carries a role word and no link and no
marker (`role-words-held`), the gate's rule of the same name decides.

The template's "asked for by <who>" clause in the task paragraph names the person or group behind
the ask. Every such subject gets one row in the ownership audit with the artifact that shows the
ask (a ticket, a chat message with its link, a design-doc requester field, an acknowledgement).
The lint checks that the clause exists, the gate's `asked-for-by-audited` rule checks that its
subject has the row.

## Counts that are a subset (subset-words)

When the source gives a count as part of a larger set (the service runs in 8 regions, the
automation covers 6), the sentence takes a subset word: "six of its regions", "six of the eight".
"The six regions" claims the six are the whole set and fails the gate's `subset-words` rule.

## Reasons not to promote: what a Pattern may cite (pattern-cites-unmarked)

A reason's Pattern names two positive examples. It may cite a story as an example of a trait
(initiative, finding work unprompted, teaching) only when that story asserts the trait in a
sentence with no marker. A story that marks the trait `(TO BE CONFIRMED)` or `(TO BE COLLECTED)`
is not yet an example of it, and the Pattern leans on a claim the document itself has not made.
The document-wide `rntp-contradiction` rule covers the explicit claim, this one covers the lean.

## Before the sink: warnings ruled, parked findings logged (marker-warnings-ruled, parked-findings-logged)

The lint's warnings are not noise the writer may carry past the gate. Before the document is
written to its sink, every `marker-direction` warning is ruled on by the caller: the sentence takes
`(TO BE COLLECTED: <artifact>)` with the artifact named, or the clause is cut, or the caller's
ruling to keep it is recorded in the candidate's decisions file. The gate's `marker-warnings-ruled`
rule blocks a sink write with an unruled warning.

Every reviewer finding the caller parks (a story placement, a wording the caller wants to keep, a
figure not worth chasing) gets one row in the candidate's decisions file with the date, the
finding, where it was raised and the reviewer's advice, so the next round does not re-open it. The
run brief names the row. The gate's `parked-findings-logged` rule reads the decisions file.

## Provider gaps when feedback is not in yet (provider-gap-fallback)

When the Feedback Summary rows are still `(TO BE COLLECTED)`, the provider gaps are the rows of
the gap analysis stage document's "Provider gaps first" table (the gaps the manager already knows
providers will raise). Address every row there with one reason not to promote, the same way a real
Feedback section would be addressed. The gate's `provider-gap-fallback` rule reads that table when
the Feedback section is a placeholder.

## Copy check (every file holding another person's prose)

Before the gate, run `scripts/promo-copycheck.py <draft> <source>...` against every file you read
that holds another person's words: the feedback file, reviewer rewrites, calibration samples, a
previous version by another author. It lists every run of 8 or more shared words by source. A
run in your own prose is rewritten in your words or moved into a quote line with its name and
role. The quote lines and the `## Feedback` section are exempt because they are verbatim by rule.
Pass `--evidence-dir <dir>` pointing at the gathered evidence: a run that also appears in a file
there prints as `source-held`, which means the fact was readable from a primary source and the run
is recorded as such rather than left for the reader to judge. A source-held run is still a run, so
rewrite it unless it is an identifier or product-name list.

## Generating questions for the candidate

When a claim cannot be verified from supplied artifacts and the caller does not have the answer,
produce a short list of plain-language questions the caller can forward to the candidate ("Which
of the three options did we ship, and why?"), not "the panel will ask X". Mark the sentence in
the draft `(TO BE CONFIRMED)` meanwhile.

## Structure

Follow [template.md](template.md). Its "Shapes the lint keys on" block holds the exact strings
`scripts/promo-lint.py` checks. Two readers, two sections:

- **Why now?** is for a VP. One paragraph: months in level first, the initiatives in bold in the
  owner's `story-ranking` order (`why_now.order` breaks ties), one "On **Project**," sentence per
  ranked project ending on its Headline number with its baseline, then operations, people and a
  roll-up in counts. Under 550 words, no bullet, no link, no bracketed criterion, no marker, no
  trait word, no unglossed internal codename. See "Why now is one paragraph for the VP".
- **Evidence** is for the panel. One `### <Project>: <Criterion>` story per project. STAR is the
  skeleton you follow, never words the reader sees: the only bold lead-in in a story is
  `**Headline**`. Four unlabelled prose paragraphs follow it, in this order:

  - **Headline**: the glossary term. Bold first line, the outcome, at least one number and the
    baseline or comparator it beat. Never the project name alone, never what the candidate did.
  - Paragraph 1, situation: opens with the bold lead `**Qn YYYY, <Project>:**`, then the obstacle
    in concrete nouns before the candidate's first verb (what did not exist, who else owned the
    code) and the criterion's marker (Ambiguity: what was undefined and from whose view. Problem
    Complexity: why the cause was not obvious or who else owned the code). Its last sentence is the
    candidate's first move, in an action verb.
  - Paragraph 2, task: what the candidate owned, who handed it over and why, stated as a fact of
    the project, shared work credited by function in the same sentence. No `Ownership:` sentence.
  - Paragraph 3, action: candidate-led sentences, name or pronoun first and a verb second: the
    fork with the cost of the fast option, why no off-the-shelf path worked, who they reached out to
    or aligned, the technique per component, every artifact linked on its identifier at the claim
    it supports. The lint's `journey-countable` fails a paragraph with none of those verbs and no
    other person named, and `one-cr-once` fails a review id that already sits in another story's
    action paragraph. Its last sentence is the altitude sentence in either form: the D24
    counterfactual, or a factual contrast naming who else was engaged and what the candidate alone
    did (D60).
  - Paragraph 4, result: each figure beside the verb that produced it, dated, relative first,
    ending on who uses the work now or on "No reuse by others is on record."
  - One quote line, verbatim with name and role, or `(TO BE COLLECTED: quote from <role>)`.

  No `**Situation**`, `**Task**`, `**Action**` or `**Result**` label anywhere. The lint fails a
  printed label and a story with fewer than four paragraphs, the gate's `star-order` rule fails a
  paragraph that is out of order, quoting its first sentence.

A project appears in full once. Every other mention is one sentence with a cross-reference.
At most 2 full stories per criterion, further projects under it in one sentence each. A story
stays under 500 words, quote excluded. A shortened story keeps every link the longer one had.

Principles are cited the way the glossary ([leadership-writing/glossary.md](../leadership-writing/glossary.md))
says: `principles.print_line` is `false` by default (D61), so no principles line is printed in the
manager's stories, the providers' bracketed tags in Feedback carry them. When `print_line` is
`true` and `principles.cite_per_statement` is `false`, close each criterion with one line
`<principles.name> demonstrated: X, Y`. When `cite_per_statement` is `true`, one principle in bold
brackets at the end of the statement it supports. Cite only principles in `principles.list` when a
list is supplied.

**Best reasons not to promote**: one intro paragraph that names the themes and counts how many
providers raised each (the lint's `rntp-intro-counts` warns without it), then five parts per reason with the template's lead-ins (Pattern with
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
- a Why now ordered by time, or by anything other than the owner's `story-ranking` table
- a Why now of more than one paragraph, a bold sentence standing alone as a win, a criterion in
  brackets, a review count in the first sentence, or a closing sentence that names a pattern in
  trait words instead of counts
- a story whose first paragraph does not open `**Qn YYYY, <Project>:**`, or a printed
  `Ownership:` sentence
- deep, thorough, rigorous, robust, strong, consistent, impressive, "ability to", "was responsible
  for", or demonstrat- plus a trait anywhere in your own prose
- a result paragraph that ends on "stakeholders" or on nothing about who uses the work now
- shared work written as a subtraction ("under X's design") in a story instead of a credit by
  function in the same sentence
- a Why now sentence carrying `(TO BE CONFIRMED)` or `(TO BE COLLECTED ...)`
- a Scope of Role that names the candidate, their hire date or their previous team
- a tenure in days, or a review window counted from the hire date instead of the level start
- a sentence that gives the absolute numbers first and the percentage after them
- a date written year first in body text
- a square bracket or `TODO` where a round-bracket marker belongs
- a promotion document written with no readiness verdict, or against a `Not ready` verdict
- a sentence about the writing (an earlier draft, the evidence pull, what is told once below)
- a task-tracker created or due date standing in for a completion date
- the same code review id in two stories' action paragraphs
- a link you could not fetch in a sentence without `(TO BE CONFIRMED)`, or `(TO BE CONFIRMED)` on a
  sentence that names no artifact (that is `(TO BE COLLECTED: <artifact>)`)
- a heading with leverage, play, strategic, proactive, cultivating, synergy, holistic or paradigm
- an 8-word run copied from a provider's or reviewer's text outside a quote line
