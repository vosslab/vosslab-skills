---
name: unit-test-starter
description: Add focused Python pytest coverage when a repository needs behavior-level tests; not for mechanical test-per-file generation or whole-system workflows.
---

# Unit test starter

Create small, durable Python pytest coverage from repository evidence. This skill
is for a bounded coverage task or an intentional repository-wide testing pass;
it is not a request to mirror every source file with a test or to test incidental
implementation details.

## Start with the test contract

Read the target repository's pytest policy and test configuration before choosing
coverage. Follow its test lanes, permanent-test criteria, command conventions,
and import arrangements. If this repository provides them, read:

- `docs/PYTEST_STYLE.md` for what merits permanent coverage and fragile-test
  exclusions.
- `docs/E2E_TESTS.md` when a proposed case might require a whole-system or
  browser workflow.
- `docs/PYTHON_STYLE.md` before writing Python tests.

Keep permanent tests offline, deterministic, and focused on observable behavior.
Use `tmp_path` for test-owned filesystem contracts. Do not add a permanent test
for dates, inventories, hardcoded defaults, internal names, unstable output, or
other incidental structure unless the repository declares it a contract.

## Scope and triage

1. Identify the requested modules, existing tests, repository test configuration,
   and safe import boundary. Ask only when the requested boundary cannot be
   inferred from the task and repository.
2. Inspect the code and existing tests before deciding which behavior is worth
   protecting. Prefer pure functions, explicit errors, data invariants, and
   isolated filesystem behavior.
3. Do not import a module whose import performs uncontrolled I/O, network work,
   subprocess execution, or other unsafe side effects. Record a precise reason
   when behavior cannot safely receive pytest coverage.
4. Put real-process, service, browser, or whole-system checks in the repository's
   E2E lane when they earn permanent coverage; use temporary verification when
   they only prove the present implementation.
5. Add only coverage that survives the permanent-test decision. A source file
   without a justified test needs no placeholder test module or blanket skip.

## Write and verify

- Prefer table-driven tests where several inputs demonstrate one contract.
- Assert a few stable results or invariants; use `pytest.raises` for explicit
  error contracts.
- Keep import setup repository-wide and minimal. Add `tests/conftest.py` only
  for a genuine shared import or environment boundary, never as a per-test hack.
- Run focused tests after each coherent change, then report the command, result,
  behaviors covered, and deliberately untested behavior with reasons.

For detailed source discovery, mapping, import setup, test construction, and
incremental-run procedure, read
[Python pytest workflow](references/python_pytest_workflow.md) when performing a
multi-module or repository-wide coverage pass.

## Completion

Return the tests added or changed, the behavior each protects, skipped or
uncovered behavior and its reason, and focused test evidence. Flag a design
problem rather than papering it over with a fragile test.

When delegated execution is explicitly requested, give one fresh subagent one
bounded testing task and one verification step. The manager workflow owns
general delegation mechanics.
