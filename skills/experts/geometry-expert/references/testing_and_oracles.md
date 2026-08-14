# Testing and oracles

Build a minimal corpus covering the contract, boundaries, degeneracies, and invariants.

## Fixture layers

1. Minimal examples with hand-verifiable answers.
2. Boundary and degeneracy cases from [robustness_and_numerics.md](robustness_and_numerics.md).
3. Fixed-seed randomized small cases compared with an independent oracle.
4. Representative performance cases matching real scale and distribution.
5. Regression fixtures reduced from every discovered failure.

Keep small fixtures inline and follow the target repository's test conventions.
Add a committed fixture directory only when the project already establishes one
or a human approves the new test data.

## Independent oracles

- GEOS/Shapely or Boost.Geometry for polygon topology and hull behavior.
- scipy.spatial/Qhull for hull, Delaunay, Voronoi, and k-d tree workflows.
- CGAL or another exact kernel for predicates, constrained triangulations, arrangements, and meshes.
- A computer algebra system for Groebner bases, normal forms, elimination, and exact solutions.
- Brute force for small intersection, nearest, range, containment, visibility, and collision cases.
- Theorem-derived invariants when multiple outputs are legal.

Use an oracle independent of the implementation under test. Two wrappers around
the same underlying library provide one implementation, not corroboration.

## Family invariants

### Predicates and polygons

- Orientation changes sign under an odd point swap and is translation invariant.
- Segment intersection is symmetric and classifies disjoint, point, and overlap
  results distinctly when the contract requires them.
- Polygon area obeys winding convention; containment distinguishes boundary.
- Boolean output has valid ring topology and expected area identities.

### Hull, triangulation, Voronoi, and Delaunay

- Hull vertices come from input and all sites lie inside/on the hull.
- Triangles preserve the domain, remain interior-disjoint, and satisfy
  appropriate Euler and incidence counts.
- Delaunay triangles satisfy the chosen empty-circle convention.
- Voronoi adjacency agrees with the Delaunay dual where general-position
  assumptions apply.

### Spatial structures and arrangements

- Nearest and range results equal brute force on fixed-seed small inputs.
- Index queries remain correct after every allowed update.
- Arrangement incidences are reciprocal and cell counts satisfy the applicable
  planar invariant.

### Distance, collision, visibility, and planning

- Distance is nonnegative, symmetric where appropriate, and zero under the
  contract's touching/overlap definition.
- GJK/support results agree with a separate primitive or sampled oracle.
- Visibility edges have unobstructed interiors.
- Every returned path begins/ends at the requested configurations and every
  path segment passes a continuous or conservative collision check.

### Mesh and conformal processing

- Mesh boundary, orientation, manifoldness, Euler characteristic, and quality
  metrics match the contract.
- Parameterization checks inverted triangles, boundary conditions, angle or
  conformal distortion, and round-trip/registration error.
- Solver convergence is necessary but not sufficient; topology and element
  quality must remain valid.

### Algebraic and realizability tasks

- Ideal membership agrees with normal-form reduction under the declared order.
- Elimination output vanishes when substituted into known exact solutions.
- A claimed realization satisfies every incidence/non-incidence relation using
  exact or certified checks.
- Failure of a numeric search is not evidence of non-realizability.

## Randomized and metamorphic checks

Use fixed seeds and shrink failures. Useful transformations include
translation, rotation, reflection, uniform scale, input permutation, duplicate
insertion, and coordinate normalization, but assert only invariants preserved
by the model. Run enough small cases to expose topology errors, then keep the
minimal failing example permanently.

## Inspectable artifacts

Emit at least one artifact when output is geometric:

- SVG or overlay for 2D points, edges, cells, paths, and boundary cases.
- JSON for coordinates, incidences, indices, exact coefficients, and metrics.
- OBJ/PLY plus a mesh-quality report for 3D or surface work.
- Solver trace for algebraic/conformal iterations, paired with invariant checks.

Temporary artifacts belong in the target repository's established, gitignored
scratch location. Documentation images follow that repository's documentation
placement rules.
