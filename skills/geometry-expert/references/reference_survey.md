# Reference survey

This is the committed coverage map for the 12 local-only book conversions in
`references/local-only/`. It is the source of truth for [topic_index.md](topic_index.md) and
[local_books.md](local_books.md). Each topic lists the books that cover it, the chapter to open,
reliable grep terms (validated against the conversions), and the coverage
strength. The books are flat text, so locate a passage by grepping the named
file for a listed term.

## How to use this survey

- Pick the topic, open the strongest book listed, and grep it for the term.
- When the survey marks coverage thin, treat the books as secondary and lean on
  the project guides, trusted-library docs, and brute-force or oracle testing.
- For implementation tasks, verify current library APIs from official docs or the
  installed package before writing API-level code. For conceptual planning, name
  the library and its role without API detail.

## Topic-to-reference map

### Convex hulls

Coverage: strong.

- `references/local-only/de_Berg-Computational_Geometry_Algorithms_and_Applications_2008.md` ch.11. grep `convex hull`.
- `references/local-only/O_Rourke-Computational_Geometry_in_C_1998.md` ch.3-4 (implementation and predicates). grep `convex hull`.
- `references/local-only/Preparata-Computational_Geometry_An_Introduction_1985.md` ch.3-4 (foundations, bounds). grep `convex hull`.
- `references/local-only/Edelsbrunner-Algorithms_in_Combinatorial_Geometry-1987.md` ch.8. grep `convex hull`.
- `references/local-only/Devadoss-Discrete_and_Computational_Geometry-2025.md` ch.2 (modern teaching). grep `convex hull`.
- `references/local-only/Kumar-Introduction_to_Computational_Geometry.md` ch.1 (intro). grep `convex hull`.

### Segment intersection and sweep line

Coverage: strong.

- `references/local-only/de_Berg-Computational_Geometry_Algorithms_and_Applications_2008.md` ch.2. grep `segment intersection`, `plane sweep`.
- `references/local-only/O_Rourke-Computational_Geometry_in_C_1998.md` ch.7. grep `segment intersection`.
- `references/local-only/Kumar-Introduction_to_Computational_Geometry.md` ch.3. grep `segment intersection`, `plane sweep`.

### Polygon triangulation

Coverage: strong.

- `references/local-only/de_Berg-Computational_Geometry_Algorithms_and_Applications_2008.md` ch.3. grep `triangulation`, `monotone`.
- `references/local-only/O_Rourke-Computational_Geometry_in_C_1998.md` ch.1. grep `triangulation`.
- `references/local-only/Devadoss-Discrete_and_Computational_Geometry-2025.md` ch.1,3. grep `triangulation`.

### Polygon boolean / clipping / overlay

Coverage: partial (de Berg on map overlay and boolean operations; Schneider on clipping). For production work, use Shapely/GEOS or Boost.Geometry.

- `references/local-only/de_Berg-Computational_Geometry_Algorithms_and_Applications_2008.md` ch.2 (map overlay, boolean operations on polygons via DCEL). grep `map overlay` (11 matches), `boolean` (11 matches).
- `references/local-only/Schneider-Geometric_Tools_for_Computer_Graphics-2003.md` ch.13 (polygon clipping). grep `clipping` (29 matches).
- `references/local-only/O_Rourke-Computational_Geometry_in_C_1998.md` (polygon intersection). grep `polygon intersection` (2 matches).
- For production boolean operations, Shapely/GEOS and Boost.Geometry are the primary tools; the books provide the underlying theory and classical algorithms.

### Voronoi and Delaunay

Coverage: strong.

- `references/local-only/de_Berg-Computational_Geometry_Algorithms_and_Applications_2008.md` ch.7,9. grep `voronoi`, `delaunay`.
- `references/local-only/O_Rourke-Computational_Geometry_in_C_1998.md` ch.5. grep `voronoi`.
- `references/local-only/Preparata-Computational_Geometry_An_Introduction_1985.md` ch.5-6. grep `voronoi`, `delaunay`.
- `references/local-only/Devadoss-Discrete_and_Computational_Geometry-2025.md` ch.3-4. grep `voronoi`, `delaunay`.
- `references/local-only/Edelsbrunner-Algorithms_in_Combinatorial_Geometry-1987.md` ch.13. grep `voronoi`, `delaunay`.

### Arrangements and duality

Coverage: strong.

- `references/local-only/de_Berg-Computational_Geometry_Algorithms_and_Applications_2008.md` ch.8. grep `arrangement`.
- `references/local-only/O_Rourke-Computational_Geometry_in_C_1998.md` ch.6. grep `arrangement`.
- `references/local-only/Edelsbrunner-Algorithms_in_Combinatorial_Geometry-1987.md` ch.1,5,7,9. grep `arrangement`, `duality`.

