#!/usr/bin/env python3
"""Deterministic lint for a promotion document written by skills/write-promo-doc.

Standard library only. One line per failure, `<rule> <section>: <quoted text or count>`,
exit 1 when anything fails, exit 0 on a clean document. Length failures print first, the
longest offender at the top, because that is the mark reviewers leave most. Warnings
(`warning <rule> ...`) are reported and never change the exit code.

Every regex below is derived from the exact strings pinned in
skills/write-promo-doc/template.md (the "Shapes the lint keys on" block). Change the template
first, then this file, never the other way round.

    # <Name> - Promotion Document
    ## Scope of Role
    ## Why now?                             under 550 words, one paragraph, months first
    ## Evidence
    ### <Project>: <Criterion>              one story, criterion from the rubric
    **Headline** <outcome, number, baseline>   bold lead-in, first line under the H3
    **Qn YYYY, <Project>:** <situation>     the first paragraph opens with the quarter lead (D62)
    <four prose paragraphs>                 situation, task, action, result in that order, no labels
                                            (D28: STAR is the writer's skeleton, never words the
                                            reader sees). No Ownership sentence (D59)
    > "...", <Name>, <role>                 one blockquote line, or
    > (TO BE COLLECTED: quote from <role>)   or the square form `> [TO BE COLLECTED: quote from <role>]`
    ## Best reasons not to promote
    ### <plain words>
    **Pattern** ... **Gap** ... **Also seen by** ... **Does not block** ... **Next** ...
    ## Feedback Summary
    Sources used: ... Sources unavailable: ...      last line of the document, no semicolon

Skips: `no-semicolons` and `no-em-dash` do not fire under `## Feedback`, whose provider text is
verbatim by rule (finding R2). `bare-identifier` and `no-process-leak` skip a leading YAML
frontmatter block between two `---` lines (finding R3), and `no-process-leak` skips the Sources
line. Every other rule still reads those lines.

Round 3b rules (the review's "What the gate missed" list, decisions D31 to D40):
    no-process-leak     a body sentence that talks about the writing, not the candidate
    journey-countable   an action paragraph with no journey verb and no other person named
    rntp-contradiction  a reason states as fact what a story marks (TO BE CONFIRMED/COLLECTED),
                        approximation by project name plus an initiative phrase
    one-cr-once         one code review id in at most one story's action paragraph
    marker-direction    an unfetchable document link sits in a (TO BE CONFIRMED) sentence, and a
                        (TO BE CONFIRMED) with no artifact in its sentence is a warning
    plain-headings      a heading with a word from the jargon denylist
Round 3 close rule (D41):
    role-words-held     warning: a story paragraph gives another person a role (senior builder, product
                        manager, principal engineer, bar raiser) and carries no link and no marker, so
                        nothing in the paragraph holds the role. A warning, because a link elsewhere in the
                        story may hold it, the checklist rule of the same name decides
Round 4 rules (the owner's reading of the first end-to-end document, decisions D49 to D55):
    scope-no-candidate  `## Scope of Role` is about the team and the proposed level. It fails on the
                        candidate's name (from the title and the Employee Name line) or alias (env var
                        PROMO_LINT_CANDIDATE_ALIAS), on joined, hired, a hire or start date, and on a
                        prior-team sentence
    tenure-months       tenure is printed in months, never days: the `Time in Current Level` header
                        line and any Why now sentence that gives a day count against a level or role
    relative-first      a Headline or Why now sentence that carries both a relative figure (percent,
                        x-factor, N times, N-fold) and the absolute pair (from X to Y, X to Y) puts the
                        relative first and the absolutes after it in round brackets
    date-format         body dates are MM/DD/YYYY, any YYYY-MM-DD outside a URL, a link target or the
                        frontmatter fails
    why-now-no-markers  Why now carries neither (TO BE COLLECTED ...) nor (TO BE CONFIRMED), a figure
                        the evidence does not hold is told in its story with the marker
Round 4 shape rules (the owner's example document, decisions D56 to D70):
    why-now-one-paragraph  Why now is one prose paragraph: no bullet, no sub-heading, no link, no
                        bracketed criterion after a bold span, no bold span over six words (a bold
                        sentence is a list the VP skims), and every bold project name sits in a
                        sentence that carries a number and its baseline. Replaces why-now-wins
    why-now-opener      the first Why now sentence carries a month count, and neither a review count
                        nor a trait word
    story-lead          a story's first paragraph opens with a bold `**Qn YYYY, <Project>:**` lead
                        naming the story's own project. The quarter label is not a date, date-format
                        allows it (D52)
    no-trait-words      no word from the house no-superlatives banlist or trait words and no claim
                        phrase from that line in Why now or a story paragraph. The list is read from
                        skills/leadership-writing/house-rules.md at run time (PROMO_LINT_HOUSE_RULES
                        overrides the path), nothing here holds a copy. Quote lines, the Feedback
                        section and the D24 altitude form `A strong <level> would have` are exempt
    scope-current-level `## Scope of Role` has three paragraphs, the middle one names the current
                        title and the last the proposed title (header lines)
    markers-consistent  skips the `## Feedback` section, whose providers tag principles in square
                        brackets in verbatim text (D70)
    warnings: candidate-subject-share (share of action-paragraph sentences opening on the
                        candidate's first name or pronoun plus a verb under CANDIDATE_SUBJECT_SHARE,
                        the pronoun from PROMO_LINT_CANDIDATE_PRONOUN or the commonest of she, he,
                        they in the stories), obstacle-first (situation paragraph has no absence
                        construction before the candidate's first sentence), figure-has-verb (a result
                        sentence with a number and no verb), reuse-named (the result paragraph's last
                        sentence names no user and is not the no-reuse sentence), rntp-intro-counts
                        (no intro paragraph counting providers before the first reason)
Retired this round: why-now-wins (D56) and ownership-line (D59, the printed sentence was a label
the reader sees, the ownership audit verdicts stay the gate).
Round 4c rules (the first end-to-end review's "What the gate cannot see yet", D72 to D80):
    marker-propagation  reads `--impact-data <path>` (the instance passes promo/<alias>/impact-data.md):
                        a figure in a Why now or story sentence that matches a table row whose LAST
                        cell carries (TO BE CONFIRMED) or (TO BE COLLECTED sits in a sentence ending
                        on the same marker. Without the argument one line says the rule is skipped
    ordering-stamped    an action sentence with first, before, then, after or earlier that links two
                        or more artifacts whose dates run against the words (MM/DD/YYYY in the
                        sentence, or `--dates <csv>` of url,date) fails. One linked artifact next to
                        an unlinked artifact noun or a date: warning. Checklist ordering-words-stamped
                        stays the blocker for stamps the lint cannot read
    credit-not-subtraction  a story sentence matching SUBTRACTION_CREDIT (the house rule credit-inline's
                        forbidden form, the regex is published in template.md for the contract twin)
    no-process-leak     phrase list extended: author field, acknowledgement names, on record is, as
                        hers/his/theirs is, evidence row, stage document
    markers-consistent  form half: a (TO BE COLLECTED ...) marker is the last token of its sentence and
                        the clause after the colon names an artifact, never an explanation (D46)
    why-now-sentence-shape  no Why now sentence over 60 words, and an `On **Project**,` sentence names
                        the candidate (PROMO_LINT_CANDIDATE_PRONOUN or first name) within 12 words
    rollup-counts-held  warning: a `N projects|initiatives|stories` count in the closing Why now
                        sentence disagrees with the story headings. The checklist row reads the
                        impact-data rows for the other counts
    story-lead          widened: the project group runs to the first `:**`, so a `::` identifier or a
                        code span with a colon in the heading is not cut at its first colon
    sentences()         a closing `)` ends a sentence too, so `x. (TO BE CONFIRMED) Next ...` splits
Round 4e rules (the round 4b review's section H, decisions D81 to D85):
    ordering-stamped    reads every paragraph between the Headline and the quote (situation, task,
                        action, result), not only the action paragraph, same severities (D81)
    dates-printed-match-csv  with `--dates`: a MM/DD/YYYY date printed within 40 characters of a
                        linked artifact equals that artifact's csv date (the shipped date), else it
                        fails naming both. The nearest link owns the date. Without the argument the
                        rule is skipped (D82)
    credit-not-subtraction  SUBTRACTION_CREDIT gains the paraphrase form `onto|into|on top of a ...
                        core|design|schema (that|which) a|another|the teammate|builder|team` (D83)
    why-now-sentence-shape  floor, warning: a Why now sentence under 10 words whose only figures are
                        cross-references (`<figure> above|below|earlier`) or that has none (D85)
Round 4 close-out rules (the round 4c review's section H, decisions D86 to D88):
    dates-csv-coverage  warning, with `--dates`: a MM/DD/YYYY printed within 40 characters of a
                        linked artifact that has no csv row prints `add a row for <url> or move the
                        date`. The nearest link owns the date, so a neighbouring link's date does not
                        fire on a link with no row (D86)
    headline-no-identifier  warning: a code review, ticket or MCM identifier (or a link to one) in a
                        story Headline, `move the identifier to the action paragraph and keep the
                        date`. The owner decides per draft (D87)
    reuse-named         silent when the result paragraph's last sentence carries a HELD impact-data
                        figure (needs `--impact-data`): a figure of an unmarked row, or a figure of a
                        marked row that the marker's sentence does not name. The checklist vp-read
                        note (D79) decides the ending of a top-ranked story (D67 amended, D88)
Hosts the writer cannot fetch are `UNVERIFIED_HOSTS` plus the comma-separated env var
PROMO_LINT_UNVERIFIED_HOSTS. Links the caller has verified by hand are exempt through the env var
PROMO_LINT_LINK_EXEMPT (comma-separated URL substrings) or an adjacent `(SUPPORTED)` tag. The
instance workflow sets both for `vstack check-run`, so no internal host name lives in this file.

Fallback (finding R1): a draft without `## Evidence` is still measured per story. The lint finds
the shallowest heading level whose titles are bracketed (`#### [<Criterion>]`), treats each such
heading as a criterion section, and splits its body at whole-line bold titles. It prints
`shape: fallback` as its first line, then the same per-story rules over those blocks. The bold
title takes the Headline slot, so `headline-first` names it. A document in the template shape
never enters the fallback, so its output is unchanged.

The readiness table (owner decision D25) is a stage document beside the draft, `<stem>.readiness.md`
for a fixture or `gap-analysis.md` in a run directory, ending `Readiness: Ready | Ready with gaps |
Not ready`. A missing table or a `Not ready` verdict fails `readiness-first`, unless the document
declares the readiness mode `draft_with_readiness` itself: a line opening `**Not ready for
submission**` in the body (the owner asked for a draft over a Not ready verdict). Then a Not ready
verdict passes with a warning, the document must also carry a `## Readiness` section, and a banner
over a Ready verdict fails (`readiness-banner`): banner and verdict always agree.

Only countable rules live here. Judgement rules (wrong criterion, STAR order of the four
paragraphs, journey, altitude, ownership verdict, contradiction, provider gaps, jargon) are in
skills/validate-writing/checklist.md section H with their quoted-failure forms.
"""
import re
import sys

