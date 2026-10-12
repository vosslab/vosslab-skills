# Execute test pruning

## Establish ownership and baseline

Identify vendored tests by upstream ownership, vendor markers, or repository documentation, even
outside vendor directories. Apply exclusions before judging value. Test ownership is separate from
implementation ownership: a repository-owned test of a vendored helper may protect local integration
behavior and receives ordinary evaluation.

Identify suite entrypoints, collection and execution commands, and supporting infrastructure.
Record a comparable starting inventory of eligible tests, support files, dependencies, runtime,
and known flaky or environment-sensitive lanes.

## Remove tests and machinery

- Delete unwanted tests directly rather than archiving, skipping, or rebuilding machinery to rescue
  them. A small assertion correction is appropriate for a demonstrated false positive in an otherwise
  valuable test; avoid speculative test expansion.
- Remove fixtures, snapshots, helpers, development dependencies, runners, and test-only configuration
  made unused by deletion. Check all remaining consumers, including vendored tests, before removing
  shared support; preserve anything they still require.
- In mixed production/test files, identify test boundaries with syntax-aware or equivalent
  language-native methods. Review the production diff before completion; deletion size does not
  establish that shared source survived.
- Use the repository's ignored `tests/_temp/` directory for temporary cleanup checks and remove them
  before completion. Report genuine product defects and important coverage gaps separately from
  cleanup results; they do not justify speculative replacement tests.

## Verify and report

Check remaining collection and run affected retained tests with repository tooling. Resolve dangling
references caused by deletion.

Report maintenance burden removed separately from test and line counts. Name costly infrastructure
eliminated, specific protection retained and why its cost is justified, known protection losses,
and verification performed, including failures or checks not run.
