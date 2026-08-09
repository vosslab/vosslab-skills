# Local books

Use this reference to choose among the 12 Markdown conversions in `local-only/`
relative to the skill root. The files stay out of git. Paths below are bare text
on purpose: locate passages with `rg`, read the surrounding section, and use
[reference_survey.md](reference_survey.md) for passage-verified coverage.

## Core algorithm books

1. `local-only/Computational_Geometry_Algorithms_and_Applications-2008.md`
   is the default source for segment intersection, polygon triangulation, range
   searching, point location, Voronoi diagrams, Delaunay triangulations, motion
   planning, quadtrees, and visibility. Search `Line Segment Intersection`,
   `Point Location and Trapezoidal Maps`, or `Delaunay Triangulations`.
2. `local-only/Computational_Geometry_in_C-1998.md` is the implementation
   companion for signed area, segment intersection, ear removal, polygon
   intersection, point location, and visibility graphs. Search `SEGMENT
   INTERSECTION`, `Triangulation by Ear Removal`, or `INTERSECTION OF CONVEX
   POLYGONS`.
3. `local-only/Geometric_Tools_for_Computer_Graphics-2003.md` is the practical
   source for 2D and 3D distance and intersection recipes, GJK, separating-axis
   tests, and numerical pitfalls. Search `Issues of Numerical Computation`,
   `GJK Algorithm`, or `The Method of Separating Axes`.
4. `local-only/Handbook_of_Discrete_and_Computational_Geometry-2018.md` is the
   comprehensive source for hulls, arrangements, mesh generation, visibility,
   point location, intersection, robust computation, and motion planning.
   Search `ROBUST GEOMETRIC COMPUTATION`, `TRIANGULATIONS AND MESH GENERATION`,
   or `ALGORITHMIC MOTION PLANNING`.

## Foundations and teaching complements

5. `local-only/Computational_Geometry_An_Introduction-1985.md` develops the
   classical foundations of geometric searching, point location, hulls, and
   Voronoi methods. Search `Introduction to Geometric Searching`, `Convex Hull
   Algorithms in the Plane`, or `A catalog of Voronoi properties`.
6. `local-only/Algorithms_in_Combinatorial_Geometry-1987.md` is the strongest
   source for arrangements, zones, sweeping, duality, hulls, point location,
   and the hull-Delaunay connection. Search `Arrangements of Hyperplanes`,
   `Representing an Arrangement in Storage`, or `Delaunay Triangulations from
   Convex Hulls`.
7. `local-only/Discrete_and_Computational_Geometry-2025.md` is an approachable
   teaching source for polygons, triangulation, hulls, Delaunay edge flips,
   Voronoi geometry, and duality. Search `POLYGONS`, `DELAUNAY
   TRIANGULATIONS`, or `VORONOI GEOMETRY`.
8. `local-only/Computational_Geometry-2022.md` supplements point location,
   triangulation, and Voronoi diagrams with alternate explanations. Its broad
   conversion includes uneven and unrelated material, so use only the named
   sections and corroborate them. Search `POINT LOCATION IN O(LOG N)` or
   `VORONOI DIAGRAMS`.
9. `local-only/Introduction_to_Computational_Geometry-2024.md` connects segment
   intersection, spatial queries, map overlay, GIS, motion planning, and
   Voronoi/Delaunay applications. Treat it as an applications survey and pair
   algorithms or formulas with a core source. Search `Spatial Queries`, `Map
   Overlay`, or `TRANSLATIONAL MOTION PLANNING`.

These five overlap deliberately. Use them to clarify pedagogy or corroborate a
damaged conversion; select the one that best matches the current question.

## Specialized books

10. `local-only/A_First_Course_in_Computational_Algebraic_Geometry-2013.md`
    covers affine algebraic geometry, ideal membership, elimination, standard
    and Groebner bases, and Buchberger's algorithm. Search `Ideal Membership`,
    `Elimination`, or `Buchberger's Algorithm`. Route here only when the problem
    is polynomial or algebraic.
11. `local-only/Conformal_Geometry_Computational_Algorithms_and_Engineering_Applications-2018.md`
    covers discrete surface Ricci flow, global conformal parameterization, and
    centroidal Voronoi tessellation for surface processing. Search `Discrete
    Surface Ricci Flow`, `Global Conformal Parameterization`, or `Centroid
    Voronoi Tessellation`.
12. `local-only/Courses_in_Discrete_and_Computational_Geometry-2026.md` covers
    realizability, segment graphs, line arrangements, point configurations,
    stretchability, and the existential theory of the reals. Search
    `Recognizing Segment Graphs`, `Existential Theory of the Reals`, or
    `Arrangements and Stretchability`.

## Source boundary

- Start with one primary book and one corroborating book, not the whole corpus.
- Treat equations, code, and symbols in conversions as suspect until the
  surrounding definitions and a second source agree.
- Use current official documentation for library APIs, supported dimensions,
  exactness models, and version-specific behavior.
- If `local-only/` is absent, continue with the committed guides,
  first-principles reasoning, official documentation, and an oracle. Keep the
  private corpus optional at runtime.