CAP_STORY = 500          # failure: one story, quote excluded
CAP_SECTION = 600        # warning: all stories under one criterion together (owner ruling 2026-11-23)
MAX_STORIES = 2          # warning: full stories under one criterion, the rest are one sentence each
CAP_WHY_NOW = 550        # failure
FULL_TELLING = 80        # one-story-once: a project told in more than 80 words under a heading is a full telling

REQUIRED = [
    (r"^# .+ - Promotion Document\s*$", "# <Name> - Promotion Document"),
    (r"^## Scope of Role\s*$", "## Scope of Role"),
    (r"^## Why now\?\s*$", "## Why now?"),
    (r"^## Evidence\s*$", "## Evidence"),
    (r"^## Best reasons not to promote\s*$", "## Best reasons not to promote"),
    (r"^## Feedback Summary\s*$", "## Feedback Summary"),
]
STORY_PARAGRAPHS = 4     # situation, task, action, result, unlabelled (D28)
RNTP = ["Pattern", "Gap", "Also seen by", "Does not block", "Next"]

HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
LEADIN = re.compile(r"^\*\*([A-Za-z ]+)\*\*")
BOLD = re.compile(r"\*\*([^*]+)\*\*")
LINK = re.compile(r"\[[^\]]+\]\([^)]+\)")
BARE_URL = re.compile(r"(?<!\()https?://\S+")
BARE_ID = re.compile(r"(?<!\[)\b(CR|review|ticket|doc)[- ]?\d{2,}\b", re.I)
QUOTE_LINE = re.compile(r'^> (".+", [A-Z][^,]+, [^,]+|\(TO BE COLLECTED: quote from [^()]+\)|\[TO BE COLLECTED: quote from [^\[\]()]+\])\s*$')
DATE = re.compile(r"\b(\d{1,2}/\d{1,2}(/\d{2,4})?|\d{4}-\d{2}-\d{2}|(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}|Q[1-4] ?\d{2,4})\b")
WORD = re.compile(r"[A-Za-z0-9][A-Za-z0-9'./%:-]*")
COMPARATOR = re.compile(r"\b(from \S+( \S+){0,3} to \S+|\d[\d,.]*( [a-z/]+){0,3} to \d|down from|up from|vs\.?|versus|against|ahead of|early|earlier|instead of|fewer|more than|less than|before|cut from|to 0)\b", re.I)

# round 4 (D49 to D55)
TITLE = re.compile(r"^# (.+?) - Promotion Document\s*$")
EMPLOYEE_LINE = re.compile(r"^-?\s*Employee Name:\s*(.+?)\s*$")
TENURE_LINE = re.compile(r"^-?\s*Time in Current Level:\s*(.+?)\s*$")
HISTORY_WORD = re.compile(r"\b(joined|hired|hire date|start date|started on|onboarded|was promoted|promoted to)\b", re.I)
PRIOR_TEAM = re.compile(r"\b(prior|previous|former|earlier|last) (team|role|org|group)\b|\bfrom the [A-Z][\w-]*( [A-Z][\w-]*)* team\b|\bcame from\b|\bmoved (over )?from\b|\btransferred (from|in)\b|\bbefore (joining|moving|coming)\b|\bhad been an?\b", re.I)
DAYS = re.compile(r"\b\d[\d,]* days\b", re.I)
TENURE_CONTEXT = re.compile(r"\b(level|role|tenure|in the job|since (joining|hire|starting))\b", re.I)
TITLE_CONTEXT = re.compile(r"\bas an? [A-Z][A-Za-z]*")      # "as an Engineer II", case matters: "as a result" is not a title
RELATIVE = re.compile(r"(?<![.\w])\d[\d.,]*\s?(%|percent|x\b|times\b|-fold\b)|\b\d[\d.,]*\s?(percentage points?)\b", re.I)   # `CR.8X`, a product name, is not a multiplier
ABSOLUTE_PAIR = re.compile(r"\b\d[\d,.]*( [a-zA-Z/]+){0,3} to \d[\d,.]*\b")
ISO_DATE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")

MARKER_COLLECTED = re.compile(r"\(TO BE COLLECTED(: [^()]+)?\)")
# the square quote-line form an instance may require instead of the round one (a provider quote that does not exist yet,
# on its own `> ` line): accepted beside the round form, never inside prose
MARKER_COLLECTED_QUOTE = re.compile(r"\[TO BE COLLECTED: quote from [^\[\]()]+\]")
MARKER_CONFIRMED = re.compile(r"\(TO BE CONFIRMED\)")
MARKER_ANY = re.compile(r"(?i)[\[(]?\s*(to be collected|to be confirmed|tbd|tbc|todo|unverified|to capture)\b[^)\]\n]*[\])]?")

# round 3b (D31 to D40)
SOURCES_LINE = re.compile(r"^Sources( used)?:", re.I)
PROCESS_LEAK = re.compile(r"earlier draft|evidence pull|reviewer of the|readiness row|in the order [a-z]+, then|told once below|working copy|author field|acknowledgement names|on record is|as (hers|his|theirs) is|evidence row|stage document", re.I)
JOURNEY_VERB = re.compile(r"ruled out|instead of|rather than|tried|rejected|aligned|asked|brought .* to|\(TO BE COLLECTED: what (she|he|they) tried", re.I)
JOURNEY_NOUN = re.compile(r"\b(builder|reviewer|team|customer|owner|manager|partner)s?\b", re.I)
INITIATIVE = re.compile(r"without a ticket|on her own|on his own|unprompted|initiative", re.I)
REVIEW_ID = re.compile(r"\bCR-(\d+)\b|\bPR #(\d+)|/pull/(\d+)\b|/reviews?/(\d+)\b", re.I)
JARGON = re.compile(r"\b(leverage|play|strategic|proactive|cultivat\w*|drive alignment|synerg\w*|holistic|paradigm)\b", re.I)
ROLE_WORD = re.compile(r"\b(senior builder|product manager|principal engineer|bar[- ]raiser)\b", re.I)   # D41
UNVERIFIED_HOSTS = ["docs.google.com"]
SUPPORTED_TAG = re.compile(r"\(SUPPORTED\)")
SENTENCE_SPLIT = re.compile(r"(?<=[.!?)])\s+(?=[A-Z\"\u201c])")   # a closing marker `)` ends a sentence too (round 4c)

# round 4 shape (D56 to D70)
CANDIDATE_SUBJECT_SHARE = 0.6   # candidate-subject-share warns under this share of action sentences (settled on the fixtures, D64)
MONTHS = re.compile(r"\b\d+ months?\b", re.I)
REVIEW_COUNT = re.compile(r"\b(authored|reviewed|wrote|landed|merged) \d[\d,]*( code)? reviews?\b|\b\d[\d,]* (code )?reviews?\b", re.I)
STORY_LEAD = re.compile(r"^\*\*Q[1-4] \d{4}, (.+?):\*\*")      # non-greedy to the first `:**`, so a `::` identifier or a code span with a colon stays whole (round 4c)
BRACKETED_CRITERION = re.compile(r"\*\*\s*\(([A-Za-z][A-Za-z ]+)\)")

# round 4c (the first end-to-end review's "What the gate cannot see yet", decisions D72 to D80)
SUBTRACTION_CREDIT = re.compile(r"with the \w+ (core|design|schema|component) (from|by|authored by) (a|another|a second|the) builder|under (a|another|the) [^.]* design|\b(onto|into|on top of) (a|an|another|the) (\w+ ){0,3}(core|design|schema) ((that|which) )?(a|another|the) (teammate|builder|team)\b", re.I)   # credit-not-subtraction, D74, the onto/into/on top of paraphrase D83. The instance copies this string as its contract twin
ORDERING_WORD = re.compile(r"\b(first|before|then|after|earlier)\b", re.I)
ARTIFACT_NOUN = re.compile(r"\b(reviews?|tickets?|documents?|docs?|notes?|designs?|pages?|dashboards?|analys[ie]s|commits?|pull requests?|CR|PR)\b")   # an unlinked event the one-link warning can point at
US_DATE = re.compile(r"\b(\d{1,2})/(\d{1,2})/(\d{4})\b")
MARKER_END = re.compile(r"\((TO BE CONFIRMED|TO BE COLLECTED(: [^()]+)?)\)\.?$")
COLLECTED_CLAUSE = re.compile(r"\b(because|which|whether|so that|since|as the|as no|as nobody)\b", re.I)
WHY_NOW_SENTENCE_CAP = 60      # why-now-sentence-shape, D76
PRONOUN_WINDOW = 12            # words after the closing bold of an `On **Project**,` sentence
ON_PROJECT = re.compile(r"^On \*\*[^*]+\*\*,?\s*(.*)$")
ROLLUP_COUNT = re.compile(r"\b(\d+) (projects?|initiatives?|stories)\b", re.I)
FIGURE = re.compile(r"(\d[\d,]*(?:\.\d+)?)\s?(%|percent\b|x\b|times\b|[A-Za-z]+)?")
FIGURE_STOPWORDS = {"and", "of", "to", "in", "a", "an", "the", "or", "per", "at", "on", "by", "for", "from", "with", "into", "across", "than", "that", "its", "was", "is", "are", "were", "ahead", "before", "after", "since", "as"}
BULLET = re.compile(r"^\s*([-*+]|\d+[.)])\s+")
ALTITUDE_FORM = re.compile(r"^A strong [A-Z][\w ]* would have\b")           # D24 counterfactual, exempt from no-trait-words
ABSENCE = re.compile(r"\b(no|never|nobody|no one|nothing|none|not exist(ed)?|could not|couldn't|had no|without|undefined|unowned|missing|lacked|exposed no|did not|had not|unmapped)\b", re.I)
ACTION_VERB = re.compile(r"\b(cut|fell|dropped|rose|reached|shipped|launched|deleted|migrated|closed|reduced|raised|grew|took|went|parsed|passed|adopted|run|runs|ran|infer|inferred|supported|stayed|copied|moved|built|wrote|fixed|removed|finished|landed|returned|served|handled|added|saved|replaced|held|uses|used|extends|extended|merged|delivered|freed|stopped|opened|came|left|put|kept|read|sent|made|got|gone|are|is|were|was)\b|\b[a-z]{3,}ed\b", re.I)
REUSE = re.compile(r"\b(now (uses?|runs?|run every|extends?|plans? from|reads?|ships?|follows?)|adopted|reused|copied|extend(s|ed)?|baseline|reference|plans? from|run(s)? every|standard|took over|picked up|carries|uses it|use it|rely on|relies on|built on|now points?|pattern to copy|copied)\b", re.I)
NO_REUSE = "No reuse by others is on record."
PRONOUNS = ("she", "he", "they")

