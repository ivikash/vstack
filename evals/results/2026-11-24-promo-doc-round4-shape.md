# 2026-11-24 promo-doc round 4 shape: the owner's example document, D56 to D71

Follow-up to `2026-11-24-promo-doc-round4-rules.md`, which held the Why now shape open until the
owner's example document had been read. Branch `promo-doc`, on top of `4afd682`. Commits `654bab8`
(house rules and checklist section C, the owner's steer), `bea1300` (template and glossary),
`29e52e2` (lint and all three promo fixtures), `7b518fc` (checklist section H), `70b34fe` (SKILL),
`777054c` (decision log, `decisions.md`, ADR 0001) and this file, the last commit on the branch.
Everything named here is fictional. Counts only, no names, no identifiers.

## What the example showed

The analysis of the owner's example document (read-only, kept in the private workspace, no
sentence or number from it reproduced here) found a Why now of one paragraph that a VP reads as a
story, stories that open on a bold quarter lead and dig the obstacle before the candidate's first
verb, figures that sit beside the verb that produced them, results that end on who uses the thing
now, no printed Ownership sentence, no principles line, and shared work credited inline by
function. Its weak points were trait words in the opening paragraph's close. Each of those became a
rule here, and the owner's steer moved the style half of them into the house rules so every genre
inherits them.

## Where each rule landed

Layer: `lint` is `scripts/promo-lint.py` (failure unless marked warning), `checklist` is
`skills/validate-writing/checklist.md` (section H unless marked C), `house` is
`skills/leadership-writing/house-rules.md`. Red before is the line count the old lint printed on
the old fixtures, red after is the new lint on the new fixtures. Green is `promo-doc-good.md`
(rewritten in the new shape) under the new lint.

