# Testing and oracles

Use this reference when building the fixture corpus and oracle comparisons for any geometry algorithm.

## Degenerate fixture corpus

Include at least these cases in the fixture corpus:
- Collinear points (all on one line, or k out of n on one line).
- Duplicate or coincident vertices.
- Near-duplicate points (coordinates differ by less than 1e-10).
- Near-overlapping or nearly-parallel segments.
- Self-intersecting polygon (figure-eight shape).
- Polygon with a zero-area spur (repeated edge traversed in both directions).
- Tiny triangles (area under 1e-20).
- Very large coordinates (values near floating-point range limits).
- Points exactly on an edge or vertex of another polygon.
- Empty input (zero points, zero segments).
- Single-point and two-point inputs.

## Oracles

Validate a custom algorithm against a trusted oracle before declaring it correct.

- Shapely/GEOS: polygon containment, intersection, union, difference, buffer, convex hull.
- scipy.spatial: Delaunay triangulation, Voronoi diagram, convex hull, k-d tree nearest neighbor.
- CGAL (via bindings or a separate program): exact predicates, constrained Delaunay, arrangement.
- Brute force on small random input: O(n^2) nearest neighbor, O(n^2) all-pairs intersection,
  O(n) point-in-polygon scan.

For brute-force oracles: generate 100-1000 random small inputs, run both implementations, and
assert agreement. Use a fixed seed for reproducibility.

## Property and stress invariants

Test these invariants in addition to exact-output comparisons:
- Convex hull: all input points lie inside or on the hull; hull vertices are a subset of input.
- Triangulation: all input vertices present; no crossing edges; Euler formula V - E + F = 2 for
  closed mesh.
- Nearest neighbor: result matches brute force on 500 random points.
- Polygon clipping: output polygon lies entirely inside the clip region.
- Orientation predicate: result is invariant under translation and uniform scaling.
- Area: non-negative after normalization; doubles under a 2x uniform scale.

## Inspectable artifacts

Generate at least one inspectable artifact when the algorithm produces geometric output:
- SVG file: 2D points, segments, polygons, and computed results (hull, triangulation edges,
  Voronoi cells).
- JSON dump: raw coordinates and computed structure (triangle vertex indices, nearest-neighbor
  IDs).
- OBJ or PLY file: 3D mesh output.
- Overlay image: input drawn with output to reveal boundary handling and degenerate-case
  treatment.

## Project locations

Place fixtures and artifacts in these standard locations:
- `tests/fixtures/geometry/` for fixture files (input/expected pairs, degenerate cases).
- `debug/geometry/` for temporary debug artifacts generated during development.
- `docs/images/` for artifacts included in project documentation.
