# Task selection

Classify a request before choosing an algorithm or opening a book.

## Choose the geometry branch

- Classical computational geometry: predicates, intersections, polygons,
  hulls, proximity, spatial queries, arrangements, meshes, visibility, or
  motion planning.
- Discrete and combinatorial geometry: incidence types, arrangements,
  realizability, stretchability, segment graphs, or complexity of geometric
  representations.
- Computational algebraic geometry: ideals, varieties, polynomial systems,
  Groebner bases, elimination, or exact symbolic coordinates.
- Conformal surface geometry: discrete curvature, Ricci flow, surface
  parameterization, registration, or intrinsic mesh metrics.

Route by the mathematical operation, not by a shared word. A Voronoi diagram on
the plane is classical; a centroidal Voronoi tessellation used during conformal
surface processing may need the conformal branch.

## Frame the input and output

Record:

- Dimension and ambient space: 2D, 3D, nD, surface-in-3D, projective, or
  algebraic.
- Primitives: points, segments, curves, polygons, polyhedra, meshes, graphs,
  equations, ideals, or parameterized surfaces.
- Operation: construct, query, transform, decide existence, optimize, or
  approximate.
- Answer type: numeric measurement, coordinates, combinatorial topology,
  symbolic object, Boolean decision, or path.
- Exactness: exact sign/topology, certified approximation, or ordinary numeric
  estimate.
- Input promises: simple polygon, manifold mesh, general position, exact
  coefficients, orientability, or none.
- Workload: object count, dimension, static vs dynamic, batch vs interactive,
  expected query count, and memory limit.

## Diagnose the failure class

- Wrong topology: a sign, incidence, winding, or degeneracy policy is unstable.
- Wrong numeric answer: units, frame, conditioning, or formula is wrong.
- Wrong model: align the algorithm's preconditions with the polygon, mesh,
  surface, field, or motion constraints.
- Slow query: align preprocessing and data structure with workload shape.
- Non-realizability or excessive precision: the task belongs to discrete theory,
  not routine coordinate construction.
- API failure: inspect the installed library and current official documentation.

## Decide whether custom code is justified

Prefer a trusted library or computer algebra system when topology or symbolic
correctness matters. Custom code is justified for teaching, an unsupported
primitive/model, a proven performance constraint, or a small independently
testable kernel. In every case, retain a brute-force, library, or theorem-based
oracle for small inputs.