| Decision | Rule | Layer | Red fixture line that fires it | Red before -> after | Green |
|---|---|---|---|---|---|
| D56 | why-now-one-paragraph (replaces why-now-wins) | lint, template, SKILL | line 19: a second paragraph, two bold sentences of 8 and 17 words, `(Ambiguity)` after a bold span, a link | 0 -> 5 lines (old content fired 2 of them, the planted bracket and link add 2, the second bold sentence 1) | 0 |
| D57 | why-now-opener | lint, SKILL step 1 | line 17: first sentence has no month count and carries "authored 212 code reviews" | 0 -> 2 | 0 |
| D58 | why-now-no-list, why-now-rollup | checklist (major) | none, judgement | 0 -> 0 | 0 |
| D59 | Ownership sentence removed, D21 amended (owner may overrule) | lint no-star-labels, checklist ownership-verdict and star-order, template, SKILL, house credit-inline, ownership fixture | line 37: "Ownership: originated the cache, executed the fix, operated the rollout." in a task paragraph | 0 -> 1 (ownership-line retired: the old lint failed 3 stories for lacking the sentence, those 3 lines are gone) | 0 (the old green fixture carried 6 Ownership sentences and fails 6 lines under the new lint) |
| D60 | altitude-two-forms, D24 amended (owner may overrule) | checklist altitude-test, template, SKILL, house show-dont-tell technique 5 | none, judgement | 0 -> 0 | 0 (the green fixture's Breakwater story closes on the factual form, "Six builders from the two teams were on the incident call", the other five keep the counterfactual) |
| D61 | principles line configurable, default off (owner may overrule) | glossary `principles.print_line`, template, SKILL, checklist C principle-citation | none, the line is absent from both fixtures now | 0 -> 0 | 0 (five `demonstrated:` lines removed from the green fixture) |
| D62 | story-lead, D52 quarter allowance | lint, template Story lead and Dates rows, SKILL, ADR 0001 | every story (first paragraphs at lines 27, 35, 45, 59, 73) opens without the lead, line 59 carries `**Q2 2026, Seawall Schema:**` on the Quayside story | 0 -> 5 (4 missing leads, 1 wrong project) | 0 |
| D63 | no-trait-words, show-not-tell | lint (list parsed from house-rules.md), checklist C no-trait-words (every genre) and H show-not-tell, house no-superlatives | line 17: "demonstrated exceptional ownership" in Why now, line 39: "deep investigation and was responsible for" in an action paragraph | 0 -> 2 | 0 (the D24 form "A strong Engineer II would have" is exempt and appears five times) |
| D64 | candidate-subject-share (warning), pronoun field | lint, SKILL candidate-facts | lines 39, 49, 77: "Failures dropped", "The migration plan was reviewed", "A dashboard was built", "Adoption was tracked" | 0 -> 1 warning (6 of 11 action sentences, 55 percent) | 0 (14 of 15, 93 percent) |
| D65 | obstacle-first (warning), checklist major | lint, checklist, template, SKILL, house technique 1 | lines 27, 35, 73: situation paragraphs opening on the candidate | 0 -> 3 warnings | 0 (the Breakwater and Tidewater situations gained "Nobody owned the token path as a whole" and "No single source held the schema") |
| D66 | figure-has-verb (warning), checklist major | lint, checklist, house technique 3 | line 79: "40 million events a day for 310 customers by 10/31/2026." | 0 -> 1 warning | 0 |
| D67 | reuse-named (warning), checklist major, house structure rule | lint, checklist, house, template | line 79: "The dashboard is the one stakeholders use.", line 51: a result ending on "the downstream team said thank you" | 0 -> 3 warnings (2 no user named, 1 "stakeholders") | 0 (three green results rewritten to end on the downstream analytics team, the platform team's campaign guide, the on-call rotation's 7 builders) |
| D68 | scope-current-level | lint, template | line 13: Scope of Role is one paragraph | 0 -> 1 | 0 (Scope split into three paragraphs, the middle names Engineer II) |
| D69 | rntp-intro-counts (warning) | lint, template item 5, SKILL | line 85: `## Best reasons not to promote` goes straight to the first `###` | 0 -> 1 warning | 0 (intro paragraph at line 111 counts the two providers) |
| D70 | markers-feedback-exempt | lint markers-consistent skip | none, green case: lines 150 and 154 of the green fixture carry `[Simplicity]` and `[Ownership and Delivery]` in provider text | 0 -> 0 | 0 (would have been 2 failures without the skip) |
| D71 | house rules carry the style, genres carry only structure (owner steer) | house show-dont-tell (seven techniques), no-superlatives (merged list), credit-inline, reuse-named. checklist C no-trait-words, credit-inline. `trait_denylist()` parses the house line | none, the lint reads the list at run time and fails the document if the line is missing or unparseable | n/a | 0 |

Kept without change: D15 (the five printed reason lead-ins, a reviewer asked for them) and D28
(four unlabelled paragraphs per story). Both recorded as kept rows in the decision log.

### The three owner-overrulable rulings

Taken from the conductor as defaults, each a single switch to reverse:

1. **Ownership line removed (D59).** Reverse by restoring the `ownership-line` lint from `4afd682`
   and the template row, and dropping the `Ownership:` clause from `no-star-labels`.
2. **Altitude in two forms (D60).** Reverse by narrowing `altitude-test` back to the D24 form, no
   lint change (the lint never checked the altitude sentence).
3. **Principles line off (D61).** Reverse by setting `principles.print_line` to `true` in the
   glossary, nothing else moves.

### What moved to the house rules (owner steer)

| Analysis section | House rule | Was promo-only before |
|---|---|---|
| 3.1 obstacle first, 3.2 fork with cost, 3.3 figure beside its verb, 3.4 technique per component, 3.5 altitude by who was engaged, 3.6 reuse named, 3.7 actor plus verb | `show-dont-tell` (Voice rules), rewritten to carry the seven techniques, first sentence kept | yes (the template and SKILL described them for stories only) |
| 3.4 denylist | `no-superlatives` (Voice rules), trait words and claim phrases merged into the one banlist, named-provider quotes exempt | yes (the plan was a promo lint list) |
| 6 credit by function | `credit-inline` (Voice rules), new | yes |
| 3.6 durability by who uses it | `reuse-named` (Structure rules), new | yes |

`date-format` and `relative-first` were already house rules from `730e70f` and are untouched. The
promo lint's `no-trait-words` reads the banlist, the trait words and the quoted claim phrases from
the `- **no-superlatives**:` line of `house-rules.md` (path relative to the script,
`PROMO_LINT_HOUSE_RULES` overrides it) and fails the document with a message naming the path when
the file or the line is missing, so the lint and the house rule cannot drift and a broken parse is
never a silent pass. The three `demonstrat-` forms are one pattern that passes a factual object
("demonstrated that", "demonstrated the fix") and fails a trait or principle noun after it.

## Counts before and after

| File | Before (`4afd682`, old lint) | Old content under the new lint | After (`29e52e2` and later) |
|---|---|---|---|
| `promo-doc-bad.md` | 45 failures, 4 warnings (49 lines) | 51 failures, 11 warnings | 57 failures, 13 warnings (70 lines), one planted case per new rule |
| `promo-doc-good.md` | 0, 0 | 24 failures, 6 warnings (13 Why now lines, 6 story-lead, 6 Ownership, 1 Scope, warnings on obstacle, reuse and the reasons intro) | 0 failures, 0 warnings, 284 words in Why now (cap 550), longest story 327 words (cap 500) |
| `promo-doc-bad.flat.md` | `shape: fallback`, 36 failures, 1 warning | 40 failures, 11 warnings | unchanged at 40 and 11 (4 new failures: 1 Scope, 2 Why now, 1 trait word, the rest story-lead, and 10 new warnings through the fallback) |
| copy check, red against the fictional feedback file | 1 run | 1 run | 1 run |
| copy check, green against the same file | 0 runs | 0 runs | 0 runs |
| talent-card and work-summary fixtures | not linted by check.sh (no lint exists for them) | n/a | check.sh green, the new house rule text breaks nothing that check.sh reads (`loop` still finds house-rules in all 6 writer skills, `glossary` 12 keys, `triggers` 36 checks). Those fixtures were not rewritten and no gate run was made over them |

### Settling the candidate-subject-share threshold

The analysis guessed 60 percent. On the fixtures: the green fixture's 15 action sentences open on
the candidate 14 times (93 percent, the one exception is the factual altitude sentence of the
Breakwater story, "Six builders from the two teams were on the incident call", which is counted
because only the D24 form is excluded). The red fixture's 11 action sentences open on the candidate
6 times (55 percent) after four passive sentences were planted. 60 percent separates the two with
a margin on each side and is recorded as `CANDIDATE_SUBJECT_SHARE` in the lint and in D64. A green
document with one factual altitude sentence per story would sit near 80 percent, still above the
line.

### Fixture lessons this round

- The first green rewrite bolded two Why now figures with their baselines ("99.7% (from 4,200 a day
  to 11 a day)", 9 words) and tripped the six-word bold cap written for bold sentences. The cap is
  now six words for a bold span with no digit and twelve for one with digits, so a bolded figure
  with its baseline passes and a bold sentence still fails.
- The first red plant for `candidate-subject-share` landed on exactly 60 percent (6 of 10), which
  is not under the line. A fifth passive sentence took it to 55 percent. The rule is strict `<`.
- `reuse-named` needed "now points" and "pattern to copy" in its verb list after the green
  Quayside result was rewritten to end on the platform team's campaign guide.

## check.sh at this commit

```
identity     ok (60 commits, all one public address)
no-org       ok (no company-specific terms or ids)
schemas      ok (workflows: 1)
frontmatter  ok (10 skills, spec-conformant names and descriptions, frontmatter parses)
loop         ok (6 writer skills: gate, min 2, max 5, house-rules)
glossary     ok (12 glossary keys all defined)
triggers     ok (36 checks, 0 failure(s), 10 skills)
rules        ok (28 rows, every enforcer exists)
promo-lint   ok (red fixture fails with 70 lines, green fixture 0 failures, flattened red fixture linted through the fallback, copy check 1 run(s) on red and 0 on green)
instance     skipped (VSTACK_INSTANCE not set)
```

## Not done

The gate skill was not run in a harness, so the checklist rows (why-now-no-list, why-now-rollup,
show-not-tell, obstacle-first, figure-has-verb, reuse-named, no-trait-words and credit-inline in
section C, the amended altitude-test and ownership-verdict) are text with a quoted-failure form and
no run proves them yet. The talent-card and work-summary fixtures were not rewritten against the new
house rule text and no gate run was made over them, check.sh is the only proof they still hold. The
instance workflow must set `PROMO_LINT_CANDIDATE_PRONOUN` from the new `candidate-facts` pronoun
field and bump its `vstack.lock` for the instance draft to be measured by these rules, and its
`draft_contract` must drop any pattern that keyed on `Ownership:`. The lint's `obstacle-first`,
`figure-has-verb` and `reuse-named` are word-list heuristics at warning level and the checklist
rules of the same name decide. `scope-current-level` keys on the header's `Current Title` and
`Proposed Title` appearing in the second and third paragraphs, a scope file that names the level
differently from the header fails and must be aligned. The lint was committed together with the
fixtures in one commit so check.sh is green at every commit on the branch.
