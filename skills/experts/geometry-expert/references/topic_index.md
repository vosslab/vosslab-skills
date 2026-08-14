# Topic index

Start here after classifying the task. Match the problem to a row, then open the
named committed guide and the strongest local source. Book paths are bare text;
search the named conversion for the listed section title. Coverage evidence is
in [reference_survey.md](reference_survey.md).

## Problem routing table

| User problem or trigger | Branch and default route | Main risk or invariant | Primary local source |
| --- | --- | --- | --- |
| Segments cross incorrectly or are missed | Classical: robust pair predicate; sweep for many segments | Closed endpoints, overlap, collinearity, event ordering | `local-only/Computational_Geometry_Algorithms_and_Applications-2008.md`, `Line Segment Intersection` |
| Polygon clipping produces strange topology | Classical: GEOS or Boost.Geometry boolean/overlay | Validity, coincident edges, holes, touch-only results | `local-only/Computational_Geometry_in_C-1998.md`, `INTERSECTION OF CONVEX POLYGONS` |
| Hull is wrong or unstable | Classical: library hull or monotone chain | Duplicates, collinear boundary policy, orientation sign | `local-only/Computational_Geometry_Algorithms_and_Applications-2008.md`, `An Example: Convex Hulls` |
| Polygon triangulation has cracks | Classical: ear clipping, monotone partition, or library | Simple-polygon precondition, holes, collinear ears | `local-only/Computational_Geometry_in_C-1998.md`, `Triangulation by Ear Removal` |
| Delaunay fails on a grid or duplicates | Classical: Qhull/CGAL with explicit site policy | Cocircular non-uniqueness, duplicates, empty-circle invariant | `local-only/Handbook_of_Discrete_and_Computational_Geometry-2018.md`, `VORONOI DIAGRAMS AND DELAUNAY TRIANGULATIONS` |
| Need cells around sites | Classical: Voronoi construction/library | Unbounded cells, collinear sites, primal-dual consistency | `local-only/Computational_Geometry_Algorithms_and_Applications-2008.md`, `Voronoi Diagrams` |
| Boundary point classification changes | Classical: three-state point-in-polygon | Inside, boundary, and outside must remain distinct | `local-only/Discrete_and_Computational_Geometry-2025.md`, `POLYGONS` |
| Need repeated face lookup | Classical: point-location structure | Queries on edges/vertices and outside the subdivision | `local-only/Computational_Geometry_Algorithms_and_Applications-2008.md`, `Point Location and Trapezoidal Maps` |
| Range or nearest-neighbor query is slow | Classical: k-d tree, range tree, R-tree, or BVH by shape | Static vs dynamic, tie policy, dimensionality | `local-only/Computational_Geometry_An_Introduction-1985.md`, `Introduction to Geometric Searching` |
| Lines or segments form a subdivision | Combinatorial: arrangement and duality | Concurrent/parallel lines, cells, incidence consistency | `local-only/Algorithms_in_Combinatorial_Geometry-1987.md`, `Representing an Arrangement in Storage` |
| Mesh has poor triangles or gaps | Mesh: library generation plus quality checks | Conformity, boundary preservation, angles, slivers | `local-only/Handbook_of_Discrete_and_Computational_Geometry-2018.md`, `TRIANGULATIONS AND MESH GENERATION` |
| Convex objects need distance/collision tests | Classical 2D/3D: GJK or separating-axis test | Coplanar/grazing contact, support-map correctness | `local-only/Geometric_Tools_for_Computer_Graphics-2003.md`, `GJK Algorithm` |
| Predicate flips near degeneracy | Robust computation: exact or filtered sign predicate | Numeric error must not change combinatorial decisions | `local-only/Handbook_of_Discrete_and_Computational_Geometry-2018.md`, `ROBUST GEOMETRIC COMPUTATION` |
| Robot must avoid obstacles | Motion planning: configuration space and roadmap | Correct C-obstacles, degrees of freedom, path clearance | `local-only/Handbook_of_Discrete_and_Computational_Geometry-2018.md`, `ALGORITHMIC MOTION PLANNING` |
| Need a visibility graph or visible region | Visibility: library or classical graph construction | Occlusion, boundary contact, holes | `local-only/Computational_Geometry_Algorithms_and_Applications-2008.md`, `Visibility Graphs` |
| Need a conformal surface map | Conformal: discrete Ricci flow or proven parameterizer | Manifold/orientability assumptions, curvature target, triangle quality | `local-only/Conformal_Geometry_Computational_Algorithms_and_Engineering_Applications-2018.md`, `Discrete Surface Ricci Flow` |
| Need elimination or polynomial solution geometry | Algebraic: computer algebra system and Groebner basis | Base field, ideal vs variety, exact coefficients, term order | `local-only/A_First_Course_in_Computational_Algebraic_Geometry-2013.md`, `Ideal Membership` |
| Ask whether a graph/configuration is geometrically realizable | Discrete theory: ETR, arrangements, stretchability | Combinatorial type, coordinate precision, complexity class | `local-only/Courses_in_Discrete_and_Computational_Geometry-2026.md`, `Recognizing Segment Graphs` |

## Family defaults

### Predicates and topology

Centralize orientation, in-circle, side-of-line, containment, and equality
policy. Use tolerance for bounded measurement error and a filtered or exact
sign predicate for topology. See
[robustness_and_numerics.md](robustness_and_numerics.md).

### Polygon operations

Use a topology library for production boolean operations. State whether rings
are open or closed, winding conventions, hole semantics, and what happens to
lower-dimensional touch results. Characterize invalid inputs before repair.

### Hull, triangulation, Voronoi, and Delaunay

Use a trusted implementation unless teaching or constraints justify custom
code. Test hull containment, triangulation incidence and area, Delaunay
empty-circle behavior, and Voronoi-Delaunay dual consistency. Accept every
legal cocircular diagonal unless the contract specifies tie-breaking.

### Spatial queries

Choose by object type and updates: k-d trees for static points, range trees for
orthogonal theory, R-trees for rectangles and dynamic GIS data, BVHs for rays
and collision, and grids for bounded near-uniform workloads. The books support
classical theory; verify modern APIs in official documentation.

### Arrangements and realizability

Use incidence structures and Euler-style invariants for constructed
arrangements. For stretchability, segment graphs, or point-configuration
realizability, route to the theory branch instead of promising a routine
floating-point construction.

### Mesh and surface geometry

Separate mesh generation, mesh repair, and surface parameterization. Record
whether the mesh must be manifold, watertight, oriented, boundary-preserving,
or conformal, and validate the property actually required.

### Algebraic geometry

State the coefficient field, variables, monomial order, input ideals, and
desired output: membership, elimination, dimension, decomposition, or sample
solutions. Prefer a computer algebra system over handwritten Buchberger code
except for instruction.

### Visibility and motion planning

Model translation, rotation, and robot shape explicitly in configuration
space. A path through workspace that ignores C-obstacles is not a planning
solution. Validate the returned path continuously or with a conservative
collision checker.
