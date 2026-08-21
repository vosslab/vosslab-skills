# Code architecture

## Overview

[vosslab-skills](../README.md) is a content-first skills repository with a guided Python
installer. Authored Markdown and YAML remain canonical; generators create small tracked indexes
and plugin manifests, while installation links source content into platform-owned directories.

Claude and Codex are primary targets. Cursor and OpenCode are compatibility targets with
structural adapter validation rather than a live-client guarantee.

## Major components

### Canonical content

| Component | Path | Responsibility |
| --- | --- | --- |
| Skill sources | [skills/](../skills/) | Category metadata, `SKILL.md`, OpenAI sidecars, references, scripts, and assets |
| Agent sources | [agents/](../agents/) | Authored agent Markdown plus canonical role and access data |
| Platform targets | [install_targets/](../install_targets/) | Adapter, support tier, and destination declarations |
| Version source | [VERSION](../VERSION) | Repository version normalized at manifest boundaries |

Each direct category under [skills/](../skills/) owns a `CATEGORY.md`. Each published skill owns
its `SKILL.md` and `agents/openai.yaml`. [agents/CATALOG.yaml](../agents/CATALOG.yaml) must match
the authored agent filenames and escalation routes.

### Installer runtime

[install_skills.py](../install_skills.py) is the human-facing entry point. It resolves the
repository root through Git and starts the interview in
[install_lib/interview.py](../install_lib/interview.py).

The root [install_lib/](../install_lib/) package separates reusable behavior:

- [install_lib/frontmatter.py](../install_lib/frontmatter.py) parses YAML metadata and converts
  repository CalVer to strict manifest SemVer.
- [install_lib/skill_discovery.py](../install_lib/skill_discovery.py) validates categories and
  produces tracked or filesystem-backed skill inventories.
- [install_lib/agent_catalog.py](../install_lib/agent_catalog.py) validates agent parity and
  renders Codex, Cursor, and OpenCode projections.
- [install_lib/install_target_data.py](../install_lib/install_target_data.py) validates target
  declarations, URLs, and contained destination paths.
- [install_lib/installer.py](../install_lib/installer.py) builds plans, preserves matching entries,
  and replaces stale skill links or agent files from the authoritative repository source.
- [install_lib/interview.py](../install_lib/interview.py) owns prompts, summaries, and final
  confirmation.

[source_me.sh](../source_me.sh) exposes this root package through `PYTHONPATH` after loading the
user shell environment. The runtime has no import dependency on [tools/](../tools/).

### Generators and validators

| Tool | Canonical input | Tracked output or result |
| --- | --- | --- |
| [tools/build_skills_index.py](../tools/build_skills_index.py) | Categories and skill frontmatter | [SKILLS_INDEX.md](SKILLS_INDEX.md) |
| [tools/build_agents_index.py](../tools/build_agents_index.py) | Agent catalog and authored Markdown | [AGENTS_INDEX.md](AGENTS_INDEX.md) |
| [tools/build_plugin_manifest.py](../tools/build_plugin_manifest.py) | Skill inventory and [VERSION](../VERSION) | Platform plugin manifests |
| [tools/openai_sidecars.py](../tools/openai_sidecars.py) | Skill sidecars and category requirements | Validation result only |

The generators support check-only validation where documented in [USAGE.md](USAGE.md). Generated
files are small and intentionally tracked.

## Data flow

### Guided installation

1. [install_skills.py](../install_skills.py) resolves the Git root and starts the interview.
2. The interview asks for a target home and platforms. Claude and Codex are the default selection.
3. Target metadata is loaded from [install_targets/](../install_targets/).
4. Skill discovery reads the tracked category and skill sources. Agent discovery validates
   [agents/CATALOG.yaml](../agents/CATALOG.yaml) against authored Markdown.
5. Codex links canonical category directories beneath `.codex/skills`; Claude, Cursor, and
   OpenCode link individual skills beneath their declared platform destinations. Authored Claude
   agents also become absolute symlinks to this clone.
6. Codex, Cursor, and OpenCode agent projections become regular files because no authored file
   exists in those native formats.
7. Final confirmation installs the repository version over mismatched destination entries.

Edits to linked source content are visible immediately. Re-running the interview refreshes
generated agent projections and changed links. Moving the clone requires another installer run so
links can point to the new location. The installer writes no receipt, version record, cache, or
hidden configuration and does not prune stale entries that are no longer in the repository.

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
- Add a platform with `install_targets/<platform>/TARGET.md`. Reuse an adapter or add rendering
  behavior under [install_lib/](../install_lib/).
- Add permanent unit behavior under [tests/](../tests/) and whole-CLI behavior under
  [tests/e2e/](../tests/e2e/).
- Add repository generators and validators under [tools/](../tools/); add maintainer-only release
  and repair commands under [devel/](../devel/).

## Known gaps

- Run optional live-client smoke checks when Cursor or OpenCode changes its published contract or
  is considered for promotion beyond compatibility support.
