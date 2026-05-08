---
name: agents-md-fixer
description: "Trim `AGENTS.md` aggressively to a small pointer file (prefer ~15 lines, hard cap ~50) that links into `docs/*.md` instead of restating rules. Use when `AGENTS.md` is bloated, philosophical, or duplicates style content already in `docs/*.md`. Does NOT touch `README.md` or files under `docs/` (use `readme-docs`, `arch-docs`, `install-usage-docs`, or `docset-updater` for those)."
mode: doer
execution: either
---

# AGENTS.md fixer

## Goal

Make `AGENTS.md` a tiny pointer file. It should mostly be links into
`docs/*.md`, not prose. The longer `AGENTS.md` grows, the worse AI coding
agents perform: they skim, prioritize poorly, and miss the load-bearing
rules. This skill audits `AGENTS.md` and returns an aggressively tightened
version, with the manager (the invoking agent) exercising judgment about
what is important for *this* repo versus frivolous.

Size guidance (line count is a rough proxy, not a contract; "line" means a
non-blank text line in the rendered Markdown):

- Prefer about 15 lines or fewer.
- Hard cap at about 50 lines. If the file is longer, something belongs in
  `docs/*.md` instead.
- The shorter the better. A 10-line `AGENTS.md` that links to the right
  docs is better than a 40-line one that restates them.

If a rule has a canonical home in `docs/*.md`, link, do not restate. The
[docs/REPO_STYLE.md](../../docs/REPO_STYLE.md) "AGENTS.md files" section
describes the philosophy.

## Required content (keep)

Keep only items that are repo-specific and load-bearing:

- Pointer links to canonical style docs that exist in this repo, for example
  [docs/REPO_STYLE.md](../../docs/REPO_STYLE.md),
  [docs/PYTHON_STYLE.md](../../docs/PYTHON_STYLE.md),
  [docs/MARKDOWN_STYLE.md](../../docs/MARKDOWN_STYLE.md),
  [docs/PYTEST_STYLE.md](../../docs/PYTEST_STYLE.md), and
  [docs/CHANGELOG.md](../../docs/CHANGELOG.md).
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
2. Get a rough size: `wc -l AGENTS.md`. Treat this as a smell test, not a
   contract. If the file is already a tight pointer file (roughly under 15
   non-blank lines) and every section already passes the rubric, report
   "no action needed" and stop. Do not invent churn.
3. For each section, apply the rubric. Categorize each as one of:
   `keep`, `link-only`, `move-to-docs`, or `delete`.
4. For `move-to-docs` items, identify the right `docs/*.md` target using
   the recommended common docs list in `docs/REPO_STYLE.md`. If the target
   doc does not exist yet, do not create it here. Note it as a follow-up
   for `docset-updater`, `install-usage-docs`, or `arch-docs`.
5. Rewrite `AGENTS.md` minimally: short headings, sentence case, bullet
   lists with `-`, and links with file-path link text per
   [docs/MARKDOWN_STYLE.md](../../docs/MARKDOWN_STYLE.md).
6. Preserve any user instruction explicitly marked as overriding defaults.

## Markdown house rules

- ASCII only; escape symbols like `&alpha;` if needed.
- Sentence case headings, short headings (3-6 words).
- Bullets use `-`, one idea per bullet.
- Use Markdown links with file-path link text. Good:
  `[docs/REPO_STYLE.md](docs/REPO_STYLE.md)`. Bad:
  `[Repo style](docs/REPO_STYLE.md)`.
- Only include a backticked path when the link text is not the path.

## Quality bar

- Final `AGENTS.md` is small: prefer about 15 non-blank lines, hard cap
  about 50. Smaller is always better. If you cannot get under 50, more
  content belongs in `docs/*.md`.
- Most of the file is links into `docs/*.md`, not prose.
- No duplication of canonical `docs/*.md` content.
- Every external concept is linked, not restated.
- No deletion of genuinely repo-specific operational rules.
- No new sections with content that has no enforcement or no concrete
  action.

## Inputs to request

- Current `AGENTS.md` content.
- The list of files under `docs/` (so the skill can choose link targets
  that actually exist).
- Any standing user override that must be preserved verbatim.

## Output

- A proposed `AGENTS.md` patch with minimal edits, ready for review.
- A change log with three short lists:
  - `moved`: each chunk moved into `docs/*.md`, with the destination file.
  - `linked`: each chunk replaced by a link, with the link target.
  - `deleted`: each chunk deleted, with one sentence of justification.
- A short follow-up list of `docs/*.md` stubs that should exist, naming
  the skill that owns each one (`docset-updater`, `install-usage-docs`,
  `arch-docs`, or `readme-docs`).

## References

- [docs/REPO_STYLE.md](../../docs/REPO_STYLE.md): "AGENTS.md files"
  section sets the 100-150 line target and the "concise and operational"
  rule.
- [docs/MARKDOWN_STYLE.md](../../docs/MARKDOWN_STYLE.md): heading and
  link conventions used in the rewrite.
- [skills/readme-docs/SKILL.md](../readme-docs/SKILL.md): sibling
  single-artifact standardizer with the same shape.

## Delegated execution

Under `execution-manager`, this skill is assigned to a fresh subagent with
one bounded task, the relevant repo rules, and one verification step. Do
not continue the same subagent across unrelated follow-up work; dispatch a
new subagent for each atomic task. See
[docs/REPO_STYLE.md](../../docs/REPO_STYLE.md#core-philosophies).
