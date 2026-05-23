# Release notes summary workstream

**Purpose:** parse `docs/CHANGELOG.md` and synthesize a user-facing
release notes summary highlighting new features. Distinct from the
report workstream (which synthesizes a single run) -- this one
synthesizes a release window.

## Templates

- Read `docs/CHANGELOG.md` between `<from-date>` and `<to-date>` (or
  between `<from-tag>` and `<to-tag>` if release tags exist). Group
  entries by their category subsection (Additions and New Features /
  Behavior or Interface Changes / Fixes and Maintenance / Removals
  and Deprecations / Decisions and Failures / Developer Tests and
  Notes). Output a Markdown summary at
  `output/release_notes_<version>.md` that leads with Additions and
  Behavior changes as headline material and demotes Fixes to a short
  bulleted list.
- Identify breaking changes by scanning Behavior or Interface Changes
  and Removals for phrases like "Removed", "Renamed", "Replaced",
  "Dropped support", "no longer". Surface them in a separate
  `## Breaking changes` section at the top of the summary so upgraders
  see them first.
- For each summary entry, link back to the corresponding day-heading
  in `docs/CHANGELOG.md` so a reader can drill into the full bullet.
  Use a relative `[YYYY-MM-DD](../docs/CHANGELOG.md#yyyy-mm-dd)`
  anchor.

**Artifact:** release notes Markdown at
`output/release_notes_<version>.md` plus the date range or tag range
consulted, so the synthesis is reproducible.

**Blocked fallback:** if changelog parsing fails on a malformed day
block (missing subsection heading, ambiguous date), emit a partial
summary covering the well-formed blocks and list the unparseable
headings under a `## Skipped entries` section. Mark
`DONE_WITH_CONCERNS`; the malformed blocks become a cleanup-workstream
candidate.
