# Lessons from historical models

Read-only source review covered the user's supplied model list. Paths below are locators relative
to the local `SynDocuments` collection, not dependencies of this portable skill. Related versions
are experiments, not a progression of certified designs. Original models were left unchanged.

## Parameter flow and interfaces

- `BrickLink/3D_print/table_bracket_2.scad`, lines 21-23, 49, 79, 88: top-level screw dimensions
  differ from cutter defaults, while calls omit those arguments. Trace each public parameter to
  the geometry it promises to control; pass the hardware dimensions explicitly.
- The same file, lines 9-15 and 117: tab length derives from the named dowel distance, while dowel
  placement repeats a literal conversion. Derive both from the same datum parameter.
- `BrickLink/3D_print/special_brick_mod-feb_22.scad`, lines 33, 61, 70: introducing a pin length
  does not automatically update independent recess/slot lengths. Trace all dependent cutters.
  Treat brick-interface dimensions as project measurements, not an official compatibility standard.
- `BrickLink/Tetrahedral_parts/tetrahedron.scad`, line 89: an inactive module converts `acos()`
  as if its output were radians. OpenSCAD inverse trigonometry already returns degrees. The active
  entry point at line 103 calls a different module; distinguish dormant code from active defects.

## Repetition and part selection

- `BrickLink/3D_print/SIFTING_TRAYS/lego_sort_tray-hole_same_dims.scad`, lines 34-69 and
  225-232: validate level indices and divisors; a hole-count condition also controls a stacking
  groove. Use explicit feature switches when two independent features should vary separately.
- That tray, lines 88-148 and 157-236: shell, aperture array, stacking interface, and reinforcement
  form useful module boundaries. Deterministic irregular patterns make comparisons reproducible.
- `BrickLink/simple_hexes.scad`, lines 13-16, and the tray, lines 108-113: names such as "hex"
  can disagree with facet count, scaling, or taper. Inspect effective apertures and ligaments.
- `BrickLink/Centennial_Wheel/Center_Support/center_support1c.scad`, lines 78-88: matching ring
  facets and radial cuts may encode intended alignment. Preserve purposeful polygons instead of
  automatically smoothing every cylinder.
- Support variants and `OpenSCAD/backups/` files retain dormant modules. Read actual top-level
  calls before treating a file as a complete part or choosing a baseline. Keep print/assembly
  selectors explicit rather than inferring the intended output from filename chronology.

## Transforms and imports

- `BrickLink/3D_print/Angle_Jig/angle_jig.scad`, lines 3 and 14-16: post placement repeats a
  literal Z value rather than deriving it from base height. Reference the intended mating plane.
- `BrickLink/3D_print/table_bracket.scad`, lines 90-96: geometry extends below Z=0 in its assembly
  frame. Provide a deliberate print placement and verify the final bounds against the bed.
- `BrickLink/3D_print/Dept_Logo_2023/dept_logo_print_v4.scad`, lines 1-5: outline extrusion and
  a shallower lettering cut are useful separation of concerns. Replace private absolute import
  paths with packaged relative assets; extend cutters beyond the exterior face.
- Corresponding logo filenames under `Dept_Logo_2023/Spring_2023/` duplicate the reviewed logo
  sources. Avoid treating duplicate copies as independent validation or automatically changing both.
- `Old_Desktop/MyDesktop/wire_port.scad`, lines 2-4: a rotationally extruded DXF depends on the
  profile's position relative to the axis; having the asset available does not prove valid geometry.

Apply these lessons through [code_best_practices.md](code_best_practices.md) and
[print_design.md](print_design.md). Validate actual changes with
[testing_and_oracles.md](testing_and_oracles.md), rather than copying historical dimensions.
