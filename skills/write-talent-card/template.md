# Template: Talent Card

This card fills a pre-existing per-person talent-review doc that already contains a
numbered skeleton. You write only the two narrative sections; the rest of the
skeleton (Background, rating tables, Code Contributions, Appendix) is supplied by the
caller and left intact. Do NOT invent or restate the Background / rating tables; if the
caller gives you the existing doc, keep its sections 1, 4, and 5 verbatim and fill in
sections 2 and 3.

The document title follows `levels.title_format` from the glossary (default `{LEVEL} - {NAME}`,
for example `Senior Engineer - Jane Doe`).

Section order (numbered headings, matching the house format):

## 1. Background
Supplied by the caller: profile/handle, months in role/level, job history, the Rating
table, and the Rating History table. Keep verbatim if present; never fabricate rating
numbers. The rating is shown here, in the table, exactly as the caller supplied it.

## 2. Rating Rationale / Key Talking Points
**Prose. EXACTLY FOUR paragraphs, in this fixed order.** No more, no fewer. Do not add
an orienting preamble sentence before paragraph 1, and do not add a fifth paragraph.
Each of the first two paragraphs is anchored to demonstrated principles from the glossary
(`principles.name`, for example **`principles.example_1`**, **`principles.example_2`**) in
bold; lead with the principle, then the concrete evidence: what the person did, the scope
(teams, services, regions), and the measurable result, with specifics (dates, counts,
adoption numbers) woven inline rather than bulleted.

1. **Major delivery.** The person's most significant delivery work this cycle: the
   flagship project(s), their role (led vs contributed), scope, and measurable/realized
   impact. Principle-anchored.
2. **Operational excellence contribution.** Their operational-excellence work: OE/COE
   items, on-call, alarms, deprecations, tooling/automation, reliability and security
   hardening, with quantified impact where the evidence allows. Principle-anchored.
3. **Growth Areas.** Begin the paragraph with `**Growth Areas:**`. Honest, concrete,
   principle-anchored growth areas grounded in the actual work. Do not soften a candid growth
   area into vague praise.
4. **Manager Support.** A one-paragraph manager support plan; begin with
   `**Manager Support:**` and write it in the first person ("I will support him/her by
   ...") with concrete actions for the next cycle.

The rating itself lives in the Background table (section 1); section 2 argues the case
behind it in the language of the organisation's principles. If the person is ineligible for a rating this cycle (for
example, tenure), say so in paragraph 1 and note that no performance judgement is being
made and why (the four-paragraph structure still holds).

## 3. Key Deliverables & Achievements
**Bulleted, grouped by theme** (NOT prose). Mirror the sample house style:

- Optional `### Shoutouts` subsection first: each shoutout as a bullet with the date,
  who recognized whom, and a link.
- Then `### Key Deliverables` with **bold theme group headers** (for example
  **Platform / Infrastructure**, **New Product Area**, **Operational Excellence**,
  **Testing & Quality**, **Code Reviews**, **Mentorship**). Under each, terse bullets:
  deliverable name, role (Owner / Lead / Contributor), date or quarter, the quantifiable
  impact, and artifact / code-review / ticket links. Keep each bullet to a line or two.

## 4. Code Contributions
Supplied by the caller (code activity + code-review stat links). Keep verbatim.

## 5. Appendix
Supplied by the caller (promotion status, pending actions). Keep verbatim.

Placeholders: `{NAME}` person name, `{HANDLE}` username/handle, `{LEVEL}` their level.

If the supplied evidence is sparse, mark sections 2 and 3 clearly as preliminary
rather than inventing content.
