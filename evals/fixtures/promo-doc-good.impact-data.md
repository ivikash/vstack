---
stage: impact-data
candidate: fictional
generated: 2026-11-24
status: complete
---

# Impact data: every number in the draft, its source, its baseline

Fictional stage document beside `promo-doc-good.md`, read by `scripts/promo-lint.py --impact-data`
for the rule marker-propagation (D72). One row per figure. The LAST cell is the status: a row whose
status carries `(TO BE CONFIRMED)` or `(TO BE COLLECTED: <artifact>)` is a marked row, and every
draft sentence that carries one of its figures must end on the same marker. When a row holds both a
held figure and an unheld one, the status cell names the unheld figure in the sentence that carries the marker (row 7), so the held figure
stays free. A year inferred from a page that printed only month and day is recorded in the baseline
cell (row 4), never in the draft (D78).

## Numbers the evidence holds

| # | Number | Baseline or comparator | Source | Evidence holds |
|---|---|---|---|---|
| 1 | 99.7% credential-fetch failure drop (4,200 a day to 11 a day) | 4,200 a day before 12/05/2025 | [review 4902](https://example.com/reviews/4902) description, `evidence/reviews/4902.md` | yes |
| 2 | 40 million events a day for 310 customers | none, an adoption count | `evidence/dashboards/lighthouse-adoption.md` row 10/31/2026 | yes |
| 3 | 9 regions, 3 weeks ahead of the committed date | committed date 03/05/2026 | `evidence/pipelines/lighthouse.md` | yes |
| 4 | Launch 02/12/2026 | the launch page prints "February 12", the year is inferred from the page's 2026 release list | `evidence/pages/lighthouse-launch.md` | yes |
| 5 | Schema sources from 3 to 1, 2,300 lines deleted, 180 pipelines | 3 sources before | [review 5010](https://example.com/reviews/5010) diff stat | yes |
| 6 | 2 teams' codebases, 4 services, 6 projects, 26 months | the roll-up counts of the closing Why now sentence | `evidence/reviews/by-project.md`, the six story headings, the candidate-facts block | yes |

## Numbers the evidence does not hold

| # | Number | Baseline or comparator | Source the draft points at | Status |
|---|---|---|---|---|
| 7 | Pages down 60% (45 to 18 a week), no incident unnoticed in the 7 months since | 45 a week in January 2026 | the on-call dashboard for the page counts, no file for the incident claim | 60% held with its baseline. The 7 months claim is not in any file (TO BE CONFIRMED) |
| 8 | Quote from the campaign owner | none | not yet asked | (TO BE COLLECTED: quote from the campaign owner) |

## Count

8 rows, 6 held, 1 confirmed-pending, 1 to collect.
