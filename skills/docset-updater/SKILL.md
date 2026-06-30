---
name: docset-updater
description: "Refresh the whole repo doc set in one pass by invoking the per-doc skills in dependency order (`arch-docs`, `setup-install-usage-docs`, `readme-docs`, `screenshot-docs`, `agents-md-fixer`), then audit any remaining `docs/` files those skills do not own. Use when the user wants all docs brought current at once, or the doc set as a whole is missing, drifted, or unaudited."
---

# Docset refresh

## Overview

Bring the full documentation set current in one pass. This skill is an
orchestrator: it does not write architecture, install, usage, `README.md`, or
`AGENTS.md` content directly. It invokes the skill that owns each of those, in an
order where later skills can link into what earlier skills produced, then audits
the remaining `docs/` files no per-doc skill owns.

## Owned-doc routing

Each of these docs has a dedicated skill. Each skill writes its own files:

- `arch-docs` -> `docs/CODE_ARCHITECTURE.md`, `docs/FILE_STRUCTURE.md` (and adds the
  links to `README.md`)
- `setup-install-usage-docs` -> `docs/USAGE.md`, `docs/INSTALL.md`
- `readme-docs` -> `README.md` (links into the `docs/` set above, reserves the
  screenshot block)
- `screenshot-docs` -> `docs/screenshots/` PNGs and the managed screenshot block
  inside `README.md` and `docs/`
- `agents-md-fixer` -> `AGENTS.md` (trims to pointers into `docs/*.md`)

Ship these as three dependency-aware waves so independent skills run together and
each wave starts from a ready precondition:

- Wave 1 (parallel): `arch-docs`, `setup-install-usage-docs`, and the remaining-docs
  audit (step 3). These write separate `docs/` files; `arch-docs` is the lone
  `README.md` writer in this wave.
- Wave 2: `readme-docs`. Starts once Wave 1 reports, so `arch-docs` has finished its
  `README.md` touch and the `docs/` link targets exist.
- Wave 3 (parallel): `screenshot-docs` and `agents-md-fixer`. `screenshot-docs` fills
  the screenshot block that `readme-docs` reserved; `agents-md-fixer` points
  `AGENTS.md` into the finished `docs/*.md` set. They write separate targets, so they
  run together.

Three preconditions set the wave order: `readme-docs` follows `arch-docs` (both write
`README.md`); `screenshot-docs` follows `readme-docs` (it fills the reserved block);
`agents-md-fixer` follows the completed `docs/*.md` set.

## Workflow

1. Read the rules and inventory
   - Read `AGENTS.md`, `docs/REPO_STYLE.md`, and `docs/MARKDOWN_STYLE.md`.
   - List `docs/` contents and root docs (`AGENTS.md`, `README.md`, `LICENSE`).
2. Dispatch the per-doc skills in three waves
   - Wave 1 (parallel): dispatch `arch-docs`, `setup-install-usage-docs`, and the
     remaining-docs audit (step 3) together in one batch.
   - Wave 2: dispatch `readme-docs` once Wave 1 reports.
   - Wave 3 (parallel): dispatch `screenshot-docs` and `agents-md-fixer` together once
     Wave 2 reports.
   - `screenshot-docs` runs as a second pass after README prose exists. When no app
     window or display is available, it adds a Known-gaps line to the report, leaves
     existing screenshots and the managed block in place, leaves both block sentinels
     for the next run, and the chain continues to `agents-md-fixer`.
   - Let each skill decide whether its docs need creation or refresh; each skill owns
     its own content.
   - Under `delegate-manager-to-subagents`, dispatch a fresh subagent per skill and
     send each wave's subagents in a single batch so they run concurrently.
3. Audit the remaining docs (this skill's direct responsibility)
   - Each file below is an independent atomic task that joins Wave 1's parallel batch.
     Under `delegate-manager-to-subagents`, give each file its own subagent with one
     owner, one target file, and one verification result. This list is the source of
     truth for which files the audit covers.
   - For each below, create or update only when repo evidence supports truthful
     content. If evidence is missing, add a short stub with a "Known gaps" task
     list instead of guessing.
     - `docs/CHANGELOG.md`
     - `docs/NEWS.md`
     - `docs/RELATED_PROJECTS.md`
     - `docs/RELEASE_HISTORY.md`
     - `docs/ROADMAP.md`
     - `docs/TODO.md`
     - `docs/TROUBLESHOOTING.md`
     - `docs/COOKBOOK.md`, `docs/DEVELOPMENT.md`, `docs/FAQ.md` (only when evidence exists)
   - Choose one file I/O doc unless more are clearly needed:
     `docs/INPUT_FORMATS.md`, `docs/OUTPUT_FORMATS.md`, or `docs/FILE_FORMATS.md`.
     Add `docs/YAML_FILE_FORMAT.md` only when YAML is a real interface surface.
4. Check centrally maintained docs
   - Verify presence and exactness only. Do not edit content.
     - `docs/AUTHORS.md`
     - `docs/MARKDOWN_STYLE.md`
     - `docs/PYTHON_STYLE.md`
     - `docs/REPO_STYLE.md`
5. Flag docs that should not exist
   - If present, recommend relocation or deletion:
     - `CONTRIBUTING.md` (prefer `docs/DEVELOPMENT.md`)
     - `CODE_OF_CONDUCT.md`
     - `COMMUNITY.md`
     - Issue/PR templates
     - `SECURITY.md`
6. Apply naming and style rules to anything this skill writes directly
   - Use ALL CAPS with underscores under `docs/`.
   - Keep links relative and descriptive.
   - Use present tense, short bullets, and avoid speculation.
7. Update changelog
   - Update `docs/CHANGELOG.md` directly when this skill runs as a standalone
     task; under `delegate-manager-to-subagents`, dispatch a docs subagent to add
     the entry.
8. Provide a short report
   - Per-doc skills run: which of the five ran and what each reported.
   - Created: list new docs.
   - Updated: list updated docs.
   - Flagged: list docs to relocate or delete.
   - Known gaps: list verification tasks only.

## Minimal stub template

For docs this skill writes directly (step 3):

- Title in sentence case.
- One paragraph describing scope and audience.
- Sections with 2 to 6 bullets each, one idea per bullet.
- "Known gaps" section when evidence is missing, with tasks only.

## Delegated execution

Under `delegate-manager-to-subagents`, dispatch a fresh subagent for each per-doc
skill and for each remaining-docs audit file, each with one bounded task, the
relevant repo rules, and one verification step. Give each subagent a single atomic
task.

Be efficient with time: subagents and tokens are cheap, wall time is scarce.
Dispatch the independent tasks in each wave as one parallel batch. Give each task one
owner, one clear outcome, and one verification step. Order the work by the three
preconditions in "Owned-doc routing" and ship everything else together. See
`docs/REPO_STYLE.md#core-philosophies` ("Be efficient with time", "Atomic task
decomposition", "Prompt positively") and the `parallel-plan` skill.
