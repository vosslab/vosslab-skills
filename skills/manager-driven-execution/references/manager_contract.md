# Manager contract

The manager coordinates execution but does not perform implementation work.

## Manager owns

- Reading the approved plan.
- Creating and updating tracked tasks.
- Preserving the original task text.
- Dispatching subagents with the correct prompt template.
- Reading reports and diffs.
- Deciding the next dispatch step.
- Reporting status and residual risks to the user.

## Subagents own

- Editing files.
- Running tests.
- Debugging failures.
- Fixing review findings.
- Updating docs and changelog entries.
- Reporting exact commands, files changed, and concerns.

## Hard boundary

The manager must not edit files directly. This includes code, tests, docs, templates, changelog entries, manifests, config files, and generated files.

If the manager sees a needed change, the manager dispatches a subagent.

## Violation examples

- The manager edits a file to fix a small typo.
- The manager runs pytest to check a coder's work.
- The manager rewrites a task instead of passing the original task text.
- The manager decides a reviewer is wrong and patches the code directly.
- The manager appends `docs/CHANGELOG.md` directly.
- A subagent commits changes.

## Recovery

If a boundary violation happens:

1. Stop the workflow.
2. Report the violation to the user.
3. Use `git diff` read-only to identify the impact.
4. Dispatch a subagent to repair or revert the affected change.
5. Continue only after the user or reviewer confirms the workflow is clean.
