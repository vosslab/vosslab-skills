# related-projects-docs skill design

## Purpose

A dedicated doc skill that owns `docs/RELATED_PROJECTS.md`. It discovers candidate
related projects by web search (GitHub, PyPI, npm, crates.io, Homebrew, Docker Hub),
then writes a sourced relationship map. Search discovers candidates; repo evidence and
cross-links decide whether they belong. Evidence-first, not search-result-first.

This replaces the generic evidence-only audit guess for `RELATED_PROJECTS.md` with a
sourced, linked artifact. It slots into `docset-updater` as its own owner (the file
moves out of the step-3 audit set), same pattern as `arch-docs` / `readme-docs`.

## Relationship taxonomy

Classify each project as one of:

- Upstream source or fork
- Direct dependency
- Optional integration target
- Companion CLI / library / demo repo
- Same-author or same-org sibling repo
- Same problem domain, independent implementation
- Prior art or inspiration
- Replacement, competitor, or alternative

## Confidence tiers (separate confirmed from plausible)

- Confirmed: explicit link, dependency, package metadata, import, or citation
- Likely: same author/org plus overlapping name or purpose
- Possible: similar domain, no direct evidence
- Rejected: tempting match, but unrelated (record to stop re-confusion)

## Evidence line per entry

Each entry states relationship, link, and a short evidence line, for example:

- Relationship: optional integration target
- Evidence: imported in pyproject optional extras; README mentions plugin support

## Output shape

```
## Confirmed related projects
### project-name
- Relationship: optional dependency
- Link: ...
- Evidence: listed in pyproject optional dependencies and referenced in README usage.
- Notes: used for exporting diagrams.

## Possible related projects
### project-name
- Relationship: same-domain alternative
- Link: ...
- Evidence: shares a GitHub topic and solves the same workflow; no direct repo link.
- Confidence: low
```

Useful sections beyond the tiers:

- Active related projects
- Archived or superseded projects
- Historical prior art
- Commonly confused unrelated projects

## Search strategy (repo evidence first, then expand)

Seed from repo evidence, then widen:

- GitHub: exact repo name, package/import name, CLI command name, author/org plus
  keyword, topics plus domain terms, code search for import name or command name
- PyPI: exact package name, normalized variants
- npm / crates.io / Homebrew / Docker Hub when repo evidence points there
- README links and badges; `pyproject.toml` / `package.json` / `Cargo.toml`
  dependencies
- docs references: "inspired by", "forked from", "compatible with", "plugin",
  "adapter"
- same-author GitHub repos; same-org repositories
- web search for quoted phrases from the README tagline

Python projects especially: `pyproject.toml` `project.name`, import package name,
`console_scripts` entry points, optional dependencies, classifiers and keywords,
`project.urls`.

## Relatedness scoring (qualitative final doc)

- High confidence: repo links to project; project links back; dependency or optional
  dependency; shared package metadata URL; explicit fork/upstream statement; same
  author/org plus shared package naming; code imports or invokes it; README documents
  compatibility.
- Medium confidence: same author/org and similar domain; same CLI/package naming
  family; shared GitHub topics plus overlapping README phrases; appears in examples,
  docs, or screenshots; mentioned in issues or release notes.
- Low confidence: similar keywords only; same acronym; same domain with no direct
  link; search-title similarity only; stars/popularity without repo evidence.

## Maintenance signals (context, not ranking)

Last release, last commit, issue activity, package version, license, language. Stars
and downloads are weak signals only.

## Follow-up TODOs the skill can emit

- Consider documenting compatibility with X.
- Consider linking Y as upstream prior art.
- Consider adding Z to alternatives.

## Implementation notes

- Tools: WebSearch and WebFetch; PyPI / GitHub APIs via `curl` where available.
- Add `time.sleep(random.random())` between API calls per repo style.
- Follow `docs/REPO_STYLE.md` and `docs/MARKDOWN_STYLE.md`; ASCII only; relative links
  for in-repo paths and full URLs for external projects.
- After this skill ships, update `docset-updater` to route `RELATED_PROJECTS.md` to it
  (Wave 1 owner) and drop it from the step-3 audit list.

## Known gaps

- Decide the skill's stop condition (how many search rounds before it writes).
- Decide whether it edits `docs/ROADMAP.md` / `docs/TODO.md` with its follow-ups or
  only reports them.
