# Code architecture

## Overview

[vosslab-skills](../README.md) is a content-first skills repository with a guided Python
installer. Authored Markdown and YAML remain canonical; generators create small tracked indexes
and plugin manifests, while installation links source content into platform-owned directories.

Claude and Codex are primary targets. Cursor, OpenCode, Grok, and Hermes are compatibility targets
with structural adapter validation rather than a live-client guarantee.

## Major components

### Canonical content

| Component | Path | Responsibility |
| --- | --- | --- |
| Skill sources | [skills/](../skills/) | Category metadata, `SKILL.md`, OpenAI sidecars, references, scripts, and assets |
| Agent sources | [agents/](../agents/) | Authored agent Markdown plus canonical role and access data |
| Platform targets | [install_targets/](../install_targets/) | Adapter, support tier, skill layout, and destination declarations |
| Version source | [VERSION](../VERSION) | Repository version normalized at manifest boundaries |

Each direct category under [skills/](../skills/) owns a `CATEGORY.md`. Each published skill owns
its `SKILL.md` and `agents/openai.yaml`. [agents/CATALOG.yaml](../agents/CATALOG.yaml) must match
the authored agent filenames and escalation routes.

### Index and installer libraries

[install_skills.py](../install_skills.py) is the human-facing entry point. It resolves the
repository root through Git and starts the interview in
[install_lib/interview.py](../install_lib/interview.py).

The root [index_lib/](../index_lib/) package owns canonical indexing and projection behavior:

- [index_lib/frontmatter.py](../index_lib/frontmatter.py) parses YAML metadata and converts
  repository CalVer to strict manifest SemVer.
- [index_lib/skill_discovery.py](../index_lib/skill_discovery.py) validates categories and
  produces tracked or filesystem-backed skill inventories.
- [index_lib/agent_catalog.py](../index_lib/agent_catalog.py) validates agent parity and
  renders Codex, Cursor, and OpenCode projections.
- [index_lib/build_all.py](../index_lib/build_all.py) validates sidecars and builds or checks every
  tracked index and plugin projection in one run.

The root [install_lib/](../install_lib/) package owns installation behavior:

- [install_lib/install_target_data.py](../install_lib/install_target_data.py) validates target
  declarations, URLs, and contained destination paths.
- [install_lib/installer.py](../install_lib/installer.py) builds plans, preserves matching entries,
  replaces stale skill links or agent files from the authoritative repository source, and unlinks
  leftover symlinks into this clone that no current skill or agent claims.
- [install_lib/interview.py](../install_lib/interview.py) owns prompts, summaries, and final
  confirmation.

[source_me.sh](../source_me.sh) exposes both root packages through `PYTHONPATH` after loading the
user shell environment. Neither runtime package depends on [tools/](../tools/).

### Generators and validators

| Tool | Canonical input | Tracked output or result |
| --- | --- | --- |
| [index_lib/build_skills_index.py](../index_lib/build_skills_index.py) | Categories and skill frontmatter | [SKILLS_INDEX.md](SKILLS_INDEX.md) |
| [index_lib/build_agents_index.py](../index_lib/build_agents_index.py) | Agent catalog and authored Markdown | [AGENTS_INDEX.md](AGENTS_INDEX.md) |
| [index_lib/build_plugin_manifest.py](../index_lib/build_plugin_manifest.py) | Skill inventory and [VERSION](../VERSION) | Platform plugin manifests |
| [index_lib/openai_sidecars.py](../index_lib/openai_sidecars.py) | Skill sidecars and category requirements | Validation result only |

The generators support check-only validation where documented in [USAGE.md](USAGE.md). Generated
files are small and intentionally tracked.

## Data flow

### Guided installation

1. [install_skills.py](../install_skills.py) resolves the Git root and starts the interview.
2. The installer uses the operating-system home and asks which platforms to install. Claude and
   Codex are the default selection.
3. Target metadata is loaded from [install_targets/](../install_targets/).
4. Skill discovery reads the tracked category and skill sources. Agent discovery validates
   [agents/CATALOG.yaml](../agents/CATALOG.yaml) against authored Markdown.
5. Each target's `skill_layout` decides the link shape. `category` targets (Codex, Hermes) link
   canonical category directories beneath their skills root; `flat` targets (Claude, Cursor,
   OpenCode, Grok) link individual skills. Authored Claude agents become absolute symlinks to this
   clone for Claude and Grok.
6. Codex, Cursor, and OpenCode agent projections become regular files because no authored file
   exists in those native formats. The `skills_only` adapter (Hermes) projects no agents.
7. Final confirmation installs the repository version over mismatched destination entries, then
   unlinks any symlink directly beneath the target's destinations whose target resolves inside this
   clone but matches no planned item.

Edits to linked source content are visible immediately. Re-running the interview refreshes
generated agent projections and changed links. Moving the clone requires another installer run so
links can point to the new location. The installer writes no receipt, version record, cache, or
hidden configuration; ownership of a stale entry is proven only by a symlink target inside this
clone, so generated agent files are never pruned.

### Repository generation

1. Maintainers edit canonical category, skill, sidecar, agent, catalog, or version data.
2. Generators render expected tracked outputs; the sidecar validator reports contract problems.
3. A normal generator run writes output. Generator `--check` forms and the sidecar
   `--check` command validate without writing.
4. Drift tests and repository checks enforce parity with canonical data.

## Testing and verification

- Fast, offline pytest tests live directly under [tests/](../tests/). Installer filesystem tests
  use `tmp_path`; they do not run the CLI as a subprocess.
- [tests/e2e/e2e_primary_adapter_contract.py](../tests/e2e/e2e_primary_adapter_contract.py)
  drives the real guided CLI in a temporary home and validates source links, generated agents, and
  state-free repetition.
- [tests/playwright/](../tests/playwright/) is reserved for browser-driven checks and currently
  contains only the shared repository-root helper.
- Generator `--check` commands validate tracked generated artifacts. The permanent and one-time
  validation split is recorded in
  [archive/platform_skills_completion_report.md](archive/platform_skills_completion_report.md).

## Extension points

- Add a category with `skills/<category>/CATEGORY.md`; add skills beneath that category.
- Add a skill with `SKILL.md`, `agents/openai.yaml`, and the category-required paths.
- Add an agent with one authored file under [agents/](../agents/) and one matching catalog record.
- Add a platform with `install_targets/<platform>/TARGET.md`. Add projection behavior under
  [index_lib/](../index_lib/) and installation behavior under [install_lib/](../install_lib/).
- Add permanent unit behavior under [tests/](../tests/) and whole-CLI behavior under
  [tests/e2e/](../tests/e2e/).
- Add indexing, metadata, and generated-projection behavior under [index_lib/](../index_lib/); add
  standalone domain utilities under [tools/](../tools/) and maintainer-only release or repair
  commands under [devel/](../devel/).

## Known gaps

- Run optional live-client smoke checks when Cursor or OpenCode changes its published contract or
  is considered for promotion beyond compatibility support.
