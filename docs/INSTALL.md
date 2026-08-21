# Install

This repository links skill trees and installs generated agent projections through a guided local
interview. Claude and Codex are primary targets. Cursor and OpenCode are maintained compatibility
targets with structural validation.

## Requirements

- Python 3.12 for repository tools and tests.
- Python packages from `pip_requirements-dev.txt` for development and validation.
- A writable home directory or isolated test root for the selected platform destinations.

## Platform support

| Platform | Tier | Skills destination | Agents destination | Reference |
| --- | --- | --- | --- | --- |
| Claude | primary | `.claude/skills` | `.claude/agents` | [Claude skills](https://docs.anthropic.com/en/docs/claude-code/skills) |
| Codex | primary | `.codex/skills` | `.codex/agents` | [Codex skills](https://developers.openai.com/codex/skills) |
| Cursor | compatibility | `.cursor/skills` | `.cursor/agents` | [Cursor skills](https://cursor.com/docs/context/skills) |
| OpenCode | compatibility | `.config/opencode/skills` | `.config/opencode/agents` | [OpenCode skills](https://opencode.ai/docs/skills) |

Codex receives one live category link at `.codex/skills/<category>`. Claude remains flat with one
link at `.claude/skills/<skill>`; Cursor and OpenCode also keep their declared platform-specific
skill roots. Claude agents are linked, while Codex, Cursor, and OpenCode agents are generated in
their native formats. Compatibility adapters receive focused structural checks, while Claude and
Codex provide the release-gated primary integration.

The shared `.agents/skills` convention is a compatibility source recognized by multiple clients;
it is not assigned to Cursor or OpenCode. This explicit-platform installer instead uses
`.codex/skills`, `.cursor/skills`, and `.config/opencode/skills` for those selected platforms.

## Run the interview

Run the main script from a local clone:

```bash
./install_skills.py
```

The interview asks for:

1. Target home directory. The displayed default is the current user's home.
2. Platforms as comma-separated names. The default is `claude,codex`; enter `cursor`, `opencode`,
   or another explicit combination when needed.
3. Final approval after the installer displays destinations and item counts.

Press Enter at the final `[y/N]` prompt to stop without writing. The installer never treats an
empty answer as approval.

Codex category destinations are absolute symlinks to canonical category directories in this clone.
Claude, Cursor, and OpenCode skill destinations link canonical skill directories. Claude agent
files link to the authored files under `agents/`. Codex, Cursor, and OpenCode need different native
agent schemas, so those small projections are generated as regular files. Moving or deleting the
clone breaks the source links; run the installer from the clone that should remain authoritative.

## Update an installation

Source edits appear through the links immediately. New Codex skills inside an already linked
category also appear immediately. Run the same interview again with the same home and platform
selection after adding a flat-platform skill, changing target declarations, authored agents, or
`agents/CATALOG.yaml`. The Git repository is authoritative: matching entries remain untouched and
mismatched entries are replaced.

The installer writes no receipt, manifest, cache, dotfile, or hidden configuration. Its persistent
writes stay inside the selected platforms' declared `skills/` and `agents/` destinations. Without
hidden ownership state, it does not prune stale entries; remove an obsolete skill or agent link
manually when its source is removed from the repository.

## Verify installation

Check generated artifacts and run the temporary-home interview lifecycle:

```bash
source source_me.sh && python3 tools/build_skills_index.py --check
source source_me.sh && python3 tools/build_plugin_manifest.py --check
source source_me.sh && python3 tools/openai_sidecars.py --check
source source_me.sh && python3 tools/build_agents_index.py --check
source source_me.sh && python3 tests/e2e/e2e_primary_adapter_contract.py
```

Every skill's `agents/openai.yaml` supplies a non-empty display name, a 25-64 character short
description, and a default prompt containing that skill's `$name`. The sidecar check also confirms
the category-specific required paths declared in `CATEGORY.md`.

## Known gaps

- [ ] Run optional live-client smoke checks when a platform release changes its published contract.
