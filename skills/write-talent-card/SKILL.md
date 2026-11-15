---
name: write-talent-card
description: Write a talent-review card for a team member from supplied evidence and the performance rating, filling the two narrative sections (Rating Rationale / Key Talking Points and Key Deliverables & Achievements) of a standard per-person review doc. Use when a manager wants a per-person calibration card that matches the house format. Does NOT fetch data; the caller provides the evidence and the rating.
disable-model-invocation: false
---

# Write Talent Card

Read [leadership-writing/house-rules.md](../leadership-writing/house-rules.md) and
[leadership-writing/rationalizations.md](../leadership-writing/rationalizations.md) first and apply every rule in them.

You turn supplied evidence about a team member into the two narrative sections of a
talent-review card a manager uses in calibration. The card follows a fixed house
format: a numbered doc whose Background (with the Rating and Rating History tables),
Code Contributions, and Appendix sections are supplied by the caller, and whose
**Rating Rationale / Key Talking Points** (section 2) and **Key Deliverables & Achievements**
(section 3) you write.

You do **not** fetch data and you do **not** decide the rating. The caller provides the
evidence, the person's level, and the rating (which is displayed in the Background
table). If evidence is missing, mark the section preliminary rather than inventing it.

## Output discipline (read first)

- Return ONLY the finished card content. No preamble, no "Here is", no "Now I'll apply
  the fixes", no notes about your process. Scan your output and delete any sentence that
  talks about writing the card rather than being the card.
- Produce the numbered sections in order. If the caller supplies the existing doc, keep
  sections 1, 4, and 5 verbatim and fill in 2 and 3. If the caller asks for only sections
  2 and 3, return just those two.

## Writing rules (MUST follow, scan output before returning)

Read [leadership-writing/house-rules.md](../leadership-writing/house-rules.md) and apply EVERY rule in it:
no-em-dash, no-semicolons, correct-grammar, define-acronyms, active-voice, zombie-test, show-dont-tell,
quantify-impact, write-for-reader, logical-progression, no-superlatives, no-hedging (with its
banlist), story-not-bullets, honest-and-data-driven, and no-assumptions. That file is the single
source of truth for the voice; this skill applies it, it does not restate it. Scan the output for
em-dashes and hedging words before returning.

Organisation-specific words (what principles are called, rating labels, level names) come from
[leadership-writing/org-profile.md](../leadership-writing/org-profile.md). Read it, or the caller's override, before writing.

The rules below are talent-card-specific and are NOT covered by house-rules; follow them too:

- THE RATING IS SHOWN, in the Background table (section 1), exactly as supplied. Do
  not invent or change rating numbers. Section 2 argues the case behind the rating in
  the language of the organisation's principles (`principles.name` in the org profile);
  it does not need to restate the rating letters. Do NOT recite the `rating.history_label`
  table in section 2 prose ("held `rating.top` in 2022 Q3 and 2023 Q1 ..."). That table is
  section 1's job; repeating it reads as padding.
  Section 2 argues what the person DID, not what their past ratings were.
- BE BALANCED. Section 2 always ends with genuine Growth Areas, not only strengths.
- A claimed strength or growth area needs at least 2 distinct examples to read as a
  pattern; with only one, call it "emerging" rather than overstating it. Attribute honestly:
  distinguish what the person led from what they contributed to, and keep example structure
  situation-behavior-impact (SBI) so each claim shows the person's own action and its result.
- ONE DELIVERABLE, ONE ROLE. Use a given deliverable once: either as an owned sub-scope
  strength OR as the growth lever, never both. State shared/co-owned attribution the first
  time you cite it (the strength paragraph); do NOT re-use that same deliverable in Growth
  Areas to argue the person lacks ownership. A card that calls a project "owned end to end"
  in paragraph 1 and "credited to others" in paragraph 3 contradicts itself and fails
  calibration. Growth Areas must rest on a DIFFERENT deliverable or an unclaimed gap.
- MISSING METRIC MARKER. When impact is not in the evidence, write
  `[TO CAPTURE: <specific metric> - not in current evidence]`, not bare "NA". This is a
  pre-panel punch-list item, distinct from house-rules `(unverified)` which marks a
  doubtful claim.
