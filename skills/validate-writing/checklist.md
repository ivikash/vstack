# Writing Checklist

The rules a leadership-writing document must satisfy. The validator checks each one and fails the
document on any real violation. Edit this file to change "the way it should be written"; the
validator enforces whatever is here.

Document types: `talent-card`, `work-summary`, `promo-doc` (people-review), and `exec-update`
(leadership status update). Rules note which type(s) they apply to; a rule with no type note
applies to all. The generic voice rules are shared across every type and live in
[leadership-writing/house-rules.md](../leadership-writing/house-rules.md) - read that file and enforce it in
addition to the type-specific rules here.

Severity key: **blocker** = unfit to share, **major** = weakens the doc, **minor** = polish.

## A. Integrity (blockers)

- **no-em-dash**: No em-dash characters anywhere. Use commas, periods, parentheses, or a
  spaced hyphen " - " instead.
- **no-semicolons**: No semicolons anywhere. Split the clauses into two sentences, or join
  them with a comma and a conjunction.
- **correct-grammar**: No grammar, spelling, punctuation, subject-verb agreement, verb
  tense, or article errors. Sentences are complete, modifiers sit next to what they modify,
  and items in a list keep parallel structure.
- **date-format**: Dates in body text are MM/DD/YYYY. A YYYY-MM-DD outside a URL, a link target
  or the frontmatter is a violation in every genre (the promo-doc lint fails it as `date-format`).
- **rating-placement** (doc-type specific):
  - talent-card: the rating lives in the Background Rating / Rating History tables,
    exactly as supplied by the caller. Do NOT invent or alter rating numbers. The Rating
    Rationale (section 2) argues the case in the language of the glossary's principles and need not
    restate the rating letters, but stating them is not a violation for a talent card.
  - work-summary and promo-doc: no performance rating or tier is printed, named, or
    paraphrased. Fail on a header rating field, a "Rating" section, a tier name, or a
    paraphrase that stands in for a rating ("a top performer", "exceeds at this level").
    The proposed level/title in a promotion doc is allowed; a performance rating tier is not.
- **no-fabrication / no-assumptions**: Every metric, quote, link, ID, and date must be
  traceable to the supplied evidence. Flag anything invented, unsupported, or that reads
  like a plausible-sounding assumption filling a gap. An unverifiable claim must be
  labeled "(unverified)" or recorded as a gap, never asserted as fact.
- **label-projected**: Any projection or test-only figure must be labeled as such, not
  presented as a realized production result.
- **no-invented-feedback**: Peer or stakeholder feedback must be left as a clearly marked
  placeholder (talent-card: `[TO BE COLLECTED: feedback text]`, promo-doc: `(TO BE COLLECTED)`
  in round brackets, see section H markers-consistent). Named reviewers or quoted feedback that
  was not supplied is a blocker.
- **attribution-honest**: Distinguish "led" from "contributed to". Do not overstate scope
  or ownership beyond what the evidence supports.

## B. Structure (blockers / major)

- **required-sections** (blocker): All sections required by the document's template are
  present and in the specified order.
  - talent-card: numbered house format, in order: 1. Background (with Rating and Rating
    History tables), 2. Rating Rationale / Key Talking Points, 3. Key Deliverables &
    Achievements, 4. Code Contributions, 5. Appendix. Section 2 is PROSE structured as
    EXACTLY FOUR paragraphs in this fixed order: (1) major delivery, (2) operational
    excellence contribution, (3) Growth Areas (paragraph begins `**Growth Areas:**`),
    (4) Manager Support (paragraph begins `**Manager Support:**`, first person).
    Paragraphs 1-2 are principle-anchored. Fail if section 2 has fewer or more than four
    paragraphs, is out of order, adds an orienting preamble sentence before paragraph 1,
    or bullets the section. Section 3 is BULLETED and grouped by theme (optional Shoutouts,
    then Key Deliverables under bold theme headers). Sections 1, 4, and 5 are
    caller-supplied; the writer fills 2 and 3. Growth Areas and Manager Support live inside
    section 2 as paragraphs 3 and 4, not as separate numbered sections.
  - work-summary: a Summary table at the very top (columns Category, Project Title,
    Project Summary, Impact, Collaborators; sorted by impact, highest first), then the
    detail sections in that same order, then a Known Gaps and Honest Assessment section.
    Each project has Summary, Timeline, Task, Challenges, Action, Result, Artifacts, in
    that order.
  - promo-doc: Header block, `## Scope of Role`, `## Why now?`, `## Evidence` with one
    `### <Project>: <Criterion>` story per project, `## Best reasons not to promote`,
    `## Feedback Summary`, optional `## Appendix` and `## Feedback`, `Sources used: ... Sources
    unavailable: ...` as the last line. Exact strings in write-promo-doc/template.md.
