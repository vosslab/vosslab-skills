---
name: openscad-3d-printing-expert
description: Write and review parametric OpenSCAD for 3D printing.
---

# OpenSCAD 3D Printing Expert

## When to use

Use for writing, refactoring, debugging, or reviewing printable parametric OpenSCAD models.
Prioritize readable source, reliable geometry, and explicit dimensional intent. Use a slicer
for toolpaths and a measured test print for physical fit; source alone proves neither.

## Workflow

1. Read the target project before editing. Identify the OpenSCAD version, entry file, module boundaries, unit conventions, printer process, nozzle, material, build volume, and slicer when known. Classify the task with [references/task_selection.md](references/task_selection.md).
2. For an existing project, inventory the `.scad` files, parameters, imported geometry, export commands, and available tests; preserve unrelated work. For a greenfield model, define the part envelope, coordinate frame, functional interfaces, intended print orientation, and acceptance checks first. Follow [references/project_workflow.md](references/project_workflow.md).
3. Map the request to [references/topic_index.md](references/topic_index.md), then load the smallest relevant guide.
4. Before writing or reviewing source, read [references/code_best_practices.md](references/code_best_practices.md). Apply its parameter, scope, module, transform, Boolean, import, and debugging rules. Keep design inputs separate from construction modules and final assembly.
5. Design the geometry for its intended process and orientation using [references/print_design.md](references/print_design.md). Resolve wall, hole, fit, support, strength, and build-volume constraints from the actual printer, material, nozzle, and slicer; treat published rules of thumb as starting points, not guarantees.
6. Validate the source with the target OpenSCAD version, render exact geometry, export the requested mesh, and inspect it in a slicer or mesh checker. Test parameter extremes and mating fits when relevant. Use [references/testing_and_oracles.md](references/testing_and_oracles.md).
7. Report changed files, assumptions, export artifact, checks actually run, and any unresolved printability or fit uncertainty.

## Core rules

For multi-part assemblies, hidden interfaces, reusable libraries, text, or Python-generated
source, read [references/extended_modeling.md](references/extended_modeling.md). Establish a
low-detail assembled model before adding detail, and keep calibrated fits separate from scaling.

- Use module arguments for reusable geometry and functions for scalar or vector calculations. OpenSCAD variables bind expressions at compile time; treat them as immutable values rather than incrementing state.
- Keep a single units convention, normally millimeters. Name the coordinate frame, center or origin convention, and reference surfaces where they affect mating parts.
- Group related controls at the top of the file and pass dimensions explicitly. Use vectors for repeated dimensions and loops for genuinely repetitive geometry; keep generated instances easy to inspect.
- Prefer named arguments for built-ins when the meaning is not obvious. Use `$fn` for a deliberate fixed facet count, or `$fa`/`$fs` for scale-aware tessellation; use modest preview resolution and finer export resolution when geometry and runtime justify it.
- Make CSG order intentional: `difference()` subtracts every child after the first from the first child. Extend cutters beyond the target surface by a small, scale-aware epsilon so coplanar faces do not create ambiguous Boolean boundaries.
- Give unioned solids real overlap where needed; avoid parts that merely touch at a face, edge, or point. Build each printable component as a closed solid with no internal fragments or unintended disconnected shells.
- Use `F5` preview for iteration and `F6` render for exact geometry checks. A clean preview is not proof of a printable mesh.
- Choose orientation before finalizing support-sensitive features. Favor self-supporting chamfers, short bridges, accessible holes, and split parts when they reduce support damage or improve strength.
- Model wall thickness and clearances from the process: nozzle width, perimeter strategy, orientation, material shrinkage, calibration, and slicer settings all affect the result. Use small tolerance coupons for critical fits.
- Keep explanatory comments focused on intent, constraints, and non-obvious geometry. Remove stale alternatives and dead modules from deliverable code.

## Reference policy

Use current official OpenSCAD documentation for language and export behavior. Use printer or
slicer documentation and measured coupons for process limits. Consult
[references/local_books.md](references/local_books.md) for the local OpenSCAD and printing corpus,
and [references/reference_survey.md](references/reference_survey.md) for inspected passages and
limitations. Apply worked modeling techniques, not unverified copied code or universalized printer
settings. Background books inform requirements and scope rather than language semantics.

## Pitfalls and verification

- Keep nominal dimensions, fit clearance, and CSG epsilon separate; changing one to compensate
  for another hides the cause of failed fits or missing walls.
- Inspect exact exports rather than judging validity from preview color or appearance.
- Record the executable version, parameter overrides, warnings, and output artifact. If OpenSCAD
  or a slicer is unavailable, report that check as unperformed rather than claiming print readiness.
- Use [references/testing_and_oracles.md](references/testing_and_oracles.md) for the completion
  checklist; physical strength and fit remain unverified until the relevant real-world checks.