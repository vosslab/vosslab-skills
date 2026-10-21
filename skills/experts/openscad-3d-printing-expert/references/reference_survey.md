# Evidence and source scope

Sources were inspected while developing this skill. Recommendations derived from them are
engineering guidance, not universal dimensional guarantees or evidence of successful prints.
Local file locations are listed in [local_books.md](local_books.md).

## Technical drawing book

*Technical Drawing with Engineering Graphics*, sixteenth edition (2023):

- "Definitions for Size Designation", lines 14204-14216: allowance specifies minimum clearance
  or maximum interference; hole/shaft allowance uses the smallest hole minus the largest shaft.
- "Fits between Mating Parts", lines 14264-14282: clearance, interference, and transition fits
  describe different ranges of mating behavior, not just one nominal gap.
- "Specifying Fit Using Limit Dimensions", lines 14284-14296: a feature's tolerance is the
  difference between its upper and lower limits. Hole and shaft tolerances are independent.
- "Translating the Model", lines 12529-12543: STL facets approximate surfaces; facet size and
  printing layer thickness are distinct contributors to surface quality and production cost.
- "Rapid Prototyping Systems", lines 12545-12547 and 12581-12583: accuracy and durability depend
  on process/material. Its FDM example uses a second support material; this is not a requirement
  for every FDM printer or support strategy.

## Computational geometry book

*Handbook of Discrete and Computational Geometry*, third edition (2018):

- Section 57.1.2, "Boundary Representation", lines 79529-79564: topology expresses incidence
  and adjacency. In an oriented manifold boundary, edge incidence and vertex neighborhoods both
  matter. Two incident faces per edge alone are not a complete validity test.
- Section 57.1.3, "Mesh Representations", lines 79578-79597: STL stores triangle-local
  coordinates without explicit adjacency, requiring topology to be inferred. A file that exists
  can still represent an invalid printable boundary.
- Avoid borrowing this conversion's wording about STL "vertex normals" as a format specification;
  use a format reference for serialization details.

## OpenSCAD cookbook

John Clark Craig, *OpenSCAD Cookbook: OpenSCAD Recipes for learning 3D modeling* (2019):

- Recipe 3, "Parameterization", lines 169-237: derive related dimensions from shared inputs
  rather than manually recalculating repeated literals. This supports the parameter-flow checks
  in [code_best_practices.md](code_best_practices.md).
- "Functions, Modules, and Regular Polygons", lines 811-855: functions calculate values;
  modules construct geometry. The polar-coordinate example explicitly uses degrees.
- Lines 863-893: group editable design controls and give raised lettering a small overlap with
  its base. Preview colors remain distinct from export/material assignment.
- "No Matter How You Slice It", lines 899-924: `projection()` projects the solid onto XY;
  `projection(cut=true)` instead sections it at Z=0. Use section views to inspect hidden geometry.
- These are inspected passages, not a claim that every recipe has been reviewed or executed.

## Additive manufacturing design guide

*A Practical Guide to Design for Additive Manufacturing*, local file labeled 2020:

- Sections 7.1-7.3, lines 1682-1720: balance load direction, wall distortion, surface finish,
  and support access when selecting orientation. Support angles may be measured from horizontal
  or vertical; state the convention instead of copying a bare angle.
- Sections 7.4-7.6, lines 1732-1765: hole orientation affects roundness; ribs can stiffen broad
  walls; hollow parts need a plan for removing trapped process material or internal supports.
- Section 8.1.1, lines 1790-1796: measure a reference part to characterize the actual system.
  The numeric table is explicitly for industrial-quality material extrusion, not every printer.
- Sections 8.1.3-8.1.8, lines 1799-1833: provide support-removal access, inspect wall toolpaths,
  and consider self-supporting hole profiles only when their changed shape preserves function.
- Sections 8.1.9-8.1.13, lines 1834-1882: print-in-place clearances depend on support removal;
  hole compensation requires machine/material verification; blend pin and boss roots into walls.