- **balance** (blocker for talent-card and promo-doc): Includes genuine growth areas
  (talent card) or a candid, specific "reasons not to promote" (promo doc). A section that
  is empty, hand-wavy, or purely positive fails this rule.

## C. Writing quality (major)

All the generic writing-voice rules live in [leadership-writing/house-rules.md](../leadership-writing/house-rules.md):
claim-has-artifact (as honest-and-data-driven), quantify-impact, no-superlatives (with its banlist, trait words and claim phrases), write-for-reader,
logical-progression, show-dont-tell (with its seven techniques), credit-inline, reuse-named, active-voice, zombie-test, no-hedging (with its banlist),
define-acronyms, date-format, link-artifacts, plain-headings (and quantify-impact's relative-first line), and story-not-bullets. Read that file and enforce every rule in it
as a checker (fail a real violation). This section adds only the people-review-specific quality
rules that are NOT generic voice:

- **no-trait-words** (major, every genre): no word from the house `no-superlatives` banlist or trait
  words, and no claim phrase from the same line, in the author's prose. The list lives in the house
  rule and nowhere else. A quote attributed to a named provider and a verbatim feedback section are
  exempt. The promo-doc lint fails the words it can match, this rule reads the paraphrased tells the
  list misses ("went the extra mile", "left no stone unturned"). Prints: `no-trait-words -> "<word
  or phrase>" in "<sentence>" -> replace with the fact that shows it (the obstacle, the technique,
  the figure with its verb)`.
- **credit-inline** (major, every genre): shared work is credited by function in the same sentence
  as the actor's act, never as a subtraction in the narrative ("under X's design", "with the core
  authored by Y", "executed inside a goal someone else framed"). The subtraction belongs only in a
  reasons-not-to-promote or gaps section. Prints: `credit-inline -> "<sentence>" subtracts -> name
  who did what in the actor's sentence ("with the security reviewers", "across three teams")`.

- **link-artifacts**: When the evidence supplies a URL for a referenced artifact (code review,
  design doc, ticket, dashboard, recognition post), the reference is a descriptive inline
  hyperlink, not a bare artifact name or a raw pasted URL. Flag a named artifact that has a URL in
  the evidence but is left unlinked, and flag a raw `https://...` dropped into prose instead of
  linked text. Do NOT flag a reference whose URL is absent from the evidence (linking it would be
  fabrication), and never treat a missing link as license to invent one.

- **two-examples**: A claimed strength or growth area needs at least 2 distinct examples to
  count as a pattern. One example is "emerging" or "one-time," not a demonstrated strength;
  label it that way rather than overstating. (Applies to talent-card strengths/growth and
  promo-doc capability claims.)
- **sbi-structure** (talent-card, work-summary): Each evidence example should map to Situation ->
  Behavior -> Impact, with Behavior (what THIS person specifically did) as the bulk and Situation
  kept short. Flag examples that are all context and no distinct individual behavior. A promo-doc
  uses STAR instead (section H, star-situation and journey-in-action).
- **principle-citation** (promo-doc): follow `principles.print_line` and
  `principles.cite_per_statement` in the glossary. `print_line` `false` (default, D61): no
  principles line in the manager's stories, the providers' quotes carry the principles. `print_line`
  `true` and `cite_per_statement` `false`: one roll-up line `<principles.name> demonstrated: X, Y, Z`
  closes each capability section and no per-statement tags appear. `true`: one principle in bold brackets at
  the end of the statement it supports, e.g. `[**principles.example_1**]`, never stacked, never
  forced onto every sentence. Fail a principle that is not in `principles.list` when a list exists. Weave role-guideline "Moving to"
  phrases as short *italic* fragments, never quoted verbatim.

## D. Length and tone (minor)

- **section-length**: No single section is a wall of text. Talent card stays scannable;
  work-summary fields are tight; promo-doc paragraphs are focused, not padded. Rough promo-doc
  guidance (advisory, by target level): Scope of Role <= 500 words; Introduction 100-200;
  each evidence example 250-1000; 3-5 examples for a `levels.mid` case, 4-6 for `levels.senior` and above (glossary).
- **specific-over-generic**: Prefer concrete specifics over generic praise
  ("strong engineer", "great team player") that could apply to anyone.

## E. Failure patterns (flag if the whole document fits one)

Beyond line-level rules, flag the document if it matches a known failure shape:

| Pattern | Tell | Fix |
|---|---|---|
| **resume-doc** | Lists accomplishments with no Situation/Behavior/Impact (or STAR in a promo-doc) | Rewrite each example as SBI (STAR for a promo-doc), show complexity and individual action |
| **hero-doc** | Superlatives everywhere ("exceptional", "world-class"); no metrics | Cut every superlative (see no-superlatives); let numbers carry it; this reads as biased |
| **team-doc** | "We" throughout; the individual is invisible | Use the person's actions; specify what THEY did vs the team |
| **shallow-breadth** | Many thin examples, none deep | Consolidate to fewer, fuller examples that show sustained depth |
| **soft-gaps** | Growth / reasons-not-to-promote dismissed or absent | Name real gaps with specific examples and a coaching plan |
| **feedback-mismatch** | Stated gaps contradict the feedback themes provided | Align the gap narrative with the actual feedback signals |

## F. Reviewer bias self-check (note any the draft may exhibit)

- **recency**: over-weighting recent events; expect dated examples across the full period.
- **halo / horn**: one trait coloring everything; each strength/gap should stand on its own
  evidence.
- **similarity**: praising style/approach that mirrors the author rather than outcomes.
- **central-tendency**: hedged, middle-of-the-road language that avoids a real judgment.
- **confirmation**: only evidence that confirms a pre-picked conclusion; look for counter-evidence.

Note any suspected bias as a flag (not necessarily a failure) so the manager can check it.
(Sections E and F apply to people-review documents.)

## G. Exec-update rules (`exec-update` only)

For a leadership status update, in addition to the shared house rules, enforce:

- **claim-cites-artifact** (major): every significant status claim is backed by a concrete artifact
  in the evidence (a metric, ticket, review, source-document cell, message, or dated meeting note).
  A bare claim with no artifact fails.
- **label-projected** (blocker): a projection, load-test, or target figure is labeled as such, not
  presented as a realized result.
- **green-by-when-red** (blocker): every RED or AT RISK section carries a `Green by: mm/dd` recovery
  date (or `Green by: (unverified)` with a matching Known Gap). GREEN / ON TRACK sections must NOT
  carry the line.
- **green-by-future** (blocker): a `Green by` date is strictly after the report date. A date on or
  before today is a blocker; the correct value is `Green by: (unverified)` with a Known Gap noting
  the slip.
- **date-has-justification** (blocker): every `Green by` date, and every projected/new date that
  differs from the source's original, is followed by a "(because ...)" reason grounded in evidence.
- **top-risks-present** (blocker): a consolidated Top Risks section is present (or an explicit
  "none open").
- **section-coverage** (major): every section the caller listed appears as a block, in order, with
  no invented sections.
- **date-conflict-surfaced** (major): when two sources disagree, the more recent dated source is
  used and the conflict is noted under Known Gaps.

## H. Promo-doc rules (`promo-doc` only)

Judgement rules the gate applies to a promotion document, on top of sections A to F. The
countable twins live in `scripts/promo-lint.py` (word caps, four paragraphs per story and no STAR
label printed, the quarter lead, a number in the Headline, one quote line per story, exact marker
spelling, links per story, bare identifiers, the one-paragraph Why now, the trait-word denylist
read from the house rules) and run before the gate. Each rule below names the quoted-failure
form the gate prints, in the shape `[severity] rule -> offending -> fix`. Vocabulary: the Headline
is the bold first line of a story (glossary), the criterion is a dimension of the caller's rubric.
A story's four prose paragraphs carry no labels (owner decision D28), so "situation", "task",
"action" and "result" below name the first, second, third and fourth paragraph after the Headline.

- **readiness-first** (blocker): the run holds a readiness table (one row per rubric criterion,
  columns Criterion, Evidence, Met / Partly / Not met, Gap) ending `Readiness: Ready | Ready with
  gaps | Not ready`, and no document exists for a `Not ready` verdict. Prints: `readiness-first ->
  no readiness verdict in the run (or: verdict Not ready at "<line>") -> write gap-analysis.md
  first, return the table and gap list instead of a document when Not ready`.
- **star-situation** (blocker): a story's first two sentences after the Headline name the customer
  or stakeholder, the ask, and what was broken or undefined. Fail when the first sentence's
  grammatical subject is the candidate. Prints: `star-situation -> "<first sentence>" -> open with
  who needed what and what was undefined, move the candidate's action to the action paragraph`.
- **star-order** (blocker): the four paragraphs between the Headline and the quote read as
  situation (the obstacle in concrete nouns, opening with the bold quarter lead), task (what the
  candidate owned, who handed it over, shared work credited by function in the same sentence),
  action (the journey, ending with the altitude sentence) and result (dated, with numbers, ending
  on who uses it now), in that order and with no printed label and no `Ownership:` sentence (D59). Fail when a paragraph
  carries another part's content, when two parts share one paragraph, or when fewer than four
  paragraphs exist. Prints: `star-order -> paragraph <n> "<first sentence of the paragraph that is
  out of place>" reads as <part>, expected <part> -> move it to position <m> (or: split it, or:
  add the missing <part> paragraph)`.
- **headline-carries-outcome** (major): the Headline states the outcome, not the project name or
  the activity. Prints: `headline-carries-outcome -> "<Headline>" -> state what changed for whom,
  with the number and its baseline`.
- **headline-baseline** (major): the Headline's number carries a baseline it beat or a comparator
  (from X to Y, N vs M, ahead of a date). Prints: `headline-baseline -> "<Headline>" -> add what the
  number is compared against`.
- **journey-in-action** (major): the situation and action paragraphs tell the journey in
  candidate-led action verbs: what was tried or ruled out, why no off-the-shelf path worked, who
  the candidate reached out to or aligned. Fail an action paragraph that lists deliverables with
  no ruled-out option and no other person. Prints: `journey-in-action -> "<action paragraph
  excerpt>" -> name one option ruled out and why, and who the candidate aligned`. Its countable
  twin is the lint's `journey-countable` (an action paragraph with no journey verb and no other
  person named). The lint catches the empty paragraph, this rule judges whether the journey the
  words claim is a real one.
