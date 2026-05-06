---
name: review-code-changes
description: Require independent review by parallel subagents for code changes and combine their
  findings. Use when a user asks Codex for independent review of changed code, validation of a
  completed implementation, plan conformance review, test coverage review, or documentation-impact
  review after a code change.
---

# Review code changes

## Overview

Use this skill to turn a code-change review into four independent review passes run by separate
subagents. The main agent is the review coordinator: gather shared context, launch independent
review subagents with separate scopes, wait for their results, then merge their findings into a
single concise review.

## Required behavior

- Launch subagents for independent review passes. The purpose of this skill is independent review.
- Treat the main agent as coordinator and integrator, not as the sole reviewer.
- Keep main-agent preflight minimal. Gather only enough context to launch the subagents.
- Send each subagent the raw shared context and its assigned scope, without telling it the expected
  conclusion.
- Wait for the subagent results before delivering the final review.
- If subagents are unavailable, state that independent review could not be performed and stop with
  the gathered context plus the reason.

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
2. Launch four independent review subagents in parallel immediately after the minimal shared
   context is ready. Use the reviewer names below so each pass has a concrete identity and scope.
   Give each subagent the same shared context plus its specific scope. Ask subagents for findings
   only, with file and line references when possible.
3. While subagents run, prepare the integration shell only: finding severity order, changed-file
   list, test-evidence list, and documentation-evidence list.
4. Wait for all review subagents to return, unless one fails irrecoverably. If a subagent fails,
   include that missing review pass as residual risk.
5. Merge returned findings by severity. Remove duplicates, keep the clearest evidence, and preserve
   dissent when reviewers disagree.
6. Deliver a code-review response: findings first, then open questions or assumptions, then a brief
   test/documentation summary.

## Review agents

### Reviewer 1: Plan auditor

Launch `Plan auditor` to verify that the current plan, ticket, or user request was implemented
according to its stated design philosophy and scope.

Review focus:
- Requirements, acceptance criteria, and non-goals.
- Whether the implementation matches the plan's sequencing and architecture.
- Scope creep, skipped work, or behavior that contradicts the plan.
- Risks from partial migrations or incomplete cleanup.

### Reviewer 2: Test auditor

Launch `Test auditor` to review smoke and unit test coverage against repo test style.

Review focus:
- Whether changed behavior has focused tests.
- Whether smoke tests cover the user-facing workflow.
- Whether tests follow `docs/PYTEST_STYLE.md` when present, otherwise the pytest section in
  [docs/PYTHON_STYLE.md](../../docs/PYTHON_STYLE.md).
- Fragile pytest patterns, over-broad assertions, order dependence, sleeps, hidden network or file
  system coupling, and tests that pass without validating the changed behavior.
- Missing focused test commands or unclear test evidence.

### Reviewer 3: Style auditor

Launch `Style auditor` to review changed code against implementation style guides.

Review focus:
- Python style from [docs/PYTHON_STYLE.md](../../docs/PYTHON_STYLE.md) when Python changed.
- Repo-wide style from [docs/REPO_STYLE.md](../../docs/REPO_STYLE.md).
- Naming, file placement, dependency choices, command examples, and generated-output handling.
- Maintainability issues introduced by the patch, including unclear ownership boundaries or
  unnecessary abstractions.

### Reviewer 4: Docs auditor

Launch `Docs auditor` to identify existing documentation that should be updated because of the code
change.

Review focus:
- README, install, usage, architecture, file structure, changelog, troubleshooting, and plan docs.
- User-visible behavior changes missing from docs.
- New commands, dependencies, outputs, files, or workflows missing from docs.
- Stale documentation contradicted by the patch.

## Agent prompt template

Use this template for each independent review subagent, replacing the bracketed reviewer and scope
text:

```text
You are [reviewer name]. Perform an independent review of this code change from one focused angle:
[scope].

Shared context:
- User request: [brief request]
- Relevant plan or ticket: [path or none found]
- Changed files: [paths]
- Repo rules read: [paths]
- Test evidence so far: [commands and results]
- Suggested review range, if known: [working tree, staged diff, commit range, or unknown]

Instructions:
- Return findings only when there is a concrete issue.
- Include file and line references when possible.
- Include severity: blocker, high, medium, or low.
- Include any missing evidence that blocks confidence.
- Keep the review focused on your assigned scope.
- Do not assume the main agent has already reviewed this scope.
- Perform any deeper history, plan, diff, or call-site inspection needed for your assigned scope.
- Make this an independent review: form your own conclusions from the provided artifacts.
```

## Output guidance

Lead with findings, ordered by severity. For each finding, include the issue, evidence, impact, and
the smallest useful fix. After findings, include open questions or assumptions, then a short summary
of tests and documentation status.

If all review passes find no issues, say that clearly and list any residual risk such as missing
test evidence, unavailable docs, or areas that were not reviewed.
