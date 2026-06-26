# Topic index

This is the routing front door. Start here, match the user problem to a row,
then open the named guide or local book. Book paths are bare text; grep the named
file for the listed keyword to find the passage. Derived from [reference_survey.md](reference_survey.md).

## Problem routing table

| User problem / trigger | Geometry task | Default algorithm or library | Robustness risks | Test fixtures | Best local book path |
| --- | --- | --- | --- | --- | --- |
| Segments cross incorrectly or missed | Segment intersection | Bentley-Ottmann sweep; Shapely for sets | Collinear, shared endpoints, vertical segments | Touching, overlapping, T-junction segments | `references/local-only/de_Berg-Computational_Geometry_Algorithms_and_Applications_2008.md` |
| Polygon clipping gives weird output | Polygon boolean / overlay | Shapely/GEOS; Boost.Geometry; Greiner-Hormann | Self-intersection, coincident edges, holes | Overlap, touch-only, hole-in-hole polygons | `references/local-only/Schneider-Geometric_Tools_for_Computer_Graphics-2003.md` |
| Convex hull wrong or unstable | Convex hull | scipy.spatial.ConvexHull; Andrew monotone chain | Collinear points, duplicates | Collinear runs, duplicate points, single point | `references/local-only/de_Berg-Computational_Geometry_Algorithms_and_Applications_2008.md` |
| Triangulation has cracks or missing vertices | Polygon triangulation | Ear clipping; monotone decomposition; CGAL | Holes, non-simple input, near-collinear ears | Non-convex, holes, collinear vertices | `references/local-only/O_Rourke-Computational_Geometry_in_C_1998.md` |
| Delaunay fails on duplicate points | Delaunay triangulation | scipy.spatial.Delaunay (Qhull); CGAL | Cocircular points, duplicates, near-degenerate | Cocircular sets, duplicate points, grid | `references/local-only/de_Berg-Computational_Geometry_Algorithms_and_Applications_2008.md` |
| Need cells around sites | Voronoi diagram | scipy.spatial.Voronoi; Fortune sweep | Cocircular sites, unbounded cells | Two sites, cocircular sites, collinear sites | `references/local-only/de_Berg-Computational_Geometry_Algorithms_and_Applications_2008.md` |
| Point on boundary classified inconsistently | Point-in-polygon / orientation | Winding or ray cast with one predicate | Points on edges/vertices, tolerance drift | On-edge, on-vertex, just-inside/outside points | `references/local-only/O_Rourke-Computational_Geometry_in_C_1998.md` |
| Which face contains this query point | Point location | Trapezoidal map; de Berg ch.6 | Points on edges, slab boundaries | Query on edge, on vertex, outside arrangement | `references/local-only/de_Berg-Computational_Geometry_Algorithms_and_Applications_2008.md` |
| Nearest neighbor is slow | Proximity / NN search | scipy.spatial.cKDTree; Boost.Geometry R-tree | Ties, duplicate coordinates, high dimension | Clustered points, duplicates, uniform random | `references/local-only/de_Berg-Computational_Geometry_Algorithms_and_Applications_2008.md` |
| Range or window query is slow | Range searching | k-d tree; range tree; R-tree | Empty ranges, boundary-inclusive queries | Empty window, edge-touching window, dense set | `references/local-only/de_Berg-Computational_Geometry_Algorithms_and_Applications_2008.md` |
| Many lines/segments form a subdivision | Arrangement / duality | Incremental arrangement; CGAL Arrangement_2 | Concurrent lines, parallel lines | Concurrent lines, parallel lines, duplicates | `references/local-only/Edelsbrunner-Algorithms_in_Combinatorial_Geometry-1987.md` |
| Mesh has cracks or bad triangles | Mesh generation / quality | CGAL mesh; Goodman ch.29; Triangle | Sliver triangles, non-conforming edges | Sliver triangles, T-junctions, boundary gaps | `references/local-only/Goodman-Handbook_of_discrete_and_computational_geometry_2018.md` |
| 3D intersections numerically unstable | Distance / intersection query | Separating axis; GJK; Schneider recipes | Near-parallel faces, grazing contact | Coplanar faces, edge-edge touch, grazing hit | `references/local-only/Schneider-Geometric_Tools_for_Computer_Graphics-2003.md` |
| Predicate flips sign near degeneracy | Robust predicates | Exact/filtered orientation, in-circle | Floating-point rounding, large coordinates | Near-collinear, near-cocircular, large coords | `references/local-only/Goodman-Handbook_of_discrete_and_computational_geometry_2018.md` |

