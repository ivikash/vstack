# House Rules

The single source of truth for HOW leadership writing reads in this repo, independent of WHAT
genre it is. Every writing skill (talent card, work summary, promo doc, executive update, and the
rewrite skills) and the validator read this file and apply it. Edit a voice rule HERE, and do not
restate it inside a skill. Genre-specific rules (rating placement, region counts, SBI or STAR structure,
green-by dates) live in the individual skills, not here.

This file is provider-neutral and contains no organization-specific names, tools, or systems. Keep
it that way: it is written for any leadership audience (executives, VPs, directors, managers) at
any company.

The audience is busy and senior. Write for a reader who will spend thirty seconds, not thirty
minutes: lead with the point, back it with a fact, cut everything else.


---

## Principles

The writing principles behind every rule in this file, in the words of the Zen of Python (Tim Peters, PEP 20), each
mapped to the rule or countable check that enforces it. A reader who knows the principle can predict the rule.

| Principle | What it means here | Enforced by |
|---|---|---|
| Explicit is better than implicit | A sentence names its subject. "The Metadata service now drops the file", never "It drops the file" or "The service drops the file" at the head of a sentence outside a list | `explicit_subject` (`implicit-subject`), active-voice, zombie-test |
| Simple is better than complex | One idea per sentence, 30 words or fewer, a link counts as one word | `max_words_per_sentence`, one-idea-per-sentence |
| Flat is better than nested | No clause inside a clause inside brackets. A span in brackets is `(2,083 to 626 µs)`, a link stands alone with nothing appended, a date never trails an identifier link | `bracket_span_format` (`bracket-span-from`, `bracket-span-about`, `bracket-span-no-unit`), `identifier_link_no_date` (`link-then-date`) |
| Sparse is better than dense | A number appears once per section, the multiplier beside the percentage once, no weasel word in place of a figure | numbers-over-adjectives, the countable weasel-word check, the comparative-with-figure check |
| Readability counts | Dates MM/DD/YYYY, no semicolons or em-dashes, every table starts with a `#` column so a reviewer can name a row, a Glossary row carries the acronym beside the term | date-format, no-semicolons, no-em-dash, `table_first_header_hash` (`table-no-hash-column`), the glossary row shape |
| In the face of ambiguity, refuse the temptation to guess | Every claim the evidence does not prove ends with `(TO BE CONFIRMED)` in that exact form, and the sentence before it names what would settle it. A quantity verb names its unit so the reader never guesses less of what | the marker rule (`marker-form`), `quantity_unit` (`quantity-without-unit`) |
| There should be one obvious way to do it | One form per thing: one marker, one date form, one bracket form, one way to write a known term (bare), one Glossary table shape | the Known terms table (`known_terms_source`, the `Write as` column, `bare-term-expanded`), the templates |
| Errors should never pass silently | A rule the model ignored becomes a countable check that fails the gate, never an instruction repeated. Every finding names the text and the fix | `scripts/style-check.py`, the workflow contracts, `RULES.md` |

---

## Mechanical rules (a violation is a blocker)

- **no-em-dash**: No em-dash characters (—) anywhere. Use commas, periods, parentheses, or a spaced hyphen " - ".
- **no-semicolons**: No semicolons anywhere. Split the clauses into two sentences, or join them with a comma and a conjunction. When a semicolon separates items in a list, rewrite the list as a bulleted list or shorten the items so commas suffice.
- **correct-grammar**: Fix grammar, spelling, punctuation, subject-verb agreement, verb tense, and article errors. This is mechanical correctness only, and it never changes a fact, number, name, or claim. Write complete sentences with a subject and a verb, keep modifiers next to what they modify, and keep parallel structure across items in a list. When a typo makes a fact ambiguous, keep the passage silent on it or label it "(unverified)" rather than guessing the intended value.
- **define-acronyms**: Expand a non-obvious acronym or codename on first use, only when the expansion is present in or derivable from the input. Do not guess an expansion.
- **date-format**: Dates in body text are written MM/DD/YYYY. Never YYYY-MM-DD in prose, a table cell or a heading. URLs, link targets and frontmatter keep whatever form the system needs. Month names ("March 2026") and quarters are not dates in this sense and stay as they are.

## Voice rules (a violation weakens the writing)

- **active-voice**: Prefer active voice with a clear actor (who did what). Rewrite passive constructions that hide the actor ("it was decided", "was implemented") into an actor-first sentence.
- **zombie-test**: Apply the "zombie trick": if "by zombies" fits after the verb, it is passive. Rewrite with a clear actor ("the feature was delivered" -> "she delivered the feature").
- **show-dont-tell**: Lead with the evidence, not the label. A bare assessment ("strong engineer", "great leader", "on track") must be immediately backed by a concrete example, metric, or artifact that demonstrates it. Seven techniques carry this in a narrative, each a sentence the reader can check:
  - Name the obstacle in concrete nouns before the actor's first verb: what did not exist (no API, no document, no owner, no test path), who else owned the code. The reader infers depth from the size of the hole.
  - Name the fork with the cost of the easy option: the fast road and why it would come back, the road taken, and that it finished in the window. Judgement is the fork, not the word "judgement".
  - Put each figure in the sentence with the verb that produced it, with its baseline, never on a separate results line.
  - Name the technique per component ("a cached format table for the first, a shared reader for the second") instead of a depth adjective.
  - Show altitude by who else was engaged (how many were on the call, who was senior) and what the actor alone did, rather than a counterfactual claim about what someone at a lower level could not have done.
  - End a result on who uses it now: a named team or person, or a plain statement that no reuse is on record.
  - Open sentences on the actor plus a verb. Where a sentence opens on something else, it is the obstacle, and the actor's verb arrives in the next clause.
