# vosslab-skills

Reusable workflow skills that guide Claude and Codex through code review, plan drafting, doc maintenance, and education content production. Aimed at maintainers curating skill definitions and users who reuse them across coding environments.

## Documentation

- [docs/INSTALL.md](docs/INSTALL.md): Plugin install, local clone setup, and individual skill import.
- [docs/USAGE.md](docs/USAGE.md): Invoking skills, browsing the index, and maintaining the plugin manifest.
- [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md): Common issues and quick checks.
- [docs/SKILLS_INDEX.md](docs/SKILLS_INDEX.md): Generated skill-by-skill index with one-line descriptions.
- [docs/CODE_ARCHITECTURE.md](docs/CODE_ARCHITECTURE.md): System layout, major components, and extension points.
- [docs/FILE_STRUCTURE.md](docs/FILE_STRUCTURE.md): Directory map and where to add new work.
- [docs/CHANGELOG.md](docs/CHANGELOG.md): Dated record of documentation and skill updates.
- [docs/REPO_STYLE.md](docs/REPO_STYLE.md): Repository organization and documentation conventions.
- [docs/EXPERT_SKILL-BEST_PRACTICES.md](docs/EXPERT_SKILL-BEST_PRACTICES.md): Conventions for authoring domain-expert skills and the local-only reference-survey pattern.
- [docs/PYTHON_STYLE.md](docs/PYTHON_STYLE.md): Python coding standards used by this repository.
- [docs/MARKDOWN_STYLE.md](docs/MARKDOWN_STYLE.md): Markdown formatting and writing rules.

## Quick start

Add the Voss Lab skills marketplace:

```bash
claude plugin marketplace add vosslab/vosslab-skills
```

Install the plugin:

```bash
claude plugin install vosslab-skills@vosslab-skills
```

Or, inside an interactive Claude Code session:

```
/plugin marketplace add vosslab/vosslab-skills
/plugin install vosslab-skills@vosslab-skills
```

Verify the marketplace is registered:

```bash
claude plugin marketplace list
```

Then invoke any skill by name in a Claude Code session:

```
/vosslab-skills:readme-docs
/vosslab-skills:blueprint-plan-drafter
/vosslab-skills:audit-code-reviewer
```

See [docs/INSTALL.md](docs/INSTALL.md) for local clone and individual skill import options.

## Skills included

- `agents-md-fixer`: Trim AGENTS.md to a small pointer file linking into docs/*.md.
- `arch-docs`: Create or refresh CODE_ARCHITECTURE.md and FILE_STRUCTURE.md.
- `audit-code-reviewer`: Parallel multi-reviewer audit before merge or release.
- `blueprint-plan-drafter`: Create forward-looking implementation plans from scratch.
- `bptools-writer`: Create and validate biology-problems bptools Python question generators.
- `delegate-manager-to-subagents`: Manage execution of an approved plan through subagents.
- `docset-updater`: Audit and refresh the full repo doc set against REPO_STYLE.md.
- `gas-town-workflow`: Gas Town style multi-agent coordination with role-mapped task routing.
- `geometry-expert`: Design, implement, debug, and review computational geometry algorithms in any language.
- `html-game-parallel-builder`: Build a TypeScript browser game using parallel subagents.
- `old-python-code-review` (deprecated): Single-pass Python correctness/security/style review; kept frozen, excluded from the published plugin.
- `parallel-plan`: Split current work into independent tracks for parallel dispatch.
- `pdf-guide`: Read, create, or review PDF files where rendering and layout matter.
- `pyside6-engineer`: Design, implement, and review PySide6 desktop applications.
- `readme-docs`: Standardize README.md to match repo conventions.
- `repo-rules-reader`: Read repo rule files and answer targeted repo-rule questions.
- `skill-writing-guide`: Guide for authoring Agent Skills (SKILL.md) in open standard format.
- `solid-js-expert`: Build and debug full-stack SolidJS, Solid Router, SolidStart, and Solid Meta code.
- `stay-busy`: Generate parallel workstreams when a delegate-manager-to-subagents workflow would idle.
- `typescript-engineer`: Resolve TypeScript errors and design strict TypeScript types.
- `ui-ux-engineer`: Review and improve UI/UX quality in any framework.
- `unit-test-starter`: Generate thorough Python 3 pytest unit tests across a repo.
- `vision-expert`: Design, implement, and review computer vision systems in Python.
- `setup-install-usage-docs`: Create or refresh docs/INSTALL.md and docs/USAGE.md stubs.
- `webwork-writer`: Create and lint WeBWorK PG/PGML questions.

Full index with links: [docs/SKILLS_INDEX.md](docs/SKILLS_INDEX.md).

## Related repositories and standards

If you are building, organizing, or distributing agent skills, start with these references:

- [Agent Skills standard (agentskills.io)](https://agentskills.io/home): Overview of the open `SKILL.md` format and why skills improve agent reliability.
- [Anthropic Skills](https://github.com/anthropics/skills): Official Claude skills repo with examples of repeatable task instructions and resources.
- [Superpowers (obra)](https://github.com/obra/superpowers): A composable skills-based workflow for coding agents.
