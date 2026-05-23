# Spec conformance workstream

**Purpose:** verify implementation matches a written spec document.
Spec-driven, complementary to the audit workstream (which is rule-
driven).

## Templates

- Compare implementation in `<file>` against spec in `<spec.md>` and
  list every divergence with line numbers and severity. Output a
  Markdown table at `output/spec_conformance_<name>.md`, columns:
  spec section, implementation file:line, divergence, severity (info /
  warning / breaking).
- Walk every requirement in `<spec.md>` (each section heading or
  numbered item is a requirement) and find code that implements it.
  List orphan requirements with no implementation; list orphan code
  paths with no spec coverage.
- For specs that include example inputs/outputs, run the
  implementation against each example and report mismatches. Save the
  input/expected/actual triple per failing case.

**Artifact:** divergence report Markdown plus, when present, an
example-vs-implementation result table.

**Blocked fallback:** partial report covering only the requirements
or code paths actually checked, with the remainder listed under a
`NEEDS_CONTEXT` section naming the missing inputs (unfindable spec
section, unparseable example, ambiguous requirement).
