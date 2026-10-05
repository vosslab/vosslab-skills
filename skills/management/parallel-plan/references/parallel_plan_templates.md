# Parallel plan templates

Use these templates to dispatch, track, and accept isolated workstreams. Keep the plan artifact
area separate from product code. Give each artifact a collision-safe path chosen by the manager.

## Parallel-ready map

Use one row per proposed stream before dispatch.

| Stream | Owner and model | Files or state | Dependencies | Unresolved decisions | Checks | Review and integration route | Ready or serialized reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `name` | fresh agent; smallest capable model | `path` | task or decision | decision ID or none | command or review | reviewers and gate | ready or reason |

Verify each exact model identifier against the currently available model catalog before dispatch. Explicitly
default to a smaller, cheaper model than the manager, choosing the smallest capable model. Record the
capability reason when a larger model is selected or no cheaper suitable model exists. Use a fresh agent
for any capability escalation.

## Seven-part dispatch brief

Give the agent the complete assigned task text; do not make it reconstruct the plan.

```text
Assignment and outcome:
- Task ID and approved plan reference:
- Complete assigned task text:
- Deliverable, acceptance criteria, and non-goals:

Ownership and boundaries:
- Owner, role, and selected model:
- Exact model identifier verified against the currently available model catalog; capability reason
  for any exception to the smallest capable smaller, cheaper default:
- Files, modules, interfaces, data, or state this assignment may change:
- Shared areas that require a manager decision before change:
- Inspection may use any repository context needed for sound work:

Context and constraints:
- Working directory and repository-bootstrap rule pointers to read first:
- Relevant evidence, established decisions, compatibility requirements, and conventions:

Dependencies and coordination:
- Prerequisites, downstream consumers, shared contracts, and ledger location:
- Decision propagation record location and this task's constraint, restatement, evidence, and pending
  next-action owner; include affected downstream consumers:
- Parallel readiness, or why this work is serialized:
- Report path and integration path:

Approach and question checkpoint:
- Before substantive work on unclear behavior or a shared boundary, report your interpretation,
  intended approach, affected boundaries, and unresolved questions.
- Challenge unsupported assumptions, including the manager's. Ask throughout execution when an
  uncertainty could affect requirements, scope, ownership, interfaces, verification, or acceptance.
- Questions identify the ambiguity, viable options and consequences when applicable, grounded
  recommendation, and exact blocking point. Mark each as clarification, challenge, decision, or
  escalation.
- While a decision is pending, continue only isolated work; mark dependent work pending. After a
  decision, restate the resulting constraint before implementing dependent work.

Verification and handoff evidence:
- Required checks and expected results:
- Exact commands and decisive output; for silent commands, exit status and explicit silence:
- Changed files or deliverables mapped to requirements:
- Failures, warnings, skipped checks, limitations, and their scope:
- Decisions applied, restated interpretation, and evidence that the decision was applied:

Review and completion route:
- Report destination and review scope: change-focused or codebase-wide:
- Fresh specification reviewer; start a different fresh quality reviewer only after the
  specification reviewer accepts the work:
- Fresh correction and re-review route for findings:
- Final integration checks and independent integration review:
```

## Question and decision record

Record consequential questions in the plan ledger and propagate each decision to affected briefs.
Question status is separate from task status. `answered` records a manager answer and stays open to
closure until affected agents confirm their interpretation, apply the decision, and provide relevant
verification evidence. `escalated` stays unresolved while the human next-action owner supplies the
needed decision; it becomes `closed` only after the affected agents confirm, apply, and verify it.

```text
Decision ID:
Type: clarification|challenge|decision|escalation
Question and blocking point:
Manager answer, evidence, or bounded investigation:
Rationale and supporting evidence:
Affected tasks:
Acceptance criteria change: none|<exact change>
Next-action owner:
Per-affected-task propagation table: [below]
Status: open|answered|escalated|closed
```

| Task | Updated brief and resulting constraint | Restated interpretation | Application and verification evidence | Pending next-action owner |
| --- | --- | --- | --- | --- |
| task ID | brief path; concrete constraint | owner confirmation, or pending | evidence path, or pending | owner and next action |

Include every affected task, including downstream consumers. Update all affected briefs before dependent
work resumes. Release each dependent assignment only after its owner restates the concrete constraint
from its updated brief. That owner may implement without waiting for other owners to finish applying it;
question closure still requires confirmation, application, and relevant verification evidence in every row.
Keep unresolved shared-contract work blocked pending the actual specialist decision or stub. Record an
unreceived specialist result as pending rather than supplying its content.

An escalated record remains `escalated` pending human action. Dependent work stays pending. A manager
answer alone does not close the record.

## Plan ledger

Keep a plain file-backed ledger, not a database. Its context identifies the approved plan by name or
path and records enough coordination evidence to recover the work without repeating plan text.

| Task | Owner | Status | Dependencies | Questions and decisions | Reviews | Checks and evidence | Next action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ID` | fresh agent and model | ready / active / pending / blocked / failed / complete | IDs | IDs | verdicts | commands or reports | owner |

Task status is separate from question status. The manager owns decisions and acceptance. A delegated
owner maintains the ledger file.

## Evidence-first handoff

Use a concise message that points to the full report rather than omitting material evidence.

```text
Status: complete|pending|blocked|failed
Report path: <manager-assigned collision-safe path>
Requirements and changed files or deliverables:
- requirement: <path or deliverable>
Commands and results:
- command: <exact command>
  result: <decisive output, or "silent; exit 0">
Decisions applied and verified:
- <decision ID>: <confirmation and evidence>
Failures, warnings, skipped checks, and limitations:
- none|<scope and consequence>
Questions or blockers:
- none|<decision-shaped question>
```

## Review and integration record

Specification review precedes quality review, and each receives a fresh reviewer. Record whether
the specification reviewer accepts the work or identifies findings; start quality review only
after specification acceptance. Findings name the requirement, evidence from a file, line, or
command output, required disposition, and review-scope limits. A fresh correction agent addresses
findings; a fresh specification reviewer rechecks them, and a different fresh quality reviewer
starts only after the re-review accepts the corrections.

The final independent integration review follows task-level acceptance. It examines how workstreams
compose, architecture, plan coverage, shared contracts, and integrated verification evidence. It may
inspect the whole codebase when that is needed for a sound verdict.

## Pressure scenarios

Use realistic scenarios to test the process before relying on it:

- A manager premise conflicts with repository evidence; the agent challenges it before implementation.
- A manager answer leaves a compatibility choice open; the agent asks again rather than guessing.
- A shared interface needs a narrow decision; dependent work stays pending while isolated work continues.
- A human product decision is needed; the ledger records the escalation and the human next action.
- A decision changes acceptance criteria; all affected briefs receive the updated constraint.
- Task reviewers accept individual work but the integration review finds a composition failure.

Record observed behavior, failure mode, and correction route. Correct demonstrated loopholes; do not
add rules merely to enforce headings or wording.

## Anti-pattern checks

Rework a dispatch when it has overlapping mutable ownership, hidden dependencies, parallel labels on
serialized work, a missing integration route, or a review limited without rationale. Rework a
question loop when it permits consequential guessing, closes after a manager reply, or lets pending
dependent work proceed.