- Treat numeric wall, hole, rib, and clearance recommendations as process-specific starting
  points. Avoid importing fixed correction values or layer-height-to-print-time ratios as laws.

## Print failure diagnosis

*3D Printing Failures: Diagnose and Repair*, local file labeled 2022:

- "Parts Not Mating Together", lines 4617-4641: use a tolerance test to establish actual fit
  behavior. The author's layer-height/nozzle-based estimates are rules of thumb, not accuracy
  specifications or a replacement for a measured coupon.
- Lines 4645-4687: investigate nozzle condition, extrusion, material condition, mechanics, and
  settings before disguising an equipment/process problem through CAD changes.
- Do not adopt generic under-extrusion, nozzle-replacement intervals, or motion-calibration
  changes from these anecdotes. Use the machine's documentation and evidence from the fault.

## Programming with OpenSCAD

`Programming_with_OpenSCAD_A_Beginners_Guide_to_Coding_3D-Printable_Objects-2021.md`:

- "Step 3: Create--Use a Walking Skeleton Approach", lines 2664-2670, and "Iteration 1:
  Connecting the Tower's Basic Building Blocks", lines 2682-2786: assemble low-detail components
  first to establish envelopes and module interfaces before adding expensive detail.
- "Design Organization Overview", lines 3126-3140: extract shared constructions as repetition
  emerges. "Final Evaluation of the Design Cycle", lines 3111-3124: omit unprintably small detail.
- "Setting Up a Design Mode and Print Mode", lines 2364-2411: reuse components for assembled
  and separate layouts. Centered solids in the example still require bed-placement checks.
- "Calibration Pyramid", lines 572-580, and "Hole-and-Pins Test", lines 592-598: dimensional
  calibration and mating-fit tests answer different questions.
- Listings around lines 2700-2756 contain editorial callout digits; reconstruct and validate
  rather than copying them. The radius/diameter prose at line 2733 conflicts with its expression.

## Simplifying 3D printing

`Simplifying_3D_Printing_with_OpenSCAD-2022.md`:

- "Creating our own OpenSCAD library", lines 3681-3779: provide convenient public entry modules
  for whole components and individual parts. Its preference for globals plus `include` is not
  adopted as a general design rule; use explicit interfaces where practical.
- "Creating a dynamic backing plate", lines 2812-2885: derive backing geometry from content,
  but its fixed character-width arithmetic is specific to the chosen font and size.
- "Creating the sliders for our desk drawer", lines 3380-3448: inspect assembled fit separately
  from exporting printable parts. The escaped import fragment at line 3411 needs reconstruction.
- "Measuring the paper tube" through "Printing out and using the measurement tool", lines
  4996-5062: use a measured gauge when calipers deform flexible stock; avoid forcing the gauge.
  The associated raft recommendation is not a universal remedy for first-layer distortion.
- "NopSCADlib", lines 3133-3147, does not establish that reference models replace measurement.
  "Downloading and installing the BOSL", lines 3167-3181, is historical library-specific advice,
  not proof of compatibility with another library generation.

## Creating models using OpenSCAD

`Creating_3D_Models_for_3D_Printing_Using_OpenSCAD-2020.md`:

- "Temporarily remove pieces from your model", lines 1823-1864: disable the entire geometry
  statement; commenting only a transform or its child can alter the next object's placement.
- "Cutting away parts temporarily", lines 1983-2022: inspect hidden interfaces through a
  diagnostic section, then restore production geometry before export.
- "Chapter 13: Hinges", lines 2024-2038 and 2153-2157: process-dependent gaps must survive
  resizing. Do not adopt whole-object scaling as a substitute for functional parameterization.
- "Chapter 22: Hollow objects", lines 3518-3558: design printable cavity roofs. Its bridge
  distances and slopes are setup-specific; guard the displayed slope formula's singular endpoints.
- Line 1763 calls F5 render; use the preview/exact-render distinction. Listings at lines 1873,
  2010, 2048-2054, and 3580-3604 contain malformed or split code. Tip-only joins in the hinge
  example do not establish robust connectivity or load capacity.

