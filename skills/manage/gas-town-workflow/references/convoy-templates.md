# Convoy templates

Ready-made task sequences for common Gas Town workflows. Copy and adapt these templates when creating convoys.

## Task description format

Every task in a convoy uses this format:

```
Role: coder | tester | reviewer | integrator | ...
Convoy: <initiative-name>
Done when:
- <objective criterion 1>
- <objective criterion 2>
```

Tag the target role in the task subject:

```
[CODER] Implement token refresh flow
[TESTER] Write tests for token refresh
[REVIEWER] Audit refresh flow changes
```

## Feature convoy

A standard feature implementation from plan to merge.

| Step | Subject | Role | Blocked by |
| --- | --- | --- | --- |
| 1 | [PLANNER] Write implementation plan for <feature> | planner | -- |
| 2 | [CODER] Implement <feature> per approved plan | coder | Step 1 |
| 3 | [TESTER] Write tests for <feature> | tester | Step 2 |
| 4 | [REVIEWER] Review <feature> code and tests | reviewer | Step 2, Step 3 |
| 5 | [INTEGRATOR] Merge <feature> branch | integrator | Step 4 |

### Example task descriptions

Step 1:
```
Role: planner
Convoy: token-refresh
Done when:
- Plan document exists with acceptance criteria
- Architect has approved design decisions
```

Step 2:
```
Role: coder
Convoy: token-refresh
Done when:
- All plan items implemented
- Code passes pyflakes lint
- No failing tests introduced
```

## Bugfix convoy

A standard bugfix from triage to merge.

| Step | Subject | Role | Blocked by |
| --- | --- | --- | --- |
| 1 | [CODER] Triage and fix <bug description> | coder | -- |
| 2 | [TESTER] Add regression test for <bug description> | tester | Step 1 |
| 3 | [REVIEWER] Review <bug> fix and regression test | reviewer | Step 1, Step 2 |
| 4 | [INTEGRATOR] Merge <bug> fix branch | integrator | Step 3 |

## Review gate template

A reviewer checklist for convoy gates.

```
Role: reviewer
Convoy: <initiative-name>
Done when:
- Code matches approved plan (no drift)
- All tests pass
- No new pyflakes warnings
- No security issues identified
- Changes are minimal and focused
```

## Maintenance convoy

A cleanup or housekeeping pass.

| Step | Subject | Role | Blocked by |
| --- | --- | --- | --- |
| 1 | [MAINTAINER] Run lint cleanup on <scope> | maintainer | -- |
| 2 | [TESTER] Verify no regressions after cleanup | tester | Step 1 |
| 3 | [REVIEWER] Review cleanup changes | reviewer | Step 1, Step 2 |

## Stabilization convoy

A debugging and stabilization pass for failing tests or broken features.

| Step | Subject | Role | Blocked by |
| --- | --- | --- | --- |
| 1 | [TESTER] Identify and document failing tests | tester | -- |
| 2 | [CODER] Fix identified failures | coder | Step 1 |
| 3 | [TESTER] Verify fixes and confirm no regressions | tester | Step 2 |
| 4 | [REVIEWER] Review stabilization changes | reviewer | Step 2, Step 3 |
