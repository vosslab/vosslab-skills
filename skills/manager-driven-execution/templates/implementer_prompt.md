# Implementer subagent prompt template

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
- Follow [docs/PYTHON_STYLE.md](../../../docs/PYTHON_STYLE.md), [docs/PYTEST_STYLE.md](../../../docs/PYTEST_STYLE.md), [docs/REPO_STYLE.md](../../../docs/REPO_STYLE.md), and [docs/MARKDOWN_STYLE.md](../../../docs/MARKDOWN_STYLE.md).

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

## Notes for the manager

- The manager passes `[FULL TASK TEXT]` from the plan verbatim. Do not silently rewrite or paraphrase requirements; surface ambiguity or missing context to the user before dispatching the subagent.
