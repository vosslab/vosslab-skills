# SVG testing and oracles

Require valid XML and rendered evidence matched to the asset's purpose.

## Structural checks

- Parse the SVG as XML and confirm the expected root, namespace, positive `viewBox`
  dimensions, and finite numeric output.
- Check unique IDs and resolve every local `href`, `url(#...)`, label, clip, mask,
  marker, filter, gradient, pattern, and symbol reference.
- Confirm external fonts, images, styles, or scripts are intentional and available in
  the real delivery environment.
- Inspect path closure, fill rules, joins, caps, transform order, marker orientation,
  filter regions, and clipped bounds where they affect the output.

## Rendered checks

- Render through the actual consumer. Inspect the smallest, typical, and largest
  target sizes on each required background.
- Check silhouette, visual hierarchy, label collisions, edge clipping, stroke weight,
  alignment, whitespace, repeated-instance consistency, and raster-image quality.
- Use a screenshot or rasterized preview for human inspection, and inspect local
  renders with `view_image` when that tool is available. Use behavioral and geometric
  assertions for durable tests; reserve pixel comparison for a grounded visual
  equivalence contract.
- When optimization is requested, compare before and after renders at target sizes and
  measure file size or node-count improvement. Confirm retained IDs, classes, ARIA,
  animation, and editor round-trip requirements.
- When the inspector requires PNG input, read
  [rendering_for_inspection.md](rendering_for_inspection.md). Conversion is supporting
  evidence: use `rsvg-convert` first and Playwright second, then return to the drawing.

## Accessibility checks

- Decorative SVG stays out of the accessibility tree; a meaningful image exposes a
  concise name, and a complex graphic provides the necessary longer explanation or
  adjacent equivalent.
- For `img`, verify host `alt`. For inline SVG, inspect `title`, `desc`, visible text,
  ARIA relationships, group semantics, and duplicate IDs in the containing document.
- Interactive SVG exposes keyboard-equivalent actions, visible focus, name/role/state,
  and a useful static or reduced-motion experience.
- Pair color with shape, text, position, pattern, or another visible cue when it
  carries meaning. Route numerical contrast measurement and hue-preserving repair to
  `color-accessibility-expert`.

## Domain oracles

- Object illustration: confirm that silhouette and characteristic parts establish
  recognition. Inspect negative spaces, major-mass proportions, projection
  consistency, overlap, line hierarchy, face-value separation, and readability at
  thumbnail size.
- Scientific: trace morphology, anatomy, orientation, labels, scale bars, and visual
  encodings to the supplied observation, data, imaging, or cited reference. Ask a
  subject expert to review inferred or case-specific content.
- Publication: render at final column, slide, poster, or page size; inspect the label,
  line, symbol, and detail level after reduction.
- Technical: cross-check projection, aligned views, shared dimensions, units, scale,
  line meanings, hidden features, section direction, tolerances, and title/revision
  information against the named drawing contract.
- Diagram: confirm that the reading order, grouping, arrows, legend, and emphasis make
  the intended explanation self-contained.

## Generative and animated SVG

- The same seed and parameters produce the same semantic scene; a different seed
  produces a valid variation. Test scene data or invariants when ordering or numeric
  precision may vary while preserving meaning.
- Bound coordinates, path complexity, element count, filter region, animation work,
  and exported file size. Exercise empty, minimum, maximum, and representative seeds.
- Use time-based motion. Test pause/cancel behavior, offscreen or hidden handling,
  pointer and keyboard input, and reduced motion.

## Completion record

Report the source asset, embed mode, target sizes/backgrounds, parser/reference checks,
rendered artifacts inspected, accessibility result, domain oracle, optimization delta,
and remaining assumptions.
