# Dana Whitfield - Promotion Document

Fictional candidate, team, projects, numbers, links and reviewers. This file is the green sample for `scripts/promo-lint.py` and the promo-doc rules in `skills/validate-writing/checklist.md`. Nothing in it describes a real person or organisation.

- Employee Name: Dana Whitfield
- Manager Name: Noor Haddad
- Current Title: Engineer II
- Proposed Title: Senior Engineer
- Time in Current Level: 26 months

## Scope of Role

Harbor Telemetry owns the ingest path that turns raw device logs into queryable tables for 1,400 internal customers. The team runs 6 services across 9 regions, receives 2.1 billion events a day, and carries a one-week on-call rotation shared by 7 builders. A Senior Engineer on this team owns a service end to end, sets the design for problems that cross two or more services, and is the reviewer other builders ask before a risky change ships.

## Why now?

Dana's case rests on three wins, ordered by impact, then ambiguity, then recency, the order the manager set for this candidate.

**Breakwater Credentials cut credential-fetch failures from 4,200 a day to 11 a day during a regional event** (Problem Complexity). Dana traced a failure nobody owned across two teams' code, ruled out the retry fix everyone expected, and shipped a cache that the partner team adopted for its own fleet in March 2026.

**Lighthouse Parser shipped to 9 regions 3 weeks ahead of the committed date and parses 40 million events a day for 310 customers** (Ambiguity). The ask arrived as one customer's complaint with no format defined. Dana wrote the definition, got two teams to agree to it, and built the parser without a prior console change to copy from.

**Tidewater Schema cut the schema sources from 3 to 1 and now generates the schema for 180 pipelines** (Problem Complexity). Dana found the same data held in three shapes and replaced all three with one derivation, the most recent of the three wins, finished in September 2026.

Beyond these, Dana completed the Quayside Tagging campaign for the team's 4 resource types on time, closed 12 of the team's 19 noisy alarms in one quarter, and wrote the onboarding guide that 3 new builders used in 2026. Each is told once below.

## Evidence

### Lighthouse Parser: Ambiguity

**Headline** Shipped to 9 regions 3 weeks ahead of the committed date, 40 million events a day for 310 customers.

**Situation** In November 2025 a customer running factory equipment asked Harbor Telemetry to accept a vendor log format the team had never seen. The ticket said "support our logs" and nothing else: no sample files, no field list, no agreed owner. From the customer's view the product was broken for their whole fleet, and the quarterly roadmap had promised format coverage for that industry. What was undefined was the format itself, and which of two teams (ingest or console) would own the user-facing change. Dana asked the customer for samples the same week rather than wait for a specification nobody was writing.

