# 2026-11-23 promo-doc round 1b: label-free STAR, lint fallback, fixture fixes, house rules

Follow-up to `2026-11-23-promo-doc-red-green.md` (findings R1 to R3, G1, G2) plus the owner's
ruling D28. Branch `promo-doc`, commits `8d4c94a`, `8d9a195`, `7e59576`, `eb1a907`, `6145448` and
this file. Inputs: `scripts/promo-lint.py`, `scripts/check.sh`, `skills/write-promo-doc/`,
`skills/validate-writing/checklist.md` section H, `skills/leadership-writing/house-rules.md`, the
three promo fixtures and their companions. Everything here is fictional.

## What changed

| # | Commit | Change | Enforcer |
|---|---|---|---|
| 1 | `8d4c94a` | D28: STAR is the skeleton the writer follows, never words the reader sees. The bold `**Situation**`, `**Task**`, `**Action**`, `**Result**` lead-ins are gone from the template, the skill and both fixtures. A story is the H3 heading, the `**Headline**` line, four unlabelled prose paragraphs in STAR order (the task paragraph ends with the `Ownership:` sentence, the action paragraph with the altitude sentence) and the quote line | lint `story-paragraphs`, `no-star-labels`, `ownership-line` replace `star-leadins`. checklist `star-order` (blocker) added. ADR 0001 amended, decision log D28, `decisions.md` row 1 |
| 2 | `8d9a195` | R1: a draft with no `## Evidence` is still measured per story. The lint finds the shallowest heading level whose titles are bracketed (`#### [<Criterion>]`), splits each such section at whole-line bold titles, prints `shape: fallback` first and runs the per-story rules on those blocks | `fallback_stories` and `lint_stories` in `promo-lint.py`, new fixture `evals/fixtures/promo-doc-bad.flat.md`, `check.sh promo-lint` asserts the `shape: fallback` line and a `story-length` hit |
| 3 | `7e59576` | R2: `no-semicolons` and `no-em-dash` skip text under `## Feedback`. R3: `bare-identifier` skips a leading YAML frontmatter block | line loop in `promo-lint.py`, section tracked per H2 |
| 4 | `eb1a907` | G1: Pier Alarm Cleanup's action paragraph names a ruled-out option (muting the 19 alarms wholesale, 2 had paged on real incidents) and a person (Owen Faraday, on-call lead). G2: a `## Feedback` section with two providers, each stating one gap, the Feedback Summary table filled with the two rows, and `promo-doc-good.ownership.md` with one verdict per story | fixtures, checklist `ownership-verdict` now names the companion file, `evals/README.md` rows |
| 5 | `6145448` | House rules: `plain-headings` under Voice rules, `quantify-impact` extended with the baseline sentence. Rule id added to the five writer skills' lists and to checklist section C. No marker convention of another genre changed | `skills/leadership-writing/house-rules.md`, `check.sh loop` and `triggers` still pass |

## Lint output, as run at `6145448`

The em-dash character in two quoted lines is written `<em-dash>` here so this file carries none.

### `promo-doc-bad.md` (red fixture, template shape): 32 failures, 1 warning, exit 1