- **credit-inline**: Shared work is credited by function in the same sentence as the actor's act ("settled the model with the security reviewers and the auth principals", "drove it across three teams: one for the review, one for the model, one for the action design"), never as a subtraction ("under X's design, with the core authored by Y"). The credit widens the actor's reach rather than shrinking the claim. The subtraction belongs only in a reasons-not-to-promote or gaps section. The subtraction form is countable and the promo-doc lint fails it (credit-not-subtraction): "with the <noun> (core, design, schema, component) from, by or authored by a, another, a second or the builder", "under a, another or the ... design", or "onto, into or on top of a ... core, design or schema (that) a teammate, builder or the team wrote". The paraphrase family reads the same way and the gate fails it: "onto a cache core a teammate wrote", "to a design the team had settled", "the schema was another builder's". Credit by function in the same clause as the candidate's own piece, with the function named before her piece or beside it, never as the boundary after it: "with the cache author she shipped the security path", not "she shipped the security path onto a cache core a teammate wrote". Write the same fact as a widening: "shipped the security path and the rollout alongside the cache author and the design owner". Each credit clause carries its own verb ("the key store came from her", "the cache author built the core"), a piece with a name hung off its end ("the key store and the role on its path from her") is a list, not a credit (D89).
- **quantify-impact**: Quantify impact wherever the evidence allows (numbers, deltas, scope, dates). "Improved performance" with an available metric left unused is a violation. A headline number carries the baseline it beat or a comparator (from X to Y, N against M, ahead of a date), because a lone number tells the reader nothing about whether it is good. Where a sentence gives both a relative figure (a percentage, an x-factor, "N times") and the absolute numbers, the relative comes first and the absolutes follow in round brackets: "cut failures by 85% (2,000 to 300 a second)", never the absolutes first with the percentage trailing.
- **plain-headings**: Headings and titles are plain words a reader outside the team understands on first read. No stacked abstract nouns ("Cultivating proactive strategic opportunity identification"), no bracketed tags inside the title ("[Ownership]", "[P1]"), no internal codename without its gloss. A heading says what the section is about in the words the reader would use. Denylist for headings and titles, failed by the promo-doc lint: leverage, play, strategic, proactive, cultivat-, drive alignment, synerg-, holistic, paradigm.
- **link-artifacts**: When an artifact has a URL in the evidence (a code review, design doc, ticket, dashboard, or recognition post), hyperlink the reference inline as descriptive markdown link text rather than pasting a bare URL or naming the artifact with no link. Prefer `[the migration design doc](https://...)` over naming it with no link or dumping a raw `https://...` into the prose. Use the artifact's real name or identifier as the link text (never "click here" or "link"). Only link when the URL is present in the evidence, never invent or guess a URL, and do not fabricate a link to make an unlinked reference look sourced.
- **write-for-reader**: Write for the reader, with fluff removed. Cut needless words, weasel words, and long winding sentences. A tight, short sentence carrying a fact beats a padded one.
- **logical-progression**: The narrative builds step by step from a base point, not a scattered pile of claims. Reorder sentences that jump between unconnected points so there is a through-line.
- **no-superlatives**: No boastful adjectives standing in for evidence. Flag every instance and require a fact or number instead. Banlist (not exhaustive): exceptional, outstanding, world-class, best, incredible, seamless, seamlessly, flawless, stellar, phenomenal, superb, top-notch. Trait words (depth and character adjectives that tell what the sentence should show): deep, deeply, thorough, thoroughly, rigorous, robust, strong, strongly, consistent, consistently, unusually, impressive, reliable, rapidly, instrumental, genuine. Claim phrases: "demonstrates", "demonstrated" or "demonstrating" followed by a trait or principle noun ("demonstrated that the cache held" is a fact and passes), "ability to", "well beyond", "beyond what is expected", "was responsible for", "owned quality". Quotes attributed to a named provider are exempt. The promo-doc lint `no-trait-words` reads the banlist, the trait words and the quoted claim phrases from this line, so an edit here changes the lint and nothing holds a second copy.
- **no-hedging**: Remove words that weaken or dodge a claim, and replace them with a fact or number. Banlist (not exhaustive):
  - Weasel words: should, might, could, often, generally, usually, probably, significant, better, worse, soon, some, most, helped to, was involved in, to some extent, as needed.
  - Vague quantifiers: a number of, various, several, multiple, complex (replace with a count).
  - Boastful filler: comprehensive, extensive, robust, powerful, complete, remarkable (remove these and let the metrics speak).
  - Unnecessary qualifiers: actually, really, basically, very, definitely, somewhat, kind of.

## Structure rules

- **story-not-bullets**: Narrative sections build a story (situation, behavior, impact) in prose, not a bare bullet dump. A permitted exception is a genre element defined as a list or table by its own skill (an artifact link list, a status summary table). Outside those, keep prose.
- **honest-and-data-driven**: Every claim stays backed by a concrete artifact, metric, ticket, review, or document that the input supplied. Never invent metrics, quotes, links, IDs, dates, or feedback.
- **no-assumptions**: If a fact is missing, do not fill the gap with a plausible guess. Validate against the supplied input, and if it is still not there, label it "(unverified)", omit it, or record it under a Known Gaps section. An unverifiable claim is never asserted as fact.
- **reuse-named**: A result paragraph ends on a named user of the artifact (a team or a person who now runs it, extends it or plans from it) or states plainly that no reuse is on record. "Stakeholders", "the business" and "customers" with no name are not a user. Adoption stands in for quality, which is never asserted.
