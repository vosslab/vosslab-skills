# Release history template

This is a writing shape for `docs/RELEASE_HISTORY.md`, not a file to copy
verbatim. `RELEASE_HISTORY.md` is the full, organized version log: it carries
more detail than `docs/NEWS.md` and aims to be the durable, portable record of
every release. Write substantive content for each subsection or omit that
subsection; never emit an empty heading.

## Shape

```
# Release history

## vYY.MM.PATCH - YYYY-MM-DD
### Highlights
### Notable fixes
### Compatibility notes
### Validation
```

## Section guidance

- `# Release history`: one `#` title, sentence case, appears once at the top.
- `## vYY.MM.PATCH - YYYY-MM-DD`: one block per release, reverse-chronological
  (newest first). The heading shape must be exactly `## v<version> - YYYY-MM-DD`
  so it stays compatible with `devel/make_release.py`. Use the repo CalVer
  shape (`0Y.0M.PATCH`, for example `26.06.1`); see the versioning rules in
  `docs/REPO_STYLE.md`.
- `### Highlights`: the shipped features and meaningful behavior changes for
  this version, summarized from the changelog `### Additions and New Features`
  and `### Behavior or Interface Changes` subsections. Fuller than the NEWS
  highlights: include the secondary items NEWS leaves out.
- `### Notable fixes`: significant bug fixes and maintenance work, summarized
  from the changelog `### Fixes and Maintenance` subsection. Keep to fixes a
  reader would care about across releases.
- `### Compatibility notes`: breaking changes, removals, deprecations, and
  migration impact, summarized from the changelog `### Removals and
  Deprecations` and any interface-breaking `### Behavior or Interface Changes`
  entries. Omit the subsection when nothing changed compatibility.
- `### Validation`: how the release was checked (test suites run, smoke checks,
  release-tool steps). Omit when there is no verifiable validation evidence.

## Rules

- ASCII only; escape any UTF-8 symbols (for example `&alpha;`).
- Sentence-case headings; ATX style with a space after the hashes.
- Omit any subsection that has no real content. Do not write a hollow doc.
- Use relative links for repo-local files; keep link text equal to the path.
- This file is fuller than `news_template.md`. Keep the two outputs distinct so
  `RELEASE_HISTORY.md` and `NEWS.md` never read identically.