```
story-length Ambiguity > Seawall Schema: 618 words, cap 500
required-section document: missing `## Feedback Summary`
no-semicolons line 13: `Harbor Telemetry owns the ingest path for 1,400 internal ...`
bare-identifier line 25: `CR-4821` is named but not linked
bare-identifier line 25: `CR-4836` is named but not linked
markers-consistent line 27: `TODO: confirm launch date`.` is not (TO BE COLLECTED) or (TO BE CONFIRMED)
bare-identifier line 37: bare URL `https://example.com/reviews/4902`, link it on the artifact's identifier
bare-identifier line 37: bare URL `https://example.com/reviews/4917.`, link it on the artifact's identifier
no-semicolons line 51: `2,300 lines of mappings were deleted by 09/18/2026 and al...`
no-em-dash line 59: `A platform campaign required tagging by 06/30/2026 <em-dash> Harb...`
markers-consistent line 93: `TBD]` is not (TO BE COLLECTED) or (TO BE CONFIRMED)
why-now-wins Why now: 0 bold wins with a number, need 3
headline-first Ambiguity > Lighthouse Parser: first line under the heading is `Dana designed and built the Lighthouse Parser end-to-end ...`, not **Headline**
story-paragraphs Ambiguity > Lighthouse Parser: 1 prose paragraphs between the Headline and the quote, need 4 (situation, task, action, result, no labels)
story-links Ambiguity > Lighthouse Parser: 0 links, every named artifact is a hyperlink on its identifier
headline-number Problem Complexity > Breakwater Credentials: `Fixed the credential storm during the regional event.` has no number
story-paragraphs Problem Complexity > Breakwater Credentials: 3 prose paragraphs between the Headline and the quote, need 4 (situation, task, action, result, no labels)
ownership-line Problem Complexity > Breakwater Credentials: task paragraph (second) does not end with `Ownership: originated ..., executed ..., operated ...`: `Dana proposed and drove the shared credential cache, arch...`
quote-per-story Problem Complexity > Breakwater Credentials: 0 quote lines, need exactly 1
story-links Problem Complexity > Breakwater Credentials: 0 links, every named artifact is a hyperlink on its identifier
headline-number Ambiguity > Seawall Schema: `Replaced the schema mappings.` has no number
ownership-line Ambiguity > Seawall Schema: task paragraph (second) does not end with `Ownership: originated ..., executed ..., operated ...`: `Dana owned the single derivation, asked for by the manage...`
headline-baseline Execution > Quayside Tagging: `Tagging shipped for all 4 resource types.` has a number with no baseline or comparator (from X to Y, N vs M, ahead of <date>)
ownership-line Execution > Quayside Tagging: task paragraph (second) does not end with `Ownership: originated ..., executed ..., operated ...`: `Dana fixed the race and shipped tagging for the 4 types.`
story-links Execution > Quayside Tagging: 0 links, every named artifact is a hyperlink on its identifier
headline-baseline Impact > Lighthouse Parser: `Lighthouse Parser parses 40 million events a day for 310 ...` has a number with no baseline or comparator (from X to Y, N vs M, ahead of <date>)
ownership-line Impact > Lighthouse Parser: task paragraph (second) does not end with `Ownership: originated ..., executed ..., operated ...`: `Dana owned adoption tracking.`
story-links Impact > Lighthouse Parser: 0 links, every named artifact is a hyperlink on its identifier
one-story-once lighthouse parser: told in full (80+ words) under 2 headings: Ambiguity, Impact
rntp-leadins reason > Cultivating proactive strategic initi...: lead-ins found [], need ['Pattern', 'Gap', 'Also seen by', 'Does not block', 'Next'] in order
rntp-leadins reason > Becoming the operational excellence c...: lead-ins found [], need ['Pattern', 'Gap', 'Also seen by', 'Does not block', 'Next'] in order
readiness-first document: no readiness table beside the draft (<stem>.readiness.md or gap-analysis.md) with a `Readiness: Ready | Ready with gaps | Not ready` verdict
warning section-length Ambiguity: 2 stories, 723 words (target at most 2 stories and 600 words), move the weakest story to one sentence or an appendix
promo-lint: 32 failure(s), 1 warning(s)
```

Against the 28 lines at `123a7f4`: the two `star-leadins` lines became two `story-paragraphs`
lines (1 and 3 paragraphs where 4 are needed), four `ownership-line` lines are new (no story in
the red fixture ends its second paragraph with the Ownership sentence), and Seawall Schema lost 4
words of labels (622 to 618, still over the cap). Every class named before is still named.

### `promo-doc-good.md` (green fixture): 0 failures, 0 warnings, exit 0

With `--counts`: Why now 223 words, stories 328, 285, 233, 221, 223 and 171 words, 18 links in
total, Pier Alarm Cleanup 223 words and 2 links after the G1 edit (the edit added prose, its two links
are unchanged).

### `promo-doc-bad.flat.md` (red fixture flattened to the pre-template shape): `shape: fallback`, 33 failures, 1 warning, exit 1

```
shape: fallback
story-length Ambiguity > Seawall Schema: 620 words, cap 500
required-section document: missing `## Evidence`
required-section document: missing `## Feedback Summary`
no-semicolons line 13: `Harbor Telemetry owns the ingest path for 1,400 internal ...`
bare-identifier line 27: `CR-4821` is named but not linked
bare-identifier line 27: `CR-4836` is named but not linked
markers-consistent line 29: `TODO: confirm launch date`.` is not (TO BE COLLECTED) or (TO BE CONFIRMED)
bare-identifier line 41: bare URL `https://example.com/reviews/4902`, link it on the artifact's identifier
bare-identifier line 41: bare URL `https://example.com/reviews/4917.`, link it on the artifact's identifier
no-semicolons line 57: `2,300 lines of mappings were deleted by 09/18/2026 and al...`
no-em-dash line 67: `A platform campaign required tagging by 06/30/2026 <em-dash> Harb...`
markers-consistent line 103: `TBD]` is not (TO BE COLLECTED) or (TO BE CONFIRMED)
why-now-wins Why now: 0 bold wins with a number, need 3
rntp-leadins reason > Cultivating proactive strategic initi...: lead-ins found [], need ['Pattern', 'Gap', 'Also seen by', 'Does not block', 'Next'] in order
rntp-leadins reason > Becoming the operational excellence c...: lead-ins found [], need ['Pattern', 'Gap', 'Also seen by', 'Does not block', 'Next'] in order
headline-first Ambiguity > Lighthouse Parser: first line under the heading is `**Lighthouse Parser**`, not **Headline**
story-paragraphs Ambiguity > Lighthouse Parser: 2 prose paragraphs between the Headline and the quote, need 4 (situation, task, action, result, no labels)
ownership-line Ambiguity > Lighthouse Parser: task paragraph (second) does not end with `Ownership: originated ..., executed ..., operated ...`: `The parser launched in [date] and is used by [N customers...`
story-links Ambiguity > Lighthouse Parser: 0 links, every named artifact is a hyperlink on its identifier
headline-first Problem Complexity > Breakwater Credentials: first line under the heading is `**Breakwater Credentials**`, not **Headline**
ownership-line Problem Complexity > Breakwater Credentials: task paragraph (second) does not end with `Ownership: originated ..., executed ..., operated ...`: `Dana noticed that credential fetches were failing during ...`
quote-per-story Problem Complexity > Breakwater Credentials: 0 quote lines, need exactly 1
story-links Problem Complexity > Breakwater Credentials: 0 links, every named artifact is a hyperlink on its identifier
headline-first Ambiguity > Seawall Schema: first line under the heading is `**Seawall Schema**`, not **Headline**
ownership-line Ambiguity > Seawall Schema: task paragraph (second) does not end with `Ownership: originated ..., executed ..., operated ...`: `By June 2026 downstream tables needed typed schemas from ...`
headline-first Execution > Quayside Tagging: first line under the heading is `**Quayside Tagging**`, not **Headline**
ownership-line Execution > Quayside Tagging: task paragraph (second) does not end with `Ownership: originated ..., executed ..., operated ...`: `A platform campaign required tagging by 06/30/2026 <em-dash> Harb...`
story-links Execution > Quayside Tagging: 0 links, every named artifact is a hyperlink on its identifier
headline-first Impact > Lighthouse Parser: first line under the heading is `**Lighthouse Parser**`, not **Headline**
ownership-line Impact > Lighthouse Parser: task paragraph (second) does not end with `Ownership: originated ..., executed ..., operated ...`: `After the launch of the Lighthouse Parser, which Dana des...`
story-links Impact > Lighthouse Parser: 0 links, every named artifact is a hyperlink on its identifier
one-story-once lighthouse parser: told in full (80+ words) under 2 headings: Ambiguity, Impact
readiness-first document: no readiness table beside the draft (<stem>.readiness.md or gap-analysis.md) with a `Readiness: Ready | Ready with gaps | Not ready` verdict
warning section-length Ambiguity: 2 stories, 727 words (target at most 2 stories and 600 words), move the weakest story to one sentence or an appendix
promo-lint: 33 failure(s), 1 warning(s)
```

Through the fallback every per-story rule names a story: `story-length` (620), `quote-per-story`,
`story-links` (4), `one-story-once`, `story-paragraphs`, `ownership-line`, `section-length`. The
bold project title takes the Headline slot, so `headline-first` fires once per story (5) and names
the title, and `headline-number` and `headline-baseline` do not run because no `**Headline**` line
is first. `required-section` still fails twice. The fallback is a measurement aid for documents
that predate the template, not a second template.

## Before and after, per finding

| Finding | Before (at `123a7f4`) | After (at `6145448`) | Proof |
|---|---|---|---|
| R1 out-of-shape draft measured per story | a draft with no `## Evidence` failed 5 `required-section` lines and 0 per-story lines | the flat fixture fails 2 `required-section` lines plus 29 per-story and document lines through the fallback, `shape: fallback` printed first | `promo-doc-bad.flat.md` output above, `check.sh promo-lint` asserts it |
| R2 house rules on provider text | a `## Feedback` line with a semicolon and an em-dash produced 2 failures | 0 failures on that line, the same line outside Feedback still fails. Test: the red fixture plus a Feedback subsection holding one semicolon and one em-dash gives the fixture's own 3 `no-semicolons` and `no-em-dash` lines and nothing from Feedback | hand test, not a committed fixture (the green fixture's providers carry no semicolon so the fixture stays clean) |
| R3 bare identifiers in frontmatter | a `source: https://...` frontmatter line and a `ticket: CR-123456` line produced 2 `bare-identifier` failures | 0 on those lines, a bare URL in the body still fails | hand test on the red fixture with a 3-line YAML block prepended |
| G1 journey-in-action on Pier Alarm Cleanup | fail by the letter: no ruled-out option, no other person in the action paragraph | pass: "ruled out muting them wholesale because 2 of the 19 had paged on real incidents" and "agreed the delete list with Owen Faraday, the on-call lead" | `promo-doc-good.md`, story still 223 words |
| G2 provider-gap-addressed | vacuous pass, no `## Feedback` section | exercised: provider 1 gap (documents run long, 08/12/2026) is reason "Writing shorter decision documents" whose Gap cites the same person and date, provider 2 gap (waits for the leverage play to be pointed out, 05/06/2026) is reason "Proposing the next leverage play before being asked" whose Gap cites the same person and date | `promo-doc-good.md` Feedback and Best reasons not to promote |
| G2 ownership-verdict audit half | not exercised, no audit beside a fixture | exercised: `promo-doc-good.ownership.md` holds one row per story, 4 SUPPORTED and 2 PARTIALLY SUPPORTED, the two partial rows name the qualification the story's Ownership sentence carries | new fixture companion |
| D28 label-free STAR | both fixtures printed the four bold labels, lint `star-leadins` counted them | no label in either fixture, lint `no-star-labels` fails a printed label, `story-paragraphs` counts the four paragraphs, `ownership-line` checks the second paragraph's close | lint output above, red fixture 32 lines |

