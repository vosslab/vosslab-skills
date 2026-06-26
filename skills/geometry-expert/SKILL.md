---
name: geometry-expert
description: Design, implement, debug, and review computational geometry algorithms in any language, including convex hull, polygon triangulation, Delaunay triangulation, Voronoi diagrams, polygon boolean clipping and overlay, segment intersection and sweep line, proximity and nearest-neighbor queries, point location, spatial data structures (k-d tree, BVH, R-tree, quadtree), arrangements, mesh processing, and distance/intersection queries in 2D, 3D, and nD. Use when working on geometric robustness, degeneracy and exact predicates, orientation and in-circle tests, winding and point-in-polygon, kernel/library choice (CGAL, Shapely/GEOS, SciPy spatial, Boost.Geometry), or geometry correctness, performance, and failure analysis.
---

# Geometry expert

## Overview

Use this skill to turn vague geometry requests into explicit tasks with stated primitives, dimension, exact-vs-approximate intent, and complexity targets.
Build project-specific geometry evidence (a written geometry contract and a fixture corpus) before changing algorithm behavior, so the skill drives a project workflow rather than a generic advisor.
Prefer simple, testable, robust algorithms over clever fragile ones, and validate every result against a trusted oracle.

## Workflow

1. Classify the geometric task and route it.
- Name the primitive, the dimension, construction vs query, exact vs approximate, and static vs dynamic.
- Consult [references/topic_index.md](references/topic_index.md) to route a problem to the geometry task, default algorithm or library, robustness risks, test fixtures, and the best local book.
- Read [references/task_selection.md](references/task_selection.md) when the request is underspecified or several geometry framings fit.

2. Detect the project shape, then write the geometry contract.
- Decide whether the target is an existing repo with geometry code or a greenfield project.
- Existing: build a geometry inventory (files owning primitives, predicates, algorithms, serialization/import, rendering/debug output, tests), then update the contract from it.
- Greenfield: write the contract first as the design source of truth, then choose the kernel/library strategy before data structures harden.
- Write the contract in the repo's existing docs location when present, otherwise create `docs/GEOMETRY_MODEL.md`: coordinate frame and axes, units, 2D vs 3D, primitive types, open vs closed polygons, winding order, tolerance policy, valid/invalid inputs, and expected degeneracy behavior.
- Read [references/project_workflow.md](references/project_workflow.md) for both paths.

3. Build the test corpus before feature code.
- Existing: capture representative and degenerate fixtures plus characterization tests around current behavior before changing algorithms.
- Greenfield: seed fixtures immediately (happy-path, boundary, degenerate, randomized small cases) with oracle expectations, then build the smallest validated geometry kernel before feature algorithms.
- Read [references/testing_and_oracles.md](references/testing_and_oracles.md) and [references/project_workflow.md](references/project_workflow.md).

4. Choose the simplest algorithm that meets the profile, and centralize predicates.
- Match the algorithm to the input-size profile: how many points, static vs dynamic, batch vs interactive, worst-case vs typical.
- Centralize robust predicates (orientation, in-circle, distance compare, epsilon decisions) in one place.
- Read [references/algorithm_design.md](references/algorithm_design.md) and [references/robustness_and_numerics.md](references/robustness_and_numerics.md).

5. Validate against an oracle and emit an artifact.
- Compare to a trusted library or brute force, then add property and randomized stress tests.
- Emit an inspectable artifact (SVG, PNG, OBJ, JSON, or an overlay) for representative and degenerate cases.
- Read [references/testing_and_oracles.md](references/testing_and_oracles.md).

6. Review and iterate one change at a time.
- Run the geometry review checklist, then make one change tied to a failing case.
- Read [references/project_workflow.md](references/project_workflow.md).

## Implementation defaults

- Reach for well-tested libraries first when available: CGAL for exact 2D/3D kernels and meshing, `scipy.spatial` for ConvexHull, Delaunay, Voronoi, and cKDTree, Shapely/GEOS for polygon boolean and topology, Boost.Geometry for C++ spatial work.
- Centralize robust orientation and in-circle predicates rather than scattering epsilons through the code.
- Reach for exact arithmetic or filtered predicates on degenerate inputs.
- Keep a trusted library or brute-force oracle even when production code is custom.
- Produce a visualization, dump, or inspectable artifact whenever the task yields geometric output.
- Load the local-only books first when present; see [references/local_books.md](references/local_books.md) and the survey in [references/reference_survey.md](references/reference_survey.md).

## Quality bar

- Favor correct-on-degeneracies over fast-on-the-happy-path.
- Document the coordinate system and tolerance policy.
- Keep predicates in one place and compare against an oracle on small cases.
- Make one change at a time, tied to a failing case.
- State what the algorithm cannot handle, such as self-intersecting input or near-degenerate precision.

## Output expectations

When using this skill, aim to produce:
- A clearly framed geometry task with stated primitives, dimension, exactness, and complexity target, plus the topic-index routing.
- For a project implementation task: a geometry contract, a fixture corpus, an algorithm choice with complexity, robustness and degeneracy handling, oracle and property tests, an inspectable artifact, and the next step.
