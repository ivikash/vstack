# 2026-11-15 contract, brief, sources header and second opinion, four harnesses

Same cell as the morning run, now rendered with the done-means contract, the `Sources:` header,
`brief.md` and the runner contract in the prompt. `--dry-run --no-publish`, fixture evidence.

| Harness | Exit | Seconds | Gate passes | Status | Contract | Second opinion |
|---|---|---|---|---|---|---|
| claude | 0 | 221 | 2 | ok | met | codex: 4 findings |
| codex | 0 | 140 | 2 | known_gaps | met | - |
| kiro | 0 | 259 | 2 | known_gaps | met | - |
| kirocrew (async job) | 0 | - | 4 | known_gaps | met (`vstack check-run`) | - |

The second opinion earned its place on the first run: of its four findings, one is a true error
(the draft named an 11/12 event as the next dated item while the evidence holds an 11/10 action),
two are provenance gaps (an overall status and a programme subtitle the evidence does not carry),
one is a wording quibble about `unavailable` versus `skipped`. None blocked; all are in meta.json.

`vstack check-run` on a run from before the contract reports 3 unmet items (no sources list, no
header, no brief), which is the regression the contract exists to catch.
