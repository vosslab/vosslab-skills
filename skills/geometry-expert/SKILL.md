---
name: geometry-expert
description: Design, implement, debug, and review computational, discrete, algebraic, and conformal geometry. Use for predicates, intersections, polygons, hulls, Voronoi or Delaunay, meshes, spatial queries, motion planning, surface maps, or realizability.
---

# Geometry expert

## Overview

Turn vague geometry requests into explicit tasks with stated primitives,
dimension, exact-vs-approximate intent, topology, and complexity targets. Route
classical computational geometry, discrete realizability, computational
algebraic geometry, and conformal surface geometry as distinct branches.
Build project evidence before changing behavior, and validate each result
against a trusted oracle or mathematical invariant.

## Workflow

1. Classify the geometry branch and route the task.
- Name the primitive, dimension, construction vs query, exact vs approximate,
  static vs dynamic, and required topological guarantees.
- Separate classical algorithms, discrete theory, algebraic computation,
  conformal surface processing, and motion planning before choosing a method.
- Read [references/task_selection.md](references/task_selection.md), then route
  through [references/topic_index.md](references/topic_index.md).

2. Detect the project shape, then write the geometry contract.
- Decide whether the target is an existing repo with geometry code or a greenfield project.
- Existing: build a geometry inventory (files owning primitives, predicates, algorithms, serialization/import, rendering/debug output, tests), then update the contract from it.
- Greenfield: write the contract first as the design source of truth, then choose the kernel/library strategy before data structures harden.
- Write the contract in the repo's existing docs location when present, otherwise create `docs/GEOMETRY_MODEL.md`: coordinate frame and axes, units, 2D vs 3D, primitive types, open vs closed polygons, winding order, tolerance policy, valid/invalid inputs, and expected degeneracy behavior.
- Read [references/project_workflow.md](references/project_workflow.md) for both paths.

3. Consult the strongest available evidence.
- Use [references/local_books.md](references/local_books.md) to choose a book
  from `local-only/`, then confirm the topic, section, and grep term in
  [references/reference_survey.md](references/reference_survey.md).
- Read the surrounding passage, not just the matching line. Corroborate damaged
  equations or OCR with a second book.
- When the corpus is absent, coverage is thin, or an API is version-sensitive,
  use official library documentation plus first-principles reasoning.

4. Build the test corpus before feature code.
- Existing: capture representative and degenerate fixtures plus characterization tests around current behavior before changing algorithms.
- Greenfield: seed fixtures immediately (happy-path, boundary, degenerate, randomized small cases) with oracle expectations, then build the smallest validated geometry kernel before feature algorithms.
- Read [references/testing_and_oracles.md](references/testing_and_oracles.md) and [references/project_workflow.md](references/project_workflow.md).

5. Choose the simplest method that meets the profile.
- Match the algorithm to the input-size profile: how many points, static vs dynamic, batch vs interactive, worst-case vs typical.
- Centralize robust predicates and exactness decisions in one place.
- For algebraic and conformal branches, preserve the mathematical model and
  topological preconditions before optimizing implementation details.
- Read [references/algorithm_design.md](references/algorithm_design.md) and [references/robustness_and_numerics.md](references/robustness_and_numerics.md).

6. Validate against an oracle and emit an artifact.
- Compare to a trusted library, computer algebra system, brute force, or a
  theorem-derived invariant, then add property and randomized stress tests.
- Emit an inspectable artifact such as SVG, PNG, OBJ, JSON, a mesh-quality
  report, or an overlay for representative and degenerate cases.
- Read [references/testing_and_oracles.md](references/testing_and_oracles.md).

7. Review and iterate one change at a time.
- Run the geometry review checklist, then make one change tied to a failing case.
- Read [references/project_workflow.md](references/project_workflow.md).

## Implementation defaults

- Reach for well-tested geometry libraries before custom kernels: CGAL for
  exact 2D/3D kernels and meshing, `scipy.spatial` for Qhull and k-d tree
  workflows, Shapely/GEOS for polygon topology, and Boost.Geometry for C++.
- Use a computer algebra system for ideal membership, elimination, and
  Groebner-basis work.
- Centralize orientation, in-circle, containment, and tolerance decisions.
- Use exact arithmetic or filtered predicates when topology depends on a sign.
- Keep a trusted library or brute-force oracle even when production code is custom.
- Produce a visualization, dump, or inspectable artifact whenever the task yields geometric output.
- Load the best-matched local book when present; use the passage-verified survey
  rather than book reputation or raw match counts.

## Quality bar

- Favor correct-on-degeneracies over fast-on-the-happy-path.
- Document the coordinate system and tolerance policy.
- Keep predicates in one place and compare against an oracle on small cases.
- State model assumptions such as simple polygons, manifold meshes, generic
  position, orientability, or exact polynomial input.
- Make one change at a time, tied to a failing case.
- State what the algorithm cannot handle, such as self-intersecting input or near-degenerate precision.

## Output expectations

When using this skill, aim to produce:
- A framed geometry task with its branch, primitives, dimension, exactness,
  topology, scale, and topic-index route.
- For implementation: a geometry contract, focused fixtures, a justified method,
  degeneracy handling, oracle and property tests, an inspectable artifact, and
  the next bounded change.
