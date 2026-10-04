---
name: bptools-writer-expert
description: Create, edit, and review biology-problems bptools question generators and YAML banks, including student-facing wording, distractor design, randomization, anti-cheat, and BBQ/QTI output via `bptools.py` and `qti_package_maker`.
---

# Bptools question authoring

## Overview

Use this skill to author regular bptools-based Python generators in `biology-problems`.
Design each question as a puzzle first, follow the repo's shared generator patterns, and verify
output with small local runs plus a student-text review.

## Required reading (load before any bptools edit)

<EXTREMELY-IMPORTANT>
Before editing any generator script or writing new `write_question()` logic,
you MUST use the Read tool on:

1. `references/docs/QUESTION_AUTHORING_GUIDE.md`
   - Primary authoring workflow, TEMPLATE.py conventions, required structure.
2. `bptools.py` at the target repo root (this skill is only invoked inside
   `biology-problems`, so the file is reachable at the repo-root path returned
   by `git rev-parse --show-toplevel`).
   - Canonical helper API. Copying signatures from memory drifts fast; read the
     live file so `formatBB_*`, `collect_and_write_questions`, `make_outfile`,
     and anti-cheat flags match what is actually defined.
3. For any task that writes or edits student-facing text (stems, choices, hints,
   YAML statements, matching values), also Read:
   - `references/docs/QUESTION_PEDAGOGY_GUIDE.md`: design workflow, distractors, review rubric.
   - `references/docs/QUESTION_VOICE_GUIDE.md`: stem anatomy, choices, instructions, mechanics.

Summarize only from the live text of these files. Exception: if you already
Read them in this session, say so and continue.
</EXTREMELY-IMPORTANT>

Use `references/question_voice.md` to jump from a task to the exact guide headings and rubric
items. Read `references/docs/QUESTION_EXEMPLARS.md` when choosing an exemplar (step 3).

Domain-specific guides in `references/docs/problems/` must be loaded when the
task touches that domain (matching sets, PUBCHEM, MC statements, pedigrees,
phylogenetic trees). See `references/docs.md` for the full index.

## Workflow

0) Classify the request and detect project state
   - Use `references/topic_index.md` as the routing front door: match the request to a row
     and load the named guide before opening any generator file.
   - Use `references/task_selection.md` to classify question family, item type, reasoning
     target, output format, randomization scope, and anti-cheat policy before writing code.
   - Use `references/project_workflow.md` to detect whether the target repo is greenfield
     (no generator exists for this question type) or existing (generators already present).
     Greenfield: write the authoring contract (puzzle design included), start from TEMPLATE.py,
     implement with bptools primitives, validate with a small run, then run the student-text
     review.
     Existing repo: inspect-first (read live bptools.py, inventory generators, audit the
     current student-facing text against the rubric), make one generator change at a time,
     then collect the four proof artifacts listed in `references/testing_and_oracles.md`.

1) Satisfy the Required reading block above. This is step zero.
2) Identify scope
   - Confirm the target script(s), question type(s), and output format(s).
   - Read `references/repos.md` to locate the target repo path.
   - Read `references/docs.md` for any additional guides relevant to the task.
3) Design the puzzle before code
   - Follow the Design workflow in `references/docs/QUESTION_PEDAGOGY_GUIDE.md`.
   - Record in the authoring contract (`references/project_workflow.md`):
     - Reasoning target: apply, analyze, evaluate, or recall.
     - Data: the figure, table, cross, sequence, or scenario that forces the reasoning.
     - Named student errors, one per wrong choice (the distractors); mark any absurd choice.
     - Chosen exemplar from `references/docs/QUESTION_EXEMPLARS.md`.
     - Draft stem: data first, one rule sentence if needed, one case sentence, one short question.
4) Start from known patterns
   - Reuse the nearest template in `references/templates.md`.
   - Keep a script structure with `parse_arguments()`, `write_question()`, and
     `main()`.
   - Use shared parser helpers from `bptools` for consistent CLI flags.
5) Implement with bptools primitives
   - Build prompts/choices as plain strings and lists.
   - Compute each distractor in code from its named error, with a comment naming the error.
   - Format questions with the relevant `bptools.formatBB_*` function.
   - Use `bptools.collect_and_write_questions(...)` and
     `bptools.make_outfile(...)`.
   - Respect anti-cheat defaults and only override intentionally.
6) Validate behavior (small run)
   - Run the modified generator with a small count (for example `-d 1`).
   - Check produced BBQ text for formatting and expected answer keys.
   - Run relevant tests for edited code paths.
   - Use `references/testing_and_oracles.md` for fixtures, oracles, and invariants.
7) Student-text review
   - Render several items (for example `-d 5`) and read each stem and choice set as a student.
   - Run `source source_me.sh && python3 devel/check_question_text.py -i <bbq file>` from the
     target repo root; treat findings as advisory prompts for a closer read.
   - Verify the key independently, by item type, per Answer verification in the pedagogy guide.
   - Apply the Review rubric items routed in `references/question_voice.md`, revise, and re-run.
8) Finish cleanly
   - Update `docs/CHANGELOG.md` directly when this skill runs as a standalone task; under `delegate-manager-to-subagents`, dispatch a docs subagent to add the entry.
   - Keep generated artifacts out of git (`bbq-*.txt`, `qti*.zip`,
     `selftest-*.html`).

## Core rules

- Treat `references/docs/QUESTION_AUTHORING_GUIDE.md` as the primary authoring reference.
- Questions are puzzles with few words: the data carries the difficulty, distractors come from
  named student errors, and seriously absurd choices are welcome alongside them.
- Maintain Python style required by this repo: tabs for indentation, ASCII comments, `main()` entrypoint.
- Draw scenarios with true randomness for student-facing content; reserve deterministic scenario
  selection for debugging, reproducibility checks, or unit tests. Follow the voice guide's
  natural choice order when one exists; shuffle choices with no meaningful order.
- Keep Blackboard sanitizer compatibility patterns (split comments in JS function declarations) when present in existing generators.
- If output behavior is unclear, inspect both `bptools.py` and the corresponding `qti_package_maker` writer/validator paths before changing format logic.

## Reference files

- Read `references/question_voice.md` for task-to-heading routing in the bundled guides and the
  rubric item IDs.
- Read `references/testing_and_oracles.md` for the fixture corpus, oracles, and proof artifacts.
- Read `references/api_surface.md` for common bptools and qti_package_maker touchpoints.

## Notes

- Bundled docs under `references/docs/` are snapshots from `biology-problems/`.
  They can drift from the live repo; treat the live repo as authoritative when
  they disagree, and refresh the snapshot when the drift matters.
- Prefer minimal, targeted changes over broad refactors.
- Reuse existing helper utilities instead of copying formatting logic into each script.
- When the request includes new question families (matching sets, MC statements, pedigrees, phylogenetic trees, PubChem), load the matching optional guide before editing.
