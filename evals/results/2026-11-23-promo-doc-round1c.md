# 2026-11-23 promo-doc round 1c: the lint fallback on a sibling rubric heading, no-org over results files

Follow-up to `2026-11-23-promo-doc-round1b.md`, whose closing paragraph left R1 open. Branch
`promo-doc`, commits `493a3ab` (fix 1), `3e810ca` (fix 2) and the commit carrying this file and
decision rows D29 and D30. Inputs: `scripts/promo-lint.py`, `scripts/check.sh`,
`evals/fixtures/promo-doc-bad.flat.md`, the round 1 close review. Everything named here is fictional
except the counts taken from the private instance's real red sample, which are numbers only.

## What failed before

| # | Finding | Evidence at `65a5db9` |
|---|---|---|
| 1 | R1 on the real draft: `fallback_stories` returned 0 stories. The draft puts a second level-4 heading (the rubric sentence) directly under each `#### [<Criterion>]`, so `split_sections(lines, 4)` gave every bracketed heading an empty body and the stories sat under non-bracketed siblings the fallback skipped | Real red sample: 29 failures, no `shape: fallback`, no `story-length`. Flat fixture had no sibling heading, so `check.sh promo-lint` stayed green while that shape was unmeasured. Proof of the gap: the lint at `65a5db9` run on the round 1c flat fixture (sibling headings added) prints 15 failures, 0 `shape` lines and 0 `story-length` lines |
| 2 | `check.sh no-org` scanned `evals/results/*.md` with none of the patterns (only `evals/fixtures/*.md` and `scripts/*.py` were added back after the `evals` exclude). A bare 12-character document id and a bare alias with an at sign and no domain matched nothing in the DENY list | Test file with one fictional alias and one fictional 12-character id placed in `evals/results/`: no-org ok. A six-digit fictional ticket id (`CR-` plus six digits) already sat in the round 1b results file and was never reported |

## What changed

| # | Commit | Change | Enforcer |
|---|---|---|---|
| 1 | `493a3ab` | `fallback_stories` walks the headings itself: a bracketed heading opens a criterion, a non-bracketed heading at the same level is appended to the criterion's body as text (`words` and `paragraphs` already skip heading lines), a shallower heading closes it. `promo-doc-bad.flat.md` gains one sibling rubric heading under each of its five bracketed headings and its intro names the shape | `check.sh promo-lint`: the flat fixture must print `shape: fallback` first and a `story-length` line |
| 2 | `3e810ca` | `evals/results/*.md` joins the second grep so every pattern reaches results files. Two generic shapes added to DENY: a 12-character run of letters and digits with at least one of each (a plain 12-letter word such as "organisation" does not match), and a short lowercase word followed by an at sign that is not followed by a domain (a full address does not match). The round 1b results file's fictional `CR-` six-digit id shortened to four digits, the one true positive | `check.sh no-org` |

## Counts before and after

| File | Before (`65a5db9`) | After (`3e810ca`) |
|---|---|---|
| `promo-doc-good.md` | 0 failures, 0 warnings | 0, 0 |
| `promo-doc-bad.md` | 32 failures, 1 warning | 32, 1 |
| `promo-doc-bad.flat.md` (no sibling heading before, sibling headings after) | `shape: fallback`, 33 failures, 1 warning | `shape: fallback`, 33 failures, 1 warning, `story-length Ambiguity > Seawall Schema: 620 words, cap 500`, `headline-first` once per story (5) |
| round 1c flat fixture under the `65a5db9` lint (red test) | 15 failures, 0 `shape`, 0 `story-length` | n/a |
| Real red sample (private instance, numbers only) | 29 failures, 0 warnings, no `shape`, 0 stories | `shape: fallback`, 8 stories measured, 58 failures, 3 `section-length` warnings, 5 `story-length` lines at 657, 655, 638, 551 and 541 words against the 500 cap |

The round 1 close review measured 6 `story-length` lines on a scratch copy with the sibling headings
demoted to italic prose. On the untouched draft the fallback finds 5, because the demoted heading
text counted as story words there (one story sat at 512 in that copy). The lint now measures the
draft as written.

## check.sh at `3e810ca` plus this commit

```
identity     ok (38 commits, all vikashagrawal1990@gmail.com)
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

Red test of no-org after the change: a file in `evals/results/` holding one fictional alias with a
trailing at sign and one fictional 12-character id makes the group print `FAIL:` and the offending
line. The file was removed before the commit. The D30 decision row first spelled the alias shape
literally and tripped the group itself; the row was reworded, the pattern was not touched.

## Not done

The gate skill was not run in a harness. The instance lock still pins `c23b669`, moving it is the
instance's step. The reviewer's scratch copy under the crew workspace was read for the red test only
and nothing from it is in this repo.
