# Harnesses

vstack does not run a model itself. `vstack run <workflow> --harness <name>` renders one prompt and
hands it to the coding agent you name, non-interactively, then reads the run directory back.
Four harnesses are wired today. Adding one is a ten-line branch in `run_on_harness` in
`bin/vstack` plus a row here.

| Harness | Command vstack runs | Skills are read from | Notes |
|---|---|---|---|
| `claude` | `claude -p --output-format text --permission-mode acceptEdits --allowedTools Read Write Edit Glob Grep "Bash(mkdir:*)" "Bash(cp:*)" "Bash(cat:*)"`, prompt on stdin | `~/.claude/skills/<name>` | The reference harness. Prompt names every skill file by absolute path, so no plugin install is needed |
| `codex` | `codex exec --skip-git-repo-check -C <run dir> -s workspace-write`, prompt on stdin | `~/.codex/skills/<name>` and `~/.agents/skills/<name>` | Same prompt. Codex reads SKILL.md through its skills dir |
| `kiro` | `kiro-cli chat --no-interactive --trust-all-tools [--agent <name>] "<prompt>"` | `~/.kiro/skills/<name>` | Kiro CLI 3.x denies any tool not named in `--trust-tools`, and the internal tool names differ by engine, so the run trusts all tools, or runs under the `vstack-runner` agent template that `vstack gen-agent --harness kiro` emits (only the MCP servers in connectors.json, read tools trusted) |
| `kirocrew` | `kirocrew cron add <id> "<prompt>" --at "in 1 minute" --approval-mode auto [--agent <bot>]` | `~/.kiro/crew/skills/<name>` | Asynchronous: the Kiro Crew agent is the harness and runs the stages with its own MCP tools. `result.json` appears when the job finishes. `vstack gen-cron --harness kirocrew` emits standing jobs whose message tells the agent to `vstack render` the workflow with its shell and follow the printed prompt, so each wake gets a fresh run directory |

## One canonical copy of every skill

`vstack link-skills --canonical <this repo>/skills --targets ~/.claude/skills ~/.codex/skills ~/.agents/skills ~/.kiro/skills ~/.kiro/crew/skills --skills <names>`
turns every harness skill directory into a symlink to this repository. A `git pull` here updates
all five. `vstack verify-skills` compares what each harness sees against `skills-lock.json` and
fails a run before any model call if a copy drifted.

Instance-specific skills (the ones that name your company's tools) are linked the same way from
the instance repository. The harness dirs end up holding two kinds of symlinks, both pointing at
git checkouts, never real copies.

## What a run leaves behind

`~/.local/state/vstack/runs/<workflow>/<harness>-<run id>/` holds `prompt.md`, `evidence.json`,
`diff.md`, `draft.md`, `gate.md`, `result.json`. `~/.local/state/vstack/ledger/runs.jsonl` gets
one appended line per run. These are the only places a workflow writes outside its sink, and the
sink is always a draft (a compose box, a `[Draft]` document) that a human sends.

## Non-interactive flags are the contract

Every harness above has a flag that means "run to completion without a prompt". That flag, the
absolute paths in the rendered prompt, and the run directory are the whole interface. Nothing
in vstack depends on a harness's plugin or marketplace format, which is why the same workflow runs
on all four.
