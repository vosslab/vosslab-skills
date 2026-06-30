# Install

This repository is a Claude Code plugin that provides reusable workflow skills. "Installed" means Claude Code can discover and invoke the skills in this repo. There are three installation methods depending on your setup.

## Requirements

- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) installed and working
- Git (for clone-based methods)
- Python 3.12 to run the local tools under `tools/` and the test suite (see
  [USAGE.md](USAGE.md))
- Developer Python packages from `pip_requirements-dev.txt` for running tools and
  tests (for example `pytest`, `rich`, `tabulate`)

## Method 1: install from the marketplace

Add the marketplace, then install the plugin:

```bash
claude plugin marketplace add vosslab/vosslab-skills
claude plugin install vosslab-skills@vosslab-skills
```

Or, inside an interactive Claude Code session:

```
/plugin marketplace add vosslab/vosslab-skills
/plugin install vosslab-skills@vosslab-skills
```

Confirm the marketplace is registered:

```bash
claude plugin marketplace list
```

Validate the plugin manifest locally from the repo root (for development):

```bash
claude plugin validate .
```

After installing, skills are available as `/vosslab-skills:<skill-name>` in any Claude Code session.

## Method 2: clone and use as a local plugin directory

```bash
git clone https://github.com/vosslab/vosslab-skills.git
claude --plugin-dir /path/to/vosslab-skills
```

This loads the plugin from a local directory for a single session. To make it persistent, add the path to your Claude Code settings.

## Method 3: import individual skills

If you only want specific skills rather than the full set, copy the skill folder into your own project's `skills/` directory.

```bash
git clone https://github.com/vosslab/vosslab-skills.git /tmp/vosslab-skills
cp -r /tmp/vosslab-skills/skills/old-python-code-review ./skills/
cp -r /tmp/vosslab-skills/skills/readme-docs ./skills/
```

Each skill is self-contained in its `skills/<name>/` folder. The `SKILL.md` file is the entry point; some skills also include `references/` and `agents/` subdirectories.

## Verify install

After installing, confirm that skills are discoverable.

**Plugin install** -- run Claude Code and invoke a skill:

```bash
claude
# then type: /vosslab-skills:readme-docs
```

**Local clone** -- check the generated skills index:

```bash
source source_me.sh && python3 tools/build_skills_index.py
cat docs/SKILLS_INDEX.md
```

If the skills index lists the expected repository skills, the repo is set up correctly.

## Updating

For plugin installs, Claude Code handles updates automatically. For local clones:

```bash
git pull --ff-only
```

## Known gaps

- [ ] Verify whether `--plugin-dir` persists across sessions or requires a settings entry.
