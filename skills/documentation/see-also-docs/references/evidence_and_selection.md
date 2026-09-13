# Related-project evidence and selection

## Visitor relevance gate

Complete this sentence with specific evidence before classifying a candidate:

> A visitor interested in this repository may also want **candidate** because both help
> **audience** accomplish **shared or adjacent goal**.

A candidate passes when the audience and goal are concrete and supported by official project
documentation or another authoritative source. Implementation language alone does not establish a
visitor relationship.

## Inclusion checklist

Require every core check and at least one relationship check.

Core checks:

- The repository and candidate serve a substantially overlapping audience.
- They support the same goal or adjacent steps in the same workflow.
- The visitor-value sentence names a concrete outcome.
- Official documentation supports the candidate's purpose.
- An authoritative source supports the claimed relationship.
- The recommendation remains useful if implementation language or framework changes.

Relationship checks:

- another way to accomplish the same task;
- a closely adjacent step in the same workflow;
- upstream, fork, successor, prior art, or inspiration;
- companion, extension, or interoperability tool;
- sibling project with a substantially overlapping user goal;
- standard, guide, dataset, or resource directly useful for the primary task.

## Taxonomy and confidence

Classify the relationship as a direct alternative, same-workflow implementation, prior art,
upstream/fork/successor, companion/interoperability tool, closely related sibling, or domain
standard/resource.

- Confirmed: explicit comparison, lineage, inspiration, reciprocal link, or reader-facing link.
- Likely: authoritative descriptions establish the same audience, problem, and substantially
  overlapping workflow.
- Possible: authoritative descriptions establish a useful adjacent workflow or partial overlap.

Publish Confirmed entries under `Confirmed related projects`; publish Likely and Possible entries
under `Possible related projects` with their confidence made clear.

## Bounded discovery

Run one seed round from repository evidence and one widening round from concrete leads. Search by
the user task, formats, standards, audience, and distinguishing workflow. Prefer official homes,
candidate documentation, comparison or lineage statements, reciprocal links, citations, and
official metadata. Treat generic keyword similarity as a lead only.

Capture each candidate's official URL, visitor-value sentence, strongest relationship evidence,
and optional maintenance context. Cite every published entry. Pace external calls according to the
target repository's current network guidance.
