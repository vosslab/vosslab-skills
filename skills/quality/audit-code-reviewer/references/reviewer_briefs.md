# Reviewer briefs

Use this reference after the coordinator has gathered minimal raw context. Give
each fresh reviewer the same shared material and only the relevant brief, so
each reviewer forms its own conclusion from raw evidence.

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
- Recommend fewer permanent tests. Check each new test idea against the
  permanent-test checklist in docs/PYTEST_STYLE.md; route ideas that fall
  short to tests/_temp/ as one-time checks and label them temporary.
- Question requirements and gates before enforcing them. Report arbitrary
  thresholds, byte or pixel equivalence, exhaustive matrices, and gates that
  lack a failure plan, each with the grounded requirement to use instead.
```

## Plan reviewer

Check the request or plan's requirements, acceptance criteria, non-goals,
sequencing, and architecture. Report scope creep, skipped work, contradictions,
or partial-migration risk.

Keep requirements and gates grounded in reality. Confirm each gate ties to
product behavior, correctness, security, repository policy, a measured
constraint, or a demonstrated failure, and report the rest with the grounded
requirement to use instead. Treat byte-equivalence or pixel-equivalence
expectations on a plan that improves its output, and thresholds such as "must
load in under 400ms", as findings. Confirm every new gate carries a failure
plan: the decision or concrete recovery that follows when it fails, so the
gate earns its place.

Apply KISS aggressively. Report mechanisms, abstractions, policies, state, and
tests as findings when the plan shows no demonstrated need for them, and
recommend clear boundaries, stable domain concepts, and replaceable components
so unexpected cases can be handled later. Robustness means the software keeps
functioning despite imperfect inputs, data, state, or behavior; expect
imperfections handled by context and impact with graceful recovery that
preserves useful operation.

## Test reviewer

Treat tests as liabilities as well as assets. Every permanent test constrains
future design and must earn its place through the permanent-test checklist in
docs/PYTEST_STYLE.md, with docs/E2E_TESTS.md, docs/REPO_STYLE.md, and any
tests/TESTS_README.md or devel/DEVEL_README.md as further authorities. When in
doubt, remove the test.

Classify every test inside the boundary as permanent-worthy, a tests/_temp/
one-time check, or a deletion. Report implementation proof that landed in the
permanent suite, and tests that needed a hack the user left unrequested;
question the test before the hack. Prefer deleting fragile tests over adding
coverage. Report slow tests; real processes, networks, external tools, or
elaborate workflows in the fast pytest lane; unstable assertions on dates,
inventories, defaults, names, order, or incidental storage; trivial wrappers;
and tests unlikely to survive ordinary refactoring.

Propose at most one new permanent test, when a real changed-code bug could
plausibly slip through and the checklist passes. Route every weaker case to
tests/_temp/, labeled temporary and kept outside Git tracking.

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
