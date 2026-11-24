---
stage: impact-data
candidate: fictional
generated: 2026-11-24
status: complete
---

# Impact data: every number in the draft, its source, its baseline

Fictional stage document beside `promo-doc-bad.md`, read by `scripts/promo-lint.py --impact-data`.
Rows 3 and 4 are marked and the draft prints their figures as fact (Why now prints the 212 review
count, the Seawall Schema action paragraph prints the 11 pages figure), which is what
marker-propagation (D72) fails.

## Numbers the evidence holds

| # | Number | Baseline or comparator | Source | Evidence holds |
|---|---|---|---|---|
| 1 | 99.7% credential-fetch failure drop (4,200 a day to 11 a day) | 4,200 a day before | [review 4902](https://example.com/reviews/4902) description | yes |
| 2 | 40 million events a day for 310 customers | none | `evidence/dashboards/lighthouse-adoption.md` | yes |

## Numbers the evidence does not hold

| # | Number | Baseline or comparator | Source the draft points at | Status |
|---|---|---|---|---|
| 3 | 212 code reviews authored | none | typed in the draft, no query recorded | (TO BE COLLECTED: the review query with its window) |
| 4 | 11 pages in the schema derivation note | none | the page count is typed in the draft, the note itself was not pulled | (TO BE CONFIRMED) |

## Count

4 rows, 2 held, 1 confirmed-pending, 1 to collect.