## Per-family detail

### Predicates and robustness

Centralize orientation, in-circle, and distance-compare in one module. Reach for
exact or filtered predicates (CGAL exact kernels, Shewchuk adaptive predicates)
when coordinates are large or inputs near-degenerate. See
[robustness_and_numerics.md](robustness_and_numerics.md). Oracle: orientation is invariant under translation
and uniform scaling; a sign that flips under translation signals a precision bug.
Book: `references/local-only/Goodman-Handbook_of_discrete_and_computational_geometry_2018.md` (grep `robust`, `predicate`).

### Convex hulls

Default to scipy.spatial.ConvexHull (Qhull) or Andrew monotone chain for 2D.
Handle collinear points and duplicates explicitly. Oracle: brute-force gift
wrapping on small random sets. Book:
`references/local-only/de_Berg-Computational_Geometry_Algorithms_and_Applications_2008.md` (grep `convex hull`).

### Segment intersection and sweep line

Use Bentley-Ottmann for many segments, a single robust segment-segment test for
pairs. Handle collinear overlap and shared endpoints. Oracle: brute-force O(n^2)
pair test on small sets. Books:
`references/local-only/de_Berg-Computational_Geometry_Algorithms_and_Applications_2008.md` (grep `plane sweep`),
`references/local-only/O_Rourke-Computational_Geometry_in_C_1998.md` (grep `segment intersection`).

### Polygon operations

Use Shapely/GEOS or Boost.Geometry for boolean union, intersection, difference,
and overlay. Validate input simplicity first. Oracle: Shapely/GEOS on fixtures.
Books: `references/local-only/Schneider-Geometric_Tools_for_Computer_Graphics-2003.md` (grep `clipping`),
`references/local-only/O_Rourke-Computational_Geometry_in_C_1998.md` (grep `polygon intersection`).

### Triangulation, Delaunay, Voronoi

Use ear clipping or monotone decomposition for simple-polygon triangulation, and
scipy.spatial (Qhull) or CGAL for Delaunay and Voronoi. Handle cocircular and
duplicate points. Oracle: empty-circle test for Delaunay; vertex-preservation
and Euler counts for triangulation. Books:
`references/local-only/de_Berg-Computational_Geometry_Algorithms_and_Applications_2008.md` (grep `delaunay`),
`references/local-only/Devadoss-Discrete_and_Computational_Geometry-2025.md` (grep `voronoi`).

### Point location

Build a trapezoidal map or slab decomposition. Handle queries exactly on edges
and vertices. Oracle: brute-force face containment on small subdivisions. Book:
`references/local-only/de_Berg-Computational_Geometry_Algorithms_and_Applications_2008.md` (grep `trapezoidal`).

### Nearest-neighbor and spatial indexes

Use scipy.spatial.cKDTree for static point sets, Boost.Geometry or an R-tree for
dynamic or rectangle data, a BVH for ray and collision queries. Oracle:
brute-force nearest neighbor on small random data. Books:
`references/local-only/de_Berg-Computational_Geometry_Algorithms_and_Applications_2008.md` (grep `kd-tree`).
R-tree/BVH detail comes from library docs; the books predate them.

### Arrangements

Build arrangements incrementally or with CGAL Arrangement_2. Handle concurrent
and parallel lines. Oracle: Euler formula on the resulting subdivision. Book:
`references/local-only/Edelsbrunner-Algorithms_in_Combinatorial_Geometry-1987.md` (grep `arrangement`).

