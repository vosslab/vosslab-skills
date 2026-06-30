---
name: setup-install-usage-docs
description: "Create or refresh `docs/INSTALL.md` and `docs/USAGE.md` from repo evidence, writing real content when install or usage evidence supports it and reporting gaps when it does not. Use when these two docs are missing, too thin, or stale. Does NOT touch `README.md`, `docs/CODE_ARCHITECTURE.md`, `docs/FILE_STRUCTURE.md`, or the broader doc set (use `readme-docs`, `arch-docs`, or `docset-updater` for those)."
---

# Setup, install, and usage docs

## Goal

Write content-supported docs for:
- `docs/INSTALL.md`: setup steps, dependencies, environment requirements.
- `docs/USAGE.md`: how to run the tool, CLI flags, practical examples.

Write a doc when repo evidence supports a real Requirements/Install section (INSTALL)
or a real Quick-start/CLI section (USAGE). Treat a basic runnable command, an entry
point, or a dependency manifest (`pip_requirements.txt`, `pyproject.toml`, `Brewfile`)
as install or usage evidence and write the doc from it; INSTALL and USAGE are
near-universal, so do not skip them when this evidence exists. Report the gap instead
of writing a file only when no such evidence exists, so the only content would be a
title plus "Known gaps".

## Inputs to request

- Primary run mode: CLI, library, or both, and which one is the main entry point.
- Supported platforms, if known, including any OS or shell constraints already stated.
- One or two common real workflows users should be able to do, described as concrete tasks.

## Workflow

1. Inspect evidence
   - Read `README.md` and `AGENTS.md` when present
     to learn purpose, constraints, and any required environment notes.
   - Look for entry points and run commands (scripts, `pyproject.toml`,
     `setup.cfg`, `Makefile`, `tools/`, `bin/`) and note what a user actually runs.
   - Identify dependencies and install method (pip editable, requirements file, system deps),
     and only record what is confirmed by repo files.
2. Write or update docs
   - Write a file when evidence supports a real Requirements/Install or
     Quick-start/CLI section; trim and correct stale files.
   - Report the gap and write no file only when no real install or usage
     evidence exists.
   - Keep doc naming under `docs/` consistent with repo conventions.
3. Keep docs minimal
   - Prefer 2 to 6 bullets per section.
   - Prefer one primary path and keep alternates out unless the repo makes them explicit.
   - Include exact commands only when verifiable from repo evidence, not inferred.
   - Target 40 to 120 lines per doc, and prefer linking to deeper docs when needed.
4. Record uncertainty explicitly
   - Add a "Known gaps" section with verification tasks only, written as TODO-style checks.
   - Do not invent versions, OS support, or flags; leave them as gaps instead.
5. Require a verify step on written INSTALL docs
   - When evidence supports writing `docs/INSTALL.md`, include a "Verify install"
     section with one command that proves the install worked in a fresh environment.
   - When no verifiable command and no real install evidence exist, report the gap
     and write no `docs/INSTALL.md` file.
6. Troubleshooting only with evidence
   - Add a troubleshooting subsection in `docs/INSTALL.md` only when
     you can cite it from repo evidence (existing issues, error messages in scripts,
     known env vars, CI failures).
   - Otherwise do not include troubleshooting content or speculative fixes.
7. Document dry-run behavior when it exists
   - If scripts that modify files expose a `--dry-run` option, document it in
     `docs/USAGE.md`.
   - Do not invent flags. If a dry-run is missing and would help, note it as a
     "Known gaps" task instead of adding unverified guidance.
8. Keep README scope separate
   - Do not move README content here. If README needs pruning or restructuring,
     use the readme-docs skill and keep INSTALL/USAGE focused on setup and run steps.
9. Update changelog
   - Update `docs/CHANGELOG.md` directly when this skill runs as a standalone task; under `delegate-manager-to-subagents`, dispatch a docs subagent to add the entry.

## docs/INSTALL.md content template

# Install

One paragraph: what "installed" means for this repo (CLI available, importable module, both).

## Requirements
- Bullet list of confirmed requirements (Python version, system tools, OS notes).
- If unknown, add a Known gaps item instead.

## Install steps
- Clone or obtain source (only if repo is not a pip package).
- Create venv (if repo standard) and name it consistently with repo conventions.
- Install dependencies (pip command supported by repo) and avoid unverified extras.
- Install the package (editable or normal) if applicable and supported by evidence.

## Verify install
- One command that proves install worked (for example, `python3 -m <module> --help`
  or import check).

## Troubleshooting
- Only include when supported by repo evidence.

## Known gaps
- Verification tasks only.

## docs/USAGE.md content template

# Usage

One paragraph: what users do with the tool.

## Quick start
- 1 to 3 minimal examples for the primary workflow, written as short command blocks.
- Include inputs and expected outputs at a high level without guessing content.

## CLI
- If a CLI exists, show:
  - How to invoke it and where it lives in the repo.
  - 3 to 6 common flags or subcommands, only if confirmed in repo evidence.

## Examples
- 2 to 4 short examples that match real workflows.
- Prefer realistic filenames and paths that already exist in repo docs or scripts.

## Inputs and outputs
- Inputs: key file types, directories, or formats, with names that match repo usage.
- Outputs: key artifacts, where they appear, and what is generated, in plain terms.

## Known gaps
- Verification tasks only.

## Output

- `docs/INSTALL.md` and `docs/USAGE.md`, written or updated where evidence supports them.
- Short report: created, updated, gaps reported without a file, and known gaps within
  written docs.

## Delegated execution

Under `delegate-manager-to-subagents`, this skill is assigned to a fresh subagent
with one bounded task, the relevant repo rules, and one verification step.
Do not continue the same subagent across unrelated follow-up work; dispatch a
new subagent for each atomic task. See
`docs/REPO_STYLE.md`.
