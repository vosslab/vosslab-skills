# vosslab-skills

Reusable workflow skills for refactoring plans, code review, repository maintenance, and education content production. Intended for maintainers who curate skill definitions and for users who inspect or reuse `SKILL.md` instructions across Claude and Codex environments.

## Skills summary

- Skills cover planning and execution workflows for software tasks.
- Skills cover quality and maintenance workflows such as review, linting, and documentation updates.
- Skills cover education-focused production workflows.
- Full generated skill index: [docs/SKILLS_INDEX.md](docs/SKILLS_INDEX.md).

## Related repositories and standards

If you are building, organizing, or distributing agent skills, these projects are worth a look.

- [Claude Scientific Skills (K-Dense)](https://github.com/K-Dense-AI/claude-scientific-skills): 140+ ready-to-use scientific and research skills using the Agent Skills standard.
- [Codex Skills Library (proflead)](https://github.com/proflead/codex-skills-library): Curated, reusable Codex skills for common developer workflows, designed for consistent results.
- [Anthropic Skills](https://github.com/anthropics/skills): Official Claude skills repo with examples of repeatable task instructions and resources.
- [Agent Skills standard (agentskills.io)](https://agentskills.io/home): Overview of the open `SKILL.md` format and why skills improve agent reliability.
- [Agent Skills Marketplace (skills.marketplace)](https://skillsmp.com/): Large directory for discovering open-source skills built on the `SKILL.md` ecosystem.
- [Superpowers (obra)](https://github.com/obra/superpowers): A composable skills-based workflow for coding agents, focused on spec-first and disciplined implementation.
- [Everything Claude Code (affaan-m)](https://github.com/affaan-m/everything-claude-code): A large, production-oriented collection of Claude Code configs, including many skill packs.
- [Awesome Claude Skills (ComposioHQ)](https://github.com/ComposioHQ/awesome-claude-skills): A curated list of practical Claude skills and related tooling.
- [UI/UX Pro Max Skill (nextlevelbuilder)](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill): An agent skill focused on UI/UX design intelligence and automated design system generation across platforms.

## Documentation

- [docs/INSTALL.md](docs/INSTALL.md): Local prerequisites and setup notes.
- [docs/USAGE.md](docs/USAGE.md): Primary workflow for browsing and using skills in this repository.
- [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md): Common issues and quick checks.
- [docs/SKILLS_INDEX.md](docs/SKILLS_INDEX.md): Generated skill-by-skill index with one-line descriptions.
- [docs/CHANGELOG.md](docs/CHANGELOG.md): Dated record of documentation and skill updates.
- [docs/REPO_STYLE.md](docs/REPO_STYLE.md): Repository organization and documentation conventions.
- [docs/PYTHON_STYLE.md](docs/PYTHON_STYLE.md): Python coding standards used by this repository.
- [docs/MARKDOWN_STYLE.md](docs/MARKDOWN_STYLE.md): Markdown formatting and writing rules.
- [docs/AUTHORS.md](docs/AUTHORS.md): Maintainer and contributor reference.

## Quick start

```bash
cd /Users/vosslab/nsh/vosslab-skills
source source_me.sh && python3 tools/build_skills_index.py
cat docs/SKILLS_INDEX.md
```

The commands above regenerate and inspect the skills index for this repository.