## Historical OpenSCAD printing guide

`OpenSCAD_for_3D_Printing-2014.md`:

- "Modules and Functions", lines 910-972: reusable modules and child-geometry placement
  wrappers. Specify a wrapper's child count and coordinate contract.
- "Chapter 6. Libraries", lines 1213-1235: separate reusable definitions from top-level output.
  "Extruding Imports" through "Copying a Flat Solid Object", lines 784-811, supports retaining
  vector source and checking imported scale against physical measurements.
- "Printing", lines 569-598: render before export and check boundaries rather than appearance.
- Historical `assign`/`child` advice, module-argument inheritance claims, loop-binding warnings,
  and override-order rules require current manual verification. Examples at lines 870 and 923 use
  `height` where native cylinders require `h`; the extrusion syntax at line 850 is historical.
  Prefer current scale-aware cutter overlap over the book's oversized cutters.

## OpenSCAD basics tutorial

`OpenSCAD_Basics_Tutorial-2020.md`:

- "Defining the Resolution and parameters of the model", lines 314-330, and "Creating the
  Rectangular Pattern of the Cut Features", lines 607-674: separate dimensions from quality
  controls and derive repeated positions from explicit pitch and extent.
- "Using the Hull function" through "Mirroring the Loft module", lines 872-987: encapsulate
  repeated construction and mirror one definition instead of duplicating it.
- "Shelling the Model geometry", lines 989-1061: shared inner/outer construction is useful,
  but reducing diameters in a sloped hull does not prove uniform normal wall thickness.
- Screenshot/text disagreement at line 609, ambiguous arguments at 628-630, and extremely thin
  hull seeds require review. `mirror([1,0,0])` reflects in a plane normal to X, not about an axis.

## Python-generated geometry

`Python_for_3D_Printing-2019.md`:

- "Python to the Rescue" and "How Python was added to OpenSCAD", lines 50-83: an external
  generator emits source; wrapper semantics are distinct from native OpenSCAD.
- "Chapter 25: Assemblies", lines 2173-2255: compose part definitions through an assembly entry.
  Avoid the example's wildcard imports and incidental access to another module's imported objects.
- "Chapter 27: Mason Bees", lines 2483-2519: derive an envelope and cutter array from explicit
  inputs; the example supplies no independent biological-suitability validation.
- "Chapter 28: Surface", lines 2528-2631: sampled fields and image processing need explicit
  physical scale and sample handling. The prose/formula mismatch at 2547, uncalled `f.close` at
  2565, and legacy Pillow API at 2596 prevent treating the listings as ready-to-run tools.
- "Appendix A: openscad.py source code", lines 2702-2811 and 3060-3147: the wrapper's sphere
  takes a diameter and emits a radius. Global accumulators and a tiny constant are not a reusable
  isolation/robustness policy; damaged indentation and repeated text need source reconciliation.
- Generator provenance, isolated output state, and repeatable variant checks in
  [extended_modeling.md](extended_modeling.md) are engineering recommendations motivated by
  these passages, not guarantees made by the book. An anecdotal watertightness claim is not proof.

## General printing design

`3D_Printing_For_Dummies-2023.md`:

- "Verifying models with Netfabb", lines 3542-3556: inspect mesh defects, size, and orientation.
  Transfer the checks, not historical UI steps; mesh shells do not mean physically hollow parts.
- "Designing Parts for 3D Printing" and "Material", lines 4289-4327: consider service conditions,
  creep, impact, moisture, and material behavior; verify the intended application with tests.
- "Orientation", lines 4329-4341: improving one load path may weaken a screw mounting region.
  Inspect the complete assembly's stresses and toolpaths rather than only minimizing supports.
- "Layer height" through "Infill level", lines 4345-4366: geometry, extrusion width, walls, and
  infill interact. Example settings are not universal strength prescriptions.
