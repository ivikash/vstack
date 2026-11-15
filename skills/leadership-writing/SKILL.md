---
name: leadership-writing
description: Shared house rules that the leadership-writing skills read (talent card, work summary, promo doc, executive update, rewrite, validate). Holds the single source of truth for HOW the writing reads. Not invoked directly - the write-* and rewrite skills read house-rules.md from here.
---

# Leadership Writing (shared foundation)

This skill exists to carry the shared house rules so every leadership-writing skill can read
it from a sibling directory. It is not meant to be invoked on its own.

The single source of truth for HOW the writing reads lives in [house-rules.md](house-rules.md).
Every writing skill (talent card, work summary, promo doc, executive update, and the rewrite
skills) and the validator read that file and apply it. Edit a voice rule there; do not restate
it inside a skill.

Organisation-specific words live in [org-profile.md](org-profile.md): what the organisation calls
its principles, how ratings and levels are labelled, what the direction-setting technical role is
called. The skills reference these as `principles.name`, `rating.top`, `levels.mid` and so on,
and substitute the profile's values. The shipped file holds neutral defaults so the skills work
for any company. A caller overrides it by pasting a profile with the same headings into the
request, or by naming a file path. Automation that wraps these skills should pass the profile on
every call rather than editing the installed copy, which an installer may overwrite.
