# Robustness and numerics

Use this reference when a geometry algorithm fails on degenerate inputs or produces wrong
topological answers.

## Degeneracy catalog

Test against all of these before declaring an algorithm correct:
- Collinear points: three or more points on the same line.
- Coincident points: duplicate or near-duplicate vertices.
- Cocircular points: four or more points on the same circle (Delaunay edge flip ambiguity).
- Near-parallel segments: intersection computed at large coordinate values, amplifying rounding
  error.
- Points exactly on an edge or boundary (containment test ambiguity).
- Zero-area polygons or zero-length segments.
- Self-intersecting polygons passed to algorithms that assume simple polygon input.
- Very large or very small coordinates (loss of precision in floating-point subtraction).

## Predicate-based design

Centralize all geometric decisions in explicit predicates; place every epsilon decision in one module.

## Curated predicate summary

| Predicate | What it decides | Robust implementation |
| --- | --- | --- |
| orientation(p, q, r) | Sign of signed area of triangle pqr (CCW, CW, collinear). | Cross product sign; use adaptive predicates for the collinear borderline. |
| in-circle(p, q, r, s) | Whether s is inside the circumcircle of (p, q, r). | 4x4 determinant sign; exact arithmetic required for Delaunay correctness. |
| distance-compare(p, q, r) | Whether d(p,q) < d(p,r) without a square root. | Compare squared distances; exact with integer or rational arithmetic. |
| side-of-line(p, q, r) | Which side of line pq point r lies on. | Same sign as orientation; choose a consistent convention for the zero case. |
| point-in-polygon | Strictly inside, on boundary, or outside. | Ray-casting or winding number; special-case points on edges explicitly. |

Use a trusted library predicate (GEOS orientation, CGAL orientation_2) before writing your own.
Locate all epsilon decisions in one file or module; document the value and the reason.

## Exact vs floating arithmetic

- Double-precision floating point is correct when inputs are well-separated and coordinates are
  not extreme.
- Switch to exact arithmetic when: collinear or cocircular cases must be resolved correctly;
  coordinates are very large or involve many subtractions; or a wrong topological answer causes
  downstream failures.
- Libraries with embedded exact predicates: CGAL, Shewchuk's predicates (C), GEOS (internally).

## Epsilon pitfalls

- Additive epsilon (a == b +/- eps): fails at large coordinates; use relative epsilon instead.
- Relative epsilon (|a - b| / max(|a|, |b|) < eps): more robust but still fails near zero.
- Cascading comparisons: one epsilon decision that leaks into a second comparison produces
  inconsistent results. Centralize predicates to prevent this.
- Asymmetric results: orientation(p, q, r) may not equal -orientation(r, q, p) under floating
  point. Use consistent argument ordering throughout.

## Further reading

For robust predicate theory and adaptive exact arithmetic: Goodman Handbook ch.45 at
`references/local-only/Goodman-Handbook_of_discrete_and_computational_geometry_2018.md`;
grep `robust`, `floating point`, or `predicate`.
For orientation and in-circle implementation details: O'Rourke; grep `orientation`.
