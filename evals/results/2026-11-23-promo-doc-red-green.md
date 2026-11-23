# 2026-11-23 promo-doc: independent red/green run

Run by a session that wrote none of the lint, the checklist, the fixtures or the drafts (decision D7).
Public head `bb9f788`. Inputs: `scripts/promo-lint.py`, `skills/validate-writing/checklist.md`
section H, `evals/fixtures/promo-doc-bad.md`, `promo-doc-good.md` with `promo-doc-good.readiness.md`,
a workflow `draft_contract` in the instance shape, and a real red sample held in a private instance
(results summarised here without any content from it). The companion file
`2026-11-23-promo-doc.md` is the author's own run on the fixtures and is confirmed below.

## Lint and contract, as run

| Document | promo-lint | exit | draft_contract unmet |
|---|---|---|---|
| `promo-doc-bad.md` (red fixture) | 28 failures, 1 warning, identical line for line to the author's recorded output | 1 | 6 (Feedback Summary missing, Does not block missing, story heading not followed by Headline, `TODO:`, em-dash, semicolon) |
| `promo-doc-good.md` (green fixture) | 0 failures, 0 warnings | 0 | 0 |
| real red sample (instance) | 41 failures, 0 warnings. 5 `required-section`, 1 `bare-identifier`, 1 `rntp-leadins`, 1 `readiness-first`, 33 `no-semicolons` and `no-em-dash` | 1 | 16 (every must_match misses, three must_not_match hit) |

`scripts/check.sh` with `VSTACK_INSTANCE` set: all ten groups ok (red fixture fails with 29 lines, green 0).

## Judgement rules (checklist H), applied by hand

| Rule | Red fixture | Green fixture |
|---|---|---|
| readiness-first | fail, no readiness table beside the draft | pass, `Readiness: Ready with gaps`, both gaps are reasons |
| criterion-fit | fail, "Seawall Schema: Ambiguity" with a Problem Complexity Situation ("The cause of the mismatches was not obvious ... owned by a different builder") | pass, every Situation carries its heading's marker |
| journey-in-action | fail, Breakwater Action lists ownership verbs and two bare URLs, no ruled-out option | fail on one story by the rule's letter: Pier Alarm Cleanup's Action ("classified all 19 alarms ..., deleted 7, retuned 5 ..., and rewrote the on-call guide") names no ruled-out option and no other person. Five of six pass. Finding G1 |
| altitude-test | fail, no story ends its Action with an altitude sentence | pass, all six Actions end "A strong Engineer II would have ..., not ..." |
| ownership-verdict | fail, "designed and built ... end-to-end ... led the launch" with no `Ownership:` line | pass on the document side, every Task closes with an `Ownership:` line. No ownership audit exists beside a fixture, so that half is not exercised |
| why-now-order | fail, Why now runs "first project ... then ... most recently" with no bold wins | pass, "ordered by impact, then ambiguity, then recency", each win carries its Headline number |
| rntp-shape | fail, both reasons are one paragraph | pass, five parts in order in both reasons, Gap dated |
| rntp-contradiction | fail, reason 1 "Dana does not propose initiatives" vs Breakwater "Dana proposed and drove the shared credential cache" | pass, narrowly: the gap is scoped to the leverage play and Does not block cites the Pier Alarm counterexample. The Onboarding story's "without being asked" is a second counterexample the reason does not cite |
| aspiration-not-gap | fail, "Becoming the operational excellence champion ... should become" | pass, both gaps are dated observations by a named person |
| provider-gap-addressed | fail, the provider's long-documents gap has no reason | pass, vacuously: the fixture has no `## Feedback` section |
| plain-headings | fail, "Cultivating proactive strategic initiative and opportunity identification [Ownership]" | pass, "Proposing the next leverage play before being asked", "Writing shorter decision documents" |

## Class table: what catches each class, failed before and improved after

"Failed before" counts rule lines on the red fixture that name the class (lint output plus the
judgement rules above). "Improved after" is the same count on the green fixture. The last column
records whether the real red sample in the instance was caught by a rule named for the class
(direct) or only because the whole document is not in the template shape (by shape).

