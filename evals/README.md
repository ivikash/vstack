# Evals

Two layers keep the skills honest.

## 1. Structural (runs in CI and in the pre-commit hook, no model)

`scripts/check.sh` runs `scripts/promo-lint.py` on the two promo-doc fixtures (red must fail, green must pass) and verifies the repository invariants: every commit uses the public author
e-mail, no company-specific term or internal id appears anywhere, every `SKILL.md` has
spec-conformant frontmatter (agentskills.io), every writer skill carries the built-in validation loop (gate, minimum two passes,
maximum five, reads `house-rules.md`), and every `principles.*` / `rating.*` / `levels.*` /
`roles.*` key a skill references is defined in `leadership-writing/glossary.md`.

## 2. Behavioural (run by hand or by an automation, needs a model)

`sample evidences/` holds synthetic evidence packs. People, projects, metrics and links in them are
invented for testing and belong to no real organisation. The table below states what a passing output must and must not contain. Run a writer skill on the sample evidence, then run
`/validate-writing` in evaluate mode on the result, and compare:

| Fixture | Skill | Must | Must not |
|---|---|---|---|
| `sample evidences/talent-card-evidence.json` | `write-talent-card` | four paragraphs in section 2, `**Growth Areas:**` and `**Manager Support:**` openers, principle in bold in paragraphs 1 and 2, `[TO CAPTURE: ...]` where the sample evidence omits a metric | any rating letter in section 2 prose, any metric not in the sample evidence, any em-dash |
| `sample evidences/exec-update-evidence.json` | `write-exec-update` | one block per section in the supplied order, a Green-by date on every RED block, a Known Gaps section that names the conflicting date in the sample evidence | a milestone presented as done when the sample evidence says target |
| `fixtures/promo-doc-good.md` (+ `.readiness.md`) | `write-promo-doc` output, green sample | `python3 scripts/promo-lint.py` reports 0 failures, every story is a `**Headline**` with a number and a baseline followed by four unlabelled paragraphs in STAR order (D28), one quote line per story, five lead-ins per reason not to promote, `Readiness: Ready with gaps` in the companion with each gap addressed as a reason, only `(TO BE COLLECTED)` and `(TO BE CONFIRMED)` markers | a project told in full twice, a bare review or ticket id, a semicolon outside the Sources line |
| `fixtures/promo-doc-bad.md` | `write-promo-doc` output, red sample | the lint exits 1 and names every lint-side class in `results/2026-11-23-promo-doc.md` (STAR missing, 500-word story, no quote, no Headline number or baseline, bare ids, `TODO` and `TBD` markers, five reason parts missing, no readiness verdict, one project under two headings) and `validate-writing` in gate mode fails criterion-fit, provider-gap-addressed, aspiration-not-gap, plain-headings, rntp-contradiction, ownership-verdict, altitude-test and why-now-order with the quoted forms in checklist section H | a pass from either layer |
| `fixtures/promo-doc-bad.flat.md` | `write-promo-doc`, red sample in the pre-template shape (`#### [<Criterion>]` sections, bold project titles, no `## Evidence`) | the lint prints `shape: fallback` first and still measures every story (the 500-word story, quotes, links, one project under two headings) | a run that fails only on `required-section` |

A behavioural run passes when `validate-writing` reports zero blockers and the Must / Must not
columns hold. Record results in `results/<date>-<sample evidence>-<harness>.md` with the date, harness and model; the first entry is in that folder.
