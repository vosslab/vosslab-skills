---
name: news-release-docs
description: "Create or refresh `docs/RELEASE_HISTORY.md` and `docs/NEWS.md` from `docs/CHANGELOG.md`, authoring two differentiated docs (full versioned dated log vs short curated highlights) and emitting a `/tmp` notes-file body for `devel/make_release.py --notes-file`. Use when preparing a release or when the release docs are drifted, empty, or out of sync with the changelog. Does NOT touch `docs/CHANGELOG.md`, `README.md`, or the broader doc set (use `docset-updater` for the rest)."
---

# News and release docs

## Overview

Read the verbose `docs/CHANGELOG.md` (and rotated archives) and author two
differentiated release docs from it:

- `docs/RELEASE_HISTORY.md`: the full, organized, reverse-chronological version
  log with notable fixes and compatibility detail.
- `docs/NEWS.md`: short curated highlights and announcements, not a full
  changelog.

Both are written in place. The skill also emits a notes-file body to a scratch
path under `/tmp` for use with `devel/make_release.py --notes-file`, and reports
that path. The two docs must stay distinct (full log vs curated highlights);
never produce identical content. Base every entry on changelog evidence and
never invent shipped work.

## Version source

Determine the target version deterministically:

1. If `docs/CHANGELOG.md` carries explicit version headings, derive the version
   from the changelog.
2. When the changelog carries only date blocks (the repo's day-block format),
   read the repo-root `VERSION` file as the version source.
3. Cross-check `VERSION` against `pyproject.toml` `[project] version`. If they
   disagree, report the mismatch and stop; do not guess. See the versioning
   rules in `docs/REPO_STYLE.md` (CalVer `0Y.0M.PATCH`, `VERSION` plus
   `pyproject.toml` as the version source).

Use the heading shape `## v<version> - YYYY-MM-DD` for every release block. This
matches `devel/make_release.py` `_prepend_release_doc`, which inserts a block of
exactly that shape above the first existing `##` heading, so the skill output
and the release tool stay compatible.

## Workflow

1. Gather changelog evidence
   - Read the active `docs/CHANGELOG.md`.
   - Read rotated archives `docs/CHANGELOG-YYYY-MM*.md` as needed to cover the
     release range. See the changelog-rotation rules in `docs/REPO_STYLE.md`
     (two newest day blocks stay active; older blocks live in archives).
   - Collect the day-block subsections (Additions and New Features, Behavior or
     Interface Changes, Fixes and Maintenance, Removals and Deprecations,
     Decisions and Failures, Developer Tests and Notes) for the target version.
2. Resolve the target version
   - Follow the "Version source" steps above.
3. Author two differentiated bodies
   - Write the `docs/RELEASE_HISTORY.md` block from
     [references/release_history_template.md](references/release_history_template.md):
     Highlights, Notable fixes, Compatibility notes, Validation. Fuller detail,
     including secondary items.
   - Write the `docs/NEWS.md` block from
     [references/news_template.md](references/news_template.md): curated
     Highlights and, only when a real upgrade step exists, Upgrade notes. Terse,
     headline items only.
   - Omit any subsection that has no real content. Keep the two bodies clearly
     different in scope and length.
4. Prepend in place
   - Prepend the `## v<version> - YYYY-MM-DD` block immediately above the first
     existing `##` heading in each doc, preserving all older content
     byte-for-byte. If a `## v<version>` heading already exists in a doc, report
     it and stop rather than duplicating.
5. Emit the notes-file body
   - Write a notes-file body to a scratch path under `/tmp` (for example
     `/tmp/news_release_notes.md`) for use as
     `devel/make_release.py --notes-file`, and report that path. The notes-file
     stays out of the repo; never write a repo-tracked scratch file.
6. Apply style
   - Follow `docs/MARKDOWN_STYLE.md`: ASCII only (escape UTF-8 symbols),
     sentence-case ATX headings, `-` bullets, relative links with path link
     text.

## Content or no file

Write a release doc only when the changelog has release-worthy content for the
target version that fills at least one substantive subsection beyond the title
and version heading. When the changelog has no release-worthy content for the
target version, report the gap in the run report and write no file. Never write
a hollow or stub doc.

## Output

- Updated `docs/RELEASE_HISTORY.md` and `docs/NEWS.md` (each gaining one
  `## v<version> - YYYY-MM-DD` block), when evidence supports them.
- A `/tmp` notes-file body path for `devel/make_release.py --notes-file`.
- A short report: version resolved and its source, docs written or skipped, and
  any gaps (missing changelog content, version mismatch).

## Delegated execution

Under `delegate-manager-to-subagents`, this skill is assigned to a fresh subagent
with one bounded task, the relevant repo rules, and one verification step.
Do not continue the same subagent across unrelated follow-up work; dispatch a
new subagent for each atomic task. See
`docs/REPO_STYLE.md`.