| # | Class of mistake | Caught by (red fixture) | Failed before (red fixture) | Improved after (green fixture) | Real red sample |
|---|---|---|---|---|---|
| 1 | Story not in STAR, task, action and result not separated | lint `headline-first`, `star-leadins` (2 stories), contract `**Situation**` and `**Result**` must_match, checklist star-situation | 3 lint lines | 0 | direct (contract Situation and Result lead-ins) |
| 2 | Story under the wrong criterion | checklist criterion-fit, contract `#### [Criterion]` must_not_match | 1 judgement fail | 0 | direct (checklist) |
| 3 | Story too long | lint `story-length` (622 words), `section-length` warning | 1 lint line, 1 warning | 0, largest story 332 words | by shape only (finding R1) |
| 4 | No senior quote on a story | lint `quote-per-story`, contract quote-line must_match | 1 lint line | 0 | direct (contract quote line) |
| 5 | Missing numbers, baselines, dates | lint `headline-number` (2), `headline-baseline` (2), `why-now-wins`, contract Headline-with-digit must_match | 5 lint lines | 0 | direct (contract Headline and markers rules) |
| 6 | Missing hyperlink on a named artifact | lint `bare-identifier` (4), `story-links` (4), checklist links-kept | 8 lint lines | 0 | direct (lint `bare-identifier`, one hit) |
| 7 | Reasons not to promote not in five parts | lint `rntp-leadins` (2), contract `**Does not block**` must_match, checklist rntp-shape | 2 lint lines, 1 judgement fail | 0 | direct (lint and contract) |
| 8 | Gap named but not addressed | lint `rntp-leadins` (missing Does not block and Next), checklist rntp-shape, rntp-contradiction | 2 judgement fails | 0 | direct (contract, checklist) |
| 9 | Jargon in headings | checklist plain-headings | 1 judgement fail | 0 | direct (checklist) |
| 10 | Provider feedback not reflected in the reasons | checklist provider-gap-addressed | 1 judgement fail | 0 (vacuous, no Feedback section) | direct (checklist) |
| 11 | Aspiration used as a reason | checklist aspiration-not-gap | 1 judgement fail | 0 | direct (checklist) |

Classes caught on the real red sample by a rule named for the class: 10 of 11. Class 3 is refused
there by `required-section` only. The gate still fails that document.

## Findings

- R1 (major): the lint's per-story rules (`story-length`, `star-leadins`, `headline-*`,
  `quote-per-story`, `story-links`, `one-story-once`, `why-now-wins`) run only inside `## Evidence`
  over `### <Project>: <Criterion>` headings. A draft in any other shape fails on five
  `required-section` lines and nothing else per story, so classes 3, 4 and 5 are not named on a
  real document that predates the template. Options: accept, because `check-run` only lints writer
  output which is in shape by construction, and keep the out-of-shape sample as the shape test; or
  add a fallback that splits on `#### [<Criterion>]` plus bold titles when `## Evidence` is
  missing. Recommendation: accept, add one docstring line saying the per-story rules need the
  template shape.
- R2 (minor): house-rule lines (`no-semicolons`, `no-em-dash`) fire inside `## Feedback`, which
  the template keeps verbatim ("Never summarise, soften or merge"). On the real red sample 14 of
  41 lines are provider text. Recommendation: skip the two house rules under `## Feedback`.
- R3 (minor): `bare-identifier` fires on a YAML frontmatter `source:` URL. Skip a leading `---`
  block.
- G1 (minor, green fixture): journey-in-action fails Pier Alarm Cleanup's Action by the rule's
  letter. Add a ruled-out option and a person to the fixture ("ruled out muting the 19 alarms
  wholesale because two had paged on real incidents, agreed the list with the on-call lead"), the
  rule is right.
- G2 (note): provider-gap-addressed and the audit half of ownership-verdict are not exercised by
  the green fixture. A fixture with a `## Feedback` section and a `<stem>.ownership.md` would make
  them testable.
- Decision log (item 5): every "Enforced by" in D1 to D27 of
  `docs/decisions/2026-11-23-promo-doc-grill.md` names a rule, template row, config key, ADR,
  glossary entry, check.sh group or bin/vstack function that exists in this tree. Zero rows name a
  missing enforcer. Instruction or process only, the remaining investment: D7 (independent run,
  this file is its first instance), D18 (refuse without rubric and target_level), D20 (three-round
  loop bound), D27 (work-branch pushes).
- Boundary (item 6): grep of the public tree and every blob in its history for every name,
  alias, document id, project codename and internal term in the private extract and the real red
  sample: 0 hits. The only working-tree matches are the owner's own name and e-mail in LICENSE,
  README, check.sh and the schema `$id` URLs. `scripts/check.sh` passes all groups. Not a blocker.
- Lock (item 7, minor): the instance pins public vstack `82031fa`, public HEAD is `bb9f788` (one
  commit, the two decision logs, no engine or lint change). `vstack check` warns. Bump the pin
  after the owner verifies this run.

Not run here: the gate skill in a harness (the judgement rules above are a hand application), and
`vstack check-run` on a real run directory (the contract was run through `check_draft_contract`
loaded from `bin/vstack` by source, same regex loop).
