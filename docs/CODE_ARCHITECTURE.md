# Code architecture

## Overview

[vosslab-skills](../README.md) is a Claude Code plugin that ships reusable
skills, sub-agent role definitions, and small Python tooling for indexing and
packaging. It is not a runtime application: most of the repo is content
([skills/](../skills/), [agents/](../agents/), [docs/](.)) plus a few
generators in [tools/](../tools/) that keep the published index and plugin
manifest in sync with that content.

The plugin is registered through [.claude-plugin/plugin.json](../.claude-plugin/plugin.json)
and [.claude-plugin/marketplace.json](../.claude-plugin/marketplace.json).
Version is tracked in [VERSION](../VERSION) and mirrored in `plugin.json`.

## Major components

- [skills/](../skills/): one folder per skill, each containing a `SKILL.md`
  with frontmatter (`name`, `description`) and skill
  instructions. These are the user-invocable units (for example
  `/vosslab-skills:audit-code-reviewer`).
- [agents/](../agents/): per-role markdown files (`architect.md`,
  `coder.md`, `expert_coder.md`, `image_evaluator.md`, `integrator.md`,
  `maintainer.md`, `monitor.md`, `orchestrator.md`, `parallelizer.md`,
  `planner.md`, `playwright_operator.md`, `reviewer.md`,
  `scheduler.md`, `tester.md`) used by orchestration skills such as
  [skills/gas-town-workflow/SKILL.md](../skills/gas-town-workflow/SKILL.md)
  and [skills/delegate-manager-to-subagents/SKILL.md](../skills/delegate-manager-to-subagents/SKILL.md).
- [tools/](../tools/): Python generators run from the repo root.
  - [tools/build_skills_index.py](../tools/build_skills_index.py) regenerates
    [docs/SKILLS_INDEX.md](SKILLS_INDEX.md) from `skills/**/SKILL.md`.
  - [tools/build_plugin_manifest.py](../tools/build_plugin_manifest.py) keeps
    [.claude-plugin/plugin.json](../.claude-plugin/plugin.json) keywords in
    sync with skill folder names.
  - [tools/list_loaded_skills.py](../tools/list_loaded_skills.py) walks the
    repo and `~/.claude/` to report which skills are loaded by Claude Code.
- [devel/](../devel/): developer-only helpers.
  - [devel/commit_changelog.py](../devel/commit_changelog.py) supports
    changelog commits.
  - [devel/setup_playwright.sh](../devel/setup_playwright.sh) installs
    Playwright for browser tests.
- [tests/](../tests/): repo-wide lint and convention enforcement (see
  [docs/PYTEST_STYLE.md](PYTEST_STYLE.md) and
  [docs/E2E_TESTS.md](E2E_TESTS.md)) plus shared helpers
  ([tests/file_utils.py](../tests/file_utils.py),
  [tests/conftest.py](../tests/conftest.py)).
- [docs/](.): style guides, install/usage, troubleshooting,
  changelog, and the generated skills index.
- [.claude-plugin/](../.claude-plugin/): plugin and marketplace manifests.

## Data flow

Primary use case (invoke a skill):

1. The user installs the plugin via `claude plugin marketplace add vosslab/vosslab-skills`
   then `claude plugin install vosslab-skills@vosslab-skills`, or clones the repo
   locally; [docs/INSTALL.md](INSTALL.md) covers both paths.
2. Claude Code (or Codex / Gemini) discovers each `skills/<name>/SKILL.md`
   and loads its frontmatter for triggering.
3. The user invokes a skill by name (for example
   `/vosslab-skills:arch-docs`).
4. The skill instructions reference canonical repo rules in
   [docs/REPO_STYLE.md](REPO_STYLE.md),
   [docs/PYTHON_STYLE.md](PYTHON_STYLE.md), and
   [docs/MARKDOWN_STYLE.md](MARKDOWN_STYLE.md) rather than restating them.
5. Manager-style skills may dispatch sub-agents from [agents/](../agents/)
   to execute atomic tasks.

Indexing flow (maintainer side):

1. A skill is added or renamed under [skills/](../skills/).
2. [tools/build_skills_index.py](../tools/build_skills_index.py) regenerates
   [docs/SKILLS_INDEX.md](SKILLS_INDEX.md).
3. [tools/build_plugin_manifest.py](../tools/build_plugin_manifest.py)
   refreshes the plugin keywords list.
4. The change is recorded in [docs/CHANGELOG.md](CHANGELOG.md).

## Testing and verification

The fast-lane test suite lives in [tests/](../tests/) and is run with
`pytest tests/`. Active gates include:

- [tests/test_pyflakes_code_lint.py](../tests/test_pyflakes_code_lint.py)
  (static analysis)
- [tests/test_ascii_compliance.py](../tests/test_ascii_compliance.py)
  (ASCII / ISO-8859-1 only)
- [tests/test_indentation.py](../tests/test_indentation.py)
  (tabs in Python)
- [tests/test_whitespace.py](../tests/test_whitespace.py)
- [tests/test_shebangs.py](../tests/test_shebangs.py)
- [tests/test_init_files.py](../tests/test_init_files.py)
  (minimal `__init__.py` rule)
- [tests/test_import_dot.py](../tests/test_import_dot.py),
  [tests/test_import_star.py](../tests/test_import_star.py),
  [tests/test_import_requirements.py](../tests/test_import_requirements.py)
- [tests/test_test_naming_conventions.py](../tests/test_test_naming_conventions.py)
- [tests/test_bandit_security.py](../tests/test_bandit_security.py)

Browser-driven Playwright tests live under
[tests/playwright/](../tests/playwright/) and are excluded from `pytest tests/`.
See [docs/PLAYWRIGHT_USAGE.md](PLAYWRIGHT_USAGE.md).

## Extension points

- Add a new skill: create `skills/<new-skill>/SKILL.md` following
  [docs/SKILL_NAMING.md](SKILL_NAMING.md) and the
  [skills/skill-writing-guide/SKILL.md](../skills/skill-writing-guide/SKILL.md)
  guide; regenerate [docs/SKILLS_INDEX.md](SKILLS_INDEX.md) with
  [tools/build_skills_index.py](../tools/build_skills_index.py).
- Add a new sub-agent role: drop a markdown file under
  [agents/](../agents/); reference it from the dispatching skill.
- Add a new generator: place it under [tools/](../tools/) with
  `#!/usr/bin/env python3` shebang and document it in
  [docs/USAGE.md](USAGE.md).
- Add a new repo-wide convention test: place it under [tests/](../tests/)
  using the `test_*.py` pytest naming convention.

## Known gaps

- No `pyproject.toml` and no root `pip_requirements.txt`; only
  [pip_requirements-dev.txt](../pip_requirements-dev.txt) exists. Confirm
  whether a runtime requirements manifest is intentionally omitted or should
  be added per [docs/REPO_STYLE.md](REPO_STYLE.md#dependency-manifests).
- A stray plan file `tingly-foraging-mccarthy.md` sits at the repo root.
  Confirm whether it should move under `docs/` or be removed.
