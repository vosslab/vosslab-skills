# Plan Quality Standard

This reference captures planning patterns and quality gates distilled from:
- `refactor_progress.md`
- `docs/active_plans/*.md`
- `docs/archive/*.md`

Use it to draft or review manager-level implementation plans for coding teams.

## 1. Plan Charter
- State one objective in concrete terms.
- Define scope and non-goals explicitly.
- Describe current state before proposing future phases.
- Declare architecture and ownership boundaries early.

## 2. Phase Design
- Use ordered phases with clear dependency flow.
- Each phase must include:
  - Deliverables
  - Done checks
  - Entry/exit criteria when relevant
- Mark optional phases explicitly.
- Keep stretch goals separate from required delivery phases.

## 3. Acceptance and Gates
- Add measurable acceptance criteria, not qualitative intent.
- Define explicit gates:
  - Unit/verification gate
  - Integration gate
  - Regression gate
  - Release gate
- Require deterministic outcomes where stability matters.

## 4. Testing and Verification
- Map tests to each phase.
- Distinguish:
  - Unit checks
  - Integration checks
  - Smoke/system checks
  - Full regression gates
- Include failure semantics (what blocks progression).

## 5. Migration and Compatibility
- Prefer additive rollout first, destructive cleanup later.
- State backward compatibility policy and limits.
- Include deletion criteria for legacy paths.
- Include rollback strategy when risk is non-trivial.

## 6. Risk Register
- List top risks with:
  - Impact
  - Trigger
  - Mitigation
  - Owner
- Include drift risks (plan vs implementation mismatch).
- Include scope creep and sequencing risks.

## 7. Manager-Level Clarity Requirements
- Use stable terminology consistently across sections.
- Avoid hidden assumptions and implied dependencies.
- Separate facts, decisions, and open questions.
- Maintain a status tracker for active vs complete vs future work.

## 8. Anti-Patterns To Reject
- Vague phases without deliverables.
- "Done" claims without test gates.
- Mixing non-goals into in-scope tasks.
- No compatibility or migration section.
- No explicit ownership boundaries.
- No risk/rollback treatment for high-impact changes.

## 9. Output Template
Use this skeleton when drafting:

1. Objective
2. Scope
3. Non-goals
4. Current State
5. Architecture Boundaries
6. Phase Plan
7. Per-Phase Deliverables and Done Checks
8. Acceptance Criteria and Gates
9. Test Strategy
10. Migration and Compatibility
11. Risks and Mitigations
12. Rollout/Release Checklist
13. Open Questions

## 10. Review Scoring Heuristic
- Blocker: missing scope boundary, no acceptance gates, no phase done checks.
- High risk: unclear dependencies, no migration policy, no regression strategy.
- Medium risk: ambiguous wording, incomplete risk treatment.
- Low risk: wording polish, formatting consistency.
