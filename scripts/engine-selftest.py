#!/usr/bin/env python3
"""Engine self-test: seven behaviours proven against a throwaway instance, no model call, seconds.

  record-replace   `vstack record` twice on one run id leaves ONE runs.jsonl line and the latest verdict wins
  gather-steps     the rendered prompt carries gather.order and gather.step_0 before the sources
  instance-var     `${instance}` in record.post_record and config expands to the workflow's own instance
  no-schedule      `vstack run --harness kirocrew --no-publish` registers nothing (no command.txt, status rendered)
  extra-checklist  gate.extra_checklists renders into the GATE section, `check` fails a missing file and a writer
                   that lacks a checklist named in <instance>/gate-policy.json required_extra_checklists
  style-rules      scripts/style-check.py self-test passes, gate-policy.json required_style_rules renders the
                   countable-rules line into the GATE section, `check` fails a writer whose gate opts out of them,
                   `check-run` marks a draft with a finding unmet and passes once it is fixed
  new-workflow     the seven intake questions of ADR 0006 in order, defaults from the nearest workflow, the five files plus a
                   dry run, `check` passes on the view, never overwrites, refuses a bad regex, --defaults takes all seven
  reflect-span     `vstack reflect` on a two-section rolling document scores only the span the run wrote: a whole-document
                   read-back (title, status table, the previous run's section, an About edited by the owner) and the
                   draft's own About block give 0 changes, no proposal, no deletion count (ADR 0020)
  reflect-markup   a link read back as `[**x**](u)` for the draft's `**[x](u)**` is not an edit: alone it is 0 changes,
                   beside a real wording edit in the same row the proposed regex names the removed words and carries no
                   emphasis marker, and the filed before and after text agree on the spelling (ADR 0020). `--dry-run`
                   prints the diff and writes nothing

Exit 1 on the first failure. Run by scripts/check.sh (group `engine`).
"""
import json, os, pathlib, shutil, subprocess, sys, tempfile

HERE = pathlib.Path(__file__).resolve().parent.parent
VSTACK = HERE / "bin" / "vstack"
EXAMPLE = HERE / "example"

def sh(*args, env=None, check=True):
    r = subprocess.run([sys.executable, str(VSTACK), *args], capture_output=True, text=True, env=env)
    if check and r.returncode not in (0, 2):
        sys.exit(f"FAIL {' '.join(args)}\n{r.stdout}\n{r.stderr}")
    return r

