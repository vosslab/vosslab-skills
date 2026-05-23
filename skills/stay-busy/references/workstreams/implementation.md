# Implementation workstream

**Purpose:** bounded code change with explicit acceptance criteria.

## Templates

- Apply `<change>` to `<file>`. Acceptance: `<test command>` passes; no
  other behavior changes; diff under `<N>` lines.
- Add `<feature>` behind `<flag>`. Default off. Acceptance: new tests
  pass, existing tests pass, flag-off behavior unchanged.
- Refactor `<function>` to `<shape>` while preserving public signature.
  Acceptance: call-site grep returns identical hit count.

**Artifact:** diff path (use `git diff > output/<name>.diff`) plus the
verification command output.

**Blocked fallback:** stop on first failed acceptance check, write a
`NEEDS_CONTEXT` report at `output/blocked_<name>.md` with the failing
command output and revert criteria.
