# Audit workstream

**Purpose:** read-only correctness, style, or contract sweep over a
bounded file set.

## Templates

- Audit all files in `<path>` for `<rule>` violations. Output a Markdown
  table of `path:line` rows with the violation excerpt. No file edits.
- Compare implementation in `<file>` against spec in `<doc>` and list
  every divergence with line numbers and severity.
- Inventory all `<symbol pattern>` occurrences across the repo via
  `git ls-files | grep`. Output the candidate list before any change.

**Artifact:** Markdown table file at `output/audit_<name>.md` plus the
`git ls-files` command log used.

**Blocked fallback:** produce a partial table over the files already
audited, mark remaining files `NEEDS_CONTEXT`, and return.
