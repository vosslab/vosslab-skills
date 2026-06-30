# Related projects

Sibling repositories and external targets that this skills collection
references or coordinates with. Details below reflect references found in
this repo's docs and skill definitions.

## Shared tooling and conventions

- `starter-repo-template`: source of the style guides, propagation system, and
  TypeScript scaffold reused here. The `html-game-parallel-builder` skill layers
  on `starter-repo-template/templates/typescript/`, and several `docs/` style
  files are mirrors propagated from this template.
- `claude-code-permissions-hook`: source of truth for
  [CLAUDE_HOOK_USAGE_GUIDE.md](CLAUDE_HOOK_USAGE_GUIDE.md). The copy in this repo
  is a mirror; edit upstream, not the local copy.

## Skill target repositories

- `biology-problems`: target repo for the `bptools-writer-expert` skill. That
  skill authors `bptools.py`-based question generators and depends on
  `qti_package_maker` for BBQ/QTI output. Bundled docs under the skill's
  `references/` are snapshots from `biology-problems`.
- `qti_package_maker`: assessment-package writer used by `biology-problems`
  generators; referenced by the `bptools-writer-expert` skill for output format
  logic.

## Known gaps

- No machine-readable manifest of sibling repos exists yet; entries above are
  drawn from prose references.
- Repository URLs are intentionally omitted until a canonical source lists them.
- The `webwork-writer-expert` skill targets a WebWork PG/PGML repo that is not
  named in repo evidence; add it here once identified.
