#!/usr/bin/env python3
"""Copy check for a promotion document: 8-word runs the draft shares with another person's prose.

    promo-copycheck.py <draft.md> <source.md> [<source.md> ...] [--evidence-dir <dir>]

Standard library only. For every source file, print each run of 8 or more consecutive words that
also appears in the draft's own prose, grouped by source. Exit 1 when any run is found, exit 0 on a
clean draft. The writer runs it against every file it read that holds another person's words: the
feedback file, the reviewer rewrites, the calibration samples (SKILL.md, "Copy check").

What counts as the draft's own prose: everything except the `## Feedback` section, whose provider
text is verbatim by rule, and blockquote lines (`> "..."`), which are quotes by rule. Words are
lower-cased, punctuation stripped, so a run survives a changed comma or capital. Numbers count as
words, so a copied sentence with its figures is still a run.

Output, one line per run under a source header:

    source: <path>
      8-word run: "<the words>"
    promo-copycheck: <n> run(s) across <m> source(s)

`--evidence-dir <dir>` (round 3 close, D41 to D48 set, item D47): a run that also appears in any
file under that directory is a fact the writer could have read from a primary source, not only
from the other person's prose. Such a run prints `source-held` with the first evidence file that
holds it, is still counted and still sets the exit code, and the record says so instead of leaving
the question to the reader.

    8-word run: "<the words>" source-held: <evidence file>
"""
import re
import sys

RUN = 8
WORD = re.compile(r"[a-z0-9][a-z0-9'./%:-]*")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$")


def own_prose(text):
    """Lines of the draft that are the author's: outside `## Feedback`, not blockquotes, not
    headings, not the Sources line."""
    out, in_feedback = [], False
    for l in text.splitlines():
        m = HEADING.match(l)
        if m and len(m.group(1)) == 2:
            in_feedback = m.group(2).strip() == "Feedback"
            continue
        if m or in_feedback or l.lstrip().startswith(">") or re.match(r"^Sources( used)?:", l, re.I):
            continue
        out.append(l)
    return "\n".join(out)


def tokens(text):
    text = re.sub(r"\]\([^)]*\)", "]", text)          # drop link targets, keep link text
    return WORD.findall(text.lower())


def shingles(words, n=RUN):
    return {tuple(words[i:i + n]) for i in range(len(words) - n + 1)}


def shared_runs(draft_words, source_words, n=RUN):
    """Maximal runs of n or more words present in both texts, as strings, in source order."""
    draft_set = shingles(draft_words, n)
    runs, i = [], 0
    while i <= len(source_words) - n:
        if tuple(source_words[i:i + n]) in draft_set:
            j = i + n
            while j < len(source_words) and tuple(source_words[j - n + 1:j + 1]) in draft_set:
                j += 1
            runs.append(" ".join(source_words[i:j]))
            i = j
        else:
            i += 1
    return runs


def evidence_shingles(evidence_dir, n=RUN):
    """(path, shingle set) for every readable text file under evidence_dir, in path order."""
    import os
    out = []
    for root, _, files in os.walk(evidence_dir):
        for f in sorted(files):
            path = os.path.join(root, f)
            try:
                with open(path, encoding="utf-8") as fh:
                    out.append((path, shingles(tokens(fh.read()), n)))
            except (UnicodeDecodeError, OSError):
                continue
    return sorted(out)


def source_held(run, evidence):
    """The first evidence file whose text contains every shingle of the run, else None."""
    ws = run.split()
    need = shingles(ws)
    for path, sh in evidence:
        if need <= sh:
            return path
    return None


def main(argv):
    args = argv[1:]
    evidence_dir = None
    if "--evidence-dir" in args:
        i = args.index("--evidence-dir")
        if i + 1 >= len(args):
            print("--evidence-dir needs a directory")
            return 2
        evidence_dir = args[i + 1]
        args = args[:i] + args[i + 2:]
    if len(args) < 2 or args[0] in ("-h", "--help"):
        print(__doc__)
        return 2
    with open(args[0], encoding="utf-8") as fh:
        draft_words = tokens(own_prose(fh.read()))
    evidence = evidence_shingles(evidence_dir) if evidence_dir else []
    total, hit_sources, held = 0, 0, 0
    for path in args[1:]:
        with open(path, encoding="utf-8") as fh:
            runs = shared_runs(draft_words, tokens(fh.read()))
        print(f"source: {path}")
        if runs:
            hit_sources += 1
        for r in runs:
            total += 1
            where = source_held(r, evidence) if evidence else None
            if where:
                held += 1
                print(f'  {RUN}-word run: "{r}" source-held: {where}')
            else:
                print(f'  {RUN}-word run: "{r}"')
    tail = f", {held} source-held" if evidence_dir else ""
    print(f"promo-copycheck: {total} run(s) across {hit_sources} source(s){tail}")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
