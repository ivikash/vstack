#!/usr/bin/env python3
"""Routing eval for the skills: does each skill's description win the prompts meant for it?

Deterministic and model-free. Every skill's description is tokenised (lowercase words of three or
more letters, a small stop list removed, each word weighted by how few descriptions carry it). A
prompt is scored against every description by summed overlap weight. A positive case passes when
its skill ranks first; a negative case passes when its skill does not rank first. Exit 1 on any
failure. Cases live in evals/triggers.json.
"""
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STOP = set("""the and for from with that this into when use used uses user caller skill skills document documents
            draft drafts write writes writing written one two any all its it is are be to of in on or as a an by not
            never every each then than them they you your has have had will does do did get gets no yes""".split())


def tokens(text):
    return {w for w in re.findall(r"[a-z][a-z-]{2,}", text.lower()) if w not in STOP}


def main():
    cases = json.load(open(ROOT / "evals" / "triggers.json"))["cases"]
    descs = {}
    for p in sorted((ROOT / "skills").glob("*/SKILL.md")):
        m = re.search(r"^description:\s*(.*)$", p.read_text(), re.M)
        descs[p.parent.name] = tokens(m.group(1)) if m else set()
    n = len(descs)
    df = {}
    for toks in descs.values():
        for t in toks:
            df[t] = df.get(t, 0) + 1
    weight = {t: math.log(1 + n / df[t]) for t in df}

    def rank(prompt):
        pt = tokens(prompt)
        scores = {name: sum(weight[t] for t in pt & toks) for name, toks in descs.items()}
        return sorted(scores.items(), key=lambda kv: -kv[1])

    checks = fails = 0
    for skill, c in cases.items():
        if skill not in descs:
            print(f"FAIL {skill}: no such skill"); fails += 1; continue
        for prompt in c.get("positive", []):
            checks += 1
            top = rank(prompt)
            if top[0][0] != skill or top[0][1] == 0:
                fails += 1
                print(f"FAIL positive {skill}: ranked first was {top[0][0]} ({top[0][1]:.2f}) for: {prompt[:70]}")
        for prompt in c.get("negative", []):
            checks += 1
            top = rank(prompt)
            if top[0][0] == skill:
                fails += 1
                print(f"FAIL negative {skill}: wrongly ranked first for: {prompt[:70]}")
    print(f"trigger eval: {checks} checks, {fails} failure(s), {n} skills")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
