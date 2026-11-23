# Template: Promotion Document

Build a story across the whole document. Do not restate a work summary as bullets. Two readers:
the "Why now?" section is for a VP who reads for two minutes, the stories are for a panel that
reads every line.

## Shapes the lint keys on (exact strings)

`scripts/promo-lint.py` and a workflow's `draft_contract` derive their patterns from this block.
Change a string here first, then the lint, never the other way round.

| Element | Exact form |
|---|---|
| Title | `# <Name> - Promotion Document` |
| Sections, in order | `## Scope of Role`, `## Why now?`, `## Evidence`, `## Best reasons not to promote`, `## Feedback Summary`, optional `## Appendix` before Feedback Summary, `## Feedback` last when real feedback exists |
| Story heading | `### <Project>: <Criterion>` (criterion name from the rubric, for example `### Lighthouse Parser: Ambiguity`) |
| Headline | the first line under the story heading, `**Headline** <outcome with at least one number and its baseline or comparator>` |
| STAR parts | paragraphs opening with the verbatim bold lead-ins `**Situation**`, `**Task**`, `**Action**`, `**Result**`, in that order |
| Ownership line | inside **Task**: `Ownership: originated ..., executed ..., operated ...` (what the candidate originated, executed and operated) |
| Altitude sentence | the last sentence of **Action**: `A strong <current level> would have ..., not ...` |
| Quote | one blockquote line, `> "<verbatim words>", <Name>, <role>` or `> (TO BE COLLECTED: quote from <role>)` |
| Principles line | after the quote, `<principles.name> demonstrated: X, Y` (glossary), once per criterion |
| Reason not to promote | `### <plain words>` then five paragraphs with the lead-ins `**Pattern**`, `**Gap**`, `**Also seen by**`, `**Does not block**`, `**Next**`, in that order |
| Markers | `(TO BE COLLECTED)` or `(TO BE COLLECTED: <what>)` when the data does not exist yet, `(TO BE CONFIRMED)` at the end of a sentence whose number or source is unconfirmed. No other form: no square brackets, no `TODO`, no `(unverified)` in this genre |
| Sources line | `Sources: used ...; unavailable ...` as the LAST line of the document (the only line that may hold a semicolon) |

Caps, quotes excluded: a story under 500 words (hard failure), Why now under 550 words (hard
failure). Per criterion: at most 2 full stories and at most 600 words together. More is a lint
warning naming the section, its story count and word count, with the instruction to move the
weakest story to one sentence or an appendix. Which story moves is a per-candidate decision kept
in the instance, never in this skill.

## The document

1. **Header block**: `# {NAME} - Promotion Document`, then Employee Name, Manager Name
   ({MANAGER}), Current Title ({CURRENT_TITLE}), Proposed Title ({PROPOSED_TITLE}), Time in
   Current Level ({TIME_IN_LEVEL}).

2. `## Scope of Role`: what the team owns and its scale, then what the PROPOSED level is expected
   to be on this team. Use the supplied scope evidence.

3. `## Why now?`: for the VP reader. One opening sentence, then three bold wins, then one closing
   paragraph that names every other project in one sentence each.

   - The three wins are the three stories with the highest rank under `why_now.order`, which the
     caller supplies (workflow `config.why_now.order`, default `["impact", "ambiguity", "recency"]`).
     Order the wins by that list, first key first. The writer never picks the order itself, and
     never orders by time unless `recency` is the first key.
   - Each win is one bold sentence carrying the story's Headline number, followed by the
     criterion in round brackets and one plain sentence on the journey. Under 550 words in total.
   - Keep the candidate as the grammatical subject of every sentence. No internal codename
     without its gloss in the same sentence.
   - No colon-plus-parenthetical-list construction for the compressed projects. Full sentences
     with a verb and a landing number.

4. `## Evidence`: one `### <Project>: <Criterion>` story per project, grouped by criterion in the
   rubric's order. The criterion names come from the rubric the caller supplies (for example
   Ambiguity, Problem Complexity, Execution, Impact, Scope and Influence). Each story:

   - `**Headline**`: the outcome, at least one number, and the baseline it beat or a comparator
     (from X to Y, N vs M, ahead of a date). Not the project name, not what the candidate did.
   - `**Situation**`: the customer or stakeholder, what was broken or undefined, why it mattered
     now, and the criterion's marker. Ambiguity: what was undefined and from whose view.
     Problem Complexity: why the cause was not obvious or who else owned the code. Execution,
     Impact, Scope and Influence: the deadline, the number at stake, or the people affected. End
     with the first thing the candidate did to get a foothold, in an action verb.
   - `**Task**`: what the candidate owned and who asked. Close with the `Ownership:` line.
   - `**Action**`: the journey in candidate-led action verbs. What was tried or ruled out and
     why, why no off-the-shelf path worked, who the candidate reached out to or aligned, every
     artifact linked on its identifier at the exact claim it supports. Close with the altitude
     sentence: why a strong engineer one level below could not have done it.
   - `**Result**`: dated, with numbers, adoption, and reuse by others.
   - The quote line, verbatim with name and role, or `(TO BE COLLECTED: quote from <role>)`.
   - After the last story under a criterion, `<principles.name> demonstrated: X, Y` (glossary),
     unless `principles.cite_per_statement` is `true`.

   A project appears in full once. Every other mention (Why now, another story, the Appendix) is
   one sentence with a cross-reference to the story heading. A criterion holds at most 2 full
   stories. Further projects under it are one sentence each after the second story, with a link to
   their evidence, or an Appendix entry.

5. `## Best reasons not to promote`: genuinely critical, evidence-based, in plain words. One
   `### <plain words heading>` per reason, five paragraphs each:

   - `**Pattern**`: the observed strength, with two positive examples by project name.
   - `**Gap**`: "What <name> does not yet do is ...", with one dated example of who pointed it
     out.
   - `**Also seen by**`: a second person who sees the same pattern, and where.
   - `**Does not block**`: "This does not block <proposed level> because ...", with evidence.
   - `**Next**`: "As a <proposed level> I want <name> to ...", then "Plan: ...".

   Every gap a feedback provider states in `## Feedback` is addressed by one reason here. An
   aspiration (what the manager would like the candidate to take on) is not a reason.

6. `## Appendix` (optional): supplementary real evidence that supports a story but does not earn
   its own narrative, extra reviews, secondary examples. The one place bullet lists are fine.
   Never invent an entry.

7. `## Feedback Summary`: a markdown table with columns Provider | Relationship | Support
   Promotion, rows `(TO BE COLLECTED)` until real feedback exists. Follow with one line that
   formal feedback is solicited through the organisation's own process.

8. `## Feedback` (only once the caller supplies real feedback): one subsection per provider, in
   the summary table's order, with their relationship, best reasons to promote, and best reasons
   not to promote, in their own words. Never summarise, soften or merge. Providers change over
   time, so no rule here names a fixed list of people.

9. Last line: `Sources: used ...; unavailable ...`.

Placeholders `{NAME}`, `{MANAGER}`, `{CURRENT_TITLE}`, `{PROPOSED_TITLE}`, `{TIME_IN_LEVEL}` are
filled from the supplied evidence. A worked, fictional example that passes the lint is
`evals/fixtures/promo-doc-good.md`.
