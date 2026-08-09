---
name: human-interact-expert
description: Design and evaluate human-computer interaction methods. Use for interaction design, usability evaluation, user research methods, cognitive design guidelines, task analysis, heuristic evaluation, mental models, accessibility, and HCI study design.
---

# Human interaction expert

## Overview

Use this skill to turn a product question into an evidence-based HCI method,
task model, guideline rationale, or evaluation plan. Frame the user goal,
context, and success evidence before selecting an interaction method.
Build project-specific artifacts such as a task model, study plan, heuristic
ledger, and accessibility acceptance criteria so each recommendation can guide
implementation and later evaluation.

## Workflow

1. Classify the HCI question and select a method.
- Identify the user group, goal, setting, device, task frequency, consequence
  of failure, and decision the team needs to make.
- Read [references/task_selection.md](references/task_selection.md) when the
  request could use research, task analysis, guidelines, or evaluation.
- Consult [references/topic_index.md](references/topic_index.md) to connect
  the question to a method, evidence artifact, guideline source, and oracle.

2. Detect the project shape and establish the evidence baseline.
- Existing project: inventory user journeys, research findings, support issues,
  analytics, interface states, accessibility checks, and prior study results.
- Greenfield project: write a concise HCI brief with users, goals, context,
  assumptions, risks, and success measures before interface construction.
- Read [references/project_workflow.md](references/project_workflow.md) for
  the project-shape path and required HCI artifacts.

3. Model the user's task and mental model.
- Map triggers, goals, actions, decisions, information needs, errors,
  recovery, handoffs, and completion evidence for each critical task.
- Capture the user's vocabulary, expectations, and visible cues that support
  recognition, memory, and confidence at each decision point.
- Turn the model into testable task-completion criteria and a study scenario.

4. Select the smallest method that answers the decision.
- Choose interviews or contextual inquiry for unknown context and mental models.
- Choose task analysis for workflow structure and allocation questions.
- Choose cognitive walkthrough or heuristic evaluation for expert inspection.
- Choose usability sessions for observed task completion and comprehension.
- Choose an evaluation study when a hypothesis, comparison, or measured
  outcome requires controlled or naturalistic evidence.

5. Translate evidence into guidelines and an implementation brief.
- State the applicable cognitive, accessibility, and platform guideline with
  its user-facing rationale and acceptance criterion.
- Hand the implementation brief to `ui-ux-engineer` for components, layouts,
  CSS, interface implementation, visual craft, and state polishing.
- Preserve the task model and rationale while the UI work turns them into a
  concrete surface.

6. Validate the recommendation with runnable evidence.
- Run guideline-conformance checks, a task-completion walkthrough, and
  measured accessibility checks; record findings and the next iteration.
- Read [references/testing_and_oracles.md](references/testing_and_oracles.md)
  for executable checks, measurement methods, and review artifacts.

## Implementation defaults

- Start with the local books when present; use [references/local_books.md](references/local_books.md)
  and [references/reference_survey.md](references/reference_survey.md) to
  select a method backed by the available corpus.
- Use [references/topic_index.md](references/topic_index.md) as the front door
  when the corpus is absent, then consult current W3C WCAG and the target
  platform's human-interface guidelines and run the named oracle.
- Recruit representative participants when a project can conduct a study;
  otherwise produce an inspection plan and clearly label its evidence scope.
- Write scenarios in the user's language and tie every finding to a task step.
- State measures before collecting evidence: completion, error, time, success,
  confidence, comprehension, or accessibility conformance.

## Quality bar

- Ground recommendations in a user goal, task context, and stated decision.
- Choose a method that can change a product decision within the available time.
- Make each guideline traceable to an observable interaction and acceptance check.
- Separate HCI method ownership from concrete interface implementation ownership.
- Record limitations, participant coverage, and unresolved assumptions clearly.

## Output expectations

When using this skill, aim to produce:
- A routed HCI question with the selected method and evidence rationale.
- A task model or study plan with users, scenarios, measures, and completion criteria.
- A guideline ledger that connects cognitive, accessibility, and platform rules
  to implementation acceptance criteria.
- A runnable validation plan with walkthrough, conformance, and measured
  accessibility oracles, plus a clear handoff to `ui-ux-engineer` when needed.
