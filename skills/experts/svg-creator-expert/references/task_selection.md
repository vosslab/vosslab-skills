# SVG task selection

Choose the final artifact and proof before choosing a drawing tool.

Default to creation. If the user says "make an SVG of X," produce the SVG and
render it as the completed artifact.

## Route the request

| Request signal | Route | Establish first |
| --- | --- | --- |
| "Make/draw/create an SVG of" an object, prop, tool, vehicle, equipment item, or small scene | Object illustration | Recognition target, subject references, view, silhouette, characteristic parts, and output size |
| Icon, logo, badge, sprite, or reusable asset | Vector asset | Target sizes, silhouette, color behavior, and reuse contract |
| Process, architecture, anatomy, or explanatory figure | Diagram | Intended message, reading order, labels, and abstraction level |
| Biological, botanical, or medical subject | Scientific illustration | Evidence source, audience, scale, orientation, and allowed simplification |
| Orthographic, section, dimensioned, or fabrication drawing | Technical drawing | Projection, units, scale, line conventions, dimensions, and governing standard |
| Procedural pattern, data-driven art, or many repeated elements | Generative SVG | Parameters, seed, bounds, element budget, and export behavior |
| Hover, focus, animation, or direct manipulation | Interactive SVG | Inline/embed mode, input methods, state semantics, and reduced-motion behavior |
| Change one object, color family, label, component, or state in an existing SVG | Targeted edit | Authored source, baseline render, selected visual object, owning nodes/styles, and preserved asset contract |
| Bloated, broken, clipped, blurry, or editor-exported SVG | Repair or optimization | Source of truth, baseline render, downstream IDs/hooks, and equivalence oracle |

## Select the artifact type

- Use [object_illustration.md](object_illustration.md) as the default route for a
  plain-language request to draw a recognizable thing.
- Use [targeted_editing.md](targeted_editing.md) for a bounded visual change to an
  existing SVG.
- Use code-native SVG for editable geometry, reusable assets, diagrams, and
  deterministic generated art.
- Use a vector editor when manual contour placement or art-directed path editing
  is central, then inspect and clean the exported SVG as code.
- Use `css-creative-expert` when the primary problem is page styling around an
  SVG, `geometry-expert` when a nontrivial geometric algorithm owns correctness,
  and `color-accessibility-expert` for measured contrast repair.

## Establish the visual contract

- Name the audience, message, embed mode, source-of-truth file, output size range,
  background assumptions, and responsive behavior.
- State the `viewBox`, aspect-ratio policy, coordinate units, visual hierarchy,
  line weights, color roles, label policy, and accessibility role.
- For scientific work, record which features are observed, measured, conventional,
  or inferred. For technical work, record projection, units, scale, and standard.
- Define the rendered evidence that will show success before path polishing begins.

Continue with [topic_index.md](topic_index.md) for the narrow source and
verification route.