# round 4 close-out (the round 4c review's section H, decisions D86 to D89)
HEADLINE_IDENTIFIER = re.compile(r"\b(CR|MCM|PR|review|ticket|issue)[- #]?\d{2,}\b|\]\(https?://[^)]*/(reviews?|tickets?|mcms?|issues?|pull)/\d+", re.I)   # headline-no-identifier, D87


def house_rules_path():
    import os
    env = os.environ.get("PROMO_LINT_HOUSE_RULES", "").strip()
    if env:
        return env
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "skills", "leadership-writing", "house-rules.md")


def trait_denylist(path=None):
    """The no-superlatives banlist, trait words and quoted claim phrases, read from the house rule
    line `- **no-superlatives**: ...` so the lint and the house rule cannot drift (D63, D71).
    Returns (words, phrases, error). A missing or unparseable file is a lint failure, never a
    silent pass."""
    path = path or house_rules_path()
    try:
        with open(path, encoding="utf-8") as fh:
            line = next((l for l in fh if l.startswith("- **no-superlatives**")), None)
    except OSError:
        return [], [], f"house rules not readable at {path}, set PROMO_LINT_HOUSE_RULES"
    if not line:
        return [], [], f"no `- **no-superlatives**` line in {path}"
    words = []
    for label in (r"Banlist \(not exhaustive\):", r"Trait words[^:]*:"):
        m = re.search(label + r"\s*([^.]+)\.", line)
        if m:
            words += [w.strip() for w in m.group(1).split(",") if w.strip()]
    m = re.search(r"Claim phrases:\s*(.+?)\. Quotes attributed", line)
    phrases = re.findall(r'"([^"]+)"', m.group(1)) if m else []
    if not words or not phrases:
        return words, phrases, f"could not parse the banlist, trait words and claim phrases from {path}"
    return words, phrases, None


def trait_pattern(words, phrases):
    """One regex for the denylist. The three demonstrat- forms become one pattern that passes a
    factual object (`demonstrated that`, `demonstrated the fix`) and fails a trait or principle
    noun (`demonstrated exceptional ownership`, `demonstrating customer obsession`)."""
    alts = [r"\b" + re.escape(w) + r"\b" for w in words]
    for p in phrases:
        if p.startswith("demonstrat"):
            continue
        alts.append(r"\b" + re.escape(p) + r"\b")
    if any(p.startswith("demonstrat") for p in phrases):
        alts.append(r"\bdemonstrat(?:es|ed|ing)\b(?!\s+(?:that|how|why|the|a|an|this|it|its|with|by|in|on|to)\b)")
    return re.compile("|".join(alts), re.I)


def first_name(lines):
    for l in lines:
        m = TITLE.match(l)
        if m:
            return m.group(1).strip().split()[0]
    return None


def header_field(lines, label):
    pat = re.compile(r"^-?\s*" + re.escape(label) + r":\s*(.+?)\s*$")
    return next((pat.match(l).group(1) for l in lines if pat.match(l)), None)


def candidate_pronoun(story_paragraphs):
    """PROMO_LINT_CANDIDATE_PRONOUN (the instance sets it from the candidate-facts block, D64), else
    the commonest of she, he, they across the story paragraphs."""
    import os
    env = os.environ.get("PROMO_LINT_CANDIDATE_PRONOUN", "").strip().lower()
    if env:
        return env
    text = " ".join(story_paragraphs).lower()
    counts = {p: len(re.findall(r"\b" + p + r"\b", text)) for p in PRONOUNS}
    best = max(counts, key=counts.get)
    return best if counts[best] else "she"


def opens_on_candidate(sentence, name, pronoun):
    """True when the sentence opens with the candidate's first name or pronoun and a word follows
    (the verb). `Dana's` and `Dana,` do not count, the actor must be the subject."""
    subj = [re.escape(name)] if name else []
    subj.append(pronoun)
    return re.match(r"^(?:" + "|".join(subj) + r")\s+[a-z]", sentence, re.I) is not None


def unverified_hosts():
    import os
    extra = [h.strip() for h in os.environ.get("PROMO_LINT_UNVERIFIED_HOSTS", "").split(",") if h.strip()]
    return UNVERIFIED_HOSTS + extra


def exempt_links():
    import os
    return [s.strip() for s in os.environ.get("PROMO_LINT_LINK_EXEMPT", "").split(",") if s.strip()]


def sentences(paragraph):
    """Sentences of a prose paragraph. A `(TO BE CONFIRMED)` after the full stop stays with the
    sentence it closes, because the split only happens before a capital letter or a quote mark."""
    return [s.strip() for s in SENTENCE_SPLIT.split(paragraph) if s.strip()]


def words(lines):
    text = "\n".join(l for l in lines if not l.lstrip().startswith(">") and not HEADING.match(l))
    text = re.sub(r"\]\([^)]*\)", "]", text)
    return len(WORD.findall(text))


def excerpt(s, n=60):
    s = s.strip()
    return s if len(s) <= n else s[: n - 3] + "..."


def split_sections(lines, level):
    """(title, body) for every heading of exactly `level`, body up to the next heading of the same
    or a higher level."""
    out, cur, body = [], None, []
    for l in lines:
        m = HEADING.match(l)
        if m and len(m.group(1)) <= level:
            if cur is not None:
                out.append((cur, body))
            cur, body = (m.group(2) if len(m.group(1)) == level else None), []
            continue
        if cur is not None:
            body.append(l)
    if cur is not None:
        out.append((cur, body))
    return out


def leadins(body, wanted):
    return [LEADIN.match(l).group(1).strip() for l in body if LEADIN.match(l) and LEADIN.match(l).group(1).strip() in wanted]


def paragraphs(body):
    """Prose paragraphs of a story body between the Headline line and the quote: blank-line
    separated blocks, headings and blockquote lines excluded."""
    out, cur, seen_headline = [], [], False
    for l in body:
        if not seen_headline:
            if l.strip():
                seen_headline = True
            continue
        if l.startswith(">"):
            break
        if not l.strip() or HEADING.match(l):
            if cur:
                out.append(" ".join(cur))
                cur = []
            continue
        cur.append(l.strip())
    if cur:
        out.append(" ".join(cur))
    return out


READINESS = re.compile(r"^Readiness: (Ready|Ready with gaps|Not ready)\s*$", re.M)


def prose_paragraphs(body):
    """Blank-line separated prose blocks of a section body, headings, blockquotes and table rows
    excluded (Scope of Role, Why now, the reasons intro)."""
    out, cur = [], []
    for l in body:
        if not l.strip() or HEADING.match(l) or l.startswith(">") or l.startswith("|"):
            if cur:
                out.append(" ".join(cur))
                cur = []
            continue
        cur.append(l.strip())
    if cur:
        out.append(" ".join(cur))
    return out


def body_before_first_heading(body):
    out = []
    for l in body:
        if HEADING.match(l):
            break
        out.append(l)
    return out


def lint_why_now_shape(body, fail, trait_check):
    """why-now-one-paragraph (D56): one prose paragraph, no bullet, no sub-heading, no link, no
    bracketed criterion after a bold span, no bold span over six words, and every bold project
    name (a bold span with no digit) sits in a sentence carrying a number and its baseline."""
    sec = "Why now"
    for l in body:
        if HEADING.match(l):
            fail("why-now-one-paragraph", sec, f"sub-heading `{excerpt(l)}`, Why now is one paragraph (D56)")
        if BULLET.match(l):
            fail("why-now-one-paragraph", sec, f"bullet `{excerpt(l)}`, Why now is one paragraph of full sentences (D56)")
        if LINK.search(l) or BARE_URL.search(l):
            fail("why-now-one-paragraph", sec, f"link in `{excerpt(l)}`, Why now carries no links, the stories do (D56)")
    paras = prose_paragraphs(body)
    for extra in paras[1:]:
        fail("why-now-one-paragraph", sec, f"{len(paras)} paragraphs, need 1, fold this one in or move it to its story: `{excerpt(extra)}`")
    text = " ".join(paras)
    for m in BRACKETED_CRITERION.finditer(text):
        fail("why-now-one-paragraph", sec, f"`({m.group(1)})` is a bracketed criterion, the story heading carries it (D56)")
    for b in BOLD.findall(text):
        n = len(b.split())
        if (n > 6 and not re.search(r"\d", b)) or n > 12:
            fail("why-now-one-paragraph", sec, f"bold span of {n} words reads as a list item, bold the project name or the number with its baseline, not the sentence (D56): `{excerpt(b)}`")
    names = {b.strip() for b in BOLD.findall(text) if not re.search(r"\d", b) and len(b.split()) <= 6}
    sents = sentences(text)
    for nm in sorted(names):
        carrying = [s for s in sents if nm in s]
        if not any(re.search(r"\d", s) and (COMPARATOR.search(s) or RELATIVE.search(s)) for s in carrying):
            fail("why-now-one-paragraph", sec, f"bold project `{nm}` has no sentence with a number and its baseline, write `On **{nm}**, <verbs> and <landing figure with baseline>` (D56)")


