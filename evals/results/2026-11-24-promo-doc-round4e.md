# Promo-doc round 4e: section H rows 1 to 5 of the round 4b review into the gate

Branch `promo-doc`, from `bbe0955` (round 4c). Input: the instance review's section H, six rows of
what the gate still could not see on the second end-to-end draft. Rows 1 to 5 land here as lint
rules, a checklist blocker, template and house-rule text and decision rows D81 to D85. Row 6 is a
ruling D79 already covers and is not built. Nothing in this repo names a real candidate, team,
project, document or figure, the fixtures are the fictional Harbor Telemetry case.

## Fixture counts

Red fixture `evals/fixtures/promo-doc-bad.md` with its stage files (`--impact-data`, `--dates`),
green fixture `evals/fixtures/promo-doc-good.md` the same way and bare.

| After commit | Red failures | Red warnings | Red failures, no stage files | Green |
|---|---|---|---|---|
| bbe0955 (before) | 65 | 14 | 62 | 0 failures, 0 warnings |
| 1. ordering-stamped over every paragraph | 66 | 14 | 62 | 0 / 0 |
| 2. dates-printed-match-csv | 67 | 14 | 62 | 0 / 0 |
| 3. credit paraphrase regex | 68 | 14 | 63 | 0 / 0 |
| 4. why-now-matches-story (checklist) | 68 | 14 | 63 | 0 / 0 |
| 5. why-now-sentence-shape floor | 68 | 15 | 63 | 0 / 0 |

The rule 4 fixture clause passes every lint rule by design: it is the sentence the checklist
reviewer quotes, and the lint cannot read it.

## The rules

| # | H row | Rule | Layer | Fires on the red fixture with |
|---|---|---|---|---|
| 1 | 1 | `ordering-stamped` reads every paragraph between the Headline and the quote (situation, task, action, result), D73 severities unchanged. Checklist `ordering-words-stamped` adds the created-stamp-against-close-stamp note for a tracker task paired with a document | lint blocker on two dated artifacts, warning on one | the Impact story's task sentence "took the dashboard in ticket 2610 after the adoption dashboard note had closed", csv rows 09/02/2026 and 09/04/2026 |
| 2 | 2 | `dates-printed-match-csv`: with `--dates`, a MM/DD/YYYY within 40 characters of a linked artifact equals that artifact's csv row, the nearest link owns the date, a link with no row is skipped. The csv holds SHIPPED dates and the draft prints shipped dates (SKILL.md conventions, template row) | lint blocker when `--dates` is given, skipped with one line otherwise, check.sh requires it to fire on red | "A dashboard was built on 08/02/2026 on the derivation from review 5010", csv row 08/20/2026 |
| 3 | 3 | `credit-not-subtraction` regex gains the `onto|into|on top of ... core|design|schema ... teammate|builder|team` alternative, house rule and checklist name the paraphrase family and the function-before-or-beside passing form | lint blocker, checklist blocker for the paraphrases the regex misses | "bolted the jittered refresh onto a cache core a teammate wrote to a design the team had settled" |
| 4 | 4 | `why-now-matches-story`: every Why now clause about a project is a subset of a sentence in that project's story, a limited scope (one region, one account, one wave) is not widened | checklist blocker, no lint | Why now "shipped tagging for every resource type in all 9 regions" against a story of 4 types and no region |
| 5 | 5 | `why-now-sentence-shape` floor: a Why now sentence under 10 words with no figure of its own warns, a figure followed within 24 characters by above, below or earlier is a cross-reference | lint warning | "Lighthouse Parser carries the 40 million above." |

## check.sh at the last commit

