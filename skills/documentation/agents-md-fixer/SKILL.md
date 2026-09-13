---
name: agents-md-fixer
description: "Trim bloated `AGENTS.md` files into concise pointers to canonical `docs/*.md` rules. Use when agent guidance duplicates repo documentation. This skill changes only `AGENTS.md`; use documentation skills for README or `docs/` changes."
---

# AGENTS.md fixer

## Goal

Make `AGENTS.md` a tiny pointer file. It should mostly be bare paths into
`docs/*.md`, not prose. This skill audits and tightly rewrites it using the
repository's load-bearing rules.

`AGENTS.md` is agent-facing. Reference docs by bare path
(`docs/PYTHON_STYLE.md`), not Markdown links.

Use the `docs/REPO_STYLE.md` `AGENTS.md files` policy for size and structure.

## Required content (keep)

Keep only items that are repo-specific and load-bearing:

- Bare path pointers to canonical style docs that exist in this repo, for example
  `docs/REPO_STYLE.md`,
  `docs/PYTHON_STYLE.md`,
  `docs/MARKDOWN_STYLE.md`,
  `docs/PYTEST_STYLE.md`, and
  `docs/CHANGELOG.md`.
- Repo-specific runtime quirks: interpreter bootstrap, env activation,
  container entry, non-default install paths.
- Non-obvious workflow constraints actually enforced in this repo (example:
  "humans run `git commit`", branch policy, hook behavior).
- Test invocation cheat-line specific to this repo.
- Any user-injected directive marked as overriding defaults (preserve it
  verbatim).

## Frivolous content (cut or move)

Flag and remove these patterns:

- Long philosophy or "why we believe X" paragraphs. Move the canonical
  version to `docs/REPO_STYLE.md`, or delete if already covered there.
- Restated style rules already in `docs/PYTHON_STYLE.md`,
  `docs/MARKDOWN_STYLE.md`, or `docs/REPO_STYLE.md`.
- Aspirational guidance with no enforcement and no concrete action.
- Generic AI etiquette unrelated to this repo (tone, manners, hedging
  advice).
- Commit-message and changelog rules already in `docs/CHANGELOG.md` or
  `docs/REPO_STYLE.md`.
- "Future considerations" sections with no owner and no date.

## Manager judgment rubric

For each line or section, answer in order. Stop at the first "yes" that
demands action.

1. Is this repo-specific (would it differ in a sibling repo)? If no, cut or
   replace with a link to the canonical doc.
2. Is the same rule already written in a `docs/*.md` file? If yes, replace
   with a link to that file.
3. If this line were removed today, would an agent's behavior change on a
   real task? If no, cut.
4. Is the canonical home a sibling doc that already exists? If yes, move
   the content there and link from `AGENTS.md`.
5. Otherwise, keep, and trim wording to a single short bullet.

## Workflow

1. Read the current `AGENTS.md` and the `docs/` index.
2. Check `wc -l AGENTS.md` against the repository policy. If it is already a
   tight pointer file and passes the rubric, report no action needed and stop.
3. For each section, apply the rubric. Categorize each as one of:
   `keep`, `link-only`, `move-to-docs`, or `delete`.
4. For `move-to-docs` items, identify the right `docs/*.md` target using
   the recommended common docs list in `docs/REPO_STYLE.md`. If the target
   doc does not exist yet, do not create it here. Note it as a follow-up
   for `docset-updater`, `setup-install-usage-docs`, or `arch-docs`.
5. Rewrite `AGENTS.md` minimally with short sentence-case headings and `-`
   bullets.
6. Preserve any user instruction explicitly marked as overriding defaults.

## Markdown house rules

- ASCII only; escape symbols like `&alpha;` if needed.
- Sentence case headings, short headings (3-6 words).
- Bullets use `-`, one idea per bullet.
- Reference docs by bare path, optionally in backticks; do not use Markdown
  link syntax.

## Quality bar

- Final `AGENTS.md` is small: prefer about 15 non-blank lines, hard cap
  about 50. Smaller is always better. If you cannot get under 50, more
  content belongs in `docs/*.md`.
- Most of the file is bare path pointers into `docs/*.md`, not prose.
- No duplication of canonical `docs/*.md` content.
- Every external concept is referenced by path, not restated.
- No deletion of genuinely repo-specific operational rules.
- No new sections with content that has no enforcement or no concrete
  action.

## Inputs to inspect

- Current `AGENTS.md` content.
- The list of files under `docs/` (so the skill can choose link targets
  that actually exist).
- Any standing override already marked for verbatim preservation.

## Output

- The applied `AGENTS.md` patch with minimal edits.
- A change log with three short lists:
  - `moved`: each chunk moved into `docs/*.md`, with the destination file.
  - `linked`: each chunk replaced by a bare path pointer, with the target.
  - `deleted`: each chunk deleted, with one sentence of justification.
- A short follow-up list of `docs/*.md` stubs that should exist, naming
  the skill that owns each one (`docset-updater`, `setup-install-usage-docs`,
  `arch-docs`, or `readme-docs`).

## References

- `docs/REPO_STYLE.md`: "AGENTS.md files"
  section sets the 100-150 line target and the "concise and operational"
  rule.
- `docs/MARKDOWN_STYLE.md`: heading and
  link conventions used in the rewrite.
- `../readme-docs/SKILL.md`: sibling
  single-artifact standardizer with the same shape.

In a docset refresh, run after the linked `docs/*.md` files exist and alongside
`screenshot-docs`; this skill owns only `AGENTS.md`.
