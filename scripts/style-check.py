#!/usr/bin/env python3
"""Countable writing-style checks on a draft: the rules a regex can count, run by every writer's gate pass.

The engine owns the mechanism, the instance owns every specific: the word list, the sentence limit, the
glossary files and the allowed acronyms live in a rules JSON the instance points at through
<instance>/gate-policy.json {"required_style_rules": "${instance}/path/rules.json"} or a workflow's
gate.style_rules. `vstack check-run` runs this on draft.md and marks the run contract_unmet on any finding,
`vstack style-check` runs it on demand, and the rendered GATE section tells the writer to run it before the
contract check.

  python3 style-check.py draft.md --rules rules.json [--glossary file ...] [--json]
  python3 style-check.py --selftest

Rules JSON keys (all optional, a missing key turns that check off):
  max_words_per_sentence   int, a sentence over it is a finding (prose only: tables, headings, code and link
                           labels are not counted, a link label counts as one word). A bullet or numbered list
                           item is its own sentence even without a terminal period, items are never joined
  weasel_words             list of words or phrases, each occurrence outside tables headers, quoted speech,
                           code and title-like link labels is a finding
  acronyms                 {"min": 2, "max": 6, "allow": [...], "glossary_headings": ["Glossary", "References"]}:
                           a run of capitals of that length whose first use is neither followed by " (" nor
                           inside round brackets, and which no glossary file and no section of the doc under one
                           of the glossary headings names, is a finding. A link label (it quotes a title), a
                           double-quoted span and a table cell that is wholly a title (a link or bold text) are
                           not read: an acronym there is someone else's wording. `glossary_heading` (one string)
                           is still accepted
  date_without_year        true: MM/DD with no /YYYY outside URLs, code and title-like link labels
  iso_dates                true: YYYY-MM-DD outside URLs and code
  url_as_label             true: a markdown link whose label is the URL itself
  semicolons               true: a semicolon outside table rows, code, title-like link labels, HTML entities,
                           the fixed heading TL;DR and lines whose prefix is in exempt_line_prefixes
  em_dashes                true: an em-dash (U+2014) outside code, outside every link label and outside a
                           table cell that is wholly a title (a link or bold text, a verbatim task title)
  hedge_words              list of words or phrases that stand in for an unproven-claim marker ("likely", "may be"):
                           each occurrence outside a marker, quoted speech, code, link labels (a label quotes a title)
                           and verbatim-title table cells is a finding. The claim carries the marker instead
  marker_exact             list of marker texts ("TO BE CONFIRMED"): a bracketed marker that carries any other text
                           inside its brackets, `(TO BE CONFIRMED which date)`, is a finding. The reason goes in the
                           sentence, the marker stays one exact form a reader and a regex both recognise
  comparatives             list of comparative words ("faster", "fewer", "more"): one in a prose sentence or a prose
                           table cell that holds no digit is a finding (link labels, quoted speech and title cells
                           are not read). A comparison carries its number
  numeric_span_needs_relative  true or {"relative": [regex, ...]}: a `from <number> to <number>` span (not a date
                           or a clock range) whose sentence carries no relative change before it is a finding. The
                           relative change comes first, the absolutes follow in brackets: `cut 50% (from 14 to 7)`.
                           Default relative patterns: a percentage (`\d%`) and a multiplier (`\dx`)
  marker_not_after         list of words ("is", "are", "remains"): a bracketed marker_exact marker whose preceding word is
                           one of them (`every delta is (TO BE CONFIRMED)`) is a finding, the marker is a tag after a
                           statement, never its verb. The same rule also counts a marker_exact text that stands outside
                           brackets (`every delta is TO BE CONFIRMED.`, `(organiser x, TO BE CONFIRMED still recurring)`)
  unclosed_brackets        true: a table cell with more `[` than `]` or more `(` than `)` (a link label or a title cut
                           short, `Bloom Rebuild[Prod Manifest bloom aggregate has no size boun`) is a finding
  space_before_punctuation list of marks ([".", ",", ";", ":", "!", "?"]): a space between a word and one of them, in a
                           table cell or in prose (`Metadata & Storage : Kraken`), is a finding. Code, URLs and the
                           table alignment row are not read, a verbatim title is (its spacing is the writer's to normalise)
  exempt_line_prefixes     list of line prefixes no check reads (the engine's own `Sources:` header line)

A title-like link label is one that opens with `[` (a bracketed tag, the label quotes a document title), a
link wrapped in `**` or a label wrapped in `**` (a bold title). The instance decides whether a title may keep its punctuation, the
engine only refrains from counting a quote as the writer's own prose.

Output: one line per finding `<rule> -> "<quote>" (line N)`, then `style-check: N finding(s)`. Exit 1 on
any finding, 0 on none.
"""
import argparse, json, pathlib, re, sys

ROMAN = {"II", "III", "IV", "VI", "VII", "VIII", "IX", "XI", "XII", "XIII", "XIV", "XV", "XX"}
# units, time words and the engine's own tokens: never an acronym a reader needs expanded
ENGINE_ALLOW = {"MM", "DD", "YYYY", "HH", "TL", "DR", "TBD", "URL", "ID", "OK", "AM", "PM", "UTC", "KB", "MB", "GB", "TB", "PB", "MS", "NS", "US", "GMT"}


