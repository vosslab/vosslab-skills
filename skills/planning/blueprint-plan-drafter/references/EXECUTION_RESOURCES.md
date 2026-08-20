# Execution resources

## Skill lifecycle

Each stage of the plan lifecycle is handled by a different skill.

| Stage | Skill | Purpose |
| --- | --- | --- |
| Plan creation | blueprint-plan-drafter | Build an implementation plan without writing code |
| Plan execution (parallel) | parallel-plan | Lightweight parallelization for active work |
| Subagent dispatch | delegate-manager-to-subagents | Fresh-subagent dispatch of independent work packages |
| Idle capacity during execution | stay-busy | Plan-related evidence work when the active plan has no obvious next task |
| Pre-merge audit | audit-code-reviewer | Parallel multi-reviewer audit before merge or release |
| Multi-agent coordination | gas-town-workflow | Role-mapped task routing with convoy patterns |

## Ownership guidance

- Name the responsibility each work package needs.
- Let `delegate-manager-to-subagents` select an available fresh subagent.
- Assign implementation and independent review to separate subagents.
- Keep focused verification with its implementation package; create a separate verification package
  when the work is genuinely independent.

## Dedicated agent classes

Use a dedicated class when its responsibility matches the work:

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
