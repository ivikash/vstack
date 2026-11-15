# The example instance

An **instance** is the private folder that holds everything naming your company: which tools, which
documents, which channels, which people. vstack reads it at run time and never contains it. This
folder is a complete instance for a made-up company (Project Lantern, tools named `docs-mcp`,
`chat-mcp`). Copy it into a private repository, replace the example values with yours, and point
`VSTACK_INSTANCE` at it. `scripts/check.sh` also runs the invariants against this folder.

```
<instance>/
  workflows/<name>.json         one recurring document: trigger, sources, writer, gate, sink, ledger
  workflows/<name>.sample.json  made-up evidence for a dry run of that workflow (real section names, invented values)
  connectors.json               connector name -> MCP server and tool. The ONLY file where real tool names appear
  glossary.md                   your company's words for the public skills (principles, ratings, levels)
  mcp-servers.json              the servers each harness must have; `vstack gen-mcp` renders each harness's block
  vstack.lock                   the vstack commit this instance was tested against
  context/<program>/            (optional) standing inputs a program's workflows read (template contracts, rules, rubrics)
  skills/                       (optional) writers that name your systems; link them the same way as vstack's
```

Every `vstack` command takes `--instance <dir>` or reads `$VSTACK_INSTANCE`, and fills
`--connectors`, `--glossary` and `--workflows` from these files. One file per pattern: a second
`connectors*.json` makes the command ask for an explicit flag.

There is no separate map file. `vstack map` derives the estate (sources, writers, gates, sinks,
ledgers, bots) from the workflows, and `vstack check` enforces the invariants over the same derivation.

## The privacy cut, as rules you can check

1. The instance repository has no public remote. `scripts/check.sh` with `VSTACK_INSTANCE` set fails
   if it finds one, or if the instance lives inside the vstack checkout.
2. Commits in the instance use your work e-mail, commits in vstack use your personal one.
   `scripts/check.sh identity` enforces the vstack side; the instance's own check enforces its side.
3. The denylist in `scripts/check.sh` lists your company's terms. When a term first appears in an
   instance file, add it to the denylist here in the same sitting.
4. A workflow in a private component (people, HR) may record only dates, ids and counts in the
   ledger, never ratings, feedback text or candidate names. `vstack check --private-component`
   refuses otherwise.
5. Drafts are the only exit. Sinks are compose boxes and `[Draft]` documents a human sends.

## Pinning

`vstack.lock` holds one line, the vstack commit the instance's workflows were last dry-run against:

```
vstack 876ff6a
```

`vstack run`, `check` and `gen-cron` print a warning when the checkout they run from is not that
commit. Move the pin after a dry run of every workflow on one harness.
