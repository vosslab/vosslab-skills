# Parallel dispatch examples

Use parallel work only when ready tasks have separate mutable ownership and no in-flight dependency. Record a
serialization reason whenever that condition does not hold. Each lane has a fresh owner, explicit model
selection, one verification step, and a review and integration route.

## Isolated work

```text
Task A: documentation source, fresh smaller capable model, ready
Task B: independent validator, fresh smaller capable model, ready
Task C: integration review, fresh capable reviewer, depends on A and B
```

Dispatch A and B together. Each brief names the ledger and asks the agent to pause for a manager decision if
its work exposes a shared contract. Dispatch C only after individual reviews accept A and B.

## Shared contract

```text
Task A: needs an API field from Task B
Task B: defines the API field
```

Serialize the dependent change. Assign a fresh specialist to make the narrow contract decision when the
approved plan does not settle it. Record the answer, evidence, affected tasks, acceptance impact, and next
action in the ledger. Update A and B briefs. A restates the resulting constraint before resuming its dependent
work.

## Pressure scenarios

Use realistic scenarios to test whether a manager actually follows this contract. Record the observed behavior,
failure mode, and correction route in plan artifacts.

| Scenario | Expected manager behavior |
| --- | --- |
| Unsupported premise | Welcome the challenge, inspect evidence, decide or investigate, and propagate the result. |
| Incomplete answer | Probe for the missing constraint; leave dependent work pending until resolved or escalated. |
| Interface disagreement | Pause dependent lanes, obtain a narrow specialist decision, and update every affected brief. |
| Product authority missing | Escalate to the human with a decision-shaped summary; record the human as next-action owner. |
| Premature closure | Require restated interpretation, applied decision, and verification evidence before closing. |
| Task reviews pass but composition fails | Route a fresh integration correction and review loop; do not accept the plan yet. |
