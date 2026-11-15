# Glossary (neutral defaults)

The writing skills and the validator read this file for every organisation-specific word:
what your company calls its values or principles, how it labels performance ratings, and how
it names levels. The skills themselves never hard-code these. A caller overrides any value by
supplying an glossary with the request (a pasted block, or a path to a file with the same
headings). When no override is supplied, the defaults below apply and the output reads in
neutral language that fits any company.

Keep every value short. The skills substitute them verbatim into prose.

## principles

- **name**: `core values` (what your organisation calls the behaviours it evaluates against,
  for example `Leadership Principles`, `Operating Principles`, `Values`)
- **list**: none supplied (when a list is supplied, writers may only cite principles from it)
- **example_1**: `Ownership and Delivery` (used only in instructions as an example anchor)
- **example_2**: `Simplicity`
- **cite_per_statement**: `false` (`true` puts one principle in bold brackets at the end of
  the statement it supports; `false` closes each capability section with one roll-up line,
  `<name> demonstrated: X, Y, Z`)

## rating

- **history_label**: `Rating History` (the name of the table that lists past ratings)
- **scale**: none supplied (when supplied, list highest to lowest, for example
  `Exceptional > Strong > Solid > Developing > Low`)
- **top**: `the top rating` (used in instructions as an example value)
- **ineligible_label**: `Ineligible` (how the caller marks a person with no rating this cycle)

## levels

- **mid**: `a mid-level` (the level whose promotion case needs 3 to 5 evidence examples)
- **senior**: `a senior level` (from here up, 4 to 6 evidence examples)
- **title_format**: `{LEVEL} - {NAME}` (document title for a talent card)

## roles

- **senior_technical_owner**: `senior technical owner` (the role that sets direction on a
  project without owning the implementation; attribution rules name it)
