---
name: see-also-docs
description: "Create or refresh `docs/RELATED_PROJECTS.md` as a visitor guide to comparable projects and resources, alternatives, prior art, lineage, and closely related companion work."
---

# See also docs

## Overview

Create or refresh `docs/RELATED_PROJECTS.md` as a sourced discovery guide for GitHub
visitors. Answer this question:

> If a visitor likes or needs this repository, what other project or resource would
> they reasonably explore next?

Use GitHub visitor-discovery scope. Treat `see-also-docs` as the routing name chosen
because the skill catalog has many `re...` prefixes.

Require a shared audience, problem, or workflow. For a QTI package converter, useful
candidates include other QTI converters, editors, validators, and directly relevant
QTI resources. Python.org has reader relevance when the repository itself concerns
Python language or tooling; implementation in Python alone supplies context rather
than a related-project relationship.

This skill is evidence-first. Web discovery finds candidates; specific overlap in
audience, purpose, or workflow decides whether a candidate belongs and at what
confidence. Write the file after at least one entry passes the visitor relevance gate
and manager checklist.

## Visitor relevance gate

Before classifying a candidate, complete this sentence with specific facts:

> A visitor interested in this repository may also want **candidate** because both
> help **audience** accomplish **shared or adjacent goal**.

A candidate passes when the sentence identifies a concrete audience and goal supported
by the candidate's own documentation or another authoritative source.

Use implementation manifests and dependency declarations to understand the repository's
subject and vocabulary. Select entries after separate evidence establishes visitor value.

## Manager inclusion checklist

Use this checklist before approving each entry. An entry is ready when every core check
and at least one relationship check is marked `[x]`.

### Core checks

- [ ] The repository and candidate serve a substantially overlapping audience.
- [ ] The candidate helps that audience accomplish the same goal or an adjacent step in
      the same workflow.
- [ ] The visitor-value sentence names a concrete outcome a visitor can accomplish.
- [ ] The candidate's official documentation supports its purpose.
- [ ] An authoritative source supports the claimed relationship.
- [ ] The recommendation remains useful if this repository changes its implementation
      language or framework.

### Relationship checks

- [ ] It offers another way to accomplish the same task.
- [ ] It supports a closely adjacent step in the same user workflow.
- [ ] It is an upstream, fork, successor, prior-art source, or inspiration.
- [ ] It is a companion project, extension, or interoperability tool for the primary
      use case.
- [ ] It is a sibling project with a substantially overlapping user goal.
- [ ] It is a standard, guide, dataset, or resource directly useful for the primary
      task.

Approve candidates that satisfy all core checks and at least one relationship check.
Keep partially researched candidates as leads in the run report.

## Relationship taxonomy

Classify each project as one of:

- Direct alternative or competitor
- Same-workflow project or independent implementation
- Prior art or inspiration
- Upstream source, fork, or successor
- Companion project, extension, or interoperability tool
- Closely related sibling project with an overlapping user goal
- Domain standard, guide, dataset, or other visitor resource

## Confidence tiers

- Confirmed: explicit comparison, lineage statement, inspiration citation, reader-facing
  link, or reciprocal project link establishes the relationship.
- Likely: authoritative descriptions establish the same audience, problem, and a
  substantially overlapping workflow.
- Possible: authoritative descriptions establish a useful adjacent workflow or partial
  overlap, with a clear visitor-value sentence.

The written file groups Confirmed entries under "Confirmed related projects" and
Likely plus Possible entries under "Possible related projects".

## Web discovery (tool-neutral, bounded)

Complete two focused search rounds.

- Use whichever available web search and fetch capabilities fit the environment.
- Search by the repository's user task, input and output formats, domain standards,
  intended audience, and distinguishing workflow. For example, use searches such as
  "QTI converter", "QTI package builder", and "QTI assessment tool" for a QTI maker.
- Query repository and package metadata where it helps verify each candidate's purpose,
  official home, authorship, or maintenance status.
- Prefer candidate documentation, explicit comparison or lineage statements, reciprocal
  project links, citations, and official project descriptions. Use generic keyword or
  title similarity as a lead for deeper verification.
- Run one seed round from repo evidence and one widening round to chase concrete
  leads. Put additional untraced leads in the run report.
