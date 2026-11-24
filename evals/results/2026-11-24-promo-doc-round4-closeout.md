# 2026-11-24 promo-doc round 4 close-out: section H of the round 4c review, D86 to D90

Follow-up to `2026-11-24-promo-doc-round4e.md`. Branch `promo-doc` from `34437ac`, main untouched.
Input: the round 4c close review's section H, "What the gate still cannot see", five rows, each a
judgement miss no lint, contract or checklist rule caught on the live draft. Every row became a rule
or a convention so no finding stays only in a report. Everything named here is fictional. Counts
only, no names, no identifiers.

## Where each row landed

| Decision | Row | Rule | Layer | Red fixture line that fires it | Red warnings added |
|---|---|---|---|---|---|
| D86 | 1 | dates-csv-coverage | lint warning with `--dates`, check.sh requires it on red, template Dated links row, checklist ordering-words-stamped coverage paragraph, SKILL convention | a result sentence "The [launch ticket] closed 10/03/2026 beside the dashboard in [review 5010]", the ticket has no csv row, the review has one. The date sits nearer the ticket, so the ticket warns and the review's dates-printed-match-csv stays quiet | 1 |
| D87 | 2 | headline-no-identifier | lint warning, check.sh requires it on red, template Identifiers in a Headline row, checklist headline-carries-outcome note, SKILL convention. The owner decides per draft | the tagging story's Headline gains "in [review 5101]" | 1 |
| D88 | 4 | reuse-named silent on a held figure | lint (held_rows reads the unmarked impact-data rows, needs `--impact-data`), checklist reuse-named amended, template result step, SKILL convention, D67 amended in place with the date | none in red, by design. Proof on scratch copies of the green fixture below | 0 |
| D89 | 3 | credit-inline verb note | checklist note under credit-not-subtraction (judgement, no lint), house rule credit-inline | none, judgement | 0 |
| D90 | 5 | bar-check counts pasted verbatim | SKILL impact-data conventions, instance mistakes row (instruction only) | none, a convention for the record beside the draft | 0 |

Lint: 3 of 5 (D86, D87 as warnings, D88 as a silence). Checklist: 4 of 5 (D86, D87, D88, D89).
House rule: 1 of 5 (D89). Skill or template: 4 of 5 (D86, D87, D88, D90). check.sh: 2 of 5 (the two
warnings must fire on red).

The attribution rule for D86 is the one dates-printed-match-csv already used: the printed date
belongs to the link with the smallest character gap, and only that link is checked. A link with
no csv row that sits beside another link's date is never the nearest, so it does not warn.

## Counts before and after

| Fixture | Before (34437ac) | After, without stage files | After, with stage files |
|---|---|---|---|
| red `promo-doc-bad.md` | 68 failures, 15 warnings (63 and 15 without stage files) | 63 failures, 16 warnings | 68 failures, 17 warnings |
| green `promo-doc-good.md` | 0 / 0 | 0 / 0 | 0 / 0 |

The red failure count did not move: the two fixture edits add warnings only. The failure lines are
identical before and after except that the tagging story's headline-baseline line now quotes the
longer Headline. headline-no-identifier fires with and without the stage files (16 warnings bare),
dates-csv-coverage needs the csv (17 with).

Red warnings by rule after this round: reuse-named 3, obstacle-first 3, marker-direction 2, and one
each of why-now-sentence-shape, section-length, rollup-counts-held, role-words-held,
rntp-intro-counts, ordering-stamped, headline-no-identifier, figure-has-verb, dates-csv-coverage.

Red failures by rule after this round: why-now-one-paragraph 5, story-lead 5, markers-consistent 4,
bare-identifier 4, scope-no-candidate 3, journey-countable 3, why-now-sentence-shape 2,
why-now-opener 2, tenure-months 2, story-paragraphs 2, rntp-leadins 2, ordering-stamped 2,
no-trait-words 2, no-semicolons 2, no-process-leak 2, marker-propagation 2, headline-number 2,
headline-baseline 2, credit-not-subtraction 2, and one each of why-now-no-markers, story-links,
story-length, scope-current-level, rntp-contradiction, required-section, relative-first,
readiness-first, quote-per-story, plain-headings, one-story-once, one-cr-once, no-star-labels,
no-em-dash, marker-direction, headline-first, dates-printed-match-csv, date-format.

