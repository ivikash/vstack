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
| Story lead | the first paragraph opens with a bold `**Qn YYYY, <Project>:**` lead naming the quarter and the story's project, then runs into prose (lint story-lead, D62). The quarter label is not a date, date-format allows it (D52). The project runs to the first `:**`, so a heading may carry a double-colon identifier or a code span with a colon (`### Dock \`Harbor::Setup\`: Execution`) and the lead names it whole (D80) |
| Shared work | credited by function in the same sentence as the candidate's act, in the task paragraph, never as a subtraction. No printed `Ownership:` sentence (D59, the D21 audit verdicts stay the gate). The subtraction form the lint fails (credit-not-subtraction, D74), as one regex the instance copies into its `draft_contract.must_not_match` twin: `with the \w+ (core\|design\|schema\|component) (from\|by\|authored by) (a\|another\|a second\|the) builder\|under (a\|another\|the) [^.]* design` (case-insensitive) |
| Altitude sentence | the last sentence of the third (action) paragraph, in one of two forms: the counterfactual `A strong <current level> would have ..., not ...` or a factual contrast naming who else was engaged and what the candidate alone did, role words per D41 (D60) |
| Quote | one blockquote line, `> "<verbatim words>", <Name>, <role>` or `> (TO BE COLLECTED: quote from <role>)` |
| Principles line | off by default (`principles.print_line` false, D61). When on, after the quote, `<principles.name> demonstrated: X, Y` (glossary), once per criterion |
| Reason not to promote | `### <plain words>` then five paragraphs with the lead-ins `**Pattern**`, `**Gap**`, `**Also seen by**`, `**Does not block**`, `**Next**`, in that order |
| Markers | `(TO BE COLLECTED)` or `(TO BE COLLECTED: <artifact>)` when the data does not exist yet, `(TO BE CONFIRMED)` at the end of a sentence whose number or source is unconfirmed. The marker is the LAST token of its sentence, and the clause after `TO BE COLLECTED:` names the artifact only (`the adoption metric`), never why it is missing, the impact-data stage document holds the reason (D46, D75). No other form: no square brackets, no `TODO`, no `(unverified)` in this genre |
| Sources line | `Sources used: ... Sources unavailable: ...` as the LAST line of the document, no semicolon, so the house no-semicolons rule holds on every line (D36) |
| Heading words | no heading or reason title contains leverage, play, strategic, proactive, cultivat-, drive alignment, synerg-, holistic or paradigm (lint plain-headings, D40) |
| Review ids | a code review id (`CR-<n>`, `PR #<n>`, a `/pull/<n>` or `/reviews/<n>` link) sits in at most one story's action paragraph. Why now and the Appendix are exempt (lint one-cr-once, D37) |
| Unfetchable links | a link to a document host the writer cannot fetch sits in a sentence ending `(TO BE CONFIRMED)` or carrying `(SUPPORTED)` after the ownership audit verified it (lint marker-direction, D38) |
| Scope of Role | the team and the proposed level only, copied from the scope file's paragraphs for the level pair. Three paragraphs: the team and its scale, what the current level does on this team, what the proposed level does (lint scope-current-level, D68). No candidate name or alias, no hire or join date, no "joined" or "hired", no prior-team sentence (lint scope-no-candidate, D49) |
| Tenure | `Time in Current Level: <N> months`, and every tenure figure in Why now in months. Never days (lint tenure-months, D50) |
| Relative first | a Headline or Why now sentence with a relative figure and the absolute pair writes the relative first and the absolutes in round brackets: `cut failures by 99.7% (from 4,200 a day to 11 a day)` (lint relative-first, D51, house rule quantify-impact) |
| Dates | MM/DD/YYYY in body text, no YYYY-MM-DD outside a URL, a link target or the frontmatter. A quarter label (`Q3 2026`) in a story lead is not a date and passes (lint date-format, D52) |
| Why now markers | none. A figure the evidence does not hold is told in its story with the marker (lint why-now-no-markers, D55). A figure whose impact-data row is marked sits in a story sentence ending on the same marker (lint marker-propagation with `--impact-data`, D72) |
| Why now shape | one prose paragraph: no bullet, no sub-heading, no link, no bracketed criterion after a bold span, no bold span longer than six words. Every bold project name sits in a sentence that carries a number and its baseline (lint why-now-one-paragraph, D56). Sentence one carries the months in level and neither a review count nor a trait word (lint why-now-opener, D57). No sentence over 60 words, and an `On **Project**,` sentence names the candidate (pronoun or first name) within 12 words after the closing bold (lint why-now-sentence-shape, D76). A `N projects`, `N initiatives` or `N stories` count in the closing sentence agrees with the story headings (lint rollup-counts-held warning, checklist row, D77) |
| Trait words | no word from the house `no-superlatives` banlist or trait words and no claim phrase from that line in Why now or a story paragraph. Quote lines, the Feedback section and the D24 altitude form `A strong <level> would have` are exempt (lint no-trait-words, D63, list read from house-rules.md) |
| Ordering words | a story sentence in any of the four paragraphs with first, before, then, after or earlier links two or more artifacts only when their dates (MM/DD/YYYY in the sentence, or the run's `--dates` csv) agree with the words (lint ordering-stamped, D73, widened from the action paragraph to the whole story in D81, checklist ordering-words-stamped for stamps the lint cannot read) |
| Printed dates beside links | the `--dates` csv holds the SHIPPED date of each artifact, and a MM/DD/YYYY printed within 40 characters of a linked artifact equals that artifact's csv date, so the reader never meets a created date beside a review link (lint dates-printed-match-csv, blocker when `--dates` is given, D82) |
| Reasons intro | `## Best reasons not to promote` opens with one paragraph that counts the providers per theme before the first `###` (lint rntp-intro-counts warning, D69) |

Caps, quotes excluded: a story under 500 words (hard failure), Why now under 550 words (hard
failure). Per criterion: at most 2 full stories and at most 600 words together. More is a lint
warning naming the section, its story count and word count, with the instruction to move the
weakest story to one sentence or an appendix. Which story moves is a per-candidate decision kept
in the instance, never in this skill.

Exact strings for an instance's `draft_contract` twins (the table above escapes `|` as `\|`, these
are the regexes as the lint holds them, all case-insensitive):

