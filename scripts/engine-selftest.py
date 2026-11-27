#!/usr/bin/env python3
"""Engine self-test: five behaviours proven against a throwaway instance, no model call, seconds.

  record-replace   `vstack record` twice on one run id leaves ONE runs.jsonl line and the latest verdict wins
  gather-steps     the rendered prompt carries gather.order and gather.step_0 before the sources
  instance-var     `${instance}` in record.post_record and config expands to the workflow's own instance
  no-schedule      `vstack run --harness kirocrew --no-publish` registers nothing (no command.txt, status rendered)
  extra-checklist  gate.extra_checklists renders into the GATE section, `check` fails a missing file and a writer
                   that lacks a checklist named in <instance>/gate-policy.json required_extra_checklists

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
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

if __name__ == "__main__":
    main()
