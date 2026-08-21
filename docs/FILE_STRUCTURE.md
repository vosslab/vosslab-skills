# File structure

This map describes the tracked repository layout, canonical data, generated outputs, and installer
destinations.

## Top-level layout

```text
vosslab-skills/
+- .claude-plugin/             Tracked generated Claude manifests
+- .codex-plugin/              Tracked generated Codex manifest
+- .cursor-plugin/             Tracked generated Cursor manifest
+- .opencode/                  Tracked OpenCode plugin output; local agents are ignored
+- agents/                     Authored agent Markdown and CATALOG.yaml
+- assets/                     Shared static assets
+- devel/                      Maintainer-only setup, repair, and release tools
+- docs/                       User, architecture, style, generated, and archived docs
+- install_lib/                Shared discovery, adapter, interview, and installer package
+- install_targets/            Per-platform installation declarations
+- skills/                     Category metadata and canonical skill trees
+- tests/                      Fast pytest, non-browser E2E, and browser test homes
+- tools/                      Repository generators and validators
+- AGENTS.md                   Repository instructions and rule pointers
+- install_skills.py           Main guided installer
+- README.md                   Project overview and quick start
+- source_me.sh                Repository Python environment bootstrap
+- VERSION                     Version source for generated manifests
+- pip_requirements*.txt       Python runtime and development dependencies
`- package.json                Supporting TypeScript and Playwright tool manifest
```

## Key subtrees

### Skills

[skills/](../skills/) uses one metadata-backed directory per category:

```text
skills/
+- documentation/
+- experts/
+- management/
+- orientation/
+- planning/
`- quality/
```

Each category contains `CATEGORY.md`. Each active skill normally contains:

```text
skills/<category>/<skill-name>/
+- SKILL.md
+- agents/
|  `- openai.yaml
+- references/                 Optional detailed guidance
+- scripts/                    Optional executable helpers
+- assets/                     Optional reusable assets
`- templates/                 Optional reusable templates
```

[install_lib/skill_discovery.py](../install_lib/skill_discovery.py) validates this structure.
[tools/build_skills_index.py](../tools/build_skills_index.py) renders
[SKILLS_INDEX.md](SKILLS_INDEX.md), and
[tools/openai_sidecars.py](../tools/openai_sidecars.py) validates the OpenAI sidecars and
category-required paths.

### Agents and installation

[agents/](../agents/) contains authored Claude-compatible Markdown.
[agents/CATALOG.yaml](../agents/CATALOG.yaml) owns role, access, authority, and escalation data.
[AGENTS_INDEX.md](AGENTS_INDEX.md) is its generated searchable index.

[install_targets/](../install_targets/) contains one `TARGET.md` for each declared platform:

| Target | Tier | Skill destination | Agent destination |
| --- | --- | --- | --- |
| Claude | primary | `.claude/skills` | `.claude/agents` |
| Codex | primary | `.codex/skills` | `.codex/agents` |
| Cursor | compatibility | `.cursor/skills` | `.cursor/agents` |
| OpenCode | compatibility | `.config/opencode/skills` | `.config/opencode/agents` |

[install_lib/](../install_lib/) contains frontmatter parsing, discovery, adapter rendering, target
validation, the interview, and state-free installation behavior.

### Tests

[tests/](../tests/) is divided by execution model:

- `tests/test_*.py` provides the fast, deterministic pytest lane.
- [tests/e2e/](../tests/e2e/) contains non-browser whole-CLI orchestration and is excluded from
  pytest collection.
- [tests/playwright/](../tests/playwright/) is reserved for browser-driven tests.
- [tests/conftest.py](../tests/conftest.py) owns collection exclusions and repository hygiene
  filters.
- [tests/TESTS_README.md](../tests/TESTS_README.md) documents the tier boundaries.

No tracked fixture directory was added for the installer work. Permanent test inputs remain inline
or are written beneath `tmp_path`.

