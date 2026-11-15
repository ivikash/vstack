# The example instance

An **instance** is the private folder that holds everything naming your company: which tools, which
documents, which channels, which people. vstack reads it at run time and never contains it. This
folder is a complete instance for a fictional company (Project Lantern, tools named `docs-mcp`,
`chat-mcp`). Copy it into a private repository, replace the example values with yours, and point
`VSTACK_INSTANCE` at it. `scripts/check.sh` also runs the invariants against this folder.

```
<instance>/
  tools.json          role -> MCP server and tool. The ONLY file where real tool names appear
  org-profile.md      your company's words for the public skills (principles, ratings, levels)
  mcp-servers.json    the servers each harness must have; `vstack gen-mcp` renders each harness's block
  graph.json          your bots and cells as a typed graph; `vstack check` enforces the invariants
  cells/*.json        one file per unit of automation (trigger, sources, writer, gate, sink, ledger)
  fixtures/*.json     synthetic evidence for dry runs. Real section names, invented values
  vstack.lock         the vstack commit this instance was tested against
  context/<program>/  (optional) standing inputs a program's cells read (section order, rules)
  skills/             (optional) writers that name your systems; link them the same way as vstack's
```

Every `vstack` command takes `--instance <dir>` or reads `$VSTACK_INSTANCE`, and fills
`--tools`, `--org-profile` and `--graph` from these files. One file per pattern: a second
`tools*.json` makes the command ask for an explicit flag.

## The privacy cut, as rules you can check

1. The instance repository has no public remote. `vstack check` with `VSTACK_INSTANCE` set fails
   if it finds one, or if the instance lives inside the vstack checkout.
2. Commits in the instance use your work e-mail, commits in vstack use your personal one.
   `scripts/check.sh identity` enforces the vstack side; the instance's own check enforces its side.
3. The denylist in `scripts/check.sh` lists your company's terms. When a term first appears in an
   instance file, add it to the denylist here in the same sitting.
4. A cell in a private component (people, HR) may record only dates, ids and counts in the ledger,
   never ratings, feedback text or candidate names. `vstack check --private-component` refuses otherwise.
5. Drafts are the only exit. Sinks are compose boxes and `[Draft]` documents a human sends.

## Pinning

`vstack.lock` holds one line, the vstack commit the instance's cells were last dry-run against:

```
vstack 876ff6a
```

`vstack run`, `check` and `gen-cron` print a warning when the checkout they run from is not that
commit. Move the pin after a dry run of every cell on one harness.