def readiness_path(draft_path):
    """The readiness table is a stage document beside the draft, not a section of it:
    <stem>.readiness.md next to a fixture, or gap-analysis.md in a run directory."""
    import os
    d, base = os.path.split(draft_path)
    stem = base[:-3] if base.endswith(".md") else base
    for cand in (os.path.join(d, stem + ".readiness.md"), os.path.join(d, "gap-analysis.md")):
        if os.path.exists(cand):
            return cand
    return None


NOT_READY_BANNER = re.compile(r"^\*\*Not ready for submission\*\*", re.M)


def lint_readiness(path, draft_text=""):
    """readiness-first. draft_text lets the document declare the draft_with_readiness mode with its banner."""
    banner = bool(NOT_READY_BANNER.search(draft_text or ""))
    if path is None:
        return ["readiness-first document: no readiness table beside the draft (<stem>.readiness.md or gap-analysis.md) with a `Readiness: Ready | Ready with gaps | Not ready` verdict"]
    with open(path, encoding="utf-8") as fh:
        t = fh.read()
    m = READINESS.search(t)
    if not m:
        return [f"readiness-first {path}: no `Readiness: Ready | Ready with gaps | Not ready` verdict line"]
    if not re.search(r"^\| *(?:# *\| *)?Criterion *\| *Evidence *\| *(Met / Partly / Not met|Status) *\| *Gap *\|", t, re.M):   # an optional # column first (house table shape, 11/27/2026)
        return [f"readiness-first {path}: no table with columns Criterion, Evidence, Met / Partly / Not met, Gap"]
    if m.group(1) == "Not ready":
        if banner:
            out = []
            if not re.search(r"^## Readiness$", draft_text, re.M):
                out.append(f"readiness-first {path}: verdict is Not ready and the document carries the Not ready banner, but no `## Readiness` section copies the verdict and table into the document")
            return out
        return [f"readiness-first {path}: verdict is Not ready, the writer returns the table and gap list instead of a document (or the document declares readiness mode draft_with_readiness with a `**Not ready for submission**` banner and a `## Readiness` section)"]
    if banner:
        return [f"readiness-banner {path}: the document carries the `**Not ready for submission**` banner but the verdict is {m.group(1)}, banner and verdict must agree"]
    return []


def candidate_names(lines):
    """The candidate's names the Scope section may not carry: the full name from the title and the
    Employee Name line, each of its words of three letters or more, and the alias from
    PROMO_LINT_CANDIDATE_ALIAS (the instance workflow sets it, no alias lives in this file)."""
    import os
    names = set()
    for l in lines:
        m = TITLE.match(l) or EMPLOYEE_LINE.match(l)
        if m:
            full = m.group(1).strip()
            names.add(full)
            names.update(w for w in re.findall(r"[A-Za-z][A-Za-z'-]{2,}", full))
    alias = os.environ.get("PROMO_LINT_CANDIDATE_ALIAS", "").strip()
    if alias:
        names.add(alias)
    return sorted(names, key=len, reverse=True)


def lint_scope(body, names, fail):
    """scope-no-candidate (D49): the section is about the team and the proposed level. One failure per
    class per sentence: the candidate's name or alias, a hire or join word (with or without its
    date), a prior-team sentence."""
    text = " ".join(l.strip() for l in body if l.strip() and not HEADING.match(l))
    for s in sentences(text):
        hit = next((n for n in names if re.search(r"\b" + re.escape(n) + r"\b", s)), None)
        if hit:
            fail("scope-no-candidate", "Scope of Role", f"`{hit}` names the candidate, the section is about the team and the proposed level: `{excerpt(s)}`")
        hw = HISTORY_WORD.search(s)
        if hw:
            what = "a hire or join date" if DATE.search(s) or re.search(r"\b(19|20)\d{2}\b", s) else "the candidate's history"
            fail("scope-no-candidate", "Scope of Role", f"`{hw.group(0)}` gives {what}, that belongs in the header or a story: `{excerpt(s)}`")
        pt = PRIOR_TEAM.search(s)
        if pt:
            fail("scope-no-candidate", "Scope of Role", f"`{pt.group(0)}` is a prior-team sentence: `{excerpt(s)}`")


def tenure_days(s):
    """A day count used as a tenure unit: `N days` in a sentence that also names a level, a role,
    tenure or a title (`as an Engineer II`). `2 days ahead of the deadline` is a delivery figure and
    is left alone (D50)."""
    m = DAYS.search(s)
    if m and (TENURE_CONTEXT.search(s) or TITLE_CONTEXT.search(s)):
        return m.group(0)
    return None


def relative_first(s):
    """relative-first (D51). Returns the failure text for a sentence that carries both a relative
    figure and an absolute pair in the wrong order or without the round brackets, else None."""
    r, a = RELATIVE.search(s), ABSOLUTE_PAIR.search(s)
    if not r or not a:
        return None
    if a.start() < r.start():
        return f"absolutes `{a.group(0)}` come before the relative `{r.group(0).strip()}`, write the relative first and the absolutes in round brackets"
    between = s[r.end():a.start()]
    if between.count("(") <= between.count(")"):
        return f"absolutes `{a.group(0)}` follow the relative `{r.group(0).strip()}` but not in round brackets"
    return None


def body_text(line):
    """A line with its link targets and bare URLs removed, for rules that read dates in prose."""
    return BARE_URL.sub("", re.sub(r"\]\([^)]*\)", "]", line))


# --- round 4c: the stage documents the lint may read ---------------------------------------------

def figure_text(text):
    """Prose with the tokens that look like figures but are not removed: link targets, bare URLs,
    code review ids, dates (year-first, MM/DD/YYYY and M/D), and the thousands commas."""
    t = body_text(text)
    t = re.sub(r"\b(CR|PR)[- #]?\d+\b", " ", t)
    t = ISO_DATE.sub(" ", t)
    t = re.sub(r"\b\d{1,2}/\d{1,2}(/\d{2,4})?\b", " ", t)
    t = re.sub(r"(?<=\d),(?=\d)", "", t)
    return t


def figures(text):
    """The figures of an impact-data cell as (number, unit) keys. A number with three or more digits,
    a decimal point, a percent or an x-factor is a figure on its own (unit kept for % and x). A one
    or two digit integer is a figure only with the unit word that follows it (`7 months`, `5 s`),
    because a bare `7` matches half the document. Normalises percent to % and times to x."""
    out = []
    for m in FIGURE.finditer(figure_text(text)):
        num, unit = m.group(1), (m.group(2) or "").lower()
        num = num.rstrip(".")
        unit = {"percent": "%", "times": "x"}.get(unit, unit)
        digits = re.sub(r"\D", "", num)
        if not digits:
            continue
        if len(digits) >= 3 or "." in num or unit in ("%", "x"):
            out.append((num, unit if unit in ("%", "x") else ""))
        elif unit and unit not in FIGURE_STOPWORDS and len(unit) >= 1 and unit.isalpha():
            out.append((num, unit))
    return out


def figure_in(sentence, key):
    """True when the figure key appears in the sentence (commas, link targets and dates removed)."""
    num, unit = key
    t = figure_text(sentence)
    n = re.escape(num)
    if unit == "%":
        return re.search(r"(?<![\d.])" + n + r"\s?(%|percent\b)", t, re.I) is not None
    if unit == "x":
        return re.search(r"(?<![\d.])" + n + r"\s?(x\b|times\b)", t, re.I) is not None
    if unit:
        return re.search(r"(?<![\d.])" + n + r"\s?" + re.escape(unit.rstrip("s")) + r"s?\b", t, re.I) is not None
    return re.search(r"(?<![\d.])" + n + r"(?![\d.]\d)", t) is not None


def impact_rows(path):
    """Marked rows of an impact-data stage document: every table row whose first cell is a row
    number and whose LAST cell (the status, `Evidence holds` or `Status`) carries (TO BE CONFIRMED)
    or (TO BE COLLECTED. Returns (row number, marker, figure keys, number cell). When the status cell
    itself names figures in the sentence that carries the marker (`The 7 months claim is not in any file (TO BE CONFIRMED)`), those are the marked figures
    and the number cell's held figures stay free. Otherwise every figure of the number cell is
    marked (marker-propagation, D72)."""
    rows = []
    with open(path, encoding="utf-8") as fh:
        for l in fh:
            if not l.startswith("|"):
                continue
            cells = [c.strip() for c in l.strip().strip("|").split("|")]
            if len(cells) < 3 or not re.fullmatch(r"\d+", cells[0]):
                continue
            status = cells[-1]
            if "(TO BE CONFIRMED)" in status:
                marker = "(TO BE CONFIRMED)"
            elif "(TO BE COLLECTED" in status:
                marker = "(TO BE COLLECTED"
            else:
                continue
            marked = [seg for seg in re.split(r"(?<=\.)\s+", status) if "(TO BE" in seg]
            keys = figures(" ".join(marked)) or figures(cells[1])
            if keys:
                rows.append((cells[0], marker, keys, cells[1]))
    return rows


