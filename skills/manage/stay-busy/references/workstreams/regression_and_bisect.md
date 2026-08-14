# Regression and bisect workstream

**Purpose:** identify the commit or change that introduced a known
regression.

## Templates

- Run `git bisect` against `<known-good ref>` and `<current ref>` using
  `<test command>` as the verdict. Record each bisect step to
  `output/bisect_<name>.log`. Stop at the first bad commit.
- Run `<test>` at HEAD and at HEAD~5, HEAD~10, HEAD~20 to coarse-bound
  the regression before bisect.

**Artifact:** bisect log path plus the identified commit SHA.

**Blocked fallback:** if bisect cannot run (build break in old
commits), record which commits failed to build and stop with
`NEEDS_CONTEXT`.
