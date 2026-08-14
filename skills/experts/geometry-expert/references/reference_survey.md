# Reference survey

This survey records what sampled passages in the 12 `local-only/` conversions
actually teach. It is the source of truth for [local_books.md](local_books.md)
and [topic_index.md](topic_index.md). Ratings mean:

- Strong: a dedicated section develops the method, model, or failure mode.
- Partial: a useful treatment appears inside a broader chapter.
- Thin: mentions or examples help only as corroboration.
- Not covered: use current official documentation or another primary source.

## How to use this survey

- Start with a strong source, search the exact section title, and read the
  surrounding passage before applying its method.
- Reference a book by its bare `local-only/` path plus the exact filename and
  listed section or grep term; keep the gitignored books out of Markdown links.
- Use partial and thin sources for teaching, applications, or corroboration.
- When `local-only/` is absent or coverage is thin, continue with the committed
  guides, current official documentation, first principles, and an independent
  oracle.

## Survey topic map

- [Classical algorithms](#classical-algorithms): robustness, hulls,
  intersections, polygons, Voronoi/Delaunay, spatial queries, arrangements,
  2D/3D queries, meshes, visibility, and planning.
- [Specialized branches](#specialized-branches): algebraic geometry, conformal
  surfaces, and realizability/ETR.
- [Applications and corroboration](#applications-and-corroboration): GIS and
  the overlapping teaching books.
- [Coverage gaps and fallback](#coverage-gaps-and-fallback): current APIs and
  topics that need external primary sources.

## Classical algorithms

### Framing, degeneracy, and numerical behavior

Coverage: strong.

- `local-only/Computational_Geometry_Algorithms_and_Applications-2008.md`,
  `1.1 An Example: Convex Hulls`, uses near-collinear hull decisions to show how
  rounding can make combinatorial results inconsistent.
- `local-only/Geometric_Tools_for_Computer_Graphics-2003.md`, `1.2 Issues of
  Numerical Computation`, develops nonassociativity, cancellation, tangency,
  and inconsistent Boolean outcomes.
- `local-only/Handbook_of_Discrete_and_Computational_Geometry-2018.md`, `45
  ROBUST GEOMETRIC COMPUTATION`, separates numerical and combinatorial
  correctness and develops exact, filtered, and soft-exact approaches.

### Convex hulls

Coverage: strong.

- `local-only/Computational_Geometry_Algorithms_and_Applications-2008.md`, `1.1
  An Example: Convex Hulls`, teaches the problem and robustness motivation.
- `local-only/Computational_Geometry_An_Introduction-1985.md`, `3.3 Convex Hull
  Algorithms in the Plane`, develops classical planar algorithms and bounds.
- `local-only/Algorithms_in_Combinatorial_Geometry-1987.md`, `8.1 Convex Hulls
  and Duality`, connects hulls with arrangements and duality.
- `local-only/Discrete_and_Computational_Geometry-2025.md`, chapter 2, is a
  modern teaching complement for planar and three-dimensional hulls.
- `local-only/Handbook_of_Discrete_and_Computational_Geometry-2018.md`, `26
  CONVEX HULL COMPUTATIONS`, is the broad reference.

### Segment intersection, sweep, and overlay

Coverage: strong for segment reporting; partial for production polygon boolean
operations.

- `local-only/Computational_Geometry_Algorithms_and_Applications-2008.md`, `2
  Line Segment Intersection`, develops the event queue, sweep status, closed
  segment semantics, degeneracies, output sensitivity, and map overlay.
- `local-only/Computational_Geometry_in_C-1998.md`, `1.5 SEGMENT INTERSECTION`
  and `7.2 SEGMENT-SEGMENT INTERSECTION`, supplies concrete predicates and code.
- `local-only/Introduction_to_Computational_Geometry-2024.md`, `3.2 LINE
  SEGMENT INTERSECTION` and `5.3.2 Map Overlay`, is a supporting application
  treatment.
- `local-only/Handbook_of_Discrete_and_Computational_Geometry-2018.md`, `42
  GEOMETRIC INTERSECTION`, provides the wider algorithmic context.

For production union, intersection, difference, and validity repair, use a
topology library such as GEOS or Boost.Geometry and verify its current API.

### Polygons, containment, and triangulation

Coverage: strong.

- `local-only/Computational_Geometry_in_C-1998.md`, `1.3 AREA OF POLYGON`, `1.6
  TRIANGULATION: IMPLEMENTATION`, and `Triangulation by Ear Removal`, gives
  executable geometric building blocks.
- `local-only/Computational_Geometry_Algorithms_and_Applications-2008.md`, `3
  Polygon Triangulation`, develops monotone partitioning and triangulation.
- `local-only/Discrete_and_Computational_Geometry-2025.md`, `1 POLYGONS`,
  teaches point-in-polygon, diagonals, ears, and why every simple polygon can be
  triangulated.
- `local-only/Computational_Geometry-2022.md`, sections on polygon
  triangulation, is an alternate teaching source.

### Voronoi diagrams and Delaunay triangulations

Coverage: strong.

- `local-only/Computational_Geometry_Algorithms_and_Applications-2008.md`, `7
  Voronoi Diagrams` and `9 Delaunay Triangulations`, is the default algorithm
  source.
- `local-only/Handbook_of_Discrete_and_Computational_Geometry-2018.md`, `27
  VORONOI DIAGRAMS AND DELAUNAY TRIANGULATIONS` and `29 TRIANGULATIONS AND MESH
  GENERATION`, covers empty-circle structure, cocircular non-uniqueness,
  constrained Delaunay, and quality meshes.
- `local-only/Discrete_and_Computational_Geometry-2025.md`, `3.4 DELAUNAY
  TRIANGULATIONS`, `4.1 VORONOI GEOMETRY`, and `4.3 REVISITING THE DELAUNAY
  TRIANGULATION`, teaches edge flipping, duality, and the general-position
  caveat.
- `local-only/Computational_Geometry_An_Introduction-1985.md`, `5.5.1 A catalog
  of Voronoi properties` through `5.6 Proximity Problems Solved by the Voronoi
  Diagram`, supplies classical foundations.
- `local-only/Algorithms_in_Combinatorial_Geometry-1987.md`, `13.1 Classical
  Voronoi Diagrams` and `13.2.3 Delaunay Triangulations from Convex Hulls`,
  emphasizes combinatorial structure.
- `local-only/Computational_Geometry-2022.md`, `VORONOI DIAGRAMS`, is a partial
  teaching complement, including higher-order diagrams.

### Point location, range searching, and spatial queries

Coverage: strong for classical static structures; not covered for current
R-tree, BVH, or library APIs.

- `local-only/Computational_Geometry_Algorithms_and_Applications-2008.md`, `5
  Orthogonal Range Searching` and `6.1 Point Location and Trapezoidal Maps`, is
  the default algorithm source.
- `local-only/Computational_Geometry_An_Introduction-1985.md`, `2.1
  Introduction to Geometric Searching` and `2.2 Point-Location Problems`,
  distinguishes query types and preprocessing, storage, and query tradeoffs.
- `local-only/Handbook_of_Discrete_and_Computational_Geometry-2018.md`, `38
  POINT LOCATION` and `40 RANGE SEARCHING`, gives broad reference coverage.
- `local-only/Algorithms_in_Combinatorial_Geometry-1987.md`, `11 Optimal point
  location search`, develops the arrangement-oriented view.
- `local-only/Computational_Geometry-2022.md`, `POINT LOCATION IN O(LOG N)`, is
  a partial teaching complement.
- `local-only/Introduction_to_Computational_Geometry-2024.md`, `5.3.1 Spatial
  Queries`, connects topology queries to point location and spatial indexes.

### Arrangements and duality

Coverage: strong.

- `local-only/Algorithms_in_Combinatorial_Geometry-1987.md`, `1.1 Arrangements
  of Hyperplanes`, `5.2 Sweeping a Simple Arrangement`, `7.1 Representing an
  Arrangement in Storage`, and `7.5 Incrementing the Arrangement`, is the
  primary source.
- `local-only/Handbook_of_Discrete_and_Computational_Geometry-2018.md`, `28
  ARRANGEMENTS`, is the broad reference.
- `local-only/Discrete_and_Computational_Geometry-2025.md`, `4.5 GEOMETRIC
  DUALITY`, is a concise teaching complement.

### Distance and intersection in 2D and 3D

Coverage: strong and practical.

- `local-only/Geometric_Tools_for_Computer_Graphics-2003.md`, `6 Distance in
  2D`, `7 Intersection in 2D`, `10 Distance in 3D`, and `11 Intersection in
  3D`, provides primitive recipes and explicit coplanar cases.
- Its `6.10 GJK Algorithm`, `10.12 GJK Algorithm`, and `The Method of Separating
  Axes` sections develop convex distance/overlap through Minkowski difference
  and separating axes.

### Mesh generation and quality

Coverage: strong in one comprehensive source; partial elsewhere.

- `local-only/Handbook_of_Discrete_and_Computational_Geometry-2018.md`, `29
  TRIANGULATIONS AND MESH GENERATION`, develops Delaunay, constrained and
  conforming triangulations, Steiner points, quality criteria, and 2D/3D mesh
  concerns.
- `local-only/Computational_Geometry_Algorithms_and_Applications-2008.md`, `14
  Quadtrees`, supports spatial decomposition but is not a mesh handbook.
- Use current CGAL, Triangle, TetGen, or target-library documentation for API
  and capability decisions.

### Visibility and motion planning

Coverage: strong.

- `local-only/Handbook_of_Discrete_and_Computational_Geometry-2018.md`, `33
  VISIBILITY` and `50 ALGORITHMIC MOTION PLANNING`, develops configuration
  space, free space, C-obstacles, arrangements, and roadmaps.
- `local-only/Computational_Geometry_Algorithms_and_Applications-2008.md`, `13
  Robot Motion Planning` and `15 Visibility Graphs`, is the default algorithm
  treatment.
- `local-only/Computational_Geometry_in_C-1998.md`, `8.2.2 Constructing the
  Visibility Graph` and `8.4.5 Conceptual Motion Planning Algorithm`, provides
  an implementation-oriented complement.
- `local-only/Introduction_to_Computational_Geometry-2024.md`, `6.5
  TRANSLATIONAL MOTION PLANNING` and `6.6 MOTION PLANNING WITH ROTATIONS`, is a
  partial applications source.

## Specialized branches

### Computational algebraic geometry

Coverage: strong in the specialist source.

- `local-only/A_First_Course_in_Computational_Algebraic_Geometry-2013.md`, `1.1
  Affine Algebraic Geometry`, `1.1.7 The Geometry of Elimination`, `2.2.1 Ideal
  Membership`, `2.2.2 Elimination`, and `2.5 Buchberger's Algorithm and Field
  Extensions`, develops standard/Groebner bases, normal forms, elimination, and
  computer algebra examples.

Route here when polynomial ideals, varieties, elimination, or symbolic
coordinates define the problem; keep ordinary polygon and mesh tasks on their
classical routes.

### Conformal surface geometry

Coverage: strong in the specialist source.

- `local-only/Conformal_Geometry_Computational_Algorithms_and_Engineering_Applications-2018.md`,
  `5.2 Discrete Surface Ricci Flow`, `6.2.1 Optimal Global Conformal
  Parametrization`, `6.2.2 Global Conformal Parameterization Using Discrete
  Euclidean Ricci Flow`, and `6.3.4 Computing Centroidal Voronoi Tessellations`,
  develops prescribed curvature, mesh metrics, remeshing, parameterization,
  registration, and surface tessellation.

### Realizability and discrete geometry theory

Coverage: strong in the specialist source.

- `local-only/Courses_in_Discrete_and_Computational_Geometry-2026.md`, `4.2
  Recognizing Segment Graphs and the Existential Theory of R`, `4.4.1 From
  Segment Graphs to Line Arrangements`, `4.4.2 From Line Arrangements to Point
  Configurations`, `5.2.1 A Brief Introduction to the Existential Theory of the
  Reals`, and `5.4.3.2 Arrangements and Stretchability`, develops
  realizability, precision, universality, and segment-intersection graphs.

## Applications and corroboration

Coverage: partial.

- `local-only/Introduction_to_Computational_Geometry-2024.md`, `1.5.3
  Geographic Information Systems (GIS)`, `5.3.1 Spatial Queries`, `5.3.2 Map
  Overlay`, and `7.2.4 Applications of Voronoi Diagrams and Delaunay
  Triangulations`, connects algorithms to GIS and engineering applications.
- `local-only/Discrete_and_Computational_Geometry-2025.md` and
  `local-only/Computational_Geometry-2022.md` are useful alternate teaching
  explanations. Keep the core sources primary for implementation.

## Coverage gaps and fallback

Current library APIs, R-tree/BVH implementation details, GPU geometry, modern
curved kernels, and deployment-specific behavior are not covered reliably by
this corpus. Use official documentation and inspect the installed version.
When `local-only/` is unavailable, use the committed guides, first principles,
and oracle tests; the skill must remain fully usable without the books.
