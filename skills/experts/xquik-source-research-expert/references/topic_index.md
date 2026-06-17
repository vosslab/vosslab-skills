# Topic index

Route the research question to an evidence artifact and a reproducible check.
Use [task_selection.md](task_selection.md) when more than one route appears to
fit.

## Research routes

| Topic | Record first | Preserve | Validate with |
| --- | --- | --- | --- |
| Account activity | Account identifier and window | Post identifiers and source URLs | Window coverage check |
| Keyword or phrase | Exact query and locale | Result order and collection time | Query replay |
| Competitor comparison | Shared window and cap | One normalized row per result | Sampling-parity check |
| Post context | Root post identifier | Parent, reply, and author links | Relationship check |
| Profile evidence | Stable user identifier | Display fields and observed time | Identifier consistency check |
| Derived analysis | Input record identifiers | Method, label, and model or rule version | Observation-analysis separation |

## Source routing

- Use current Xquik API documentation for public request and response contracts.
- Use current Xquik MCP documentation when the agent should call a tool directly.
- Resolve and pin the current stable `x-developer` version before publishing code.
- Use [project_workflow.md](project_workflow.md) to place evidence in a project.
- Use [testing_and_oracles.md](testing_and_oracles.md) to verify the packet.

Never infer private implementation details, unobserved coverage, or deleted
content from an otherwise successful response.
