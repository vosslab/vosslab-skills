# File structure

Map of the [vosslab-skills](../README.md) repo: where files live, what they
do, and where to add new work.

## Top-level layout

```text
vosslab-skills/
+- .claude-plugin/             Claude Code plugin and marketplace manifests
+- .codex-plugin/              Codex plugin manifest
+- .cursor-plugin/             Cursor plugin manifest
+- .opencode/                  OpenCode plugin manifest and install doc
+- agents/                     sub-agent role definitions (one .md per role)
+- assets/                     shared static assets (logo, etc.)
+- devel/                      developer-only helpers (changelog, version, clean)
+- docs/                       style guides, install/usage, changelog, index
+- skills/                     user-invocable skills (one folder per skill)
+- tests/                      pytest gates and shared test helpers
+- tools/                      generators kept in sync with skills/ content
+- AGENTS.md                   agent instructions, links into docs/
+- CLAUDE.md                   Claude Code project entry point
+- LICENSE                     license text
+- README.md                   project overview and quick start
+- REPO_TYPE                   repo-type marker for style propagation
+- VERSION                     repo version (mirrored in plugin manifests)
+- pip_requirements-dev.txt    developer Python dependencies
+- pip_extras.txt              extra Python dependencies
`- source_me.sh                shell entry: exports PYTHONUNBUFFERED, etc.
```

## Key subtrees

### [skills/](../skills/)

One folder per skill, each containing a `SKILL.md` with frontmatter
(`name`, `description`) and skill instructions.
Folder name matches the skill name. New skill folders should follow
[docs/SKILL_NAMING.md](SKILL_NAMING.md). The full one-line summary list
is in [docs/SKILLS_INDEX.md](SKILLS_INDEX.md).

### [agents/](../agents/)

Per-role markdown files used by orchestration skills. Current roles:
`architect.md`, `coder.md`, `expert_coder.md`, `image_evaluator.md`,
`integrator.md`, `maintainer.md`, `monitor.md`, `orchestrator.md`,
`parallelizer.md`, `planner.md`, `playwright_operator.md`,
`reviewer.md`, `scheduler.md`, `tester.md`.

### [tools/](../tools/) vs [devel/](../devel/)

- [tools/](../tools/) holds repo content generators that any contributor may
  rerun: [tools/build_skills_index.py](../tools/build_skills_index.py),
  [tools/build_plugin_manifest.py](../tools/build_plugin_manifest.py),
  [tools/list_loaded_skills.py](../tools/list_loaded_skills.py),
  [tools/pdftomd.py](../tools/pdftomd.py),
  [tools/sync_typescript_package_pins.py](../tools/sync_typescript_package_pins.py),
  [tools/plan_headings.sh](../tools/plan_headings.sh).
- [devel/](../devel/) holds developer-only helpers:
  [devel/commit_changelog.py](../devel/commit_changelog.py),
  [devel/query_changelog.py](../devel/query_changelog.py),
  [devel/rotate_changelog.py](../devel/rotate_changelog.py),
  [devel/changelog_lib.py](../devel/changelog_lib.py),
  [devel/bump_version.py](../devel/bump_version.py),
  [devel/flatten_broken_md_links.py](../devel/flatten_broken_md_links.py),
  [devel/dist_clean.sh](../devel/dist_clean.sh),
  [devel/setup_playwright.sh](../devel/setup_playwright.sh), and
  [devel/DEVEL_README.md](../devel/DEVEL_README.md).

### [tests/](../tests/)

Repo-wide pytest gates plus helpers. Run with `pytest tests/`. The
[tests/playwright/](../tests/playwright/) subtree is excluded from pytest
collection by [tests/conftest.py](../tests/conftest.py); see
[docs/PLAYWRIGHT_USAGE.md](PLAYWRIGHT_USAGE.md).
Helper modules: [tests/file_utils.py](../tests/file_utils.py),
[tests/check_ascii_compliance.py](../tests/check_ascii_compliance.py),
[tests/fix_ascii_compliance.py](../tests/fix_ascii_compliance.py),
[tests/fix_whitespace.py](../tests/fix_whitespace.py). Gates also cover
skill frontmatter, internal links, plugin-manifest drift, and Markdown links;
[tests/TESTS_README.md](../tests/TESTS_README.md) documents the suite.

### [docs/](.)

Two flavors live here:

- Centrally maintained style docs (do not edit locally):
  [docs/REPO_STYLE.md](REPO_STYLE.md),
  [docs/PYTHON_STYLE.md](PYTHON_STYLE.md),
  [docs/MARKDOWN_STYLE.md](MARKDOWN_STYLE.md),
  [docs/PYTEST_STYLE.md](PYTEST_STYLE.md),
  [docs/TYPESCRIPT_STYLE.md](TYPESCRIPT_STYLE.md),
  [docs/CLAUDE_HOOK_USAGE_GUIDE.md](CLAUDE_HOOK_USAGE_GUIDE.md),
  [docs/AUTHORS.md](AUTHORS.md).
- Repo-specific docs:
  [docs/INSTALL.md](INSTALL.md), [docs/USAGE.md](USAGE.md),
  [docs/TROUBLESHOOTING.md](TROUBLESHOOTING.md),
  [docs/CHANGELOG.md](CHANGELOG.md) with archive
  [docs/CHANGELOG-2026-06a.md](CHANGELOG-2026-06a.md),
  [docs/NEWS.md](NEWS.md), [docs/RELEASE_HISTORY.md](RELEASE_HISTORY.md),
  [docs/E2E_TESTS.md](E2E_TESTS.md),
  [docs/PLAYWRIGHT_USAGE.md](PLAYWRIGHT_USAGE.md),
  [docs/SKILLS_INDEX.md](SKILLS_INDEX.md),
  [docs/SKILL_NAMING.md](SKILL_NAMING.md),
  [docs/archive/SKILL_PHILOSOPHY_REVIEW.md](archive/SKILL_PHILOSOPHY_REVIEW.md),
  [docs/CODE_ARCHITECTURE.md](CODE_ARCHITECTURE.md),
  [docs/FILE_STRUCTURE.md](FILE_STRUCTURE.md),
  [docs/EXPERT_SKILL-BEST_PRACTICES.md](EXPERT_SKILL-BEST_PRACTICES.md)
  (conventions for authoring domain-expert skills and the local-only reference-survey pattern).
- Archived skill folders live under [docs/archive/skills/](archive/skills/):
  currently [docs/archive/skills/old-manager-review-existing-plan/](archive/skills/old-manager-review-existing-plan/)
  and [docs/archive/skills/old-orchestrate-next-milestone/](archive/skills/old-orchestrate-next-milestone/).
  Archived skills are no longer indexed in `skills/` and are excluded from
  the plugin manifest; historical content is preserved for reference.
  See [docs/archive/skills/README.md](archive/skills/README.md) for
  retirement context and replacements.

### Plugin manifests

Per-platform manifests, all regenerated by
[tools/build_plugin_manifest.py](../tools/build_plugin_manifest.py):

- [.claude-plugin/plugin.json](../.claude-plugin/plugin.json) and
  [.claude-plugin/marketplace.json](../.claude-plugin/marketplace.json)
  for Claude Code.
- [.codex-plugin/plugin.json](../.codex-plugin/plugin.json) for Codex.
- [.cursor-plugin/plugin.json](../.cursor-plugin/plugin.json) for Cursor.
- [.opencode/](../.opencode/) for OpenCode
  ([.opencode/plugins/vosslab_skills.js](../.opencode/plugins/vosslab_skills.js)
  and [.opencode/INSTALL.md](../.opencode/INSTALL.md)).

## Generated artifacts

- [docs/SKILLS_INDEX.md](SKILLS_INDEX.md) is regenerated from
  `skills/**/SKILL.md` by
  [tools/build_skills_index.py](../tools/build_skills_index.py). Edit
  source `SKILL.md` files, not the index.
- The plugin manifests under [.claude-plugin/](../.claude-plugin/),
  [.codex-plugin/](../.codex-plugin/), [.cursor-plugin/](../.cursor-plugin/),
  and [.opencode/](../.opencode/) are regenerated by
  [tools/build_plugin_manifest.py](../tools/build_plugin_manifest.py). Edit the
  source skills, not the manifests.
- `.pytest_cache/` is gitignored and produced by pytest runs.

## Documentation map

- Project overview and quick start: [README.md](../README.md).
- Install (plugin and local clone): [docs/INSTALL.md](INSTALL.md).
- Skill invocation and tooling commands: [docs/USAGE.md](USAGE.md).
- Common issues: [docs/TROUBLESHOOTING.md](TROUBLESHOOTING.md).
- Skill index: [docs/SKILLS_INDEX.md](SKILLS_INDEX.md).
- Architecture: [docs/CODE_ARCHITECTURE.md](CODE_ARCHITECTURE.md).
- Dated change log: [docs/CHANGELOG.md](CHANGELOG.md).

## Where to add new work

- New skill: `skills/<skill-name>/SKILL.md` (folder name matches skill
  name; see [docs/SKILL_NAMING.md](SKILL_NAMING.md)). Regenerate
  [docs/SKILLS_INDEX.md](SKILLS_INDEX.md).
- New sub-agent role: `agents/<role>.md`. Reference it from the
  dispatching skill.
- New generator: [tools/](../tools/), with `#!/usr/bin/env python3`
  shebang and an entry in [docs/USAGE.md](USAGE.md).
- New developer helper: [devel/](../devel/).
- New test gate: `tests/test_*.py` (see
  [docs/PYTEST_STYLE.md](PYTEST_STYLE.md)).
- New documentation: `docs/SCREAMING_SNAKE_CASE.md` per
  [docs/REPO_STYLE.md](REPO_STYLE.md#naming); link from
  [README.md](../README.md) when appropriate.
