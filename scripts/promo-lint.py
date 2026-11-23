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
    ## Why now?                             under 550 words, three bold wins each with a number
    ## Evidence
    ### <Project>: <Criterion>              one story, criterion from the rubric
    **Headline** <outcome, number, baseline>   bold lead-in, first line under the H3
    <four prose paragraphs>                 situation, task, action, result in that order, no labels
                                            (D28: STAR is the writer's skeleton, never words the
                                            reader sees). The task paragraph ends `Ownership: ...`
    > "...", <Name>, <role>                 one blockquote line, or
    > (TO BE COLLECTED: quote from <role>)
    ## Best reasons not to promote
    ### <plain words>
    **Pattern** ... **Gap** ... **Also seen by** ... **Does not block** ... **Next** ...
    ## Feedback Summary
    Sources: used ...; unavailable ...      last line of the document

Skips: `no-semicolons` and `no-em-dash` do not fire under `## Feedback`, whose provider text is
verbatim by rule (finding R2). `bare-identifier` skips a leading YAML frontmatter block between two
`---` lines (finding R3). Every other rule still reads those lines.

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
COMPARATOR = re.compile(r"\b(from \S+( \S+){0,3} to \S+|down from|up from|vs\.?|versus|against|ahead of|early|earlier|instead of|fewer|more than|less than|before|cut from|to 0)\b", re.I)

MARKER_COLLECTED = re.compile(r"\(TO BE COLLECTED(: [^()]+)?\)")
MARKER_CONFIRMED = re.compile(r"\(TO BE CONFIRMED\)")
MARKER_ANY = re.compile(r"(?i)[\[(]?\s*(to be collected|to be confirmed|tbd|tbc|todo|unverified|to capture)\b[^)\]\n]*[\])]?")


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


def lint(text):
    lines = text.splitlines()
    length_fails, fails, warnings, counts = [], [], [], []
    shape = "template"

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
        m = HEADING.match(l)
        if m and len(m.group(1)) == 2:
            section = m.group(2)
        in_feedback = section == "Feedback"       # provider text is verbatim by rule (R2), house rules skip it
        in_frontmatter = i <= frontmatter_end     # a leading YAML block is metadata, not prose (R3)
        if ";" in l and not l.startswith("Sources:") and not in_feedback:
            fail("no-semicolons", f"line {i}", f"`{excerpt(l)}`")
        if "\u2014" in l and not in_feedback:
            fail("no-em-dash", f"line {i}", f"`{excerpt(l)}`")
        collected += len(MARKER_COLLECTED.findall(l))
        confirmed += len(MARKER_CONFIRMED.findall(l))
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
        for m in BARE_URL.finditer(l):
            fail("bare-identifier", f"line {i}", f"bare URL `{excerpt(m.group(0), 40)}`, link it on the artifact's identifier")
        if not l.startswith("#"):
            stripped = LINK.sub("", l)
            for m in BARE_ID.finditer(stripped):
                fail("bare-identifier", f"line {i}", f"`{m.group(0)}` is named but not linked")
    counts.append(f"markers (TO BE COLLECTED): {collected}, (TO BE CONFIRMED): {confirmed}")

    for title, body in split_sections(lines, 2):
        if title == "Why now?":
            n = words(body)
            counts.append(f"words Why now: {n} (cap {CAP_WHY_NOW})")
            if n >= CAP_WHY_NOW:
                length_fails.append((n - CAP_WHY_NOW, f"why-now-length Why now: {n} words, cap {CAP_WHY_NOW}"))
            wins = [b for b in BOLD.findall("\n".join(body)) if re.search(r"\d", b)]
            if len(wins) < 3:
                fail("why-now-wins", "Why now", f"{len(wins)} bold wins with a number, need 3")

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
            lint_stories(parsed, fail, length_fails, warnings, counts)

        if title == "Best reasons not to promote":
            reasons = split_sections(body, 3)
            if not reasons:
                fail("rntp-leadins", "Best reasons not to promote", "no `### <reason>` headings")
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
            lint_stories(fallback, fail, length_fails, warnings, counts)

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


def lint_stories(stories, fail, length_fails, warnings, counts):
    """Per-story rules over (project, criterion, body) triples, from the template shape or the
    fallback splitter. The body's first non-empty line is the Headline slot."""
    by_criterion, tellings = {}, {}
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
        paras = paragraphs(sbody)
        if len(paras) < STORY_PARAGRAPHS:
            fail("story-paragraphs", sec, f"{len(paras)} prose paragraphs between the Headline and the quote, need {STORY_PARAGRAPHS} (situation, task, action, result, no labels)")
        if len(paras) >= 2 and not re.search(r"Ownership: [^.]+\.?\s*$", paras[1]):
            fail("ownership-line", sec, f"task paragraph (second) does not end with `Ownership: originated ..., executed ..., operated ...`: `{excerpt(paras[1])}`")
        for p in paras[:STORY_PARAGRAPHS]:
            m = LEADIN.match(p)
            if m and m.group(1).strip() in ("Situation", "Task", "Action", "Result"):
                fail("no-star-labels", sec, f"`**{m.group(1).strip()}**` is a label the reader sees, STAR is the writer's skeleton only (D28)")
        quotes = [l for l in sbody if l.startswith(">")]
        if len(quotes) != 1:
            fail("quote-per-story", sec, f"{len(quotes)} quote lines, need exactly 1")
        elif not QUOTE_LINE.match(quotes[0]):
            fail("quote-form", sec, f"`{excerpt(quotes[0])}` is not `> \"...\", <Name>, <role>` or `> (TO BE COLLECTED: quote from <role>)`")
        links = len(LINK.findall("\n".join(sbody)))
        counts.append(f"links {sec}: {links}")
        if links == 0:
            fail("story-links", sec, "0 links, every named artifact is a hyperlink on its identifier")
    for crit, ns in by_criterion.items():
        total = sum(ns)
        counts.append(f"words section {crit}: {total} over {len(ns)} stories (warn above {MAX_STORIES} stories or {CAP_SECTION} words)")
        if len(ns) > MAX_STORIES or total > CAP_SECTION:
            warnings.append(f"warning section-length {crit}: {len(ns)} stories, {total} words (target at most {MAX_STORIES} stories and {CAP_SECTION} words), move the weakest story to one sentence or an appendix")
    for project, ts in tellings.items():
        full = [c for c, n in ts if n > FULL_TELLING]
        if len(full) > 1:
            fail("one-story-once", project, f"told in full ({FULL_TELLING}+ words) under {len(full)} headings: {', '.join(full)}")


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