- **no-process-leak** (blocker): no sentence in the body talks about the writing of the document
  (an earlier draft, an evidence pull, the reviewer of the previous version, a readiness row, the
  order the wins were put in, what is told once below, a working copy, a document's author field,
  whose names an acknowledgement carries, what is or is not on record, "the diagnosis as hers is",
  an evidence row, a stage document). The reader meets the work, never the evidence pipeline: the
  marker form is `(TO BE CONFIRMED)` as the last token of the sentence with no clause saying what is
  unconfirmed, the stage document holds that (D75). The lint fails the phrases it can match, this
  rule reads the rest. The frontmatter, the run brief and the Sources
  line are exempt. Prints: `no-process-leak -> "<sentence>" -> delete it, the document is the
  document`.
- **one-cr-once** (major): a code review id appears in the action paragraph of at most one story.
  A second story that needs it cross-references the first by heading. Why now and the Appendix
  are exempt. The lint counts the ids it can parse, this rule catches a review named in words.
  Prints: `one-cr-once -> "<review id>" in "<story A>" and "<story B>" -> keep it where the claim
  lives, cross-reference the other`.
- **marker-direction** (major): a link to a document the writer could not fetch sits in a sentence
  ending `(TO BE CONFIRMED)`, unless the ownership audit verified it and the sentence carries
  `(SUPPORTED)` or the workflow config exempts the link. And `(TO BE CONFIRMED)` is the marker for
  a figure whose artifact exists: a sentence with the marker and no link, number or document
  title in it means the data does not exist yet, so the marker is `(TO BE COLLECTED: <artifact>)`.
  The lint fails the first and warns on the second, this rule decides the warnings. Prints:
  `marker-direction -> "<sentence>" -> end it (TO BE CONFIRMED) (or: replace the marker with (TO
  BE COLLECTED: <artifact>))`.