### Mesh and 3D geometry

Use CGAL meshing or Triangle for 2D quality meshes; lean on Goodman ch.29 plus
current library docs for mesh generation and anisotropic meshing. Oracle:
conformance and quality metrics (no slivers, watertight boundary). Books:
`references/local-only/Goodman-Handbook_of_discrete_and_computational_geometry_2018.md` (grep `mesh generation`),
`references/local-only/de_Berg-Computational_Geometry_Algorithms_and_Applications_2008.md` (grep `quadtree`).

### Distance and intersection queries

Use Schneider recipes for point-to-X distance, GJK for convex overlap, and
separating-axis tests for boxes and polytopes. Handle coplanar and grazing
contact. Oracle: brute-force sampled distance on small inputs. Book:
`references/local-only/Schneider-Geometric_Tools_for_Computer_Graphics-2003.md` (grep `distance`, `separating axis`).

## Alias and trigger vocabulary

- Polygon boolean: clipping, overlay, union, intersection, difference, dissolve.
- Spatial index: k-d tree, R-tree, BVH, quadtree, nearest neighbor, range query.
- Orientation test: ccw, signed area, winding, point-in-polygon, side-of-line.
- Degeneracy: collinear, coincident, cocircular, coplanar, duplicate points.
- Triangulation: constrained, conforming, Delaunay, Voronoi, monotone, ear clip.

## Book source map (which book for this problem)

- Sweep line and Voronoi: `references/local-only/de_Berg-Computational_Geometry_Algorithms_and_Applications_2008.md` (grep `plane sweep`, `voronoi`).
- Implementation details and predicates: `references/local-only/O_Rourke-Computational_Geometry_in_C_1998.md` (grep `convex hull`).
- Intersection and distance recipes: `references/local-only/Schneider-Geometric_Tools_for_Computer_Graphics-2003.md` (grep `distance`).
- Mesh generation and robust computation: `references/local-only/Goodman-Handbook_of_discrete_and_computational_geometry_2018.md` (grep `mesh generation`, `robust`).
- Foundations and bounds: `references/local-only/Preparata-Computational_Geometry_An_Introduction_1985.md` (grep `voronoi`), `references/local-only/Edelsbrunner-Algorithms_in_Combinatorial_Geometry-1987.md` (grep `arrangement`).
- Modern teaching: `references/local-only/Devadoss-Discrete_and_Computational_Geometry-2025.md` (grep `triangulation`).
- General intro: `references/local-only/Kumar-Introduction_to_Computational_Geometry.md` (grep `convex hull`), `references/local-only/3GE_Collection_on_Mathematics.Computational_Geometry_2022.md` (grep `voronoi`).
- Where coverage is thin (mesh, robust predicates, R-tree/BVH, library APIs),
  route to the project guides and trusted-library docs instead.

## New project by shape (greenfield routing)

- Polygon clipping / CAD-like tool: kernel Shapely/GEOS (Python) or
  Boost.Geometry (C++). First fixture: two overlapping rectangles plus one
  touch-only pair, with expected union and intersection areas.
- Mesh processing: kernel CGAL or Triangle. First fixture: a square-with-hole
  domain meshed to a quality bound, checked for slivers and a watertight boundary.
- Nearest-neighbor / spatial search: kernel scipy.spatial.cKDTree or an R-tree.
  First fixture: 100 random points with brute-force nearest-neighbor answers.
- CG teaching / demo app: kernel a small custom 2D module over de Berg
  algorithms. First fixture: a convex hull on collinear-heavy points with the
  expected hull vertices.
- GIS / topology-heavy project: kernel Shapely/GEOS with valid-geometry checks.
  First fixture: a self-touching polygon and its repaired, validated result.
- 3D intersection/distance engine: kernel Schneider recipes plus GJK. First
  fixture: two boxes in touch, overlap, and separated poses with expected
  distance and overlap flags.
