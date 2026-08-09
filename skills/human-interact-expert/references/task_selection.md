# Task selection

Use this guide to choose an HCI method from the decision the team must make.
Start with [topic_index.md](topic_index.md), then write the smallest evidence
plan that can answer the question.

## HCI method ownership

Own the interaction and evaluation method: choose the study, model the user's
task, select guidelines, and explain their rationale. Hand concrete components,
layouts, CSS, interface implementation, visual craft, and state polishing to
`ui-ux-engineer` with the task model and acceptance criteria.

## Method selection

| Decision needed | Preferred method | Evidence artifact | Runnable oracle |
| --- | --- | --- | --- |
| Learn context and vocabulary | Contextual inquiry or interviews | Field notes and mental-model map | Scenario walkthrough against notes |
| Map work, handoffs, and errors | Task analysis | Goal-action task model | Complete each modeled path |
| Inspect learnability before a study | Cognitive walkthrough | Step-by-step question ledger | Reviewer walks each action |
| Find broad interface issues | Heuristic evaluation | Severity-ranked finding ledger | Map each finding to a check |
| Observe whether users succeed | Usability evaluation | Script, measures, and findings | Timed task-completion run |
| Compare alternatives or contexts | Evaluation study | Hypothesis and analysis plan | Measure the preregistered outcome |
| Explain a cognitive guideline | Cognitive analysis | Guideline-to-task rationale | Inspect the matching interaction |
| Establish accessible behavior | WCAG and platform guidance | Success-criterion trace | Run accessibility checks |

## Selection procedure

1. Name the decision, user group, task, context, and consequence of an error.
2. Select the method whose artifact provides evidence for that decision.
3. Define participant or reviewer coverage, scenario, measure, and stopping rule.
4. Write the expected task-completion outcome before gathering evidence.
5. Create an implementation brief for `ui-ux-engineer` when the method identifies
   a concrete surface change.

## Corpus-absent route

Start at [topic_index.md](topic_index.md) when local books are unavailable.
Use current W3C WCAG for accessibility success criteria and the target platform's
human-interface guidelines for platform behavior. Run the selected runnable
oracle from [testing_and_oracles.md](testing_and_oracles.md) and record its
result with the task model or study plan.
