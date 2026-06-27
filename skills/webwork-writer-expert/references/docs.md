# WebWork Authoring Docs

All authoring, tooling, and reference docs bundled with this skill. Paths are
relative to `skills/webwork-writer-expert/`.

## Required reading (load before any PGML edit)

The skill mandates reading these three before editing any `.pg`/`.pgml` file.
See the Required reading block in `SKILL.md`.

- [references/docs/HOW_TO_LINT.md](docs/HOW_TO_LINT.md)
  - How to run the local renderer API lint / render a problem end-to-end.
- [references/docs/PG_COMMON_PITFALLS.md](docs/PG_COMMON_PITFALLS.md)
  - Catalog of PG/PGML mistakes the renderer and reviewers catch repeatedly.
- [references/docs/WEBWORK_PROBLEM_AUTHOR_GUIDE.md](docs/WEBWORK_PROBLEM_AUTHOR_GUIDE.md)
  - Canonical authoring reference: PGML-first structure, randomization rules,
    inline grading, HTML whitelist.

## Core authoring

- [references/docs/webwork/WEBWORK_HEADER_STYLE.md](docs/webwork/WEBWORK_HEADER_STYLE.md)
  - OPL-style header tags (DESCRIPTION, KEYWORDS, DBsubject, etc.).
- [references/docs/webwork/PGML_LINTER_EXPECTATIONS.md](docs/webwork/PGML_LINTER_EXPECTATIONS.md)
  - Common PGML pitfalls and what the linter should flag.
- [references/docs/webwork/PGML_QUESTION_TYPES.md](docs/webwork/PGML_QUESTION_TYPES.md)
  - Preferred PGML style patterns for common question types in this repo.
- [references/docs/webwork/QUESTION_STATEMENT_EMPHASIS.md](docs/webwork/QUESTION_STATEMENT_EMPHASIS.md)
  - Highlighting key phrases and data in PGML question statements.

## Question-type specific

- [references/docs/webwork/MATCHING_PROBLEMS.md](docs/webwork/MATCHING_PROBLEMS.md)
  - Matching layout patterns, PopUp vs DropDown notes, PG 2.17 constraints.
- [references/docs/webwork/ORDERING_PROBLEMS.md](docs/webwork/ORDERING_PROBLEMS.md)
  - Ordering (rank/sequence / DraggableProof) question patterns.

## Graphs and molecules

- [references/docs/webwork/HOW_TO_MAKE_GRAPHS.md](docs/webwork/HOW_TO_MAKE_GRAPHS.md)
  - Static display graphs via `PGgraphmacros.pl` on the local PG 2.17 renderer.
- [references/docs/webwork/RDKIT_MOLECULAR_STRUCTURES.md](docs/webwork/RDKIT_MOLECULAR_STRUCTURES.md)
  - Rendering SMILES molecules with RDKit.js in PGML.

## Color and accessibility

- [references/docs/webwork/COLOR_TEXT_IN_WEBWORK.md](docs/webwork/COLOR_TEXT_IN_WEBWORK.md)
  - Safe color strategies (PGML tag wrappers vs MathJax).
- [references/docs/webwork/COLOR_CLASS_MIGRATION_PLAN.md](docs/webwork/COLOR_CLASS_MIGRATION_PLAN.md)
  - Color class migration and strict conversion plan.
- [references/docs/webwork/COLOR_CONTRAST_ACCESSIBILITY.md](docs/webwork/COLOR_CONTRAST_ACCESSIBILITY.md)
  - Target contrast ratios and accessibility guidance.

## HTML and tables

- [references/docs/webwork/HTML_TO_WEBWORK_PLAN.md](docs/webwork/HTML_TO_WEBWORK_PLAN.md)
  - HTML translation rules and blocked tags (table, tr, td).
- [references/docs/webwork/NICETABLES_TRANSLATION_PLAN.md](docs/webwork/NICETABLES_TRANSLATION_PLAN.md)
  - niceTables translation guidance for HTML tables.
- [references/docs/webwork/REPLACEMENT_RULES_IMPLEMENTATION_PLAN.md](docs/webwork/REPLACEMENT_RULES_IMPLEMENTATION_PLAN.md)
  - Replacement rules, sub/sup conversions, and color handling.

## Randomization

- [references/docs/webwork/RANDOMIZATION_REFERENCE.md](docs/webwork/RANDOMIZATION_REFERENCE.md)
  - PG randomization entry points and seed stability notes.

## PG version notes

- [references/docs/webwork/PG_2_17_RENDERER_MACROS.md](docs/webwork/PG_2_17_RENDERER_MACROS.md)
  - Available macro files in the local PG 2.17 renderer.
- [references/docs/webwork/PG_2.20_to_2.16_features.md](docs/webwork/PG_2.20_to_2.16_features.md)
  - Feature comparison across PG 2.16 through 2.20 (a `.txt` twin exists and is
    intentionally not listed separately).

## Index

- [references/docs/webwork/INDEX.md](docs/webwork/INDEX.md)
  - Raw index of docs in the `webwork/` subfolder.

## PubChem biochem notes

Use when editing PUBCHEM PGML problems.

- [references/docs/pubchem/PGML_PUBCHEM_CONVERSION_SUMMARY.md](docs/pubchem/PGML_PUBCHEM_CONVERSION_SUMMARY.md)
- [references/docs/pubchem/PUBCHEM_PGML_SYNTAX_NOTES.md](docs/pubchem/PUBCHEM_PGML_SYNTAX_NOTES.md)
- [references/docs/pubchem/README_PUBCHEM_PGML.md](docs/pubchem/README_PUBCHEM_PGML.md)

## Renderer and lint tooling

- [references/linting.md](linting.md) - local lint and render instructions.
- [references/docs/RENDERER_API_USAGE.md](docs/RENDERER_API_USAGE.md) - renderer API reference.
- [references/docs/HOW_TO_LINT.md](docs/HOW_TO_LINT.md) - also listed under Required reading.
