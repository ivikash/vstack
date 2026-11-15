---
name: leadership-writing
description: Shared house rules, glossary defaults and the rationalizations table that every leadership-writing skill reads (talent card, work summary, promo doc, executive update, rewrite, validate). Use when a writing or validating skill tells you to read house-rules.md, glossary.md or rationalizations.md from here. Not invoked on its own.
---

# Leadership Writing (shared foundation)

This skill exists to carry the shared house rules so every leadership-writing skill can read
it from a sibling directory. It is not meant to be invoked on its own.

The single source of truth for HOW the writing reads lives in [house-rules.md](house-rules.md).
Every writing skill (talent card, work summary, promo doc, executive update, and the rewrite
skills) and the validator read that file and apply it. Edit a voice rule there; do not restate
it inside a skill.

Organisation-specific words live in [glossary.md](glossary.md): what the organisation calls
its principles, how ratings and levels are labelled, what the direction-setting technical role is
called. The skills reference these as `principles.name`, `rating.top`, `levels.mid` and so on,
and substitute the profile's values. The shipped file holds neutral defaults so the skills work
for any company. A caller overrides it by pasting a profile with the same headings into the
request, or by naming a file path. Automation that wraps these skills should pass the profile on
every call rather than editing the installed copy, which an installer may overwrite.
