# vosslab-skills

Reusable Codex skills for refactoring plans, code review, repository maintenance, and education content production. Intended for maintainers who curate skill definitions and for users who inspect or reuse `SKILL.md` instructions.

## Skills summary

- General engineering workflow skills: `readme-fix`, `read-repo-rules`, `docset-refresh`, `arch-docs`, `install-usage-docs`.
- Planning and execution skills: `manager-make-new-plan`, `manager-review-existing-plan`, `orchestrate-next-milestone`, `parallel-plan`, `parallel-web-game-build`.
- Domain or task-specific skills: `python-code-review`, `unit-test-starter`, `pyflakes-fix`, `ascii-lint-fix`, `pdf`, `bptools-writer`, `webwork-writer`.
- System skill tooling is under `skills/.system/` and includes `skill-creator` and `skill-installer`.
- Full generated skill index: [docs/SKILLS_INDEX.md](docs/SKILLS_INDEX.md).

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
