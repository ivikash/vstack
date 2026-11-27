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
                           labels are not counted, a link label counts as one word)
  weasel_words             list of words or phrases, each occurrence outside tables headers, quoted speech,
                           code and title-like link labels is a finding
  acronyms                 {"min": 2, "max": 6, "allow": [...], "glossary_heading": "Glossary"}: a run of
                           capitals of that length whose first use is neither followed by " (" nor inside
                           round brackets, and which no glossary file and no section under the doc's own
                           glossary heading names, is a finding
  date_without_year        true: MM/DD with no /YYYY outside URLs, code and title-like link labels
  iso_dates                true: YYYY-MM-DD outside URLs and code
  url_as_label             true: a markdown link whose label is the URL itself
  semicolons               true: a semicolon outside table rows, code, title-like link labels, HTML entities,
                           the fixed heading TL;DR and lines whose prefix is in exempt_line_prefixes
  em_dashes                true: an em-dash (U+2014) outside code and title-like link labels
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


def _exempt(line, prefixes):
    s = line.lstrip()
    return any(s.startswith(p) for p in prefixes)


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
            blob = _links_replaced(blob, keep_prose_labels=False)
            for s in re.split(r"(?<=[.!?])\s+(?=[\"'(\[*A-Z0-9])", blob):
                n = len(s.split())
                if n > int(limit):
                    add("sentence-length", f"{n} words: {s[:70]}", start)
        for i, l in enumerate(lines):
            bare = l.strip()
            if not bare or _is_table_row(l) or bare.startswith("#") or _exempt(l, prefixes) or bare.startswith("<!--"):
                flush(); para, start = [], None
                continue
            bare = re.sub(r"^(\s*([-*+]|\d+[.)])\s+)", "", bare)
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
            t = _links_replaced(l)
            t = re.sub(r"\"[^\"\n]*\"|“[^”\n]*”", "QUOTE", t)
            for m in pat.finditer(t):
                if re.search(r"\bhow\s*$", t[:m.start()], re.I):
                    continue  # "how many", "how much": a question, not a hedge
                add("weasel-word", f"{m.group(1)}: {t[max(0, m.start() - 30):m.end() + 30]}", i + 1)

    # acronyms: first use expanded, or named by a glossary
    ac = rules.get("acronyms")
    if ac:
        lo, hi = int(ac.get("min", 2)), int(ac.get("max", 6))
        allow = set(ac.get("allow", [])) | ENGINE_ALLOW | ROMAN
        gl_text = "\n".join(glossary_texts)
        heading = ac.get("glossary_heading", "Glossary")
        own = re.search(r"^#{1,6}\s+" + re.escape(heading) + r"\b.*?(?=^#{1,6}\s|\Z)", code_free, re.M | re.S)
        gl_text += "\n" + (own.group(0) if own else "")
        known = set(re.findall(r"(?<![A-Za-z0-9])([A-Z]{2}[A-Z0-9]{0,8})s?(?![A-Za-z0-9])", gl_text))
        tok = re.compile(r"(?<![A-Za-z0-9/&-])([A-Z]{%d}[A-Z0-9]{0,%d})s?(?![A-Za-z0-9/-])" % (lo, max(0, hi - lo)))
        seen = set()
        for i, l in enumerate(lines):
            if _exempt(l, prefixes) or l.strip().startswith("<!--"):
                continue
            t = _links_replaced(l, keep_prose_labels=True)
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
                in_brackets = before.endswith("(") or re.search(r"\((the |an? )?$", before) is not None
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
            t = _links_replaced(l)
            for m in re.finditer("\u2014", t):
                add("em-dash", t[max(0, m.start() - 40):m.end() + 20], i + 1)
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
    ])
    f = check(bad, rules)
    rules_hit = {r for r, _, _ in f}
    want = {"sentence-length", "weasel-word", "acronym-unexpanded", "date-without-year", "iso-date", "url-as-label", "semicolon", "em-dash"}
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
    print("style-check selftest: ok (8 rules fire on the bad text, 0 findings on the good text)")


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
