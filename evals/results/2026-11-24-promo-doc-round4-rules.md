# 2026-11-24 promo-doc round 4: the owner's reading of the first end-to-end document, D49 to D55

Follow-up to `2026-11-24-promo-doc-round3-close.md`. Branch `promo-doc`, recreated from `05d5c83`
(main). Commits `e8c9dba` (lint rules and both fixtures), `b998626504b` (SKILL and template), `730e70f`
(checklist H, house rules, the writer skills' rule lists), `e556caa` (decision rows D49 to D55 and
seven class rows in `decisions.md`), `b465441135c` (this file), `6005d4f` and `8afb111` (this file's commit list
written in a form the no-org id scan accepts). Everything named here is
fictional. Counts only, no names, no identifiers.

## What the owner found

The owner read the first promotion document the workflow produced end to end and marked seven
things no rule had caught: the Scope of Role section talked about the candidate (hire date,
previous team) instead of the team and the proposed level, tenure was counted in days from the
hire date instead of months from the level start, sentences gave the absolute numbers first and
the percentage after them, body dates were year-first, the config keys had chosen which story
came first, the document never said in one place why this person, and Why now carried a marker.
Each became a rule with a decision row.

## Where each rule landed

| Decision | Rule | Layer | Red fixture line that fires it | Count added |
|---|---|---|---|---|
| D49 | scope-no-candidate | lint (name, alias, hire or join word, prior-team sentence), checklist blocker for the rest, SKILL (scope file keyed by level pair, stop and write `questions.md` when missing), template row | line 13, a Scope sentence with the candidate's first name, "joined", a year and "from the <other> team" | 3 (one per class in the sentence) |
| D50 | tenure-months, candidate-facts | lint (header line and Why now), checklist blocker (facts from the block, windows from the level start), SKILL "Candidate facts", template header and Tenure rows | line 9, `Time in Current Level: 790 days`, and line 17, "In 790 days as an Engineer II" | 2 |
| D51 | relative-first | lint (Headline and Why now sentences), house rule line under quantify-impact, checklist section C, template row | line 19, a bold win reading "from 4,200 a day to 11 a day, a 99 percent drop" | 1 |
| D52 | date-format | lint (body, URLs, link targets and frontmatter exempt), house rule (mechanical), checklist section A, the writer skills' rule lists | line 65, a result sentence dated `2026-06-28` | 1 |
| D53 | owner-ranked-stories | checklist blocker, why-now-order widened to read the `story-ranking` table, SKILL "The owner ranks the stories" and the stop in "Inputs, and when to refuse", template Why now and Headline steps | none, the table is a stage document the lint cannot see | 0 |
| D54 | vp-read | checklist blocker, judgement only | none | 0 |
| D55 | why-now-no-markers | lint, SKILL and template Why now rules | line 19, "which cut pages by more than half (TO BE CONFIRMED)" | 1 |

Lint: 5 of 7 (D49, D50, D51, D52, D55). Checklist: 5 of 7 carry a row (D49, D50, D53, D54, and
why-now-order rewritten for D53). House rule: 2 of 7 (D51 as a line under quantify-impact, D52 as
a new mechanical rule), both for every genre. Skill or template: 6 of 7 (all but D54).

The `COMPARATOR` pattern behind `headline-baseline` now also accepts a bare `X to Y` pair, so a
Headline in the new form (`down 60% (from 45 to 18 a week)`) still counts as carrying its baseline.

## Counts before and after

| File | Before (`05d5c83`) | After (`e8c9dba` and later) |
|---|---|---|
| `promo-doc-bad.md` | 37 failures, 4 warnings (41 lines) | 45 failures, 4 warnings (49 lines). One planted case per rule, 8 new lines in total |
| old `promo-doc-bad.md` under the new lint | n/a | 37 failures, 4 warnings (no new rule fires on the old content) |
| `promo-doc-good.md` | 0 failures, 0 warnings | 0, 0. Three wording edits: the Breakwater win and the Pier Alarm Headline now lead with the percentage and carry the absolutes in round brackets, and the Pier Alarm result sentence follows the same form |
| old `promo-doc-good.md` under the new lint | n/a | 0, 0 |
| `promo-doc-bad.flat.md` | `shape: fallback`, 36 failures, 1 warning | unchanged, 36 and 1 |
| copy check, red against the fictional feedback file | 1 run | 1 run |
| copy check, green against the same file | 0 runs | 0 runs |

The first attempt at the D55 case put the marker mid-sentence, which also tripped
`markers-consistent` (a 46th failure). The sentence was split so the marker ends it, the same
lesson as round 3b: a planted case fires one rule, and every fixture edit is recounted.

## Held, not changed

| Item | State | Why |
|---|---|---|
| Why now shape: one opening sentence, three bold wins, one closing paragraph | held as it is, `why-now-wins` still asks for three bold wins with a number | the owner rejects the three bold wins and is sending an example document in the shape they want. A later item changes the shape, the template, the lint and both fixtures together. Nothing in this round depends on the wins being bold or three |

## check.sh at this commit

```
identity     ok (50 commits, all one public address)
no-org       ok (no company-specific terms or ids)
schemas      ok (workflows: 1)
frontmatter  ok (10 skills, spec-conformant names and descriptions, frontmatter parses)
loop         ok (6 writer skills: gate, min 2, max 5, house-rules)
glossary     ok (11 glossary keys all defined)
triggers     ok (36 checks, 0 failure(s), 10 skills)
rules        ok (28 rows, every enforcer exists)
promo-lint   ok (red fixture fails with 49 lines, green fixture 0 failures, flattened red fixture linted through the fallback, copy check 1 run(s) on red and 0 on green)
instance     skipped (VSTACK_INSTANCE not set)
```

## Not done

The gate skill was not run in a harness, so the four new checklist rows are text with a
quoted-failure form and no run proves them yet. The scope file, the `candidate-facts` block and
the `story-ranking` table are instance inputs: their shapes are described in the SKILL, no public
fixture holds them, and the instance workflow must set `PROMO_LINT_CANDIDATE_ALIAS` for the alias
half of `scope-no-candidate`. The lint's `tenure-months` reads a day count only beside a level,
role, tenure or title word, so a delivery figure such as "2 days ahead of the deadline" passes. The
`relative-first` pair pattern needs a `to` between the two absolutes, a pair written "4,200 and
11" is not seen. GLOSSARY unchanged, no new term.
