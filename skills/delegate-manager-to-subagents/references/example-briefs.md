# Example subagent briefs

Use these examples when writing subagent dispatches. Keep the same
seven-part shape: plan reference, context bootstrap, background, scope,
boundaries, verification, and handoff.

## Example 1: Implementer brief

### Plan reference
`~/.claude/plans/example.md#WP-A`

### Context bootstrap
Invoke `repo-rules-reader` before editing files.

### Background
This task implements the isolated loader change needed before the CLI
wiring task can run.

### Scope
1. Add `load_sheet_registry()` in `sheet_registry.py`.
2. Preserve existing caller behavior.
3. Add focused tests for missing required keys.

### Boundaries
- CLI wiring belongs to WP-B.
- Changelog belongs to the docs subagent.
- Keep public names from the approved plan unchanged.

### Verification
Run:
`source source_me.sh && pytest tests/test_sheet_registry.py -k load_sheet_registry`

Expected success line:
`3 passed in 0.12s`

### Handoff
Report files changed, exact command output, requirement coverage,
concerns, and residual risks.

## Example 2: Spec reviewer brief

### Plan reference
`~/.claude/plans/example.md#WP-A`

### Context bootstrap
Invoke `repo-rules-reader` before reviewing the diff.

### Background
The implementer completed WP-A. This review checks whether the diff
matches the approved task text.

### Scope
1. Confirm `load_sheet_registry()` exists.
2. Confirm caller behavior is preserved.
3. Confirm tests cover missing required keys.

### Boundaries
- Review spec compliance only.
- Quality and style review is a separate pass.

### Verification
Use the supplied diff and task text. Cite file lines for each finding.

### Handoff
Return `SPEC_COMPLIANT` or `SPEC_GAPS`, with each finding grounded in
the diff.

## Example 3: Quality reviewer brief

### Plan reference
`~/.claude/plans/example.md#WP-A`

### Context bootstrap
Invoke `repo-rules-reader` before reviewing the diff.

### Background
Spec review passed. This review checks repo-style and maintainability
issues.

### Scope
1. Check Python style.
2. Check pytest style.
3. Check repo rules relevant to the changed files.

### Boundaries
- Spec compliance is the prior reviewer's pass; surface a style issue
  here only when it affects correctness.
- Read-only review; file edits stay with the implementer.

### Verification
Use the supplied diff, command output, and repo rules from
`repo-rules-reader`.

### Handoff
Return `QUALITY_APPROVED` or `QUALITY_ISSUES`, with each item grounded
in a diff line or exact command output.
