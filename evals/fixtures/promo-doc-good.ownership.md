# Ownership audit: Dana Whitfield, Engineer II to Senior Engineer

Stage document written before the promotion document, fictional, the green companion of `promo-doc-good.md`. One attribution line per story. The verdict backs every ownership verb the story uses (led, owned, drove, architected, designed, end-to-end). No `Ownership:` sentence is printed in the document (D59), the shared work is credited by function inside the task paragraph and the qualification column here says what that sentence carries. Checklist rule `ownership-verdict` reads this file.

| Story | Ownership verbs in the story | Evidence checked | Verdict | Qualification carried into the story |
|---|---|---|---|---|
| Lighthouse Parser: Ambiguity | owned the definition and the ingest side | [the format definition](https://example.com/docs/lighthouse-format) lists Dana as sole author, [review 4821](https://example.com/reviews/4821) and [review 4836](https://example.com/reviews/4836) authored by Dana | SUPPORTED | none |
| Breakwater Credentials: Problem Complexity | own the root cause and the fix across both code bases | [the credential cache design](https://example.com/docs/breakwater-design) lists Dana as author and the Identity team's senior owner as reviewer, [review 4917](https://example.com/reviews/4917) was merged by the Identity team | PARTIALLY SUPPORTED | the Identity team's senior owner reviewed and ran the rollout on their fleet, credited in the task paragraph |
| Tidewater Schema: Problem Complexity | owned the single derivation | [the schema derivation note](https://example.com/docs/tidewater-derivation) sole author, [review 5010](https://example.com/reviews/5010) authored by Dana | SUPPORTED | none |
| Quayside Tagging: Execution | took over the campaign | [ticket 2502](https://example.com/tickets/2502) reassigned to Dana after the rollback, the requirement came from the platform team | PARTIALLY SUPPORTED | the platform team wrote the requirement and the first builder reviewed the fix, credited in the task paragraph |
| Pier Alarm Cleanup: Impact | volunteered to own the cleanup | [the alarm review](https://example.com/docs/pier-alarm-review) names Dana as proposer, [review 5130](https://example.com/reviews/5130) authored by Dana | SUPPORTED | none |
| Onboarding Guide: Scope and Influence | wrote the guide without being asked | [the onboarding guide](https://example.com/docs/onboarding-guide) sole author, [review 5155](https://example.com/reviews/5155) authored by Dana | SUPPORTED | none |

No story uses led, drove, architected, designed or end-to-end. Verdict UNSUPPORTED appears on no row, so no story needs an ownership verb removed.
