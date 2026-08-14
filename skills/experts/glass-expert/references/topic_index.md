# Topic index

This is the symptom router. Match the observed problem to a row, then open the
named guide. The table is keyed by what breaks, not by API name; for an API
lookup use [api_quick_reference.md](api_quick_reference.md).

## Symptom routing table

| Symptom | Likely cause | Guide | Fix invariant |
| --- | --- | --- | --- |
| Glass renders flat gray everywhere, on screen | Old SDK, `#available` branch not taken, Info.plist compatibility opt-out, or Reduce Transparency on | [api_quick_reference.md](api_quick_reference.md) availability section | Build with the macOS 26+ SDK; confirm the runtime branch and system settings |
| Glass invisible over the app window | Plain backdrop; nothing to sample | [layers_and_sampling.md](layers_and_sampling.md) | Put contrast-bearing content behind the glass; invisible over plain white is expected |
| App looks right on screen but the capture shows flat gray | Offscreen render path skipped backdrop compositing | [capture_paths.md](capture_paths.md) | Capture the live window with `screencapture -l <window-id>` |
| Glass region identical with Reduce Transparency toggled | Effect not live; a flat fill is masquerading as glass | [testing_and_oracles.md](testing_and_oracles.md) | The reduced capture must be visibly more opaque; run `scripts/compare_captures.py` |
| Text unreadable over some backdrops but fine over others | Contrast depends on user-controlled backdrop; material guarantees no minimum | [color_and_contrast.md](color_and_contrast.md) | Guarantee contrast with accessibility checks plus a scrim, never one lucky backdrop |
| Hardcoded label color breaks in one appearance mode | Glass flips light/dark treatment from backdrop luminance | [color_and_contrast.md](color_and_contrast.md) | Use semantic styles (`.foregroundStyle(.primary)`) so vibrancy adapts |
| Tint looks different over different content | `.tint` modulates the sampled backdrop, it does not paint | [color_and_contrast.md](color_and_contrast.md) | Verify tint over light and dark backdrops before shipping |
| Two nearby glass shapes refuse to merge or morph | Shapes not grouped in one container | [layers_and_sampling.md](layers_and_sampling.md) | Wrap them in one `GlassEffectContainer`; morph with `glassEffectID` |
| Glass control renders as a pill when a card was expected | Default shape is a capsule | [api_quick_reference.md](api_quick_reference.md) | Pass `in: .rect(cornerRadius:)` or another shape |
| Glass over a sidebar or another glass panel looks muddy | Glass stacked on glass | [layers_and_sampling.md](layers_and_sampling.md) | Glass samples the content layer; keep glass off glass |
| Glass element loses translucency after adding a background | Opaque `.background(...)` inserted into the sampling path | [layers_and_sampling.md](layers_and_sampling.md) | Keep the path between glass and content clear of opaque layers |
| Toolbar or menu looks different on macOS 27 than 26 | System retuned its chrome (uniform frosted toolbar in 27) | [design_placement.md](design_placement.md) | Expected; standard toolbar and menu APIs inherit each year's look |
| Same code, different opacity across backdrops | Material self-adjusts opacity for legibility | [color_and_contrast.md](color_and_contrast.md) | Expected behavior; compare captures against the same backdrop |

## Fast checks before deep debugging

1. Is anything with visual contrast actually behind the glass?
2. Is the capture from the live screen, not an offscreen render?
3. Is Reduce Transparency off on the test machine (and its state labeled)?
4. Built with the macOS 26+ SDK, `#available` branch taken, compatibility
   opt-out absent?
