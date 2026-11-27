# Rules and what enforces them

Every rule this repository lives by, paired with the check that makes breaking it fail. A rule with
no enforcer is a wish. When a rule is broken twice, the fix is a new row in the right-hand
column, not a stronger sentence in a document. (The discipline is pstack's `/correct`: fix the
class at the highest level that works, architecture first, docs last.)

| Rule | Enforced by | Level |
|---|---|---|
| Public commits use the personal e-mail, private commits the work e-mail | `scripts/check.sh identity` (public), the instance's own check (private) | check |
| No company term, host, ticket, chat, doc or account id in any public file | `scripts/check.sh no-org` denylist | check |
| The instance lives outside the public checkout and has no public remote | `scripts/check.sh instance` with `VSTACK_INSTANCE` | check |
| Skill frontmatter follows the Agent Skills spec (name = directory, lowercase-hyphen, max 64; description non-empty, max 1024) and parses as YAML (no unquoted `: ` inside a value) | `scripts/check.sh frontmatter`, `vstack verify-skills` | check, engine |
| Every skill description carries a trigger phrase and wins its own prompts | `scripts/trigger-eval.py` (36 cases) via `check.sh triggers` | check |
| Every writer runs the gate: minimum 2 passes, maximum 5, reads house-rules | `scripts/check.sh loop` | check |
| Every glossary key a skill references exists | `scripts/check.sh glossary` | check |
| Every JSON file parses and the example instance passes the invariants | `scripts/check.sh schemas` | check |
| Writers and gates never fetch | writers receive evidence.json only; `vstack check` invariant 2; the derived map (`vstack map`) has no W/G to S edge by construction | engine |
| Every writer has exactly one gate, `min_passes` at least 2 | `vstack check` invariant 3, `schema/workflow.schema.json` | engine |
| Every sink records; ledger fields never empty | `vstack check` invariant 4 | engine |
| The private component records only dates, ids and counts | `vstack check` invariant 5 (field pattern) | engine |
| Every workflow can run with no side effects | `vstack check` requires `sink.dry_run_path`; a `<workflow>.sample.json` beside it feeds `--dry-run` | engine |
| A writer reads at least two sources, or the connectors the workflow requires | `vstack check` coverage (`coverage.min_sources`, `coverage.require_connectors`) | engine |
| A run is done when its artifacts exist, not when the model says so | `verify_contract` in `vstack run`; status becomes `contract_unmet`; `vstack check-run <dir>` | engine |
| Gather uses read-only tools; the only write outside the run dir is the sink | prompt stage 0 runner contract; Claude `--allowedTools`; Kiro `vstack-runner` agent from `vstack gen-agent` | prompt, harness |
| The reader sees which sources were used and which were unavailable | `Sources:` header required by the contract; writer rule | contract |
| The human reads a brief, not the draft | `brief.md` of exactly three lines required by the contract | contract |
| A passed gate rule names what it checked | validate-writing `## Red flags`; stage 4 verification rule in the prompt | skill, prompt |
| High-stakes drafts get an independent critic | `gate.second_opinion` or `--second-opinion <harness>`; findings recorded in meta.json, never block | engine |
| The same mistake is not made twice | `vstack retro` lists recurring Known Gaps and asks for an enforcer per line; this table | process |
| A correction to a document's shape is enforced, not remembered | `draft_contract.must_match` / `must_not_match` on the workflow, checked by `verify_contract` on every run (`contract_unmet` on a miss) and printed into the prompt's Done-means block; `vstack check` refuses an invalid pattern. The instance's `context/<workflow>/mistakes.md` holds the dated correction each rule encodes | engine, contract |
| A promotion story is STAR under a Headline with a number and a baseline, under 500 words, with one quote line, and the two round-bracket markers only | `scripts/promo-lint.py` on every `write-promo-doc` draft: `scripts/check.sh promo-lint` on the fixtures (red must fail, green must pass), `check_promo_lint` in `verify_contract` for `vstack check-run` (`contract_unmet` on a failing line). Shapes pinned in `write-promo-doc/template.md` | check, engine, contract |
| A promotion document is written only after a readiness verdict, never against `Not ready` | `readiness-first` in `scripts/promo-lint.py` (gap-analysis.md beside the draft) and checklist section H | check, skill |
| Judgement rules on a promotion document (criterion fit, journey, altitude, ownership verdict, contradiction, provider gaps, Why now order) fail with the offending text quoted | `skills/validate-writing/checklist.md` section H, applied by the gate; `evals/results/<date>-promo-doc.md` records what each layer caught | skill |
| A decision from a review is a code artifact, not chat | `docs/decisions/<date>-<topic>.md` (one table, enforcer per row) and `decisions.md` at the root (one row per class of mistake) | process |
| Excuses have rebuttals | `skills/leadership-writing/rationalizations.md`, read by every writer and the validator | skill |
| Every run is counted, by any harness path | `vstack record` appends the `runs.jsonl` line and is the last step of the rendered prompt, idempotent by run id | `vstack record`, prompt stage 6 |
| Every run measures itself the same way | `scorecard.json` per run dir, engine-computed, schema `schema/scorecard.json`, trends and two-in-a-row flags in `vstack retro` | `vstack record`, `vstack retro` |
| Every writer loops | a writer workflow with no gate, or a gate with min_passes under 2 or max_passes over 5, fails `vstack check` | `vstack check` |
| Edits to a landed document feed the contract | `vstack reflect` diffs the landed document against draft.md 24 h and 7 d after landing, files wording and structure edits as proposals, fact edits as mistakes, counts deletions, auto-applies a proposal seen twice | `vstack reflect` |
| A workflow never creates a document per run | `documents.json` in the instance lists the rolling documents and the per-event kinds (folder, template-fixed title). A document-writing sink whose `document` is neither fails `vstack check` | `vstack check` |

Rows marked `skill` or `prompt` are the weakest kind: nothing fails when a model ignores them. Each
one is a candidate for promotion to `contract` or `engine` as soon as a run shows it ignored.
