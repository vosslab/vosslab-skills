# Project workflow

Use this guide on a target project after the task has been classified.

## Build an evidence inventory

Inspect source, tests, fixtures, data import/export, visualization, and existing
documentation. Identify who owns:

- Coordinate frames, units, primitives, meshes, equations, and serialization.
- Predicates, topology, tolerance/exactness, and normalization.
- Algorithms, spatial structures, solvers, and external libraries.
- Rendering/debug artifacts and user-visible error handling.

Treat existing behavior and a dirty tree as user-owned evidence. Characterize
it before changing an algorithm.

## Write the geometry contract

Use an existing canonical document when present; otherwise create
`docs/GEOMETRY_MODEL.md` if the target repository permits it. Record only the
fields relevant to the branch:

- Ambient space, axes, units, dimension, and transformations.
- Primitive and topology conventions: open/closed rings, winding, holes,
  manifoldness, boundary, incidence, and empty/lower-dimensional results.
- Exactness and tolerance policy, including who owns predicates.
- Valid input promises and explicit rejection/normalization behavior.
- Scale, update/query workload, latency, and memory expectations.
- Algebraic field, variables, monomial order, and symbolic output when relevant.
- Surface topology, curvature/boundary conditions, and distortion goals for
  conformal work.
- Robot degrees of freedom, obstacle model, and clearance/contact semantics for
  planning.

## Existing-project path

1. Trace one representative input through parsing, model, computation, output,
   and rendering.
2. Reconcile the contract with current behavior and document unknowns.
3. Add characterization tests around behavior that a change might affect.
4. Add the smallest degenerate and representative oracle cases.
5. Make one bounded change tied to one failing case.
6. Re-run invariants, artifacts, and representative performance checks.

## Greenfield path

1. Write the contract before choosing permanent data structures.
2. Compare candidate libraries on model fit, exactness, topology, dimensions,
   license, packaging, performance, and deployment.
3. Create hand-checkable, boundary, degenerate, and fixed-seed oracle cases.
4. Build the smallest kernel: primitives/model, centralized predicates or
   symbolic types, fixture loading, oracle comparison, and one artifact.
5. Add one feature family at a time and preserve the kernel invariants.

## Review checklist

- The geometry branch and mathematical model are explicit.
- Coordinate, topology, and exactness conventions have one owner.
- Preconditions are validated or clearly delegated to a trusted library.
- Degenerate cases and multiple legal outputs are tested correctly.
- The oracle is independent and small random cases are reproducible.
- At least one artifact makes boundary/topology behavior inspectable.
- Performance evidence matches expected scale and workload shape.
- Current library behavior comes from official docs or installed-version
  inspection; book conversions supply concepts and judgment.
- Limitations and unsupported inputs are stated plainly.
