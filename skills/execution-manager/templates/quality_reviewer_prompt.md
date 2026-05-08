# Quality reviewer subagent prompt template

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

## Notes for the manager

- Run this quality review only after the spec reviewer reports SPEC_COMPLIANT.
- If the verdict is QUALITY_ISSUES and any issues are tagged Important, re-dispatch the implementer to fix them, then re-dispatch the quality reviewer for a second pass.
- Treat Nit items as optional; the manager decides whether to require a fix or let them slide.
