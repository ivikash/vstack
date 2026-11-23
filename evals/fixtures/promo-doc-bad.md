# Dana Whitfield - Promotion Document

Fictional candidate, team, projects, numbers, links and reviewers. This file is the red sample: it carries every class of mistake a reviewer marked on a real document, re-created with invented content. `scripts/promo-lint.py` must fail on it and `evals/results/` records which rule catches which class.

- Employee Name: Dana Whitfield
- Manager Name: Noor Haddad
- Current Title: Engineer II
- Proposed Title: Senior Engineer
- Time in Current Level: 26 months

## Scope of Role

Harbor Telemetry owns the ingest path for 1,400 internal customers; the team runs 6 services across 9 regions. A Senior Engineer owns a service end to end.

## Why now?

Dana joined Harbor Telemetry in 2024 and started on the Lighthouse Parser, which was the first project. Then came the Breakwater Credentials work during the regional event, and after that the Seawall Schema project, and most recently the Quayside Tagging campaign. Each project built on the one before it and Dana grew with each one. Dana demonstrated exceptional ownership across the Lighthouse Parser, Breakwater Credentials, Seawall Schema and Quayside Tagging, and the team relies on Dana for the hardest problems.

**Lighthouse Parser shipped early and customers love it.** Dana also worked on the Pier Alarm Cleanup and wrote an onboarding guide.

## Evidence

### Lighthouse Parser: Ambiguity

Dana designed and built the Lighthouse Parser end-to-end after a customer asked for a new log format. Dana wrote the parser in CR-4821 and the console changes in CR-4836, aligning with the console team along the way. Dana led the launch across all regions, and before that evaluated a vendor library, rejected it because of its licence, measured the regex path at 9 times the latency budget, and wrote a streaming parser instead, which is the kind of judgement the next level expects.

The parser launched in [date] and is used by [N customers] today. Adoption is 0.4% and trending up. `TODO: confirm launch date`.

> "Dana turned a one-line complaint into a definition two teams signed.", Rhea Castellan, Principal Engineer

### Breakwater Credentials: Problem Complexity

**Headline** Fixed the credential storm during the regional event.

Dana noticed that credential fetches were failing during the 10/20/2025 regional event and immediately started debugging. The fleet was large and the failure rate was high.

Dana proposed and drove the shared credential cache, architected the jittered refresh, and owned the rollout to both teams. See https://example.com/reviews/4902 and https://example.com/reviews/4917.

Failures dropped significantly and the Identity team was happy.

### Seawall Schema: Ambiguity

**Headline** Replaced the schema mappings.

By June 2026 downstream tables needed typed schemas from the pattern-based parsers that Harbor Telemetry runs for 180 pipelines. The problem was that three different builders had, over the course of two years, each written a schema mapping by hand for their own part of the system, and the three mappings disagreed with each other in 27 separate places, which produced three mismatch incidents in a single quarter. The cause of the mismatches was not obvious to anyone on the team, because the same field data lived in three different forms: as flat keys inside the pattern library, as nested records in the parser output, and as column definitions in the table definitions, and each of those three forms was owned by a different builder who had a different understanding of what the canonical shape was supposed to be. Nobody owned the problem as a whole, and each builder's tests passed against their own copy, which is why the mismatches only showed up downstream when a customer's query returned the wrong type for a column that had looked correct in every unit test along the way. The team had discussed the problem in two design reviews without agreeing on an owner, and the manager had raised it in three consecutive planning meetings as a risk that nobody had picked up, partly because each of the three builders believed their own mapping was the correct one and the other two were the ones that needed to change. The downstream consumers, meanwhile, had started to write their own correction layers on top of the tables, which added a fourth copy of the mapping to the system and made the next incident harder to trace than the one before it.

Dana owned the single derivation, asked for by the manager after the third mismatch incident in [ticket 2455](https://example.com/tickets/2455), and also took on the migration of every pipeline that depended on any of the three mappings, which included the 180 pipelines themselves and the 12 downstream correction layers that consumers had written in the meantime.

Dana traced all three forms back to the pattern library and wrote an algorithm that derives the typed schema from the pattern alone, documented in [the schema derivation note](https://example.com/docs/tidewater-derivation), which runs to 11 pages and covers every edge case the three mappings had handled differently, including the 27 known mismatches and 9 further cases that nobody had noticed because they had not yet produced an incident. Dana considered keeping the hand-written mappings behind a feature flag so that the migration could be rolled back per pipeline, and rejected that option because the flag would have kept all three sources alive indefinitely and the team would never have deleted them. Dana then considered generating the mappings once and checking them in as code, and rejected that too because a generated file is a fourth copy the moment the pattern changes. Dana walked the two other builders through the derivation in two sessions before deleting their mappings, shipped the derivation in [review 5010](https://example.com/reviews/5010), and migrated the 180 pipelines in 4 batches of 45, pausing after each batch for a week to watch the downstream tables for type errors, of which there were none in any of the four batches. The 12 downstream correction layers were removed by their owners after Dana sent each of them a diff showing that the corrected and the derived schema were identical for their tables.

2,300 lines of mappings were deleted by 09/18/2026 and all 180 pipelines infer their schema, and the 27 mismatches are gone, and the 12 correction layers are gone too, and there has been no mismatch incident since; the downstream team said thank you.

> "One source of truth where there were three.", Felix Marchetti, Senior Engineer

### Quayside Tagging: Execution

**Headline** Tagging shipped for all 4 resource types.

A platform campaign required tagging by 06/30/2026 — Harbor Telemetry's 4 types did not support it.

Dana fixed the race and shipped tagging for the 4 types.

Dana took over the campaign.

All 4 types supported tagging on 06/28/2026.

> "Dana did the boring work nobody else would.", Noor Haddad, Engineering Manager

### Lighthouse Parser: Impact

**Headline** Lighthouse Parser parses 40 million events a day for 310 customers.

After the launch of the Lighthouse Parser, which Dana designed and built end-to-end, customers in the factory machines segment adopted it faster than any format before it. Dana had written the format definition, got two teams to sign it, built the streaming parser and the two console changes, and launched in all 9 regions three weeks ahead of the committed date, as told above, and the adoption numbers followed from that launch.

Dana owned adoption tracking.

Dana built a dashboard.

40 million events a day for 310 customers by 10/31/2026.

> (TO BE COLLECTED: quote from the product manager)

Core values demonstrated: Ownership and Delivery.

## Best reasons not to promote

### Cultivating proactive strategic initiative and opportunity identification [Ownership]

Across Lighthouse, Breakwater, Seawall and Quayside, Dana executed well once directed. But the leverage play on the team's repetitive manifest tests had to be pointed out before Dana automated it. Dana does not propose initiatives.

### Becoming the operational excellence champion for the team

Dana should become the team's operational excellence champion and own the Sev2 reduction initiative, which would demonstrate the next level. [Plan: TBD]

## Feedback

### Rhea Castellan, Principal Engineer

Relationship: reviewer on two designs. Best reasons to promote: Dana owns problems that cross teams. Best reasons not to promote: Dana's documents are long, the derivation note ran to 11 pages and I had to ask for a 3-page version before the review could proceed.

Sources: used sample evidence; unavailable none
