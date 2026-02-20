# Bptools Authoring Docs (biology-problems)

Read these first for any bptools Python authoring task:

- docs/QUESTION_AUTHORING_GUIDE.md
  - Primary workflow for creating new generators from TEMPLATE.py.
- docs/REPO_STYLE.md
  - Repo organization, naming, and doc conventions.
- docs/PYTHON_STYLE.md
  - Python style rules (tabs, structure, lint expectations).
- docs/CHANGELOG.md
  - Update when changing code or docs.
- docs/QUESTION_FUNCTION_INDEX.md
  - Index of all write_question functions with git dates.
- docs/UNIFICATION_PLAN.md
  - Standardizing `-d`/`-x` flag handling across generators.
- docs/YAML_QUESTION_BANK_INDEX.md
  - Index of YAML question banks.
- bptools.py
  - Core shared helper module; read for API surface before authoring.

Optional domain-specific guides (load only when relevant):

- problems/matching_sets/MATCHING_SET_AUTHORING_GUIDE.md
  - Matching-set YAML authoring and generator behavior.
- problems/biochemistry-problems/PUBCHEM/README_PUBCHEM_BPTOOLS.md
  - PubChem-specific bptools generator patterns and caveats.
- problems/multiple_choice_statements/MC_STATEMENTS_AUTHORING_GUIDE.md
  - MC statements YAML authoring and conversion flow.
- problems/inheritance-problems/pedigrees/PEDIGREE_PIPELINE.md
  - Pedigree generation pipeline overview.
- problems/inheritance-problems/pedigrees/PEDIGREE_SPEC_v1.md
  - Pedigree data/spec contract.
- problems/inheritance-problems/phylogenetic_trees/TREELIB_SPEC_v1.md
  - Tree library data/spec contract.
- problems/inheritance-problems/phylogenetic_trees/TREELIB_TECH.md
  - Tree library technical implementation notes.
- problems/inheritance-problems/phylogenetic_trees/TREELIB_USAGE.md
  - Tree library usage patterns and examples.

qti_package_maker docs (for output/engine behavior):

- /Users/vosslab/nsh/PROBLEMS/qti_package_maker/docs/USAGE.md
- /Users/vosslab/nsh/PROBLEMS/qti_package_maker/docs/FORMATS.md
- /Users/vosslab/nsh/PROBLEMS/qti_package_maker/docs/ENGINES.md
- Stable upstream reference: https://github.com/vosslab/qti_package_maker/
