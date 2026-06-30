---
name: readme-docs
description: "Standardize `README.md` to match repo conventions: brief purpose, quick start, links to `docs/`, and a screenshots placeholder for the screenshot-docs skill. Use when `README.md` has drifted or is missing key pointers. Does NOT touch any file under `docs/` (use `arch-docs`, `setup-install-usage-docs`, or `docset-updater` for those)."
---

# README fix

## Goal

Make `README.md` short, correct, and consistent with this repo's documentation layout.
Keep deeper detail in `docs/` and link it from the README.

## Required sections

- Title.
- One paragraph: what it is and who it is for.
- "Documentation" section pointing into `docs/` (INSTALL, USAGE, TROUBLESHOOTING,
  CODE_ARCHITECTURE, FILE_STRUCTURE as applicable).
- Quick start for one primary path (keep it verifiable).

## Optional sections (only with evidence or genuinely short)

- Live demo link (see "Live demo / GitHub Pages" section below).
- Installation summary (otherwise link `docs/INSTALL.md`).
- Usage examples (otherwise link `docs/USAGE.md`).
- Testing command (only if you can confirm the command exists).
- Troubleshooting pointer (otherwise link `docs/TROUBLESHOOTING.md`).
- Status or maturity note (experimental, stable, deprecated).
- Maintainer or support link (issues, discussion, contact).
- Screenshots placeholder (see "Screenshots placeholder" section below).

## Live demo / GitHub Pages

When the repo deploys to GitHub Pages (a browser app, game, or interactive demo),
link the live GitHub Pages instance near the top of the README so users can run it
in one click without cloning. Evidence the repo uses Pages:

- A `gh-pages` branch, a `docs/` site root, or an `index.html` at the deploy root.
- A GitHub Actions workflow under `.github/workflows/` that deploys to Pages
  (for example `actions/deploy-pages` or `peaceiris/actions-gh-pages`).
- A configured Pages URL the user provides.

Construct the URL as `https://<owner>.github.io/<repo>/` (or the user-supplied custom
domain). Add a short, prominent line under the overview paragraph, for example:

```
Play it live: [<owner>.github.io/<repo>](https://<owner>.github.io/<repo>/)
```

Keep the link text the visible URL so readers see exactly where it goes. Only add the
link when you have confirmed Pages is deployed; do not guess a URL for a repo that does
not publish to Pages.

## Screenshots placeholder

When the README warrants a screenshots section (evidence: existing `docs/screenshots/`
directory, a prior README screenshots section, or explicit user request), insert the
empty managed screenshot block at the appropriate position in `README.md`. The block
is two sentinel comment lines with a one-line pointer between them:

```
<!-- screenshots:begin (managed by screenshot-docs) -->
Screenshots are managed by the screenshot-docs skill.
<!-- screenshots:end -->
```

The `screenshot-docs` skill owns the actual `docs/screenshots/` PNG files, the
`![alt](docs/screenshots/...)` embed syntax, and alt-text rules. In a second pass it
rewrites the lines between the two sentinels with real image embeds, keeping the
sentinels intact so repeat runs stay idempotent. readme-docs keeps ownership of
README prose and the two sentinel lines only. Insert the sentinels and the pointer
line; leave image embeds and PNG files to `screenshot-docs`.

Note: `tests/test_markdown_links.py` validates `![alt](path)` image embeds the
same as text links (the image path must be a tracked file). Image-path correctness
is the responsibility of `screenshot-docs`; readme-docs inserts only the two
sentinel comment lines and one-line pointer.

## Inputs to request

- Current `README.md` content.
- How the tool is intended to be run (CLI, library, web service, container).
- Known prerequisites and common failures, if any.

## Workflow

1. Read the current README and docs index
   - Read `README.md`.
   - Scan `docs/` for existing target docs (INSTALL, USAGE, TROUBLESHOOTING, etc.).
2. Enforce the README role
   - README contains:
     - One paragraph: what the project is and who it is for.
     - One "Quick start" that actually works or is clearly scoped.
     - A "Documentation" section with links to the deeper docs.
   - Move long explanations into the appropriate `docs/*.md` file and link it, instead
     of expanding README.
