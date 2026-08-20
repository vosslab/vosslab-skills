# Failure investigation workstream

**Purpose:** pin a known failure to a single change, function, or
input.

## Templates

- Reproduce `<failure>` with `<minimal command>`. Capture the exact
  error text and stack trace. Save to `output/repro_<name>.log`.
- Cluster recent `<failure pattern>` occurrences across logs in
  `<path>`. Output a Markdown table grouped by error signature.
- Hypothesis-list for `<failure>`: enumerate 3-5 plausible causes,
  each with a one-command falsification test.

**Artifact:** reproduction log path plus the hypothesis list path.

**Blocked fallback:** file a `NEEDS_CONTEXT` note with the failing
input, exact error, and the smallest unexplored hypothesis.
