---
name: review-code-changes
description: Launch focused parallel review agents for code changes and combine their findings.
  Use when a user asks Codex to review changed code, validate a completed implementation, check
  plan conformance, inspect test coverage, or identify documentation updates needed after a code
  change.
---

# Review code changes

## Overview

Use this skill to turn a code-change review into four focused parallel review passes. The main
agent gathers the shared context, launches review agents with separate scopes, then merges their
findings into a single concise review.

## Workflow

1. Gather shared context before launching agents:
   - User request and any referenced plan document.
   - `git status --short` and the relevant `git diff`.
   - Repo rule files that exist, especially `AGENTS.md`,
     [docs/REPO_STYLE.md](../../docs/REPO_STYLE.md),
     [docs/PYTHON_STYLE.md](../../docs/PYTHON_STYLE.md), `docs/PYTEST_STYLE.md` when present,
     [docs/MARKDOWN_STYLE.md](../../docs/MARKDOWN_STYLE.md), and
     [docs/CHANGELOG.md](../../docs/CHANGELOG.md).
   - Focused test commands already run and their results, if available.
2. Launch four review agents in parallel. Give each agent the same shared context plus its specific
   scope below. Ask agents for findings only, with file and line references when possible.
3. Continue local review while the agents run. Focus on integration risks and any areas outside the
   delegated scopes.
4. Merge returned findings by severity. Remove duplicates, keep the clearest evidence, and preserve
   dissent when reviewers disagree.
5. Deliver a code-review response: findings first, then open questions or assumptions, then a brief
   test/documentation summary.

## Review agents

### Plan implementation

Ask this agent to verify that the current plan, ticket, or user request was implemented according
to its stated design philosophy and scope.

Review focus:
- Requirements, acceptance criteria, and non-goals.
- Whether the implementation matches the plan's sequencing and architecture.
- Scope creep, skipped work, or behavior that contradicts the plan.
- Risks from partial migrations or incomplete cleanup.

### Test compliance

Ask this agent to review smoke and unit test coverage against repo test style.

Review focus:
- Whether changed behavior has focused tests.
- Whether smoke tests cover the user-facing workflow.
- Whether tests follow `docs/PYTEST_STYLE.md` when present, otherwise the pytest section in
  [docs/PYTHON_STYLE.md](../../docs/PYTHON_STYLE.md).
- Fragile pytest patterns, over-broad assertions, order dependence, sleeps, hidden network or file
  system coupling, and tests that pass without validating the changed behavior.
- Missing focused test commands or unclear test evidence.

### Code style compliance

Ask this agent to review changed code against implementation style guides.

Review focus:
- Python style from [docs/PYTHON_STYLE.md](../../docs/PYTHON_STYLE.md) when Python changed.
- Repo-wide style from [docs/REPO_STYLE.md](../../docs/REPO_STYLE.md).
- Naming, file placement, dependency choices, command examples, and generated-output handling.
- Maintainability issues introduced by the patch, including unclear ownership boundaries or
  unnecessary abstractions.

### Documentation impact

Ask this agent to identify existing documentation that should be updated because of the code
change.

Review focus:
- README, install, usage, architecture, file structure, changelog, troubleshooting, and plan docs.
- User-visible behavior changes missing from docs.
- New commands, dependencies, outputs, files, or workflows missing from docs.
- Stale documentation contradicted by the patch.

## Agent prompt template

Use this template for each review agent, replacing the bracketed scope text:

```text
Review this code change from one focused angle: [scope].

Shared context:
- User request: [brief request]
- Relevant plan or ticket: [path or none found]
- Changed files: [paths]
- Repo rules read: [paths]
- Test evidence so far: [commands and results]

Instructions:
- Return findings only when there is a concrete issue.
- Include file and line references when possible.
- Include severity: blocker, high, medium, or low.
- Include any missing evidence that blocks confidence.
- Keep the review focused on your assigned scope.
```

## Output guidance

Lead with findings, ordered by severity. For each finding, include the issue, evidence, impact, and
the smallest useful fix. After findings, include open questions or assumptions, then a short summary
of tests and documentation status.

If all review passes find no issues, say that clearly and list any residual risk such as missing
test evidence, unavailable docs, or areas that were not reviewed.
