# SVG project workflow

## Existing asset

For a bounded visual change, read
[targeted_editing.md](targeted_editing.md) and keep the existing asset workflow below
as the delivery contract.

1. Locate the authored SVG, generated copies, build/export scripts, callers, and
   the real display path. Identify whether the asset is loaded through `img`, CSS,
   inline markup, a component, a sprite, print, or another consumer.
2. Render a baseline at the smallest and largest intended sizes. Record clipping,
   fonts, color inheritance, background assumptions, line weight, and current
   accessibility behavior.
3. Inventory the structural surface: `viewBox`, groups, IDs, URL references,
   symbols, masks, clips, filters, markers, styles, scripts, external resources,
   text, and editor metadata.
4. Change the owning source. Preserve downstream IDs, selectors, component props,
   and build behavior that are part of the contract.
5. Re-render through the same consumer and apply the oracles in
   [testing_and_oracles.md](testing_and_oracles.md).

## Greenfield asset

1. Write the visual contract from [task_selection.md](task_selection.md). For a
   requested object, use [object_illustration.md](object_illustration.md). Sketch two
   or three thumbnail/block arrangements before committing to detailed paths.
2. Choose a coordinate system that keeps important geometry readable. Establish
   `viewBox`, aspect-ratio behavior, margins, background, and target size range.
3. Build semantic groups in drawing order. Start with primitives, shared styles,
   and reusable definitions; introduce detailed paths after silhouette and hierarchy
   work at target size.
4. Add labels, callouts, dimensions, scale bars, or interaction states with explicit
   ownership. Keep visible text live when editability or localization matters.
5. Render early, inspect at actual size, and refine geometry before adding effects.

## Delivery modes

- `img` or CSS image: treat the SVG as an image boundary. Put the useful text
  alternative on the host element and verify the file with the actual background.
- Inline SVG: use meaningful groups, `title`/`desc` or visible labels, ARIA
  relationships, focus behavior, and scoped IDs/styles as required by the graphic.
- Standalone asset: include the SVG namespace, stable intrinsic or responsive sizing,
  an appropriate accessible name/description, and self-contained resources. Declare
  each intentional external dependency explicitly.
- Vector-editor handoff: keep logical layers/groups and necessary editing metadata;
  maintain a separate optimized delivery artifact when the pipeline supports it.
- Print/publication: design and inspect at final physical size. Treat font embedding,
  color mode, strokes, label size, and publisher specifications as delivery concerns.

## Structure and geometry defaults

- Prefer `rect`, `circle`, `ellipse`, `line`, `polyline`, and `polygon` when they
  express intent more clearly than a path.
- Use groups for meaningful objects and shared transforms. Use `defs`, gradients,
  patterns, markers, clips, masks, symbols, and `use` for deliberate reuse.
- Keep IDs unique within the host document. Prefix reusable-asset IDs when multiple
  inline SVGs may share a page.
- Use non-scaling strokes when constant screen-space weight is part of the visual
  contract. For proportional scaling, scale geometry and strokes together.
- Bound filters and masks to the region they need so effects remain visible and the
  render area stays proportionate.

## Scientific and technical change control

- Preserve a source ledger for observed/measured facts, conventional symbols,
  simplifications, and inferred reconstructions.
- Use a graphic scale bar for scientific subjects that may be resized. Keep technical
  scale, units, dimensions, projection, and revision information explicit.
- Require both subject-matter or fabrication review and attractive rendered evidence;
  each answers a distinct part of the quality contract.
