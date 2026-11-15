---
name: Write Exec Update
description: Write a leadership status update (program, project, or org update for executives) from a supplied evidence object. Produces an overall line, one status block per tracked section or workstream (RED/YELLOW/GREEN with a projected Green-by date when RED), near-term milestones, top risks, due action items, and a Known Gaps section. Use when a caller has gathered status evidence and wants the standard executive update. Does NOT fetch data; the caller provides the evidence.
disable-model-invocation: false
---

# Write Exec Update

You turn a supplied, structured evidence object about a program, project, or organization into a
standard leadership status update, ready to send to executives. This skill is domain-agnostic: the
caller passes the update's name and a list of tracked sections (workstreams, waves, regions, teams,
or whatever it tracks), and you render them in a fixed shape aimed at a senior, time-poor reader.

You do **not** fetch data. The caller provides the evidence object: the name, an overall status, a
list of sections (each with status, summary, milestones), risks, action items, and known gaps, with
an evidence pointer on every fact (a source document, a message, a ticket, a dashboard, or a dated
meeting note). If evidence is missing, do not invent it; leave it out, label it `(unverified)`, or
record it under Known Gaps.

First read [leadership-writing/house-rules.md](../leadership-writing/house-rules.md) and apply every rule in it.
This skill adds only the rules specific to an executive status update below.

## Output discipline (read first)

- Return ONLY the finished update. The FIRST line is the header; the LAST line is the end of the
  Known Gaps section. No preamble, no "Here is", no notes about your tools, evidence, or process.
- Before returning, scan your output and DELETE any sentence that talks about writing the update
  rather than being the update. A leaked process sentence (and any em-dash inside it) is a blocker.
- Write for a reader who spends thirty seconds: lead with status and the one fact that justifies it.

## Exec-update-specific rules

- **claim-cites-artifact**: Every significant status claim is backed by a concrete artifact in the
  evidence (a metric, a ticket, a review, a source-document cell, a message, or a dated meeting
  note). A bare claim with no artifact fails.
- **label-projected**: If a number is a projection, a load-test figure, or a target rather than a
  realized result, say so explicitly. Never present a target or projected date as realized.
- **green-by-when-red**: Whenever a section is RED or AT RISK, include a `Green by: mm/dd` line
  giving the projected date it returns to GREEN, taken from the evidence (the recovery milestone or
  the blocking item's estimated completion date). If the evidence gives no such date, write
  `Green by: (unverified)` and add a Known Gap. Omit the line when the section is GREEN or ON TRACK.
- **green-by-future**: A `Green by` date must be strictly after the report date. A section that is
  RED today cannot have gone green in the past, so a `Green by` on or before today is a blocker;
  the correct value is `Green by: (unverified)` with a Known Gap noting the slip. Do not reuse a
  blocking item's already-passed date.
- **date-has-justification**: Every `Green by` date, and every projected or new date that differs
  from the source's original, is followed by a "(because ...)" reason grounded in the evidence (the
  milestone, unblock, dependency, or decision it is tied to). A bare projected date fails.
- **top-risks-present**: Include a consolidated Top Risks section listing the most serious open or
  in-progress risks across sections (or an explicit "none open"). A missing Top Risks section fails.
- **section-coverage**: Every section the caller listed appears as a block, in the order given, and
  no extra sections are invented.
- **date-conflict-surfaced**: When two sources disagree on a date or status, prefer the more recent
  dated source, use it, and note the conflict under Known Gaps. Silently picking one date fails.

## Evidence-only rule

Use ONLY the fields in the supplied evidence object. Never present a target or projected date as a
realized result. When a fact is not in the evidence, it does not go in the update.

## Structure

Follow [format.md](format.md) exactly: header + overall line, one block per section in the order the
caller supplied, near-term milestones, top open risks, due action items, and a single Known Gaps
section. Use the name and section labels the caller provides; do not invent sections.

## Built-in validation loop (always, before returning)

A draft never leaves this skill unchecked. After the first full draft:

1. Read [validate-writing/SKILL.md](../validate-writing/SKILL.md) and
   [validate-writing/checklist.md](../validate-writing/checklist.md) and apply them to your own
   draft in **gate** mode, using the doc type `exec-update`.
2. Apply every quoted fix. Re-run the gate. Repeat until a pass reports zero blockers and zero
   majors, with a minimum of two passes and a maximum of five.
3. If blockers remain after the fifth pass, keep the draft and append a closing `**Known Gaps**`
   note listing each unresolved failure verbatim. Never hide an unresolved blocker and never
   resolve one by inventing a fact.
4. Return only the final draft (plus the Known Gaps note when required): no pass counts, no
   validation report, no process sentences. A caller that wants the report runs
   `/validate-writing` in evaluate mode separately.
