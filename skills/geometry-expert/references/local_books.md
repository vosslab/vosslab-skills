# Local books

Use this reference to pick the right local-only book for a geometry task. The 12
converted books live in `references/local-only/` and stay out of git. Load them
by bare path text at runtime and grep the named file for a keyword. The detailed
coverage map lives in [reference_survey.md](reference_survey.md).

## Reading order (strongest first for algorithm work)

1. `references/local-only/de_Berg-Computational_Geometry_Algorithms_and_Applications_2008.md`
   Best for the core algorithms taught clearly: plane sweep, segment
   intersection, polygon triangulation, Voronoi, Delaunay, point location,
   range searching, and arrangements. Start here. grep `plane sweep`, `voronoi`.
2. `references/local-only/O_Rourke-Computational_Geometry_in_C_1998.md`
   Best for concrete implementation, orientation predicates, and code-level
   detail on hulls, triangulation, and segment intersection. grep `convex hull`.
3. `references/local-only/Schneider-Geometric_Tools_for_Computer_Graphics-2003.md`
   Best for practical distance, intersection, and primitive recipes, including
   GJK and separating-axis tests in 2D and 3D. grep `distance`, `intersection`.
4. `references/local-only/Goodman-Handbook_of_discrete_and_computational_geometry_2018.md`
   Best as a comprehensive reference for lookups, including mesh generation
   (ch.29) and robust computation (ch.45). grep `mesh generation`, `robust`.
5. `references/local-only/Preparata-Computational_Geometry_An_Introduction_1985.md`
   Best for foundations and combinatorial bounds on hulls, Voronoi, point
   location, and range searching. grep `convex hull`, `voronoi`.
6. `references/local-only/Edelsbrunner-Algorithms_in_Combinatorial_Geometry-1987.md`
   Best for arrangements, duality, and combinatorial geometry depth. grep
   `arrangement`, `duality`.
7. `references/local-only/Devadoss-Discrete_and_Computational_Geometry-2025.md`
   Best for modern teaching of triangulation, Voronoi, and Delaunay. grep
   `triangulation`, `voronoi`.
8. `references/local-only/Kumar-Introduction_to_Computational_Geometry.md`
   Best as a general intro to hulls, segments, and triangulation. grep `convex
   hull`, `segment intersection`.
9. `references/local-only/3GE_Collection_on_Mathematics.Computational_Geometry_2022.md`
   Best as a general intro and collection covering point location, range search,
   and Voronoi. grep `point location`, `voronoi`.

## Specialized books (off the default path)

- `references/local-only/Pach-Discrete_and_Computational_Geometry_2026.md`
  Advanced theory: graph product structure and existential theory of reals.
  Use only for advanced-theory tasks. grep `graph product`, `discrete geometry`.
- `references/local-only/Decker-First_Course_in_Computational_Algebraic_Geometry_2013.md`
  Algebraic geometry and Groebner bases. Use only for algebraic-geometry tasks.
  grep `groebner`, `ideal`.
- `references/local-only/Jin-Conformal_Geometry-Computational_Algorithms_and_Engineering_Applications_2018.md`
  Conformal geometry and Ricci flow. Use only for conformal-mapping or
  surface-parameterization tasks. grep `conformal`, `ricci flow`.

## Practical mapping

- For the core algorithms, start with de Berg, then O'Rourke for implementation.
- For distance and intersection code, read Schneider.
- For mesh generation and robust computation, read Goodman (ch.29, ch.45).
- For foundations and bounds, read Preparata and Edelsbrunner.
- For algebraic or conformal tasks only, read Decker or Jin.
- Where the survey marks coverage thin (mesh, robust predicates, R-tree/BVH,
  current library APIs), lean on the project guides and trusted-library docs.
