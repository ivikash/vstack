# Format: Executive Status Update

The update is a header + overall line, one block per tracked section (in the caller's order), a
near-term milestones list, top risks, due action items, then one Known Gaps section. No em-dashes.
The caller supplies the update name and the section list; use them verbatim.

Output uses single-asterisk `*bold*` for headers so it renders in most chat and rich-text
surfaces; if the caller specifies a different target format, follow that instead.

## Header + overall

```
*<Update name>: Status Update (mm/dd)*
Sources: <one short line naming the sources actually used, e.g. status doc, discussion thread, meeting notes dated ...>
Overall: <one or two sentences on overall health and the nearest dated milestone, from evidence>
```

Use the date the caller supplies (`currentDate`) for `mm/dd`.

## Section blocks (caller's order)

Emit one block per section in the evidence `sections` array, in that order. Each block:

```
*<Section label>*: <RED | YELLOW | GREEN | ON TRACK | AT RISK, from evidence>
<one or two sentences: what moved since the last update, what is in flight, and the nearest dated milestone with its owner. Lead with evidence (a ticket, an estimated completion date, a review, a source cell, a meeting date). Label any date that is a target or projection.>
Green by: <mm/dd> (because <reason>)   (REQUIRED only when the section is RED or AT RISK; the projected recovery date from evidence followed by a parenthetical reason tying it to a recovery milestone or unblock, or "(unverified)" with a Known Gap. Omit when GREEN or ON TRACK.)
Counts: <optional. If the section carries done/total counts in the evidence, render them here as "X of N <label> ..." with the not-done items named. Omit if the evidence has no counts.>
```

The `Green by` date MUST be in the FUTURE, strictly after the report date (`currentDate`). A section
that is RED today cannot have turned green on a past date. If the only date in the evidence is on or
before `currentDate`, it has already slipped and is NOT a valid recovery date: write
`Green by: (unverified)` (slipped past its date, new date not set) and record the slip under Known
Gaps. Never place a past or same-day date in `Green by`, and do not reuse a blocking item's stale
date as the recovery date.

EVERY new or projected date (the `Green by` date, and any date that differs from what the source
originally stated) MUST be followed by a `(because ...)` reason grounded in the evidence: the
milestone, unblock, dependency, or decision it is tied to. A projected date with no justification is
not allowed; if you cannot state why, the date is `(unverified)`.

If the evidence has no movement for a section, write one sentence stating its current state and the
next milestone. Do not pad.

## Near-term milestones (next ~2 weeks)

```
*Near-term milestones*
- <mm/dd> - <milestone> (<owner>, <ref if any>) - <state: done | in progress | at risk; label targets>
```

List milestones from the evidence whose date falls within about two weeks of `currentDate`, soonest
first. If none, write `- none in the next two weeks`.

## Top risks

```
*Top risks*
- <risk> (owner <name>, target <mm/dd>, <status>) - <one-line mitigation from evidence>
```

List risks the evidence marks open or in progress, highest impact first. If none, write
`- none open`.

## Due action items

```
*Action items due*
- <owner> - <action> (<due, from evidence>) - <status>
```

List action items from the evidence that are pending or in progress with a near-term due date. If
none, write `- none due`.

## Known Gaps (single section, last)

```
*Known Gaps*
- <each unresolved, conflicting, or unverified item from evidence, one per line, naming the section or milestone and what is missing or unconfirmed. Call out cross-source date conflicts here.>
```

If there are no gaps, write a single line: `- none`. Do not pad or soften this section.
