# WebWork Authoring Docs (biology-problems)

Use these first when creating or editing PG/PGML problems:

- references/docs/webwork/WEBWORK_PROBLEM_AUTHOR_GUIDE.md
  - PGML-first structure, randomization rules, inline grading, HTML whitelist.
- references/docs/webwork/WEBWORK_HEADER_STYLE.md
  - OPL-style header tags (DESCRIPTION, KEYWORDS, DBsubject, etc.).
- references/docs/webwork/MATCHING_PROBLEMS.md
  - Matching layout patterns, PopUp vs DropDown notes, PG 2.17 constraints.
- references/docs/webwork/PGML_LINTER_EXPECTATIONS.md
  - Common PGML pitfalls and what the linter should flag.
- references/docs/webwork/COLOR_TEXT_IN_WEBWORK.md
  - Safe color strategies (PGML tag wrappers vs MathJax).
- references/docs/webwork/HTML_TO_WEBWORK_PLAN.md
  - HTML translation rules and blocked tags (table, tr, td).
- references/docs/webwork/RANDOMIZATION_REFERENCE.md
  - PG randomization entry points and seed stability notes.
- references/docs/webwork/COLOR_CLASS_MIGRATION_PLAN.md
  - Color class migration and strict conversion plan.
- references/docs/webwork/REPLACEMENT_RULES_IMPLEMENTATION_PLAN.md
  - Replacement rules, sub/sup conversions, and color handling.
- references/docs/webwork/NICETABLES_TRANSLATION_PLAN.md
  - niceTables translation guidance for HTML tables.
- references/docs/webwork/INDEX.md
  - Index of all WebWork authoring docs in this repo.

Repo-wide rules to keep in mind:

- docs/REPO_STYLE.md (do not edit locally)
- docs/PYTHON_STYLE.md (do not edit locally)
- docs/MARKDOWN_STYLE.md (do not edit locally)
- docs/CHANGELOG.md (add entries for any edits you make)

Biochemistry PUBCHEM PGML notes (use when editing those problems):

- references/docs/pubchem/PGML_PUBCHEM_CONVERSION_SUMMARY.md
- references/docs/pubchem/PUBCHEM_PGML_SYNTAX_NOTES.md
- references/docs/pubchem/README_PUBCHEM_PGML.md

Renderer and lint docs:

- references/linting.md (local lint and render instructions)
- references/docs/RENDERER_API_USAGE.md
- references/docs/HOW_TO_LINT.md
