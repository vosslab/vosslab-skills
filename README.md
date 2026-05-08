# vosslab-skills

Reusable workflow skills for refactoring plans, code review, repository maintenance, and education content production. Intended for maintainers who curate skill definitions and for users who inspect or reuse `SKILL.md` instructions across Claude and Codex environments.

## Documentation

- [docs/INSTALL.md](docs/INSTALL.md): Plugin install, local clone setup, and individual skill import.
- [docs/USAGE.md](docs/USAGE.md): Invoking skills, browsing the index, and maintaining the plugin manifest.
- [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md): Common issues and quick checks.
- [docs/SKILLS_INDEX.md](docs/SKILLS_INDEX.md): Generated skill-by-skill index with one-line descriptions.
- [docs/CODE_ARCHITECTURE.md](docs/CODE_ARCHITECTURE.md): System layout, major components, and extension points.
- [docs/FILE_STRUCTURE.md](docs/FILE_STRUCTURE.md): Directory map and where to add new work.
- [docs/CHANGELOG.md](docs/CHANGELOG.md): Dated record of documentation and skill updates.
- [docs/REPO_STYLE.md](docs/REPO_STYLE.md): Repository organization and documentation conventions.
- [docs/PYTHON_STYLE.md](docs/PYTHON_STYLE.md): Python coding standards used by this repository.
- [docs/MARKDOWN_STYLE.md](docs/MARKDOWN_STYLE.md): Markdown formatting and writing rules.

## Quick start

Install as a Claude Code plugin:

```bash
claude plugin add https://github.com/vosslab/vosslab-skills
```

Then invoke any skill by name in a Claude Code session:

```
/vosslab-skills:old-python-code-review
/vosslab-skills:readme-docs
/vosslab-skills:blueprint-plan-drafter
```

See [docs/INSTALL.md](docs/INSTALL.md) for local clone and individual skill import options.

## Skills summary

- Skills cover planning and execution workflows for software tasks.
- Skills cover quality and maintenance workflows such as review, linting, and documentation updates.
- Skills cover education-focused production workflows.
- Full generated skill index: [docs/SKILLS_INDEX.md](docs/SKILLS_INDEX.md).

## Related repositories and standards

If you are building, organizing, or distributing agent skills, start with these references:

- [Agent Skills standard (agentskills.io)](https://agentskills.io/home): Overview of the open `SKILL.md` format and why skills improve agent reliability.
- [Anthropic Skills](https://github.com/anthropics/skills): Official Claude skills repo with examples of repeatable task instructions and resources.
- [Superpowers (obra)](https://github.com/obra/superpowers): A composable skills-based workflow for coding agents.
