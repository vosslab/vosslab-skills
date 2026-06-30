# AGENTS.md

Canonical rules live in docs/. Read them; this file only points and flags repo quirks.

## Style and rules
- Repo style: docs/REPO_STYLE.md
- Python style: docs/PYTHON_STYLE.md
- Markdown style: docs/MARKDOWN_STYLE.md
- Pytest style: docs/PYTEST_STYLE.md
- E2E tests: docs/E2E_TESTS.md
- Skills index: docs/SKILLS_INDEX.md

## Repo quirks
- Run repo tools via `source source_me.sh && python3 tools/<script>.py` (Python 3.12 only). This is an AI-agent runtime rule, not a requirement for repo scripts.
- Generated files: edit the source, then regenerate; do not hand-edit output. `tools/build_plugin_manifest.py` builds the plugin manifests (`.claude-plugin/plugin.json`) from `skills/**/SKILL.md`; `tools/build_skills_index.py` builds docs/SKILLS_INDEX.md from `skills/**/SKILL.md`; `tools/list_loaded_skills.py` lists loaded skills.
- Only humans run `git commit`; agents stage changes and record them in docs/CHANGELOG.md.
- When changing code, run focused tests on the changed file (tests use the `-k` flag, e.g. `pytest test_feature.py -k changed_file.py`); documentation changes need no tests.

## User directive (overrides defaults)
When in doubt, implement the changes the user asked for rather than waiting for a response; the user is not the best reader and will likely miss your request and then be confused why it was not implemented or fixed.
