# OpenSCAD project workflow

## Existing project

1. Read repository instructions and inspect the `.scad` entrypoint, included libraries, imports, parameter definitions, exports, and tests. Check `openscad --version` and relevant command help before relying on version-specific behavior.
2. Render the baseline before changing it. Save its warnings, dimensions, and export result; note local modifications and preserve them.
3. Trace the requested feature from top-level parameters through modules to final assembly. Record units, coordinate conventions, and which dimensions are externally observable or mating interfaces.
4. Change the smallest responsible module. Preserve existing parameter names and defaults unless the requested outcome requires a contract change. Keep one source of truth for shared dimensions.
5. Compare the changed render/export against the baseline, then run the checks in [testing_and_oracles.md](testing_and_oracles.md).

## Greenfield model

1. Create a short model contract: purpose, envelope, critical dimensions and datums, interfaces, expected loads, target process, material, printer/nozzle, and preferred print orientation. Mark unknowns.
2. Set top-level parameters and a clear axis/origin convention. Use millimeters unless the target workflow specifies another unit; avoid hidden scale conversions.
3. Build reusable primitives as small named modules. Construct complex solids from simple positive geometry first; apply subtractions in clearly grouped `difference()` blocks. Use comments for design intent, not narration of syntax.
4. Add major geometry progressively and preview each stage. Keep optional parts and variants selectable through explicit top-level parameters or a documented part selector.
5. Validate the nominal case and meaningful parameter bounds. Check that dimensions remain positive, walls remain viable for the intended process, cutters stay through features, and components do not become disconnected.
6. Render exact geometry and export using the installed OpenSCAD version. Inspect the mesh in the target slicer, checking orientation, scale, manifold status, supports, build volume, and thin features.
7. Deliver `.scad` source plus requested mesh output and a concise parameter/print note. State remaining machine-specific uncertainties.

## Source organization

Apply [code_best_practices.md](code_best_practices.md) when writing or reviewing source.

- Put editable design inputs near the top, then derived dimensions, construction modules, and a final assembly/selector.
- Derive repeated dimensions from a small number of named parameters. Use `let()` or scoped assignments for local derived values; do not rely on imperative reassignment.
- Keep coordinate transforms next to the geometry they place. Prefer named transforms or small placement modules when a transform encodes an assembly relationship.
- Use `include` when library variables and module code must be evaluated in the caller's scope; use `use` when importing only modules/functions. Check include ordering when command-line `-D` overrides matter.
- Keep the final top-level geometry explicit. Ensure debug highlights, calibration geometry, and test coupons are selected intentionally and are excluded from production exports unless requested.