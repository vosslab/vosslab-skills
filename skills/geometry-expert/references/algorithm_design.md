# Algorithm design

Use this reference when choosing an algorithm after classifying the geometric task.

## Default decision order

1. Reuse a well-tested library (scipy.spatial, Shapely/GEOS, CGAL, Boost.Geometry). Libraries handle
   degenerate inputs and edge cases that custom code misses.
2. Apply a classical algorithm from the literature (sweep line, divide and conquer, randomized
   incremental). Use the local books for implementation details; see the reading map below.
3. Build a custom algorithm only when library APIs or classical methods do not meet the constraints.

## Algorithm families and when each fits

| Family | Default choice | Use when |
| --- | --- | --- |
| Convex hull | scipy.spatial.ConvexHull or CGAL | Boundary needed for containment, compression, or preprocessing. |
| Polygon boolean ops | Shapely/GEOS | Union, intersection, difference, clipping, buffering. |
| Triangulation | scipy.spatial.Delaunay or CGAL | Mesh generation, area decomposition, interpolation. |
| Voronoi diagram | scipy.spatial.Voronoi | Nearest-region queries, proximity partitioning, mesh dual. |
| Nearest neighbor | scipy.spatial.cKDTree | Static point sets; batch or single queries. |
| Spatial index (dynamic) | R-tree (rtree library) or BVH | Insertions/deletions at runtime; bounding-box queries. |
| Segment intersection | Sweep line (Shamos-Hoey or Bentley-Ottmann) | All-pairs or reporting crossings in large segment sets. |
| Point location | Trapezoidal decomposition or triangulation | Repeated containment queries over a fixed arrangement. |
| Range search | k-d tree or range tree | k-NN or orthogonal range queries on static point sets. |
| Distance queries | Schneider recipes | Point-to-segment, segment-to-segment, GJK, separating axes. |
| Mesh generation | CGAL or library + Goodman ch.29 | Quality triangular or tetrahedral mesh from a boundary. |

## Complexity and input size

- Under 10,000 points: brute force, O(n log n) classical, or any library call is fine.
- 10,000 to 1,000,000 points: use O(n log n) algorithms or library data structures.
- Over 1,000,000 points: require spatial indexes, streaming, or approximate methods.
- Interactive (latency under 50 ms): precompute a spatial index once and reuse it per frame.
- Dynamic updates (insertions/deletions): prefer R-tree or BVH over k-d tree (static).

## Reading map

Consult [reference_survey.md](reference_survey.md) for the full topic-to-book map with grep keywords
and located chapters. Quick routing:
- Sweep line, Voronoi, point location: de Berg.
- Implementation details and predicate code: O'Rourke.
- Intersection and distance recipes: Schneider.
- Mesh generation and robust computation: Goodman ch.29 and ch.45.
- Foundations and combinatorial bounds: Preparata, Edelsbrunner.
- Modern teaching coverage: Devadoss, Kumar, 3GE.
