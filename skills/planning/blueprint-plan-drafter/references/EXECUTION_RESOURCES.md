# Execution resources

## Skill lifecycle

Each stage of the plan lifecycle is handled by a different skill.

| Stage | Skill | Purpose |
| --- | --- | --- |
| Detailed technical planning | blueprint-plan-drafter | Define technical decisions, file scope, milestones, and completion evidence |
| Concise planning | modest-plan-drafter | Define a bounded coding or non-coding outcome, approach, and completion checks |
| Plan execution (parallel) | parallel-plan | Lightweight parallelization for active work |
| Subagent dispatch | delegate-manager-to-subagents | Fresh-subagent dispatch of independent work packages |
| Idle capacity during execution | stay-busy | Plan-related evidence work when the active plan has no obvious next task |
| Pre-merge audit | audit-code-reviewer | Parallel multi-reviewer audit before merge or release |
| Multi-agent coordination | gas-town-workflow | Role-mapped task routing with convoy patterns |

## Execution handoff

Planning ends with the plan artifact. Once execution is requested, the execution manager derives
tasks, ownership, briefs, and dispatch from the approved outcomes, file scope, dependencies, and
verification. The plan's brief parallel-readiness notes inform this work without preassigning it.

Use the execution skills' current guidance for model selection, ownership, independent review, and
integration. Give shared resources and generated artifacts clear responsibility during execution.
Use `audit-code-reviewer` for a requested parallel pre-merge or pre-release audit, and
`gas-town-workflow` only when the user requests that role-mapped workflow.

## Dedicated agent classes

During execution, use a dedicated class when its responsibility matches the work:

| Responsibility | Agent class |
| --- | --- |
| Cross-cutting design decision | `architect` |
| Focused implementation | `coder` or `expert_coder` |
| Independent assessment | `reviewer` |
| Distinct test work | `tester` |
| Integration and conflict resolution | `integrator` |
| Browser interaction and capture | `playwright_operator` |
| Visual assessment | `image_evaluator` |

Use a capable fresh subagent for work without a matching dedicated class.