- **altitude-test** (major, amended by D60 altitude-two-forms): each story's action paragraph ends
  with one altitude sentence in one of two forms: the counterfactual `A strong <current level>
  would have ..., not ...` (D24), or a factual contrast naming who else was engaged (how many were
  on the call, who was senior, role words backed per `role-words-held`) and what the candidate
  alone did. A factual contrast whose role words nothing holds fails `role-words-held`, not this
  rule. Prints: `altitude-test -> story "<heading>" has no altitude sentence -> end the action
  paragraph with "A strong <current level> would have ..., not ..." or with who else was engaged
  and what the candidate alone did`.
- **criterion-fit** (blocker): the criterion in a story's heading matches the marker its situation
  paragraph carries (Ambiguity: what was undefined and from whose view. Problem Complexity: why
  the cause was not obvious or who else owned the code). Prints: `criterion-fit -> "<heading>"
  carries the marker of <other criterion> ("<sentence>") -> move the story under <other criterion>
  or rewrite the situation paragraph`.
- **ownership-verdict** (blocker, D21 amended by D59): every ownership verb in a story (led, owned,
  drove, architected, designed, end-to-end) is backed by an attribution line in the ownership audit
  (a stage document beside the draft, `ownership-audit.md` in a run directory or
  `<stem>.ownership.md` beside a fixture) with a verdict SUPPORTED, PARTIALLY SUPPORTED or
  UNSUPPORTED. No `Ownership:` sentence is printed in the story: a PARTIALLY SUPPORTED verdict is
  carried as an inline credit by function in the task paragraph (house rule credit-inline), never
  as a subtraction. Prints: `ownership-verdict -> "<verb>" in "<sentence>" has no audit row (or:
  audit says UNSUPPORTED, or: PARTIALLY SUPPORTED with no inline credit) -> qualify the verb, add
  the attribution, or credit the other party in the sentence`.