def main():
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="vstack-selftest-"))
    try:
        inst = tmp / "inst"
        shutil.copytree(EXAMPLE, inst)
        wf_path = next((inst / "workflows").glob("*.json"))
        wf_path = [p for p in (inst / "workflows").glob("*.json") if not p.name.endswith(".sample.json")][0]
        wf = json.load(open(wf_path))
        marker = tmp / "post-record-ran.txt"
        wf["gather"] = {"order": "generator first, then ledger", "step_0": "run `echo step-zero` before any source",
                        **({"read_only": wf["gather"]["read_only"]} if isinstance(wf.get("gather"), dict) and wf["gather"].get("read_only") else {})}
        wf["record"] = {"post_record": f"{sys.executable} -c \"import pathlib; pathlib.Path('{marker}').write_text(open('${{instance}}/vstack.lock').read())\""}
        wf.setdefault("config", {})["instanceRoot"] = "${instance}"
        wf_path.write_text(json.dumps(wf, indent=2))
        runs = tmp / "runs"; ledger = tmp / "ledger"; cache = tmp / "cache"
        common = ["--instance", str(inst), "--run-root", str(runs), "--ledger-root", str(ledger), "--cache-root", str(cache),
                  "--skills-dir", str(HERE / "skills")]

        # gather-steps + instance-var in the prompt
        r = sh("render", str(wf_path), *common)
        prompt = r.stdout
        assert "Order: generator first, then ledger" in prompt, "gather.order not rendered"
        assert "Step 0 (before any source below): run `echo step-zero`" in prompt, "gather.step_0 not rendered"
        i_order, i_src = prompt.index("Order: generator"), prompt.index("- connector `")
        assert i_order < i_src, "gather.order rendered after the sources"
        assert "${instance}" not in prompt, "${instance} left unexpanded in the prompt"
        print("gather-steps  ok")

        # no-schedule: kirocrew harness with --no-publish must not call the host CLI
        r = sh("run", str(wf_path), "--harness", "kirocrew", "--no-publish", *common)
        run_dirs = sorted((runs / wf["id"]).glob("kirocrew-*"))
        assert run_dirs, "no run dir created"
        rd = run_dirs[-1]
        assert not (rd / "command.txt").exists(), "kirocrew no-publish run wrote command.txt (it tried to schedule)"
        meta = json.load(open(rd / "meta.json"))
        assert meta["result"]["status"] == "rendered", meta["result"]
        print("no-schedule   ok")

        # record-replace + instance-var in post_record
        (rd / "draft.md").write_text("# draft\n\nbody\n")
        (rd / "result.json").write_text(json.dumps({"status": "ok", "mode": "no-publish"}))
        sh("record", str(rd), "--instance", str(inst), "--ledger-root", str(ledger))
        lines1 = (ledger / "runs.jsonl").read_text().splitlines()
        first = json.loads(lines1[-1])
        assert marker.exists() and marker.read_text().strip().startswith("vstack"), "post_record did not expand ${instance} to the run's instance"
        # make the run pass the generic contract now (gate.md) and record again
        (rd / "gate.md").write_text("pass 1: fail\npass 2: pass\n")
        sh("record", str(rd), "--instance", str(inst), "--ledger-root", str(ledger))
        lines2 = (ledger / "runs.jsonl").read_text().splitlines()
        ids = [json.loads(l)["run_id"] for l in lines2]
        assert len(lines2) == len(lines1), f"rerun appended a second line ({len(lines1)} -> {len(lines2)})"
        assert ids.count(first["run_id"]) == 1, "run id appears twice"
        second = [json.loads(l) for l in lines2 if json.loads(l)["run_id"] == first["run_id"]][0]
        assert second["recorded_by"] == "vstack record" and second != first, "second record did not replace the line"
        print("record-replace ok")
        print("instance-var  ok")

        # extra-checklist: gate.extra_checklists renders into the GATE section, `check` fails a missing file,
        # and gate-policy.json required_extra_checklists fails a writer whose gate lacks the checklist
        style = inst / "style.md"
        style.write_text("# Style\n\n- **lead-with-outcome**: the first sentence states the result.\n")
        wf = json.load(open(wf_path))
        wf["gate"]["extra_checklists"] = ["${instance}/style.md"]
        wf_path.write_text(json.dumps(wf, indent=2))
        r = sh("render", str(wf_path), *common)
        assert f"further checklist rules, each scored the same way: {inst.resolve()}/style.md" in r.stdout, "extra_checklists not rendered in the GATE section"
        assert "${instance}" not in r.stdout, "${instance} left unexpanded in extra_checklists"
        r = sh("check", "--instance", str(inst), check=False)
        assert r.returncode == 0, f"check failed with an existing checklist:\n{r.stdout}{r.stderr}"
        wf["gate"]["extra_checklists"] = ["${instance}/missing.md"]
        wf_path.write_text(json.dumps(wf, indent=2))
        r = sh("check", "--instance", str(inst), check=False)
        assert r.returncode != 0 and "does not exist" in r.stdout + r.stderr, "check passed a checklist file that does not exist"
        wf["gate"].pop("extra_checklists")
        wf_path.write_text(json.dumps(wf, indent=2))
        (inst / "gate-policy.json").write_text(json.dumps({"required_extra_checklists": ["${instance}/style.md"]}))
        r = sh("check", "--instance", str(inst), check=False)
        assert r.returncode != 0 and "required checklist" in r.stdout + r.stderr, "check passed a writer that lacks the required checklist"
        wf["gate"]["extra_checklists"] = ["${instance}/style.md"]
        wf_path.write_text(json.dumps(wf, indent=2))
        r = sh("check", "--instance", str(inst), check=False)
        assert r.returncode == 0, f"check failed a writer that carries the required checklist:\n{r.stdout}{r.stderr}"
        print("extra-checklist ok")

        # style-rules: the countable style checks the instance names apply to every writer, in the prompt, in
        # `check` (no opt-out) and in `check-run` (a finding is unmet)
        r = subprocess.run([sys.executable, str(HERE / "scripts" / "style-check.py"), "--selftest"], capture_output=True, text=True)
        assert r.returncode == 0, f"style-check --selftest failed:\n{r.stdout}{r.stderr}"
        rules = inst / "style-rules.json"
        rules.write_text(json.dumps({"max_words_per_sentence": 40, "weasel_words": ["several"], "date_without_year": True,
                                     "iso_dates": True, "url_as_label": True, "semicolons": True, "em_dashes": True,
                                     "exempt_line_prefixes": ["Sources:"]}))
        (inst / "gate-policy.json").write_text(json.dumps({"required_extra_checklists": ["${instance}/style.md"], "required_style_rules": "${instance}/style-rules.json"}))
        r = sh("check", "--instance", str(inst), check=False)
        assert r.returncode == 0, f"check failed with a valid required_style_rules:\n{r.stdout}{r.stderr}"
        r = sh("render", str(wf_path), *common)
        assert "Countable rules (every finding is a blocker" in r.stdout and "style-check" in r.stdout, "required_style_rules not rendered into the GATE section"
        assert str(rules.resolve()) in r.stdout or str(rules) in r.stdout, "the rules path is not named in the GATE section"
        wf = json.load(open(wf_path)); wf["gate"]["style_rules"] = False; wf_path.write_text(json.dumps(wf, indent=2))
        r = sh("check", "--instance", str(inst), check=False)
        assert r.returncode != 0 and "does not run the required style rules" in r.stdout + r.stderr, "check passed a writer whose gate opts out of the style rules"
        wf["gate"].pop("style_rules"); wf_path.write_text(json.dumps(wf, indent=2))
        (inst / "gate-policy.json").write_text(json.dumps({"required_extra_checklists": ["${instance}/style.md"], "required_style_rules": "${instance}/missing-rules.json"}))
        r = sh("check", "--instance", str(inst), check=False)
        assert r.returncode != 0 and "does not exist" in r.stdout + r.stderr, "check passed a required_style_rules file that does not exist"
        (inst / "gate-policy.json").write_text(json.dumps({"required_extra_checklists": ["${instance}/style.md"], "required_style_rules": "${instance}/style-rules.json"}))
        # check-run: a run whose draft carries a date with no year is unmet on the style rule, met once fixed
        (rd / "draft.md").write_text("# draft\n\nSources: used a.b; unavailable none\n\nThe worker ran out of memory on 11/20 and several tasks stalled.\n")
        (rd / "gate.md").write_text("passes: 2\n"); (rd / "brief.md").write_text("a\nb\nc\n"); (rd / "diff.md").write_text("first run\n")
        (rd / "evidence.json").write_text(json.dumps({"sources": [], "evidence_hash": "x"}))
        r = sh("check-run", str(rd), "--workflow", str(wf_path), "--instance", str(inst), check=False)
        out = r.stdout + r.stderr
        assert r.returncode != 0 and "style date-without-year" in out and "style weasel-word" in out, f"check-run did not report the style findings:\n{out}"
        (rd / "draft.md").write_text("# draft\n\nSources: used a.b; unavailable none\n\nThe worker ran out of memory on 11/20/2026 and 3 tasks stalled.\n")
        r = sh("check-run", str(rd), "--workflow", str(wf_path), "--instance", str(inst), check=False)
        out = r.stdout + r.stderr
        assert "style " not in out.replace("style rules:", ""), f"check-run still reports a style finding on the fixed draft:\n{out}"
        print("style-rules   ok")

        # new-workflow: the seven intake questions of ADR 0006, in that order, with defaults from the nearest workflow,
        # write the five files plus a dry run, pass `check` inside the instance, never overwrite, and refuse a bad regex
        vm = __import__("types").ModuleType("vstack_mod"); vm.__file__ = str(VSTACK)
        exec(compile(VSTACK.read_text(), str(VSTACK), "exec"), vm.__dict__)
        assert [k for k, _ in vm.INTAKE] == ["document", "audience", "due", "sources", "lands", "never", "example"], "INTAKE is not the seven questions of ADR 0006 in order"
        out = tmp / "nw-out"
        answers = tmp / "answers.json"
        answers.write_text(json.dumps({"document": "Weekly budget note, one rolling file", "audience": "the owner", "due": "1 0 * * MON UTC",
                                       "sources": "docs.read, chat.search", "lands": "files.write reports/budget/<YYYY-MM-DD>.md",
                                       "never": ["\\bforecast\\b :: no forecasts (owner ruling)", "never names a vendor price"],
                                       "example": str(inst / "glossary.md")}))
        r = sh("new-workflow", "budget-weekly", "--instance", str(inst), "--answers", str(answers), "--out", str(out), "--skills-dir", str(HERE / "skills"), check=False)
        assert r.returncode == 0 and "invariants: PASS" in r.stdout, f"new-workflow failed:\n{r.stdout}{r.stderr}"
        assert f"nearest: {wf['id']}" in r.stdout, "nearest workflow not reported"
        for rel in ("workflows/budget-weekly.json", "workflows/budget-weekly.sample.json", "context/budget-weekly/mistakes.md",
                    "context/budget-weekly/example.md", "adr/budget-weekly/0001-why-it-exists-and-what-it-must-never-do.md"):
            assert (out / rel).exists(), f"new-workflow did not write {rel}"
        nw = json.load(open(out / "workflows/budget-weekly.json"))
        assert nw["trigger"]["cron"] == "1 0 * * MON" and nw["trigger"]["timezone"] == "UTC", nw["trigger"]
        assert [s["connector"] for s in nw["sources"]] == ["docs.read", "chat.search"], nw["sources"]
        assert nw["sink"]["connector"] == "files.write" and nw["sink"]["dry_run_path"] == "budget-weekly.md", nw["sink"]
        assert nw["draft_contract"]["must_not_match"] == [{"pattern": "\\bforecast\\b", "why": "no forecasts (owner ruling)"}], nw["draft_contract"]
        assert "Never: never names a vendor price" in nw["writer"]["extra_inputs"], "a plain never sentence did not reach the writer"
        assert "${instance}/style.md" in nw["gate"]["extra_checklists"], "gate-policy required checklist not added to the new gate"
        assert "never names a vendor price" in (out / "adr/budget-weekly/0001-why-it-exists-and-what-it-must-never-do.md").read_text(), "ADR 0001 lacks the never line"
        assert "Weekly budget note" in (out / "adr/budget-weekly/0001-why-it-exists-and-what-it-must-never-do.md").read_text(), "ADR 0001 lacks the document"
        assert (out / "context/budget-weekly/example.md").read_text().count("\n") > 2, "example.md was not copied from the given file"
        prompts = list((out / "runs/budget-weekly").glob("print-*/prompt.md"))
        assert len(prompts) == 1 and "Readers: the owner" in prompts[0].read_text(), "dry run prompt missing or without the audience"
        r = sh("check", "--instance", str(out / ".instance-view"), check=False)
        assert r.returncode == 0, f"check failed on the view with the new workflow:\n{r.stdout}{r.stderr}"
        r = sh("new-workflow", "budget-weekly", "--instance", str(inst), "--defaults", "--out", str(out), check=False)
        assert r.returncode != 0 and "never overwrites" in r.stderr, "new-workflow overwrote an existing workflow"
        r = sh("new-workflow", "budget-bad", "--instance", str(inst), "--defaults", "--set", "never=( :: unclosed", "--out", str(out), check=False)
        assert r.returncode != 0 and "not a valid regex" in r.stderr, "new-workflow accepted a never rule that is not a regex"
        r = sh("new-workflow", "budget-defaults", "--instance", str(inst), "--defaults", "--out", str(out), "--skills-dir", str(HERE / "skills"), check=False)
        assert r.returncode == 0 and r.stdout.count("(default)") == 7, f"--defaults did not take all seven defaults:\n{r.stdout}{r.stderr}"
        print("new-workflow  ok")

        reflect_behaviours(tmp, inst, vm, wf["id"])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

