---
title: 0009 Readiness mode draft_with_readiness, the document declares it
date: 2026-11-27
area: factory
realm: public
kind: note
status: accepted
---

# 0009 Readiness mode draft_with_readiness, the document declares it

## Context

The promotion-document lint fails `readiness-first` on a `Not ready` verdict: the writer returns the readiness table and gap list, never prose over missing evidence (RULES row, owner decision of 11/23). An owner can still want the draft anyway, as a scaffold that shows the gaps in place, and an instance should be able to say so without weakening the default.

## Decision

The document itself declares the mode. When the draft carries a line opening `**Not ready for submission**` and a `## Readiness` section, a `Not ready` verdict in the readiness table beside it passes `readiness-first` with a warning line (`warning readiness-first: ... declares readiness mode draft_with_readiness`). Without the `## Readiness` section the banner is not enough and the rule fails. A banner over a `Ready` or `Ready with gaps` verdict fails the new `readiness-banner` rule, so banner and verdict always agree. No flag, no environment variable: the reader of the document sees the same declaration the lint keys on.

## Alternatives

A `--allow-not-ready` flag or an environment variable: invisible to the reader of the landed document and not passed by `check-run`, which calls the lint with the draft path alone. Loosening `readiness-first` itself: drops the default rule for every instance.

## Consequences

An instance that wants the mode writes the banner and the section into its draft contract (`must_match` on both when its force setting is on) and keeps the default otherwise. `scripts/check.sh` proves the three cases on the green fixture: verdict Not ready without the banner fails, with banner and section passes with the warning, banner over Ready fails `readiness-banner`.