- **one-story-once** (major): a project is told in full (more than 80 words) under exactly one
  heading. Every other mention, in Why now, another story or the Appendix, is one sentence with a
  cross-reference. Prints: `one-story-once -> "<project>" told under "<heading A>" and "<heading
  B>" -> keep the fuller telling, replace the other with one sentence and a cross-reference`.
- **quote-per-story** (major): every story ends with one verbatim quote from a named person with
  their role, or `(TO BE COLLECTED: quote from <role>)`. Prints: `quote-per-story -> story
  "<heading>" has <0 or 2+> quotes -> add one verbatim quote with name and role, or the marker`.
- **why-now-order** (blocker): the "On **Project**," sentences of the Why now paragraph follow the
  owner's `story-ranking` table, with `why_now.order` from the caller's config breaking ties only
  (D53), never the writer's choice and never time, and each carries its story's Headline number
  with its baseline. Prints: `why-now-order -> projects are ordered <observed> against ranking
  <order> (or: sentence "<sentence>" carries no Headline number) -> reorder by <order>, carry the
  number`.
- **why-now-no-list** (major): no Why now sentence names more than three projects, and a project
  with no story in Evidence is not named in Why now (it goes to the Appendix, D14). The lint
  checks the one-paragraph shape, this rule reads the sentences. Prints: `why-now-no-list ->
  "<sentence>" names <n> projects (or: names "<project>", which has no story) -> split it, or move
  the project to the Appendix`.
- **why-now-rollup** (major): the closing Why now sentence rolls up in at least two counts
  (projects, services, teams, regions, months) and carries no word from the house no-superlatives
  line. Prints: `why-now-rollup -> "<sentence>" has <n> counts (or: carries "<trait word>") ->
  close on counts, not on a pattern word`.
- **show-not-tell** (major): the judgement twin of the lint's `no-trait-words`: a paraphrased tell
  the denylist misses ("went the extra mile", "raised the bar", "a safe pair of hands") in Why now
  or a story paragraph, or a sentence that asserts a trait the surrounding sentences do not show.
  Prints: `show-not-tell -> "<sentence>" tells <trait> -> replace with the obstacle, the fork, the
  technique or the figure with its verb that shows it`.
- **obstacle-first** (major): the situation paragraph names the obstacle in concrete nouns before
  the candidate's first verb: what did not exist (no API, no document, no owner, no test path),
  who else owned the code. The lint warns when no absence construction precedes the candidate's
  first sentence, this rule judges whether the obstacle is specific enough that a reader could name
  it back. Prints: `obstacle-first -> story "<heading>" situation "<first sentences>" -> name what
  did not exist before "<candidate's first verb>"`.
- **figure-has-verb** (major): every figure in a result paragraph sits in the sentence with the
  verb that produced it, relative first, with its baseline. No bare results line. The lint warns
  on a numbered sentence with no verb, this rule reads whether the verb is the one that produced
  the figure. Prints: `figure-has-verb -> "<sentence>" -> write "<verb> ... <figure> (<baseline>)"`.
