# Parallel dispatch examples

Use this reference when an approved plan contains workstreams, work packages,
`Depends on:` lines, or a parallel-plan-ready milestone. The goal is to teach
the manager how to exploit existing parallel structure in the plan, not how
to invent new structure.

Role names below match `role-catalog.md`: implementer, spec reviewer,
quality reviewer, tester, docs subagent.

## Example 1: Independent implementation lanes

Plan shape:

- WP-A: docs update. Depends on: none. Owner: docs subagent.
- WP-B: test harness. Depends on: none. Owner: tester.
- WP-C: implementation. Depends on: none. Owner: implementer.
- WP-D: integration. Depends on: WP-B, WP-C. Owner: implementer.

Manager dispatch:

1. Create all four tracked tasks via `TaskCreate`, with `addBlockedBy` for WP-D.
2. Dispatch WP-A, WP-B, and WP-C concurrently (three fresh subagents).
3. Run spec review and quality review after each implementation task lands.
4. Wait on WP-B and WP-C completed-and-reviewed before dispatching WP-D.
5. Dispatch the docs closeout subagent after WP-D so the changelog can quote
   the final integrated diff.

Why this is safe:

- No shared file ownership across the three independent lanes.
- Dependencies are explicit (`Depends on: WP-B, WP-C`).
- Review paths are independent until integration.

## Example 2: Shared file forces sequencing

Plan shape:

- WP-A and WP-B both touch `src/config.ts`.
- Neither has `Depends on:`, but both edit the same file.

Manager dispatch:

1. Dispatch only WP-A first.
2. State the sequencing reason in the dispatch note: shared file ownership on
   `src/config.ts`.
3. Dispatch WP-B after WP-A is reviewed, or after the plan is split by
   ownership (e.g., one task owns the file and the other consumes its
   exports).

Why this is serial:

- Parallel edits to the same file would create integration risk that
  read-only manager review cannot resolve without dispatching a follow-up
  coder.

## Example 3: Tester lane runs beside implementation

Plan shape:

- WP-A: implement feature module. Owner: implementer.
- WP-B: write regression tests from the accepted contract. Owner: tester.
- WP-C: wire feature into CLI. Depends on: WP-A. Owner: implementer.

Manager dispatch:

1. Dispatch WP-A and WP-B concurrently when the test contract is already
   clear in the plan.
2. Dispatch WP-C after WP-A is spec-and-quality-reviewed.
3. If WP-A changes the accepted contract during implementation, dispatch a
   small follow-up to the tester to update WP-B; do not silently rewrite the
   original task text.

Why this reduces wall time:

- Test scaffolding does not need to wait for implementation when the
  contract is already specified.
- The tester and implementer touch separate files (test files vs. feature
  module), so review paths stay independent.