def held_rows(path):
    """Held figures of an impact-data stage document: for every numbered table row, the figures of
    the number cell that no marker covers. An unmarked row holds every figure. A marked row whose
    status names the unheld figure in the marker's own sentence (`5.5x held with its baseline. 1.5%
    to 3.7% not in the body (TO BE CONFIRMED)`) holds the rest, the same split impact_rows makes.
    Returns (row number, figure keys, number cell). reuse-named (D67 amended by D88) is silent
    when a result paragraph's last sentence carries one of these figures, because the D79 note
    lets a top-ranked story end on its held figure instead of a user name."""
    rows = []
    with open(path, encoding="utf-8") as fh:
        for l in fh:
            if not l.startswith("|"):
                continue
            cells = [c.strip() for c in l.strip().strip("|").split("|")]
            if len(cells) < 3 or not re.fullmatch(r"\d+", cells[0]):
                continue
            status = cells[-1]
            all_keys = figures(cells[1])
            if "(TO BE CONFIRMED)" in status or "(TO BE COLLECTED" in status:
                marked = [seg for seg in re.split(r"(?<=\.)\s+", status) if "(TO BE" in seg]
                marked_keys = figures(" ".join(marked)) or all_keys
                keys = [k for k in all_keys if k not in marked_keys]
            else:
                keys = all_keys
            if keys:
                rows.append((cells[0], keys, cells[1]))
    return rows


def sentence_marker(sentence):
    """The marker a sentence ends on: `(TO BE CONFIRMED)`, `(TO BE COLLECTED`, or None."""
    m = MARKER_END.search(sentence.strip())
    if not m:
        return None
    return "(TO BE CONFIRMED)" if m.group(1) == "TO BE CONFIRMED" else "(TO BE COLLECTED"


def lint_marker_propagation(sec, sentence, rows, fail, why_now=False):
    """marker-propagation (D72): a figure that matches a marked impact-data row sits in a sentence
    ending on the same marker. In Why now no marker is allowed (D55), so the figure moves to its
    story. One failure per row per sentence."""
    ending = sentence_marker(sentence)
    for n, marker, keys, cell in rows:
        hit = next((k for k in keys if figure_in(sentence, k)), None)
        if hit is None or ending == marker:
            continue
        shown = (hit[0] + (" " + hit[1] if hit[1] and hit[1] not in ("%", "x") else hit[1])).strip()
        where = "move the figure to its story and end that sentence with the marker (D55)" if why_now else f"end the sentence with `{marker}{')' if marker.endswith('COLLECTED') else ''}`"
        fail("marker-propagation", sec, f"`{shown}` matches impact-data row {n} (`{excerpt(cell, 40)}`) whose status carries {marker}{')' if marker.endswith('COLLECTED') else ''}, {where}: `{excerpt(sentence)}`")


def lint_marker_form(sec, sentence, fail):
    """markers-consistent, the form half (D75, D46): a marker is the last token of its sentence, and
    the clause after `TO BE COLLECTED:` names an artifact, not an explanation (no because, which,
    whether, so that, since). The CONFIRMED position is also checked per line above."""
    for m in MARKER_COLLECTED.finditer(sentence):
        tail = sentence[m.end():].strip().lstrip(".").strip()
        if tail:
            fail("markers-consistent", sec, f"`(TO BE COLLECTED ...)` is not the last token of its sentence, `{excerpt(tail, 40)}` follows it (D75): `{excerpt(sentence)}`")
        inner = (m.group(1) or "")[2:]
        if inner and (COLLECTED_CLAUSE.search(inner) or len(inner.split()) > 12):
            fail("markers-consistent", sec, f"`(TO BE COLLECTED: {excerpt(inner, 40)})` explains instead of naming the artifact, the stage document holds the reason (D46, D75): `{excerpt(sentence)}`")


def read_dates(path):
    """`url,date` rows of a dates csv. The date is MM/DD/YYYY or YYYY-MM-DD, returned as (y, m, d)."""
    out = {}
    with open(path, encoding="utf-8") as fh:
        for l in fh:
            if "," not in l or l.lower().startswith("url,"):
                continue
            url, date = (x.strip() for x in l.strip().rsplit(",", 1))
            d = parse_date(date)
            if url and d:
                out[url] = d
    return out


def parse_date(s):
    m = US_DATE.search(s)
    if m:
        return (int(m.group(3)), int(m.group(1)), int(m.group(2)))
    m = ISO_DATE.search(s)
    if m:
        y, mo, d = m.group(0).split("-")
        return (int(y), int(mo), int(d))
    return None


def artifact_dates(sentence, dates):
    """(label, url, date) per linked artifact in a sentence. The date is the csv row for the url
    (exact or substring), else the first MM/DD/YYYY after the link before the next link, else the
    one before it since the previous link."""
    links = list(re.finditer(r"\[([^\]]+)\]\((https?://[^)]+)\)", sentence))
    out = []
    for i, m in enumerate(links):
        url = m.group(2)
        d = dates.get(url) or next((v for k, v in dates.items() if k in url or url in k), None)
        if d is None:
            after = sentence[m.end(): links[i + 1].start() if i + 1 < len(links) else len(sentence)]
            before = sentence[links[i - 1].end() if i else 0: m.start()]
            d = parse_date(after) or parse_date(before)
        out.append((m.group(1), url, d))
    return out


def lint_ordering(sec, sentence, dates, have_dates, fail, warnings):
    """ordering-stamped (D73, D81): a story sentence (any paragraph between the Headline and the
    quote, not only the action paragraph) with first, before, then, after or earlier that
    links two or more dated artifacts whose dates run against the words fails. The claimed order is
    the textual order, reversed for a pair with `after` or `earlier` between them, or with `before`
    ahead of both. One linked artifact: warning. A linked artifact with no readable date when a dates
    file was given: warning. The checklist blocker ordering-words-stamped reads the stamps the lint
    cannot."""
    ow = ORDERING_WORD.search(sentence)
    if not ow:
        return
    arts = artifact_dates(sentence, dates)
    if not arts:
        return
    if len(arts) == 1:
        rest = re.sub(r"\[[^\]]+\]\([^)]+\)", " ", sentence)
        if ARTIFACT_NOUN.search(rest) or US_DATE.search(rest):
            warnings.append(f"warning ordering-stamped {sec}: `{ow.group(0)}` orders one linked artifact against an event with no stamp in the sentence, link the other event or drop the order (checklist ordering-words-stamped, D73): `{excerpt(sentence)}`")
        return
    for label, url, d in arts:
        if d is None and have_dates:
            warnings.append(f"warning ordering-stamped {sec}: no date for `{label}` ({excerpt(url, 40)}) in the sentence or the dates file, the order it sits in cannot be checked (D73)")
    spans = [m for m in re.finditer(r"\[[^\]]+\]\([^)]+\)", sentence)]
    head = sentence[: spans[0].start()]
    for i in range(len(arts) - 1):
        a, b = arts[i], arts[i + 1]
        if a[2] is None or b[2] is None:
            continue
        between = sentence[spans[i].end(): spans[i + 1].start()]
        reversed_pair = re.search(r"\b(after|earlier)\b", between, re.I) is not None or (i == 0 and re.search(r"\bbefore\b", head, re.I) is not None and not re.search(r"\b(first|then|after|earlier)\b", between, re.I))
        earlier, later = (b, a) if reversed_pair else (a, b)
        if earlier[2] == later[2]:
            warnings.append(f"warning ordering-stamped {sec}: `{earlier[0]}` and `{later[0]}` carry the same date, write both in one clause with no order (checklist ordering-words-stamped, D44)")
        elif earlier[2] > later[2]:
            fail("ordering-stamped", sec, f"`{excerpt(sentence)}` claims `{earlier[0]}` before `{later[0]}`, dates {fmt_date(earlier[2])} and {fmt_date(later[2])} run the other way, write both in one clause or drop the order (checklist ordering-words-stamped, D73)")


def fmt_date(d):
    return f"{d[1]:02d}/{d[2]:02d}/{d[0]}"


DATE_LINK_WINDOW = 40          # dates-printed-match-csv, D82: characters between a printed date and the link it belongs to
CROSS_REFERENCE = re.compile(r"\b(above|below|earlier)\b", re.I)   # why-now-sentence-shape floor, D85: `<figure> above` is not the sentence's own figure
WHY_NOW_SENTENCE_FLOOR = 10    # why-now-sentence-shape floor, D85


def lint_dates_printed(sec, sentence, dates, fail, warnings=None):
    """dates-printed-match-csv (D82, blocker when `--dates` is given): a MM/DD/YYYY date printed
    within DATE_LINK_WINDOW characters of a linked artifact equals that artifact's csv date. The
    csv holds the SHIPPED date and the draft prints the shipped date, so a created date beside a
    review link (the reader cannot see which one it is) fails naming both. The nearest link owns
    the date. A link with no csv row is a `dates-csv-coverage` warning (D86): the date it carries
    is not checked by anything, so the writer adds the row or moves the date. Because the nearest
    link owns the date, a neighbouring link's date never fires on a link with no row."""
    links = list(re.finditer(r"\[([^\]]+)\]\((https?://[^)]+)\)", sentence))
    if not links:
        return
    for dm in US_DATE.finditer(sentence):
        def gap(lm):
            return max(0, lm.start() - dm.end(), dm.start() - lm.end())
        nearest = min(links, key=gap)
        if gap(nearest) > DATE_LINK_WINDOW:
            continue
        url = nearest.group(2)
        row = dates.get(url) or next((v for k, v in dates.items() if k in url or url in k), None)
        if row is None:
            if warnings is not None:
                warnings.append(f"warning dates-csv-coverage {sec}: `{dm.group(0)}` beside `{nearest.group(1)}` has no dates.csv row, so nothing checks it, add a row for {url} or move the date (D86): `{excerpt(sentence)}`")
            continue
        printed = parse_date(dm.group(0))
        if printed and printed != row:
            fail("dates-printed-match-csv", sec, f"`{dm.group(0)}` beside `{nearest.group(1)}` is not the dates file's {fmt_date(row)} for it, the draft prints the shipped date the csv holds, so one of the two is the created date (D82): `{excerpt(sentence)}`")


