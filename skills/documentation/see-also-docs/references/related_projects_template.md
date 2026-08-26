# Related projects writing-shape template

Use this writing shape to create `docs/RELATED_PROJECTS.md`. Fill each section with
projects or resources that pass the visitor relevance gate in the parent skill. Each
entry gives a real link, a visitor-value line, and a short evidence line. Include each
tier section that has entries. For a search with zero passing entries, preserve the
documentation tree and report the gap.

Conventions:

- GitHub Flavored Markdown, ATX headings (`#`, `##`, `###`).
- One `#` title only; sentence-case headings; ASCII only.
- Each project is an `###` heading with bullet fields below it.
- Relative Markdown links for in-repo paths; full URLs for external projects.

## Skeleton

```
# Related projects

## Confirmed related projects

### project-name
- Relationship: <one taxonomy label>
- Link: https://example.com/project
- Why visitors may care: <shared or adjacent goal for the same audience>
- Evidence: <one line; what makes this a strong-evidence match>
- Notes: <optional one line of context>

## Possible related projects

### project-name
- Relationship: <one taxonomy label>
- Link: https://example.com/other
- Why visitors may care: <specific adjacent value for an interested visitor>
- Evidence: <one line; authoritative but weaker relationship evidence>
- Confidence: low

## Evidence notes

Short prose summary of the source basis behind the entries above (project documentation,
explicit comparisons, lineage statements, official descriptions, or reciprocal links).
```

## Section meanings

- Confirmed related projects: strong relationship evidence such as an explicit comparison,
  reader-facing link, reciprocal link, citation, or fork/upstream statement.
- Possible related projects: authoritative descriptions establish a shared or adjacent
  visitor workflow, with a real link and a specific reason visitors may care.
- Evidence notes: a short summary of where the evidence came from, so a later reader can
  judge the basis without re-running every search.

Keep known gaps and untraced leads in the run report. The published file contains useful,
evidenced destinations for visitors.
