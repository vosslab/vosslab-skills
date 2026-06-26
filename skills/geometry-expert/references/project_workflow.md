# Project workflow

Use this reference when the skill is invoked on a target project, not while building geometry-expert.

## Detect project state

Inspect the target repo before writing geometry code:
- Search for geometry source files (primitives, predicates, algorithm implementations).
- Search for geometry tests and fixtures.
- Search for architecture docs that describe a coordinate system, tolerance, or geometry model.

If any of these exist, follow the existing-project path. If none exist, follow the greenfield path.

## Geometry contract

Both paths write and maintain a geometry contract. Use the target repo's existing docs location when
present; otherwise create `docs/GEOMETRY_MODEL.md`. The contract records:
- Coordinate frame and axis directions; units (meters, pixels, normalized).
- 2D vs 3D (or both); primitive types in use.
- Polygon openness convention (open or closed; first vertex repeated or not).
- Winding order (clockwise or counterclockwise for positive area).
- Tolerance policy: one location, one value, documented reason.
- Valid and invalid input definitions.
- Expected degeneracy behavior (collinear points, duplicate vertices, zero-area polygons).

## Existing project path

1. Build a geometry inventory: list files owning primitives, predicates, algorithms,
   serialization/import, rendering/debug output, and tests.
2. Update the geometry contract from the inventory; fill in any gaps.
3. Write characterization tests around current behavior before changing any algorithm
   (migration safety). Investigation and instrumentation are free before this step.
4. Build or extend the fixture corpus (degenerate and representative cases).
5. Make algorithm changes tied to failing fixtures, one change at a time.

## Greenfield path

1. Write the geometry contract first as the design source of truth.
2. Choose the geometry library against explicit criteria:
   - Language ecosystem and packaging.
   - Exactness needs (floating-point tolerance acceptable, or exact arithmetic required).
   - Topology support (2D polygon booleans, 3D mesh, or higher).
   - Licensing and deployment constraints.
   - Performance at expected input size.
   - Candidates: Shapely/GEOS (Python 2D polygon ops), CGAL (C++ exact 2D/3D),
     scipy.spatial (Delaunay/Voronoi/kd-tree), Boost.Geometry (C++ 2D), custom.
3. State early performance assumptions: input size (hundreds vs millions), interactive vs batch,
   static vs dynamic structure, exactness or tolerance-based.
4. Seed a fixture corpus: happy-path, boundary, degenerate, and small random cases with
   oracle-verified expected outputs.
5. Build the minimal geometry kernel milestone. The kernel is complete only when all of these pass:
   primitives defined and constructed; predicates implemented and tested; fixture loading working;
   oracle comparison tests passing; one debug artifact (SVG, JSON dump, or coordinate printout)
   generated.
6. Build feature algorithms on top of the validated kernel.

## Geometry review checklist

Before closing any geometry task, verify:
- Coordinate system is documented in the contract.
- Degeneracy cases are exercised in fixtures.
- Tolerance policy is explicit: one location, one value, documented reason.
- Predicates are centralized (no scattered epsilons).
- Oracle or brute-force comparison is present for the core algorithm.
- At least one inspectable artifact is generated.
- Performance is tested at expected input size, not just on tiny examples.
