# Install

This repository links skill trees and installs generated agent projections through a guided local
interview. Claude and Codex are primary targets. Cursor, OpenCode, Grok, and Hermes are maintained
compatibility targets with structural validation.

## Requirements

- Python 3.12 for repository tools and tests.
- Python packages from `pip_requirements-dev.txt` for development and validation.
- A writable operating-system home directory for the selected platform destinations.

## Platform support

| Platform | Tier | Skills destination | Agents destination | Reference |
| --- | --- | --- | --- | --- |
| Claude | primary | `.claude/skills` | `.claude/agents` | [Claude skills](https://docs.anthropic.com/en/docs/claude-code/skills) |
| Codex | primary | `.codex/skills` | `.codex/agents` | [Codex skills](https://developers.openai.com/codex/skills) |
| Cursor | compatibility | `.cursor/skills` | `.cursor/agents` | [Cursor skills](https://cursor.com/docs/context/skills) |
| OpenCode | compatibility | `.config/opencode/skills` | `.config/opencode/agents` | [OpenCode skills](https://opencode.ai/docs/skills) |
| Grok | compatibility | `.grok/skills` | `.grok/agents` | [Grok CLI](https://github.com/xai-org/grok-cli) |
| Hermes | compatibility | `.hermes/skills` | none | [Hermes skills](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/) |

Each `TARGET.md` declares a `skill_layout`. Codex and Hermes use `category` and receive one live
link per category at `<skills root>/<category>`. Claude, Cursor, OpenCode, and Grok use `flat` and
receive one link per skill at `<skills root>/<skill>`. Claude and Grok agents are linked (Grok reads
Claude-format agents natively), while Codex, Cursor, and OpenCode agents are generated in their
native formats. Hermes has no user-defined agent files, so its `skills_only` adapter declares no
agents destination. Compatibility adapters receive focused structural checks, while Claude and
Codex provide the release-gated primary integration.

The shared `.agents/skills` convention is a compatibility source recognized by multiple clients;
it is not assigned to Cursor or OpenCode. This explicit-platform installer instead uses
`.codex/skills`, `.cursor/skills`, `.config/opencode/skills`, `.grok/skills`, and `.hermes/skills`
for those selected platforms. Grok also scans `~/.claude/skills` and `~/.claude/agents` on its own,
so a Claude installation already serves Grok; select `grok` when Claude is not installed.

## Run the interview

Run the main script from a local clone:

```bash
./install_skills.py
```

The interview asks for:

1. Platforms as comma-separated names. The default is `claude,codex`; enter `cursor`, `opencode`,
   `grok`, `hermes`, or another explicit combination when needed.
2. Final approval after the installer displays the operating-system home, destinations, and item
   counts.

The installer always uses the current operating-system home. It does not ask for an alternate
home and has no command-line option for one.

Press Enter at the final `[y/N]` prompt to stop without writing. The installer never treats an
empty answer as approval.

Codex and Hermes category destinations are absolute symlinks to canonical category directories in
this clone. Claude, Cursor, OpenCode, and Grok skill destinations link canonical skill directories.
Claude and Grok agent files link to the authored files under `agents/`. Codex, Cursor, and OpenCode
need different native agent schemas, so those small projections are generated as regular files.
Moving or deleting the clone breaks the source links; run the installer from the clone that should
remain authoritative.

## Update an installation

Source edits appear through the links immediately. New Codex skills inside an already linked
category also appear immediately. Run the same interview again with the same platform selection
after adding a flat-platform skill, changing target declarations, authored agents, or
`agents/CATALOG.yaml`. The Git repository is authoritative: matching entries remain untouched and
mismatched entries are replaced.

The installer writes no receipt, manifest, cache, dotfile, or hidden configuration. Its persistent
writes stay inside the selected platforms' declared `skills/` and `agents/` destinations.

### Stale links

Renaming or removing a skill leaves a dangling per-skill link on flat platforms such as Claude.
After installing a platform, the installer removes any symlink directly beneath that platform's
declared destinations whose target resolves inside this clone but no longer matches a current
skill or agent, and reports each as an `unlink` change. Ownership comes from the link target, so
links into other repositories, hand-made directories, and regular files are never touched.
Generated agent files (Codex TOML, Cursor and OpenCode Markdown) carry no ownership marker and are
not pruned; remove an obsolete generated agent file manually.

## Verify installation

Check generated artifacts and run the temporary-home interview lifecycle:

```bash
source source_me.sh && python3 index_lib/build_all.py --check
source source_me.sh && python3 tests/e2e/e2e_primary_adapter_contract.py
```

Every skill's `agents/openai.yaml` supplies a non-empty display name, a 25-64 character short
description, and a default prompt containing that skill's `$name`. The sidecar check also confirms
the category-specific required paths declared in `CATEGORY.md`.

## Known gaps

- [ ] Run optional live-client smoke checks when a platform release changes its published contract.
