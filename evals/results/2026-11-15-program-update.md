# 2026-11-15 program-update fixture, three harnesses

Cell `example-instance/cells/program-update.json` run with `--dry-run --no-publish` on its fixture.

| Harness | Exit | Seconds | Gate passes | Status |
|---|---|---|---|---|
| claude | 0 | 128 | 2 | known_gaps (fixture carries a conflicting date on purpose) |
| codex | 0 | 141 | 3 | known_gaps |
| kiro | 0 | 189 | 2 | known_gaps |

Must: one block per section in the supplied order, Green-by on the RED block, Known Gaps naming the conflicting date. Held on all three. Must not: a target presented as done. Held on all three.
