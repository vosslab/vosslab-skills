# vosslab-skills

Reusable skills and agent roles for coding, documentation, code review, and
education-content production. Canonical repository data produces first-class Claude and Codex
installations, with maintained Cursor and OpenCode compatibility outputs.

## Quick start

Clone the repository, then run the guided installer from the repository root. It installs beneath
the current operating-system home and asks only which platforms to install; Claude and Codex are
the default selection.

```bash
./install_skills.py
```

The interview shows the destinations before asking for confirmation. Choose Cursor or OpenCode
when their compatibility adapters are useful. See
[docs/INSTALL.md](docs/INSTALL.md) for destinations and update behavior.

Skills are linked directly from each platform destination back to this clone, so the installer does
not duplicate skill trees and source edits are immediately visible. Codex preserves the repository
categories at `~/.codex/skills/<category>`; Claude remains flat at
`~/.claude/skills/<skill>`. Authored Claude agents use the same link model. Native Codex, Cursor,
and OpenCode agent projections are the only generated files.

## Canonical model

- `skills/<category>/<name>/SKILL.md` contains each skill's authored instructions.
  `CATEGORY.md` provides the category title, description, order, visibility, and required paths.
  Every skill also carries `agents/openai.yaml` with display metadata and a default prompt.
- `agents/<name>.md` contains the authored Claude-compatible agent instruction body.
  [agents/CATALOG.yaml](agents/CATALOG.yaml) supplies each agent's identity, responsibility,
  Gas Town role, access level, authority, and escalation metadata.
- `install_targets/<platform>/TARGET.md` declares an adapter, support tier, and destinations.
  Claude and Codex are `primary`; Cursor and OpenCode are `compatibility`.
- [install_skills.py](install_skills.py) and [install_lib/](install_lib/) create
  reproducible local installations without installer state or hidden configuration.

## Maintainer checks

Generate or check published artifacts from their canonical sources:

```bash
source source_me.sh && python3 tools/build_skills_index.py --check
source source_me.sh && python3 tools/build_plugin_manifest.py --check
source source_me.sh && python3 tools/openai_sidecars.py --check
source source_me.sh && python3 tools/build_agents_index.py --check
```

The index and manifests come from skills and category metadata. The searchable agent index comes
from the agent catalog plus authored Markdown, while installation renders agent adapters directly
from those canonical sources. See
[docs/USAGE.md](docs/USAGE.md) for maintenance commands and
[docs/CODE_ARCHITECTURE.md](docs/CODE_ARCHITECTURE.md) for extension points.

## Documentation

- [docs/INSTALL.md](docs/INSTALL.md): Platform tiers, destinations, and installer lifecycle.
- [docs/USAGE.md](docs/USAGE.md): Canonical sources, generated outputs, and verification.
- [docs/SKILLS_INDEX.md](docs/SKILLS_INDEX.md): Generated skill catalog.
- [docs/AGENTS_INDEX.md](docs/AGENTS_INDEX.md): Generated agent roles and authority index.
- [docs/CODE_ARCHITECTURE.md](docs/CODE_ARCHITECTURE.md): Components, data flow, and extension
  points.
- [docs/FILE_STRUCTURE.md](docs/FILE_STRUCTURE.md): Directory map and generated-output owners.
- [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md): Common checks and recovery guidance.

## Skills included

Representative workflow skills include `audit-code-reviewer`, `blueprint-plan-drafter`,
`delegate-manager-to-subagents`, `docset-updater`, `readme-docs`, and `repo-rules-reader`.
Domain-expert skills cover computational geometry, Apple Liquid Glass, computer vision, CSS,
Podman, PySide6, SolidJS, TypeScript, PDF work, and education-content generators. Browse the
complete generated catalog in [docs/SKILLS_INDEX.md](docs/SKILLS_INDEX.md).

## Related standards

- [Agent Skills standard](https://agentskills.io/home): Overview of the open `SKILL.md` format.
- [Anthropic Skills](https://github.com/anthropics/skills): Claude skill examples and resources.
