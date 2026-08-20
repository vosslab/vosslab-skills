# Definitions

Canonical terminology for manager planning docs in this skill.

## Planning terms
- Milestone: timeboxed planning unit with deliverables and gates. Use in docs only.
- Workstream: parallel lane inside a milestone. Ownable by one coder or a small pair.
- Work package: one-owner chunk with a clear outcome.
- Patch: a reviewable code change set (PR-sized), used in summaries and changelog entries.

## Plan sections
- Context: evidence and conditions that motivate the plan.
- Objectives: concrete outcomes the plan aims to achieve.
- Design philosophy: the plan's central trade-off and guiding principles.
- Scope: work the plan completes.
- Non-goals: intentional exclusions that keep the plan bounded.
- Current state summary: relevant behavior, evidence, constraints, and known gaps.
- Architecture boundaries and ownership: durable components and their responsibilities.
- Mapping: relationship between planning units, components, and review boundaries.
- Milestone plan: ordered delivery units used when sequencing benefits from milestones.
- Workstream breakdown: independent lanes used when parallel coordination adds value.
- Work packages: one-owner tasks with clear outcomes and dependencies.
- Acceptance criteria and gates: observable conditions used to evaluate important outcomes.
- Test and verification strategy: repository-appropriate evidence selected for the change.
- Risk register: material risks with triggers, owners, and mitigations.
- Rollout and release checklist: applicable steps for safely delivering the result.
- Documentation close-out requirements: documentation called for by the repository or change.
- Patch plan and reporting format: review boundaries and reporting labels for repository changes.
- Open questions and decisions needed: decision procedures and non-blocking follow-up questions.

## Durable naming
- Reserve milestone, workstream, and work package for planning artifacts.
- Name repository identifiers after enduring behavior, responsibility, or structure.
- Use stage, step, or pass for pipeline and algorithm steps.
- Use component, module, subsystem, or contract for implementation boundaries.
- Give tests behavior-based names such as `test_export_contract.py`.
