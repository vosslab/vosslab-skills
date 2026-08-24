---
name: svg-creator-expert
description: >-
  Create finished, editable SVG illustrations from plain-language requests. Use
  when the user asks to draw an object, icon, scene, diagram, scientific figure,
  or technical illustration as SVG, or to edit, debug, animate, or optimize an
  existing SVG.
---

# SVG creator expert

## Overview

Turn an image request into a finished SVG file whose subject is recognizable,
geometry is editable, style is coherent, and rendered result fits its actual use.
A request such as "make an SVG of a garbage dumpster" means create the SVG and
inspect its render as the completed response. Infer reasonable visual defaults for
unspecified details.

Use the local-only books as working drawing references when they are available.
Read focused passages for shape construction, perspective, line hierarchy,
vector layering, shading, and SVG implementation before drawing. Subject
references establish what the requested object looks like; the local books
establish how to construct and communicate it. For ordinary manufactured objects,
use Scott Robertson's audited *How to Draw* conversion as the key construction
reference and pair it with an SVG implementation source.

## Instruction style

Use positive, outcome-directed language in implementation notes, prompts, and
delegation briefs. State the desired artifact, construction method, visual qualities,
and verification evidence. Omit irrelevant tools and alternatives. Name a restrictive
boundary when safety or correctness requires it, then pair it with the intended action.

## Workflow

1. Commit to the requested artifact.
- Default to producing an editable `.svg` file at the requested or project-appropriate
  location. Keep the editable SVG as the source deliverable and use raster previews
  as verification evidence.
- Route ordinary requests to object illustration first. Select the matching alternate
  route for a diagram, scientific figure, technical drawing, generative artwork,
  interactive graphic, or existing-asset repair.
- Read [references/task_selection.md](references/task_selection.md). For an object,
  icon, piece of equipment, or small scene, read
  [references/object_illustration.md](references/object_illustration.md).
- For a bounded change to one object, color, label, component, or state in an existing
  SVG, read [references/targeted_editing.md](references/targeted_editing.md).

2. Establish what must be recognizable.
- Identify the subject's silhouette, major masses, characteristic parts, openings,
  overlaps, materials, and likely orientation from user-provided or independently
  checked subject references. Synthesize an original construction from common
  observations across the references.
- Infer a clear view, palette, target size, background, and level of detail when
  unspecified. For a manufactured object that benefits from depth, prefer a
  consistent three-quarter view.
- For project work, inspect the source-of-truth path, callers, embed mode, existing
  visual language, and build/export flow. Read
  [references/project_workflow.md](references/project_workflow.md).

3. Pull techniques from the local corpus.
- When `references/local-only/` is present, read focused source passages directly.
  For object creation, read at least one focused construction passage and one
  SVG/vector implementation passage from the default stack in
  [references/local_books.md](references/local_books.md).
- Use [references/reference_survey.md](references/reference_survey.md) for verified
  search terms and [references/topic_index.md](references/topic_index.md) for a
  narrower problem. Record the paths and passages that materially informed the work.
- Use current specifications for version-sensitive SVG behavior. For scientific or
  technical content, verify subject facts, scale, projection, units, and standards
  from the owning source.

4. Construct before decorating.
- Reduce the subject to boxes, cylinders, ellipses, wedges, and other primitives.
  Establish the silhouette and negative spaces, then project characteristic parts
  onto the major masses. Keep depth directions and ellipses internally consistent.
- Choose a small line hierarchy and two or three fill values per material or object.
  Use overlap, value, and restrained highlights to explain form before adding texture.
- Start with thumbnails or a block layout. Select a composition whose silhouette and
  characteristic parts remain clear at target size, then polish its paths.

5. Implement as structured SVG.
- Set a stable `viewBox`; group parts by meaning and drawing order; prefer readable
  primitives and transforms; and use paths for contours that require them.
- Use unique descriptive IDs. Put repeated parts in `defs` or `symbol` and instantiate
  them with `use` when this improves consistency and editing.
- Preserve live text for editable or localized assets. For fixed outlines, convert
  text to paths and retain an accessible text equivalent.
- Scientific work distinguishes observed, measured, simplified, and inferred content.
  Technical work declares its projection, units, scale, and line meanings. Generative
  work records its parameters and seed.

6. Render, inspect, and revise the picture.
- Parse the XML, resolve IDs and references, then render through the real delivery
  path at the smallest and largest intended sizes.
- Inspect recognizability, silhouette, perspective, proportions, line hierarchy,
  face-value separation, clipping, labels, contrast, and accessibility. Revise the
  SVG when the render exposes a weakness. Completion requires valid markup and a
  successful rendered inspection.
- Use the oracles in
  [references/testing_and_oracles.md](references/testing_and_oracles.md).

7. Deliver the finished asset.
- Optimize after the correct render exists, with a before/after equivalence
  check that preserves IDs, semantics, CSS hooks, animation, and editability.
- Report the SVG path, embed mode, rendered evidence, local passages used, important
  design decisions, and any remaining subject or delivery uncertainty.

## Quality bar

- The requested subject is recognizable from its silhouette and characteristic parts
  before decorative detail is noticed.
- Geometry remains crisp and legible across the target size range.
- Semantic groups, readable geometry, and reusable definitions make the structure
  straightforward to edit.
- Scientific claims, scale, and labels trace to evidence; technical views and
  dimensions agree; generative output is reproducible from its recorded inputs.
- Accessibility matches the delivery context: decorative graphics stay silent,
  meaningful graphics have an appropriate name or description, and interactive
  graphics support keyboard and reduced-motion use.
- Completion evidence includes valid XML and the actual rendered asset.

## Output expectations

When using this skill, produce:

- A finished SVG implementation for creation requests. For review requests, produce
  a file-specific review grounded in the authored source and its render.
- The illustration route, visual contract, source-of-truth file, and embed mode.
- Rendered proof at relevant sizes plus structural, accessibility, and domain
  checks appropriate to the asset.
- The local source paths and focused passages used to guide construction and SVG work.
- Any remaining uncertainty about source facts, standards, fonts, or downstream
  export requirements.
