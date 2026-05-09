# Role catalog and subagent prompt templates

Supporting reference for `delegate-manager-to-subagents/SKILL.md`. Lists the
subagent roles the manager dispatches and the verbatim prompt templates for each role.

The manager dispatches one of these roles per task; the SKILL.md workflow says when.

## Role mapping

| Role | Agent file | Responsibility |
| --- | --- | --- |
| manager | (the main agent itself) | No file edits. Dispatches and reviews. |
| implementer | `agents/coder.md` | Writes production code or docs per task spec. |
| spec reviewer | `agents/reviewer.md` | Read-only check that code matches the supplied task spec. |
| quality reviewer | `agents/reviewer.md` | Read-only lightweight repo-style check. |
| tester | `agents/tester.md` | Test work, only when explicitly required by the plan. |
| docs subagent | `agents/planner.md` (or general-purpose) | All `docs/CHANGELOG.md` edits and other docs. |

Other repo agents exist for different workflows: `agents/architect.md`, `agents/integrator.md`, `agents/maintainer.md`, `agents/monitor.md`, `agents/orchestrator.md`, `agents/parallelizer.md`, `agents/scheduler.md`. This skill does not dispatch them. It uses plain execution terms such as lane, dependency, workstream, and parallel dispatch when reducing wall time, and uses additional redundant reviewers or multi-role coordination only when the approved plan explicitly calls for it.

## Implementer subagent prompt template

Paste this prompt to the dispatched `coder` subagent (or `general-purpose` if `coder` is unavailable). Replace `[FULL TASK TEXT]` and `[CONTEXT]` verbatim from the plan. Do not paraphrase or summarize. The manager launches the subagent with this exact prompt so the implementer has complete, unambiguous requirements and understands their task boundaries.

```text
You are implementing: [TASK NAME]

## Task description

[FULL TASK TEXT FROM PLAN, PASTED VERBATIM]

## Context

[SCENE-SETTING: where this fits, dependencies, repo style summary]

## Hard rules

- Tabs only for Python indentation; never spaces.
- Avoid `try`/`except`; if needed, keep to two lines max.
- No `assert` statements in plain `.py` scripts or library modules; only inside `tests/` or `tests_e2e/`.
- Use `dict[key]` when the key must exist; do not use `dict.get(key, fallback)` to hide bugs.
- ASCII only; escape Greek letters as `&alpha;` etc.
- Run focused pytest under `tests/` via `source source_me.sh && pytest tests/ -k <changed_file>`. Documentation-only changes do not require pytest runs.
- Do NOT commit. Only humans run `git commit`.
- Do NOT write outside the task scope.
- Follow `docs/PYTHON_STYLE.md`, `docs/PYTEST_STYLE.md`, `docs/REPO_STYLE.md`, and `docs/MARKDOWN_STYLE.md`.

## Self-review checklist

- Is the task description fully addressed? Check each requirement against your changes.
- Did you follow repo style? Lint with pyflakes; verify indentation, imports, and naming.
- Did you avoid scope creep? Stick to the task; do not refactor beyond the boundary.
- Did you avoid try/except unless truly needed? If catching exceptions, keep it under two lines.
- Did tests pass? Run `source source_me.sh && pytest tests/ -k <changed_file>` and confirm no failures.
- Are tests verifying behavior, not mocks? Check that assertions test actual output, not call counts.
- If changes are user-visible or architectural, flag it in your report so the manager can dispatch a docs subagent for `docs/CHANGELOG.md`.

## Report format

- Status: one of `DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT`.
- Files changed: list of absolute file paths.
- Tests run: exact commands and pass/fail outcomes.
- Self-review findings: short summary of discipline checks (YAGNI, style, scope).
- Concerns: blockers, ambiguity, scope creep, or missing context.
```

Notes for the manager: pass `[FULL TASK TEXT]` from the plan verbatim. Do not silently rewrite or paraphrase requirements; surface ambiguity or missing context to the user before dispatching the subagent.

## Spec reviewer subagent prompt template