- TONE CALIBRATED BY RATING (internal signal): the rating sets how strong the
  language is, not the content. A top rating earns confident, differentiated,
  metric-backed language; a middle rating reads balanced, specific, and honest about
  gaps; a low rating leads with what the person does well then is direct and concrete
  about gaps. Do not write glowing prose for a middle rating (it reads as biased and
  erodes calibration credibility), and do not soften a low rating into vague positivity.
  If the person is ineligible for a rating this cycle, say so and render no performance
  judgement. Stay within the no-superlatives rule at every level.

## Section formats (the part that matters most)

Follow [template.md](template.md) exactly. The two sections you write have DIFFERENT
shapes, and getting the shape right is as important as the content:

- **Section 2, Rating Rationale / Key Talking Points = PROSE, EXACTLY FOUR paragraphs,
  in this fixed order** (no orienting preamble sentence, no fifth paragraph):
  1. **Major delivery** - the flagship delivery work this cycle (role, scope, realized
     impact), anchored to one principle from the org profile in bold.
  2. **Operational excellence contribution** - OE/COE, on-call, alarms, deprecations,
     tooling/automation, reliability/security hardening, quantified where possible,
     anchored to one principle from the org profile in bold.
  3. **Growth Areas** - the paragraph begins with `**Growth Areas:**`; honest, concrete,
     principle-anchored, grounded in the work. Name each gap with ONE concrete example, not an
     exhaustive audit. This is a manager's calibration note, not a code review: do not
     itemize every open CR, missing approval, or TODO ("open with zero approvals, disables
     X behind a TODO" belongs in a review comment). State the pattern, then move on.
  4. **Manager Support** - the paragraph begins with `**Manager Support:**`; first person
     ("I will support him/her by ..."), concrete actions for next cycle.
  Paragraphs 1 and 2 lead with the principle, then give concrete evidence, scope, and measurable
  result with specifics woven inline. Do NOT bullet this section.

- **Section 3, Key Deliverables & Achievements = BULLETED, grouped by theme.**
  Order: optional `### Shoutouts`, optional `### Feedback Providers`, then `### Key
  Deliverables`.
  - `### Shoutouts` holds ONLY corroborated recognition: each bullet has a date, the
    author, and a link. Recognition you cannot corroborate does NOT go here and is NEVER
    asserted as fact.
  - `### Feedback Providers` lists named providers for calibration: each is a person, their
    relationship to the work, and `[TO BE COLLECTED: feedback text]`. This is where
    uncorroborated recognition and expected reviewers go, honestly marked.
  - `### Key Deliverables` uses bold theme-group headers and terse bullets: deliverable
    name, role (Owner / Lead / Contributor), date or quarter, quantifiable impact, and
    artifact / code-review / ticket links. Do NOT write this section as prose.

## Built-in validation loop (always, before returning)

A draft never leaves this skill unchecked. After the first full draft:

1. Read [validate-writing/SKILL.md](../validate-writing/SKILL.md) and
   [validate-writing/checklist.md](../validate-writing/checklist.md) and apply them to your own
   draft in **gate** mode, using the doc type `talent-card`.
2. Apply every quoted fix. Re-run the gate. Repeat until a pass reports zero blockers and zero
   majors, with a minimum of two passes and a maximum of five.
3. If blockers remain after the fifth pass, keep the draft and append a closing `**Known Gaps**`
   note listing each unresolved failure verbatim. Never hide an unresolved blocker and never
   resolve one by inventing a fact.
4. Return only the final draft (plus the Known Gaps note when required): no pass counts, no
   validation report, no process sentences. A caller that wants the report runs
   `/validate-writing` in evaluate mode separately.

The default output is markdown. If the caller asks for a specific chat format (for
example `*bold*` and bullets rather than `#` headings), follow that instruction.

Return only the finished card.

## Red flags (this genre)

Stop and re-read the rule when you see yourself producing any of these, on top of the shared list:

- a rating letter or word in section 2 prose
- a growth area with no example of the behaviour behind it
- a principle cited that is not in the org profile list
