---
name: ideonomy-plain
description: Expand, vary, invert, or recombine an idea with randomized ideonomy methods. Use for alternatives, opposites, unexpected angles, or fresh frameworks when output must remain portable plain text. Use `ideonomy-rich` for monospace art.
---

# Ideonomy plain

## Purpose

Expand an idea by treating its properties as dimensions that can be substituted, negated,
combined, abstracted, or reinstantiated. Produce a structured plain-text artifact that remains
readable through terminals, chat relays, email, and other low-format channels.

## Select a method tuple

Run the picker from this skill directory:

```bash
bin/pick
```

Use `--more` or `--less` to change tuple size, `--print` to list picks without their bodies,
`--seed N` for a repeatable tuple, or `--random-org` when network-backed entropy is requested.
The active primitive catalog is indexed in [`methods/README.md`](methods/README.md). Read and apply
every method file returned by the picker.

## Work in two passes

1. Internally identify axes from every picked dimension prompt, apply every picked operator to
   those axes, and fit the results into the picked organon.
2. Externally publish the organon as the artifact. Use headers named after the user's idea, the
   concrete operator move, or the organon's natural structure. Keep the procedure implicit.

The structure should reveal gaps, asymmetries, unnamed cases, or surprising neighbors. A flowing
brainstorm without an organon does not complete the skill.

## Portable rendering

- Use ordinary Markdown headings, lists, and fenced ASCII tables or diagrams.
- Build diagram borders from `+`, `-`, and `|` only.
- Render charts as labeled lists when a two-dimensional table would not survive the channel.
- Keep labels meaningful without color, typography, or Markdown rendering.
- Keep every file and generated artifact in this skill's plain workflow ASCII.

## Output contract

- Name the selected operators, organon, and dimension prompts briefly.
- Show the resulting structured artifact with intrinsic content headers rather than phase labels.
- Identify the strongest new idea or useful gap surfaced by the structure.
- Mention important directions the selected tuple did not explore when that helps the user continue.

## Catalog discipline

The picker composes three primitive categories: operators, organons, and dimension prompts. Add a
new primitive only when it is irreducible to existing methods, useful beyond one request, and
supported by observed value. Extend the relevant directory and update `methods/README.md`.

Keep historical recipe sketches under `examples/historical-recipes/` as inspiration only. They do
not enter the active picker because saved combinations would become preferred defaults and reduce
the randomized search space. [`examples/walkthrough.md`](examples/walkthrough.md) shows the active
workflow without defining a reusable tuple.

## Use boundary

Use this skill while the user is exploring alternatives, inversions, dimensions, or unexpected
frames. Once the desired idea is chosen and the task becomes implementation, return to the
appropriate execution workflow. Use `ideonomy-rich` when expressive Unicode monospace rendering is
part of the requested result.

## Attribution

The operators, organons, and method framing derive from Grace Kind's essays on Patrick Gunkel's
Ideonomy. Preserve that attribution when republishing or extending the catalog.