```
credit-not-subtraction (D74), must_not_match:
with the \w+ (core|design|schema|component) (from|by|authored by) (a|another|a second|the) builder|under (a|another|the) [^.]* design

no-process-leak phrases (D75), must_not_match:
earlier draft|evidence pull|reviewer of the|readiness row|in the order [a-z]+, then|told once below|working copy|author field|acknowledgement names|on record is|as (hers|his|theirs) is|evidence row|stage document

marker end (D75), the form every marker sentence ends on:
\((TO BE CONFIRMED|TO BE COLLECTED(: [^()]+)?)\)\.?$

environment the lint reads: PROMO_LINT_CANDIDATE_PRONOUN, PROMO_LINT_CANDIDATE_ALIAS,
PROMO_LINT_HOUSE_RULES, PROMO_LINT_UNVERIFIED_HOSTS, PROMO_LINT_LINK_EXEMPT
arguments: --impact-data <impact-data.md> (marker-propagation), --dates <url,date csv of SHIPPED dates> (ordering-stamped, dates-printed-match-csv, window 40 characters)
```

## The document

1. **Header block**: `# {NAME} - Promotion Document`, then Employee Name, Manager Name
   ({MANAGER}), Current Title ({CURRENT_TITLE}), Proposed Title ({PROPOSED_TITLE}), Time in
   Current Level ({TIME_IN_LEVEL}, a month count from the `candidate-facts` block, never days).

2. `## Scope of Role`: what the team owns and its scale, then what the CURRENT level does on this
   team, then what the PROPOSED level is expected to be. Three paragraphs, the text the run
   config's `scope_file` holds for the level pair (`target_level`), copied. The gap between the
   second and third paragraph is what the whole document argues (D68). Nothing about the
   candidate: no name, no hire or join date, no prior team (D49). Without the file or the level
   pair the run stops and asks.

