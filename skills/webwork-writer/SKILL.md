---
name: webwork-writer
description: Create, edit, and lint WeBWorK PG/PGML questions following docs/webwork guidance, HTML whitelist constraints, and renderer-based lint checks. Use for tasks like authoring new PGML problems, adjusting randomization or grading, fixing PGML rendering issues, and running renderer API linting.
---

# WebWork Question Authoring

## Overview

Use this skill to author or adjust PG/PGML problems with the local WebWork renderer, repo rules, and the docs in references/.

## Required reading (load before any PGML edit)

<EXTREMELY-IMPORTANT>
Before editing any `.pg` or `.pgml` file, before proposing fixes, and before
running the renderer, you MUST use the Read tool on each of these files:

1. `skills/webwork-writer/references/docs/HOW_TO_LINT.md`
2. `skills/webwork-writer/references/docs/PG_COMMON_PITFALLS.md`
3. `skills/webwork-writer/references/docs/WEBWORK_PROBLEM_AUTHOR_GUIDE.md`

Do not summarize from memory. Do not skip because "you already know PGML."
Agents that skip these docs ship problems with well-known pitfalls that fail
renderer lint and waste human review time.

Exception: if you have already Read all three files earlier in the same session,
you do not need to re-read them. State explicitly that you already loaded them
this session before continuing.
</EXTREMELY-IMPORTANT>

## Workflow

1) Satisfy the Required reading block above. This is step zero; nothing else
   happens first.
2) Identify the target repo and file, then read any additional relevant doc
   references from `references/docs.md` for the question type at hand.
3) Apply the PGML structure and rules from the WebWork author guide.
4) Make edits in the problem file and update `docs/CHANGELOG.md` directly when this skill runs as a standalone task; under `delegate-manager-to-subagents`, dispatch a docs subagent to add the entry.
5) Render with `-r` using the local renderer API to visually confirm layout and
   checkbox behavior (prerequisite).
6) Lint or render with the local renderer API when the change affects PGML
   output.

## Core Rules (from repo docs)

- Use PGML-first structure with inline grading; keep setup, answers, and PGML text in separate sections.
- PGML is single-pass: do not build PGML tag wrappers inside Perl strings. If a variable contains HTML, render it with `[$var]*`.
- HTML whitelist blocks `table`, `tr`, `td`; use flexbox divs or niceTables instead.
- For matching problems on PG 2.17, use PopUp widgets and HTML-only `MODES(TeX => '', HTML => ...)` wrappers for layout.
- Prefer local `PGrandom` seeded with `problemSeed` for deterministic randomization; avoid `SRAND` unless you want to reset the global RNG; sort hash keys before random selection.
- Avoid MathJax color macros; use HTML spans and CSS for color.
- Always render with `-r` to visually confirm layout and checkbox behavior before reporting results.

## Self-contained PGML files

PGML files are uploaded to the problem server individually, so each file must
be fully self-contained. Do not factor shared helpers into a sibling `.pl`
macro and `loadMacros()` it from several PGMLs -- the uploaded file will not
have access to it.

When several PGML files need the same helpers (SVG primitives, lookup tables,
domain utilities), inline a copy of the helpers inside each file. To keep
maintenance sane, wrap each reusable chunk in a clearly labelled block so it
can be copy-pasted between files verbatim:

```perl
# ==== BEGIN BLOCK: svg_primitives (v1) ====
sub svg_text { ... }
sub svg_rect { ... }
# ==== END BLOCK: svg_primitives ====
```

Conventions:

- Use `# ==== BEGIN BLOCK: <name> (v<N>) ====` and matching `END BLOCK` lines.
- Bump the version suffix when the block changes so drift across files is easy
  to spot with `grep`.
- Keep each block independent (no cross-block calls that aren't also in the
  block set) so a block can be dropped into a new file without pulling in a
  whole web of dependencies.
- When fixing a bug in a block, update every PGML that carries it; a repo-wide
  `grep` on the block name surfaces them all.

## Reference Files

- Read references/repos.md to locate local repos and paths.
- Read references/docs.md for the full index of authoring docs, grouped by purpose.
- Read references/linting.md to run renderer API linting.
- Check bundled reference docs and examples; render them when needed to confirm renderer capabilities (for example, whether a macro is present).

## Notes

- Keep solution text plain when exporting to systems that do not render HTML.
- For matching problems, use the PG 2.17-safe patterns documented in docs/webwork.

## Delegated execution

Under `delegate-manager-to-subagents`, this skill is assigned to a fresh subagent
with one bounded task, the relevant repo rules, and one verification step.
Do not continue the same subagent across unrelated follow-up work; dispatch a
new subagent for each atomic task. See
`docs/REPO_STYLE.md`.
