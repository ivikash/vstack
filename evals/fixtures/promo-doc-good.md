# Dana Whitfield - Promotion Document

Fictional candidate, team, projects, numbers, links and reviewers. This file is the green sample for `scripts/promo-lint.py` and the promo-doc rules in `skills/validate-writing/checklist.md`. Nothing in it describes a real person or organisation.

- Employee Name: Dana Whitfield
- Manager Name: Noor Haddad
- Current Title: Engineer II
- Proposed Title: Senior Engineer
- Time in Current Level: 26 months

## Scope of Role

Harbor Telemetry owns the ingest path that turns raw device logs into queryable tables for 1,400 internal customers. The team runs 6 services across 9 regions, receives 2.1 billion events a day, and carries a one-week on-call rotation shared by 7 builders.

An Engineer II on this team owns a component inside one service, ships changes a senior engineer has scoped, carries the on-call rotation, and reviews changes to the code they own.

A Senior Engineer on this team owns a service end to end, sets the design for problems that cross two or more services, is the reviewer other builders ask before a risky change ships, and brings the next problem to the team before anyone assigns it.

## Why now?

Dana has 26 months in level as an Engineer II after 14 months as an Engineer I on the same team. In that time she has delivered across three initiatives, **Breakwater Credentials**, **Lighthouse Parser** and **Tidewater Schema**, while carrying the team's on-call. On **Breakwater Credentials**, she traced a failure nobody owned across two teams' code, disproved the retry fix with a reproduction, and shipped a shared cache that cut credential-fetch failures by **99.7% (from 4,200 a day to 11 a day)**, which the Identity team adopted for its own 2,000-host fleet in March 2026. On **Lighthouse Parser**, she turned one customer's one-line complaint into a 14-field format definition two teams signed, wrote both the ingest and the console halves so neither team waited on the other, and launched in all 9 regions 3 weeks ahead of the committed date, parsing **40 million events a day for 310 customers** by 10/31/2026. On **Tidewater Schema**, she found the same field data held in three hand-written shapes, replaced all three with one derivation, and cut the schema sources **from 3 to 1** across 180 pipelines, deleting 2,300 lines of mappings. On operations she classified all 19 of the team's noisy alarms by whether a customer could tell the difference and closed 12 of them in one quarter, cutting pages by 60% (from 45 to 18 a week), and she carries one of the team's 7 on-call slots. She wrote the onboarding script the 3 builders who joined in 2026 used to ship their first change in 11, 9 and 14 days instead of the 6-week average before it. Across these 3 initiatives she shipped in 2 teams' codebases and 4 services in 26 months.

## Evidence

### Lighthouse Parser: Ambiguity

**Headline** Shipped to 9 regions 3 weeks ahead of the committed date, 40 million events a day for 310 customers.

**Q4 2025, Lighthouse Parser:** a customer running factory machines asked Harbor Telemetry to accept a vendor log format the team had never seen. The ticket said "support our logs" and nothing else: no sample files, no field list, no agreed owner. From the customer's view the product was broken for their whole fleet, and the quarterly roadmap had promised format coverage for that industry. What was undefined was the format itself, and which of two teams (ingest or console) would own the user-facing change. Dana asked the customer for samples the same week rather than wait for a specification nobody was writing.

