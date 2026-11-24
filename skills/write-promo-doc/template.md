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
| Story body | four prose paragraphs between the Headline and the quote, in STAR order (situation, task, action, result), with NO labels. STAR is the skeleton the writer follows, never words the reader sees (owner decision D28). The lint counts the paragraphs and fails a bold `**Situation**`, `**Task**`, `**Action**` or `**Result**` lead-in, the gate checks the order |
| Ownership line | the last sentence of the second (task) paragraph: `Ownership: originated ..., executed ..., operated ...` (what the candidate originated, executed and operated) |
| Altitude sentence | the last sentence of the third (action) paragraph: `A strong <current level> would have ..., not ...` |
| Quote | one blockquote line, `> "<verbatim words>", <Name>, <role>` or `> (TO BE COLLECTED: quote from <role>)` |
| Principles line | after the quote, `<principles.name> demonstrated: X, Y` (glossary), once per criterion |
| Reason not to promote | `### <plain words>` then five paragraphs with the lead-ins `**Pattern**`, `**Gap**`, `**Also seen by**`, `**Does not block**`, `**Next**`, in that order |
| Markers | `(TO BE COLLECTED)` or `(TO BE COLLECTED: <what>)` when the data does not exist yet, `(TO BE CONFIRMED)` at the end of a sentence whose number or source is unconfirmed. No other form: no square brackets, no `TODO`, no `(unverified)` in this genre |
| Sources line | `Sources used: ... Sources unavailable: ...` as the LAST line of the document, no semicolon, so the house no-semicolons rule holds on every line (D36) |
| Heading words | no heading or reason title contains leverage, play, strategic, proactive, cultivat-, drive alignment, synerg-, holistic or paradigm (lint plain-headings, D40) |
| Review ids | a code review id (`CR-<n>`, `PR #<n>`, a `/pull/<n>` or `/reviews/<n>` link) sits in at most one story's action paragraph. Why now and the Appendix are exempt (lint one-cr-once, D37) |
| Unfetchable links | a link to a document host the writer cannot fetch sits in a sentence ending `(TO BE CONFIRMED)` or carrying `(SUPPORTED)` after the ownership audit verified it (lint marker-direction, D38) |
| Scope of Role | the team and the proposed level only, copied from the scope file's paragraphs for the level pair. No candidate name or alias, no hire or join date, no "joined" or "hired", no prior-team sentence (lint scope-no-candidate, D49) |
| Tenure | `Time in Current Level: <N> months`, and every tenure figure in Why now in months. Never days (lint tenure-months, D50) |
| Relative first | a Headline or Why now sentence with a relative figure and the absolute pair writes the relative first and the absolutes in round brackets: `cut failures by 99.7% (from 4,200 a day to 11 a day)` (lint relative-first, D51, house rule quantify-impact) |
| Dates | MM/DD/YYYY in body text, no YYYY-MM-DD outside a URL, a link target or the frontmatter (lint date-format, D52, house rule date-format) |
| Why now markers | none. A figure the evidence does not hold is told in its story with the marker (lint why-now-no-markers, D55) |

Caps, quotes excluded: a story under 500 words (hard failure), Why now under 550 words (hard
failure). Per criterion: at most 2 full stories and at most 600 words together. More is a lint
warning naming the section, its story count and word count, with the instruction to move the
weakest story to one sentence or an appendix. Which story moves is a per-candidate decision kept
in the instance, never in this skill.

## The document

1. **Header block**: `# {NAME} - Promotion Document`, then Employee Name, Manager Name
   ({MANAGER}), Current Title ({CURRENT_TITLE}), Proposed Title ({PROPOSED_TITLE}), Time in
   Current Level ({TIME_IN_LEVEL}, a month count from the `candidate-facts` block, never days).

2. `## Scope of Role`: what the team owns and its scale, then what the PROPOSED level is expected
   to be on this team. The text is the two paragraphs the run config's `scope_file` holds for the
   level pair (`target_level`), copied. Nothing about the candidate: no name, no hire or join
   date, no prior team (D49). Without the file or the level pair the run stops and asks.

3. `## Why now?`: for the VP reader. One opening sentence, then three bold wins, then one closing
   paragraph that names every other project in one sentence each.

   - The three wins are the three projects ranked highest in the owner's `story-ranking` table
     (per-candidate decisions file: project, rank, one line on why it matters), in that order.
     `why_now.order` (workflow `config.why_now.order`, default `["impact", "ambiguity",
     "recency"]`) breaks ties between equal ranks only (D53). The writer never picks the order
     itself. Without the table the run stops and asks.
   - No `(TO BE CONFIRMED)` and no `(TO BE COLLECTED ...)` in Why now. A figure the evidence does
     not hold stays in its story with the marker (D55). Where a sentence gives a relative figure and
     the absolute pair, the relative comes first and the absolutes follow in round brackets (D51).
     Tenure, when named, is in months (D50).
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
     (from X to Y, N vs M, ahead of a date). Not the project name, not what the candidate did. A
     relative figure comes first, the absolute pair after it in round brackets (D51). Under each
     criterion the first full story is the project the `story-ranking` table ranks highest there
     (D53).
   - Then four prose paragraphs in STAR order. STAR is the skeleton you follow, never words the
     reader sees: no `**Situation**`, `**Task**`, `**Action**` or `**Result**` label, no
     "Ownership:" on a line of its own. A panel reads a story, not a form.
   - Paragraph 1, situation: the customer or stakeholder, what was broken or undefined, why it
     mattered now, and the criterion's marker. Ambiguity: what was undefined and from whose view.
     Problem Complexity: why the cause was not obvious or who else owned the code. Execution,
     Impact, Scope and Influence: the deadline, the number at stake, or the people affected. End
     with the first thing the candidate did to get a foothold, in an action verb.
   - Paragraph 2, task: what the candidate owned and who asked. Its last sentence is the
     `Ownership: originated ..., executed ..., operated ...` sentence.
   - Paragraph 3, action: the journey in candidate-led action verbs. What was tried or ruled out
     and why, why no off-the-shelf path worked, who the candidate reached out to or aligned, every
     artifact linked on its identifier at the exact claim it supports. Its last sentence is the
     altitude sentence: why a strong engineer one level below could not have done it.
   - Paragraph 4, result: dated, with numbers, adoption, and reuse by others.
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

9. Last line: `Sources used: ... Sources unavailable: ...`. No semicolon anywhere in the document.

Placeholders `{NAME}`, `{MANAGER}`, `{CURRENT_TITLE}`, `{PROPOSED_TITLE}`, `{TIME_IN_LEVEL}` are
filled from the supplied evidence. A worked, fictional example that passes the lint is
`evals/fixtures/promo-doc-good.md`.
