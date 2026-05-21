---
name: audit-code-reviewer
description: "Parallel multi-reviewer audit launched before merge or release; not for single-pass review."
---

# Review code changes

## Overview

Use this skill to turn a code-change review into six independent review passes run by separate
subagents. The main agent is the review coordinator: gather shared context, launch independent
review subagents with separate scopes, wait for their results, then merge their findings into a
single concise review.

## Required behavior

- Prefer design-level fixes over symptom patches; cite `docs/REPO_STYLE.md` when flagging this.
- Launch subagents for independent review passes. The purpose of this skill is independent review.
- Treat the main agent as coordinator and integrator, not as the sole reviewer.
- Keep main-agent preflight minimal. Gather only enough context to launch the subagents.
- Send each subagent the raw shared context and its assigned scope, without telling it the expected
  conclusion.
- Wait for the subagent results before delivering the final review.
- If subagents are unavailable, state that independent review could not be performed and stop with
  the gathered context plus the reason.
- Do the fixes that make sense. After merging findings, apply obvious low-risk fixes directly;
  leave blockers, contested fixes, and architecture-level changes for the user.

## Workflow

1. Gather shared context before launching agents:
   - User request and any referenced plan document.
   - `git status --short` and the relevant `git diff`.
   - Repo rule files that exist, especially `AGENTS.md`,
     `docs/REPO_STYLE.md`,
     `docs/PYTHON_STYLE.md`, `docs/PYTEST_STYLE.md` when present,
     `docs/MARKDOWN_STYLE.md`, and
     `docs/CHANGELOG.md`.
   - Focused test commands already run and their results, if available.
2. Launch six independent review subagents in parallel immediately after the minimal shared
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
7. Do the fixes that make sense. After delivering findings, apply the obvious low-risk fixes
   (typos, missing comments, stale doc lines, dead imports, fragile pytest deletions flagged by
   Test auditor). Skip fixes that require design judgment, cross-file coordination, or user input.

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

Launch `Test auditor` to prune fragile pytests and route elaborate scenarios to E2E, keeping
`tests/` fast and stable. Less is more: the default action is removal, not addition.

Review focus:
- Goal: remove fragile pytests. Do not propose new pytests unless a missing one is the root cause
  of a real correctness bug in the changed code.
- Flag pytests that take more than ~1 second, or that look like they would: sleeps, real
  subprocess calls, real filesystem trees beyond `tmp_path`, network calls, large fixtures, or
  model loads.
- Flag elaborate end-to-end scenarios sitting in `tests/`: whole-script CLI runs, I/O round trips,
  real external tools. These belong in `tests/e2e/` per
  `docs/E2E_TESTS.md`, not in pytest. Recommend moving or deleting, not
  rewriting in place.
- Flag fragile assertions per `docs/PYTEST_STYLE.md`: dates,
  collection sizes, lists of required keys, hardcoded defaults, tunable constants, dataclass
  storage, function-name strings, and over-broad or order-dependent assertions.
- Flag tests of trivial behavior, thin stdlib wrappers, `_temp.*` files, or tests that will not
  still pass next week without code changes.
- Only after pruning, note any genuinely missing pure-function pytest where a real bug could
  plausibly slip through. Keep this list small and concrete.

### Reviewer 3: Style auditor

Launch `Style auditor` to review changed code against implementation style guides.

Review focus:
- Python style from `docs/PYTHON_STYLE.md` when Python changed.
- Repo-wide style from `docs/REPO_STYLE.md`.
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

### Reviewer 5: Legacy/dead-code auditor

Launch `Legacy auditor` to find unused code, dead branches, and legacy cruft introduced or left
behind by the change. Goal: prevent feature drift and keep the code lean.

Review focus:
- Functions, classes, imports, files, flags, or config keys that are no longer referenced after
  the change.
- Superseded code paths, compatibility shims, or TODO/FIXME notes that should be removed now that
  the change has landed.
- Duplicate implementations or near-duplicate helpers that should be consolidated.
- Disabled tests, commented-out blocks, and unreachable branches.
- Dependencies in `pip_requirements.txt`, `Brewfile`, or similar that no code references anymore.

### Reviewer 6: Comment auditor

Launch `Comment auditor` to confirm changed code is well commented and easy to read. Anchor
the review in `docs/PYTHON_STYLE.md` commenting rules when Python
changed.

Review focus:
- Non-trivial logic has a short comment above it explaining intent.
- Function and module docstrings present where the style guide expects them, using Google style
  for Python.
- Variable, function, and file names are descriptive and match repo naming conventions.
- Visual function separators (`#====`) used in Python where the style guide expects them.
- No emoji or non-ASCII characters in comments; UTF-8 escaped where needed.
- Overly long functions, deeply nested logic, or unclear control flow that hurts readability.
- Stale, misleading, or redundant comments that contradict the code.

## Subagent dispatch

Dispatch a fresh subagent for each atomic task. Reusing a subagent across tasks
carries stale context, encourages drift, and weakens independent judgment.
`SendMessage` is for status only; do not use it to chain follow-on editing
work onto a teammate that has already finished its assigned task. See
`docs/REPO_STYLE.md`.

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