- "Printing Big: Bonding and Joining Parts", lines 4437-4449: split oversized objects and
  validate each section. Joining datums and fit checks are the skill's engineering extension.

## Operational and application background

These books contribute scope or requirements context, not additional OpenSCAD language rules.

- `3D_Printer_User_Guide_Fundamentals_Maintenance-2020.md`: "Chapter 5: 3D Slicer Settings",
  lines 503-605, separates geometry from layers, infill, support, adhesion, and G-code. "Chapter 7:
  Basic Maintenance of 3D Printer", lines 705-747, explains machine-condition effects. Broad
  shell/infill/angle defaults and filament-diameter claims are not adopted; use machine documents.
- `Changing_Lives_Through_3-D_Printing-2021.md`: "Creation by Adding Multiple Layers", lines
  140-157, is introductory background. "Printing Dinosaur Bones and Sharing Data", lines
  1181-1230, motivates replicas and sharing but supplies no geometric accuracy specification.
  "Chapter Three: Many Marvelous Medical Uses", lines 696-758, is not clinical design validation.
  The material taxonomy around lines 158-170 is unreliable and is excluded from technical rules.
- `Learning_Mathematics_in_the_Context_of_3D_Printing-2022.md`: "2.1.2 Parametric Modeling",
  lines 145-166, supports dependency-driven construction, not direct translation of GUI constraints.
  "4 3D printing of tessellations", lines 1476-1509, informs tiles and height-based relief models;
  filament changes remain a slicer/printer concern. "3 The Vertex-connector" through section 3.2,
  lines 1746-1790, motivates one connector replicated by symmetry. The extracted angle derivation
  is incomplete around 1768-1770; independently verify it before use. Pedagogy is not a fit standard.
- `Smart_Revolution_How_AI_and_3D_Printing_are_Transforming_Industry-2024.md`: "Intelligent
  Design Systems", lines 405-425, frames goals/material/manufacturing constraints. "Ensuring
  Precision with 3D Printing", lines 691-713, and "Technical Limitations of 3D Printing", lines
  1217-1241, motivate calibration and qualified outcomes. These passages provide no executable
  optimizer, tolerance budget, or structural validation; promotional claims do not supply evidence.

## Review limits

Every book in the dedicated subject collection is accounted for in
[local_books.md](local_books.md), excluding its directory index. Review covers selected substantive
passages and headings, not every page. Source books remain unmodified and unbundled. Conversion
damage is noted without asserting whether an error originated in print or extraction. No book
listing is claimed to have compiled, rendered, or printed during this documentation work.

## Public documentation

- [OpenSCAD documentation](https://openscad.org/documentation.html) links to the language manual.
  [Language reference](https://files.openscad.org/documentation/manual/The_OpenSCAD_Language.html)
  grounds scoped bindings, modules/functions, Boolean child order, and special variables.
- [Transformations](https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations): nested
  transforms act from the child outward; vector rotations apply X, then Y, then Z.
- [Extrusion](https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/2D_to_3D_Extrusion): profile
  projection, extrusion axes, and rotational-profile restrictions. Some features require snapshots;
  verify the installed version instead of assuming everything on the page is available.
- [SVG import](https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Importing_Geometry/SVG_Import):
  unsupported text/effects, open-path stroke handling, and DPI-dependent sizing.
- [FAQ](https://files.openscad.org/documentation/manual/FAQ.html) and
  [STL export](https://files.openscad.org/documentation/manual/STL_Export.html): F5 display is not
  F6 validation; inspect exact render errors and ambiguous contact. The hosted export page contains
  historical examples, so its old format list is not a current compatibility matrix.
- [Prusa modeling guide](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135):
  orientation affects strength/finish; fits depend on settings, geometry, material, and calibration.
  Test prints resolve uncertainty. Its example gap does not specify a radial/diametral convention.

## Historical model evidence

[model_patterns.md](model_patterns.md) records source-level observations from the user's older
models. These examples motivate coding checks; their filenames and comments do not prove a
model rendered, sliced, fitted, or printed successfully.
