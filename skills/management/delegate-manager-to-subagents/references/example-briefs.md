# Brief examples

Use this complete template for each bounded assignment. Supply the task text directly so the agent does not
need to reconstruct the approved plan.

## Seven-part dispatch brief

```text
Assignment and outcome:
- Plan: [path and task identifier]
- Complete assigned task text: [verbatim plan task]
- Deliverable, acceptance criteria, and non-goals: [...]

Ownership and boundaries:
- Owner and role: [fresh agent and role]
- Delegate model: [exact identifier verified against the currently available model catalog]
- Model selection: [smallest capable smaller, cheaper model; capability reason for exceptions]
- Permitted changes: [files, modules, interfaces, or state]
- Shared areas: [inspect freely; ask the manager before changing]

Context and constraints:
- Working directory: [...]
- Bootstrap: read [repository-rule pointers] before work; do not duplicate their contents here.
- Evidence, decisions, compatibility constraints, and conventions: [...]

Dependencies and coordination:
- Prerequisites and downstream consumers: [...]
- Shared contracts and task-ledger location: [...]
- Decision propagation record: [location; this task's updated brief, constraint, restatement, evidence,
  and pending next-action owner; include affected downstream consumers]
- Parallel readiness: [ready / serialized because ...]
- Integration path: [...]

Approach and question checkpoint:
- Before substantive edits for consequential ambiguity, report your interpretation, intended approach,
  affected boundaries, and unresolved questions.
- Challenge unsupported assumptions, including mine. Ask about consequential uncertainty in requirements,
  scope, ownership, interfaces, verification, or acceptance.
- Frame each question with ambiguity, options and consequences when applicable, grounded recommendation,
  and exact blocking point. Continue only isolated work while it is pending.
- After a decision, restate the resulting constraint before dependent implementation.

Verification and handoff evidence:
- Required checks and expected results: [...]
- Report exact commands and decisive output, or exit status when a command is silent.
- Map requirements to changed files or other deliverables. Scope failures, warnings, skipped checks,
  limitations, decision identifiers, confirmed interpretations, and evidence that decisions were applied.

Review and completion route:
- Report destination: [...]
- Review scope: [change-focused or codebase-wide]
- Route: fresh specification reviewer, different fresh quality reviewer after specification acceptance,
  fresh correction and re-review agents as needed, then fresh integration review.
```

## Review prompt

```text
Assignment and outcome: [approved task and acceptance criteria]
Review scope: [change-focused or codebase-wide, including repository context examined]
Evidence: [handoff commands, output, decision identifiers, and relevant files]
Verdict: [specification compliance or quality only]
Report concrete findings with file/line or command evidence, required disposition, and limits on the verdict.
Do not combine specification and quality verdicts. Challenge unsupported assumptions and ask the manager
when the evidence cannot resolve a consequential question.
```

## Handoff prompt

```text
Status: [complete / pending / blocked]
Requirements to deliverables: [...]
Commands and decisive output: [...]
Decisions applied: [identifier, restated constraint, confirmation, and verification evidence]
Failures, warnings, skipped checks, limitations, and blockers: [...]
Recommended review route: [...]
```
