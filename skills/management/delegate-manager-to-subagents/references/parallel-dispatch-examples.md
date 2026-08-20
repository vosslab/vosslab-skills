# Parallel dispatch examples

Use the plan's dependency graph and ownership boundaries.

## Independent tasks

Dispatch tasks together when the plan marks them dependency-free with separate ownership.

```text
Task A: component A, ready
Task B: component B, ready
Task C: integration, depends on A and B
```

Dispatch A and B together. Dispatch C after both complete and pass review.

## Shared ownership

Sequence tasks that edit the same files or depend on an unsettled interface. A focused reviewer can
resolve an unclear dependency before implementation continues.
