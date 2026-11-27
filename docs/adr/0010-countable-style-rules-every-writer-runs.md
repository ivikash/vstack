---
title: 0010 Countable style rules every writer runs
date: 2026-11-27
area: factory
realm: public
kind: note
status: accepted
---

# 0010 Countable style rules every writer runs

## Context

A gate scores a writing-style checklist (ADR 0007, `gate.extra_checklists`), and the model doing the scoring can still pass a draft that carries a date with no year, a 90-word sentence, a semicolon, or an acronym nobody expanded. An independent read of 55 landed documents on 11/27/2026 found 33 failing at least one rule a regex can count. A rule a model applies is a wish until something fails when it is ignored (docs/RULES.md).

## Decision

The engine gains `scripts/style-check.py`: the countable half of a writing style, one function, no model call. It counts sentences over a word limit (prose only, a link label is one word), words from a weasel list (table headers, quoted speech and title-like link labels excluded), runs of 2 to 6 capitals whose first use is neither followed by a bracket nor inside one and which no glossary file and no `## Glossary` section of the draft names, `MM/DD` with no year, `YYYY-MM-DD`, links labelled with their URL, semicolons outside table rows, and em-dashes. Every limit, list and glossary path lives in a rules JSON the instance owns. The instance names it once in `gate-policy.json required_style_rules` and it applies to every writer: the rendered GATE section tells the writer to run `vstack style-check` until it prints zero findings, `vstack check-run` runs it on `draft.md` and marks any finding unmet, and `vstack check` fails a rules file that does not exist or parse and a writer whose `gate.style_rules` opts out or points elsewhere.

A title-like link label (one opening with `[`, or a bold link) is exempt from the date, semicolon and em-dash counts: it quotes a document or task title, which is not the writer's prose.

## Alternatives

Per-workflow `draft_contract` regexes for each rule: 60 workflows, 8 patterns each, and every new workflow starts without them. A checklist line alone: the state before this decision. Fixing the landed documents by hand: 580 dates in one folder, and the next run writes them again.

## Consequences

A draft that used to land with an unexpanded team acronym now stops at the contract check until the writer expands it on first use or the instance adds the term to a glossary the rules name. The instance tunes the word list and the allow list in its own JSON, never in the engine. `scripts/engine-selftest.py` style-rules proves the self-test, the GATE line, the no-opt-out check and the check-run behaviour. `scripts/style-check.py --selftest` proves all eight rules fire on a bad text and none on a good one.