3. Standardize structure (minimal, repeatable)
   - Project name heading.
   - Short overview paragraph.
   - Documentation links list.
   - Quick start for the primary path (one path only: local, container, or installable
     package).
   - Optional: "Testing" section only if a test command is verifiable in repo files.
4. Documentation section policy (curated, not exhaustive)
   - Link text must be the file path so readers know they are clicking a file and see
     the exact filename.
   - Good:
     - `[docs/MARKDOWN_STYLE.md](docs/MARKDOWN_STYLE.md)`: Markdown rules for this repo.
   - Bad:
     - `[Style Guide for Markdown](docs/MARKDOWN_STYLE.md)`
   - Only include a backticked path when the link text is not the path.
   - Choose the documentation list format based on doc count:
     - Small docset (3 to 8): single list, each item includes path link as link text
       + one line description. Do not repeat the path in backticks.
     - Medium docset (9 to 16): group into 2 to 4 labeled subsections, keep each
       group short.
     - Large docset (more than 16): list 3 to 6 core docs plus 1 to 2 index docs
       that cover the long tail. Do not enumerate everything.
5. Decide which docs are link only versus needing a short README section
   - Link only is fine for:
     - Standards and policies (style guides, repo style).
     - Internals that most users do not need first (architecture, file structure),
       unless the repo is developer facing.
   - Include a short README section (then link to the full doc) for:
     - Installation and prerequisites: keep a minimal quick start, then link
       `docs/INSTALL.md`.
     - Primary usage path: one minimal example, then link `docs/USAGE.md`.
     - Key concepts users must understand early (formats, engines, question bank
       rules, version compatibility): 3 to 8 lines max, then link the authoritative
       doc.
     - Troubleshooting: only include 2 to 3 verified common failures, otherwise
       link `docs/TROUBLESHOOTING.md`.
6. Keep README short by moving detail into docs
   - If README starts to grow past the quick start and a curated doc map, move long
     sections into the correct `docs/*.md` file and link it from README.
7. Apply Markdown house rules
   - ASCII only; escape symbols like `&alpha;` if needed.
   - Sentence case headings, short headings.
   - Bullets use `-`, one idea per bullet.
   - Relative links with descriptive text.
   - When referencing files, use Markdown links so users can click through. Markdown
     links are created using the syntax `[link text](URL)`, where "link text" is the
     clickable text that appears in the document, and "URL" is the web address or
     file path the link points to. This allows users to navigate between different
     content easily. Use file-path link text so readers know the exact filename
     (good: `[docs/MARKDOWN_STYLE.md](docs/MARKDOWN_STYLE.md)`, bad:
     `[Style Guide for Markdown](docs/MARKDOWN_STYLE.md)`).
8. Enforce REPO_STYLE documentation rules
   - Do not add banned docs (CONTRIBUTING.md, templates, SECURITY.md unless supported).
   - If a missing common doc is required to keep README concise (usually INSTALL or
     USAGE), create a minimal stub under `docs/` using ALL CAPS naming and link it.
   - Prefer social links over hard coded email when adding contact.
9. Keep claims verifiable
   - Only include commands you can confirm exist (scripts, Makefile targets, documented
     CLI).
   - If a detail is unclear, add a short note pointing to where it should be verified,
     then stop.

## Quality bar
- README stays short. Prefer links plus one line descriptions over large inlined manuals.
- Documentation links use the file path as link text and include a one line
  description. Do not repeat the same path in backticks.
- Include short sections only when they unblock getting started or explain a
  required concept.
- For large docsets, list core docs plus index docs, not everything.

## Output

- A proposed README patch with minimal edits.
- A short checklist of missing docs under `docs/` that should exist for this repo type.

## References (optional)

- GitHub Docs: "About READMEs" for expected content and auto TOC behavior.
- Standard Readme community spec for section ordering.
- READMINE template for an explicit TOC example.

## Delegated execution

Under `delegate-manager-to-subagents`, this skill is assigned to a fresh subagent
with one bounded task, the relevant repo rules, and one verification step.
Do not continue the same subagent across unrelated follow-up work; dispatch a
new subagent for each atomic task. See
`docs/REPO_STYLE.md`.