def lint_why_now_sentence_shape(sentence, k, name, pronoun, fail, warnings=None):
    """why-now-sentence-shape (D76): no Why now sentence over WHY_NOW_SENTENCE_CAP words, and an
    `On **Project**,` sentence names the candidate (pronoun or first name) within PRONOUN_WINDOW
    words after the closing bold. Floor (D85, warning): a sentence under WHY_NOW_SENTENCE_FLOOR
    words with no figure of its own, a `<figure> above|below|earlier` cross-reference is not its
    own, carries no new fact for the VP."""
    n = len(WORD.findall(sentence.replace("**", "")))
    if n > WHY_NOW_SENTENCE_CAP:
        fail("why-now-sentence-shape", "Why now", f"sentence {k + 1} runs {n} words, cap {WHY_NOW_SENTENCE_CAP}, split it (D76): `{excerpt(sentence)}`")
    if warnings is not None and n < WHY_NOW_SENTENCE_FLOOR:
        own = [m for m in re.finditer(r"\d[\d,.]*%?", sentence) if not CROSS_REFERENCE.search(sentence[m.end(): m.end() + 24])]
        if not own:
            warnings.append(f"warning why-now-sentence-shape Why now: sentence {k + 1} runs {n} words, floor {WHY_NOW_SENTENCE_FLOOR}, and carries no figure of its own, a cross-reference tells the VP nothing new, cut it or fold its fact into the project's sentence (D85): `{excerpt(sentence)}`")
    m = ON_PROJECT.match(sentence)
    if m:
        head = WORD.findall(m.group(1).replace("**", ""))[:PRONOUN_WINDOW]
        subj = {pronoun} | ({name.lower()} if name else set())
        if not any(w.lower().strip(".,'") in subj or w.lower().strip(".,").rstrip("'s") in subj for w in head):
            fail("why-now-sentence-shape", "Why now", f"`On **Project**,` sentence holds `{pronoun}` or `{name}` back past {PRONOUN_WINDOW} words, the candidate's verb comes right after the project (D76): `{excerpt(sentence)}`")


def lint_rollup_counts(sentence, stories, warnings):
    """rollup-counts-held (D77, warning): a `N projects`, `N initiatives` or `N stories` count in the
    closing Why now sentence agrees with the story headings (distinct projects, or headings for
    stories). The checklist row of the same name reads the impact-data rows for the other counts."""
    distinct = len({p.lower() for p, _, _ in stories})
    for m in ROLLUP_COUNT.finditer(sentence):
        n, noun = int(m.group(1)), m.group(2).lower()
        actual = len(stories) if noun.startswith("stor") else distinct
        if actual and n != actual:
            warnings.append(f"warning rollup-counts-held Why now: closing sentence counts `{m.group(0)}`, the draft has {actual} {'story headings' if noun.startswith('stor') else 'distinct story projects'} (D77): `{excerpt(sentence)}`")


def lint(text, impact=None, dates=None, held=None):
    lines = text.splitlines()
    length_fails, fails, warnings, counts = [], [], [], []
    shape = "template"
    marked_projects, reasons = {}, []

    def fail(rule, section, what):
        fails.append(f"{rule} {section}: {what}")

    for pat, name in REQUIRED:
        if not any(re.match(pat, l) for l in lines):
            fail("required-section", "document", f"missing `{name}`")

    collected = confirmed = 0
    frontmatter_end = 0
    if lines and lines[0].strip() == "---":
        frontmatter_end = next((i for i, l in enumerate(lines[1:], 2) if l.strip() == "---"), 0)
    section = None
    for i, l in enumerate(lines, 1):
        hm = HEADING.match(l)
        if hm and len(hm.group(1)) == 2:
            section = hm.group(2)
        in_feedback = section == "Feedback"       # provider text is verbatim by rule (R2), house rules skip it
        in_frontmatter = i <= frontmatter_end     # a leading YAML block is metadata, not prose (R3)
        is_sources = bool(SOURCES_LINE.match(l))
        if ";" in l and not in_feedback:
            fail("no-semicolons", f"line {i}", f"`{excerpt(l)}`")
        if "\u2014" in l and not in_feedback:
            fail("no-em-dash", f"line {i}", f"`{excerpt(l)}`")
        if hm and JARGON.search(hm.group(2)):
            fail("plain-headings", f"line {i}", f"`{excerpt(hm.group(2))}` contains `{JARGON.search(hm.group(2)).group(0)}`, a word from the jargon denylist (house rule plain-headings)")
        if not in_frontmatter and not is_sources and not in_feedback:
            pm = PROCESS_LEAK.search(l)
            if pm:
                fail("no-process-leak", f"line {i}", f"`{pm.group(0)}` talks about the writing, not the candidate: `{excerpt(l)}`")
        collected += len(MARKER_COLLECTED.findall(l)) + (len(MARKER_COLLECTED_QUOTE.findall(l)) if l.startswith(">") else 0)
        confirmed += len(MARKER_CONFIRMED.findall(l))
        if not in_feedback:                       # providers tag principles in square brackets, verbatim (D70)
            for m in MARKER_ANY.finditer(l):
                tok = m.group(0)
                if MARKER_COLLECTED.fullmatch(tok) or MARKER_CONFIRMED.fullmatch(tok) or (l.startswith(">") and MARKER_COLLECTED_QUOTE.fullmatch(tok)):
                    continue
                fail("markers-consistent", f"line {i}", f"`{excerpt(tok)}` is not (TO BE COLLECTED) or (TO BE CONFIRMED)")
            for m in MARKER_CONFIRMED.finditer(l):
                tail = l[m.end():].lstrip(".").lstrip()
                if tail and not tail[0].isupper() and not tail.startswith(("(", "[", "|", "*")):
                    fail("markers-consistent", f"line {i}", f"`(TO BE CONFIRMED)` is not at the end of its sentence: `{excerpt(l)}`")
        if in_frontmatter:
            continue
        iso = ISO_DATE.search(body_text(l))
        if iso:
            fail("date-format", f"line {i}", f"`{iso.group(0)}` is not MM/DD/YYYY, the house date-format rule (D52): `{excerpt(l)}`")
        tm = TENURE_LINE.match(l)
        if tm and not (re.search(r"\b\d+ months?\b", tm.group(1), re.I) and not DAYS.search(tm.group(1))):
            fail("tenure-months", f"line {i}", f"`Time in Current Level: {tm.group(1)}` is not a month count (D50)")
        for m in BARE_URL.finditer(l):
            fail("bare-identifier", f"line {i}", f"bare URL `{excerpt(m.group(0), 40)}`, link it on the artifact's identifier")
        if not l.startswith("#"):
            stripped = LINK.sub("", l)
            for m in BARE_ID.finditer(stripped):
                fail("bare-identifier", f"line {i}", f"`{m.group(0)}` is named but not linked")
    counts.append(f"markers (TO BE COLLECTED): {collected}, (TO BE CONFIRMED): {confirmed}")

    names = candidate_names(lines)
    name, pronoun = first_name(lines), None
    current_title, proposed_title = header_field(lines, "Current Title"), header_field(lines, "Proposed Title")
    trait_words, trait_phrases, trait_err = trait_denylist()
    if trait_err:
        fail("no-trait-words", "document", trait_err)
    traits = trait_pattern(trait_words, trait_phrases) if not trait_err else None

    def trait_check(sec, sentence):
        if traits is None or ALTITUDE_FORM.match(sentence):
            return
        m = traits.search(sentence)
        if m:
            fail("no-trait-words", sec, f"`{m.group(0)}` tells what the sentence should show, replace it with the obstacle, the technique or the figure with its verb (house rule no-superlatives, D63): `{excerpt(sentence)}`")

    # round 4c: the pronoun is needed in Why now, which the loop meets before Evidence
    evidence_paras = [p for t, b in split_sections(lines, 2) if t == "Evidence" for _, sb in split_sections(b, 3) for p in paragraphs(sb)]
    pronoun = candidate_pronoun(evidence_paras)
    why_now_sents, parsed = [], []

    for title, body in split_sections(lines, 2):
        if title == "Scope of Role":
            lint_scope(body, names, fail)
            paras = prose_paragraphs(body)
            if len(paras) != 3:
                fail("scope-current-level", "Scope of Role", f"{len(paras)} paragraphs, need 3: the team and its scale, what the current level does here, what the proposed level does (D68)")
            else:
                if current_title and current_title.lower() not in paras[1].lower():
                    fail("scope-current-level", "Scope of Role", f"middle paragraph does not name the current title `{current_title}`, it describes what the current level does on this team (D68): `{excerpt(paras[1])}`")
                if proposed_title and proposed_title.lower() not in paras[2].lower():
                    fail("scope-current-level", "Scope of Role", f"last paragraph does not name the proposed title `{proposed_title}` (D68): `{excerpt(paras[2])}`")

        if title == "Why now?":
            n = words(body)
            counts.append(f"words Why now: {n} (cap {CAP_WHY_NOW})")
            if n >= CAP_WHY_NOW:
                length_fails.append((n - CAP_WHY_NOW, f"why-now-length Why now: {n} words, cap {CAP_WHY_NOW}"))
            lint_why_now_shape(body, fail, trait_check)
            prose = " ".join(l.strip() for l in body if l.strip() and not HEADING.match(l)).replace("**", "")
            for k, s in enumerate(sentences(prose)):
                if k == 0:
                    if not MONTHS.search(s):
                        fail("why-now-opener", "Why now", f"first sentence carries no month count, open with the months in level and the prior roles (D57): `{excerpt(s)}`")
                    rc = REVIEW_COUNT.search(s)
                    if rc:
                        fail("why-now-opener", "Why now", f"`{rc.group(0)}` is a review count, it belongs in the review-process story, not sentence one (D57): `{excerpt(s)}`")
                    if traits is not None and traits.search(s):
                        fail("why-now-opener", "Why now", f"`{traits.search(s).group(0)}` is a trait word in sentence one (D57): `{excerpt(s)}`")
                else:
                    trait_check("Why now", s)
                if MARKER_COLLECTED.search(s) or MARKER_CONFIRMED.search(s):
                    fail("why-now-no-markers", "Why now", f"`{excerpt(s)}` carries a marker, leave the figure out of Why now and tell it in its story (D55)")
                d = tenure_days(s)
                if d:
                    fail("tenure-months", "Why now", f"`{d}` is a tenure in days, print months (D50): `{excerpt(s)}`")
                rf = relative_first(s)
                if rf:
                    fail("relative-first", "Why now", f"{rf}: `{excerpt(s)}`")
                if impact is not None:
                    lint_marker_propagation("Why now", s, impact, fail, why_now=True)
                lint_marker_form("Why now", s, fail)
            raw = " ".join(l.strip() for l in body if l.strip() and not HEADING.match(l))
            why_now_sents = sentences(raw)
            for k, s in enumerate(why_now_sents):
                lint_why_now_sentence_shape(s, k, name, pronoun, fail, warnings)

        if title == "Evidence":
            stories = split_sections(body, 3)
            if not stories:
                fail("story-shape", "Evidence", "no `### <Project>: <Criterion>` story heading")
            parsed = []
            for head, sbody in stories:
                if ":" not in head:
                    fail("story-shape", excerpt(head, 40), "heading is not `### <Project>: <Criterion>`")
                    project, crit = head.strip(), "(none)"
                else:
                    project, crit = (x.strip() for x in head.rsplit(":", 1))
                parsed.append((project, crit, sbody))
            marked_projects = lint_stories(parsed, fail, length_fails, warnings, counts, trait_check, name, pronoun, impact, dates, held)

        if title == "Best reasons not to promote":
            reasons = split_sections(body, 3)
            if not reasons:
                fail("rntp-leadins", "Best reasons not to promote", "no `### <reason>` headings")
            intro = prose_paragraphs(body_before_first_heading(body))
            if not intro or not re.search(r"\b(\d+|one|two|three|four|both|all|each|every)\b.*\bprovider", " ".join(intro), re.I):
                warnings.append("warning rntp-intro-counts Best reasons not to promote: no intro paragraph counting the providers per theme before the first reason (D69)")
            for head, rbody in reasons:
                sec = f"reason > {excerpt(head, 40)}"
                found = leadins(rbody, RNTP)
                if found != RNTP:
                    fail("rntp-leadins", sec, f"lead-ins found {found}, need {RNTP} in order")
                gap = next((l for l in rbody if l.startswith("**Gap**")), "")
                if gap and not DATE.search(gap):
                    fail("rntp-dated-example", sec, f"**Gap** has no dated example of who pointed it out: `{excerpt(gap)}`")

    if not any(re.match(r"^## Evidence\s*$", l) for l in lines):
        fallback = fallback_stories(lines)
        if fallback:
            shape = "fallback"
            pronoun = candidate_pronoun([p for _, _, sb in fallback for p in paragraphs(sb)])
            marked_projects = lint_stories(fallback, fail, length_fails, warnings, counts, trait_check, name, pronoun, impact, dates, held)
    if marked_projects and reasons:
        lint_rntp_contradiction(reasons, marked_projects, fail)
    if why_now_sents and parsed:
        lint_rollup_counts(why_now_sents[-1], parsed, warnings)

    length_fails.sort(key=lambda x: -x[0])
    return [f for _, f in length_fails] + fails, warnings, counts, shape


