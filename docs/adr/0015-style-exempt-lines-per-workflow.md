---
title: 0015 A workflow names the lines its countable style rules skip
date: 2026-11-27
area: factory
realm: public
kind: note
status: accepted
---

# 0015 A workflow names the lines its countable style rules skip

## Context

Two workflows carried a shape their owner had agreed that a house rule counts: a metrics table whose header reads `Last week (Fri mm/dd to Fri mm/dd)` with no year, and a task line in another tool's date form (`- [ ] #todo <subject> 📅 YYYY-MM-DD`, which that tool's plugin reads). The instance rules JSON is the house style for every writer, so loosening the date rules there would loosen them for every document. The only line-level exemption the checker had was `exempt_line_prefixes`, also instance-wide.

## Decision

- `scripts/style-check.py` gains `exempt_line_patterns` (regexes, beside `exempt_line_prefixes`) and a `--exempt <regex>` flag: a line that matches is read by no check. Every other line still is.
- A workflow lists its own under `draft_contract.style_exempt` as `{pattern, why}` rows. `vstack check-run`, `vstack record` and `vstack style-check --workflow` pass them to the checker as `--exempt`, `vstack check` compiles each pattern and requires its `why` (the owner's ruling it records), and the rendered prompt shows them to the writer beside the shape rules. `must_match` and `must_not_match` still read every line.
- The instance rules JSON stays the house style. An exemption is scoped to one workflow and names its reason.

`--selftest` proves the two listed lines are not read while the table body and the prose beside them still are, and that without the patterns every date counts.

## Alternatives

Loosening the instance date rules: every document would lose the check. A second rules JSON for those two workflows: `gate-policy.json required_style_rules` makes one file mandatory and `vstack check` fails a writer that names another. Rewriting the agreed shapes: the owner ruled they stay.

## Consequences

A workflow can keep an owner-agreed shape without a standing finding, and the exemption is visible in the workflow file, the prompt and `vstack check`. A pattern that matches more than the agreed line hides findings on those lines too, so a pattern is anchored to the shape (`^...$`).
