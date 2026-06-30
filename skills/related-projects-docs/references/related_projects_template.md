# Related projects writing-shape template

This is a writing-shape reference for `docs/RELATED_PROJECTS.md`, not a file to copy
verbatim. Fill each section only with projects that have a real link and a short
evidence line. Omit a tier section when it has no entries. Never write a hollow file
to satisfy the shape; if no entry clears the evidence bar, write no file and report the
gap (see the content-or-no-file threshold in the parent SKILL.md).

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
- Evidence: <one line; what makes this a strong-evidence match>
- Notes: <optional one line of context>

## Possible related projects

### project-name
- Relationship: <one taxonomy label>
- Link: https://example.com/other
- Evidence: <one line; weaker basis, no direct repo link>
- Confidence: low

## Evidence notes

Short prose summary of the source basis behind the entries above (manifests,
reciprocal links, package metadata, GitHub topics). This is a summary, not a raw
search log.
```

## Section meanings

- Confirmed related projects: strong-evidence sources only (explicit link or reciprocal
  link, dependency, package metadata, import, citation, fork/upstream statement).
- Possible related projects: weaker matches (same domain, shared topics, overlapping
  name) that still carry a real link and an evidence line.
- Evidence notes: a short summary of where the evidence came from, so a later reader can
  judge the basis without re-running every search.

Known gaps and untraced leads go to the run report, never into the doc as a section
that would license a near-empty file.
