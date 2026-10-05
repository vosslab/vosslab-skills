# Definitions

Canonical terminology for manager planning docs in this skill.

## Planning terms
- Milestone: delivery unit with observable outcomes and meaningful dependencies. Use in docs only.
- Workstream: naturally independent area noted briefly within a milestone; detailed assignments
  are defined during execution.

## Plan sections
- Context: evidence and conditions that motivate the plan.
- Objectives: concrete outcomes the plan aims to achieve.
- Design philosophy: the plan's central trade-off and guiding principles.
- Scope: work the plan completes.
- Non-goals: intentional exclusions that keep the plan bounded.
- Current state summary: relevant behavior, evidence, constraints, and known gaps.
- Architecture boundaries and ownership: durable components and their responsibilities.
- Mapping: relationship between planning units, components, and review boundaries.
- File scope: expected files or directories and intended changes, including canonical sources for
  generated outputs; an edit boundary refined as evidence emerges.
- Milestone plan: ordered delivery units used when sequencing benefits from milestones.
- Exit criteria: observable conditions that demonstrate a milestone's outcome.
- Test and verification strategy: repository-appropriate evidence selected for the change,
  distinguishing one-time checks from permanent tests and naming responses to blocking failures.
- Risk register: material risks with triggers, owners, and mitigations.
- Rollout and release checklist: applicable steps for safely delivering the result.
- Documentation close-out requirements: documentation called for by the repository or change.
- Open questions and decisions needed: decision procedures and non-blocking follow-up questions.

## Durable naming
- Use milestone and workstream in planning prose; work-package assignments belong to execution
  artifacts.
- Name repository identifiers after enduring behavior, responsibility, or structure.
- Use stage, step, or pass for pipeline and algorithm steps.
- Use component, module, subsystem, or contract for implementation boundaries.
- Give tests behavior-based names such as `test_export_contract.py`.
