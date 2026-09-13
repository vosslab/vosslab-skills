# Reviewer briefs

Use this reference after the coordinator has gathered minimal raw context. Give
each fresh reviewer the same shared material and only the relevant brief. Do not
provide suspected defects, intended conclusions, or a proposed fix.

## Common prompt

```text
You are [reviewer name]. Perform an independent review of this code change from one focused angle:
[scope].

Shared context:
- User request: [brief request]
- Relevant plan or ticket: [path or none found]
- Changed files: [paths]
- Repo rules read: [paths]
- Test evidence so far: [commands and results]
- Suggested review boundary, if known: [paths, supplied diff, or unknown]

Instructions:
- Return findings only when there is a concrete issue.
- Include file and line references when possible.
- Include severity: blocker, high, medium, or low.
- Include missing evidence that blocks confidence.
- Keep the review focused on the assigned scope.
- Form your own conclusion from the supplied artifacts.
```

## Plan reviewer

Check the request or plan's requirements, acceptance criteria, non-goals,
sequencing, and architecture. Report scope creep, skipped work, contradictions,
or partial-migration risk.

## Test reviewer

Apply the repository's pytest and E2E authorities. Prefer deleting fragile tests
over adding coverage. Flag slow tests; real processes, networks, external tools,
or elaborate workflows in the fast pytest lane; unstable assertions on dates,
inventories, defaults, names, order, or incidental storage; trivial wrappers;
and tests unlikely to survive ordinary refactoring. Only after pruning, identify
a small, concrete missing pure-function test when a real changed-code bug could
plausibly slip through.

## Style reviewer

Review changed code against applicable repository and language style authorities.
Check naming, placement, dependencies, command examples, generated-output
handling, ownership boundaries, unnecessary abstraction, and maintainability.

## Documentation reviewer

Identify documentation that the change makes stale or newly necessary: README,
installation, usage, architecture, file structure, changelog, troubleshooting,
plans, commands, dependencies, outputs, or user-visible behavior.

## Legacy reviewer

Find dead imports, code, branches, flags, configuration, compatibility shims,
TODO/FIXME notes, disabled tests, commented-out blocks, duplicate helpers, and
dependencies no longer referenced after the change. Favor a lean result over
compatibility residue with no demonstrated owner.

## Comment reviewer

Apply applicable commenting authority. Check nontrivial intent comments and
expected docstrings; clear descriptive names; visual separators where local
Python style requires them; ASCII-safe comments; readable control flow; and
stale or redundant comments. Do not allow temporary workstream or milestone tags
in permanent comments.