```
identity     ok (71 commits, all <public e-mail>)
no-org       ok (no company-specific terms or ids)
schemas      ok (workflows: 1)
frontmatter  ok (10 skills, spec-conformant names and descriptions, frontmatter parses)
loop         ok (6 writer skills: gate, min 2, max 5, house-rules)
glossary     ok (12 glossary keys all defined)
triggers     ok (36 checks, 0 failure(s), 10 skills)
rules        ok (28 rows, every enforcer exists)
promo-lint   ok (red fixture fails with 83 lines and 68 failures, 63 failures without its stage files, green fixture 0 failures and 0 warnings with and without, flattened red fixture linted through the fallback, copy check 1 run(s) on red and 0 on green)
instance     skipped (VSTACK_INSTANCE not set)
```

Invocation, from the repo root: `bash scripts/check.sh`. The promo-lint group now also requires
`dates-printed-match-csv` among the failures the red stage files add.

## Commits

| Commit | Content |
|---|---|
| `585fa06` | ordering-stamped over every story paragraph, checklist note, template row, red task sentence, two csv rows |
| `48400f6` | dates-printed-match-csv, SKILL shipped-date convention, template row and arguments line, check.sh red requirement, red created date |
| `f50fc27` | credit paraphrase regex in lint and template twin, house rule credit-inline, checklist credit-not-subtraction, red sentence |
| `35638d3` | checklist why-now-matches-story, template Why now row, red widened clause |
| `9c06bc8` | why-now-sentence-shape floor warning, red cross-reference sentence |
| `79f53bc` | decision log D81 to D85, class row in decisions.md |
| this file | results record |

Every commit was pushed to `origin promo-doc` on its own before the next. `main` is untouched.

## Exact strings the instance copies

Argument names and the lines the lint prints when they are absent:

```
--dates <url,date csv>        rows `url,date`, MM/DD/YYYY or YYYY-MM-DD, the SHIPPED date of each artifact
                              read by ordering-stamped and dates-printed-match-csv
absent: "ordering-stamped read dates from the sentences only, dates-printed-match-csv skipped: no --dates <path>"
--impact-data <impact-data.md>  unchanged from round 4c
```

Rule names as they print, for the instance's contract and bar-check: `ordering-stamped`,
`dates-printed-match-csv`, `credit-not-subtraction`, `why-now-sentence-shape` (the floor prints as
`warning why-now-sentence-shape Why now: sentence <k> runs <n> words, floor 10, ...`), checklist
`why-now-matches-story`.

credit-not-subtraction (D74, D83), `draft_contract.must_not_match`, case-insensitive, one string:

```
with the \w+ (core|design|schema|component) (from|by|authored by) (a|another|a second|the) builder|under (a|another|the) [^.]* design|\b(onto|into|on top of) (a|an|another|the) (\w+ ){0,3}(core|design|schema) ((that|which) )?(a|another|the) (teammate|builder|team)\b
```

Constants: `DATE_LINK_WINDOW = 40` (characters between a printed date and the link that owns it),
`WHY_NOW_SENTENCE_FLOOR = 10` (words), `CROSS_REFERENCE = \b(above|below|earlier)\b` read over the
24 characters after a figure. The dates csv convention the instance's SKILL stage notes copy: the
csv row is the shipped date, the draft prints the shipped date beside the link, a created date that
is the story is written as "opened MM/DD/YYYY, shipped MM/DD/YYYY" with the shipped date beside the
link and the exception recorded in the impact-data row's baseline cell.

## Limits

- `dates-printed-match-csv` takes the nearest link as the owner of a date. A sentence that prints
  one date between two links at equal distance is owned by the first link in text order.
- The credit regex alternative needs the owner phrase (`a teammate wrote`, `the team had settled`)
  within the same clause after the noun. "to a design the team had settled" with `to` is the
  checklist's, not the lint's, so a draft can still carry it past the lint.
- The floor reads 24 characters after a figure for a cross-reference word, so "the 85% in the
  Breakwater sentence above" (more than 24 characters) counts as the sentence's own figure.
- `why-now-matches-story` has no countable twin, the fixture clause is the reviewer's example only.
- At the public head the lint was not run over the instance draft, the instance item does that.
