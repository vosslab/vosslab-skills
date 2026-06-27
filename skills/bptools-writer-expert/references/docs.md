# Bptools Authoring Docs

Bundled snapshots of the `biology-problems` authoring docs plus pointers to
live code and external references. Paths are relative to
`skills/bptools-writer-expert/` unless noted otherwise.

Snapshot note: the docs under `references/docs/` were copied from the
`biology-problems` repo. They can drift. For questions where live code
behavior matters, prefer the live files in the target repo
(`git rev-parse --show-toplevel` from inside `biology-problems`).

## Required reading (load before any bptools edit)

Mandated by the Required reading block in `SKILL.md`.

- [references/docs/QUESTION_AUTHORING_GUIDE.md](docs/QUESTION_AUTHORING_GUIDE.md)
  - Primary workflow for creating new generators from TEMPLATE.py.
- `bptools.py` in the target repo root (live file; read via
  `git rev-parse --show-toplevel` + `/bptools.py`).
  - Canonical helper API surface for `formatBB_*`, `collect_and_write_questions`,
    `make_outfile`, and anti-cheat flags.

## Core authoring

- [references/docs/QUESTION_FUNCTION_INDEX.md](docs/QUESTION_FUNCTION_INDEX.md)
  - Index of all `write_question` functions with git dates.
- [references/docs/UNIFICATION_PLAN.md](docs/UNIFICATION_PLAN.md)
  - Standardizing `-d`/`-x` flag handling across generators.
- [references/docs/YAML_QUESTION_BANK_INDEX.md](docs/YAML_QUESTION_BANK_INDEX.md)
  - Index of YAML question banks.

## Domain-specific guides (load when the task touches that domain)

### Matching sets

- [references/docs/problems/matching_sets/MATCHING_SET_AUTHORING_GUIDE.md](docs/problems/matching_sets/MATCHING_SET_AUTHORING_GUIDE.md)
  - Matching-set YAML authoring and generator behavior.

### PubChem biochemistry

- [references/docs/problems/biochemistry-problems/PUBCHEM/README_PUBCHEM_BPTOOLS.md](docs/problems/biochemistry-problems/PUBCHEM/README_PUBCHEM_BPTOOLS.md)
  - PubChem-specific bptools generator patterns and caveats.

### Multiple-choice statements

- [references/docs/problems/multiple_choice_statements/MC_STATEMENTS_AUTHORING_GUIDE.md](docs/problems/multiple_choice_statements/MC_STATEMENTS_AUTHORING_GUIDE.md)
  - MC statements YAML authoring and conversion flow.

### Pedigrees

- [references/docs/problems/inheritance-problems/pedigrees/PEDIGREE_PIPELINE.md](docs/problems/inheritance-problems/pedigrees/PEDIGREE_PIPELINE.md)
  - Pedigree generation pipeline overview.
- [references/docs/problems/inheritance-problems/pedigrees/PEDIGREE_SPEC_v1.md](docs/problems/inheritance-problems/pedigrees/PEDIGREE_SPEC_v1.md)
  - Pedigree data/spec contract.

### Phylogenetic trees

- [references/docs/problems/inheritance-problems/phylogenetic_trees/TREELIB_SPEC_v1.md](docs/problems/inheritance-problems/phylogenetic_trees/TREELIB_SPEC_v1.md)
  - Tree library data/spec contract.
- [references/docs/problems/inheritance-problems/phylogenetic_trees/TREELIB_TECH.md](docs/problems/inheritance-problems/phylogenetic_trees/TREELIB_TECH.md)
  - Tree library technical implementation notes.
- [references/docs/problems/inheritance-problems/phylogenetic_trees/TREELIB_USAGE.md](docs/problems/inheritance-problems/phylogenetic_trees/TREELIB_USAGE.md)
  - Tree library usage patterns and examples.

## External references (live, not bundled)

- `biology-problems/docs/CHANGELOG.md` (target repo) - update when changing code
  or docs.
- `biology-problems/docs/REPO_STYLE.md`, `PYTHON_STYLE.md` (target repo) -
  already loaded via the user's global CLAUDE.md; do not duplicate here.

### qti_package_maker docs (for output/engine behavior)

- `/Users/vosslab/nsh/PROBLEMS/qti_package_maker/docs/USAGE.md`
- `/Users/vosslab/nsh/PROBLEMS/qti_package_maker/docs/FORMATS.md`
- `/Users/vosslab/nsh/PROBLEMS/qti_package_maker/docs/ENGINES.md`
- Stable upstream reference: https://github.com/vosslab/qti_package_maker/