- **reuse-named** (major): the result paragraph ends on a named user of the work (a team or a
  builder who now runs it, extends it or plans from it) or on the exact sentence "No reuse by
  others is on record." "Stakeholders", "the business" and "customers" with no name are not a
  user. The lint warns, this rule decides. Prints: `reuse-named -> story "<heading>" ends "<last
  sentence>" -> name who uses it now, or write the no-reuse sentence`.
- **owner-ranked-stories** (blocker): the per-candidate decisions file holds a `story-ranking`
  table (project, rank, one line on why it matters) written by the owner. The Why now order and
  the first full story under each criterion follow it. A run with no table writes `questions.md`
  listing every candidate project with its evidence strength (held numbers, markers, code review
  count) and no draft. Prints: `owner-ranked-stories -> no story-ranking table in the decisions
  file (or: story "<heading>" is first under <criterion>, the table ranks "<project>" above it) ->
  stop and write questions.md (or: reorder to the table)`.
- **vp-read** (blocker): after reading Why now and the first two stories, the reviewer can state
  in one sentence, quoting the draft, what the candidate did that nobody else on the team was
  doing and why it was hard. When no such sentence can be written, fail, naming the story that
  should have carried it. Prints: `vp-read -> after Why now and stories "<heading A>" and
  "<heading B>" no draft sentence says what only the candidate did and why it was hard -> add it
  to story "<heading>" (what nobody else was doing, and the obstacle)`.
  Note (D79): when the first two stories both end on the sentence "No reuse by others is on
  record.", the reviewer states in the review whether the result paragraph's last held figure is
  strong enough to carry the ending, or moves that figure last so the VP's final line on each
  top story is a number, not a gap. A marker in the sentence before the no-reuse sentence fails
  this note. Prints: `vp-read -> stories "<heading A>" and "<heading B>" both end on the
  no-reuse sentence, the sentence before it is "<sentence>" -> end on the held figure, or state
  why the figure cannot carry the ending`.
- **rollup-counts-held** (major, D77): every count in the closing Why now sentence (projects,
  services, teams, regions, months, pipelines) has one impact-data row, or is a count of the
  draft's own story headings (projects, initiatives, stories). The lint warns when a heading count
  disagrees, this rule reads the impact-data file for the rest. Prints: `rollup-counts-held ->
  closing sentence counts "<N noun>" -> add the impact-data row that holds it, or count what the
  draft shows`.
- **scope-no-candidate** (blocker): `## Scope of Role` describes the team and the proposed level
  and is the scope file's text for the level pair. The lint fails the candidate's name or alias, a
  hire or join word and a prior-team sentence, this rule reads the rest: a sentence about what the
  candidate did, or a next-level paragraph that is the current-level one with the title changed.
  Prints: `scope-no-candidate -> "<sentence>" is about the candidate (or: the next-level paragraph
  repeats the current-level one) -> replace with the scope file's paragraphs for <level pair>`.
- **candidate-facts** (blocker): the header tenure, every "in N months as a <title>" clause and the
  review-count window come from the `candidate-facts` block (prior roles with months, level start
  date, months in level) and run from the level start, never the hire date. A fact the block does
  not hold is a TODO row for the owner and `(TO BE CONFIRMED)` in the text, never a guess. The lint
  fails a day count, this rule reads the source. Prints: `candidate-facts -> "<figure>" in
  "<sentence>" is not in the candidate-facts block (or: counts from the hire date) -> take it from
  the block, or mark it (TO BE CONFIRMED) and add the TODO row`.
- **rntp-shape** (blocker): each reason not to promote has five parts in order: Pattern with two
  positive examples, Gap with one dated example of who pointed it out, Also seen by a second
  person, Does not block <level> with evidence, Next with a plan. Prints: `rntp-shape -> reason
  "<heading>" lacks <part> -> add <part> with <what it needs>`.
- **rntp-contradiction** (blocker, document-wide): no reason's stated gap is contradicted by a
  story, and no reason states as fact a claim that any story marks `(TO BE CONFIRMED)` or `(TO BE
  COLLECTED)`. The scan covers every reason against every story, not the reason beside the story.
  The lint approximates the second half by project name plus an initiative phrase (without a
  ticket, on her own, on his own, unprompted, initiative), this rule reads every claim. Prints:
  `rntp-contradiction -> gap "<gap sentence>" vs story "<story sentence>" -> narrow the gap to what
  the stories support, or remove the contradicting claim` or `rntp-contradiction -> reason
  "<sentence>" states as fact what story "<heading>" marks -> add the marker or narrow the claim`.
