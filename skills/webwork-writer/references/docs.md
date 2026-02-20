# WebWork Authoring Docs (biology-problems)

Use these first when creating or editing PG/PGML problems:

- docs/webwork/WEBWORK_PROBLEM_AUTHOR_GUIDE.md
  - PGML-first structure, randomization rules, inline grading, HTML whitelist.
- docs/webwork/WEBWORK_HEADER_STYLE.md
  - OPL-style header tags (DESCRIPTION, KEYWORDS, DBsubject, etc.).
- docs/webwork/MATCHING_PROBLEMS.md
  - Matching layout patterns, PopUp vs DropDown notes, PG 2.17 constraints.
- docs/webwork/PGML_LINTER_EXPECTATIONS.md
  - Common PGML pitfalls and what the linter should flag.
- docs/webwork/COLOR_TEXT_IN_WEBWORK.md
  - Safe color strategies (PGML tag wrappers vs MathJax).
- docs/webwork/HTML_TO_WEBWORK_PLAN.md
  - HTML translation rules and blocked tags (table, tr, td).
- docs/webwork/RANDOMIZATION_REFERENCE.md
  - PG randomization entry points and seed stability notes.
- docs/webwork/COLOR_CLASS_MIGRATION_PLAN.md
  - Color class migration and strict conversion plan.
- docs/webwork/REPLACEMENT_RULES_IMPLEMENTATION_PLAN.md
  - Replacement rules, sub/sup conversions, and color handling.
- docs/webwork/NICETABLES_TRANSLATION_PLAN.md
  - niceTables translation guidance for HTML tables.
- docs/webwork/INDEX.md
  - Index of all WebWork authoring docs in this repo.

Repo-wide rules to keep in mind:

- docs/REPO_STYLE.md (do not edit locally)
- docs/PYTHON_STYLE.md (do not edit locally)
- docs/MARKDOWN_STYLE.md (do not edit locally)
- docs/CHANGELOG.md (add entries for any edits you make)

Biochemistry PUBCHEM PGML notes (use when editing those problems):

- problems/biochemistry-problems/PUBCHEM/CONVERSION_SUMMARY.md
- problems/biochemistry-problems/PUBCHEM/PGML_SYNTAX_NOTES.md
- problems/biochemistry-problems/PUBCHEM/README_PGML.md

Renderer and lint docs:

- /Users/vosslab/nsh/webwork-pg-renderer/docs/RENDERER_API_USAGE.md
- /Users/vosslab/nsh/webwork-pg-renderer/script/HOW_TO_LINT.md