**Task** Dana owned the definition and the ingest side, asked for by the product manager in [ticket 2210](https://example.com/tickets/2210). Nobody owned the console side when Dana started. Ownership: originated the format definition, executed both halves of the parser, operated the launch.

**Action** Dana obtained 3 sample files from the customer and wrote a one-page definition of the format with 14 fields, then ruled out the existing regex path after measuring it at 9 times the latency budget on a 1 MB file. Dana evaluated a vendor library and rejected it because its licence barred redistribution, then wrote a streaming parser in [review 4821](https://example.com/reviews/4821). Dana reached out to the console team, agreed on a shared field list in [the format definition](https://example.com/docs/lighthouse-format), and wrote the 2 console changes in [review 4836](https://example.com/reviews/4836) so the launch would not wait on another team's queue. A strong Engineer II would have built the parser to a given definition, not written the definition and got two teams to sign it.

**Result** Lighthouse Parser launched in all 9 regions on 02/12/2026, 3 weeks ahead of the committed date. By 10/31/2026 it parsed 40 million events a day for 310 customers. The console team reused the field list for its next two formats.

> "Dana turned a one-line complaint into a definition two teams signed, and then built both halves so nobody waited. That is what I expect from a senior engineer.", Rhea Castellan, Principal Engineer

Core values demonstrated: Ownership and Delivery, Simplicity.

### Breakwater Credentials: Problem Complexity

**Headline** Credential-fetch failures down from 4,200 a day to 11 a day under regional load.

**Situation** On 10/20/2025 a regional event pushed the 8,000-host processing fleet to refresh credentials at once. 4,200 fetches a day failed, and 300 customers saw delayed data. The cause was not obvious: the token path crossed code owned by Harbor Telemetry and by the Identity team, and each team's dashboard showed its own half as healthy. The expected fix, more retries, had already been tried once and made the spike worse. Dana pulled both teams' dashboards side by side before anyone had agreed whose problem it was.

**Task** Dana was asked by the on-call lead to own the root cause and the fix across both code bases, in [ticket 2381](https://example.com/tickets/2381). Ownership: originated the cache design, executed the fix in both code bases, the Identity team operated its own rollout.

**Action** Dana reproduced the spike in a test region with 400 hosts and showed that retries amplified it by 3 times. Dana read the Identity team's client and found that every host fetched independently, then ruled out a per-host backoff because it only delayed the storm. Dana proposed a shared cache with jittered refresh in [the credential cache design](https://example.com/docs/breakwater-design), reviewed it with the Identity team's senior owner, and shipped it in [review 4902](https://example.com/reviews/4902) and [review 4917](https://example.com/reviews/4917). A strong Engineer II would have added retries inside the team's own code, not disproved the fix with a number and changed another team's client.

**Result** Failures fell from 4,200 a day to 11 a day by 12/05/2025, and the next regional event on 02/03/2026 passed with no customer-visible delay. The Identity team adopted the cache for its own 2,000-host fleet in March 2026.

> "The retry fix was the obvious one and Dana proved it was wrong with a number before anyone argued.", Owen Faraday, Senior Engineer

### Tidewater Schema: Problem Complexity

**Headline** Schema sources cut from 3 to 1, 2,300 lines of hand-written mappings deleted across 180 pipelines.

**Situation** By June 2026 downstream tables needed typed schemas from pattern-based parsers. Three builders had each written a mapping by hand, and the three disagreed in 27 places. The cause was not obvious: the same field data lived in the pattern library, the parser output, and the table definitions, and each was owned by a different builder. Dana diffed the three mappings before proposing anything.

**Task** Dana owned the single derivation, asked for by the manager after the third mismatch incident in [ticket 2455](https://example.com/tickets/2455). Ownership: originated the derivation, executed the migration, operated the 4 batches.

**Action** Dana traced all three forms to the pattern library and wrote an algorithm that derives the typed schema from the pattern alone, documented in [the schema derivation note](https://example.com/docs/tidewater-derivation). Dana rejected keeping the hand-written mappings behind a flag because the flag would have kept all three sources alive, and walked the two other builders through the derivation before deleting their mappings. Dana shipped it in [review 5010](https://example.com/reviews/5010) and migrated the 180 pipelines in 4 batches. A strong Engineer II would have fixed the 27 mismatches one by one, not removed two of the three sources.

**Result** 2,300 lines of mappings were deleted by 09/18/2026. All 180 pipelines infer their schema, and the 27 mismatches are gone.

> "One source of truth where there were three. Dana saw the shape of the problem before writing a line.", Felix Marchetti, Senior Engineer

Core values demonstrated: Ownership and Delivery, Simplicity.

### Quayside Tagging: Execution

**Headline** Tagging shipped for all 4 resource types 2 days ahead of the campaign date, deletion errors down from 90 a week to 0.

**Situation** In 2026 a platform campaign required every resource type to support tagging by 06/30/2026. Harbor Telemetry's 4 types did not. The first attempt by another builder produced 90 deletion errors a week for customers because a tag write raced the delete path, and the campaign owner was asking the team weekly for a date. Dana asked for the rolled-back change and the error logs on the day the handover happened.

**Task** Dana took over the campaign for the team's 4 types in [ticket 2502](https://example.com/tickets/2502) after the first attempt was rolled back. Ownership: executed and operated the campaign, the platform team originated the requirement.

**Action** Dana ruled out the first hypothesis, a permissions gap, by reproducing the error with full permissions. Dana found the race in the delete handler, fixed it in [review 5088](https://example.com/reviews/5088), and then shipped tagging for the 4 types in [review 5101](https://example.com/reviews/5101), testing each partition before the campaign date. A strong Engineer II would have retried the permissions fix, not reproduced the race first.

**Result** All 4 types supported tagging on 06/28/2026, 2 days before the deadline. Deletion errors dropped from 90 a week to 0 and stayed there through October 2026.

> (TO BE COLLECTED: quote from the campaign owner)

Core values demonstrated: Ownership and Delivery.

### Pier Alarm Cleanup: Impact

**Headline** Pages down from 45 to 18 a week, 12 of 19 noisy alarms closed in one quarter.

**Situation** In Q1 2026 the on-call rotation received 45 pages a week, and 19 alarms fired without a customer-facing cause. Builders had started to ignore pages, which is how a real incident on 01/14/2026 went unnoticed for 40 minutes. Dana pulled the 90-day page history the week after that incident.

**Task** Dana volunteered to own the cleanup and the manager agreed in the team's quarterly plan ([the alarm review](https://example.com/docs/pier-alarm-review)). Ownership: originated the proposal, executed the cleanup, operates the on-call guide.

**Action** Dana classified all 19 alarms by whether a customer could tell the difference, deleted 7, retuned 5 with data from 90 days of history, and rewrote the on-call guide so each remaining alarm names its first check, in [review 5130](https://example.com/reviews/5130). A strong Engineer II would have retuned the alarms assigned to them, not decided which 7 the team could live without.

**Result** Pages fell from 45 a week to 18 a week by 03/31/2026, a 60 percent drop. No incident has gone unnoticed since. (TO BE CONFIRMED)

> "Our on-call stopped dreading the phone. Dana did the boring work nobody else would.", Noor Haddad, Engineering Manager

Core values demonstrated: Ownership and Delivery.

### Onboarding Guide: Scope and Influence

**Headline** 3 new builders shipped their first change within 2 weeks instead of 6.

**Situation** In 2025 a new builder on Harbor Telemetry took 6 weeks on average to ship a first change, because the setup steps lived in 4 people's heads. Nobody had asked for a guide. Dana started writing one while onboarding the next builder.

**Task** Dana wrote the guide without being asked and the manager made it the team standard in [the onboarding guide](https://example.com/docs/onboarding-guide). Ownership: originated and executed the guide, operates it for each new builder.

**Action** Dana recorded every step while onboarding a new builder in January 2026, turned the 31 steps into a checked script in [review 5155](https://example.com/reviews/5155), and reviewed the 3 new builders' first changes. A strong Engineer II would have written notes for themselves, not a script the team and two other teams run.

**Result** The 3 builders who joined in 2026 shipped their first change in 11, 9 and 14 days. Two other teams copied the guide format in Q3 2026.

> (TO BE COLLECTED: quote from a builder onboarded in 2026)

Core values demonstrated: Ownership and Delivery.

## Best reasons not to promote

### Proposing the next leverage play before being asked

**Pattern** Dana executes fully once a problem is named, as Breakwater Credentials and Quayside Tagging show.

**Gap** What Dana does not yet do is propose the leverage play first: on 05/06/2026 Owen Faraday had to point out that the team's repeated manifest tests could be automated before Dana took it on, and Dana then built it well.

**Also seen by** Rhea Castellan saw the same pattern in the Q2 2026 design review.

**Does not block** This does not block Senior Engineer because the Pier Alarm Cleanup was Dana's own proposal and the role guideline asks for owning problems, which Dana does.

**Next** As a Senior Engineer I want Dana to bring one unprompted proposal per quarter. Plan: a monthly review of the team's toil list that Dana owns from November 2026.

### Writing shorter decision documents

**Pattern** Dana's design documents are complete, as the credential cache design and the schema derivation note show.

**Gap** What Dana does not yet do is write for a reader with five minutes: on 08/12/2026 Felix Marchetti asked for the 11-page derivation note to be cut to 3 pages before the review could proceed.

**Also seen by** Noor Haddad raised the same point in the July 2026 one-on-one.

**Does not block** This does not block Senior Engineer because both documents reached the right decision and the reviewers' changes were to length, not substance.

**Next** As a Senior Engineer I want Dana to lead with the decision and the one number that supports it. Plan: a senior engineer reviews Dana's next two documents for length before they go out.

## Feedback Summary

| Provider | Relationship | Support Promotion |
|---|---|---|
| (TO BE COLLECTED) | (TO BE COLLECTED) | (TO BE COLLECTED) |
| (TO BE COLLECTED) | (TO BE COLLECTED) | (TO BE COLLECTED) |

Formal feedback is to be solicited through the organisation's own process.

Sources: used sample evidence; unavailable none