def read_rules(path):
    r = json.loads(pathlib.Path(path).read_text())
    if not isinstance(r, dict):
        raise SystemExit(f"style-check: {path} is not a JSON object")
    return r


def _title_like(label, bold):
    """A label that quotes a title verbatim: the whole link is bold, the label itself is bold, or it opens with a
    bracketed tag such as [Draft]."""
    return bold or label.startswith("[") or (label.startswith("**") and label.rstrip().endswith("**"))


def _strip_code(text):
    text = re.sub(r"```.*?```", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
    return re.sub(r"`[^`\n]*`", "`code`", text)


# a link never spans lines: a stray `[` on one line must not pair with a `](url)` lines later and swallow the prose between
LINK = re.compile(r"(\*\*)?\[((?:[^\[\]\n]|\[[^\]\n]*\])*)\]\(([^)\s]*)\)(\*\*)?")


def _links_replaced(text, keep_prose_labels=True, placeholder="link"):
    """Replace every markdown link: a title-like label becomes the placeholder, a prose label keeps its words
    (or also becomes the placeholder when keep_prose_labels is False). The URL is always dropped."""
    def one(m):
        bold = bool(m.group(1) or m.group(4))
        label = m.group(2)
        if _title_like(label, bold) or not keep_prose_labels:
            return placeholder
        return label
    return LINK.sub(one, text)


def _lines(text):
    return text.split("\n")


def _is_table_row(line):
    return line.lstrip().startswith("|")


def _is_table_header(lines, i):
    if not _is_table_row(lines[i]):
        return False
    nxt = lines[i + 1] if i + 1 < len(lines) else ""
    return bool(re.match(r"^\s*\|?\s*:?-{3,}", nxt))


def _title_cells_blanked(line, placeholder="title"):
    """In a table row, a cell that is wholly one link (bold or not), wholly bold text, or opens with a bracketed tag
    quotes a title verbatim (a task, a tracker row, a ticket, a document): replace it with the placeholder so no
    count reads it. Other cells stay."""
    if not _is_table_row(line):
        return line
    cells = re.split(r"(?<!\\)\|", line)
    out = []
    for c in cells:
        t = c.strip()
        # wholly a link, wholly bold, or opening with a bracketed tag such as [ALARM] or [Draft]: a title copied verbatim
        if t and (re.fullmatch(r"(\*\*)?\[(?:[^\[\]\n]|\[[^\]\n]*\])*\]\([^)\s]*\)(\*\*)?", t) or re.fullmatch(r"\*\*[^*\n]+\*\*", t) or re.match(r"\[[A-Za-z][^\]\n]{0,30}\]", t)):
            out.append(f" {placeholder} ")
        else:
            out.append(c)
    return "|".join(out)


def _exempt(line, prefixes):
    s = line.lstrip()
    return any(s.startswith(p) for p in prefixes)


# an unproven-claim marker in brackets, any marker word: (TO BE CONFIRMED), [TO BE COLLECTED: text]
MARKER = re.compile(r"\(TO BE [A-Z]+\b[^)]*\)|\[TO BE [A-Z]+[^\]]*\]")
QUOTED = re.compile(r"\"[^\"\n]*\"|\u201c[^\u201d\n]*\u201d")
SENTENCE_END = re.compile(r"(?<=[.!?])\s+(?=[\"'(\[*A-Z0-9])")
LIST_ITEM = re.compile(r"^\s*([-*+]|\d+[.)])\s+")


def _prose_units(lines, prefixes):
    """Yield (text, lineno) for every unit a per-sentence rule reads: each prose sentence (paragraphs joined, list items
    their own sentence, every link collapsed to one word, a label quotes a title) and each prose table cell (header
    rows and verbatim-title cells skipped). Quoted speech is blanked, it is someone else's wording."""
    def clean(t):
        t = _links_replaced(t, keep_prose_labels=False, placeholder="Link")
        return QUOTED.sub("QUOTE", t)
    para, start = [], None
    def flush():
        if para:
            for s in SENTENCE_END.split(clean(" ".join(para))):
                if s.strip():
                    yield s, start
    for i, l in enumerate(lines):
        bare = l.strip()
        if _is_table_row(l):
            yield from flush(); para, start = [], None
            if _is_table_header(lines, i) or re.match(r"^\s*\|?\s*:?-{3,}", l):
                continue
            for c in re.split(r"(?<!\\)\|", _title_cells_blanked(l)):
                c = c.strip()
                if c and c != "title":
                    for s in SENTENCE_END.split(clean(c)):
                        if s.strip():
                            yield s, i + 1
            continue
        if not bare or bare.startswith("#") or _exempt(l, prefixes) or bare.startswith("<!--"):
            yield from flush(); para, start = [], None
            continue
        if LIST_ITEM.match(l):
            yield from flush(); para, start = [], None
            bare = LIST_ITEM.sub("", bare)
        if start is None:
            start = i + 1
        para.append(bare)
    yield from flush()


def check(text, rules, glossary_texts=()):
    findings = []
    prefixes = list(rules.get("exempt_line_prefixes", []))
    raw_lines = _lines(text)
    code_free = _strip_code(text)
    lines = _lines(code_free)
    assert len(lines) == len(raw_lines), "code stripping changed the line count"

    def add(rule, quote, lineno):
        findings.append((rule, quote.strip()[:90], lineno))

    # sentences: prose lines only, links collapsed to one word, paragraph by paragraph
    limit = rules.get("max_words_per_sentence")
    if limit:
        para, start = [], None
        def flush():
            if not para:
                return
            blob = " ".join(para)
            # a link is one word, and the placeholder opens with a capital so a sentence that ends right before a
            # link-led sentence still splits there
            blob = _links_replaced(blob, keep_prose_labels=False, placeholder="Link")
            for s in re.split(r"(?<=[.!?])\s+(?=[\"'(\[*A-Z0-9])", blob):
                n = len(s.split())
                if n > int(limit):
                    add("sentence-length", f"{n} words: {s[:70]}", start)
        LIST_ITEM = re.compile(r"^\s*([-*+]|\d+[.)])\s+")
        for i, l in enumerate(lines):
            bare = l.strip()
            if not bare or _is_table_row(l) or bare.startswith("#") or _exempt(l, prefixes) or bare.startswith("<!--"):
                flush(); para, start = [], None
                continue
            if LIST_ITEM.match(l):
                # a list item is its own sentence even without a terminal period: close whatever came before and
                # never join it with the next item (a list of link-led bullets is not one 90-word sentence)
                flush(); para, start = [], None
                bare = LIST_ITEM.sub("", bare)
            if start is None:
                start = i + 1
            para.append(bare)
        flush()

    # weasel words: everywhere but table headers, quoted speech, title-like labels, code, exempt lines
    weasel = [w for w in rules.get("weasel_words", []) if w.strip()]
    if weasel:
        pat = re.compile(r"(?<![\w-])(" + "|".join(re.escape(w) for w in weasel) + r")(?![\w-])", re.I)
        for i, l in enumerate(lines):
            if _exempt(l, prefixes) or _is_table_header(lines, i) or re.match(r"^\s*\|?\s*:?-{3,}", l):
                continue
            t = _links_replaced(_title_cells_blanked(l))
            t = re.sub(r"\"[^\"\n]*\"|“[^”\n]*”", "QUOTE", t)
            for m in pat.finditer(t):
                if re.search(r"\bhow\s*$", t[:m.start()], re.I):
                    continue  # "how many", "how much": a question, not a hedge
                if re.search(r"\bat\s*$", t[:m.start()], re.I) and re.match(r"\s+(\d|one\b|two\b|three\b|four\b|five\b|six\b|seven\b|eight\b|nine\b|ten\b)", t[m.end():], re.I):
                    continue  # "at most 100", "at most one", "at least 3": a bound with its number, not a hedge
                add("weasel-word", f"{m.group(1)}: {t[max(0, m.start() - 30):m.end() + 30]}", i + 1)

    # acronyms: first use expanded, or named by a glossary
    ac = rules.get("acronyms")
    if ac:
        lo, hi = int(ac.get("min", 2)), int(ac.get("max", 6))
        allow = set(ac.get("allow", [])) | ENGINE_ALLOW | ROMAN
        gl_text = "\n".join(glossary_texts)
        headings = ac.get("glossary_headings") or [ac.get("glossary_heading", "Glossary"), "References"]
        for heading in headings:
            # every section of the document under that heading, at any level, counts as the document's own glossary
            for own in re.finditer(r"^(#{1,6})\s+" + re.escape(heading) + r"\b.*?(?=^#{1,6}\s|\Z)", code_free, re.M | re.S):
                gl_text += "\n" + own.group(0)
        known = set(re.findall(r"(?<![A-Za-z0-9])([A-Z]{2}[A-Z0-9]{0,8})s?(?![A-Za-z0-9])", gl_text))
        tok = re.compile(r"(?<![A-Za-z0-9/&-])([A-Z]{%d}[A-Z0-9]{0,%d})s?(?![A-Za-z0-9/-])" % (lo, max(0, hi - lo)))
        seen = set()
        for i, l in enumerate(lines):
            if _exempt(l, prefixes) or l.strip().startswith("<!--") or l.lstrip().startswith("#"):
                continue  # a heading is a label, the first use in prose is the one that must expand
            # a link label quotes a title (a task, a tracker row, a doc), a double-quoted span is someone else's words,
            # a table cell that is wholly a title likewise: an acronym there is not the writer's to expand
            t = _title_cells_blanked(l)
            t = _links_replaced(t, keep_prose_labels=False)
            t = re.sub(r"\"[^\"\n]*\"|\u201c[^\u201d\n]*\u201d", "quote", t)
            t = t.replace("TL;DR", "tldr")
            t = re.sub(r"\(TO BE [A-Z]+\b[^)]*\)|\[TO BE [A-Z]+[^\]]*\]", "marker", t)
            for m in tok.finditer(t):
                a = m.group(1)
                # letters then digits (SEV2, a session code, a region number) is an identifier, not an acronym
                if len(a) < lo or len(a) > hi or a in allow or a in known or a in seen or re.search(r"\d", a):
                    continue
                seen.add(a)
                before = t[:m.start()].rstrip()
                after = t[m.end():]
                # inside an open bracket on this line: "(the plain phrase, TERM)" and "(TERM)" both count as expanded
                in_brackets = before.count("(") > before.count(")")
                expands = re.match(r"\s*\(", after) is not None
                if not (in_brackets or expands):
                    add("acronym-unexpanded", f"{a}: {t[max(0, m.start() - 30):m.end() + 30]}", i + 1)

    # dates
    if rules.get("date_without_year"):
        for i, l in enumerate(lines):
            if _exempt(l, prefixes):
                continue
            t = _links_replaced(l)
            t = re.sub(r"https?://\S+", "URL", t)
            for m in re.finditer(r"(?<![\d/])(\d{1,2})/(\d{1,2})(?![\d/])", t):
                mo, d = int(m.group(1)), int(m.group(2))
                if 1 <= mo <= 12 and 1 <= d <= 31:
                    add("date-without-year", f"{m.group(0)}: {t[max(0, m.start() - 30):m.end() + 20]}", i + 1)
    if rules.get("iso_dates"):
        for i, l in enumerate(lines):
            if _exempt(l, prefixes):
                continue
            t = _links_replaced(l)
            t = re.sub(r"https?://\S+", "URL", t)
            for m in re.finditer(r"(?<![\w/])(\d{4}-\d{2}-\d{2})(?![\w/])", t):
                add("iso-date", f"{m.group(0)}: {t[max(0, m.start() - 30):m.end() + 20]}", i + 1)

    # links whose label is the URL
    if rules.get("url_as_label"):
        for i, l in enumerate(lines):
            for m in re.finditer(r"\[\s*https?://[^\]]*\]\(", l):
                add("url-as-label", m.group(0), i + 1)

    # semicolons and em-dashes
    if rules.get("semicolons"):
        for i, l in enumerate(lines):
            if _exempt(l, prefixes) or _is_table_row(l):
                continue
            t = _links_replaced(l)
            t = t.replace("TL;DR", "TLDR").replace("&amp;", "").replace("&lt;", "").replace("&gt;", "").replace("&nbsp;", "")
            t = re.sub(r"&\w+;", "", t)
            for m in re.finditer(";", t):
                add("semicolon", t[max(0, m.start() - 40):m.end() + 20], i + 1)
    if rules.get("em_dashes"):
        for i, l in enumerate(lines):
            if _exempt(l, prefixes):
                continue
            # a verbatim title keeps its own punctuation: every link label, and a table cell that is wholly a title
            t = _links_replaced(_title_cells_blanked(l), keep_prose_labels=False)
            for m in re.finditer("\u2014", t):
                add("em-dash", t[max(0, m.start() - 40):m.end() + 20], i + 1)

    def word_pattern(words):
        return re.compile(r"(?<![\w-])(" + "|".join(re.escape(w) for w in words) + r")(?![\w-])", re.I)

    # hedge words: a guess written as a word ("likely leave") where the claim should carry the marker
    hedges = [w for w in rules.get("hedge_words", []) if w.strip()]
    if hedges:
        pat = word_pattern(hedges)
        for i, l in enumerate(lines):
            if _exempt(l, prefixes) or _is_table_header(lines, i) or re.match(r"^\s*\|?\s*:?-{3,}", l) or l.strip().startswith("<!--"):
                continue
            t = _links_replaced(_title_cells_blanked(l), keep_prose_labels=False)
            t = QUOTED.sub("QUOTE", t)
            t = MARKER.sub("marker", t)
            for m in pat.finditer(t):
                add("hedge-word", f"{m.group(1)}: {t[max(0, m.start() - 30):m.end() + 30]}", i + 1)

    # marker form: the marker is one exact bracketed form, a reason goes in the sentence, never inside the brackets
    for marker in rules.get("marker_exact", []) or []:
        if not str(marker).strip():
            continue
        esc = re.escape(marker.strip())
        pat = re.compile(r"\(\s*" + esc + r"\b([^)]*)\)|\[\s*" + esc + r"\b([^\]]*)\]")
        for i, l in enumerate(lines):
            if _exempt(l, prefixes) or l.strip().startswith("<!--"):
                continue
            for m in pat.finditer(l):
                inner = (m.group(1) if m.group(1) is not None else m.group(2)) or ""
                if inner.strip():
                    add("marker-not-exact", m.group(0), i + 1)

    # comparatives: a comparison in a sentence or a prose cell that holds no digit has no data behind it
    comps = [w for w in rules.get("comparatives", []) if w.strip()]
    if comps:
        pat = word_pattern(comps)
        for unit, lineno in _prose_units(lines, prefixes):
            if re.search(r"\d", unit):
                continue
            for m in pat.finditer(unit):
                add("comparative-without-number", f"{m.group(1)}: {unit[max(0, m.start() - 40):m.end() + 30]}", lineno)

    # from X to Y: the relative change leads, the absolutes follow in brackets
    span_rule = rules.get("numeric_span_needs_relative")
    if span_rule:
        rel = span_rule.get("relative") if isinstance(span_rule, dict) else None
        rel_pats = [re.compile(p, re.I) for p in (rel or [r"\d\s*%", r"\d\s*x\b"])]
        # a plain number (not a date 11/30/2026, not a clock 07:00, not an identifier 1Q), an optional unit, then "to" and a number
        SPAN = re.compile(r"\bfrom\s+(?:about\s+|around\s+|roughly\s+)?(\d[\d,]*(?:\.\d+)?)(?![\d/:A-Za-z])(?:\s*%|\s+[A-Za-z]+)?\s+to\s+(?:about\s+|around\s+|roughly\s+)?(\d[\d,]*(?:\.\d+)?)(?![\d/:])", re.I)
        for unit, lineno in _prose_units(lines, prefixes):
            for m in SPAN.finditer(unit):
                if re.fullmatch(r"(19|20)\d\d", m.group(1)) and re.fullmatch(r"(19|20)\d\d", m.group(2)):
                    continue  # from 2026 to 2027 is a period, not a change
                before = unit[:m.start()]
                if not any(p.search(before) for p in rel_pats):
                    add("span-without-relative", f"{m.group(0)}: {unit[max(0, m.start() - 40):m.end() + 20]}", lineno)
    # marker as a predicate: the marker is a tag after a statement ("every delta was not fetched (TO BE CONFIRMED)"),
    # never the verb ("every delta is TO BE CONFIRMED", "is (TO BE CONFIRMED)") and never bare outside its brackets
    not_after = [w for w in rules.get("marker_not_after", []) or [] if str(w).strip()]
    markers = [str(m).strip() for m in rules.get("marker_exact", []) or [] if str(m).strip()]
    if markers and not_after:
        after_pat = re.compile(r"(?<![\w-])(" + "|".join(re.escape(w) for w in not_after) + r")\s*[(\[]\s*(" + "|".join(re.escape(m) for m in markers) + r")\b", re.I)
        bare_pat = re.compile(r"\b(" + "|".join(re.escape(m) for m in markers) + r")\b")
        for i, l in enumerate(lines):
            if _exempt(l, prefixes) or l.strip().startswith("<!--"):
                continue
            t = _links_replaced(_title_cells_blanked(l), keep_prose_labels=False)
            t = QUOTED.sub("QUOTE", t)
            for m in after_pat.finditer(t):
                add("marker-as-predicate", f"{m.group(1)}: {t[max(0, m.start() - 30):m.end() + 12]}", i + 1)
            for m in bare_pat.finditer(t):
                if re.search(r"[(\[]\s*$", t[:m.start()]) and re.match(r"[^)\]\n]*[)\]]", t[m.end():]):
                    continue  # inside its own brackets, marker-not-exact judges what else is in there
                add("marker-as-predicate", f"bare: {t[max(0, m.start() - 30):m.end() + 20]}", i + 1)

    # unclosed brackets in a table cell: a link label or a title cut short reads as garbled text
    if rules.get("unclosed_brackets"):
        for i, l in enumerate(lines):
            if not _is_table_row(l) or _exempt(l, prefixes) or re.match(r"^\s*\|?\s*:?-{3,}", l):
                continue
            for c in re.split(r"(?<!\\)\|", l):
                c = c.strip()
                if not c:
                    continue
                if c.count("[") > c.count("]") or c.count("(") > c.count(")"):
                    add("unclosed-bracket", c, i + 1)

    # a space before punctuation: "Storage : Kraken", "landed , on"
    marks = [str(m) for m in rules.get("space_before_punctuation", []) or [] if str(m)]
    if marks:
        sp = re.compile(r"[^\s|]([ \t]+)[" + re.escape("".join(marks)) + r"](?=[\s|]|$)")
        for i, l in enumerate(lines):
            if _exempt(l, prefixes) or l.strip().startswith("<!--") or re.match(r"^\s*\|?\s*:?-{3,}", l):
                continue
            t = LINK.sub(lambda m: (m.group(1) or "") + "[" + m.group(2) + "](URL)" + (m.group(4) or ""), l)
            t = QUOTED.sub("QUOTE", re.sub(r"https?://\S+", "URL", t))
            for m in sp.finditer(t):
                add("space-before-punctuation", t[max(0, m.start() - 30):m.end() + 10], i + 1)
    return findings


def run(draft, rules, glossary_paths=()):
    text = pathlib.Path(draft).read_text()
    gl = []
    for g in glossary_paths:
        p = pathlib.Path(g).expanduser()
        if p.exists():
            gl.append(p.read_text())
    return check(text, rules, gl)


def selftest():
    rules = {"max_words_per_sentence": 12, "weasel_words": ["several", "significant", "a number of"],
             "acronyms": {"min": 2, "max": 6, "allow": ["CR"], "glossary_heading": "Glossary"},
             "date_without_year": True, "iso_dates": True, "url_as_label": True, "semicolons": True, "em_dashes": True,
             "hedge_words": ["likely", "may be", "seems"], "marker_exact": ["TO BE CONFIRMED"],
             "comparatives": ["faster", "fewer", "more"], "numeric_span_needs_relative": True,
             "marker_not_after": ["is", "are", "remains"], "unclosed_brackets": True,
             "space_before_punctuation": [".", ",", ";", ":", "!", "?"],
             "exempt_line_prefixes": ["Sources:"]}
    bad = "\n".join([
        "# Title", "Sources: used a.b; unavailable c.d", "",
        "This sentence has far too many words for the twelve word limit set in the rules above.",
        "Several teams saw a significant change on 11/23 and the long date 2026-11-27 stayed.",
        "The PMDB alarm fired, see [https://example.com/x](https://example.com/x) and the review ended; it closed.",
        "An em-dash — here. The ZAZ (zero allocation zone) is fine, and QQQ is in the glossary.",
        "| col | 11/23 | a; b |", "|---|---|---|", "| [[Draft] Title (11/06-11/13)](https://e.com) | **[Task — title](https://e.com)** | [**[Tag] Task — 11/13 title**](https://e.com) |",
        "", "## Glossary", "| Term | Means |", "|---|---|", "| QQQ | a glossary term |",
        "", "A stray [bracket opens here and the date 10/09 must still count,", "then a link [CR-9](https://e.com/9) closes a bracket on another line.",
        "", "No activity since 11/11/2026, likely leave (roster status). Written 11/27/2026 (TO BE CONFIRMED which date).",
        "The new path is faster with fewer calls. Latency fell from 1,700 ms to 600 ms.",
        "Last week's counts were not fetched, so every delta is TO BE CONFIRMED.",
        "| 22 | Metadata & Storage : Kraken | Output below baseline on Bloom Rebuild[Prod Manifest has no size boun, planned? |",
    ])
    f = check(bad, rules)
    rules_hit = {r for r, _, _ in f}
    want = {"sentence-length", "weasel-word", "acronym-unexpanded", "date-without-year", "iso-date", "url-as-label", "semicolon", "em-dash",
            "hedge-word", "marker-not-exact", "comparative-without-number", "span-without-relative",
            "marker-as-predicate", "unclosed-bracket", "space-before-punctuation"}
    missing = want - rules_hit
    assert not missing, f"selftest: rules that did not fire on the bad text: {sorted(missing)}\n{f}"
    quotes = [q for r, q, _ in f]
    assert sum(1 for r, _, _ in f if r == "weasel-word") == 2, f"weasel count {f}"
    assert any(q.startswith("PMDB") for r, q, _ in f if r == "acronym-unexpanded"), f
    assert not any(q.startswith(("ZAZ", "QQQ", "CR", "LINK", "link")) for r, q, _ in f if r == "acronym-unexpanded"), f
    assert sum(1 for r, _, _ in f if r == "acronym-unexpanded") == 1, f
    assert sum(1 for r, _, _ in f if r == "date-without-year") == 3, f"table cell 11/23 and the date after a stray bracket count, the title-like labels do not: {f}"
    assert sum(1 for r, _, _ in f if r == "semicolon") == 1, f"only the prose semicolon counts (Sources line, table row exempt): {f}"
    assert sum(1 for r, _, _ in f if r == "em-dash") == 1, f"the em-dash in the bold title label is exempt: {f}"
    good = "\n".join([
        "# Title", "Sources: used a.b; unavailable c.d", "",
        "The deletion worker (DW) ran out of memory on 11/20/2026. The fix landed on 11/21/2026 in [CR-1](https://e.com/CR-1).",
        "Peak memory fell 65% (from 1,700 MB to 600 MB). TL;DR is a heading. Written 11/27/2026 (TO BE CONFIRMED).",
        "| When | What |", "|---|---|", "| 11/23/2026 | the PMDB alarm, see Glossary |", "", "## Glossary", "| PMDB | the metadata database |",
    ])
    g = check(good, rules)
    assert not g, f"selftest: findings on the good text: {g}"
    # the four false positives of the 11/27/2026 fix wave, each a text that must produce NO finding
    r12 = dict(rules); r12["max_words_per_sentence"] = 12
    bullets = "\n".join([
        "## References", "",
        "- [Tracker](https://e.com/t): row 6, the source of the title and goal",
        "- [Thread, #chan 11/10/2026](https://e.com/s): the audit that surfaced the dropped footer",
        "- [Message, root cause 11/12/2026](https://e.com/m): how the delete led to repeated timeouts",
        "- [Ticket](https://e.com/k): the 11/11/2026 customer stall and the patch",
        "1. First numbered item without a period",
        "2. Second numbered item, also its own sentence",
    ])
    f = [x for x in check(bullets, r12) if x[0] == "sentence-length"]
    assert not f, f"(1) link-led bullets were joined into one sentence: {f}"
    f = [x for x in check("Short one ends here. [Next link](https://e.com/n) opens the next sentence that stays under the limit.", r12) if x[0] == "sentence-length"]
    assert not f, f"(2) the link placeholder merged two sentences: {f}"
    assert [x for x in check("- " + " ".join(["word"] * 13), r12) if x[0] == "sentence-length"], "(1) a 13-word bullet must still count"
    acr = "\n".join([
        "# Doc", "",
        "See [DP: FieldStats for map-key fields (ZQX usage analysis)](https://e.com/a) and \"the QQW service said so\".",
        "| Task | Owner |", "|---|---|", "| **[Evaluate RRT eviction for the cache](https://e.com/b)** | a builder |", "| **VVB title without a link** | a builder |",
        "The KKZ term is named under References below and the JJY term under the Glossary.",
        "", "## Glossary", "| JJY | a glossary row |", "", "## References", "- KKZ: the reference list names it",
    ])
    f = [x for x in check(acr, rules) if x[0] == "acronym-unexpanded"]
    assert not f, f"(3) acronyms inside a title label, a quote, a title cell or named under Glossary or References must not count: {f}"
    assert [x for x in check("The PPQ fired.", rules) if x[0] == "acronym-unexpanded"], "(3) a bare acronym in prose must still count"
    f = [x for x in check("# The PPQ heading\n\nThe managed queue (the queue service, PPQ) then fires. A fan-out of at most 100 pieces, several of them.", rules) if x[0] in ("acronym-unexpanded", "weasel-word")]
    assert len(f) == 1 and f[0][0] == "weasel-word" and f[0][1].startswith("several"), f"(3) a heading is not the first use, a comma-expanded term in brackets is expanded, 'at most 100' is a bound, 'several' still counts: {f}"
    f = [x for x in check("| 7 | ticket | [ALARM] [region] Service-QQV-Alarm fired | open |\n|---|---|---|---|\n| 8 | x | at most one change | y |", rules) if x[0] in ("acronym-unexpanded", "weasel-word")]
    assert not f, f"a cell opening with a bracketed tag is a verbatim ticket title, 'at most one' is a bound: {f}"
    f = [x for x in check("| [(ORR) Parallelize multiple accounts](https://e.com/o) | open |\n|---|---|\n| **several things** | a cell with several words |", rules) if x[0] == "weasel-word"]
    assert len(f) == 1 and "a cell with several" in f[0][1], f"weasel words inside a verbatim title (link or bold cell) do not count, in a prose cell they do: {f}"
    em = "\n".join([
        "| Task | Status |", "|---|---|",
        "| [(Bloom) Manifest aggregate has no size bound — rebuild OOMs](https://e.com/c) | open |",
        "| **Stream 2: Benchmark metadata — real numbers** | open |",
        "Prose with [a label — dashed](https://e.com/d) inside the link.",
    ])
    f = [x for x in check(em, rules) if x[0] == "em-dash"]
    assert not f, f"(4) an em-dash inside a link label or a title cell must not count: {f}"
    f = [x for x in check("| Task | Note |\n|---|---|\n| [t](https://e.com/t) | a cell — with prose |\nProse — dashed.", rules) if x[0] == "em-dash"]
    assert len(f) == 2, f"(4) an em-dash in a prose cell or in prose must still count twice: {f}"
    # the four rules of the 11/27/2026 fix wave pass 4 (validation pass 2): a silent case and a still-fires case each
    # hedge words: inside a marker, a quote, a title label or a title cell they are not the writer's guess
    hedge_ok = "\n".join([
        "On leave per the roster status (TO BE CONFIRMED). The owner wrote \"it seems fine\" in the thread.",
        "See [Likely causes of the stall — a review](https://e.com/l) and [**May be later**](https://e.com/m).",
        "| Task | Note |", "|---|---|", "| **Seems slow: the likely fix** | on leave (TO BE CONFIRMED) |",
    ])
    f = [x for x in check(hedge_ok, rules) if x[0] == "hedge-word"]
    assert not f, f"hedge words inside a marker, a quote, a title label or a title cell must not count: {f}"
    f = [x for x in check("No activity since 11/11/2026, likely leave (roster status). It may be a leave. The cause seems clear.", rules) if x[0] == "hedge-word"]
    assert len(f) == 3 and [q.split(":")[0] for _, q, _ in f] == ["likely", "may be", "seems"], f"three hedge words in prose must count once each: {f}"
    f = [x for x in check("| Who | Likely note |\n|---|---|\n| a | the cause is likely a leave |\n| b | unlikely |", rules) if x[0] == "hedge-word"]
    assert len(f) == 1, f"a hedge word in a prose cell counts, 'unlikely' is another word: {f}"
    # marker form: the exact marker passes, a marker with a reason inside the brackets fails, another marker word is not read
    f = [x for x in check("Written 11/27/2026 (TO BE CONFIRMED). Quotes [TO BE COLLECTED: feedback text] stay. The count is 0 (TO BE CONFIRMED), 4 gaps.", rules) if x[0] == "marker-not-exact"]
    assert not f, f"the exact marker and another marker word must not count: {f}"
    f = [x for x in check("Due 12/07/2026 (TO BE CONFIRMED which date). Read [TO BE CONFIRMED: not read] and (TO BE CONFIRMED, timestamps missing).", rules) if x[0] == "marker-not-exact"]
    assert len(f) == 3, f"a marker with text inside its brackets must count each time: {f}"
    # comparatives: a sentence or a prose cell with a digit carries its data, a title or a quote is not the writer's claim
    comp_ok = "\n".join([
        "The new path is 70% faster (from 1,200 ms to 360 ms) with 3 fewer calls. One or more of the 14 files was read.",
        "The post says \"faster pruning for more formats\". See [Faster DDF and fewer DynamoDB calls](https://e.com/f).",
        "| Change | Impact |", "|---|---|", "| **Fewer calls — faster DDF** | 2 fewer DynamoDB calls per query |",
    ])
    f = [x for x in check(comp_ok, rules) if x[0] == "comparative-without-number"]
    assert not f, f"a comparative with a digit in its sentence or cell, in a quote, in a link label or in a title cell must not count: {f}"
    f = [x for x in check("The new path is faster with fewer calls. It does more of the design work (TO BE CONFIRMED).\n| Change | Impact |\n|---|---|\n| x | faster DDF and fewer calls |", rules) if x[0] == "comparative-without-number"]
    assert len(f) == 5 and f[2][1].startswith("more"), f"a comparative in a sentence or a prose cell with no digit counts each time, a marker does not excuse it: {f}"
    # from X to Y: a percentage or a multiplier before the span passes, a date or clock range is not a span, a bare span fails
    span_ok = "\n".join([
        "Peak memory fell 65% (from 1,700 MB to 600 MB). Sev2s were cut 2x (from 14 to 7 a week).",
        "Re:Invent runs from 11/30/2026 to 12/04/2026, the watcher from 07:00 to 19:00, the report from 1Q to 4Q and the plan from 2026 to 2027.",
        "| When | What |", "|---|---|", "| 11/23/2026 | halved 50% (from 8 to 4) |",
    ])
    f = [x for x in check(span_ok, rules) if x[0] == "span-without-relative"]
    assert not f, f"a span after a percentage or multiplier, a date range, a clock range, a quarter or a year span must not count: {f}"
    f = [x for x in check("Peak memory fell from 1,700 MB to 600 MB. Sev2s went from 14 to 7 a week (a 50% cut).\n| When | What |\n|---|---|\n| 11/23/2026 | from 8 to 4 |", rules) if x[0] == "span-without-relative"]
    assert len(f) == 3, f"a span with no relative change before it in its sentence or cell counts each time, a percentage after it does not excuse it: {f}"
    r_rel = dict(rules); r_rel["numeric_span_needs_relative"] = {"relative": [r"\d\s*%", r"\bhalved\b"]}
    f = [x for x in check("Sev2s halved (from 14 to 7 a week). Latency went from 9 ms to 3 ms (3x).", r_rel) if x[0] == "span-without-relative"]
    assert len(f) == 1 and f[0][1].startswith("from 9 ms to 3"), f"the instance's relative patterns replace the default: {f}"
    # the three rules of the 11/27/2026 fix wave pass 5 (validation pass 3): a silent case and a still-fires case each
    # marker as a predicate: the marker is a tag after a statement, never its verb and never bare
    f = [x for x in check("Every delta was not fetched (TO BE CONFIRMED). Count 0 (TO BE CONFIRMED), 4 gaps. See [Is TO BE CONFIRMED a verb](https://e.com/v).\n| a | b |\n|---|---|\n| (TO BE CONFIRMED) | \"it is TO BE CONFIRMED\" |", rules) if x[0] == "marker-as-predicate"]
    assert not f, f"a marker after a statement, alone in a cell, inside a link label or a quote must not count: {f}"
    f = [x for x in check("Every delta is TO BE CONFIRMED. The root causes are (TO BE CONFIRMED). Prepared (organiser x, TO BE CONFIRMED still recurring). The owner remains [TO BE CONFIRMED].", rules) if x[0] == "marker-as-predicate"]
    assert len(f) == 4 and sorted(q.split(":")[0] for _, q, _ in f) == ["are", "bare", "bare", "remains"], f"a bare marker and a marker after is/are/remains count each time: {f}"
    assert not [x for x in check("Every delta is TO BE CONFIRMED.", {"marker_exact": ["TO BE CONFIRMED"]}) if x[0] == "marker-as-predicate"], "without marker_not_after the predicate rule is off"
    # unclosed brackets: a cut title in a cell counts, paired brackets, a closing bracket alone (a) b) list) and prose do not
    f = [x for x in check("| t | n |\n|---|---|\n| [**[Tag][Prod] Title (V1)**](https://e.com/a) | a) first, b) second [1] (TO BE CONFIRMED) |\nProse with a [stray bracket is not a cell.", rules) if x[0] == "unclosed-bracket"]
    assert not f, f"paired brackets, a closing bracket alone and prose must not count: {f}"
    f = [x for x in check("| t | n |\n|---|---|\n| Bloom Rebuild[Prod Manifest has no size boun, planned? | fired (ECS memory over 85% |", rules) if x[0] == "unclosed-bracket"]
    assert len(f) == 2, f"a cell with an open [ or ( and no close counts once per cell: {f}"
    # a space before punctuation: in a cell or in prose it counts, inside code, a URL, a quote or the alignment row it does not
    f = [x for x in check("| 22 | [Sync] Storage: Kraken | 13:00 |\n|:---|---:|:---:|\nSee [a title: here](https://e.com/x?a=1 ) and `code : here`. The owner wrote \"done .\" there.", rules) if x[0] == "space-before-punctuation"]
    assert not f, f"a colon with no space before it, code, a URL, a quote and the alignment row must not count: {f}"
    f = [x for x in check("| 22 | [Sync] Metadata & Storage : Kraken | x |\n|---|---|---|\nA space before a comma , and a period .", rules) if x[0] == "space-before-punctuation"]
    assert len(f) == 3, f"a space before : , . counts each time, in a cell and in prose: {f}"
    print("style-check selftest: ok (15 rules fire on the bad text, 0 findings on the good text, 4 fix-wave false positives stay silent and their real cases still fire, 4 pass-4 rules silent on the allowed shapes and firing on the faults, 3 pass-5 rules the same)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("draft", nargs="?")
    ap.add_argument("--rules")
    ap.add_argument("--glossary", action="append", default=[])
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        selftest(); return 0
    if not a.draft or not a.rules:
        ap.error("draft and --rules are required")
    rules = read_rules(a.rules)
    gl = list(a.glossary) + [str(pathlib.Path(a.rules).parent / g) if not g.startswith(("/", "~")) else g for g in rules.get("glossary_files", [])]
    f = run(a.draft, rules, gl)
    if a.json:
        print(json.dumps([{"rule": r, "quote": q, "line": n} for r, q, n in f]))
    else:
        for r, q, n in f:
            print(f'{r} -> "{q}" (line {n})')
        print(f"style-check: {len(f)} finding(s)")
    return 1 if f else 0


if __name__ == "__main__":
    sys.exit(main())