def fallback_stories(lines):
    """A draft that predates the template has no `## Evidence` and no `### <Project>: <Criterion>`
    headings. Its stories still sit under criterion headings of one level, written `#### [<Criterion>]`,
    and each story opens with a bold title on a line of its own. Find the shallowest heading level
    with a bracketed title, treat each bracketed heading as a criterion section, and split its body
    at whole-line bold titles. The title line takes the Headline slot, so headline-first fails
    saying so and the per-story rules measure the block (finding R1).

    A non-bracketed heading at the bracketed level (a rubric sentence written as a sibling
    `#### <rubric>` directly under `#### [<Criterion>]`) is body text of the enclosing criterion,
    not a section of its own, so the stories under it still belong to that criterion (round 1c)."""
    bracketed = re.compile(r"^\[(.+)\]\s*$")
    bold_title = re.compile(r"^\*\*[^*]+\*\*\s*$")
    levels = sorted({len(m.group(1)) for l in lines for m in [HEADING.match(l)] if m and bracketed.match(m.group(2))})
    if not levels:
        return []
    level = levels[0]
    sections, crit, body = [], None, []
    for l in lines:
        m = HEADING.match(l)
        if m and len(m.group(1)) <= level:
            b = bracketed.match(m.group(2))
            if b:
                if crit is not None:
                    sections.append((crit, body))
                crit, body = b.group(1).strip(), []
                continue
            if len(m.group(1)) == level and crit is not None:
                body.append(l)      # sibling rubric heading, stays inside the criterion
                continue
            if crit is not None:    # a shallower heading closes the criterion
                sections.append((crit, body))
            crit, body = None, []
            continue
        if crit is not None:
            body.append(l)
    if crit is not None:
        sections.append((crit, body))
    out = []
    for crit, body in sections:
        cur, sbody = None, []
        for l in body:
            if bold_title.match(l):
                if cur is not None:
                    out.append((cur, crit, sbody))
                cur, sbody = l.strip().strip("*").strip(), [l]
                continue
            if cur is not None:
                sbody.append(l)
        if cur is not None:
            out.append((cur, crit, sbody))
    return out


def review_ids(text):
    """Code review identifiers in a paragraph, normalised to the digits: CR-<n>, PR #<n>, a
    /pull/<n> or /reviews/<n> link target (one-cr-once, D37)."""
    return {next(g for g in m.groups() if g) for m in REVIEW_ID.finditer(text)}