DRAFT_TWO_SECTIONS = """# Budget notes

Sources: used docs.read; unavailable none

| Last run | Items |
|---|---|
| 11/28/2026 | 2 |

## 11/28/2026 (covers 11/25/2026 to 11/27/2026)

Two items this run.

## Items
| # | Item | Owner | Note |
|---|---|---|---|
| 1 | **[Cache rebuild](https://example.com/t/1)** | a builder | finished 11/27/2026 |
| 2 | **[Queue split](https://example.com/t/2)** | a builder | in review |

## About
One rolling document, newest run on top.
"""

# the whole document as the store returns it: title and status table (the frame), this run's section with its
# sub-heading demoted and the bold links turned inside out, the previous run's section, and an About the owner edited
LANDED_WHOLE_DOC = """<!-- id=a-0, type=heading, hash=1 -->
# Budget notes

<!-- id=a-1, type=table, hash=2 -->
| Last run | Items |
| --- | --- |
| 11/28/2026 | 2 |

<!-- id=a-2, type=heading, hash=3 -->
## 11/28/2026 (covers 11/25/2026 to 11/27/2026)

<!-- id=a-3, type=paragraph, hash=4 -->
Two items this run.

<!-- id=a-4, type=heading, hash=5 -->
### Items

<!-- id=a-5, type=table, hash=6 -->
| # | Item | Owner | Note |
| --- | --- | --- | --- |
| 1 | [**Cache rebuild**](https://example.com/t/1) | a builder | finished 11/27/2026 |
| 2 | [**Queue split**](https://example.com/t/2) | a builder | in review |

<!-- id=b-0, type=heading, hash=7 -->
## 11/26/2026 (covers 11/23/2026 to 11/25/2026)

<!-- id=b-1, type=paragraph, hash=8 -->
One item this run, and the owner rewrote this sentence by hand.

<!-- id=b-2, type=heading, hash=9 -->
### Items

<!-- id=b-3, type=table, hash=10 -->
| # | Item | Owner | Note |
| --- | --- | --- | --- |
| 1 | [**Index repair**](https://example.com/t/0) | a builder | done |

<!-- id=c-0, type=heading, hash=11 -->
## About

<!-- id=c-1, type=paragraph, hash=12 -->
One rolling document, newest run on top, edited by the owner on 11/28/2026.
"""


