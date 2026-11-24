# 2026-11-24 promo-doc round 3 close: the eight "What the gate missed" items of the round 3b review

Follow-up to `2026-11-24-promo-doc-round3b.md`. Branch `promo-doc`, from `a7993dc`. Commits
`36a3b0f` (lint warning, copy check flag, red fixture case), `bfddde1` (checklist H and SKILL) and the
commit carrying this file with decision rows D41 to D48. Everything named here is fictional. Counts
only, no names, no identifiers.

## What the round 3b review found

An independent reviewer that wrote none of the material reran the round 3 checklist on the fixed
real draft and its private evidence, read-only. Verdict: round 3 closed. All 11 reviewer classes
pass, 3 of them weak (missing adoption data, a story placement the owner parked, a teaching moment
not yet collected). Of 17 evidence rows rechecked, 0 failed and 2 carried a role word (a seniority
and a product-manager role) that no evidence file held. The copy check left 3 runs, all identifier
or product-name lists. The sink document matched the committed draft block for block. Every gate
count the fixers had claimed reproduced: 0 lint failures, 8 warnings, 0 of 26 contract rules unmet.

The review then listed eight more things the gate let through. Three of them were wording the
reviewer asked to fix in the draft itself (a seniority with no directory row, a product-manager
role resting on a typed quote, a count read as the whole set where the source gives a larger one).
Those three landed in the private instance with a fourth optional one (a Pattern leaning on a
marked story), and the instance lint stayed at 0 failures and the contract at 0 unmet.

## Where each item landed

| # | Item | Lint | Checklist | Writer rule (SKILL) | Instance | Decision |
|---|---|---|---|---|---|---|
| 1 | role words on other people with nothing holding them | `role-words-held` warning, a story paragraph with a role word and no link and no marker | major, reads the evidence | "Roles given to other people" | contract `must_not_match` twin for the ask form (role word plus ask verb on a plain prose line with no link and no marker) | D41 |
| 2 | "asked for by" subject with no audit row | none (the audit is a stage document) | `asked-for-by-audited`, major | same section | none | D42 |
| 3 | a Pattern leaning on a marked story | none (the rntp-contradiction approximation keys on explicit initiative phrases) | `pattern-cites-unmarked`, blocker | "What a Pattern may cite" | none | D43 |
| 4 | ordering words on stamps that disagree | none | `ordering-words-stamped`, major | asana-date-role section extended | none | D44 |
| 5 | a subset count with the definite article | none | `subset-words`, major | "Counts that are a subset" | none | D45 |
| 6 | marker-direction warnings carried past the sink | none new, the warning exists | `marker-warnings-ruled`, blocker before the sink write | "Before the sink" | a parked-findings row naming the four warnings | D46 |
| 7 | copy-check runs also held by a primary source | `promo-copycheck.py --evidence-dir`, prints `source-held` with the file | copy-check row takes the source-held form | "Copy check" extended | gate copycheck line passes the flag | D47 |
| 8 | parked reviewer findings with no record | none | `parked-findings-logged`, major | "Before the sink" | decisions file gains a "Parked reviewer findings" table with 2 rows | D48 |

Lint: 1 of 8 as a warning (item 1) plus the copy check flag (item 7). Checklist: 8 of 8 carry a row.
Writer rule: 8 of 8. Instance contract: 1 twin (item 1). Items 2 to 6 and 8 have no countable form
because each needs a stage document, a stamp, or a decision the draft regex cannot read.

## Counts before and after

| File | Before (`a7993dc`) | After (this commit) |
|---|---|---|
| `promo-doc-good.md` | 0 failures, 0 warnings | 0, 0 (no edit, its one role word sits in a paragraph with a link) |
| `promo-doc-bad.md` | 37 failures, 3 warnings (40 lines) | 37 failures, 4 warnings (41 lines, one new sentence giving a role with no link and no marker) |
| `promo-doc-bad.flat.md` | `shape: fallback`, 36 failures, 1 warning | unchanged, the flat fixture was not edited |
| copy check, red fixture against the fictional feedback file | 1 run, exit 1 | 1 run, exit 1, and `source-held` named when a scratch evidence file holds the same words |
| copy check, green fixture | 0 runs, exit 0 | 0 runs, exit 0, with and without `--evidence-dir` |
| real draft in the instance (private) | 0 failures, 8 warnings, 0 of 26 contract rules unmet | 0 failures, 9 warnings (the new warning on one story paragraph whose role word the owner will rule on), 0 of 27 contract rules unmet. The new contract twin hits 1 line on the pre-fix draft and 0 after |

## check.sh at this commit

```
identity     ok (45 commits, all one public address)
no-org       ok (no company-specific terms or ids)
schemas      ok (workflows: 1)
frontmatter  ok (10 skills, spec-conformant names and descriptions, frontmatter parses)
loop         ok (6 writer skills: gate, min 2, max 5, house-rules)
glossary     ok (11 glossary keys all defined)
triggers     ok (36 checks, 0 failure(s), 10 skills)
rules        ok (28 rows, every enforcer exists)
promo-lint   ok (red fixture fails with 41 lines, green fixture 0 failures, flattened red fixture linted through the fallback, copy check 1 run(s) on red and 0 on green)
instance     ok (outside this repo, no public remote)
```

Head after this commit: see the commit that carries this file on `promo-doc`, parent `bfddde1`.

## Not done

The gate skill was not run in a harness, so the seven new checklist rows are text with a
quoted-failure form and no run proves them yet. `marker-warnings-ruled` has no countable form
because the run contract is a regex over the draft and the engine does not expose the lint's
warning count, a cap is parked until it does. The sentence the review rated low stakes (an ordering
word on stamps three minutes apart) was not changed in the real draft, the owner holds it with the
reviewer's suggested wording. GLOSSARY unchanged, no new term.
