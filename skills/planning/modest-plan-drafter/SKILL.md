---
name: modest-plan-drafter
description: Draft concise plans for bounded coding, teaching, research, writing, or organizational work. Use when a short approach and observable completion checks suffice; use blueprint-plan-drafter for complex technical coordination.
---

# Modest plan drafter

## Purpose and routing

Turn a request into a concise plan with evidence, scope, decisions, and observable outcomes.
Produce the planning artifact before execution. Aim for roughly one page as a soft target;
necessary decisions determine the detail.

Use Modest when the outcome can be described, executed, and verified with a short approach.
Use `blueprint-plan-drafter` for coding work involving cross-module coordination, shared contracts,
migrations, significant compatibility risk, or coordinated multi-agent implementation and review.
Honor explicit skill choices. If a requested Modest plan leaves important technical decisions
unresolved, explain the need for Blueprint or expand the relevant detail.

## Establish the evidence

- Inspect source material relevant to the outcome. For repository work, read operative repository
  rules or reuse a valid same-session receipt. Load specialized guidance only when applicable.
- Establish the intended audience, current state, scope, and material constraints. Resolve
  discoverable facts from evidence; clarify choices that materially change the outcome.
- Keep observations, assumptions, and decisions distinct. Use a bounded investigation with a
  decision rule when evidence is needed to select an approach.

For broad code investigation, read [GRAPHIFY_GUIDE.md](references/GRAPHIFY_GUIDE.md) when a Graphify
map or repository wrapper is available. Otherwise use targeted searches and source inspection.

## Draft the plan

Use this default shape, adapting it to the task:

1. **Goal and context:** intended outcome, relevant evidence, audience, and scope.
2. **Approach:** a short sequence of meaningful actions, necessary decisions, and dependencies.
3. **Completion checks:** observable evidence that the requested outcome is achieved.

For file-based work, add **File scope** after Approach: expected files or directories and the
purpose of each change. Include relevant tests, documentation, and generated outputs with their
canonical sources. Treat this as the expected edit boundary, refined as evidence emerges.

Include assumptions, constraints, tradeoffs, and material risks where useful. Name exact components,
interfaces, or validation commands when they affect execution. Leave detailed task assignments and
dispatch to execution. Keep the artifact proportional to the decisions the work needs.

## Quality and verification

- Ground requirements in product needs, meaningful contracts, measured constraints, or demonstrated
  failures. Use thresholds, byte or pixel equivalence, and exhaustive matrices only when those
  needs justify them. Improvement work should permit intended changes.
- Apply KISS aggressively: mechanisms, abstractions, policies, state, configuration, and tests must
  solve demonstrated needs. Prefer sensible fixed behavior or a simpler shared design before
  adding options, parameters, modes, overrides, or extension points. Distinguish genuinely different
  tasks from internal implementation choices; every extra choice adds maintenance and combinations.
- Give each new blocking gate a grounded reason and a concrete decision, correction, or recovery
  action on failure. Drop gates whose failure would identify no real problem or change no decision.
- For software work, read [CODE_VERIFICATION.md](references/CODE_VERIFICATION.md) before drafting
  design and completion checks. It covers robustness, adaptability, repository policy, and the
  distinction between one-time evidence and justified permanent tests. For non-coding work, choose
  evidence appropriate to the deliverable.

## Completion

Finish when the outcome and boundaries are clear, the approach carries necessary decisions and
dependencies, file scope is useful where applicable, and completion checks are observable and
proportionate. Resolve blocking choices or define an explicit evidence-led investigation that
precedes dependent work. Return the plan in the requested format; save a file when requested or
required by the active workflow. Execution begins as a separate task.
