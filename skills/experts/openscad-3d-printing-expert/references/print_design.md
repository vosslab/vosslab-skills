# Design for printing and fit

## Separate dimensions and allowances

- Define nominal hardware dimensions separately from intended clearance, manufacturing tolerance,
  and Boolean overlap. Tolerance is the allowed variation of a feature, not a synonym for a gap.
- State whether clearance is radial/per-side or diametral/total. For concentric round features,
  radial clearance is half the difference between hole and shaft diameters. Changing both mating
  dimensions changes the resulting gap; compensate deliberately rather than applying an allowance
  twice by accident.
- Select clearance, transition, or interference fit from the required insertion, motion, and
  retention. Derive worst-case clearance from the smallest hole and largest shaft; nominal values
  alone do not establish interchangeability.
- Print a small mating coupon using the intended material, orientation, and slicer settings.
  Record measured dimensions and fit behavior, then change the named allowance. Preserve nominal
  hardware measurements so calibration does not become an unexplained geometry change.

These definitions are grounded in [reference_survey.md](reference_survey.md). The
[Prusa modeling guide](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135)
explicitly says there is no universal fit value. Its suggested starting gap for movable parts
is not clearly defined as per-side or total; choose and document a convention rather than copying
that number into a parameter with ambiguous meaning.

## Orientation and printable detail

- Choose the print orientation using load direction, bed contact, hole axes, support access, and
  visible-surface finish. Layer adhesion makes strength orientation-dependent; a CAD inspection
  cannot certify a loaded bracket or clip.
- Check wall and rib thickness in actual sliced toolpaths. Nominal nozzle diameter alone does not
  determine printable wall width; extrusion width and perimeter strategy matter.
- Check bridges and overhangs against the machine/material and cooling setup. Use a chamfer,
  changed orientation, accessible support, or split part when justified by the functional surface.
- Keep structural ribs/supports distinct from slicer-generated support material. Include access
  for support removal, screw installation, and insertion paths when designing cavities.
- Review elephant-foot effects at mating surfaces and orientation-dependent hole shape. A coupon
  in a different orientation does not necessarily calibrate the final interface.
- Validate minimum ligaments between perforations and walls, not just nominal aperture diameter.
  Tapered, faceted, rotated, or stretched apertures have different effective openings.

## Functional feature decisions

- Specify support angles relative to horizontal or vertical. Check the slicer's convention before
  translating an overhang recommendation into geometry.
- Add ribs or local root fillets where a broad wall, pin, or boss needs reinforcement; avoid
  thickening the entire part by default. Check root stress, toolpaths, and distortion together.
- For horizontal holes, compare reorientation, a self-supporting profile, and planned drilling
  or reaming. A teardrop is not interchangeable with a round bearing or sealing surface.
- Distinguish print-in-place joints from separately printed mating parts. Provide a viable route
  to remove support or residual material from the gap; a nominal clearance alone is insufficient.
- For hollow parts, specify how trapped powder, resin, or support is removed when that process
  requires it. Do not introduce drainage holes into a part that must remain sealed without
  resolving the functional conflict.
- When fits change unexpectedly, check source dimensions, exported scale, and sliced geometry,
  then investigate the printer/material process before changing CAD allowances. Keep process
  compensation tied to measurements rather than hiding faults with smaller mating parts.

These recommendations draw on the polymer/material-extrusion chapters and fit troubleshooting
passages in [reference_survey.md](reference_survey.md); their numerical examples are not defaults.

## Imported artwork

Construct the profile in XY, extrude it, then orient the solid. OpenSCAD extrusion uses the XY
projection of the input; tilting a profile first can change its section unexpectedly.
For rotational extrusion, keep the profile on one side of the Y axis and avoid isolated-point
contact at the rotation axis. Check the installed version's supported features.

For SVG artwork, convert unsupported text and effects into suitable paths, check contour
completeness, and measure a known span. Unitless SVG dimensions can depend on DPI. Open paths
and closed shapes have different stroke handling; screen appearance is not the imported solid.
For engraving, specify the remaining floor thickness and extend the cutter past the outer face.

Sources: [OpenSCAD extrusion manual](https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/2D_to_3D_Extrusion)
and [SVG import manual](https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Importing_Geometry/SVG_Import).
Finish with [testing_and_oracles.md](testing_and_oracles.md).