## Scratch proofs for D88 and the D86 attribution (not committed)

Copies of the green fixture in a temp directory, linted with the green stage files:

| Copy | Change | With `--impact-data` | Without |
|---|---|---|---|
| held ending | the schema story's result paragraph gains a last sentence "The derivation deleted 2,300 lines of hand-written mappings across 180 pipelines." (impact-data row 5 holds both figures) | 0 failures, 0 warnings | 0 failures, 1 warning: reuse-named on that sentence |
| attribution | the credential story's review link becomes "[the storm ticket](no csv row) and [review 4902](csv row) on 11/12/2025" | 0 failures, 0 warnings (the date is nearest review 4902, which the csv holds, so neither rule speaks) | same |

## check.sh at this commit

```
identity     ok (77 commits, all <public e-mail>)
no-org       ok (no company-specific terms or ids)
schemas      ok (workflows: 1)
frontmatter  ok (10 skills, spec-conformant names and descriptions, frontmatter parses)
loop         ok (6 writer skills: gate, min 2, max 5, house-rules)
glossary     ok (12 glossary keys all defined)
triggers     ok (36 checks, 0 failure(s), 10 skills)
rules        ok (28 rows, every enforcer exists)
promo-lint   ok (red fixture fails with 85 lines and 68 failures, 63 failures without its stage files, green fixture 0 failures and 0 warnings with and without, flattened red fixture linted through the fallback, copy check 1 run(s) on red and 0 on green)
instance     skipped (VSTACK_INSTANCE not set)
```

The promo-lint group now also requires `warning dates-csv-coverage` and `warning
headline-no-identifier` lines on the red fixture with its stage files. Every other group is
unchanged and green.

## Commits

| Commit | What |
|---|---|
| `17c5b87` | lint: the two warnings, held_rows and the reuse-named silence, red fixture lines, check.sh |
| `fdade2c` | template rows, checklist H notes, house rule credit-inline verb clause, SKILL conventions |
| `e8a6098` | D86 to D90, D67 amended in place, one class row in decisions.md |
| `f099c46` | this results file (its id added in the next commit) |

## What the instance copies

No new argument and no new environment variable. The two new rules are warnings, so the instance
adds no contract twin for them (a twin exists only for a countable failure). D88 changes a silence,
not a line the contract could count. The instance's lock moves to the new head, its bar-check for
this round pastes the lint's `--counts` lines and the `promo-lint:` line verbatim (D90), and its
mistakes file gains the retyped-figure row.

## Not done, and limits

- D88 has no red fixture line and no check.sh guard: the silence is proven on a scratch copy of the
  green fixture only. A green fixture story ending on its held figure would guard it, at the cost of
  changing a green ending the owner's example shape set.
- headline-no-identifier reads `CR`, `MCM`, `PR`, `review`, `ticket` or `issue` before a number, or a
  link into a `/reviews/`, `/tickets/`, `/mcms/`, `/issues/` or `/pull/` path. An identifier in
  another spelling passes the lint and is the checklist note's.
- dates-csv-coverage reads the 40-character window dates-printed-match-csv uses. A date further
  from its link than that is attributed to nothing and is the checklist's.
- D89 (the credit verb) and D90 (verbatim counts) have no lint, by design: one is judgement over a
  clause, the other a convention for a record the lint does not read.
- Pre-existing, not changed here: the D85 row of the decision log quotes a draft sentence that
  carries a real project name from the live run. It predates this round and check.sh's no-org
  list does not cover it. Noted for the owner.
- The instance was edited only as the dispatch named: lock bump, bar-check-round4g.md, one
  mistakes row, committed locally and not pushed.
- Semicolons in this file: 0.
