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
  placeholder (for example `[TO BE COLLECTED]`). Named reviewers or quoted feedback that
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
  - promo-doc: Header block, Scope of Role, Promotion Assessment (with "Why now?"),
    capability sections, Best reasons not to promote, Feedback Summary.
- **balance** (blocker for talent-card and promo-doc): Includes genuine growth areas
  (talent card) or a candid, specific "reasons not to promote" (promo doc). A section that
  is empty, hand-wavy, or purely positive fails this rule.

## C. Writing quality (major)

All the generic writing-voice rules live in [leadership-writing/house-rules.md](../leadership-writing/house-rules.md):
claim-has-artifact (as honest-and-data-driven), quantify-impact, no-superlatives, write-for-reader,
logical-progression, show-dont-tell, active-voice, zombie-test, no-hedging (with its banlist),
define-acronyms, link-artifacts, and story-not-bullets. Read that file and enforce every rule in it
as a checker (fail a real violation). This section adds only the people-review-specific quality
rules that are NOT generic voice:

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
- **sbi-structure**: Each evidence example should map to Situation -> Behavior -> Impact, with
  Behavior (what THIS person specifically did) as the bulk and Situation kept short. Flag
  examples that are all context and no distinct individual behavior.
- **principle-citation** (promo-doc): follow `principles.cite_per_statement` in the glossary.
  `false` (default): one roll-up line `<principles.name> demonstrated: X, Y, Z` closes each
  capability section and no per-statement tags appear. `true`: one principle in bold brackets at
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
| **resume-doc** | Lists accomplishments with no Situation/Behavior/Impact | Rewrite each example as SBI; show complexity and individual action |
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

> To extend: add rules under the right severity, or add a doc-type note in
> required-sections. Keep rule ids short and stable so verdicts are easy to scan.
