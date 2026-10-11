---
name: prune-tests
description: Reduce permanent test-suite maintenance burden across languages and frameworks by removing low-value tests and unnecessary support while preserving meaningful protection worth its upkeep.
---

# Prune test burden

Reduce permanent testing cost, not test count. Remove tests whose protection does not justify their
actual ongoing burden. Keep a simple, deterministic test when it protects stable, meaningful
behavior for little cost. Passing status alone neither protects nor condemns a test.

Tests created to verify an implementation, debug a problem, or support a refactoring are temporary
by default. Once that work is complete, their continued existence requires a meaningful stable
contract. Their original usefulness does not justify permanent retention. The outcome is a smaller,
simpler suite that still protects important behavior efficiently.

## Establish the scope

- Default to the current repository's permanent suite when the user supplies no narrower scope.
  Include all languages, frameworks, test lanes, and inline or colocated tests.
- Read applicable repository testing and development rules. Identify the suite's entrypoints,
  supporting infrastructure, collection commands, and execution commands.
- Record a comparable starting inventory: tests, support files, dependencies, runtime, and known
  flaky or environment-sensitive lanes. Preserve production code in mixed source/test files.

## Compare protection with burden

Evaluate suites and modules before individual tests. Remove whole groups that provide little useful
protection relative to their fixture, dependency, runtime, flakiness, or coupling cost.

- Delete fragile, redundant, trivial, speculative, obsolete, implementation-specific, and
  marginal-value tests, especially where their machinery dominates their protection.
- Delete tests that freeze changeable behavior, internal organization, tunable defaults,
  incidental formatting, or completed implementation details.
- Target arbitrary thresholds, unnecessary byte or pixel equivalence, exhaustive matrices, and
  version-only gates unless an actual product requirement gives them meaningful protection.
- Question tests that demand unrequested implementation hacks or obstruct appropriate recovery
  from imperfect inputs.
- Remove gates whose failure identifies no meaningful correctness problem and leads to no
  concrete decision or recovery action.

Simple, deterministic checks of scientific calculations, validation and decoding, serialization,
authorization, security, or data integrity often have low maintenance cost and meaningful value.
Retain them when their assertions protect an intentionally stable behavior and are not redundant.
Do not keep a category merely by name: inspect what its assertions actually establish.

When a group is mixed or its value is uncertain, inspect its assertions and distinct behaviors
before whole-module deletion. Retain inexpensive valuable cases and remove costly or redundant
portions; dominant scaffolding does not condemn every test in the file. Keep the review bounded,
without turning uncertainty into automatic deletion or a new framework. Use no deletion or
retention quotas.

## Remove costly machinery safely

- Delete unwanted tests directly rather than archiving, skipping, or rebuilding machinery to
  rescue them. A small correction to an otherwise valuable assertion is appropriate when it fixes
  a demonstrated false positive; do not turn pruning into speculative test expansion.
- Remove fixtures, snapshots, helpers, dev dependencies, runners, and test-only configuration
  made unused by deletion. Check remaining consumers before removing shared support.
- In files that mix production code and tests, identify the test ownership with syntax-aware
  boundaries or an equivalent language-native method. Review the resulting production diff before
  completion; never treat a large deletion as evidence that shared source survived.

## Verify and report

- Check remaining collection and run affected retained tests with the repository's tooling.
  Resolve dangling references caused by deletion. Impose no arbitrary coverage requirements or
  deletion quotas.
- Use ignored `/tests/_temp/` under the repository root for temporary checks supporting cleanup;
  remove those checks before completion. Keep genuine product defects and important coverage gaps
  separate from cleanup results rather than using them to justify speculative replacement tests.
- Report maintenance burden removed separately from raw test and line counts. Name the costly
  infrastructure eliminated, the specific protection retained and why its cost is low enough,
  known protection losses, and verification performed, including failures or checks not run.
