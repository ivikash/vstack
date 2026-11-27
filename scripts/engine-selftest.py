#!/usr/bin/env python3
"""Engine self-test: six behaviours proven against a throwaway instance, no model call, seconds.

  record-replace   `vstack record` twice on one run id leaves ONE runs.jsonl line and the latest verdict wins
  gather-steps     the rendered prompt carries gather.order and gather.step_0 before the sources
  instance-var     `${instance}` in record.post_record and config expands to the workflow's own instance
  no-schedule      `vstack run --harness kirocrew --no-publish` registers nothing (no command.txt, status rendered)
  extra-checklist  gate.extra_checklists renders into the GATE section, `check` fails a missing file and a writer
                   that lacks a checklist named in <instance>/gate-policy.json required_extra_checklists
  style-rules      scripts/style-check.py self-test passes, gate-policy.json required_style_rules renders the
                   countable-rules line into the GATE section, `check` fails a writer whose gate opts out of them,
                   `check-run` marks a draft with a finding unmet and passes once it is fixed

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
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

if __name__ == "__main__":
    main()
