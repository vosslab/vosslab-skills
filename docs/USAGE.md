# Usage

This repository is a collection of Claude Code skills under `skills/`, plus
maintenance tools under `tools/` and a test suite under `tests/`. Skills are
invoked inside a Claude Code session; the tools and tests are run locally with
`source source_me.sh && python3`.

## Invoke a skill

Once the plugin is installed (see [INSTALL.md](INSTALL.md)), invoke any skill by
name in a Claude Code session:

```
/vosslab-skills:readme-docs
/vosslab-skills:blueprint-plan-drafter
/vosslab-skills:audit-code-reviewer
```

Each skill lives in `skills/<name>/SKILL.md`, the entry point Claude loads.
Browse the generated one-line index in [SKILLS_INDEX.md](SKILLS_INDEX.md).

## Maintenance tools

All tools run from the repo root. Use the bootstrap pattern so the right Python
environment is active:

```bash
source source_me.sh && python3 tools/<script>.py
```

| Tool | Purpose | Notable flags |
| --- | --- | --- |
| `tools/build_skills_index.py` | Regenerate `docs/SKILLS_INDEX.md` from `skills/**/SKILL.md` | `--check` exits nonzero if the index is stale |
| `tools/build_plugin_manifest.py` | Regenerate the platform plugin manifests (Claude, Codex, Cursor, OpenCode) | `-c` / `--check` exits nonzero if manifests are stale |
| `tools/list_loaded_skills.py` | List loaded skills across repo, personal, plugin cache, and harness | `-n` / `--names-only`, `-c NAME` / `--check NAME`, `-x` / `--collisions` |
| `tools/pdftomd.py` | Convert a PDF to text-first Markdown | `-o` output, `-p` pages, `--ocr` / `--no-ocr` |

Generated files (`docs/SKILLS_INDEX.md`, the `.claude-plugin/` manifests, and
sibling platform manifests) are produced by these tools. Edit the source
`SKILL.md` files, then regenerate; do not hand-edit the output.

## Examples

Regenerate the skills index after adding or editing a skill:

```bash
source source_me.sh && python3 tools/build_skills_index.py
```

Check whether the index and manifests are up to date without writing files:

```bash
source source_me.sh && python3 tools/build_skills_index.py --check
source source_me.sh && python3 tools/build_plugin_manifest.py --check
```

Convert a PDF to Markdown, writing `paper.md` next to the input:

```bash
source source_me.sh && python3 tools/pdftomd.py paper.pdf
```

## Run the tests

The fast pytest suite lives under `tests/` and enforces repo conventions
(ASCII compliance, typing, import rules, skill frontmatter, manifest drift):

```bash
pytest tests/
```

Run a single test file, optionally narrowed with `-k`:

```bash
pytest tests/test_skills_index_in_sync.py
```

## Inputs and outputs

- Inputs: `skills/**/SKILL.md` skill definitions, `agents/` agent definitions,
  and `VERSION`.
- Outputs: `docs/SKILLS_INDEX.md` and the per-platform plugin manifests under
  `.claude-plugin/` (and sibling platform manifest directories).

## Known gaps

- [ ] Confirm the exact set of platform manifest output paths emitted by
  `tools/build_plugin_manifest.py` against the directories tracked in git.
- [ ] Confirm `tools/pdftomd.py` runtime dependency: it imports `fitz`
  (listed in `pip_extras.txt`) and may require an OCR backend for `--ocr`.