### Tools and development

[tools/](../tools/) contains repository-facing generators and validators. Shared runtime behavior
used by the installer and tools belongs in [install_lib/](../install_lib/).

[devel/](../devel/) contains maintainer-only setup, changelog, cleanup, versioning, and release
commands. Reusable runtime modules and permanent tests do not belong there.

## Generated artifacts

The repository intentionally tracks these small generated artifacts:

| Generated path | Owner |
| --- | --- |
| [SKILLS_INDEX.md](SKILLS_INDEX.md) | [tools/build_skills_index.py](../tools/build_skills_index.py) |
| [AGENTS_INDEX.md](AGENTS_INDEX.md) | [tools/build_agents_index.py](../tools/build_agents_index.py) |
| [.claude-plugin/](../.claude-plugin/) | [tools/build_plugin_manifest.py](../tools/build_plugin_manifest.py) |
| [.codex-plugin/](../.codex-plugin/) | [tools/build_plugin_manifest.py](../tools/build_plugin_manifest.py) |
| [.cursor-plugin/](../.cursor-plugin/) | [tools/build_plugin_manifest.py](../tools/build_plugin_manifest.py) |
| [.opencode/INSTALL.md](../.opencode/INSTALL.md) | [tools/build_plugin_manifest.py](../tools/build_plugin_manifest.py) |
| [.opencode/plugins/vosslab_skills.js](../.opencode/plugins/vosslab_skills.js) | [tools/build_plugin_manifest.py](../tools/build_plugin_manifest.py) |

Platform-native agent projections are generated during installation. They live in the selected
home, not in the tracked repository. Codex links category directories beneath `.codex/skills`;
Claude keeps individual skill links flat beneath `.claude/skills`. Cursor and OpenCode use their
native global roots. Skill trees and authored Claude agents are linked directly to the clone rather
than regenerated or copied. The installer creates no separate receipt, version record, cache, or
hidden configuration.

## Local and ignored material

[.gitignore](../.gitignore) excludes:

- Hidden runtime skill trees under `skills/.*/`.
- Local reference corpora under `local-only/` and local book inputs under `books_to_process/`.
- Repository-local generated agent folders for Codex, Cursor, and OpenCode.
- Temporary output, dependency installs, build output, coverage, and browser test reports.

These paths are local state, not canonical repository structure.

## Documentation map

- [README.md](../README.md): Project purpose and quick start.
- [INSTALL.md](INSTALL.md): Requirements, targets, interview, links, and updates.
- [USAGE.md](USAGE.md): Maintainer commands and installer lifecycle.
- [CODE_ARCHITECTURE.md](CODE_ARCHITECTURE.md): Components, data flow, verification, and extension
  points.
- [SKILLS_INDEX.md](SKILLS_INDEX.md): Generated public skill catalog.
- [AGENTS_INDEX.md](AGENTS_INDEX.md): Generated agent catalog.
- [REPO_STYLE.md](REPO_STYLE.md): Repository placement and workflow rules.
- [PYTEST_STYLE.md](PYTEST_STYLE.md): Permanent-test and fixture policy.
- [E2E_TESTS.md](E2E_TESTS.md): Whole-system test placement.
- [archive/](archive/): Completed reports, decisions, and retired source material.

Root [AGENTS.md](../AGENTS.md) points agents to the canonical style documents. Root
[README.md](../README.md) remains the user-facing landing page.

## Where to add new work

- Skills and skill-owned resources: [skills/](../skills/).
- Authored agents and catalog data: [agents/](../agents/).
- Shared installer or generator logic: [install_lib/](../install_lib/).
- Repository generators and validators: [tools/](../tools/).
- Maintainer-only setup and release scripts: [devel/](../devel/).
- Fast tests: [tests/](../tests/); whole-CLI checks: [tests/e2e/](../tests/e2e/).
- Durable documentation: [docs/](.); completed work records:
  [docs/archive/](archive/).
