# Task selection

Choose the smallest X data collection that can answer the stated decision.
Start with [topic_index.md](topic_index.md), then define the evidence packet
before calling an API or SDK.

## Selection table

| Question | Collection route | Evidence artifact | Oracle |
| --- | --- | --- | --- |
| What did one account publish? | Account timeline within a fixed window | Post ledger | Identifier and window check |
| Which public posts match a term? | Bounded search query | Query result ledger | Query replay |
| How do several accounts differ? | Same-window account samples | Comparison table | Sampling-parity check |
| What context surrounds one post? | Post plus available reply evidence | Conversation packet | Parent and reply link check |
| Who is the subject of a claim? | Profile lookup by stable identifier | Profile evidence row | Identifier consistency check |

## Selection procedure

1. State the decision, accounts or terms, time window, locale, and exclusions.
2. Choose one route whose output can change that decision.
3. Set a sample cap and stopping rule before collection.
4. Record stable identifiers, query text, source URLs, and collection time.
5. Run the matching check in
   [testing_and_oracles.md](testing_and_oracles.md).

Do not widen the collection merely because more fields or routes are available.
Use [project_workflow.md](project_workflow.md) when the result will feed an
existing report, dataset, dashboard, or implementation.