- Add `time.sleep(random.random())` between API or web calls to pace server load, per
  `docs/REPO_STYLE.md`.
- Cite every entry with a link and a one-line summary of the relationship evidence.

## Workflow

1. Seed from repo evidence
   - Read `README.md`, `AGENTS.md`, and relevant `docs/` to identify the primary
     audience, user goal, inputs, outputs, standards, comparisons, lineage, inspiration,
     companion work, and outbound project links.
   - Read manifests when present to confirm project identity, official URLs, keywords,
     commands, formats, and other vocabulary that describes the user-facing purpose.
   - Read any existing `docs/RELATED_PROJECTS.md`; preserve accurate entries and
     refresh the affected sections.
   - Write a one-sentence description of what visitors use this repository to accomplish.
2. Discover candidates with bounded web discovery
   - Run the seed round, then one widening round, per the rules above.
   - For each candidate, capture its official link, visitor-value sentence, and strongest
     evidence.
3. Apply the visitor relevance gate
   - Complete the manager inclusion checklist for existing entries and newly discovered
     candidates.
   - Build the final candidate set from entries that satisfy the checklist.
4. Classify by confidence tier
   - Assign a relationship from the taxonomy and a tier (Confirmed, Likely, or
     Possible) using the evidence and visitor value.
   - Record maintenance signals (last release, last commit, license, language) as
     context after determining relevance.
5. Write the owned file when evidence supports it
   - Apply the content-or-no-file threshold below.
   - When the threshold is met, write `docs/RELATED_PROJECTS.md` in the output shape
     below, following the writing-shape template in
     [references/related_projects_template.md](references/related_projects_template.md).
6. Report follow-ups
   - In the run report, list untraced leads and suggestions ("consider evaluating X
     as an alternative", "consider linking Y as prior art").
   - Keep these follow-ups in the run report.

## Content-or-no-file threshold

Write `docs/RELATED_PROJECTS.md` when at least one candidate passes the visitor relevance
gate and manager checklist. Give every entry a real link, a specific visitor-value line,
and an evidence line. A single Likely or Possible entry qualifies when it meets all three
requirements.

For a search with zero passing candidates, preserve the documentation tree and report
the user-task searches performed. Put known gaps and untraced leads in the run report so
the published file contains useful destinations.

## Output shape

`docs/RELATED_PROJECTS.md` uses each of these tier sections when it has entries:

```
# Related projects

## Confirmed related projects

### project-name
- Relationship: same-workflow alternative
- Link: https://example.com/project
- Why visitors may care: offers another way to convert assessments into QTI packages.
- Evidence: official documentation describes QTI conversion for LMS import workflows.

## Possible related projects

### project-name
- Relationship: same-workflow project
- Link: https://example.com/other
- Why visitors may care: supports an adjacent authoring workflow for the same audience.
- Evidence: official documentation describes the overlapping workflow.
- Confidence: low

## Evidence notes

Short prose summary of the source basis (project documentation, explicit comparisons,
lineage statements, official descriptions, or reciprocal links).
```

## Style

- Follow `docs/MARKDOWN_STYLE.md` and `docs/REPO_STYLE.md`.
- ASCII only; escape symbols like `&alpha;` if needed.
- Sentence-case, short headings; `-` for bullets, one idea per bullet.
- Use relative Markdown links for in-repo paths and full URLs for external projects.
- Present tense, active voice; state facts the evidence supports.

## Wrap up

- Apply the threshold: save `docs/RELATED_PROJECTS.md` for passing entries and report
  zero-result searches in the run report.
- Limit authored documentation to `docs/RELATED_PROJECTS.md` and the changelog entry.
- Update `docs/CHANGELOG.md` directly when this skill runs as a standalone task; under
  `delegate-manager-to-subagents`, dispatch a docs subagent to add the entry.

## Example requests

- "Document the projects related to this repo."
- "Refresh docs/RELATED_PROJECTS.md with current alternatives and prior art."
- "Find sibling repos and prior art for this tool and write them up with sources."
- "Show visitors other QTI converters and QTI authoring resources like this project."

## Delegated execution

Under `delegate-manager-to-subagents`, this skill is assigned to a fresh subagent
with one bounded task, the relevant repo rules, and one verification step.
Dispatch a new subagent for each atomic follow-up task. See `docs/REPO_STYLE.md`.
