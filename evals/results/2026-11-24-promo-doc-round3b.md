# 2026-11-24 promo-doc round 3b: the ten "What the gate missed" items

Follow-up to `2026-11-23-promo-doc-round1c.md`. Branch `promo-doc`, from `0c6a165`. Commits
`a27b82a` (lint rules and the Sources line), `07bfd9a` (copy check), `ac99470` (checklist, SKILL,
house rule) and the commit carrying this file with decision rows D31 to D40. Everything named here is
fictional. Counts only.

## Where each item landed

| # | Item | Lint | Checklist | Writer rule (SKILL or template) | Decision |
|---|---|---|---|---|---|
| 1 | no-process-leak | blocker, regex over the body, frontmatter and Sources line exempt | blocker, the phrases the regex cannot match | SKILL output discipline names the phrases | D31 |
| 2 | journey-countable | major, action paragraph with no journey verb and no other person | journey-in-action kept as the judgement twin | SKILL action paragraph names the lint | D32 |
| 3 | rntp-contradiction, document-wide | approximation: project in a marked story sentence and in an unmarked reason sentence with an initiative phrase | blocker, widened to every reason against every story and marked claims | none | D33 |
| 4 | asana-date-role | none (no countable form) | blocker, quoted-failure form | SKILL "Task-tracker dates and other builders' fixes" | D34 |
| 5 | provider-gap-fallback | none | blocker, reads the gap analysis "Provider gaps first" table when Feedback is a placeholder | SKILL section of the same name | D35 |
| 6 | Sources line without semicolon | no-semicolons has no exemption left, `vstack check-run` accepts the new line | required-sections note updated | template row and step 9, SKILL output discipline | D36 |
| 7 | one-cr-once | major, CR-n, PR #n, /pull/n and /reviews/n in the action paragraphs | major, a review named in words | template row | D37 |
| 8 | marker-direction | major failure for an unfetchable link without the marker, warning for a bare (TO BE CONFIRMED) | major, decides the warnings | template row | D38 |
| 9 | copy-check | `scripts/promo-copycheck.py` (new), wired into `check.sh promo-lint` | blocker | SKILL "Copy check" | D39 |
| 10 | plain-headings denylist | major, nine words | kept for the rest | house rule plain-headings carries the list | D40 |

Lint: 6 of 10 (items 1, 2, 3 as approximation, 7, 8, 10) plus the Sources change and the new copy
check script. Checklist: 9 of 10 carry a row (all but item 6). Writer rule only: item 4 and item 5
have no countable form.

## Counts before and after

| File | Before (`0c6a165`) | After (this commit) |
|---|---|---|
| `promo-doc-good.md` | 0 failures, 0 warnings | 0, 0 (three wording edits: a told-once sentence, a heading with a denylist word, a bare confirmed-marker given its number) |
| `promo-doc-bad.md` | 32 failures, 1 warning | 37 failures, 3 warnings (one new case per lint rule: process sentence in Why now, unmarked initiative claim in a reason, one review id in two action paragraphs, unfetchable link without its marker, two bare confirmed-markers as warnings, the existing jargon heading now also fails plain-headings) |
| old `promo-doc-bad.md` under the new lint | n/a | 35 failures, 1 warning (plain-headings and two journey-countable lines fire on the old content with no fixture edit) |
| `promo-doc-bad.flat.md` | `shape: fallback`, 33 failures, 1 warning | `shape: fallback`, 36 failures, 1 warning |
| copy check, red fixture against the fictional feedback file | n/a | 1 run, exit 1 |
| copy check, green fixture against the same file | n/a | 0 runs, exit 0 |

## check.sh at this commit

```
identity     ok (42 commits, all one public address)
no-org       ok (no company-specific terms or ids)
schemas      ok (workflows: 1)
frontmatter  ok (10 skills, spec-conformant names and descriptions, frontmatter parses)
loop         ok (6 writer skills: gate, min 2, max 5, house-rules)
glossary     ok (11 glossary keys all defined)
triggers     ok (36 checks, 0 failure(s), 10 skills)
rules        ok (28 rows, every enforcer exists)
promo-lint   ok (red fixture fails with 40 lines, green fixture 0 failures, flattened red fixture linted through the fallback, copy check 1 run(s) on red and 0 on green)
instance     skipped (VSTACK_INSTANCE not set)
```

## Not done

The gate skill was not run in a harness, so the checklist rows are text with a quoted-failure form
and no run proves them yet. The host and exemption lists for marker-direction are environment
variables the instance workflow must set (`PROMO_LINT_UNVERIFIED_HOSTS`, `PROMO_LINT_LINK_EXEMPT`),
no internal host is in public. GLOSSARY unchanged, no new term. The instance lock still pins an
older commit.
