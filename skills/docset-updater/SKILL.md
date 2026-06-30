---
name: docset-updater
description: "Refresh the whole repo doc set in one pass by invoking the per-doc skills in dependency order (`arch-docs`, `setup-install-usage-docs`, `readme-docs`, `related-projects-docs`, `news-release-docs`, `screenshot-docs`, `agents-md-fixer`), then audit any remaining `docs/` files those skills do not own. Use when the user wants all docs brought current at once, or the doc set as a whole is missing, drifted, or unaudited."
---

# Docset refresh

## Overview

Bring the full documentation set current in one pass. This skill is an
orchestrator: it does not write architecture, install, usage, `README.md`, or
`AGENTS.md` content directly. It invokes the skill that owns each of those, in an
order where later skills can link into what earlier skills produced, then audits
the remaining `docs/` files no per-doc skill owns.

## Owned-doc routing

Each artifact has one owning skill. Dependencies follow ownership, so independent
owners run together:

- `arch-docs` -> `docs/CODE_ARCHITECTURE.md`, `docs/FILE_STRUCTURE.md`
- `setup-install-usage-docs` -> `docs/USAGE.md`, `docs/INSTALL.md`
- `related-projects-docs` -> `docs/RELATED_PROJECTS.md`
- `news-release-docs` -> `docs/RELEASE_HISTORY.md`, `docs/NEWS.md`
- `readme-docs` -> `README.md` (sole owner; links the core docs by convention,
  reserves the screenshot block)
- `screenshot-docs` -> `docs/screenshots/` PNGs and the managed screenshot block
  inside `README.md` and `docs/`
- `agents-md-fixer` -> `AGENTS.md` (bare-path pointers into `docs/*.md`)

`readme-docs` owns all of `README.md`, so the doc producers create only their own
`docs/` files and `readme-docs` writes every README link. With one owner per artifact,
the producers carry no write conflict and run together.

Dispatch by dependency edges, not a fixed barrier, so each owner starts as early as
its inputs allow:

- Start immediately, no dependencies (one concurrent batch): `arch-docs`,
  `setup-install-usage-docs`, `related-projects-docs`, `news-release-docs`,
  `readme-docs`, and the remaining-docs audit (step 3). Each owns separate files, so
  they carry no write conflict. `readme-docs` links the core docs
  (`CODE_ARCHITECTURE`, `FILE_STRUCTURE`, `INSTALL`, `USAGE`) by convention, so it runs
  alongside their producers; the final Markdown link check confirms the files exist.
- `screenshot-docs` <- `readme-docs`: start as soon as `readme-docs` has reserved the
  screenshot block. It does not depend on the other producers, so it runs concurrently
  with the still-running batch (including the slow `related-projects-docs`) instead of
  waiting behind it.
- `agents-md-fixer` <- the doc producers and audit outputs: start once the `docs/*.md`
  files it links exist. It points `AGENTS.md` at created paths, not prose, so it waits
  for file existence only, not content quality.

`related-projects-docs` is the likely long pole: its bounded web discovery (search,
fetch, and package/repo metadata with rate-limit sleeps) is network-bound and may
dominate wall time. The dependency-edge model matters because it lets the
`readme-docs` -> `screenshot-docs` path finish in parallel rather than stall behind
that network-bound producer. Keep discovery bounded; do not gate the rest of the
refresh on it.

### README links for conditional docs

`readme-docs` links the core docs above by convention. Conditional docs (for example
`docs/TROUBLESHOOTING.md`, created only when evidence supports them) stay discoverable
through `docs/` and `AGENTS.md`. A conditional doc created in this same run is not
guaranteed a README link in the same run; link it on a later pass when it is present.

## Workflow

1. Read the rules and inventory
   - Read `AGENTS.md`, `docs/REPO_STYLE.md`, and `docs/MARKDOWN_STYLE.md`.
   - List `docs/` contents and root docs (`AGENTS.md`, `README.md`, `LICENSE`).
2. Dispatch the per-doc skills by dependency edges
   - Start immediately in one concurrent batch (no dependencies): `arch-docs`,
     `setup-install-usage-docs`, `related-projects-docs`, `news-release-docs`,
     `readme-docs`, and the remaining-docs audit (step 3).
   - `screenshot-docs` <- `readme-docs`: dispatch as soon as `readme-docs` has reserved
     the screenshot block, concurrently with the still-running producers (do not wait
     for the slow `related-projects-docs`).
   - `agents-md-fixer` <- doc producers and audit outputs: dispatch once the `docs/*.md`
     files it links exist.
   - `screenshot-docs` runs after README prose exists. When no app window or display is
     available, it adds a Known-gaps line to the report, leaves existing screenshots and
     the managed block in place, leaves both block sentinels for the next run, and
     `agents-md-fixer` still proceeds.
   - Let each skill decide whether its docs need creation or refresh; each skill owns
     its own content.
   - Under `delegate-manager-to-subagents`, dispatch a fresh subagent per skill. Send
     every dependency-free task as one parallel batch, then dispatch `screenshot-docs`
     and `agents-md-fixer` the moment their edges resolve rather than waiting on the
     whole batch.
3. Audit the remaining docs (this skill's direct responsibility)
   - Each file below is an independent atomic task that joins the dependency-free batch.
     Under `delegate-manager-to-subagents`, give each file its own subagent with one
     owner, one target file, and one verification result. This list is the source of
     truth for which files the audit covers.
   - For each below, create or update a doc only when repo evidence supports at
     least one useful section beyond its title, intro, and any known gaps. When
     evidence is thin, record the doc under Known gaps in the step-8 report and
     write no file.
     - `docs/CHANGELOG.md`
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
   - Per-doc skills run: which of the per-doc owners ran and what each reported.
   - Created: list new docs.
   - Updated: list updated docs.
   - Flagged: list docs to relocate or delete.
   - Known gaps: list verification tasks only.

## Content shape for audited docs

When evidence supports a doc this skill writes directly (step 3), follow this shape:

- Title in sentence case.
- One paragraph describing scope and audience.
- At least one substantive section grounded in repo evidence, with 2 to 6 bullets each,
  one idea per bullet.

When not to create a file: when the only content would be a title, an intro, and a
known-gaps list, write no file. Record the doc under Known gaps in the step-8 report so
the gap stays visible and the owning skill can create the doc once evidence supports it.

## Delegated execution

Under `delegate-manager-to-subagents`, dispatch a fresh subagent for each per-doc
skill and for each remaining-docs audit file, each with one bounded task, the
relevant repo rules, and one verification step. Give each subagent a single atomic
task.

Be efficient with time: subagents and tokens are cheap, wall time is scarce.
Dispatch every dependency-free task as one parallel batch, then release
`screenshot-docs` and `agents-md-fixer` the moment their edges in "Owned-doc routing"
resolve rather than waiting on the whole batch (this keeps the fast
`readme-docs` -> `screenshot-docs` path off the critical path of the network-bound
`related-projects-docs`). Give each task one owner, one clear outcome, and one
verification step. See `docs/REPO_STYLE.md#core-philosophies` ("Be efficient with
time", "Atomic task decomposition", "Prompt positively") and the `parallel-plan` skill.
