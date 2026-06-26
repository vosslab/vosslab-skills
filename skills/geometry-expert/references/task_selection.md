# Task selection

Use this reference to classify a geometry request before consulting the topic index or algorithm guides.

## Task dimensions

Answer these questions to frame the task:

- Dimension: 2D (plane geometry, polygons, lines), 3D (meshes, volumes, solids), or nD (k-d trees,
  high-dimensional proximity).
- Primitive type: point, segment, ray, line, polygon, polyhedron, curve, or surface.
- Operation type: construction (build a structure: hull, triangulation, Voronoi diagram), query
  (answer a question: contains, nearest, intersects, locate), or transformation (clip, union,
  offset, simplify).
- Exactness: exact combinatorial answer (inside/outside, crossing yes/no) or approximate numeric
  result (distance, area, centroid).
- Dynamism: static (all input known upfront, batch processing) or dynamic/online (points arrive
  one at a time, support insertions/deletions).
- Scale: hundreds of points (any algorithm works), thousands (O(n log n) algorithms), millions
  (spatial indexes, streaming, or approximate methods).
- Interaction: batch (results computed offline) or interactive (latency budget under 50 ms per
  frame).

## Common task types

- Containment: point-in-polygon, point-in-convex-hull, inside/outside solid.
- Proximity: nearest neighbor, k-nearest neighbors, range search, closest pair.
- Intersection: segment/segment, polygon/polygon, ray/mesh, line/plane.
- Construction: convex hull, triangulation, Delaunay triangulation, Voronoi diagram.
- Boolean operations: polygon union, intersection, difference, clipping.
- Distance: point-to-segment, segment-to-segment, point-to-mesh, Hausdorff distance.
- Decomposition: triangulation, convex decomposition, arrangement of lines/segments.
- Spatial indexing: k-d tree, BVH, R-tree, grid hash for batch proximity or scene queries.
- Mesh operations: Delaunay mesh generation, remeshing, normal estimation, mesh repair.

## Clarifying questions to answer internally

- What dimension and primitive types are involved?
- Is the answer combinatorial (topology) or numeric (coordinates, distances)?
- How many geometric objects exist, and do they change at runtime?
- What is the failure mode: wrong topology, wrong numeric answer, slow query, or crash on
  degenerate input?
- Is a trusted library available for this language and platform?
- Does correctness require exact arithmetic, or is floating-point tolerance acceptable?
