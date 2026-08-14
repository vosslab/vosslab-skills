---
name: old-python-code-review
description: "Single-pass Python correctness, security, and style review on demand; not for multi-reviewer audits before merge (use audit-code-reviewer for that)."
---

# Old Python Code Review

## Workflow
1. Apply `repo-rules-reader` to the requested repo rule files. For the default review baseline, read
   `AGENTS.md`, `docs/REPO_STYLE.md`, `docs/PYTHON_STYLE.md`, `docs/PYTEST_STYLE.md` when present,
   and `docs/CHANGELOG.md`.
2. Extract the review-relevant rules, especially how to run Python, Python style, pytest style,
   repo workflow rules, and the latest changelog entry.
3. Inspect changed files first (`git diff`, `git status --short`), then inspect related call sites.
4. If the repo has `docs/active_plans/`, identify the active plan document(s) that govern the
   change. Otherwise, skip plan-conformance steps.
5. If an active plan exists, map code and tests to plan requirements, acceptance criteria, and
   stated constraints. Otherwise, skip this step.
6. Prioritize findings by severity: plan mismatch/regressions when applicable,
   correctness/safety, then maintainability.
7. Provide concrete, minimal fixes with before/after examples when a fix is straightforward.
8. Flag uncertainty explicitly and ask targeted review questions for unclear logic or contracts.

## Review Output Contract
- Report findings first, ordered by severity.
- For each finding include:
  - Severity (`P1` critical, `P2` high, `P3` medium, `P4` low)
  - File path and line reference
  - Risk and likely impact
  - Recommended change
- After findings, include:
  - Open questions
  - Test gaps and residual risk
  - Brief summary

## What To Check
- Prefer design-level fixes over symptom patches; cite `docs/REPO_STYLE.md` when flagging this.
- Plan conformance: implementation and tests match active plan scope, ordering, and acceptance
  criteria.
- Plan drift: behavior changed without corresponding plan/changelog updates, or plan claims
  complete while code is partial.
- Correctness: edge cases, off-by-one logic, stale assumptions, API misuse, compatibility breaks.
- Security: unsafe eval/exec, command injection, path traversal, deserialization hazards, and weak
  validation.
- Maintainability: dead code, hidden coupling, unclear naming, duplicated logic, brittle tests.
- Python style: tabs for indentation, import module names rather than imported symbols when
  practical, no relative imports, direct required-key access, minimal try/except, shebangs only on
  runnable scripts, and `source source_me.sh && python ...` command examples.
- Pytest style: small deterministic tests, plain asserts, stable behavior-focused expectations,
  `tmp_path` for filesystem tests, and no assertions on dates, collection sizes, required key
  lists, hardcoded defaults, function names, or other fragile details.
- Performance only when materially relevant.

## Fix Guidance
- Prefer small, local edits that preserve behavior unless a bug requires behavior change.
- Keep fixes aligned with repo Python style and test conventions.
- Add or adjust tests for each behavior-changing fix.
