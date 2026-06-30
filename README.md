# vosslab-skills

Reusable workflow skills that guide Claude and Codex through code review, plan drafting, doc maintenance, and education content production. Aimed at maintainers curating skill definitions and users who reuse them across coding environments.

## Documentation

Getting started:

- [docs/INSTALL.md](docs/INSTALL.md): Plugin install, local clone setup, and individual skill import.
- [docs/USAGE.md](docs/USAGE.md): Invoking skills, browsing the index, and maintaining the plugin manifest.
- [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md): Common issues and quick checks.
- [docs/SKILLS_INDEX.md](docs/SKILLS_INDEX.md): Generated skill-by-skill index with one-line descriptions.

Repository internals:

- [docs/CODE_ARCHITECTURE.md](docs/CODE_ARCHITECTURE.md): System layout, major components, and extension points.
- [docs/FILE_STRUCTURE.md](docs/FILE_STRUCTURE.md): Directory map and where to add new work.
- [docs/EXPERT_SKILL-BEST_PRACTICES.md](docs/EXPERT_SKILL-BEST_PRACTICES.md): Conventions for authoring domain-expert skills.

Conventions and standards:

- [docs/REPO_STYLE.md](docs/REPO_STYLE.md): Repository organization and documentation conventions.
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

Then invoke any skill by name in a Claude Code session:

```
/vosslab-skills:readme-docs
/vosslab-skills:blueprint-plan-drafter
/vosslab-skills:audit-code-reviewer
```

See [docs/INSTALL.md](docs/INSTALL.md) for local clone and individual skill import options.

## Skills included

A few representative skills from the collection:

- `audit-code-reviewer`: Parallel multi-reviewer audit before merge or release.
- `blueprint-plan-drafter`: Create forward-looking implementation plans from scratch.
- `delegate-manager-to-subagents`: Manage execution of an approved plan through subagents.
- `docset-updater`: Audit and refresh the full repo doc set against REPO_STYLE.md.
- `readme-docs`: Standardize README.md to match repo conventions.
- `related-projects-docs`: Build a sourced, confidence-tiered docs/RELATED_PROJECTS.md.
- `news-release-docs`: Author docs/RELEASE_HISTORY.md and docs/NEWS.md from the changelog.
- `skill-writing-guide`: Guide for authoring Agent Skills (SKILL.md) in open standard format.

Domain-expert skills cover computational geometry, computer vision, PySide6, SolidJS,
TypeScript, PDF work, and education-content generators (bptools and WeBWorK).

Full index with one-line descriptions: [docs/SKILLS_INDEX.md](docs/SKILLS_INDEX.md).

## Related repositories and standards

If you are building, organizing, or distributing agent skills, start with these references:

- [Agent Skills standard (agentskills.io)](https://agentskills.io/home): Overview of the open `SKILL.md` format and why skills improve agent reliability.
- [Anthropic Skills](https://github.com/anthropics/skills): Official Claude skills repo with examples of repeatable task instructions and resources.
