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
    > (TO BE COLLECTED: quote from <role>)
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
Not ready`. A missing table or a `Not ready` verdict fails `readiness-first`.

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
QUOTE_LINE = re.compile(r'^> (".+", [A-Z][^,]+, [^,]+|\(TO BE COLLECTED: quote from [^()]+\))\s*$')
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
RELATIVE = re.compile(r"\b\d[\d.,]*\s?(%|percent|x\b|times\b|-fold\b)|\b\d[\d.,]*\s?(percentage points?)\b", re.I)
ABSOLUTE_PAIR = re.compile(r"\b\d[\d,.]*( [a-zA-Z/]+){0,3} to \d[\d,.]*\b")
ISO_DATE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")

MARKER_COLLECTED = re.compile(r"\(TO BE COLLECTED(: [^()]+)?\)")
MARKER_CONFIRMED = re.compile(r"\(TO BE CONFIRMED\)")
MARKER_ANY = re.compile(r"(?i)[\[(]?\s*(to be collected|to be confirmed|tbd|tbc|todo|unverified|to capture)\b[^)\]\n]*[\])]?")

# round 3b (D31 to D40)
SOURCES_LINE = re.compile(r"^Sources( used)?:", re.I)
PROCESS_LEAK = re.compile(r"earlier draft|evidence pull|reviewer of the|readiness row|in the order [a-z]+, then|told once below|working copy", re.I)
JOURNEY_VERB = re.compile(r"ruled out|instead of|rather than|tried|rejected|aligned|asked|brought .* to|\(TO BE COLLECTED: what (she|he|they) tried", re.I)
JOURNEY_NOUN = re.compile(r"\b(builder|reviewer|team|customer|owner|manager|partner)s?\b", re.I)
INITIATIVE = re.compile(r"without a ticket|on her own|on his own|unprompted|initiative", re.I)
REVIEW_ID = re.compile(r"\bCR-(\d+)\b|\bPR #(\d+)|/pull/(\d+)\b|/reviews?/(\d+)\b", re.I)
JARGON = re.compile(r"\b(leverage|play|strategic|proactive|cultivat\w*|drive alignment|synerg\w*|holistic|paradigm)\b", re.I)
ROLE_WORD = re.compile(r"\b(senior builder|product manager|principal engineer|bar[- ]raiser)\b", re.I)   # D41
UNVERIFIED_HOSTS = ["docs.google.com"]
SUPPORTED_TAG = re.compile(r"\(SUPPORTED\)")
SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"\u201c])")

# round 4 shape (D56 to D70)
CANDIDATE_SUBJECT_SHARE = 0.6   # candidate-subject-share warns under this share of action sentences (settled on the fixtures, D64)
MONTHS = re.compile(r"\b\d+ months?\b", re.I)
REVIEW_COUNT = re.compile(r"\b(authored|reviewed|wrote|landed|merged) \d[\d,]*( code)? reviews?\b|\b\d[\d,]* (code )?reviews?\b", re.I)
STORY_LEAD = re.compile(r"^\*\*Q[1-4] \d{4}, ([^*:]+):\*\*")
BRACKETED_CRITERION = re.compile(r"\*\*\s*\(([A-Za-z][A-Za-z ]+)\)")
BULLET = re.compile(r"^\s*([-*+]|\d+[.)])\s+")
ALTITUDE_FORM = re.compile(r"^A strong [A-Z][\w ]* would have\b")           # D24 counterfactual, exempt from no-trait-words
ABSENCE = re.compile(r"\b(no|never|nobody|no one|nothing|none|not exist(ed)?|could not|couldn't|had no|without|undefined|unowned|missing|lacked|exposed no|did not|had not|unmapped)\b", re.I)
ACTION_VERB = re.compile(r"\b(cut|fell|dropped|rose|reached|shipped|launched|deleted|migrated|closed|reduced|raised|grew|took|went|parsed|passed|adopted|run|runs|ran|infer|inferred|supported|stayed|copied|moved|built|wrote|fixed|removed|finished|landed|returned|served|handled|added|saved|replaced|held|uses|used|extends|extended|merged|delivered|freed|stopped|opened|came|left|put|kept|read|sent|made|got|gone|are|is|were|was)\b|\b[a-z]{3,}ed\b", re.I)
REUSE = re.compile(r"\b(now (uses?|runs?|run every|extends?|plans? from|reads?|ships?|follows?)|adopted|reused|copied|extend(s|ed)?|baseline|reference|plans? from|run(s)? every|standard|took over|picked up|carries|uses it|use it|rely on|relies on|built on|now points?|pattern to copy|copied)\b", re.I)
NO_REUSE = "No reuse by others is on record."
PRONOUNS = ("she", "he", "they")


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


def lint_readiness(path):
    if path is None:
        return ["readiness-first document: no readiness table beside the draft (<stem>.readiness.md or gap-analysis.md) with a `Readiness: Ready | Ready with gaps | Not ready` verdict"]
    with open(path, encoding="utf-8") as fh:
        t = fh.read()
    m = READINESS.search(t)
    if not m:
        return [f"readiness-first {path}: no `Readiness: Ready | Ready with gaps | Not ready` verdict line"]
    if not re.search(r"^\| *Criterion *\| *Evidence *\| *(Met / Partly / Not met|Status) *\| *Gap *\|", t, re.M):
        return [f"readiness-first {path}: no table with columns Criterion, Evidence, Met / Partly / Not met, Gap"]
    if m.group(1) == "Not ready":
        return [f"readiness-first {path}: verdict is Not ready, the writer returns the table and gap list instead of a document"]
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


def lint(text):
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
        collected += len(MARKER_COLLECTED.findall(l))
        confirmed += len(MARKER_CONFIRMED.findall(l))
        if not in_feedback:                       # providers tag principles in square brackets, verbatim (D70)
            for m in MARKER_ANY.finditer(l):
                tok = m.group(0)
                if MARKER_COLLECTED.fullmatch(tok) or MARKER_CONFIRMED.fullmatch(tok):
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
            pronoun = candidate_pronoun([p for _, _, sb in parsed for p in paragraphs(sb)])
            marked_projects = lint_stories(parsed, fail, length_fails, warnings, counts, trait_check, name, pronoun)

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
            marked_projects = lint_stories(fallback, fail, length_fails, warnings, counts, trait_check, name, pronoun)
    if marked_projects and reasons:
        lint_rntp_contradiction(reasons, marked_projects, fail)

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


def lint_stories(stories, fail, length_fails, warnings, counts, trait_check=lambda sec, s: None, name=None, pronoun="she"):
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
        quotes = [l for l in sbody if l.startswith(">")]
        if len(quotes) != 1:
            fail("quote-per-story", sec, f"{len(quotes)} quote lines, need exactly 1")
        elif not QUOTE_LINE.match(quotes[0]):
            fail("quote-form", sec, f"`{excerpt(quotes[0])}` is not `> \"...\", <Name>, <role>` or `> (TO BE COLLECTED: quote from <role>)`")
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
            # reuse-named (D67, warning): the last result sentence names a user or is the no-reuse sentence
            last = MARKER_CONFIRMED.sub("", rsents[-1]).strip() if rsents else ""
            if last and last != NO_REUSE and not (REUSE.search(last) and re.search(r"\b[A-Z][a-z]+\b|\bteams?\b", last[1:])):
                warnings.append(f"warning reuse-named {sec}: result paragraph does not end on who uses the work now (a named team or builder) or on `{NO_REUSE}` (D67): `{excerpt(last)}`")
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
    paths = [a for a in argv[1:] if a != "--counts"]
    if not paths or paths[0] in ("-h", "--help"):
        print(__doc__)
        print("usage: promo-lint.py [--counts] <draft.md>...   --counts also prints words per story and section, links per story and marker counts, for a before/after comparison of a shortening")
        return 2
    rc = 0
    for path in paths:
        with open(path, encoding="utf-8") as fh:
            out, warnings, counts, shape = lint(fh.read())
        out += lint_readiness(readiness_path(path))
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
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv))