- **asana-date-role** (blocker): every task-tracker date in a result paragraph is the task's
  completion date, never its created or due date, and a task whose code fix is another builder's
  change has a row in the ownership audit (a stage document beside the draft) naming that builder
  and the verdict. Prints: `asana-date-role -> "<sentence>" carries a <created|due> date as the
  result (or: task "<title>" fixed by another builder has no ownership-audit row) -> use the
  completion date (or: add the audit row and qualify the verb)`.
- **provider-gap-fallback** (blocker): when the Feedback section is a placeholder (its table rows
  are `(TO BE COLLECTED)` markers), the provider gaps are read from the gap analysis stage
  document's "Provider gaps first" table instead, and each row there is addressed by one reason in
  Best reasons not to promote. `provider-gap-addressed` reads the Feedback section when it holds
  real text, this rule reads the gap analysis when it does not. Prints: `provider-gap-fallback ->
  gap-analysis row "<gap>" has no reason -> add a reason in the five-part shape`.
- **aspiration-not-gap** (blocker): a reason names an observed gap, not what the manager would
  like the candidate to take on next. Prints: `aspiration-not-gap -> "<reason heading or
  sentence>" is an ask, not an observed gap -> replace with a gap a reviewer or provider has
  pointed out, with its date`.
- **provider-gap-addressed** (blocker): every gap a feedback provider states in `## Feedback` is
  addressed by one reason in Best reasons not to promote. Providers change, so the check reads
  the Feedback section present in the document, never a fixed list of names. Prints:
  `provider-gap-addressed -> provider gap "<sentence>" has no reason -> add a reason in the five-
  part shape`.
- **plain-headings** (major): reason headings and story headings are plain words, no bracketed
  principle tags, no abstract nouns stacked ("Cultivating proactive strategic opportunity
  identification"). The lint fails a heading with a word from the house denylist (leverage, play,
  strategic, proactive, cultivat-, drive alignment, synerg-, holistic, paradigm), this rule judges
  the rest. Prints: `plain-headings -> "<heading>" -> rewrite as what the candidate does
  not yet do, in plain words`.
- **copy-check** (blocker): no run of 8 or more words in the author's prose is shared with a file
  that holds another person's words (the feedback file, reviewer rewrites, calibration samples).
  `scripts/promo-copycheck.py <draft> <source>... --evidence-dir <dir>` lists runs by source, the
  quote lines and the Feedback section are exempt because they are verbatim by rule. A run the
  script prints as `source-held` (the same words sit in a file under the evidence directory) is
  recorded as such and passes when it is an identifier, data-format or product-name list, and is
  rewritten when it is a sentence of argument. Prints: `copy-check -> "<run>" from <source> ->
  rewrite in the author's words or move it into a quote line with its name and role` or
  `copy-check -> "<run>" from <source>, source-held by <evidence file> -> recorded, no change`.
- **role-words-held** (major): a role word on another person in a story (senior builder, principal
  engineer, product manager, bar raiser) attached to a specific act is backed by a people-directory
  row in the evidence or an artifact naming the role. Otherwise the sentence takes `(TO BE
  CONFIRMED)` or the plain word "builder". The lint warns on a story paragraph with a role word and
  no link and no marker, this rule reads the evidence for the rest. Prints: `role-words-held ->
  "<role word>" in "<sentence>" has no directory row or artifact -> write builder, or end the
  sentence (TO BE CONFIRMED), or add the row`.
- **asked-for-by-audited** (major): the subject of every "asked for by" clause in a task paragraph
  has one row in the ownership audit with the artifact that shows the ask (a ticket, a chat message
  with its link, a design-doc requester field, an acknowledgement). The lint checks that the clause
  exists, this rule checks its evidence. Prints: `asked-for-by-audited -> "asked for by <subject>"
  in story "<heading>" has no audit row -> add the row with the artifact, or name the subject the
  evidence holds`.
- **pattern-cites-unmarked** (blocker): a reason's Pattern cites a story as an example of a trait
  only when that story asserts the trait in a sentence with no marker. A story that marks the trait
  `(TO BE CONFIRMED)` or `(TO BE COLLECTED)` is not yet an example of it. `rntp-contradiction`
  covers a reason's explicit claim, this rule covers the Pattern's lean. Prints:
  `pattern-cites-unmarked -> Pattern "<sentence>" cites story "<heading>" for <trait>, which the
  story marks "<marked sentence>" -> cite a story that asserts it, or drop the example`.
