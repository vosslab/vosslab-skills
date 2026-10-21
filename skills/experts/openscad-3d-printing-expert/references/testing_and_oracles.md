# Validate OpenSCAD models

## Source and render checks

1. Query the installed version and its CLI help. OpenSCAD export flags change over time; use options supported by the target installation.
2. Run a syntax/CSG evaluation, then an exact render and mesh export. A typical CLI form is `openscad --hardwarnings -o output.stl model.scad`; confirm this form with `openscad --help` because packaged versions may differ.
3. Treat warnings as findings to inspect. Resolve undefined values, empty geometry, unsupported operations, and Boolean failures at their source.
4. Record the exact parameter overrides and export command so another person can reproduce the mesh.

## Geometry checks

- Confirm exact rendered geometry is non-empty and fits the stated envelope.
- Inspect the exported mesh in a slicer or mesh checker. Confirm expected scale, orientation, closed/manifold solid, no unintended disconnected fragments, and no missing features.
- Inspect critical walls, holes, slots, and thin features in the slicer preview at the selected nozzle and perimeter settings. A mathematically valid solid can still slice poorly.
- Check each mating pair in assembled and separated views. Test motion, insertion, and retention requirements; use a fit coupon for critical interfaces.
- Check support contact, bridge lengths, overhangs, build-plate contact, and expected strength direction at the intended print orientation.
- Exercise meaningful parameter bounds and at least one non-default configuration. Confirm derived dimensions stay valid and subtractive cutters continue through their intended surfaces.

## Conditional checks

- For an assembly/print selector, export each intended part and verify bed placement, expected
  component count, and shared interfaces. Remove diagnostic section cuts from production output.
- After resizing a model, recheck calibrated gaps, hardware interfaces, and minimum walls.
  Uniform scaling is not a fit-preservation guarantee.
- For generated source, retain the input-to-output mapping and exercise distinct variants to
  detect leaked generator state. Compare native and wrapper units before blaming the mesh exporter.
- Reconstructed book listings need actual source evaluation and exact export before reuse.
  Markdown callouts or damaged formulas cannot serve as a passing test oracle.

## Reproducible examples

Run these commands through the terminal tool from the model's project directory. Use a fresh
output path for each configuration so an old mesh cannot be mistaken for a successful new export.
Check both the exit status and diagnostic output, then inspect the newly produced file.

Render/export a single part:

```sh
openscad --hardwarnings -o output.stl model.scad
```

Override a documented parameter when the installed version supports `-D`:

```sh
openscad --hardwarnings -D 'wall=2.4' -o output.stl model.scad
```

Use `openscad --help` and the installed manual as authority for option spelling and availability. Do not claim a mesh or print check passed unless that command actually ran and its output was inspected.

For a string selector on a POSIX shell, preserve the OpenSCAD string quotes inside the override:
`openscad --hardwarnings -D 'part="base"' -o base.stl model.scad`.
Adapt quoting to the actual shell; `part` must be a parameter the source actually exposes.

STL carries no unit metadata; verify the slicer's interpretation against a known dimension.
Treat STL as geometry-only, not a record of preview colors, materials, or assembled part intent.
Report separately: source evaluation, exact export, mesh checks, slicer checks, and physical
coupon/print checks. A successful export does not establish strength, clearance, or slice quality.

## Failure diagnosis

- **Preview looks wrong, exact render looks right:** preview/OpenCSG artifact; judge exported geometry from exact render and slicer.
- **Exact render reports a Boolean problem:** reduce to the smallest failing module; check tangent or coplanar surfaces, non-overlapping joins, degenerate dimensions, and cutter extent.
- **Mesh export succeeds but slicer rejects or repairs it:** inspect manifoldness, self-intersections, zero-thickness faces, internal shells, and duplicate/unintended solids.
- **Part fits in CAD but fails in a print:** identify whether error follows XY/Z axes, material, orientation, first-layer effects, or slicer settings; adjust a measured clearance parameter, then reprint a coupon.
- **Model changes unexpectedly under parameter override:** check OpenSCAD compile-time variable binding and lexical scope; prefer explicit module parameters and derived expressions.