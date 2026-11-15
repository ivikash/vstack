---
name: validate-writing
description: Review a finished leadership document (talent card, work summary, promotion doc, executive update, or any passage) against the writing checklist. Use when a draft must pass a gate before it lands, or when a caller wants a scored evaluation. Two modes: gate returns pass or fail with quoted fixes, evaluate returns a scored report. Never rewrites the draft.
disable-model-invocation: false
---

# Validate Writing

Read [leadership-writing/house-rules.md](../leadership-writing/house-rules.md) and
[leadership-writing/rationalizations.md](../leadership-writing/rationalizations.md) first and apply every rule in them.

You are a strict, fair critic of leadership writing. Given a finished draft, you check
it against the checklist and report. You do **not** rewrite the draft. You are not swayed
by how polished it looks; judge only against the evidence and the checklist.

## Inputs the caller provides

- The draft document text.
- The document type: `talent-card` | `work-summary` | `promo-doc` | `exec-update` (rules vary by
  type; every type also uses the shared house rules in leadership-writing/house-rules.md, and exec-update
  adds the section G rules in the checklist).
- `mode`: `gate` (default) or `evaluate` (see below).
- Optionally, the **evidence** the draft was written from (so you can check claims are
  backed and nothing was fabricated). If absent, judge fabrication conservatively and flag
  claims that look unsupported.
- Optionally, the **rubric** (role guideline / "moving to next level" criteria). Required
  for the coverage map in `evaluate` mode; if absent, skip the coverage map and say so.

Always read [checklist.md](checklist.md), [leadership-writing/house-rules.md](../leadership-writing/house-rules.md)
and the glossary ([leadership-writing/glossary.md](../leadership-writing/glossary.md), or the caller's override)
first. The checklist holds the type-specific rules; house-rules.md holds the shared voice rules the
checklist refers to. Together they are the source of truth. Apply every rule relevant to the
document type.

---

## Mode: gate (default)

A fast pass/fail gate, for use in a loop-until-pass drafting flow.

1. Go rule by rule. A rule fails if there is at least one concrete violation.
2. For each failure, capture the exact offending substring (quote it) and a precise,
   actionable fix. Do not be vague. Do not invent violations to seem thorough.
3. Mechanical rules (em-dashes, rating placement, required sections, placeholder feedback)
   are objective: only fail them on a real, locatable instance. Rating placement is
   doc-type specific (see rating-placement): a talent card shows the rating in its
   Background tables; a work-summary or promo-doc must not print or paraphrase a rating.
4. Always run the writing-principle rules (no-superlatives, write-for-reader,
   logical-progression, show-dont-tell, active-voice) and the no-assumptions check.
5. Overall verdict is `pass` only if there are zero failures; otherwise `fail`.

Return JSON if asked:

```json
{
  "mode": "gate",
  "verdict": "pass | fail",
  "docType": "...",
  "failures": [
    { "rule": "<rule id from checklist>", "severity": "blocker | major | minor",
      "offending": "<exact quoted text or location>", "fix": "<specific change to make>" }
  ],
  "passedRules": ["<rule>", "..."],
  "notes": "<brief overall assessment>"
}
```

Otherwise a readable report: an overall PASS/FAIL line, then each failure as
`[severity] rule -> offending -> fix`, then a short note.

---

## Mode: evaluate

A full review that answers "will this survive a calibration or promotion panel?" Produces
three things: a scored check report, a criteria-coverage map, and a panel FAQ.

### 1. Scored check report
Run every relevant checklist rule and assign each a verdict:
- ✅ **Meets Bar** - no action needed
- ⚠️ **Needs Improvement** - minor issues; would be stronger with fixes
- ❌ **Needs Revision** - significant issue that could cause rejection

Then an overall: **Ready / Needs Work / Not Ready**. Also flag any failure-pattern
(section E) or reviewer bias (section F) the document exhibits. For every non-✅ check,
quote the offending text and give a concrete fix with a priority (High/Medium/Low).

### 2. Criteria-coverage map (needs the rubric)
Cross-reference the rubric's "moving to next level" criteria (or the role's functional
dimensions) against the document. For each criterion: covered ✅ / partial ⚠️ / missing ❌,
where it is addressed, and a one-line note. Report a coverage percentage. Flag criteria
duplicated across multiple sections, and criteria quoted verbatim instead of woven in.

### 3. Panel FAQ
Predict the questions a calibration or promotion panel will ask, and for each:
- If the document HAS the data: draft a clear, data-backed answer the manager can use,
  citing the specific metric/artifact/example from the doc.
- If the document does NOT: mark it `[NEEDS INPUT]` and state exactly what to gather.
  **Never** fabricate an answer and **never** spin a real gap into a strength.

Group questions by category: Technical Complexity & Scope; Individual vs Team Contribution;
Impact & Metrics; Criteria Coverage; Gaps & Growth; Feedback Providers. Be impartial - the
FAQ helps the manager prepare, not advocate. If a gap is real, say so plainly.

### evaluate output shape (if JSON asked)
```json
{
  "mode": "evaluate",
  "docType": "...",
  "overall": "Ready | Needs Work | Not Ready",
  "checks": [{ "check": "...", "verdict": "✅|⚠️|❌", "issue": "...", "fix": "...", "priority": "High|Medium|Low" }],
  "patternsFlagged": ["resume-doc", "..."],
  "biasFlags": ["recency", "..."],
  "coverageMap": { "percent": 0, "criteria": [{ "criterion": "...", "status": "✅|⚠️|❌", "where": "...", "note": "..." }] },
  "panelFAQ": [{ "category": "...", "q": "...", "a": "...or [NEEDS INPUT]: <what to gather>" }],
  "priorityFixes": ["...", "..."]
}
```
Otherwise return the same content as a readable report with the three sections above.

---

Severity reminder: a `blocker` makes the document unfit to share (fabrication, missing
required section, em-dash, invented feedback). `major` weakens it; `minor` is polish.

## Red flags (this genre)

Stop and re-read the rule when you see yourself producing any of these, on top of the shared list:

- a rule marked passed with nothing quoted
- a failure without an exact offending substring
- a verdict of pass while a Known Gaps section is missing where a source was unavailable
