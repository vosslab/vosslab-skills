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

Convert a technical or scientific book to agent-ready Markdown with the
`book-to-markdown` skill. It selects a source-aware conversion tool and supports
a measured PDF sample before a whole-book conversion:

```bash
source source_me.sh && python3 skills/book-to-markdown/scripts/pdf_to_markdown.py \
  paper.pdf --pages 0,1,25-30 --measure --json-report /tmp/paper.measure.json
source source_me.sh && python3 skills/book-to-markdown/scripts/pdf_to_markdown.py \
  paper.pdf -o /tmp/paper.raw.md
source source_me.sh && python3 skills/book-to-markdown/scripts/clean_markdown.py \
  -i /tmp/paper.raw.md -o /tmp/paper.clean.md
```

For EPUB, HTML, DOCX, or ODT, use Pandoc first; existing Markdown or text can
go directly to the cleaner:

```bash
pandoc book.epub --from epub --to gfm --wrap=none -o /tmp/book.raw.md
source source_me.sh && python3 skills/book-to-markdown/scripts/clean_markdown.py \
  -i /tmp/book.raw.md -o /tmp/book.clean.md
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
