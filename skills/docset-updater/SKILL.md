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

Each of these docs has a dedicated skill. Invoke them in this order so
downstream skills see current content to point at:

1. `arch-docs` -> `docs/CODE_ARCHITECTURE.md`, `docs/FILE_STRUCTURE.md`
2. `setup-install-usage-docs` -> `docs/USAGE.md`, `docs/INSTALL.md`
3. `readme-docs` -> `README.md` (links into the `docs/` set above)
4. `screenshot-docs` -> `docs/screenshots/` (captures app screenshots, writes them to
   `docs/screenshots/`, and rewrites the readme-docs managed screenshot block with real
   embeds; runs as a second pass after README prose exists)
5. `agents-md-fixer` -> `AGENTS.md` (trims to pointers into `docs/*.md`)

## Workflow

1. Read the rules and inventory
   - Read `AGENTS.md`, `docs/REPO_STYLE.md`, and `docs/MARKDOWN_STYLE.md`.
   - List `docs/` contents and root docs (`AGENTS.md`, `README.md`, `LICENSE`).
2. Run the per-doc skills in order
   - Invoke `arch-docs`, then `setup-install-usage-docs`, then `readme-docs`, then
     `screenshot-docs`, then `agents-md-fixer`, each via the Skill tool.
   - `screenshot-docs` runs as a second pass after README prose exists. When no app
     window or display is available, it adds a Known-gaps line to the report, leaves
     existing screenshots and the managed block in place, leaves both block sentinels
     for the next run, and the chain continues to `agents-md-fixer`.
   - Let each skill decide whether its docs need creation or refresh; do not
     duplicate their work here.
   - Under `delegate-manager-to-subagents`, dispatch a fresh subagent per skill
     instead of invoking inline (one atomic task per subagent).
3. Audit the remaining docs (this skill's direct responsibility)
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
skill and for the remaining-docs audit, each with one bounded task, the relevant
repo rules, and one verification step. Do not continue the same subagent across
unrelated follow-up work. See `docs/REPO_STYLE.md`.
