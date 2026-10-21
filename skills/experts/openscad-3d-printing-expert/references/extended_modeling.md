# Extend parametric modeling workflows

Read when a task involves multi-part assemblies, reusable libraries, generated source, text,
concealed interfaces, or instructional models. These recommendations synthesize the inspected
book passages in [reference_survey.md](reference_survey.md); they do not certify book listings
as executable or their printed examples as suitable for another machine.

## Build an assembly progressively

1. Represent each component with inexpensive geometry at its intended envelope and datum.
   Assemble these first to check interfaces, placement, and insertion paths.
2. Stabilize module arguments and part selection, then replace simple geometry with detail.
   Refactor repeated constructions when they emerge; avoid speculative framework design.
3. Use the same component definitions for assembly inspection and separate print layouts.
   A print-layout selector must also place every component on the bed and avoid collisions;
   separation in XY alone does not establish a printable layout.
4. Add only details that can survive the intended scale and process. Increasing tessellation
   cannot make a sub-resolution ornament physically printable.

For build-volume splits, define joining datums and alignment features before exporting sections.
Validate each section and the assembled relationship, including access for fasteners or adhesive.
A mesh repair after splitting must preserve those interfaces rather than merely close surfaces.

## Expose a small part API

- Provide named entry modules for printable parts and an optional assembly; callers should not
  need to know the internal cutter, mirror, or placement sequence.
- Keep construction helpers separate from public dimensions. Use `children()` for reusable
  placement wrappers only when it reduces real repetition; specify child count and local frame.
- Treat third-party hardware models as references. Confirm dimensions against the actual hardware
  and record library version; a model library does not eliminate measurement.
- Distinguish library generations and APIs. A book using BOSL does not establish compatibility
  with BOSL2 or the currently installed release. Check real imports and signatures before use.

## Inspect hidden geometry

- Disable a complete transform-child statement with `*` or a deliberate block. Commenting only
  the transform leaves its child behind; commenting only the child can attach the transform to
  the following statement.
- Use a diagnostic section cut to reveal cavity floors, wall thickness, and mating clearances.
  Keep diagnostic cutters outside the production construction and disable them before export.
- `projection()` collapses geometry onto XY; `projection(cut=true)` sections at Z=0. Translate
  or orient the model deliberately to inspect another plane, and keep diagnostic output separate.
- A reduced inner hull or scaled solid does not guarantee constant normal wall thickness.
  Inspect the thinnest region, sloped walls, junctions, and openings rather than trusting a
  diameter difference as a complete shell check.

## Preserve functional dimensions

- Separate scalable body dimensions from calibrated gaps, hardware sizes, and minimum walls.
  Whole-object scaling changes all of them; revalidate interfaces and print-in-place joints after
  resizing rather than assuming the original fit survives.
- An enclosed cavity needs a printable roof and a usable interior. Compare a validated bridge,
  sloped roof, split construction, and removable support. Guard slope formulas against invalid
  angles and confirm positive remaining cavity height and wall thickness.
- For text-backed parts, define font, size, alignment, spacing, and margins together. Test short,
  long, and representative strings. Monospaced advances do not imply identical glyph bounds;
  fixed character-width multipliers are not general text measurement.
- For deformable stock, avoid forcing calipers or a gauge into the interface. A tapered printed
  gauge can characterize the mating envelope, but measure the gauge itself and account for its
  print error before treating its nominal diameter as a measurement.

## External source generators

- Use native OpenSCAD unless an external generator adds a demonstrated capability, such as data
  processing, sampled surfaces, or a large family of variants. Identify the generator's runtime
  and dependencies separately from the OpenSCAD executable.
- Record generator inputs, versions, units, selected variant, and output paths. Retain generated
  `.scad` for inspection and trace it back to its editable source; make repairs in the generator
  when it owns the geometry rather than hand-editing disposable output.
- Audit wrapper semantics: radius versus diameter, degrees versus radians, centering, transform
  composition, and whether a nominal 2D object is represented as a thin 3D approximation.
- Reset or isolate mutable generator state between outputs. Test distinct configurations in one
  process when global accumulators exist; a second export must not contain the first part's state.
- Define sampled surfaces by physical XY spacing and height scale, not just image/grid dimensions.
  Handle singularities and invalid samples explicitly; inspect topology and feature size after
  quantization or image processing.
- Reconstruct damaged listings only against a reliable source, then execute them. Editorial
  callout digits, split fences, broken indentation, and obsolete dependencies are not valid code.
  Render the generated result and run [testing_and_oracles.md](testing_and_oracles.md).

## Instructional and application models

- For mathematical connectors, derive the angle and axis convention, build one connector, then
  replicate by symmetry. Verify equations independently when extracted figures or formulas are
  missing; GUI sketch constraints do not automatically translate into OpenSCAD expressions.
- Separate a relief model's geometry from its printing strategy. Height changes or separate
  tiles can encode a pattern, but filament changes and pauses belong in the slicer/printer setup.
- Assess material and orientation against every relevant load path, including screw installation,
  not just the most visible cantilever. Consider temperature, creep, moisture, and impact.
- Treat application stories and AI-generated-design claims as context, not proof of optimization,
  structural safety, biological suitability, or clinical validity. Medical and other high-consequence
  parts need domain-specific requirements and validation beyond this CAD skill.
