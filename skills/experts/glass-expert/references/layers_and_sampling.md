# Layers and sampling

Glass is a backdrop-sampling effect: it blurs, refracts, and tints whatever
renders behind it. Layer order decides whether the effect exists at all.

## The sampling path

Keep this stack clear of opaque layers, bottom to top:

```text
vibrant label             .foregroundStyle(.primary) -- adapts with the material
glass surface             .glassEffect(...) -- samples everything below it
(keep this gap clear)     an opaque .background(...) here blocks sampling
content layer             gradient, photo, document, editor -- what glass refracts
```

## Layer rules

- Glass sits above content in z-order (`ZStack` or `.overlay`) with real
  content underneath. Glass with nothing behind it refracts nothing and reads
  as an empty gray panel.
- Keep glass off glass. Glass samples the content layer; a glass surface
  stacked over another glass surface muddies both and defeats the depth cue.
- Modifier order matters: an opaque `.background(...)` wrapped around a glass
  element removes the translucency it was meant to show. A scrim between text
  and glass is intentional and fine; an opaque fill between glass and content
  is the bug.
- Content should reach under the glass edges. A glass bar floating over empty
  margin samples nothing at its boundary and loses the effect where it is most
  visible.

## Containers, merging, and morphing

- Group nearby custom glass shapes in one `GlassEffectContainer(spacing:)` so
  they sample consistently and merge when close. Independent glass views
  sample independently and can render visibly different.
- Morph one glass shape into another with `glassEffectID(_:in:)` plus a
  `@Namespace`, inside the shared container.

## Shape and interactivity

- `.glassEffect()` defaults to a capsule. Pass
  `in: .rect(cornerRadius:)` (or another shape) for anything that is not a
  pill.
- Add `.interactive()` to custom glass controls the user clicks or touches so
  the material responds the way system controls do.

## Verifying the layer work

Layer bugs and dead glass look identical in a bad capture. After any change
here, run the evidence protocol in
[testing_and_oracles.md](testing_and_oracles.md); the seed harness in
[component_seeds.md](component_seeds.md) gives a known-good sampling path to
compare against.
