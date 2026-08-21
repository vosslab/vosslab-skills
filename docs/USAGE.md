# Usage

Use this repository to maintain canonical `SKILL.md` sources, authored Claude-compatible agent
instructions, searchable indexes, and local installations.

## Quick start

Run the guided installer from the repository root:

```bash
./install_skills.py
```

The interview defaults to Claude and Codex, shows each destination, and writes only after final
approval. Enter Cursor or OpenCode by name when their compatibility adapters are needed. Skill
sources and authored Claude agents are linked rather than copied; re-run the same interview after
changing target declarations, authored agents, or `agents/CATALOG.yaml`.

Codex links repository categories at `~/.codex/skills/<category>`. Claude keeps individual skill
links flat at `~/.claude/skills/<skill>`. Cursor uses `~/.cursor/skills`, and OpenCode uses
`~/.config/opencode/skills`; `.agents/skills` remains an unused shared compatibility location.

## Platform outputs

| Source | Generated projection | Installation adapters |
| --- | --- | --- |
| `skills/<category>/<name>/SKILL.md` | `docs/SKILLS_INDEX.md` and platform manifests | `claude_markdown`, `codex_toml`, `cursor_markdown`, `opencode_markdown` |
| `agents/<name>.md` | Target-specific agent file at install time | Claude Markdown, Codex TOML, Cursor Markdown, OpenCode Markdown |
| `agents/CATALOG.yaml` | `docs/AGENTS_INDEX.md` | Catalog identity, role, and access data |

Claude and Codex are primary outputs. Cursor and OpenCode are compatibility outputs with linked
skills, generated native agent files, and focused adapter checks. This compatibility tier supplies
structural evidence while the primary tier supplies the release-gated integration evidence.

## Regenerate outputs

Edit canonical skill, category, sidecar, catalog, or authored agent source data, then run the
matching generator or validator. The check forms report drift without writing files.

```bash
source source_me.sh && python3 tools/build_skills_index.py
source source_me.sh && python3 tools/build_plugin_manifest.py
source source_me.sh && python3 tools/build_agents_index.py

source source_me.sh && python3 tools/build_skills_index.py --check
source source_me.sh && python3 tools/build_plugin_manifest.py --check
source source_me.sh && python3 tools/openai_sidecars.py --check
source source_me.sh && python3 tools/build_agents_index.py --check
```

The manifest builder produces Claude, Codex, Cursor, and OpenCode manifest artifacts. The agent
index builder produces [AGENTS_INDEX.md](AGENTS_INDEX.md) from
[agents/CATALOG.yaml](../agents/CATALOG.yaml) and authored Markdown. The installer renders each
target-specific agent file directly from those canonical sources.
`tools/openai_sidecars.py --check` validates every tracked skill's `agents/openai.yaml`: a non-empty
display name, a 25-64 character short description, and a default prompt containing the skill's
`$name`. It also verifies category-specific required paths from `CATEGORY.md`.

## Installer lifecycle

[install_skills.py](../install_skills.py) is the human-facing entry point.
[install_lib/interview.py](../install_lib/interview.py) owns questions and confirmations, while
[install_lib/installer.py](../install_lib/installer.py) owns side-effect-free planning, links, and
generated native agent files.

The installer creates no state directory or hidden configuration. It writes only the selected
platforms' installed skills and agents. The Git repository is authoritative: existing matching
entries are left alone and mismatches are replaced after final confirmation. There are no plan,
apply, update, or status modes.

## Verification

Run the fast metadata, projection, installer, and Markdown-link checks:

```bash
source source_me.sh && python3 -m pytest \
  tests/test_skills_index_in_sync.py \
  tests/test_agent_adapters.py \
  tests/test_skill_installer.py \
  tests/test_install_target_data.py \
  tests/test_openai_sidecars.py \
  tests/test_markdown_links.py
source source_me.sh && python3 tests/e2e/e2e_primary_adapter_contract.py
```

## Known gaps

- [ ] Record optional live-client smoke observations with the relevant platform release.
