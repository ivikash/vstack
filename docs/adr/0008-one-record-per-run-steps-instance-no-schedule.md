---
title: 0008 One record per run, gather steps, the instance variable, dry runs never schedule
date: 2026-11-27
area: factory
realm: public
kind: note
tags: [meta, decision, factory]
status: accepted
---
# 0008 One record per run, gather steps, the instance variable, dry runs never schedule

## Context
Four builders ran the engine in parallel from separate worktrees of one instance on 11/27/2026 and each hit the same four edges: a rerun of `vstack record` after a fix kept the first (failed) `runs.jsonl` line, so the dashboard kept saying contract unmet. `gather.step_0` (a generator the worker must run first) was in the workflow JSON but never in the rendered prompt. `record.post_record` and `config` paths were absolute, so a worktree run rendered the main checkout's dashboard. `vstack run --harness kirocrew --no-publish` registered a one-shot scheduled job as a side effect of a hand-driven dry run.

## Decision
- `runs.jsonl` holds one line per run id. `vstack record` replaces the earlier line for the same run id in place, the latest record wins.
- The renderer writes `gather.order` and every `gather.step_N` (in number order) at the top of the GATHER section, before the sources.
- `${instance}` expands in every workflow string to the directory that holds the workflow's `workflows/` dir, or to `--instance` when given. Instances write it instead of an absolute path.
- The `kirocrew` harness never schedules for `--dry-run` or `--no-publish`: it renders, writes `meta.json` with `status: rendered`, and stops. `print` is the hand-driven harness.

## Consequences
- Retro and dashboard counts read the final verdict of a run, never the first.
- A generator-first workflow is visible to the worker without repeating the command in a source note.
- A run from a worktree reads and renders that worktree.
- Reversing any of these means changing `bin/vstack` and `scripts/engine-selftest.py` together.

## Enforced by
`scripts/engine-selftest.py`, run by `scripts/check.sh` group `engine`.

## Source row
engine asks in the four batch build reports of 11/27/2026.