This is a read-only spec-compliance check. The reviewer will NOT modify any files. The manager pastes the same task description that was given to the implementer below, so the reviewer can compare the latest diff against the original requirements exactly as stated. The reviewer's job is to verify that what was implemented matches what was asked for, nothing more and nothing less.

```text
You are reviewing: [TASK NAME]

## Task description (the spec)

[FULL TASK TEXT FROM PLAN, PASTED VERBATIM]

## Diff to review

[git diff or list of changed files; manager fills in]

## Your job

- Read the diff and confirm the code matches the supplied task spec exactly.
- Flag missing requirements: what the spec asks for that is NOT in the diff.
- Flag unrequested additions: what is in the diff that the spec did NOT ask for.
- Do NOT comment on style or quality. That is a separate review pass.
- Do NOT modify any files. This is a read-only review.

## Output format

Verdict: SPEC_COMPLIANT or SPEC_GAPS

Missing: (bullet list of unmet spec requirements with file:line references when possible)
- [requirement]: not found in [file]
- [requirement]: needs clarification

Extra: (bullet list of additions not in the spec)
- [addition]: added to [file] but not requested in spec
- [addition]: unclear purpose or scope

Notes: (short remarks if any)
- [observation about approach, assumptions, or edge cases]
- [question for the implementer if needed]
```

Notes for the manager: pass the same `[FULL TASK TEXT]` that was given to the implementer so the reviewer compares the actual diff to the original spec. If the verdict is `SPEC_GAPS`, re-dispatch the implementer to address the `Missing` and `Extra` items, then re-dispatch the spec reviewer. Do not run quality review until the spec reviewer reports `SPEC_COMPLIANT`.

## Quality reviewer subagent prompt template

This template is for a lightweight, single-pass code-style review against vosslab repository rules. It is intentionally narrower than the `/audit-code-reviewer` skill, which dispatches six parallel review subagents (spec, test, perf, maintainability, security, docs). This template performs ONE read-only quality pass focused on repo-style conformance.

```text
You are reviewing: [TASK NAME]

## Diff to review

[git diff or list of changed files; manager fills in]

## Scope

- One pass only.
- Lightweight repo-style check against docs/PYTHON_STYLE.md and docs/PYTEST_STYLE.md.
- Do NOT perform a multi-pass audit; that is the role of `/audit-code-reviewer`.
- Do NOT modify any files. This is read-only inspection only.
- Do NOT re-check spec compliance; that is the spec reviewer's job.

## Checks (vosslab focus)

- Tabs vs spaces for Python indentation (vosslab uses tabs exclusively; PEP 8's spaces are not used).
- try/except overuse (discouraged; max two-line cases when necessary).
- dict.get(key, default) patterns that hide missing-required-key bugs (use dict[key] when key must exist).
- assert statements in plain .py scripts or library modules (only tests/test_*.py and tests_e2e/ may use assert).
- Brittle pytest assertions (dates, collection sizes, required-key lists, hardcoded defaults, tunable constants, dataclass storage).
- Pytest runtime budget (each test under one second; slower work belongs in tests_e2e/).
- ASCII compliance (escape Greek letters as &alpha;, &beta;, etc.; no UTF-8 symbols).
- Shebang policy (executable scripts only; library modules, helper files, __init__.py, and test files do not get shebangs).
- Argparse minimalism (no flags users do not change between runs; avoid "what if someone wants to..." parameters).

## Output format

- Verdict: QUALITY_APPROVED or QUALITY_ISSUES.
- Important: bullet list of issues likely to cause bugs or repo-rule violations, with file:line references.
- Nit: bullet list of small style cleanups, with file:line references.
- Notes: short remarks if any.
```

Notes for the manager: run this quality review only after the spec reviewer reports SPEC_COMPLIANT. If the verdict is QUALITY_ISSUES and any issues are tagged Important, re-dispatch the implementer to fix them, then re-dispatch the quality reviewer for a second pass. Treat Nit items as optional; the manager decides whether to require a fix or let them slide.
