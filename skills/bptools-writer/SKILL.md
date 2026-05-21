---
name: bptools-writer
description: Create, edit, and validate biology-problems bptools Python question generators and supporting YAML content. Use when requests involve authoring question scripts, updating files under problems/*-problems, tuning randomization or anti-cheat behavior, or debugging BBQ/QTI output that depends on bptools.py and qti_package_maker.
---

# Bptools Question Authoring

## Overview

Use this skill to author regular bptools-based Python generators in `biology-problems`.
Follow the repo's shared generator patterns and verify output with small local runs.

## Required reading (load before any bptools edit)

<EXTREMELY-IMPORTANT>
Before editing any generator script or writing new `write_question()` logic,
you MUST use the Read tool on:

1. `skills/bptools-writer/references/docs/QUESTION_AUTHORING_GUIDE.md`
   - Primary authoring workflow, TEMPLATE.py conventions, required structure.
2. `bptools.py` at the target repo root (this skill is only invoked inside
   `biology-problems`, so the file is reachable at the repo-root path returned
   by `git rev-parse --show-toplevel`).
   - Canonical helper API. Copying signatures from memory drifts fast; read the
     live file so `formatBB_*`, `collect_and_write_questions`, `make_outfile`,
     and anti-cheat flags match what is actually defined.

Do not summarize from memory. Exception: if you already Read both in this
session, say so and continue.
</EXTREMELY-IMPORTANT>

Domain-specific guides in `references/docs/problems/` must be loaded when the
task touches that domain (matching sets, PUBCHEM, MC statements, pedigrees,
phylogenetic trees). See `references/docs.md` for the full index.

## Workflow

1) Satisfy the Required reading block above. This is step zero.
2) Identify scope
   - Confirm the target script(s), question type(s), and output format(s).
   - Read `references/repos.md` to locate the target repo path.
   - Read `references/docs.md` for any additional guides relevant to the task.
3) Start from known patterns
   - Reuse the nearest template in `references/templates.md`.
   - Keep a script structure with `parse_arguments()`, `write_question()`, and
     `main()`.
   - Use shared parser helpers from `bptools` for consistent CLI flags.
4) Implement with bptools primitives
   - Build prompts/choices as plain strings and lists.
   - Format questions with the relevant `bptools.formatBB_*` function.
   - Use `bptools.collect_and_write_questions(...)` and
     `bptools.make_outfile(...)`.
   - Respect anti-cheat defaults and only override intentionally.
5) Validate behavior
   - Run the modified generator with a small count (for example `-d 1`).
   - Check produced BBQ text for formatting and expected answer keys.
   - Run relevant tests for edited code paths.
6) Finish cleanly
   - Update `docs/CHANGELOG.md` directly when this skill runs as a standalone task; under `delegate-manager-to-subagents`, dispatch a docs subagent to add the entry.
   - Keep generated artifacts out of git (`bbq-*.txt`, `qti*.zip`,
     `selftest-*.html`).

## Core Rules

- Treat `references/docs/QUESTION_AUTHORING_GUIDE.md` as the primary authoring reference.
- Maintain Python style required by this repo: tabs for indentation, ASCII comments, `main()` entrypoint.
- Keep randomness well mixed for student-facing content; avoid predictable round-robin selection unless explicitly requested for reproducibility/debugging.
- Keep Blackboard sanitizer compatibility patterns (split comments in JS function declarations) when present in existing generators.
- If output behavior is unclear, inspect both `bptools.py` and the corresponding `qti_package_maker` writer/validator paths before changing format logic.

## Reference Files

- Read `references/docs.md` for the full bundled doc index plus external qti_package_maker pointers.
- Read `references/repos.md` for local repo paths and high-value files.
- Read `references/api_surface.md` for common bptools and qti_package_maker touchpoints.
- Read `references/templates.md` for starter template locations.

## Notes

- Bundled docs under `references/docs/` are snapshots from `biology-problems/`.
  They can drift from the live repo; treat the live repo as authoritative when
  they disagree, and refresh the snapshot when the drift matters.
- Prefer minimal, targeted changes over broad refactors.
- Reuse existing helper utilities instead of copying formatting logic into each script.
- When the request includes new question families (matching sets, MC statements, pedigrees, phylogenetic trees, PubChem), load the matching optional guide before editing.

## Delegated execution

Under `delegate-manager-to-subagents`, this skill is assigned to a fresh subagent
with one bounded task, the relevant repo rules, and one verification step.
Do not continue the same subagent across unrelated follow-up work; dispatch a
new subagent for each atomic task. See
`docs/REPO_STYLE.md`.
