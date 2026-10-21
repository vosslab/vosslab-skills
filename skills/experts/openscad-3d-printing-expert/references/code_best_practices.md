# Write maintainable OpenSCAD code

Use this guide when writing or reviewing `.scad` source. Language semantics come from the
[OpenSCAD language reference](https://files.openscad.org/documentation/manual/The_OpenSCAD_Language.html);
the organization and review rules below are engineering recommendations, not language requirements.

For assemblies, reusable part APIs, diagnostic sections, text layout, or generated source, also
read [extended_modeling.md](extended_modeling.md). It applies the book corpus to those workflows
and identifies source-conversion and historical-library pitfalls.

## Parameters and scope

- Organize a file as design inputs, derived dimensions, functions/modules, then one explicit
  top-level part or assembly selector. Preserve a project's existing naming and indentation style.
- Name dimensions by physical meaning: `shaft_diameter`, `wall_thickness`, `hole_pitch`,
  `clearance_radial`. Prefer `d=` or `r=` explicitly for cylinders and circles; state which a
  public parameter represents. Keep units consistent, usually millimeters and degrees.
- OpenSCAD trigonometric functions take degrees and inverse trigonometric functions return
  degrees. Convert only at an explicit boundary to a source that actually uses radians.
- Derive dependent dimensions once. Keep nominal mating dimensions, fit allowances, and Boolean
  overlap separate. A cutter epsilon is a numerical construction allowance, not a fit tolerance.
- Treat assignments as scoped bindings, not successive state updates. The last assignment in a
  scope can affect earlier uses in that scope. Use expressions, `let()`, functions, and list
  comprehensions rather than attempted accumulator updates inside loops.
- Pass reusable dimensions as module/function arguments. Avoid modules that silently depend on
  unrelated global variables. Use intentional special-variable settings such as `$fn` locally.
- Use `assert()` for actual geometric preconditions: positive thickness, holes staying within
  their material envelope, valid counts, and enough material around a recess. State the failed
  constraint in the message. Do not silently clamp an invalid design into a different part.
- Keep command-line override inputs at top level and derived values as expressions of those
  inputs. Exercise an override; successful parsing alone does not prove it changed the geometry.

## Modules and geometry ownership

- Use functions for values and modules for geometry. Give a module a meaningful physical job:
  a mounting hole, shell, rib, or printable part. Avoid one module per trivial transform unless
  it names a reusable placement or datum.
- Separate positive bodies from cutters. For multiple positive bodies, make their `union()`
  explicit as the first child of `difference()`; subsequent children are all subtractive.
- Prefer a 2D profile plus `linear_extrude()` for constant-section parts. Use `rotate_extrude()`
  for suitable rotational sections. Keep the input profile in its intended 2D plane; verify the
  axis and radial placement before producing the full solid.
- Keep reusable libraries free of unintended top-level output. Use `use <...>` for module and
  function definitions; use `include <...>` when top-level evaluation or library constants are
  needed. Follow a dependency's own loading instructions rather than substituting one for the other.
- Inventory library versions, fonts, imported SVG/DXF/STL files, and their resolution paths.
  Package required assets or document how to obtain them. Keep private absolute paths out of
  reusable source. Check imported dimensions against a known feature before modeling around them.

## Coordinate frames and transforms

- Document each part's local origin, mating datum, and axis convention. Choose `center=true`
  intentionally; mixing centered and corner-based primitives requires explicit offsets.
- Read nested transforms from the geometry outward. Translating after rotating is different
  from rotating a translation. Test a recognizable asymmetric feature when orientation is unclear.
- Keep an assembly placement separate from the part's print placement. A correctly assembled
  sloping part may need a different orientation to sit flat on the print bed.
- For repeated holes or ribs, derive positions from a pitch and datum. OpenSCAD ranges include
  their endpoint: an intended count normally needs indices from zero through count minus one.
  Guard zero/invalid counts explicitly instead of assuming an inverted range creates nothing.
- Derive angular repetition from the instance count. Check the seam for duplicated instances and
  inspect the first and last positions after changing count, pitch, or edge margins.

## Robust Boolean construction

- Extend through-cutters beyond both target faces. Pick a small overlap relative to the model's
  scale and nearby features; excessive overlap can remove an adjacent wall or hidden feature.
- Give intended connected components volumetric overlap where needed. Coincident faces and
  edge/point-only contact deserve explicit inspection; a preview is not a topology check.
- Model internal cavities so the intended floor and walls survive. Check the subtraction height
  and start plane independently rather than increasing a cutter until the preview looks right.
- Use `hull()` intentionally: it creates a convex envelope and can fill wanted recesses. For a
  constant-section rounded outline, a 2D construction followed by extrusion is often simpler than
  a 3D hull or Minkowski sum. Account for any rounding operation's change to the external envelope.
- Use `polyhedron()` only when simpler primitives or extrusion do not express the part clearly.
  Verify face winding against OpenSCAD's convention, planar faces or explicit triangulation,
  closed edges, and non-self-intersection. Render a minimal polyhedron before adding cutouts.

## Resolution and debugging

- Choose tessellation by the feature and required smoothness. Use modest preview resolution and
  an explicit export-quality setting; `$preview` may select quality but should not silently change
  functional dimensions or omit required production geometry.
- Reserve fixed `$fn` for intentional faceting or controlled resolution. With positive `$fn`,
  `$fa` and `$fs` do not choose the circle's fragment count. Scope expensive settings to the
  curved features that need them rather than making every repeated hole extremely dense.
- A low-sided inscribed circular hole can be narrower across its flats than its nominal diameter.
  Check effective clearance at export resolution before changing fit allowances.
- Use `echo()` for derived values and `#`, `%`, `!`, or `*` modifiers for isolated debugging.
  Restore the intended top-level output before export; highlighted/background previews are not
  evidence that every shown object belongs to the exported solid.
- Reduce a failing CSG tree to the responsible module. Inspect dimensions and transforms before
  adding resolution or wrapping everything in `render()`. `convexity` is a preview aid, not a
  repair for invalid geometry.

## Review checklist

- Can a reader find the user controls, units, datum, and selected output immediately?
- Does each module expose the dimensions it owns, with shared interfaces derived consistently?
- Do nominal and non-default parameters retain positive walls and correctly placed cutters?
- Are fit allowances distinct from Boolean overlap and tessellation error?
- Are imported assets and libraries available without the author's private directory layout?
- Does the exact exported mesh contain only the intended printable components?

Finish with [testing_and_oracles.md](testing_and_oracles.md). Report source review, render, mesh
inspection, slicer inspection, and physical fit checks separately; each proves a different claim.
