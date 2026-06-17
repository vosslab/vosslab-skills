# Project workflow

Use this guide after choosing a route in [topic_index.md](topic_index.md).
Keep the source evidence reproducible inside the target project's existing
data and documentation conventions.

## Existing-project path

1. Inspect the project's report schema, source ledger, retention rules, and
   existing X data adapters.
2. Reuse established field names for identifiers, source URLs, timestamps,
   queries, sample limits, and derived values.
3. Define a bounded collection with
   [task_selection.md](task_selection.md).
4. Preserve raw observations separately from labels, scores, summaries, and
   other analysis.
5. Add the evidence packet without replacing unrelated historical records.
6. Run the relevant checks from
   [testing_and_oracles.md](testing_and_oracles.md).

## Greenfield path

1. Write a short research brief with the decision, scope, exclusions, time
   window, sample cap, locale, and stopping rule.
2. Define a record containing stable identifier, source URL, query, collection
   time, observed fields, and separately named derived fields.
3. Record the current public contract and exact verified SDK version when code
   is part of the deliverable.
4. Collect the smallest useful sample and retain a replayable request ledger.
5. Produce findings that state scope limits beside each conclusion.
6. Run every applicable evidence oracle before delivery.

If credentials or authorized access are unavailable, stop at a collection plan.
Do not substitute guessed, cached, or fabricated records for live evidence.
