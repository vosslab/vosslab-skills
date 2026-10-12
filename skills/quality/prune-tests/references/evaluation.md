# Evaluate test protection

Ask: what meaningful defect could reach users or developers without this test, and would its actual
assertions fail for that reason? Inspect claimed protection rather than accepting a test's label.

## Compare protection with burden

Evaluate suites and modules before individual tests, considering fixtures, dependencies, runtime,
flakiness, coupling, and review overhead. Evaluate marginal protection: a test worth keeping in
isolation may be unnecessary when retained tests already establish the same behavior.

Simple, deterministic tests can justify retention when they protect important, stable behavior at
negligible maintenance cost. Scientific correctness, authorization, data integrity, and repository
invariants are examples, not protected categories. Retain only distinct assertions with worthwhile
protection.

Explicit ASCII or encoding restrictions and whitespace rules are deliberate repository requirements,
even when checked through source inspection. Distinguish these from incidental source inventories
or implementation-shape assertions. Judge the adopted requirement, actionable failures, redundancy,
and maintenance cost; neither source inspection nor simplicity makes a test trivial.

## Identify deletion candidates

- Remove fragile, redundant, trivial, speculative, obsolete, implementation-specific, and marginal
  checks, especially when their machinery dominates their protection.
- Remove assertions freezing changeable behavior, internal organization, tunable defaults,
  incidental formatting, or completed implementation details.
- Target arbitrary thresholds, unnecessary byte or pixel equivalence, exhaustive matrices, and
  version-only gates unless an actual product requirement or repository policy justifies them.
- Question tests demanding unrequested implementation hacks or obstructing appropriate recovery
  from imperfect inputs.
- Remove gates whose failure identifies no meaningful correctness or repository-policy violation
  and leads to no concrete decision or recovery action.

Tests created for debugging, refactoring, or implementation proof are temporary by default.
Their former usefulness does not justify permanent retention; continued protection needs a stable,
meaningful contract.

Prefer whole-module removal when the group provides little useful protection. For mixed or uncertain
groups, inspect assertions and distinct behaviors before deleting the module; costly scaffolding
does not condemn every case. Keep this review bounded. The burden of proof remains on retention,
and unresolved uncertainty favors deletion.