### Point location

Coverage: strong.

- `references/local-only/de_Berg-Computational_Geometry_Algorithms_and_Applications_2008.md` ch.6. grep `point location`, `trapezoidal`.
- `references/local-only/Preparata-Computational_Geometry_An_Introduction_1985.md` ch.2. grep `point location`.
- `references/local-only/Edelsbrunner-Algorithms_in_Combinatorial_Geometry-1987.md` ch.11. grep `point location`.
- `references/local-only/3GE_Collection_on_Mathematics.Computational_Geometry_2022.md` ch.6. grep `point location`.

### Range searching and k-d trees

Coverage: strong.

- `references/local-only/de_Berg-Computational_Geometry_Algorithms_and_Applications_2008.md` ch.5. grep `range search`, `kd-tree`.
- `references/local-only/Preparata-Computational_Geometry_An_Introduction_1985.md` ch.2. grep `range search`.
- `references/local-only/3GE_Collection_on_Mathematics.Computational_Geometry_2022.md` ch.5. grep `range search`.

### Mesh and 3D

Coverage: concentrated in Goodman; thin elsewhere.

- `references/local-only/Goodman-Handbook_of_discrete_and_computational_geometry_2018.md` ch.29 is best (Delaunay mesh, anisotropic). grep `mesh generation`, `anisotropic`.
- `references/local-only/de_Berg-Computational_Geometry_Algorithms_and_Applications_2008.md` ch.14 (quadtrees). grep `quadtree`.
- `references/local-only/Schneider-Geometric_Tools_for_Computer_Graphics-2003.md` ch.9-11 (3D primitives, distance, intersection). grep `mesh`, `intersection`.
- Coverage is thin outside Goodman; for mesh generation lean on Goodman ch.29
  plus current library docs.

### Robust predicates and exact arithmetic

Coverage: thin in books. Goodman ch.45 is the dedicated source; other books cover orientation and degeneracy briefly.

- `references/local-only/Goodman-Handbook_of_discrete_and_computational_geometry_2018.md` ch.45 is the dedicated robust-computation source. grep `robust`, `predicate`, `floating-point`.
- `references/local-only/de_Berg-Computational_Geometry_Algorithms_and_Applications_2008.md` ch.1 and `references/local-only/O_Rourke-Computational_Geometry_in_C_1998.md` discuss orientation and degeneracy.
- The literal phrase "in-circle" is sparse in the raw text. Carry the curated
  predicate summary in [robustness_and_numerics.md](robustness_and_numerics.md) and point to Goodman ch.45
  plus library predicates (CGAL exact kernels, Shewchuk predicates) rather than
  relying on book lookup.

### Distance and intersection recipes

Coverage: strong, practical (Schneider is the primary source).

- `references/local-only/Schneider-Geometric_Tools_for_Computer_Graphics-2003.md` ch.6,7,10,11 (point-to-X, GJK, separating axes). grep `distance`, `intersection`, `separating axis`.

### Modern spatial indexing and library APIs

Coverage: not covered by the books (they predate R-tree and BVH). Route to project guides and trusted-library docs.

- Not covered well by the books. Route to the project guides, trusted-library
  docs (Boost.Geometry R-tree, scipy.spatial, Shapely STRtree), and brute-force
  oracles. Treat the books as secondary support here.

## Weak-coverage decision (in scope, books secondary)

Mesh generation, robust predicates, R-tree/BVH spatial indexing, and current
library APIs stay in scope. For these, route to the project guides, trusted
library docs, brute-force oracles, and the curated summary in
[robustness_and_numerics.md](robustness_and_numerics.md), and treat the local books as secondary support.

## Routing tiers

- General intros, default routing: `references/local-only/Kumar-Introduction_to_Computational_Geometry.md`
  and `references/local-only/3GE_Collection_on_Mathematics.Computational_Geometry_2022.md`
  cover hulls, triangulation, segments, range search, point location, and Voronoi.
- Specialized, off the default path:
  `references/local-only/Decker-First_Course_in_Computational_Algebraic_Geometry_2013.md`
  (algebraic geometry, Groebner bases; grep `groebner`, `ideal`),
  `references/local-only/Jin-Conformal_Geometry-Computational_Algorithms_and_Engineering_Applications_2018.md`
  (conformal geometry, Ricci flow; grep `conformal`, `ricci flow`), and
  `references/local-only/Pach-Discrete_and_Computational_Geometry_2026.md`
  (advanced theory: graph product structure, existential theory of reals; grep
  `graph product`, `discrete geometry`). Route here only for algebraic,
  conformal, or advanced-theory tasks.
