# Next-iteration push workstream

**Purpose:** open the next version axis (the user's "NEW3" pattern:
when shipping version N, scope work for version N+1 in parallel so the
next release does not start from scratch). Name the next version and
propose its scope without committing production code.

## Templates

- Draft `docs/<NEXT_VERSION>_PROPOSAL.md` with: motivating problem,
  proposed feature set, acceptance criteria, dependency graph, rollout
  shape. No production code changes.
- Identify which current workstreams close out the current version
  versus set up the next version; list them in two columns.
- Propose 3 candidate names for the next version and a one-sentence
  rationale each.

**Artifact:** proposal Markdown path plus a column-split workstream
list.

**Blocked fallback:** emit a `NEEDS_CONTEXT` note with the questions
that must be answered before next-version scope can be drafted.
