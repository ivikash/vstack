# Leadership Writing Skills

A set of [Claude Code](https://docs.claude.com/en/docs/claude-code) **Skills** that help
leaders (executives, VPs, directors, managers) turn evidence they already have into the
documents they write every cycle: people reviews and status updates. Some skills draft a
document, one rewrites a draft you already have, and one checks a draft against a writing
standard. Every skill shares one set of house rules, defined once in
[`skills/leadership-writing/house-rules.md`](skills/leadership-writing/house-rules.md). That
file ships as the `leadership-writing` skill so it installs as a sibling of the other skills;
the write-* and rewrite skills read it from `../leadership-writing/house-rules.md`.

| Skill | What it does |
|---|---|
| **`/rewrite`** | Takes a draft you already have and rewrites it to follow the house rules (active, show-don't-tell, honest, data-driven, no em-dashes, no hedging), fixing grammar, spelling, and punctuation along the way. It changes how the passage reads, never what it claims: every fact, metric, and link must already be in the input, and it invents nothing. |
| **`/rewrite-and-validate`** | The same rewrite, then a self-validation loop that checks the result against the writing checklist and re-rewrites until it passes, running a minimum of two validation passes before returning the draft. |
| **`/validate-writing`** | Checks a finished draft against a writing checklist and returns a pass/fail verdict with specific, quotable fixes. Run it after drafting, or in a loop until the draft passes. It reports; it does not rewrite. Edit [`skills/validate-writing/checklist.md`](skills/validate-writing/checklist.md) to encode exactly how you want documents written. |
| **`/write-promo-doc`** | Writes a narrative promotion case, including a candid "reasons not to promote" section. |
| **`/write-talent-card`** | Writes a per-person calibration card. |
| **`/write-work-summary`** | Writes a Summary / Timeline / Task / Challenges / Action / Result / Artifacts document. |
| **`/write-exec-update`** | Writes a leadership status update: an overall line, per-section RED/YELLOW/GREEN status with a projected recovery date when RED, near-term milestones, top risks, and known gaps. |
| **`leadership-writing`** | Shared foundation, not invoked directly. Holds `house-rules.md`, the single source of truth for the shared voice that every skill above reads, and `org-profile.md`, the neutral defaults for every organisation-specific word (what principles are called, rating and level labels). Ships as a skill so `npx skills add` installs it alongside the others. |

## What these are (and are not)

These skills handle the **writing**, not the plumbing. You supply the evidence (projects,
metrics, links, a proposed rating, a level rubric); the drafting skills produce a
well-structured document in a consistent, honest manager voice, and the checking skills
grade or tighten a draft against the same standard.

They do **not** publish anywhere, and most do not fetch data. The exception is
`/write-promo-doc`: when you supply links to artifacts (design docs, CRs, OpsWins,
tickets), it fetches them to verify your claims before writing, and surfaces any
discrepancy rather than silently trusting or overwriting your summary. Every other skill
stays purely a writer: pair it with whatever tools you already use to gather evidence (a
docs system, a task tracker, chat search) and to share the result. The skills stay
agnostic to your company, your rating scale, and your career ladder.

## Guarantees built into the writing

- No em-dashes.
- No fabricated metrics, quotes, links, or reviewers. Unverified items carry an
  "(unverified)" label, and projected or test figures stay distinct from realized results.
- Balanced output: promotion docs always include a candid, evidence-based "reasons not to
  promote" section, and talent cards always include growth areas.
- Peer feedback stays as `[TO BE COLLECTED]` placeholders for you to fill through your own
  process.

## Your organisation's vocabulary

The skills never hard-code a company's words. `skills/leadership-writing/org-profile.md` holds
neutral defaults (`core values`, `Rating History`, `a senior level`). To use your own, pass a
profile with the same headings in the request (or a path to one). An automation that wraps these
skills should pass it on every call rather than edit the installed copy.

## Validation is built in

Every writer skill (`write-*`, `rewrite`) runs `validate-writing` on its own draft in gate mode,
applies the fixes, and repeats: at least two passes, at most five. Unresolved blockers surface in a
closing `**Known Gaps**` note, never silently. `rewrite-and-validate` remains for callers that want
the loop named explicitly. `scripts/check.sh` (also the pre-commit hook, `git config core.hooksPath
.githooks`) verifies these invariants and that no company-specific term enters the repository; see
[evals/README.md](evals/README.md).

## Install

`npx skills add ivikash/Leadership-Writing-Skills`

## Use

Invoke a skill and pass it the evidence. For the promotion doc, also pass a level rubric
(copy and fill in
[`skills/write-promo-doc/rubric-TEMPLATE.md`](skills/write-promo-doc/rubric-TEMPLATE.md)).

```
/write-work-summary <paste or reference the engineer's projects, metrics, artifact links>
```

To draft, then check: run a `write-*` skill, then `/validate-writing` in its gate mode,
and apply the quoted fixes until the draft passes. To tighten a draft you already have,
run `/rewrite`, or `/rewrite-and-validate` when you want the rewrite checked before it
comes back.

You can also let an automation gather the evidence first and then hand it to a skill to
write. See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for that pattern.

## License

MIT. See [LICENSE](LICENSE).
