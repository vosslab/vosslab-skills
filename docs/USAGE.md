# Usage

Use this repository to maintain canonical `SKILL.md` sources, authored Claude-compatible agent
instructions, searchable indexes, and local installations.

## Quick start

Run the guided installer from the repository root:

```bash
./install_skills.py
```

The installer uses the current operating-system home automatically. The interview defaults to
Claude and Codex, shows each destination, and writes only after final approval. Enter Cursor,
OpenCode, Grok, or Hermes by name when their compatibility adapters are needed. Skill sources and
authored Claude agents are linked rather than copied; re-run the same interview after changing
target declarations, authored agents, or `agents/CATALOG.yaml`. Each run also unlinks stale
symlinks beneath the selected destinations that point into this clone but no longer match a skill
or agent, so renamed skills leave no dangling links.

Codex and Hermes link repository categories at `~/.codex/skills/<category>` and
`~/.hermes/skills/<category>`. Claude keeps individual skill links flat at
`~/.claude/skills/<skill>`, as do Cursor (`~/.cursor/skills`), OpenCode
(`~/.config/opencode/skills`), and Grok (`~/.grok/skills`); `.agents/skills` remains an unused
shared compatibility location. Hermes installs skills only; it has no agent files.

## Platform outputs

| Source | Generated projection | Installation adapters |
| --- | --- | --- |
| `skills/<category>/<name>/SKILL.md` | `docs/SKILLS_INDEX.md` and platform manifests | `claude_markdown`, `codex_toml`, `cursor_markdown`, `opencode_markdown`, `skills_only` |
| `agents/<name>.md` | Target-specific agent file at install time | Claude Markdown (also Grok), Codex TOML, Cursor Markdown, OpenCode Markdown |
| `agents/CATALOG.yaml` | `docs/AGENTS_INDEX.md` | Catalog identity, role, and access data |

Claude and Codex are primary outputs. Cursor, OpenCode, Grok, and Hermes are compatibility outputs
with linked skills, linked or generated agent files where the platform has them, and focused
adapter checks. This compatibility tier supplies
structural evidence while the primary tier supplies the release-gated integration evidence.

## Regenerate outputs

Edit canonical skill, category, sidecar, catalog, or authored agent source data, then run the
merged indexing command. Its check form reports sidecar or generated-output drift without writing.

```bash
source source_me.sh && python3 index_lib/build_all.py
source source_me.sh && python3 index_lib/build_all.py --check
```

The merged launcher validates OpenAI sidecars, produces Claude, Codex, Cursor, and OpenCode
manifest artifacts, writes [SKILLS_INDEX.md](SKILLS_INDEX.md), and builds
[AGENTS_INDEX.md](AGENTS_INDEX.md) from
[agents/CATALOG.yaml](../agents/CATALOG.yaml) and authored Markdown. The installer renders each
target-specific agent file directly from those canonical sources.
The focused commands under [index_lib/](../index_lib/) remain available when maintaining one
projection. `index_lib/openai_sidecars.py --check` validates every tracked skill's
`agents/openai.yaml`: a non-empty display name, a 25-64 character short description, a default
prompt containing the skill's `$name`, and category-specific required paths from `CATEGORY.md`.

## Installer lifecycle

[install_skills.py](../install_skills.py) is the human-facing entry point.
[install_lib/interview.py](../install_lib/interview.py) owns questions and confirmations, while
[install_lib/installer.py](../install_lib/installer.py) owns side-effect-free planning, links, and
generated native agent files.

The installer creates no state directory or hidden configuration. It writes only the selected
platforms' installed skills and agents. The Git repository is authoritative: existing matching
entries are left alone and mismatches are replaced after final confirmation. There are no plan,
apply, update, or status modes, and no command-line flags for alternate installation roots.

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
