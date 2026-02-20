---
name: coder-implement-next-phase
description: Implement the manager-prioritized phase of an existing plan and carry it to completion, including adjacent fixes needed to pass gates and close the phase cleanly. Use when a manager/reviewer says to start the next phase and expects end-to-end delivery with evidence.
---

# Coder Implement Next Phase

## Overview
Execute the selected plan phase to completion, not just partial checkboxes.
Prioritize finishing the phase with passing gates and clear evidence.

## Operating mode
- Treat the manager-selected phase as the primary target.
- Implement code, tests, and documentation updates required to close that phase.
- Include adjacent fixes when they are necessary to pass phase gates or prevent immediate regressions.
- Keep changes contract-driven and avoid case-specific hacks.

## Inputs to read first
0. Review STYLE guides in AGENTS.md, docs/PYTHON_STYLE.md, and docs/REPO_STYLE.md
1. Manager directive naming the target phase (or latest explicit manager instruction).
2. Target plan in `docs/active_plans/`.
3. `refactor_progress.md` for active/completed context.
4. Related archive precedent if cited by the plan.
5. Current repo state (`git status --short`, `git diff`).

## Mandatory constraints
- Treat the plan design philosophy near the top as binding architecture policy.
- Do not stop at partial progress when the remaining work is directly required to close the selected phase.
- Do not ask for guidance before attempting concrete unblock steps.
- Do not weaken strict gates to force a pass.
- Do not move geometry/runtime policy into tool/report layers unless the plan explicitly requires it.
- Do not claim completion without reproducible command evidence.

## Scope policy
- Primary scope: selected phase deliverables and done checks.
- Allowed adjacent scope: fixes that are strictly required to satisfy selected-phase gates.
- Deferred scope: improvements not required for selected-phase closure.

When adjacent scope is used, record:
- why it was required,
- what gate it unblocked,
- why deferral would leave the phase incomplete.

## Workflow
1. Lock the target phase:
- Identify exact phase id/name and extract deliverables, done checks, and gates.
- Record explicit out-of-scope items from later phases.

2. Build execution map:
- Map deliverables to file paths.
- Map done checks/gates to exact commands.
- Identify likely adjacent fixes needed for closure.

3. Implement to closure:
- Apply required edits for the phase.
- Apply adjacent unblock fixes when needed.
- Keep design-philosophy alignment explicit in decisions.

4. Validate gates:
- Run phase-required tests/commands first.
- Run broader regression gates required by the plan.
- Run targeted `pytest` regression: `source source_me.sh && python3 -m pytest -q tests/test*.py -k <file>/py`.
- Treat any failing `pytest` run as `Not complete` until fixed.
- Iterate until gates pass or a concrete blocker remains.

5. Prepare evidence:
- Capture command outputs and pass/fail results.
- Capture before/after artifacts when visuals/behavior are part of acceptance.
- Capture residual risks and ownership.

6. Close out docs:
- Update `docs/CHANGELOG.md` with concrete changes and validation commands/results.
- Update plan status language only when evidence supports closure.

## Implementation checklist template
- Phase target:
- Deliverables completed:
- Adjacent fixes applied (and why):
- Deferred items:
- Files changed:
- Commands run:
- Gate results:
- Remaining blockers:
- Completion decision: `Complete` or `Not complete`

## Failure handling
- If phase target is ambiguous, pick the most recent manager-specified phase and state the assumption.
- If gates conflict, follow the plan-defined gate hierarchy and report the conflict explicitly.
- If blocked, report exact blocker plus attempted mitigations; do not present partial work as complete.

## Manager completion report (required)
Submit one manager-grade close-out report at phase end using this structure.

Required sections:
1. `Phase decision`: `Complete` or `Not complete`.
2. `Scope execution`: what was completed, what was deferred, and why.
3. `Files changed`: exact paths grouped by runtime/tests/docs/tooling.
4. `Gate evidence`: exact commands with PASS/FAIL.
5. `Design philosophy alignment`: how implementation followed plan philosophy and avoided hacks.
6. `Visual/behavior evidence`: before/after paths and measured values (when required).
7. `Open risks`: unresolved risks with impact and owner.
8. `Next action`: one prioritized next step.

Report template:

```text
Phase decision: Complete | Not complete

Scope execution:
- Completed:
- Deferred:
- Adjacent fixes (required for closure):

Files changed:
- Runtime:
- Tests:
- Docs:
- Tooling:

Gate evidence:
- <command>: PASS/FAIL
- <command>: PASS/FAIL

Design philosophy alignment:
- <how implementation stayed aligned and avoided hacks>

Visual/behavior evidence:
- Before: <path>
- After: <path>
- Measurements: <metric=value, threshold=value>

Open risks:
- <risk, impact, owner>

Next action:
- <single prioritized next step>
```

## Output contract
Return results in this order:
1. Phase completion decision (`Complete` or `Not complete`).
2. Deliverables implemented (mapped to files).
3. Validation evidence (commands and outcomes).
4. Known gaps and risks.
5. Next action recommendation.
