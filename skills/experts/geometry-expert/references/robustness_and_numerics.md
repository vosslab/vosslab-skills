# Robustness and numerics

Use this guide when numerical error can change a geometric decision, topology,
or iterative model.

## Separate measurement from decision

A distance or area may tolerate bounded error. Orientation, in-circle,
incidence, containment, and edge ordering are sign decisions whose wrong sign
can corrupt topology. Centralize these predicates, define the zero case, and
place all epsilon comparisons in that policy.

The sampled sources explain why:

- `local-only/Geometric_Tools_for_Computer_Graphics-2003.md`, `1.2 Issues of
  Numerical Computation`, shows nonassociativity, cancellation, tangency, and
  order-dependent Boolean results.
- `local-only/Computational_Geometry_Algorithms_and_Applications-2008.md`, `1.1
  An Example: Convex Hulls`, shows near-collinear rounding producing an
  inconsistent combinatorial hull.
- `local-only/Handbook_of_Discrete_and_Computational_Geometry-2018.md`, `45
  ROBUST GEOMETRIC COMPUTATION`, develops exact, filtered, and soft-exact
  strategies and explains the missing robustness guarantee in ad hoc epsilon.

## Degeneracy catalog

Exercise at least the cases relevant to the contract:

- Collinear, cocircular, coplanar, concurrent, or parallel inputs.
- Duplicate points, zero-length edges, repeated vertices, and zero-area faces.
- Shared endpoints, coincident edges, tangency, and touch-only intersections.
- Points exactly on boundaries and queries exactly on subdivision vertices.
- Self-intersecting polygons passed to simple-polygon algorithms.
- Nonmanifold, unoriented, inverted, sliver, or disconnected meshes.
- Very large/small coordinates and subtraction of nearly equal values.
- Polynomial coefficients outside the declared base field or silently rounded.
- Conformal iterations on invalid topology or poor triangles.

Degeneracy is not always invalid input. The contract must say whether each case
is rejected, normalized, represented as a lower-dimensional result, or resolved
by a deterministic tie-break.

## Core predicates

| Predicate | Decision | Robust default |
| --- | --- | --- |
| `orientation(p, q, r)` | Counterclockwise, clockwise, or collinear | Filtered/adaptive determinant sign; exact fallback near zero |
| `in_circle(p, q, r, s)` | Site inside, on, or outside an oriented circumcircle | Filtered/adaptive determinant with orientation convention |
| `side_of_line(p, q, r)` | Side or boundary | Reuse orientation and its zero policy |
| `distance_compare(p, q, r)` | Which squared distance is smaller | Compare squared values; exact integers/rationals when available |
| `point_in_polygon(p, ring)` | Inside, boundary, or outside | Explicit boundary predicate plus winding/ray logic |
| `incidence(a, b)` | Whether algebraic/geometric objects meet | Preserve exact symbolic input or use certified predicates |

Test permutation signs and boundary classifications directly. A robust
predicate has a documented input domain and does not expose an arbitrary
epsilon as mathematical truth.

## Arithmetic strategy

Choose deliberately:

1. Ordinary floating point for measurements on well-scaled, well-separated
   data when a numeric error bound is acceptable.
2. Filtered predicates: evaluate quickly, estimate the error bound, and fall
   back to exact arithmetic when the sign is uncertain.
3. Exact integers, rationals, expansions, or an exact geometry kernel when a
   sign or incidence must be certified.
4. Symbolic computer algebra for ideal and elimination tasks; preserve exact
   coefficients through the decisive operation.

Exact predicates with inexact constructions can still produce inconsistent
derived coordinates. State whether the kernel guarantees exact decisions only
or exact constructions too.

## Tolerance policy

- Attach tolerances to measured quantities with units and scale.
- Use absolute tolerance near zero and relative tolerance at scale only for
  approximate numeric comparisons.
- Apply topology-changing tolerance only through a contract-defined
  snapping/normalization operation.
- Normalize or rescale coordinates only when the transformation preserves the
  intended model, and test inverse mapping.
- Keep one policy owner so every algorithm makes the same decision.

## Specialized numerical checks

- Delaunay/Voronoi: accept multiple legal triangulations for cocircular sites;
  test empty-circle and dual invariants rather than one edge list.
- Mesh/conformal: track inverted elements, minimum angle, area, curvature error,
  energy, and boundary constraints alongside solver residuals.
- GJK/separating axes: define touching vs overlap and test support-map extrema.
- Motion planning: numeric waypoints require continuous or conservative segment
  collision checks; sampled collision-free points are insufficient.
- Algebraic geometry: record coefficient field and monomial order; verify
  reductions and substitutions exactly when the input is exact.