## Judgement rules touched by this round, applied by hand

| Rule | Red fixture | Green fixture |
|---|---|---|
| star-order (new, blocker) | fail twice. Lighthouse Parser: Ambiguity has 1 paragraph, "Dana designed and built the Lighthouse Parser end-to-end ..." reads as action in position 1, expected situation. Quayside Tagging: Execution paragraph 2 "Dana fixed the race and shipped tagging for the 4 types." reads as action, expected task, and paragraph 3 "Dana took over the campaign." reads as task, expected action (the two were swapped in this round so the rule has a clean case) | pass, all six stories read situation, task ending `Ownership:`, action ending with the altitude sentence, result |
| journey-in-action | fail, unchanged | pass on all six, G1 closed |
| provider-gap-addressed | fail, unchanged (the provider's long-documents gap has no reason) | pass, both provider gaps map to a reason by person and date |
| ownership-verdict | fail, unchanged, and no audit beside the fixture | pass, every verb backed by the Ownership sentence and an audit row |
| plain-headings (now a house rule too) | fail, unchanged | pass |

## check.sh at `6145448`

```
identity     ok (34 commits, all vikashagrawal1990@gmail.com)
no-org       ok (no company-specific terms or ids)
schemas      ok (workflows: 1)
frontmatter  ok (10 skills, spec-conformant names and descriptions, frontmatter parses)
loop         ok (6 writer skills: gate, min 2, max 5, house-rules)
glossary     ok (11 glossary keys all defined)
triggers     ok (36 checks, 0 failure(s), 10 skills)
rules        ok (28 rows, every enforcer exists)
promo-lint   ok (red fixture fails with 33 lines, green fixture 0 failures, flattened red fixture linted through the fallback)
instance     skipped (VSTACK_INSTANCE not set)
```

Exit 0. The identity line counts the five commits of this round. `VSTACK_INSTANCE` was not set in
this session, so the instance group did not run.

## Notes for the instance and the owner

- An instance `draft_contract` that keyed on `^\*\*Situation\*\* `, `^\*\*Task\*\* `,
  `^\*\*Action\*\* ` and `^\*\*Result\*\* ` must drop those four `must_match` patterns and may add
  `must_not_match ^\*\*(Situation|Task|Action|Result)\*\*`. The shared shapes file carries the
  change.
- `no-star-labels` is an extra countable rule beyond what the round asked for. It exists so a
  writer that prints the labels fails before the gate, the cheapest enforcer of D28.
- `ownership-line` makes the Ownership sentence countable (D21 had it in the template only). It
  fires on every red-fixture story with two or more paragraphs, which is the intended signal on a
  document written before the rule.
- The green fixture's provider text carries no semicolon on purpose, so R2 is proven by the hand
  test above and not by a committed fixture. A committed fixture with a verbatim provider
  semicolon would prove it in `check.sh` at the cost of a semicolon in the tree.
- Marker conventions of talent-card (`[TO CAPTURE: ...]`) and exec-update (`(unverified)`) are
  untouched, that decision stays with the owner.
- The judgement rules above are a hand application, the gate skill was not run in a harness in
  this round.

## After round 1b, rerun at `c23b669` by a fresh reviewer

Fixture counts unchanged: red fixture 32 failures and 1 warning, green fixture 0, flat fixture `shape: fallback` with 33 failures and 1 warning. On the instance's real out-of-shape red sample the lint dropped from 41 to 29 lines (R2 and R3 landed) but printed no `shape: fallback` line and 0 per-story lines, where the flat fixture prints 29. Cause: that document puts a second heading of the same level, the rubric sentence, directly under each bracketed criterion heading, so `split_sections` gives every bracketed heading an empty body and `fallback_stories` returns no story. The flat fixture has no such sibling heading, so `check.sh promo-lint` stays green while the shape R1 described is still unmeasured. With the sibling headings demoted to prose the same document yields 6 `story-length` lines (512 to 657 words) and 3 `section-length` warnings. R1 stays open until `fallback_stories` treats a non-bracketed heading at the bracketed level as body text and the flat fixture carries the sibling heading. Instance record: the candidate folder's round 1c bar check.
