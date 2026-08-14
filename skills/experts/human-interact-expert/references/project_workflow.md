# Project workflow

Use this guide after routing the question through [topic_index.md](topic_index.md).
Create project evidence before recommending an HCI method or accepting a result.

## Detect project shape

Inspect the target project for user journeys, research notes, product goals,
support requests, analytics, interface states, accessibility reports, tests,
and prior study results. Follow the existing-project path when this evidence
exists; otherwise establish a greenfield HCI brief.

## Existing-project path

1. Inventory the critical user journeys and identify the primary task, users,
   context, devices, errors, recovery paths, and current success evidence.
2. Capture a baseline: current completion behavior, observed friction, support
   themes, analytics, accessibility findings, and the relevant interface states.
3. Select a research, task-analysis, guideline, or evaluation method with
   [task_selection.md](task_selection.md).
4. Write a task model and evidence plan. Name the scenario, participants or
   reviewers, measures, success criterion, and decision that results will inform.
5. Create a guideline ledger that links each cognitive, WCAG, or platform rule
   to a task step and observable acceptance criterion.
6. Hand concrete interface work to `ui-ux-engineer` with the task model,
   findings, guideline rationale, and validation criteria.
7. Run the checks in [testing_and_oracles.md](testing_and_oracles.md), compare
   them with the baseline, and record the next evidence-backed change.

## Greenfield path

1. Write `docs/HCI_BRIEF.md` with intended users, goals, context of use,
   assumptions, risks, primary tasks, completion criteria, and accessibility scope.
2. Model the primary task from trigger through completion, including choices,
   information needs, errors, recovery, and confirmation.
3. Choose the smallest useful study or inspection method with
   [task_selection.md](task_selection.md), then define a scenario and measures.
4. Build a guideline ledger from cognitive design principles, current W3C WCAG,
   and the target platform's human-interface guidelines.
5. Give `ui-ux-engineer` the task model and acceptance criteria for the concrete
   components, layouts, CSS, interaction states, and visual craft.
6. Run the task walkthrough, guideline trace, and accessibility measurements
   from [testing_and_oracles.md](testing_and_oracles.md) before expanding scope.

## Corpus-absent route

Use [topic_index.md](topic_index.md) to choose the method when local books are
absent. Consult current W3C WCAG and the target platform's human-interface
guidelines, then run the applicable runnable oracle in
[testing_and_oracles.md](testing_and_oracles.md). Store the resulting evidence
with the HCI brief, task model, or study report.
