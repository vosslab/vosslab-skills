---
name: prune-tests
description: Aggressively delete permanent tests and reduce suite size and complexity across languages and frameworks. Use for aggressive test removal or suite reduction, retaining only protection with exceptional, demonstrated long-term value.
---

# Aggressive test removal

Assume the repository contains far too many permanent tests. Aggressively delete them. Spend effort
finding reasons to remove tests. Preserve only tests with exceptional, demonstrable long-term value.
Passing tests receive no special protection. When in doubt, remove the test.

Tests created to verify an implementation, debug a problem, or support a refactoring are temporary
by default. Once that work is complete, their continued existence requires exceptional
justification. Their original usefulness does not justify permanent retention. The primary outcome
is a dramatically smaller permanent suite with substantially less testing complexity.

## Establish the scope

- Default to the current repository's permanent suite when the user supplies no narrower scope.
  Apply the same deletion standard across languages, frameworks, and test lanes.
- Read applicable repository testing and development rules. Identify the suite's entrypoints,
  supporting infrastructure, and existing collection and execution commands. Include inline and
  colocated tests, not just files under `tests/`. Preserve production code in files shared with tests.
- Record a comparable starting inventory so the final report can show the reduction achieved.

## Delete whole groups first

Evaluate entire suites and test modules for deletion before examining individual tests. Prefer
removing whole groups of marginal-value tests and their supporting infrastructure. Treat every test
as a deletion candidate, including well-written tests that currently pass.

- Delete fragile, redundant, trivial, speculative, obsolete, implementation-specific, and
  marginal-value tests.
- Delete tests that freeze changeable behavior, internal organization, tunable defaults,
  incidental formatting, or completed implementation details.
- Target arbitrary thresholds, unnecessary byte or pixel equivalence, exhaustive matrices, and
  version-only gates. Retain such constraints only when an actual product requirement establishes
  their exceptional value.
- Question tests that demand unrequested implementation hacks or obstruct appropriate recovery
  from imperfect inputs.
- Remove gates whose failure identifies no meaningful correctness problem and leads to no
  concrete decision or recovery action.
- Perform deletions directly within the authorized scope. Do not rescue, rewrite, replace,
  archive, or skip unwanted tests.
- Remove fixtures, snapshots, helpers, and test-only configuration made unused by deletion. Check
  remaining consumers before removing shared support.

## Require exceptional retention value

Every retained test must earn its place. The absence of an obvious reason to delete a test is not a
reason to keep it. Uncertainty favors deletion.

Retain a test only when its actual assertions provide substantial, unique protection for important,
intentionally stable behavior, with demonstrable value exceeding its maintenance cost. Identify
the concrete failure those assertions detect and why that protection deserves to remain.

Critical workflows, scientific correctness, security, and data integrity are strong candidates;
category labels and hypothetical regressions do not establish value by themselves.

## Verify and report

- Check remaining collection and run affected retained tests with the repository's tooling.
  Resolve dangling references caused by deletion. Impose no arbitrary coverage requirements or
  deletion quotas.
- Use ignored `/tests/_temp/` under the repository root for temporary checks supporting cleanup;
  remove those checks before completion. Keep genuine product defects and important coverage gaps
  separate from cleanup results rather than using them to justify speculative replacement tests.
- Report the reduction achieved, complexity eliminated, concrete justification for retained
  protection, important gaps and product defects, and verification performed, including failures
  or checks not run. Group shared retention justifications concisely while accounting for every
  retained test.
