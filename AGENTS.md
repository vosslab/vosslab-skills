# AGENTS.md

Canonical rules live in docs/. Read them; this file only points and flags repo quirks.

## Style and rules
- Repo style: docs/REPO_STYLE.md
- Python style: docs/PYTHON_STYLE.md
- Markdown style: docs/MARKDOWN_STYLE.md
- Pytest style: docs/PYTEST_STYLE.md
- E2E tests: docs/E2E_TESTS.md
- Human guidance: docs/HUMAN_GUIDANCE.md
- Skills index: docs/SKILLS_INDEX.md

## Repo quirks
- Run repo Python tools via `source source_me.sh && python3 <path-to-script>.py` (Python 3.12 only). This is an AI-agent runtime rule, not a requirement for repo scripts.
- Generated files: edit the source, then regenerate; do not hand-edit output. `index_lib/build_all.py` validates sidecars and builds the skill index, agent index, and plugin manifests from canonical sources; `index_lib/list_loaded_skills.py` lists loaded skills.
- Preserve existing file content outside the intended edit boundary. Modify files in place, avoid repository-history or staging operations, and record requested changes in docs/CHANGELOG.md.
- When changing code, run focused tests on the changed file (tests use the `-k` flag, e.g. `pytest test_feature.py -k changed_file.py`); documentation changes need no tests.

## User directive (overrides defaults)
When in doubt, implement the changes the user asked for rather than waiting for a response; the user is not the best reader and will likely miss your request and then be confused why it was not implemented or fixed.
