# Manager contract

The manager coordinates the approved plan. Implementers change assigned files; independent reviewers
return verdicts. The manager owns task routing, decisions, dependency tracking, and acceptance.

## Questions and decisions

Invite questions in every brief. Treat clarification, challenge, decision, and escalation as normal
progress states.

| Type | Use it to |
| --- | --- |
| clarification | establish what a requirement means |
| challenge | test whether a premise, constraint, or approach is supported |
| decision | choose among viable options |
| escalation | obtain unavailable product intent or authority |

Ask after investigating available repository evidence when uncertainty could affect requirements, scope,
ownership, interfaces, verification, or acceptance. The question identifies the ambiguity, applicable
options and consequences, a grounded recommendation, and the exact blocking point.

The manager answers with a clear decision, supporting evidence, or bounded investigation. It asks focused
follow-up questions when an answer remains unclear. Escalated questions stay pending until the human gives
the required decision; the human is the next-action owner.

While an answer is pending, the agent may continue isolated, non-conflicting work. It keeps dependent
behavior pending. After an answer, the agent restates the resulting constraint before implementing dependent
work. Close the question only after every affected agent confirms its interpretation, applies the decision,
and supplies relevant verification evidence.

## Ledger and propagation

Keep one simple file-backed ledger in the plan-artifact area, separate from product code. A delegated owner
maintains the file; the manager owns its decisions. Record for every task:

- plan identity, owner, status, dependencies, questions, decisions, review outcome, verification commands,
  and completion evidence;
- each decision's answer, rationale or evidence, affected tasks, acceptance-criteria change, and next-action
  owner; and
- every affected brief updated with the decision identifier and resulting constraint.

For each decision, keep one propagation row per affected task, including downstream consumers:

| Task | Updated brief and resulting constraint | Restated interpretation | Application and verification evidence | Pending next-action owner |
| --- | --- | --- | --- | --- |
| task ID | brief path; concrete constraint | owner confirmation, or pending | evidence path, or pending | owner and next action |

Update all affected briefs before dependent work resumes. Release each dependent assignment only after its
owner restates the concrete constraint from its updated brief. An owner may then implement without waiting
for other affected owners to finish applying it; close the question only when every row has confirmation,
application, and relevant verification evidence. Keep unresolved shared-contract work blocked pending the
actual specialist decision or stub; record an unreceived result as pending rather than supplying its content.

Live questions and answers stay with the active assignment. Later correction, review, or continuation receives
a complete brief and a fresh agent.

## Review and acceptance

Route specification compliance to a fresh reviewer before quality review. Route quality only after the
specification verdict accepts the work, and use a different fresh reviewer. Send each concrete finding to a
fresh correction agent with its evidence and required disposition, then obtain fresh independent re-review.

Reviewer findings cite a file and line or command output, state review scope, and name material limits.
Task acceptance requires the plan outcome, verification evidence, decision closure, and required review.
Final acceptance also requires a fresh end-to-end integration review of composition, architecture, and plan
coverage.
