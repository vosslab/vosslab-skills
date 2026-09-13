---
name: see-also-docs
description: "Create or refresh `docs/RELATED_PROJECTS.md` as a visitor guide to comparable projects and resources, alternatives, prior art, lineage, and closely related companion work."
---

# See also docs

## Purpose

Create or refresh `docs/RELATED_PROJECTS.md` as a sourced visitor-discovery guide. Include only
destinations that share a concrete audience, problem, or workflow with the target repository.

## Evidence boundary

Read [`references/evidence_and_selection.md`](references/evidence_and_selection.md) before web
discovery. It owns the visitor relevance sentence, inclusion checklist, relationship taxonomy,
confidence tiers, and bounded two-round search method.

Use implementation manifests to understand the repository's subject and vocabulary. Establish
visitor value separately; a shared implementation language or dependency is not enough.

## Workflow

1. Read the repository README, agent guidance, relevant docs, manifests, and existing
   `docs/RELATED_PROJECTS.md`. Identify the primary audience, user goal, formats, standards,
   comparisons, lineage, companion work, and outbound project links.
2. Write one sentence describing what visitors use this repository to accomplish.
3. Run the seed and widening discovery rounds from `evidence_and_selection.md` using the available
   search and fetch tools.
4. For every candidate, capture the official link, visitor-value sentence, relationship type,
   confidence tier, and strongest authoritative evidence.
5. Apply the full inclusion checklist. Keep partial research and untraced leads in the run report.
6. Write the owned file only when at least one candidate passes. Follow
   [`references/related_projects_template.md`](references/related_projects_template.md).
7. Refresh existing entries that remain accurate and remove claims no longer supported by current
   evidence.
8. Update the target repository changelog when its rules require that documentation handoff.

## Publication threshold

One Confirmed, Likely, or Possible entry qualifies when it has a real link, a specific visitor-value
line, authoritative relationship evidence, and every required checklist result. When no candidate
passes, preserve the documentation tree and report searches, gaps, and untraced leads outside the
published file.

## Output contract

Group explicit comparison or lineage evidence under `Confirmed related projects`. Group useful
same-audience or adjacent-workflow candidates under `Possible related projects`, stating confidence
when needed. For each entry include:

- relationship type;
- official link;
- why visitors may care;
- evidence supporting the relationship;
- confidence when it is not confirmed.

Close with concise evidence notes describing the authority basis. Follow the target repository's
Markdown and ASCII rules. Limit authored product documentation to `docs/RELATED_PROJECTS.md` plus
the required changelog record.

## Completion

Return the published path and passing entries with their evidence, or a zero-result receipt naming
the searches performed and why candidates failed. Report remaining leads separately so the public
file contains only useful, supported destinations.