3. `## Why now?`: for the VP reader. One paragraph, under 550 words, no bullets, no sub-headings,
   no criterion names, no markers (D55), no links.

   - Sentence one: months in level (D50) and the prior roles in one clause. Not the review
     counts, those belong in the review-process story.
   - Sentence two: how many initiatives, listed with the project name in bold, in the
     `story-ranking` order (D53, ties by `why_now.order`, D4). The writer never picks the order.
   - One sentence per ranked project, three at most, each opening "On **Project**," with the
     candidate's pronoun or name within 12 words of the closing bold, two or three candidate verbs,
     and ending on that story's Headline number with its baseline, relative first (D51). Bold the
     number, not the sentence. No criterion in brackets. No Why now sentence over 60 words (D76).
   - One sentence on operations (incidents root-caused, on-call scopes with a gloss each), one on
     people (who the candidate onboarded or mentored), then one closing sentence that rolls up in
     counts (projects, services, teams, months), not in trait words.
   - Projects with no story are not named here. They go to the Appendix (D14).
   - The candidate is the grammatical subject of every sentence. No internal codename without its
     gloss in the same sentence. No trait adjective or claim phrase from the show-not-tell
     denylist.

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
     `Ownership:` sentence. A panel reads a story, not a form.
   - Paragraph 1, situation: name the obstacle in concrete nouns before the candidate's first
     verb: what did not exist (no API, no document, no owner, no test path), who else owned the
     code, and the criterion's marker (D11). Open the paragraph with a bold lead
     `**Qn YYYY, <Project>:**` so the panel sees the window. End with the first thing the
     candidate did, in an action verb.
   - Paragraph 2, task: what the candidate owned, who handed it over and why it was handed to
     them, stated as a fact of the project. Credit shared work by function in the same sentence as
     the candidate's act, never as a subtraction (house rule credit-inline). No printed
     `Ownership:` sentence (D59): the ownership audit's verdicts (D21) stay the gate, so the task
     paragraph carries only verbs the audit marks SUPPORTED, qualified where it marks PARTIALLY
     SUPPORTED.
   - Paragraph 3, action: candidate-led sentences, the name or pronoun first and a verb second.
     Name the fork: the fast option with its cost, the option taken, and that it finished in the
     window (D32). Name the technique per component instead of an adjective about depth. Every
     artifact linked on its identifier at the exact claim it supports (D13). End with the
     altitude sentence in either form: the D24 counterfactual, or a factual contrast naming who
     else was engaged (role words per D41) and what the candidate alone did (D60).
   - Paragraph 4, result: each figure in the sentence with the verb that produced it, relative
     first (D51), dated. End on the candidate's own held figure or on who uses it now: a named
     team or builder, or the sentence "No reuse by others is on record." (house rule reuse-named).
     Never end on another builder's change, and when the no-reuse sentence closes the story,
     the sentence before it carries a held figure, not a marker (D79).
   - No trait adjective or claim phrase from the denylist anywhere in a story paragraph.
     Adjectives belong to the providers, in quotes.
   - The quote line, verbatim with name and role, or `(TO BE COLLECTED: quote from <role>)`.
   - The `<principles.name> demonstrated: X, Y` line after the last story under a criterion is
     printed only when `principles.print_line` is `true` (glossary, default `false`, D61), and
     never when `principles.cite_per_statement` is `true`.

   A project appears in full once. Every other mention (Why now, another story, the Appendix) is
   one sentence with a cross-reference to the story heading. A criterion holds at most 2 full
   stories. Further projects under it are one sentence each after the second story, with a link to
   their evidence, or an Appendix entry.

5. `## Best reasons not to promote`: genuinely critical, evidence-based, in plain words. One
   intro paragraph before the first reason that names the themes and counts how many providers
   raised each (D69), then one `### <plain words heading>` per reason, five paragraphs each:

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
