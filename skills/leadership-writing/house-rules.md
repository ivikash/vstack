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

## Mechanical rules (a violation is a blocker)

- **no-em-dash**: No em-dash characters (—) anywhere. Use commas, periods, parentheses, or a spaced hyphen " - ".
- **no-semicolons**: No semicolons anywhere. Split the clauses into two sentences, or join them with a comma and a conjunction. When a semicolon separates items in a list, rewrite the list as a bulleted list or shorten the items so commas suffice.
- **correct-grammar**: Fix grammar, spelling, punctuation, subject-verb agreement, verb tense, and article errors. This is mechanical correctness only, and it never changes a fact, number, name, or claim. Write complete sentences with a subject and a verb, keep modifiers next to what they modify, and keep parallel structure across items in a list. When a typo makes a fact ambiguous, keep the passage silent on it or label it "(unverified)" rather than guessing the intended value.
- **define-acronyms**: Expand a non-obvious acronym or codename on first use, only when the expansion is present in or derivable from the input. Do not guess an expansion.

## Voice rules (a violation weakens the writing)

- **active-voice**: Prefer active voice with a clear actor (who did what). Rewrite passive constructions that hide the actor ("it was decided", "was implemented") into an actor-first sentence.
- **zombie-test**: Apply the "zombie trick": if "by zombies" fits after the verb, it is passive. Rewrite with a clear actor ("the feature was delivered" -> "she delivered the feature").
- **show-dont-tell**: Lead with the evidence, not the label. A bare assessment ("strong engineer", "great leader", "on track") must be immediately backed by a concrete example, metric, or artifact that demonstrates it.
- **quantify-impact**: Quantify impact wherever the evidence allows (numbers, deltas, scope, dates). "Improved performance" with an available metric left unused is a violation. A headline number carries the baseline it beat or a comparator (from X to Y, N against M, ahead of a date), because a lone number tells the reader nothing about whether it is good.
- **plain-headings**: Headings and titles are plain words a reader outside the team understands on first read. No stacked abstract nouns ("Cultivating proactive strategic opportunity identification"), no bracketed tags inside the title ("[Ownership]", "[P1]"), no internal codename without its gloss. A heading says what the section is about in the words the reader would use. Denylist for headings and titles, failed by the promo-doc lint: leverage, play, strategic, proactive, cultivat-, drive alignment, synerg-, holistic, paradigm.
- **link-artifacts**: When an artifact has a URL in the evidence (a code review, design doc, ticket, dashboard, or recognition post), hyperlink the reference inline as descriptive markdown link text rather than pasting a bare URL or naming the artifact with no link. Prefer `[the migration design doc](https://...)` over naming it with no link or dumping a raw `https://...` into the prose. Use the artifact's real name or identifier as the link text (never "click here" or "link"). Only link when the URL is present in the evidence, never invent or guess a URL, and do not fabricate a link to make an unlinked reference look sourced.
- **write-for-reader**: Write for the reader, with fluff removed. Cut needless words, weasel words, and long winding sentences. A tight, short sentence carrying a fact beats a padded one.
- **logical-progression**: The narrative builds step by step from a base point, not a scattered pile of claims. Reorder sentences that jump between unconnected points so there is a through-line.
- **no-superlatives**: No boastful adjectives standing in for evidence. Flag every instance and require a fact or number instead. Banlist (not exhaustive): exceptional, outstanding, world-class, best, incredible, seamless, flawless, stellar, phenomenal, superb, top-notch.
- **no-hedging**: Remove words that weaken or dodge a claim, and replace them with a fact or number. Banlist (not exhaustive):
  - Weasel words: should, might, could, often, generally, usually, probably, significant, better, worse, soon, some, most, helped to, was involved in, to some extent, as needed.
  - Vague quantifiers: a number of, various, several, multiple, complex (replace with a count).
  - Boastful filler: comprehensive, extensive, robust, powerful, complete, remarkable (remove these and let the metrics speak).
  - Unnecessary qualifiers: actually, really, basically, very, definitely, somewhat, kind of.

## Structure rules

- **story-not-bullets**: Narrative sections build a story (situation, behavior, impact) in prose, not a bare bullet dump. A permitted exception is a genre element defined as a list or table by its own skill (an artifact link list, a status summary table). Outside those, keep prose.
- **honest-and-data-driven**: Every claim stays backed by a concrete artifact, metric, ticket, review, or document that the input supplied. Never invent metrics, quotes, links, IDs, dates, or feedback.
- **no-assumptions**: If a fact is missing, do not fill the gap with a plausible guess. Validate against the supplied input, and if it is still not there, label it "(unverified)", omit it, or record it under a Known Gaps section. An unverifiable claim is never asserted as fact.
