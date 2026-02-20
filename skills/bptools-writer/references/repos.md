# Repos and Local Paths

This skill assumes these local repos:

- /Users/vosslab/nsh/PROBLEMS/biology-problems
  - Primary target repo for bptools generators.
  - Core shared helper: /Users/vosslab/nsh/PROBLEMS/biology-problems/bptools.py
  - Core authoring guide: /Users/vosslab/nsh/PROBLEMS/biology-problems/docs/QUESTION_AUTHORING_GUIDE.md

- /Users/vosslab/nsh/PROBLEMS/qti_package_maker
  - Packaging/parsing/engine layer used by bptools output paths.
  - CLI converter: /Users/vosslab/nsh/PROBLEMS/qti_package_maker/tools/bbq_converter.py
  - Item model and validation: qti_package_maker/assessment_items/
  - Engine writers/readers: qti_package_maker/engines/
  - Stable upstream reference: https://github.com/vosslab/qti_package_maker/

If paths differ in a session, discover the active locations before editing logic.
