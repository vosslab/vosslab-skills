# Testing and oracles

Validate each evidence packet against the route chosen in
[topic_index.md](topic_index.md). Preserve the check result with the collection
notes.

## Contract and version checks

- Reopen the current Xquik API documentation before naming a request or field.
- Resolve the current stable SDK version with `npm view x-developer version`.
- Confirm every code example pins that exact version.
- Reject undocumented fields, guessed limits, and private implementation claims.

## Evidence checks

- Identifier check: every factual row has a stable post or account identifier.
- Provenance check: every result set has its query, source URL, and collection time.
- Window check: timestamps fall inside the declared range or carry an exception.
- Sampling-parity check: comparisons use the same window, cap, and exclusions.
- Relationship check: referenced parents, replies, authors, and posts resolve to
  the identifiers recorded in the packet.
- Separation check: observed fields and derived analysis use distinct columns.

## Replay check

1. Select at least one record from each collection route.
2. Replay its documented lookup using the same stable identifier or query.
3. Compare the returned identifier and source URL with the stored record.
4. Record expected drift for mutable fields such as counts or display names.
5. Mark deleted, protected, or unavailable content as unavailable, not absent.

Use [project_workflow.md](project_workflow.md) to store these results in an
existing project or a greenfield research brief.
