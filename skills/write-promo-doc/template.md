# Template: Promotion Document

Build a story across the whole document. Do not restate a work summary as bullets.

1. **Header block**: `# {NAME} - Promotion Document`, then Employee Name,
   Manager Name ({MANAGER}), Current Title ({CURRENT_TITLE}),
   Proposed Title ({PROPOSED_TITLE}), Time in Current Level ({TIME_IN_LEVEL}).

2. `## Scope of Role`: what the team owns and its scale, then what the PROPOSED level
   is expected to be on this team. Use the supplied scope evidence.

3. `## Promotion Assessment` with a `**Why now?**` narrative opening paragraph: tell
   the candidate's story and the headline case, grounded in real metrics.

   - Cap this to 2-3 flagship stories told in full (situation, hard part, resolution,
     headline number). Compress every other initiative into a single sentence each;
     don't give every project in scope its own paragraph here, that's what the
     capability sections are for.
   - Keep the candidate as the grammatical subject of every sentence in this section.
     Don't let "the work," "the event," or "the incident" become the subject partway
     through, that hands agency away from the person the document is about.
   - Do not use a colon-plus-parenthetical-list construction to summarize compressed
     initiatives (e.g., "three systems: X (did Y), Z (did W)"). Write them as full
     sentences with a verb and a landing number, the same rhythm as the flagship
     stories, just shorter.

4. `### Evidence`, then **capability sections** mirroring the supplied rubric under it.
   Use the rubric's dimension names as headers (for example
   `#### [Ambiguity / Technical Complexity]`, `#### [Scope and Influence]`,
   `#### [Impact]`, `#### [Execution]`). Under each, tell one or two deep narrative
   project stories: context, challenge, the person's specific actions, measurable
   result, with artifacts inline as links.

   A project story that works well follows this shape: a bolded project header
   (optionally quarter-tagged, e.g. `**Q2 2026 - Project Name**`), then a separate
   paragraph for each beat, situation, then the ambiguity or design decision, then
   execution, then impact, sized to how much that beat actually needs, not compressed
   into one block. Artifact links go inline mid-sentence at the exact claim they
   support rather than collected in a trailing list. If a real quote from a reviewer
   is available for that story, close it with a closing attributed quote before moving
   to the next story. Never fabricate the quote; omit it if none was supplied.

   Close the whole section (after its last story and quote) with one consolidated
   line, `<principles.name> demonstrated: X, Y, Z` (org profile), covering every story in
   that section, not one tag per story, unless `principles.cite_per_statement` is `true`.

   Optional: if the evidence includes real supplementary examples that support the
   section but don't need full narrative treatment (extra CRs, secondary feedback
   responses), don't force them into the narrative or drop them. Hold them for the
   `## Appendix` (see step 6).

5. `## Best reasons not to promote`: GENUINELY CRITICAL and evidence-based. Pull from
   the supplied gaps and verification notes. Be specific (scope overstatement, omitted
   incidents, unverified headline metrics, areas not yet at the target bar). For each
   gap, note the trajectory and how the manager is coaching it. Tag each with the
   single principle it maps to most precisely (for example `[principles.example_2]`), not a
   generic label.

6. `## Appendix` (optional): supplementary real evidence that supports a capability
   section but doesn't earn its own narrative story, extra CRs, secondary review
   examples, additional artifacts. This is the one place bullet lists are fine even
   though the rest of the document is narrative prose (story-not-bullets governs the
   Evidence section, not this one). Group by the capability-dimension header it
   supports. Never invent an appendix entry; only include what the caller supplied.

7. `## Feedback Summary`: a markdown table with columns
   Provider | Relationship | Support Promotion, populated with clearly-marked
   placeholder rows `[TO BE COLLECTED]`. Do NOT invent reviewers or quotes. Follow with
   a one-line note that formal feedback is to be solicited through the org's own process.

8. `## Feedback` (only once the caller supplies real feedback, never before): one
   subsection per provider, in the same order as the summary table, each with their
   relationship to the candidate, their best reasons to promote, and their best
   reasons not to promote, in their own words. Do not summarize, soften, or merge
   feedback across providers, and do not add a provider who isn't in the summary
   table. Leave this section out entirely until real feedback exists; a placeholder
   table in step 7 is not a license to draft placeholder content here.

Placeholders: `{NAME}`, `{MANAGER}`, `{CURRENT_TITLE}`, `{PROPOSED_TITLE}`,
`{TIME_IN_LEVEL}` are filled from the supplied evidence.
