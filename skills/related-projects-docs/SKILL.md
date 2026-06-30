---
name: related-projects-docs
description: "Create or refresh `docs/RELATED_PROJECTS.md` from repo evidence plus bounded web discovery, writing a sourced, confidence-tiered map of upstreams, dependencies, integrations, sibling repos, and alternatives. Use when the user asks to document, discover, or refresh related or sibling projects, prior art, or alternatives for a repo. Does NOT touch `README.md`, `docs/CODE_ARCHITECTURE.md`, `docs/FILE_STRUCTURE.md`, `docs/INSTALL.md`, `docs/USAGE.md`, or the broader doc set (use `arch-docs`, `readme-docs`, or `docset-updater` for those)."
---

# Related projects docs

## Overview

Create or refresh `docs/RELATED_PROJECTS.md`: a sourced map of projects related to
this repo (upstreams and forks, dependencies, integration targets, companion repos,
same-author siblings, same-domain alternatives, and prior art).

This skill is evidence-first, not search-result-first. Web discovery finds candidates;
repo evidence and reciprocal links decide whether a candidate belongs and at what
confidence. Write the file only when real evidence supports at least one entry.

## Relationship taxonomy

Classify each project as one of:

- Upstream source or fork
- Direct dependency
- Optional integration target
- Companion CLI, library, or demo repo
- Same-author or same-org sibling repo
- Same problem domain, independent implementation
- Prior art or inspiration
- Replacement, competitor, or alternative

## Confidence tiers

- Confirmed: explicit link, dependency, package metadata, import, or citation.
- Likely: same author or org plus overlapping name or purpose.
- Possible: similar domain, no direct evidence.
- Rejected: tempting match, but unrelated. Record these so they are not re-confused.

The written file groups Confirmed entries under "Confirmed related projects" and
Likely plus Possible entries under "Possible related projects".

## Web discovery (tool-neutral, bounded)

Discovery is a bounded step, not an open-ended crawl.

- Use the available web search and fetch tools. Do not assume one specific tool by
  name; use whichever search and fetch capabilities the environment provides.
- Query package and repository metadata where available (GitHub repo and topics,
  PyPI, npm, crates.io, Homebrew, Docker Hub) by exact name, normalized name, import
  or package name, and CLI command name.
- Treat as higher-confidence evidence: GitHub repo links and reciprocal links,
  dependency-graph or dependents data, package metadata (`project.urls`, optional
  extras, entry points, classifiers), explicit fork/upstream statements, and official
  project links. Treat generic web hits (keyword or title similarity, stars alone) as
  lower-confidence.
- Cap discovery at 2 search rounds: one seed round from repo evidence, one widening
  round to chase concrete leads. Stop after the second round even if more candidates
  could exist; record untraced leads as run-report follow-ups, not doc entries.
- Add `time.sleep(random.random())` between API or web calls to avoid overloading
  servers, per `docs/REPO_STYLE.md`.
- Cite every entry with a link and a short evidence line. The evidence line is a
  one-line summary of the basis, not a raw search log.

## Workflow

1. Seed from repo evidence
   - Read `README.md`, `AGENTS.md`, and `docs/` for "inspired by", "forked from",
     "compatible with", "plugin", "adapter", badges, and outbound links.
   - Read manifests when present: `pyproject.toml` (`project.name`, import package,
     `console_scripts`, optional dependencies, classifiers, keywords, `project.urls`),
     `package.json`, `Cargo.toml`, `pip_requirements.txt`.
   - Read any existing `docs/RELATED_PROJECTS.md` to update rather than rewrite.
   - List the concrete names, packages, commands, authors, and orgs to search for.
2. Discover candidates with bounded web discovery
   - Run the seed round, then one widening round, per the rules above.
   - For each candidate, capture the link and the strongest evidence found.
3. Classify by confidence tier
   - Assign a relationship from the taxonomy and a tier (Confirmed, Likely, Possible,
     Rejected) using the evidence, not the candidate's popularity.
   - Keep maintenance signals (last release, last commit, license, language) as
     context, not as ranking.
4. Write the owned file only when evidence supports it
   - Apply the content-or-no-file threshold below.
   - When the threshold is met, write `docs/RELATED_PROJECTS.md` in the output shape
     below, following the writing-shape template in
     [references/related_projects_template.md](references/related_projects_template.md).
5. Report follow-ups (report-only)
   - In the run report, list untraced leads and suggestions ("consider documenting
     compatibility with X", "consider linking Y as prior art").
   - Do NOT edit `docs/ROADMAP.md`, `docs/TODO.md`, or any other doc with these
     follow-ups; report them only.

## Content-or-no-file threshold

Write `docs/RELATED_PROJECTS.md` only when at least one Confirmed or evidenced entry
exists beyond the title and intro. A single Likely or Possible entry with a real link
and evidence line qualifies; a vague guess with no link does not.

When no candidate clears that bar, write NO file. Report the gap in the run report
instead: state that no evidenced related projects were found and list what was
searched. Never write a hollow or stub file with empty tier sections, and never add a
"Known gaps" section to the doc to justify a near-empty file. Known gaps belong in the
run report only.

## Output shape

`docs/RELATED_PROJECTS.md` uses these sections (omit a tier section when it has no
entries):

```
# Related projects

## Confirmed related projects

### project-name
- Relationship: optional dependency
- Link: https://example.com/project
- Evidence: listed in pyproject optional dependencies and referenced in README usage.
- Notes: used for exporting diagrams.

## Possible related projects

### project-name
- Relationship: same-domain alternative
- Link: https://example.com/other
- Evidence: shares a GitHub topic and solves the same workflow; no direct repo link.
- Confidence: low

## Evidence notes

Short prose summary of the source basis (manifests, reciprocal links, package
metadata, GitHub topics). Not a raw search log.
```

When useful, add focused subsections such as "Commonly confused unrelated projects"
for Rejected matches worth recording.

## Style

- Follow `docs/MARKDOWN_STYLE.md` and `docs/REPO_STYLE.md`.
- ASCII only; escape symbols like `&alpha;` if needed.
- Sentence-case, short headings; `-` for bullets, one idea per bullet.
- Use relative Markdown links for in-repo paths and full URLs for external projects.
- Present tense, active voice; state facts the evidence supports.

## Wrap up

- Save `docs/RELATED_PROJECTS.md` only when the threshold is met; otherwise report the
  gap and write no file.
- Leave `README.md` to `readme-docs` and architecture docs to `arch-docs`.
- Update `docs/CHANGELOG.md` directly when this skill runs as a standalone task; under
  `delegate-manager-to-subagents`, dispatch a docs subagent to add the entry.
- Note that docs-only changes do not require tests unless otherwise requested.

## Example requests

- "Document the projects related to this repo."
- "Refresh docs/RELATED_PROJECTS.md with current upstreams and alternatives."
- "Find sibling repos and prior art for this tool and write them up with sources."

## Delegated execution

Under `delegate-manager-to-subagents`, this skill is assigned to a fresh subagent
with one bounded task, the relevant repo rules, and one verification step.
Do not continue the same subagent across unrelated follow-up work; dispatch a
new subagent for each atomic task. See
`docs/REPO_STYLE.md`.
