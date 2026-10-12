---
name: prune-tests
description: Reduce permanent test-suite maintenance burden across languages and frameworks by removing low-value tests and unnecessary support while preserving meaningful protection worth its upkeep.
---

# Prune test burden

**When in doubt, delete the test.**

Reduce permanent testing burden, not merely test count. Delete by default within scope; retain only
meaningful, stable protection that justifies its maintenance cost. Simple tests can meet that
standard; hypothetical value, low cost, and passing status alone cannot.

## Workflow

1. Establish scope from repository rules and the user's request. Default to the repository's own
   permanent suite across languages, frameworks, and test lanes, including inline tests.
   Exclude vendored tests and support from inventory, evaluation, and changes, including propagated
   hygiene checks outside vendor directories. Repository-owned tests of dependencies remain eligible.
   Read [references/execution.md](references/execution.md) for ownership and baseline inventory.
2. Evaluate modules before individual tests. Judge actual assertions and the meaningful defect they
   detect, not names or categories. Explicit repository policies are legitimate contracts even when
   checked through source inspection. Read [references/evaluation.md](references/evaluation.md)
   for retention and deletion criteria. Inspect mixed or uncertain groups briefly; remaining doubt
   favors deletion. Use no retention, deletion, or arbitrary coverage quotas.
3. Prune low-value modules, tests, and unused machinery directly. Preserve production code and
   support required by remaining consumers. Implementation proof is temporary by default; avoid
   speculative replacement tests. Follow [references/execution.md](references/execution.md)
   for cleanup mechanics.
4. Verify remaining collection and affected tests with repository tooling; resolve dangling references.
5. Report maintenance burden removed separately from counts, worthwhile protection retained,
   known protection losses, and verification results, including failures and checks not run.
