# Testing and oracles

Use these oracles to validate HCI recommendations with evidence an agent can
produce. Start with [topic_index.md](topic_index.md) to choose the relevant
task and record each result beside its acceptance criterion.

## Guideline-conformance checks

Create a guideline ledger with columns for task step, user need, guideline,
implementation acceptance criterion, evidence, and status. Run each check
against the built interface or prototype.

- Run `npx @axe-core/cli <target-url>` for automated semantic and accessibility
  findings when the target is a web surface.
- Run the project's lint, component-test, or platform accessibility-inspector
  command for each rule covered by the ledger.
- Review visible labels, instructions, feedback, error recovery, recognition
  cues, and confirmation at every task step against the stated guideline.
- Save the ledger and command output as the conformance record.

## Task-completion walkthroughs

Write one scenario per critical task with a start state, user goal, expected
actions, information needed, likely error, recovery path, and completion proof.

1. Reset the target to the scenario start state.
2. Walk through the task using keyboard, pointer, touch, voice, or assistive
   technology inputs appropriate to the target user and platform.
3. Record each action, system response, error, recovery, completion status,
   elapsed time, and unresolved question.
4. Compare the observed path with the task model and mark mismatches for review.
5. Capture screenshots, logs, or a short recording that makes completion and
   friction visible to the team.

## Measured accessibility checks

- Run automated WCAG-oriented scanning with `npx @axe-core/cli <target-url>`
  and triage each finding against the relevant success criterion.
- Measure foreground/background contrast with a contrast checker and record
  the ratio for normal text, large text, controls, focus indicators, and icons.
- Traverse every critical task by keyboard and record focus order, visible focus,
  activation, escape, and error-recovery behavior.
- Inspect names, roles, values, and states with the platform accessibility tree
  or browser accessibility inspector; record the result for each task control.
- Run the target platform's accessibility inspector and map findings to current
  W3C WCAG and the platform's human-interface guidelines.

## Evidence standard

Treat an HCI recommendation as supported when the guideline ledger, at least
one task-completion walkthrough, and measured accessibility checks agree with
the task model. Report the evidence scope, participant or reviewer coverage,
and remaining uncertainty with the finding.

## Corpus-absent route

Use [topic_index.md](topic_index.md) to select the check when local books are
absent. Consult current W3C WCAG and the target platform's human-interface
guidelines to set acceptance criteria, then run the matching runnable oracle
above and preserve its output with the project evidence.
