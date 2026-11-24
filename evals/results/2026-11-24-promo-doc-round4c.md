# 2026-11-24 promo-doc round 4c: what the gate could not see, D72 to D80

Follow-up to `2026-11-24-promo-doc-round4-shape.md`. Branch `promo-doc` from `61e79f8` (15 commits over
main), main untouched. Input: the first end-to-end review's section "What the gate cannot see yet",
eight rows, each a miss the reviewer caught by judgement that no lint, contract or checklist rule
counted, plus one lint limit the run had worked around (a story renamed so its heading would clear
the lead pattern's colon). Everything named here is fictional. Counts only, no names, no identifiers.

## Where each rule landed

| Decision | Rule | Layer | Red fixture line that fires it | Red failures added |
|---|---|---|---|---|
| D72 | marker-propagation | lint (reads `--impact-data <path>`, one printed line when absent), checklist blocker for the figures the matcher skips, template, SKILL stage-document section | Why now prints the 212 review count that impact-data row 3 marks to collect, the schema story's action paragraph prints 11 pages that row 4 marks to confirm | 2 (only with the stage file) |
| D73 | ordering-stamped | lint (fail on two dated linked artifacts against the words, warning on one linked artifact beside an unlinked artifact noun or a date, `--dates <csv>` for the stamps), checklist ordering-words-stamped twin paragraph, template row | "reproduced the race first in review A and then shipped in review B" with the csv dating A five days after B | 1 fail (with the csv), 1 warning |
| D74 | credit-not-subtraction | lint blocker, house rule credit-inline names the form, checklist blocker for paraphrases, template Shared work row and the exact-strings block | a task sentence "with the cache core from a second builder, under the other team's design" | 1 |
| D75 | no-process-leak phrases, markers-consistent form | lint (eight phrases, marker as last token, collect-marker names an artifact only), checklist no-process-leak and markers-consistent, template Markers row, SKILL marker section | "as the evidence row for the dashboard's author field records", "(TO BE COLLECTED: the adoption count, because nobody has measured it since launch) and trending up" | 1 + 2 |
| D76 | why-now-sentence-shape | lint major, template Why now shape row and step 3 | a 74-word `On **Project**,` sentence that holds the pronoun back 40 words (two failures), and the old fixture's own 77-word sentence (one more) | 3 |
| D77 | rollup-counts-held | lint warning (projects, initiatives, stories against the headings), checklist major under vp-read (impact-data rows for the other counts), SKILL conventions | "Across 7 projects" against 4 distinct story projects | 0 (warning) |
| D78 | inferred year in the baseline cell | stage-document convention in SKILL, green impact-data row 4 | none, no lint | 0 |
| D79 | no-reuse ending note | checklist vp-read note, template result step (end on the held figure or who uses it now, never another builder's change) | none, judgement | 0 |
| D80 | story-lead takes `::` | lint pattern `(.+?)` to the first `:**`, template Story lead row, D62 amended | none in red. The GREEN heading now carries a `::` identifier and the previous lint fails it with one story-lead line, the new one passes | 0 |

Lint: 7 of 9 (D72 to D77, D80). Checklist: 6 of 9 carry a row or a note (D72, D73, D74, D75, D77,
D79). House rule: 1 of 9 (D74, inside credit-inline, every genre). Skill or template: 8 of 9.

Also changed in the lint: `sentences()` now splits after a closing `)` before a capital, so
`"... since. (TO BE CONFIRMED) Next sentence"` is two sentences, which the marker rules need. On the
old red fixture this moved one relative-first message to the sentence that carries the figure and
changed no count. The green fixture's one such result paragraph now ends on a named team.

## Counts before and after

| Fixture | Before (61e79f8) | After, without stage files | After, with stage files |
|---|---|---|---|
| red `promo-doc-bad.md` | 57 failures, 13 warnings | 62 failures, 14 warnings | 65 failures, 14 warnings |
| old red under the new lint | 57 | 58 (the 77-word Why now sentence) | not run, no stage files for it |
| green `promo-doc-good.md` | 0 / 0 | 0 / 0 | 0 / 0 |
| green under the OLD lint | 0 / 0 | 1 story-lead failure (the `::` heading) | |

Red failures by rule after this round: why-now-one-paragraph 5, story-lead 5, markers-consistent 4,
bare-identifier 4, scope-no-candidate 3, journey-countable 3, why-now-sentence-shape 2,
why-now-opener 2, tenure-months 2, story-paragraphs 2, rntp-leadins 2, no-trait-words 2,
no-semicolons 2, no-process-leak 2, marker-propagation 2, headline-number 2, headline-baseline 2,
and one each of why-now-no-markers, story-links, story-length, scope-current-level,
rntp-contradiction, required-section, relative-first, readiness-first, quote-per-story,
plain-headings, ordering-stamped, one-story-once, one-cr-once, no-star-labels, no-em-dash,
marker-direction, headline-first, date-format, credit-not-subtraction.

New files beside the fixtures: `promo-doc-good.impact-data.md` (8 rows, 6 held, one confirmed-pending
with its marked figure named in the status sentence, one to collect), `promo-doc-good.dates.csv` (12
artifact dates in the order the stories tell them), `promo-doc-bad.impact-data.md` (4 rows, 2
marked), `promo-doc-bad.dates.csv` (two reviews dated against the sentence that orders them).

## check.sh at this commit

```
identity     ok (64 commits, all <public e-mail>)
no-org       ok (no company-specific terms or ids)
schemas      ok (workflows: 1)
frontmatter  ok (10 skills, spec-conformant names and descriptions, frontmatter parses)
loop         ok (6 writer skills: gate, min 2, max 5, house-rules)
glossary     ok (12 glossary keys all defined)
triggers     ok (36 checks, 0 failure(s), 10 skills)
rules        ok (28 rows, every enforcer exists)
promo-lint   ok (red fixture fails with 79 lines and 65 failures, 62 failures without its stage files, green fixture 0 failures and 0 warnings with and without, flattened red fixture linted through the fallback, copy check 1 run(s) on red and 0 on green)
instance     skipped (VSTACK_INSTANCE not set)
```

The promo-lint group now runs the red fixture with and without its stage files and requires the
stage files to add failures with `marker-propagation` and `ordering-stamped` among them, and runs the
green fixture both ways requiring 0 failures and 0 warnings each time. Every other genre's group is
unchanged and green.

## Commits

| Commit | What |
|---|---|
| `e2ba4a4` | lint rules, both fixtures, four stage files, check.sh |
| `bce91a8` | template, house rule credit-inline, checklist H, SKILL stage-document section |
| `37bf7c3` | D72 to D80, D62 amended, two class rows in decisions.md |
| `42ac9cf` | this results file (its id added in the next commit) |

## What the instance copies

The instance's workflow passes two arguments and reads these strings into its `draft_contract`.
All regexes are case-insensitive. The same block is in `skills/write-promo-doc/template.md`.

```
arguments to scripts/promo-lint.py:
  --impact-data promo/<alias>/impact-data.md      turns on marker-propagation
  --dates promo/<alias>/dates.csv                 url,date rows (MM/DD/YYYY or YYYY-MM-DD) for ordering-stamped

environment variables the lint reads:
  PROMO_LINT_CANDIDATE_PRONOUN   she | he | they, for why-now-sentence-shape and candidate-subject-share
  PROMO_LINT_CANDIDATE_ALIAS     for scope-no-candidate
  PROMO_LINT_HOUSE_RULES         path override for the no-superlatives line
  PROMO_LINT_UNVERIFIED_HOSTS    comma-separated hosts for marker-direction
  PROMO_LINT_LINK_EXEMPT         comma-separated URL substrings verified by hand

draft_contract.must_not_match, credit-not-subtraction (D74):
with the \w+ (core|design|schema|component) (from|by|authored by) (a|another|a second|the) builder|under (a|another|the) [^.]* design

draft_contract.must_not_match, no-process-leak (D75, the whole lint list):
earlier draft|evidence pull|reviewer of the|readiness row|in the order [a-z]+, then|told once below|working copy|author field|acknowledgement names|on record is|as (hers|his|theirs) is|evidence row|stage document

the form every marker sentence ends on (D75), for a must_match on marked sentences:
\((TO BE CONFIRMED|TO BE COLLECTED(: [^()]+)?)\)\.?$

a collect-marker that explains instead of naming, must_not_match (D75, D46):
\(TO BE COLLECTED: [^()]*\b(because|which|whether|so that|since|as the|as no|as nobody)\b[^()]*\)
```

Impact-data conventions the lint relies on (SKILL "The impact-data stage document"): the status is
the LAST cell of the row, a row holding a held and an unheld figure names the unheld one in the
status sentence that carries the marker, a one or two digit count is matched only with its unit word
(`7 months`, `11 pages`), an inferred year sits in the baseline cell (D78), and a count in the
closing Why now sentence has a row or counts the story headings (D77).

## Not done, and limits

- The one and two digit figure matcher skips a bare count (`18 and 7` in a status cell with no unit
  word), so a marked row in that form is not propagated by the lint. The checklist
  marker-propagation row reads those. An instance that writes `18 reviews and 7 packages` in the
  status sentence gets the lint check.
- ordering-stamped reads the dates it is given. With no `--dates` file and no MM/DD/YYYY in the
  sentence it is silent on two-artifact sentences, and prints one line saying it read the sentences
  only. The checklist ordering-words-stamped stays the blocker for tool stamps.
- rollup-counts-held in the lint counts only projects, initiatives and stories. Services, teams,
  regions and months are the checklist row's, against the impact-data rows.
- D79 (the no-reuse ending) and D78 (the inferred year) have no lint and no red fixture line, by
  design: both are a reviewer's statement or a stage-document cell.
- The instance was read, not edited. Its lock bump, the contract twins above and a fresh reviewer
  are the follow-up item the conductor named.
- Semicolons in this file: 0.
