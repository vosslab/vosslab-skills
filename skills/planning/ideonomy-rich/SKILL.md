---
name: ideonomy-rich
description: Expand an idea with randomized ideonomy methods and expressive monospace art. Use when the channel supports Unicode box drawing, figlet banners, density gradients, and visible reasoning structure. Use `ideonomy-plain` for portable text.
---

# Ideonomy rich

## Purpose

Expand an idea by varying its properties along dimensions, applying randomized operators, and
rendering the result as an expressive monospace artifact. The visible structure should teach the
reader how the ideas relate, not merely decorate prose.

## Select a method tuple

Run the picker from this skill directory:

```bash
bin/pick
```

Use `--more` or `--less` to change tuple size, `--print` to list picks without their bodies,
`--seed N` for a repeatable tuple, or `--random-org` when network-backed entropy is requested.
The catalog is indexed in [`methods/README.md`](methods/README.md); the picked method files are the
instructions to apply.

## Work in two passes

1. Internally apply every picked dimension prompt, then every picked operator, and finally fit the
   results into the picked organon. Hold intermediate reasoning rather than publishing a process log.
2. Externally render one coherent artifact whose headers name the actual idea, operator moves, and
   organon. The reader should be able to infer which dimensions and operations produced each part.

## Load rendering guidance

Read [`rendering/README.md`](rendering/README.md) for the visual hierarchy, width, banner, legend,
dimension, operator-divider, and trail contracts. Then read the matching focused guide when the
picked organon is one of these:

- Atlas: [`rendering/atlas.md`](rendering/atlas.md)
- Chart: [`rendering/chart.md`](rendering/chart.md)
- Cycle: [`rendering/cycle.md`](rendering/cycle.md)
- Dictionary: [`rendering/dictionary.md`](rendering/dictionary.md)
- List: [`rendering/list.md`](rendering/list.md)
- Scale: [`rendering/scale.md`](rendering/scale.md)
- Tree: [`rendering/tree.md`](rendering/tree.md)

For another organon, apply the shared rendering principles to its natural structure. Unicode glyph
examples live in these rendering references so this entrypoint remains ASCII.

## Visible artifact contract

Render these five layers as one composition:

1. A compact title banner, using local `figlet` or `toilet` when available and a plain title when
   neither tool exists.
2. A tuple legend naming the selected operators, organon, and dimension prompts.
3. A dimensions block showing the explored axes and marking any pivotal dimension.
4. The organon body, divided by operator-named headers that state each concrete transformation.
5. An ideonomy trail that summarizes the moves and names at least one promising direction not
   surfaced by the current tuple.

The artifact's main header names the organon. Use intrinsic content headers instead of phase labels.
Make the operator and its specific move visible together.

## Rendering constraints

- Keep every line at or below 100 characters and preview the final block in a monospace context.
- Give each glyph, line weight, density, and marker one consistent semantic role within the piece.
- Use one box-drawing style per diagram while varying styles between hierarchy levels when helpful.
- Use motion, density, or enclosure only when it represents a real relationship.
- Keep prose short enough that the composition remains the primary explanation.
- Preserve readable fallback meaning in labels and spacing even when color is unavailable.

## Completion

Return the rendered artifact and a short plain-language interpretation of its most useful new
directions. The tuple, dimensions, operator moves, organon, and `not surfaced` trail line must all be
visible. If the requested channel cannot preserve Unicode monospace output, use `ideonomy-plain`
instead.