Dana owned the definition and the ingest side, asked for by the product manager in [ticket 2210](https://example.com/tickets/2210), and took the console side as well when nobody on the console team had picked it up, agreeing the shared field list with that team's two reviewers.

Dana obtained 3 sample files from the customer and wrote a one-page definition of the format with 14 fields, then ruled out the existing regex path after measuring it at 9 times the latency budget on a 1 MB file. She evaluated a vendor library and rejected it because its licence barred redistribution, then wrote a streaming parser in [review 4821](https://example.com/reviews/4821). She reached out to the console team, agreed on a shared field list in [the format definition](https://example.com/docs/lighthouse-format), and wrote the 2 console changes in [review 4836](https://example.com/reviews/4836) so the launch would not wait on another team's queue. A strong Engineer II would have built the parser to a given definition, not written the definition and got two teams to sign it.

Lighthouse Parser launched in all 9 regions on 02/12/2026, 3 weeks ahead of the committed date. By 10/31/2026 it parsed 40 million events a day for 310 customers. The console team reused the field list for its next two formats.

> "Dana turned a one-line complaint into a definition two teams signed, and then built both halves so nobody waited. That is what I expect from a senior engineer.", Rhea Castellan, Principal Engineer

### Breakwater Credentials: Problem Complexity

**Headline** Credential-fetch failures down 99.7% (from 4,200 a day to 11 a day) under regional load.

**Q4 2025, Breakwater Credentials:** on 10/20/2025 a regional event pushed the 8,000-host processing fleet to refresh credentials at once. 4,200 fetches a day failed, and 300 customers saw delayed data. Nobody owned the token path as a whole: it crossed code owned by Harbor Telemetry and by the Identity team, each team's dashboard showed its own half as healthy, and no runbook described how a token travelled between them. The expected fix, more retries, had already been tried once and made the spike worse. Dana pulled both teams' dashboards side by side before anyone had agreed whose problem it was.

Dana was asked by the on-call lead to own the root cause and the fix across both code bases, in [ticket 2381](https://example.com/tickets/2381), and shipped the Identity team's half with that team's senior owner as reviewer, who then ran the rollout on their fleet.

Dana reproduced the spike in a test region with 400 hosts and showed that retries amplified it by 3 times. She read the Identity team's client and found that every host fetched independently, then ruled out a per-host backoff because it only delayed the storm. She proposed a shared cache with jittered refresh in [the credential cache design](https://example.com/docs/breakwater-design), reviewed it with the Identity team's senior owner, and shipped it in [review 4902](https://example.com/reviews/4902) and [review 4917](https://example.com/reviews/4917). Six builders from the two teams were on the incident call, two of them senior engineers, and Dana was the one who disproved the retry fix with the reproduction and changed the other team's client.

Failures fell by 99.7% (from 4,200 a day to 11 a day) by 12/05/2025, and the next regional event on 02/03/2026 passed with no customer-visible delay. The Identity team adopted the cache for its own 2,000-host fleet in March 2026.

> "The retry fix was the obvious one and Dana proved it was wrong with a number before anyone argued.", Owen Faraday, Senior Engineer

### Tidewater Schema: Problem Complexity

**Headline** Schema sources cut from 3 to 1, 2,300 lines of hand-written mappings deleted across 180 pipelines.

**Q2 2026, Tidewater Schema:** by June 2026 downstream tables needed typed schemas from pattern-based parsers. No single source held the schema: three builders had each written a mapping by hand, the three disagreed in 27 places, and nobody owned the problem as a whole. The cause was not obvious because the same field data lived in the pattern library, the parser output and the table definitions, each owned by a different builder. Dana diffed the three mappings before proposing anything.

Dana owned the single derivation, asked for by the manager after the third mismatch incident in [ticket 2455](https://example.com/tickets/2455), and migrated the 180 pipelines with the two builders whose mappings she replaced reviewing each batch.

Dana traced all three forms to the pattern library and wrote an algorithm that derives the typed schema from the pattern alone, documented in [the schema derivation note](https://example.com/docs/tidewater-derivation). She rejected keeping the hand-written mappings behind a flag because the flag would have kept all three sources alive, and walked the two other builders through the derivation before deleting their mappings. She shipped it in [review 5010](https://example.com/reviews/5010) and migrated the 180 pipelines in 4 batches. A strong Engineer II would have fixed the 27 mismatches one by one, not removed two of the three sources.

Dana deleted 2,300 lines of mappings by 09/18/2026, and all 180 pipelines now infer their schema with the 27 mismatches gone. The downstream analytics team now runs its new tables from the derived schema instead of a correction layer.

> "One source of truth where there were three. Dana saw the shape of the problem before writing a line.", Felix Marchetti, Senior Engineer

### Quayside Tagging: Execution

**Headline** Tagging shipped for all 4 resource types 2 days ahead of the campaign date, deletion errors down from 90 a week to 0.

**Q2 2026, Quayside Tagging:** a platform campaign required every resource type to support tagging by 06/30/2026, and Harbor Telemetry's 4 types did not. The first attempt by another builder produced 90 deletion errors a week for customers because a tag write raced the delete path, no test covered the delete path, and the campaign owner was asking the team weekly for a date. Dana asked for the rolled-back change and the error logs on the day the handover happened.

Dana took over the campaign for the team's 4 types in [ticket 2502](https://example.com/tickets/2502) after the first attempt was rolled back, working from the requirement the platform team had written and with the first builder reviewing the fix.

Dana ruled out the first hypothesis, a permissions gap, by reproducing the error with full permissions. She found the race in the delete handler, fixed it in [review 5088](https://example.com/reviews/5088), and then shipped tagging for the 4 types in [review 5101](https://example.com/reviews/5101), testing each partition before the campaign date. A strong Engineer II would have retried the permissions fix, not reproduced the race first.

All 4 types supported tagging on 06/28/2026, 2 days before the deadline, and deletion errors dropped from 90 a week to 0 and stayed there through October 2026. The platform team's campaign guide now points other teams at Dana's race fix as the pattern to copy.

> (TO BE COLLECTED: quote from the campaign owner)

### Pier Alarm Cleanup: Impact

**Headline** Pages down 60% (from 45 to 18 a week), 12 of 19 noisy alarms closed in one quarter.

**Q1 2026, Pier Alarm Cleanup:** the on-call rotation received 45 pages a week, and 19 alarms fired without a customer-facing cause. No alarm had an owner or a documented first check, builders had started to ignore pages, and a real incident on 01/14/2026 went unnoticed for 40 minutes. Dana pulled the 90-day page history the week after that incident.

Dana volunteered to own the cleanup and the manager agreed in the team's quarterly plan ([the alarm review](https://example.com/docs/pier-alarm-review)), with the on-call lead agreeing the delete list before any alarm went.

Dana classified all 19 alarms by whether a customer could tell the difference, and ruled out muting them wholesale because 2 of the 19 had paged on real incidents in the 90-day history. She agreed the delete list with Owen Faraday, the on-call lead, before the first change, then deleted 7, retuned 5 with data from the 90 days, and rewrote the on-call guide so each remaining alarm names its first check, in [review 5130](https://example.com/reviews/5130). A strong Engineer II would have retuned the alarms assigned to them, not decided which 7 the team could live without.

Pages fell by 60% (from 45 a week to 18 a week) by 03/31/2026, and no incident has gone unnoticed in the 7 months since. (TO BE CONFIRMED) The on-call rotation's 7 builders now run the first-check guide on every page.

> "Our on-call stopped dreading the phone. Dana did the boring work nobody else would.", Noor Haddad, Engineering Manager

### Onboarding Guide: Scope and Influence

**Headline** 3 new builders shipped their first change within 2 weeks instead of 6.

**Q1 2026, Onboarding Guide:** a new builder on Harbor Telemetry took 6 weeks on average to ship a first change, because the setup steps lived in 4 people's heads and no document held them. Nobody had asked for a guide. Dana started writing one while onboarding the next builder.

Dana wrote the guide without being asked and the manager made it the team standard in [the onboarding guide](https://example.com/docs/onboarding-guide), with the two builders she onboarded checking each step as they ran it.

Dana recorded every step while onboarding a new builder in January 2026, turned the 31 steps into a checked script in [review 5155](https://example.com/reviews/5155), and reviewed the 3 new builders' first changes. A strong Engineer II would have written notes for themselves, not a script the team and two other teams run.

The 3 builders who joined in 2026 shipped their first change in 11, 9 and 14 days. Two other teams copied the guide format in Q3 2026.

> (TO BE COLLECTED: quote from a builder onboarded in 2026)

## Best reasons not to promote

Two themes came up, and both providers raised one each: one provider sees Dana waiting for someone to name the next improvement, one sees her documents running long. The manager's own view matches both.

### Proposing the next improvement before being asked

**Pattern** Dana executes fully once a problem is named, as Breakwater Credentials and Quayside Tagging show.

**Gap** What Dana does not yet do is propose the next improvement first: on 05/06/2026 Owen Faraday had to point out that the team's repeated manifest tests could be automated before Dana took it on, and Dana then built it well.

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
| Felix Marchetti | Senior Engineer, reviewer on the Tidewater Schema design | Yes |
| Owen Faraday | Senior Engineer, on-call lead and peer on Breakwater Credentials | Yes |

Both providers gave their feedback in writing. Their words are reproduced in Feedback without editing.

## Feedback

### Felix Marchetti, Senior Engineer

Relationship: reviewed the schema derivation note and two other designs by Dana in 2026. Best reasons to promote: Dana saw that three mappings were one problem and removed two sources instead of patching 27 mismatches. [Simplicity] Best reasons not to promote: Dana's documents run long. The derivation note was 11 pages and I asked on 08/12/2026 for a 3-page version before the review could proceed.

### Owen Faraday, Senior Engineer

Relationship: on-call lead during the 10/20/2025 regional event and peer on Breakwater Credentials. Best reasons to promote: Dana disproved the retry fix with a number before anyone argued and changed another team's client to fix ours. [Ownership and Delivery] Best reasons not to promote: Dana waits for someone to point at the next improvement. The repeated manifest tests were automated well, but only after I named them on 05/06/2026.

Sources used: sample evidence. Sources unavailable: none
