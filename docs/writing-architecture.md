# Architecture

## The writing / plumbing split

These skills do one thing: **writing**. Given evidence, they produce a well-structured
document in a consistent, honest voice. They do not gather data and they do not publish.

That separation is deliberate. People-review work has two halves:

1. **Plumbing** (org-specific): fetching evidence from your docs system, task tracker,
   code host, and chat; and publishing the finished document back. Every company wires
   this differently, and it often touches confidential systems.
2. **Writing** (universal): turning evidence into a clear, balanced, well-structured
   document. This is the same craft everywhere.

By packaging only the writing half as portable skills, the same writing standard can be
shared widely, while each team keeps its own plumbing separate and private.

## Pairing a skill with a fetch step

A typical end-to-end flow:

```
gather evidence  ->  apply the writing skill  ->  publish
(your tools)         (this repo)                  (your tools)
```

You can drive this manually (gather, paste evidence, run `/write-...`, copy the result
where it belongs), or with automation. If you use an orchestration layer that runs
multiple steps, have an early step collect the evidence and a later step invoke the
writing skill on that evidence, then a final step publish the output. The skill is the
stable, reusable middle; the fetch and publish steps are yours to implement against
whatever systems you have.

## Why skills rather than a monolithic script

- A skill is the idiomatic, shareable unit of reusable instructions in Claude Code.
- Keeping writing rules in the skill (not in a caller's prompt) means one source of
  truth: improve the voice once and every caller benefits.
- The skills carry no data sources, so they are safe to publish and easy to audit.

## Extending

- **New document type**: add a new skill directory with its own `SKILL.md` and
  `template.md`.
- **Different ladder or rating scale**: you do not edit the skills. Pass your own rubric
  (see `skills/write-promo-doc/rubric-TEMPLATE.md`) and your own rating terms as input.