def reflect_behaviours(tmp, inst, vm, wf_id):
    """reflect-span and reflect-markup (ADR 0020), end to end through `vstack reflect` plus the module's own functions."""
    runs = tmp / "reflect-runs"; ledger = tmp / "reflect-ledger"
    rd = runs / wf_id / "kirocrew-20261128-000100-abcdef"
    rd.mkdir(parents=True)
    (rd / "draft.md").write_text(DRAFT_TWO_SECTIONS)
    (rd / "landed-24h.md").write_text(LANDED_WHOLE_DOC)
    (rd / "result.json").write_text(json.dumps({"status": "ok", "landed": {"mode": "chorus", "doc_id": "docAAAAAAAAA"}}))
    (rd / "scorecard.json").write_text(json.dumps({"run_id": "20261128-000100-abcdef", "workflow": wf_id}))
    ctx = inst / "context" / wf_id
    props = ctx / "proposals.md"; dels = ctx / "deletions.json"
    before_props = props.read_text() if props.exists() else ""
    # --dry-run writes nothing and prints the diff
    r = sh("reflect", str(rd), "--age", "24h", "--instance", str(inst), "--ledger-root", str(ledger), "--dry-run", check=False)
    assert r.returncode == 0, f"reflect --dry-run failed:\n{r.stdout}{r.stderr}"
    assert not (rd / "reflect-24h.json").exists() and not (ledger / "reflect.jsonl").exists(), "reflect --dry-run wrote a file"
    dry = json.loads(r.stdout)
    assert dry["would_file"] == {"proposals": 0, "mistakes": 0, "deletions": 0, "proposed_regexes": []}, f"dry run would file from the frame or another section: {dry['would_file']}"
    # the real reflect: only the written span is scored
    r = sh("reflect", str(rd), "--age", "24h", "--instance", str(inst), "--ledger-root", str(ledger), check=False)
    assert r.returncode == 0, f"reflect failed:\n{r.stdout}{r.stderr}"
    out = json.load(open(rd / "reflect-24h.json"))
    assert out["changes"] == [] and out["owner_edit_ratio"] == 0, f"reflect scored blocks outside the written span as owner edits: {out['counts']} {[(c['kind'], (c['before'] or c['after'] or '')[:60]) for c in out['changes']]}"
    assert out["span"] == {"draft_blocks_outside": 4, "landed_blocks_outside": 8}, out["span"]  # title, status table, About heading and paragraph; those plus the previous run's four blocks
    assert (props.read_text() if props.exists() else "") == before_props, "reflect filed a proposal from the frame or another run's section"
    assert not dels.exists() or all(v == 0 for v in json.load(open(dels)).values()), "reflect counted the About block as a deletion"
    print("reflect-span  ok")

    # reflect-markup: the exact read-back pair alone is no edit
    d = vm.reflect_diff("| # | Item |\n|---|---|\n| 1 | **[x](https://example.com/u)** |", "| # | Item |\n| --- | --- |\n| 1 | [**x**](https://example.com/u) |")
    assert d["changes"] == [] and d["owner_edit_ratio"] == 0, d
    # beside a real wording edit in the same row, the proposed regex names the removed words, not the link
    before = "| # | Item | Note |\n|---|---|---|\n| 1 | **[Cache rebuild](https://example.com/t/1)** | finished, we think it is likely stable |"
    after = "| # | Item | Note |\n| --- | --- | --- |\n| 1 | [**Cache rebuild**](https://example.com/t/1) | finished |"
    d = vm.reflect_diff(before, after)
    assert len(d["changes"]) == 1 and d["changes"][0]["kind"] == "wording", d
    c = d["changes"][0]
    assert "**[Cache rebuild](https://example.com/t/1)**" in c["before"] and "**[Cache rebuild](https://example.com/t/1)**" in c["after"], f"before and after disagree on the link spelling: {c}"
    rx = vm._proposed_regex(c["before"], c["after"])
    assert rx and "\\*" not in rx and "we" in rx and "likely" in rx, f"the proposed regex came from the link markup, not the removed words: {rx}"
    assert d["owner_edit_ratio"] < 0.3, f"the edit ratio counts the link markup: {d['owner_edit_ratio']}"
    # the canonical form covers italic and nested markers too, and leaves a plain link alone
    assert vm.canon_markup("[*x*](u) [_y_](u) [***z***](u) [**[Tag] t**](u) [p](u)") == "*[x](u)* _[y](u)_ ***[z](u)*** **[[Tag] t](u)** [p](u)"
    print("reflect-markup ok")


if __name__ == "__main__":
    main()