- **ordering-words-stamped** (major): an ordering word between two tool-stamped events (before,
  after, then, once) is used only when the stamps agree with the order claimed. When the stamps
  disagree or sit within minutes of each other, the two events share one clause with no order.
  Prints: `ordering-words-stamped -> "<sentence>" claims <event A> before <event B>, stamps
  <stamp A> and <stamp B> -> write both in one clause ("the day she ..."), or drop the order`.
  Countable twin (D73): the lint's `ordering-stamped` fails an action sentence whose two or more
  linked artifacts carry dates (in the sentence or the run's `--dates` csv) that run against the
  words, and warns on one linked artifact. This rule reads the stamps the lint cannot (a tracker's
  created time, a page's history) and every ordering claim kept takes a decisions-file row.
- **subset-words** (major): a count that is a subset in its source takes a subset word ("six of
  its", "six of the eight"), never the definite article alone. Prints: `subset-words -> "<the N
  things>" where the source gives <M> in total -> write "N of its M" or "N of the M"`.
- **marker-warnings-ruled** (blocker, before the sink write): every lint `marker-direction` warning
  on the draft is ruled on before the document is written to its sink. A ruling is one of: the
  sentence now carries `(TO BE COLLECTED: <artifact>)` with the artifact named, the clause is cut,
  or the caller's decision to keep it is a row in the candidate's decisions file. An unruled
  warning blocks the write, not the draft. Prints: `marker-warnings-ruled -> warning "<sentence>"
  has no ruling -> name the artifact in (TO BE COLLECTED: ...), cut the clause, or record the
  ruling in the decisions file before the sink write`.
- **parked-findings-logged** (major): every reviewer finding the caller parks (a placement, a
  wording kept, a figure not chased) has one row in the candidate's decisions file with the date,
  the finding, where it was raised and the reviewer's advice. A finding mentioned only in a
  bar-check or run brief is not logged. Prints: `parked-findings-logged -> finding "<finding>"
  parked in <file> has no decisions row -> add the row with date and the reviewer's advice`.
- **markers-consistent** (blocker): exactly two markers, in round brackets: `(TO BE COLLECTED)`
  or `(TO BE COLLECTED: <what>)` when the data does not exist yet, `(TO BE CONFIRMED)` at the end
  of a sentence whose number or source is unconfirmed. Fail any square-bracket form, `TODO`,
  `TBD`, `TBC` or `(unverified)` in a promo-doc. The marker is the last token of its sentence and
  the clause after `TO BE COLLECTED:` names the artifact only (D46, D75). Prints:
  `markers-consistent -> "<token>" -> use (TO BE COLLECTED) or (TO BE CONFIRMED)`.
- **marker-propagation** (blocker, D72): a figure the impact-data stage document marks `(TO BE
  CONFIRMED)` or `(TO BE COLLECTED: ...)` in its status cell sits in a story sentence ending on the
  same marker, never as fact, and never in Why now (D55). The lint fails every match it can read
  with `--impact-data`, this rule reads the figures the lint's matcher skips (a one or two digit
  count with no unit word). Prints: `marker-propagation -> "<sentence>" prints <figure> as fact,
  impact-data row <n> marks it -> end the sentence with the row's marker, or move it out of Why
  now`.
- **credit-not-subtraction** (blocker, D74, the house rule credit-inline): no story sentence credits
  shared work as a subtraction from the candidate's claim ("with the cache core from a second
  builder", "under another builder's design"). The lint fails the two regex forms, this rule reads
  the paraphrases. Prints: `credit-not-subtraction -> "<sentence>" -> write the credit as a
  widening in the same sentence as the candidate's act`.
- **links-kept** (major): every code review, document or ticket named in a story is a hyperlink on
  its identifier pointing at the real artifact, and a shortened story keeps every link the longer
  version had (compare `promo-lint.py --counts` before and after). Prints: `links-kept -> story
  "<heading>" dropped <n> links in the rewrite (or: "<identifier>" is bare) -> restore the links`.
- **section-length** (major): a story under 500 words quote excluded, Why now under 550, at most
  2 full stories and 600 words under one criterion. The lint measures, the gate prints the longest
  offender first: `section-length -> "<heading>" <n> words, cap <cap> -> cut <what> and keep every
  link`.

> To extend: add rules under the right severity, or add a doc-type note in
> required-sections. Keep rule ids short and stable so verdicts are easy to scan.