def lint_stories(stories, fail, length_fails, warnings, counts, trait_check=lambda sec, s: None, name=None, pronoun="she", impact=None, dates=None, held=None):
    """Per-story rules over (project, criterion, body) triples, from the template shape or the
    fallback splitter. The body's first non-empty line is the Headline slot. Returns the projects
    named inside a marked sentence of any story, for the document-wide rntp-contradiction scan."""
    by_criterion, tellings, review_sites, marked_projects = {}, {}, {}, {}
    projects = [p for p, _, _ in stories]
    hosts, exempt = unverified_hosts(), exempt_links()
    subject_hits, subject_total, subject_offenders = 0, 0, []
    for project, crit, sbody in stories:
        sec = f"{crit} > {project}"
        n = words(sbody)
        counts.append(f"words {sec}: {n} (cap {CAP_STORY})")
        by_criterion.setdefault(crit, []).append(n)
        tellings.setdefault(project.lower(), []).append((crit, n))
        if n >= CAP_STORY:
            length_fails.append((n - CAP_STORY, f"story-length {sec}: {n} words, cap {CAP_STORY}"))
        first = next((l for l in sbody if l.strip()), "")
        if not first.startswith("**Headline**"):
            fail("headline-first", sec, f"first line under the heading is `{excerpt(first)}`, not **Headline**")
        headline = first[len("**Headline**"):].strip() if first.startswith("**Headline**") else ""
        if headline and not re.search(r"\d", headline):
            fail("headline-number", sec, f"`{excerpt(headline)}` has no number")
        if headline and re.search(r"\d", headline) and not COMPARATOR.search(headline):
            fail("headline-baseline", sec, f"`{excerpt(headline)}` has a number with no baseline or comparator (from X to Y, N vs M, ahead of <date>)")
        rf = relative_first(headline) if headline else None
        if rf:
            fail("relative-first", sec, f"{rf}: `{excerpt(headline)}`")
        # headline-no-identifier (D87, warning): a review, ticket or MCM identifier in the Headline
        hid = HEADLINE_IDENTIFIER.search(headline) if headline else None
        if hid:
            warnings.append(f"warning headline-no-identifier {sec}: Headline carries the identifier `{excerpt(hid.group(0), 40)}`, move the identifier to the action paragraph and keep the date (D87): `{excerpt(headline)}`")
        paras = paragraphs(sbody)
        if len(paras) < STORY_PARAGRAPHS:
            fail("story-paragraphs", sec, f"{len(paras)} prose paragraphs between the Headline and the quote, need {STORY_PARAGRAPHS} (situation, task, action, result, no labels)")
        if paras:
            lead = STORY_LEAD.match(paras[0])
            if not lead:
                fail("story-lead", sec, f"first paragraph does not open with a bold `**Qn YYYY, {project}:**` lead (D62): `{excerpt(paras[0])}`")
            elif lead.group(1).strip().lower() != project.lower():
                fail("story-lead", sec, f"lead names `{lead.group(1).strip()}`, the story is `{project}` (D62)")
            # obstacle-first (D65, warning): an absence construction before the candidate's first sentence
            sits = sentences(paras[0])
            before = []
            for s in sits:
                if opens_on_candidate(STORY_LEAD.sub("", s).strip(), name, pronoun):
                    break
                before.append(s)
            if not any(ABSENCE.search(s) for s in before):
                warnings.append(f"warning obstacle-first {sec}: situation paragraph names no absence (no <noun>, nobody, could not, had no) before the candidate's first sentence, name the obstacle in concrete nouns first (D65): `{excerpt(paras[0])}`")
        if len(paras) >= 2 and re.search(r"\bOwnership: ", paras[1]):
            fail("no-star-labels", sec, f"`Ownership:` is a label the reader sees, credit shared work by function inside the sentence instead (D59)")
        for p in paras[:STORY_PARAGRAPHS]:
            m = LEADIN.match(p)
            if m and m.group(1).strip() in ("Situation", "Task", "Action", "Result"):
                fail("no-star-labels", sec, f"`**{m.group(1).strip()}**` is a label the reader sees, STAR is the writer's skeleton only (D28)")
        for p in paras:
            for s in sentences(p):
                trait_check(sec, s)
                # credit-not-subtraction (D74): shared work credited as a subtraction from the candidate's claim
                sub = SUBTRACTION_CREDIT.search(s)
                if sub:
                    fail("credit-not-subtraction", sec, f"`{sub.group(0)}` credits shared work as a subtraction, write the credit as a widening in the same sentence as the candidate's act (house rule credit-inline, D74): `{excerpt(s)}`")
                if impact is not None:
                    lint_marker_propagation(sec, s, impact, fail)
                lint_marker_form(sec, s, fail)
                # ordering-stamped (D73, widened to every paragraph between the Headline and the quote, D81)
                lint_ordering(sec, s, dates or {}, dates is not None, fail, warnings)
                if dates is not None:
                    lint_dates_printed(sec, s, dates, fail, warnings)
        quotes = [l for l in sbody if l.startswith(">")]
        if len(quotes) != 1:
            fail("quote-per-story", sec, f"{len(quotes)} quote lines, need exactly 1")
        elif not QUOTE_LINE.match(quotes[0]):
            fail("quote-form", sec, f"`{excerpt(quotes[0])}` is not `> \"...\", <Name>, <role>`, `> (TO BE COLLECTED: quote from <role>)` or `> [TO BE COLLECTED: quote from <role>]`")
        links = len(LINK.findall("\n".join(sbody)))
        counts.append(f"links {sec}: {links}")
        if links == 0:
            fail("story-links", sec, "0 links, every named artifact is a hyperlink on its identifier")
        # journey-countable (D32): the action paragraph names a journey or another person
        if len(paras) >= 3:
            action = paras[2]
            if not JOURNEY_VERB.search(action) and not JOURNEY_NOUN.search(action):
                fail("journey-countable", sec, f"action paragraph has no journey verb (ruled out, instead of, tried, rejected, aligned, asked) and names no other person: `{excerpt(action)}`")
            for rid in review_ids(action):
                review_sites.setdefault(rid, []).append(sec)
            # candidate-subject-share (D64, warning, document-wide): action sentences opening on the candidate plus a verb
            for s in sentences(action):
                if ALTITUDE_FORM.match(s):
                    continue
                subject_total += 1
                if opens_on_candidate(s, name, pronoun):
                    subject_hits += 1
                else:
                    subject_offenders.append(f"{sec}: `{excerpt(s, 50)}`")
        if len(paras) >= 4:
            result = paras[3]
            rsents = sentences(result)
            # figure-has-verb (D66, warning): a result sentence with a number and no verb
            for s in rsents:
                if re.search(r"\d", s) and not ACTION_VERB.search(s):
                    warnings.append(f"warning figure-has-verb {sec}: result sentence carries a number and no verb, put the figure beside the verb that produced it (D66): `{excerpt(s)}`")
            # reuse-named (D67, warning): the last result sentence names a user or is the no-reuse sentence.
            # Silent when that sentence carries a figure from a HELD impact-data row (D88, needs --impact-data):
            # the D79 checklist note decides whether a top-ranked story ends on its held figure
            last = MARKER_CONFIRMED.sub("", rsents[-1]).strip() if rsents else ""
            held_ending = bool(held) and any(figure_in(last, k) for _, keys, _ in held for k in keys)
            if last and last != NO_REUSE and not held_ending and not (REUSE.search(last) and re.search(r"\b[A-Z][a-z]+\b|\bteams?\b", last[1:])):
                warnings.append(f"warning reuse-named {sec}: result paragraph does not end on who uses the work now (a named team or builder), on a held impact-data figure, or on `{NO_REUSE}` (D67, D88): `{excerpt(last)}`")
            if re.search(r"\bstakeholders\b", last, re.I):
                warnings.append(f"warning reuse-named {sec}: `stakeholders` is not a name (D67): `{excerpt(last)}`")
        # marker-direction (D38): per sentence of the story's prose
        for p in paras:
            # role-words-held (D41): a role given to another person with nothing in the paragraph to hold it
            rw = ROLE_WORD.search(p)
            if rw and not LINK.search(p) and not MARKER_CONFIRMED.search(p) and not MARKER_COLLECTED.search(p):
                warnings.append(f"warning role-words-held {sec}: `{rw.group(0)}` in `{excerpt(p)}` has no link and no marker in its paragraph, back the role with a people-directory row or an artifact, or write builder")
            for s in sentences(p):
                for url in re.findall(r"\]\((https?://[^)]+)\)", s):
                    if any(h in url for h in hosts) and not any(x in url for x in exempt) and not SUPPORTED_TAG.search(s) and not MARKER_CONFIRMED.search(s):
                        fail("marker-direction", sec, f"link to `{excerpt(url, 40)}` cannot be fetched by the writer, its sentence must end (TO BE CONFIRMED) or carry (SUPPORTED): `{excerpt(s)}`")
                if MARKER_CONFIRMED.search(s):
                    bare = MARKER_CONFIRMED.sub("", s)
                    if not LINK.search(bare) and not re.search(r"\d", bare):
                        warnings.append(f"warning marker-direction {sec}: `{excerpt(s)}` has (TO BE CONFIRMED) but names no artifact, link or number, did you mean (TO BE COLLECTED: <artifact>)")
                if MARKER_CONFIRMED.search(s) or MARKER_COLLECTED.search(s):
                    for project in projects:
                        if project.lower() in s.lower():
                            marked_projects.setdefault(project, []).append(sec)
    for rid, secs in review_sites.items():
        if len(secs) > 1:
            fail("one-cr-once", rid, f"review id in the action paragraph of {len(secs)} stories: {', '.join(secs)}, keep it where the claim lives and cross-reference the rest")
    for crit, ns in by_criterion.items():
        total = sum(ns)
        counts.append(f"words section {crit}: {total} over {len(ns)} stories (warn above {MAX_STORIES} stories or {CAP_SECTION} words)")
        if len(ns) > MAX_STORIES or total > CAP_SECTION:
            warnings.append(f"warning section-length {crit}: {len(ns)} stories, {total} words (target at most {MAX_STORIES} stories and {CAP_SECTION} words), move the weakest story to one sentence or an appendix")
    for project, ts in tellings.items():
        full = [c for c, n in ts if n > FULL_TELLING]
        if len(full) > 1:
            fail("one-story-once", project, f"told in full ({FULL_TELLING}+ words) under {len(full)} headings: {', '.join(full)}")
    if subject_total:
        share = subject_hits / subject_total
        counts.append(f"candidate-subject share: {subject_hits} of {subject_total} action sentences ({share:.0%}, warn under {CANDIDATE_SUBJECT_SHARE:.0%})")
        if share < CANDIDATE_SUBJECT_SHARE:
            shown = "; ".join(subject_offenders[:4]).replace(";", ",")
            warnings.append(f"warning candidate-subject-share stories: {subject_hits} of {subject_total} action sentences ({share:.0%}) open on the candidate's name or pronoun plus a verb, target {CANDIDATE_SUBJECT_SHARE:.0%} (D64), offenders: {shown}")
    return marked_projects


def lint_rntp_contradiction(reasons, marked_projects, fail):
    """Lint approximation of the document-wide rntp-contradiction rule (D33): a project that a story
    names inside a marked sentence may not appear, unmarked, in a reason sentence that claims
    initiative (without a ticket, on her own, on his own, unprompted, initiative). The full rule is
    judgement and lives in checklist section H."""
    for head, rbody in reasons:
        sec = f"reason > {excerpt(head, 40)}"
        for p in (l.strip() for l in rbody if l.strip() and not HEADING.match(l)):
            for s in sentences(p):
                if not INITIATIVE.search(s) or MARKER_CONFIRMED.search(s) or MARKER_COLLECTED.search(s):
                    continue
                for project, secs in marked_projects.items():
                    if project.lower() in s.lower():
                        fail("rntp-contradiction", sec, f"`{excerpt(s)}` states as fact what story {secs[0]} marks, add the marker or narrow the claim")


def main(argv):
    show_counts = "--counts" in argv
    args = [a for a in argv[1:] if a != "--counts"]
    impact_path = dates_path = None
    paths = []
    i = 0
    while i < len(args):
        if args[i] == "--impact-data" and i + 1 < len(args):
            impact_path, i = args[i + 1], i + 2
        elif args[i] == "--dates" and i + 1 < len(args):
            dates_path, i = args[i + 1], i + 2
        else:
            paths.append(args[i])
            i += 1
    if not paths or paths[0] in ("-h", "--help"):
        print(__doc__)
        print("usage: promo-lint.py [--counts] [--impact-data <impact-data.md>] [--dates <url,date csv>] <draft.md>...\n"
              "  --counts       also prints words per story and section, links per story and marker counts, for a before/after comparison of a shortening\n"
              "  --impact-data  the impact-data stage document (one table row per figure, status in the last cell), turns on marker-propagation\n"
              "  --dates        `url,date` rows (MM/DD/YYYY or YYYY-MM-DD, the SHIPPED date) for the linked artifacts, read by ordering-stamped and dates-printed-match-csv")
        return 2
    impact = impact_rows(impact_path) if impact_path else None
    held = held_rows(impact_path) if impact_path else None
    dates = read_dates(dates_path) if dates_path else None
    rc = 0
    for path in paths:
        with open(path, encoding="utf-8") as fh:
            out, warnings, counts, shape = lint(fh.read(), impact, dates, held)
        with open(path, encoding="utf-8") as fh:
            draft_text = fh.read()
        rd = readiness_path(path)
        out_r = lint_readiness(rd, draft_text)
        out += out_r
        if not out_r and rd and NOT_READY_BANNER.search(draft_text):
            warnings.append("warning readiness-first: verdict is Not ready, document declares readiness mode draft_with_readiness with its banner, not for submission")
        prefix = f"{path}: " if len(paths) > 1 else ""
        if shape != "template":
            print(f"{prefix}shape: {shape}")
        if show_counts:
            for line in counts:
                print(prefix + line)
        for line in out + warnings:
            print(prefix + line)
        if out:
            rc = 1
        print(f"{prefix}promo-lint: {len(out)} failure(s), {len(warnings)} warning(s)")
    # the stage documents not given, one line each, after the verdict so `shape:` stays the first line
    if impact is None:
        print("marker-propagation skipped: no --impact-data <path>, figures are not checked against the impact-data markers")
    if dates is None:
        print("ordering-stamped read dates from the sentences only, dates-printed-match-csv skipped: no --dates <path>")
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv))
