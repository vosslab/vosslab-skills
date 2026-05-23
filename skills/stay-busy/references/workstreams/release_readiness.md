# Release readiness workstream

**Purpose:** pre-release gate covering version sync, changelog
presence, README first-paragraph compliance, and license file.
Read-only verification that produces a pass/fail checklist.

## Templates

- Verify version sync per `docs/REPO_STYLE.md` versioning rules:
  `pyproject.toml` `[project] version`, the `VERSION` file, and any
  sibling `pyproject.toml` versions (multi-package repos) all agree.
  Report any mismatch with the conflicting values.
- Verify `docs/CHANGELOG.md` has an entry for the planned release date
  and that it lists categorized bullets (Additions / Behavior changes
  / Fixes / Removals).
- Verify `README.md` first paragraph is pure prose, under 250
  characters, no badges, no Markdown links, no code spans, no raw
  URLs (per `docs/REPO_STYLE.md` GitHub About description rules).
- Verify `LICENSE` file is present and the license text matches the
  declared license per `docs/REPO_STYLE.md` licensing policy (GPLv3,
  LGPLv3, or CC BY-SA 4.0 depending on content type).
- Output a Markdown checklist at
  `output/release_readiness_<version>.md` with one row per check,
  status (PASS / FAIL), and the offending detail when FAIL.

**Artifact:** checklist Markdown plus the source values consulted
(version strings extracted, first-paragraph text, license header).

**Blocked fallback:** produce the checklist showing which items
passed and which were unverifiable (missing file, malformed format,
ambiguous policy). The user can act on the partial result; missing
items become an action list for a follow-up workstream.
