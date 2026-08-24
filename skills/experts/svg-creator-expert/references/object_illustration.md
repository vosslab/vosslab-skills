# Object illustration workflow

Use this route when the request is primarily "make an SVG of this thing." The
default result is a recognizable, polished, editable SVG with rendered proof.

## Separate what from how

- Subject references establish what the object looks like: silhouette, proportions,
  characteristic parts, joints, openings, materials, labels, and variations.
- The local books establish how to draw it: primitive construction, perspective,
  projection, line hierarchy, value grouping, vector layering, and SVG structure.
- For a biological or medical subject, `local-only/LOCAL_SERVIER_SVG_FILE_PATHS.txt`
  may locate an existing local SVG. Search `/Lab_apparatus/` for equipment. Inspect
  the candidate itself and verify its license, attribution, ownership, and fit before
  reuse.
- Use multiple subject references when available. Observe common structure and
  synthesize it into original geometry.

## Use the local construction stack

When the local corpus is present, read focused passages from the layers that affect
the request. The first two layers are the minimum for an ordinary object illustration.

1. Form and perspective: the primary source is
   `local-only/object_construction/How_to_Draw_Drawing_and_Sketching_Objects_and_Environments_from_Your_Imagination-2013.md`.
   This repaired and audited conversion is the key construction reference. Use
   `X-Y-Z COORDINATE SYSTEM`, `WORKING WITH VOLUME`, `PLANNING BEFORE PERSPECTIVE`,
   `ELLIPSE BASICS AND TERMINOLOGY`, `HINGING AND ROTATING FLAPS AND DOORS`, or
   `CUTTING VOLUMES` according to the object's geometry. Drawing Mentor supplies a
   compact second explanation of primitives and perspective; search
   `local-only/drawing_fundamentals/Drawing_Mentor_1-3_Drawing_Materials_Lines_and_Shapes_Perspective_and_3D_Shapes-2013.md`
   for `objects you can describe on paper using only shapes` and
   `Two Point Perspective`. For cylindrical manufactured parts, also use the
   Engineering Graphics source and search `Curves and Circles in Perspective`.
2. SVG implementation:
   `local-only/svg_authoring/Mastering_SVG-2018.md`, search
   `viewBox and viewport in SVG`, or
   `local-only/svg_authoring/Generative_Art_with_JavaScript_and_SVG-2024.md`,
   search `Grouping and Reusing Elements`.
3. Line and depth hierarchy:
   `local-only/scientific_illustration/A_Handbook_of_Biological_Illustration-1988.md`,
   search `heaviest lines are used to draw the closest parts`, and
   `local-only/technical_drawing/Technical_Drawing_with_Engineering_Graphics_Sixteenth_Edition-2023.md`,
   search `Alphabet of Lines`.
4. Vector construction and shading:
   `local-only/vector_tools/Quick_and_Easy_Vector_Graphics-2020.md`, search
   `Z-Ordering` or `Boolean Operations`; or
   `local-only/vector_tools/Adobe_Illustrator_Classroom_in_a_Book_2022_Release-2022.md`,
   search `Organizing Your Artwork with Layers` or `Working with gradients`.
5. Composition and detail control:
   `local-only/drawing_fundamentals/The_Everything_Drawing_Book-2005.md`, search
   `Thumbnail Sketches and Working Drawings`; and the biological illustration
   handbook, search `CLARITY`.

Apply concepts from these passages to an original illustration. The committed guide
and current SVG sources provide the same construction layers on every installation.

## Build the object

1. Write a one-sentence recognition target: what should a viewer identify, at what
   size, and which features make that identification reliable?
2. Choose the view. When a manufactured-equipment request leaves the view open,
   start with a stable three-quarter view showing the front, one side, and top. Use one-point,
   two-point, axonometric, or flat projection deliberately. Maintain that projection's
   depth directions throughout the object.
3. Draw two or three tiny massing alternatives. Reduce the object to boxes, cylinders,
   ellipses, wedges, and cutouts. Compare silhouette and negative space at target size.
4. Build the chosen massing as SVG groups. Establish readable major planes and
   overlaps, then add characteristic parts.
5. Establish a style system before detail. A useful starting ratio is outer contour
   `2`, internal edge `1`, and fine detail `0.6-0.75`, adjusted for target size. Use
   two or three face values and one light direction. Use flat value separation as the
   default; add a restrained gradient when it communicates a material or curved form.
6. Render early. Correct recognition, perspective, proportions, and face separation
   before adding texture, tiny controls, labels, or decorative highlights. Use the
   rendered checks in [testing_and_oracles.md](testing_and_oracles.md).

## Keep component families consistent

When creating several objects for one project, record and reuse the projection or
depth vectors, viewer elevation, light direction, contour ratios, corner treatment,
and face-value palette. Give components compatible coordinate scales and semantic
groups. Put genuinely repeated parts such as wheels, tubes, wells, caps, arrows, and
droplets in `defs` or `symbol`; use `use` or data-driven generation for instances.
Consistency across the family matters more than maximizing detail in any one object.

## Calibration example: garbage dumpster

For a request such as "make an SVG of a garbage dumpster":

- Establish the recognizable masses: tapered or rectangular bin, front and side
  planes, top opening or lid, upper rim, and the lifting or wheel details appropriate
  to the chosen dumpster type.
- Use the user's requested view. When the view is open, use a three-quarter view.
  Construct the bin as related polygons or a box-derived path; keep corresponding
  depth edges parallel or converging according to the selected projection.
- Use the darkest contour on the near silhouette, lighter internal edges, and a small
  value change between front, side, lid, and recessed features. Let overlap and face
  values create depth before introducing gradients.
- Group the body, lid, hardware, and ground shadow separately. Reuse repeated wheels,
  hinges, or lifting pockets with `symbol` and `use` when it keeps them consistent.
- Render at the requested size and at thumbnail size. Revise until the silhouette and
  characteristic parts identify it clearly as a dumpster.

The same method scales to lab equipment: a tube begins as a cylinder and ellipses, a
rack as a box and repeated holes, a micropipette as aligned tapered masses, and a
centrifuge as a rounded box with a lid and control plane.

## Completion oracle

The result is complete when the silhouette and characteristic parts identify the
requested object, the projection is internally consistent, characteristic parts are
placed on plausible major masses, the line and value hierarchy survives at target
size, and the SVG remains structured enough to revise or reuse.
