# Targeted SVG editing

Use this side route for a bounded change to an existing SVG, such as changing one
object from blue to red, adjusting a label, moving a component, or revising one
symbol. Keep the requested visual change central and preserve the asset's established
composition, geometry, behavior, and delivery contract.

## Establish the edit target

1. Locate the authored source and its real consumer. Record the embed mode, target
   sizes, backgrounds, and any CSS or component props that influence the SVG.
2. Render a baseline through the real delivery path. Keep matching full-size and
   thumbnail captures for the final comparison.
3. Describe the target in visual and structural terms: object, part, current
   appearance, requested appearance, relevant states, and expected extent of change.
4. Map the rendered target to source nodes before editing. Prefer semantic IDs,
   groups, classes, and symbols. For flattened artwork, combine geometry bounds,
   drawing order, paint values, clipping, and temporary diagnostic highlights to
   identify the owning paths.

A repeated color may serve several unrelated objects. Classify its use sites by
visual role and object ownership before changing the selected object's paint.

## Trace the rendered paint

Inspect every layer that contributes to the target's visible appearance:

- `fill`, `stroke`, and inline `style` presentation values.
- Rules in `<style>`, host-page CSS, inherited `color`, and custom properties.
- Gradient stops, patterns, masks, filters, opacity, and blend behavior.
- Hover, focus, selected, disabled, animated, and data-driven states.
- Reused definitions reached through `use`, `href`, or component instances.

Use the browser's computed style when host CSS participates in the final color. Use a
temporary diagnostic render with candidate nodes assigned conspicuous colors when a
flattened export makes source-to-render mapping uncertain.

## Apply a color-family edit

Treat a shaded object as a coordinated palette of visual roles.

1. Identify the object's color roles: highlight, light face, base face, shadow face,
   outline, reflection, and state accent.
2. Choose the destination hue and preserve the existing light-to-dark ordering,
   contrast between adjacent faces, material cues, and shared light direction.
3. Scope the destination palette to the selected object. When a shared class or paint
   token also serves other objects, introduce an object-specific class, custom
   property, or definition for the target.
4. Apply the same role mapping to the target's relevant interaction or data states.
5. Keep semantic colors such as warnings, status indicators, measurements, or brand
   marks tied to their owning meaning.

For example, changing one blue machine housing to red usually means mapping its pale
blue highlight, middle blue body, and dark blue side plane to a pale red, middle red,
and dark red family. The charcoal outline can retain its structural role.

## Preserve the asset contract

- Edit the owning source and keep its generation or export flow intact.
- Preserve the `viewBox`, geometry, transforms, drawing order, clipping, IDs, CSS
  hooks, accessibility relationships, and reusable definitions that belong to the
  asset contract.
- Keep the implementation change proportional to the visual request. Add a semantic
  group or scoped paint token when it makes the target explicit and future edits
  reliable.
- Preserve live text, localization hooks, interaction behavior, and reduced-motion
  behavior that participate in the edited object.

## Verify the finished edit

1. Parse the edited SVG and resolve its local references.
2. Render before and after at identical sizes, backgrounds, states, and embed mode.
3. Confirm that the selected object shows the requested change and that all other
   regions preserve their baseline appearance and placement.
4. Inspect target-size recognition, face separation, outline contrast, clipping,
   accessibility, and state consistency.
5. Report the edited source path, selected object, paint or property mapping, rendered
   evidence, and any intentional structural cleanup.

Read [rendering_for_inspection.md](rendering_for_inspection.md) for PNG inspection and
[testing_and_oracles.md](testing_and_oracles.md) for structural and rendered checks.
