# Algorithm design

Choose a method only after [task_selection.md](task_selection.md) establishes
the branch, model, exactness, and workload.

## Decision order

1. Reuse a well-tested geometry library or computer algebra system whose model
   matches the contract.
2. Choose a classical or specialist method supported by a passage in
   [reference_survey.md](reference_survey.md).
3. Prototype against a brute-force, library, or theorem-derived oracle.
4. Write a custom production algorithm only when constraints justify its added
   robustness and maintenance burden.

## Classical algorithm families

| Task | Default route | Use custom work when |
| --- | --- | --- |
| Convex hull | Qhull/scipy, CGAL, or GEOS; monotone chain for small 2D code | Teaching, streaming, or a special boundary policy requires it |
| Polygon boolean/overlay | GEOS/Shapely or Boost.Geometry | The target curved/exact model needs a different kernel |
| Simple-polygon triangulation | Library, ear clipping, or monotone decomposition | Input promises and hole behavior are explicit and tested |
| Delaunay/Voronoi | Qhull/scipy or CGAL | Teaching or special metrics/constraints require it |
| Segment reporting | Brute force for small sets; Bentley-Ottmann style sweep for large sets | Event semantics and degeneracies can be fully specified |
| Point location | Triangulation, slab, or trapezoidal structure | A fixed subdivision receives enough queries to repay preprocessing |
| Range/proximity | k-d tree, range tree, R-tree, BVH, or grid by workload | A special distance or hardware layout dominates |
| Distance/collision | Library primitive tests, GJK, or separating axes | Support mappings and contact semantics are testable |
| Mesh generation | CGAL, Triangle, TetGen, or domain library | Boundary, conformity, and quality requirements are specialized |
| Visibility/planning | Visibility graph, cell decomposition, or roadmap library | Configuration-space assumptions and continuous collision checks are explicit |

Choose from representative benchmarks of dimension, distribution, updates, and
query counts; asymptotic complexity alone does not select the best structure.

## Specialized algorithm families

### Algebraic computation

Use a computer algebra system for standard/Groebner bases, ideal membership,
elimination, and polynomial-system work. Specify coefficient field and monomial
order because they change both method and output. Handwritten Buchberger code is
normally appropriate only for instruction or tightly bounded experimentation.

### Conformal surface processing

Select a method from the desired invariant: angle preservation,
parameterization, prescribed curvature, registration, or remeshing. Check mesh
manifoldness, orientation, boundary conditions, and triangle quality before
iteration. A numerically converged solve is not valid if the topological model
or discrete metric assumptions are violated.

### Realizability and discrete theory

For segment graphs, order types, stretchability, and point configurations,
first determine whether the request is a recognition or existence problem.
Coordinate search may require extreme precision or encode an ETR-hard problem;
treat failed floating-point optimization as an inconclusive search result rather
than a proof of non-realizability.

## Data-structure fit

- Static point queries: k-d tree or task-specific classical structure.
- Dynamic rectangles or GIS features: R-tree.
- Ray, collision, and scene queries: BVH.
- Bounded, roughly uniform neighborhoods: grid or spatial hash.
- Planar subdivision incidence: DCEL or equivalent half-edge structure.
- Surface topology: half-edge mesh with explicit manifold and boundary policy.
- Polynomial ideals: the computer algebra system's exact polynomial and ideal
  types, not floating arrays.

Verify current APIs and supported dimensions in official documentation. The
books establish concepts and failure modes, not version-specific calls.

## Reading routes

- Classical algorithms: `local-only/Computational_Geometry_Algorithms_and_Applications-2008.md`.
- Concrete predicates and polygon code: `local-only/Computational_Geometry_in_C-1998.md`.
- 2D/3D distance and intersection: `local-only/Geometric_Tools_for_Computer_Graphics-2003.md`.
- Robustness, meshes, and planning: `local-only/Handbook_of_Discrete_and_Computational_Geometry-2018.md`.
- Arrangements and duality: `local-only/Algorithms_in_Combinatorial_Geometry-1987.md`.
- Algebraic computation: `local-only/A_First_Course_in_Computational_Algebraic_Geometry-2013.md`.
- Conformal surfaces: `local-only/Conformal_Geometry_Computational_Algorithms_and_Engineering_Applications-2018.md`.
- Realizability and ETR: `local-only/Courses_in_Discrete_and_Computational_Geometry-2026.md`.
