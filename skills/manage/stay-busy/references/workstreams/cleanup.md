# Cleanup workstream

**Purpose:** lint, ASCII, markdown-link, and changelog grooming scoped
to files touched by the current milestone. Anti-clutter, not
housekeeping-for-its-own-sake.

## Templates

- Run `pytest tests/test_pyflakes_code_lint.py -k <file>` and fix every
  reported issue. Acceptance: clean rerun.
- Run `pytest tests/test_ascii_compliance.py -k <file>` and fix every
  non-ASCII character per `docs/MARKDOWN_STYLE.md` escape rules.
- Verify every Markdown link in `<doc>` resolves via
  `pytest tests/test_markdown_links.py -k <doc>`. Fix dead links by
  pointing to the moved target.

**Artifact:** command output log plus the diff applied.

**Blocked fallback:** file a `NEEDS_CONTEXT` note listing each
unfixable issue and its required decision.
