# Post-processing screenshots before committing

Apply these steps after capturing a screenshot and before copying it into
`docs/screenshots/`.

## Hook constraint: process under /tmp

The repo permission hook scopes image tools (`convert`, `magick`, `optipng`,
`pngcrush`, and similar) to `/tmp` paths only. Process the image while it lives
under `/tmp`, then copy the finished PNG into `docs/screenshots/` with `cp`.

## Size ceiling and budget

Cap the longer edge at 1920 px and keep each PNG under about 1 MB. For the
common landscape screenshot the longer edge is the width, so this reads as a
1920 px width cap; a tall portrait capture is bounded by its height instead. A
file whose longer edge exceeds 1920 px and is over 1 MB should be resized
(below). A file already within 1920 px that still exceeds 1 MB is acceptable
when the detail earns it; note the reason in the PR description or CHANGELOG.
Match the budget documented in [embedding.md](embedding.md).

Why 1920 px, not smaller: GitHub renders an inline README image downscaled to
the text column (about 880 px) and opens the native-resolution file when the
reader clicks it. A 1920 px landscape capture therefore stays crisp in the
column on Retina displays and reveals genuine full detail on click, with no
separate thumbnail file to maintain. Downscaling to 880 px would throw that
detail away.

The budget is not about storage cost (GitHub charges nothing for it). It is
about page load time on the README and Pages, and about git history weight: a
committed PNG stays in `.git` forever, so every re-capture adds another copy.

## Aspect ratio: design for 16:10 landscape

The design target for every screenshot is a 16:10 landscape frame; at the
1920 px ceiling that is 1920x1200. This is the shape README screenshots read
best in, and it pairs with the width ceiling: a 16:10 capture at or below 1920 px
wide needs no resize at all.

How much control you have over the ratio depends on the capture kind:

- Synthetic captures let the coder set the exact pixels, so hit 16:10 dead on.
  The Playwright viewport is set to 1280x800 in `scripts/screenshot_web.mjs`
  (bump to 1920x1200 for more detail). A terminal-output render
  (`scripts/capture_cli.sh`) is sized by its text, so pad it toward a 16:10
  canvas rather than committing a thin strip.
- Real app windows only approximate 16:10: size the window as close as the app
  allows before capturing.

A wider landscape (16:9) is acceptable; reserve portrait or tall shapes for
content that is genuinely vertical, since those render small in the README
column.

Aspect ratio is a capture-time choice. The resize step below only bounds size;
it preserves whatever ratio you captured and never crops or pads to reach 16:10.

## Resize only when the longer edge exceeds 1920 px

A Retina capture is often 2560 px or 3840 px wide and several MB. Downscaling
those to the 1920 px ceiling is the step that brings them under budget while
keeping full-detail-on-click. A capture whose longer edge is already at or below
1920 px needs no resize. The `1920x1920>` argument is a bounding box, not target
dimensions: it scales the image down to fit inside 1920x1920 while preserving
aspect ratio, so it never crops, pads, squares, or enlarges. A 2560x1600 (16:10)
capture becomes 1920x1200, still 16:10. Use `convert` or `magick` (whichever is
on the PATH; both are ImageMagick):

```bash
convert /tmp/capture.png -resize '1920x1920>' /tmp/capture.png
cp /tmp/capture.png docs/screenshots/main_window.png
```

The `>` suffix only shrinks images larger than the target, so a capture whose
longer edge is already at or below 1920 px is left untouched.

If ImageMagick is unavailable, resize with Pillow (`pillow` in
`pip_requirements.txt`):

```python
import PIL.Image
img = PIL.Image.open('/tmp/capture.png')
img.thumbnail((1920, 1920))           # in-place, preserves aspect ratio
img.save('/tmp/capture.png')
```

## Optional: lossless optimize

Resize does the heavy lifting. If `optipng` or `pngcrush` happens to be
installed, you may crush the resized `/tmp` file for a further 5 to 20 percent.
Use this optional step when either tool is already on the PATH, and keep the capture
workflow dependency-free:

```bash
optipng -o3 /tmp/capture.png            # or: pngcrush -rem allb -reduce /tmp/capture.png /tmp/capture_crushed.png
```

## Summary workflow

```bash
# 1. Capture into /tmp (see embedding.md for capture commands)
screenshot --window "App Name" /tmp/capture.png

# 2. Resize only when the longer edge exceeds the 1920 px ceiling
convert /tmp/capture.png -resize '1920x1920>' /tmp/capture.png

# 3. Optional: lossless crush, only if optipng/pngcrush is already installed
optipng -o3 /tmp/capture.png

# 4. Copy finished PNG into the committed folder
cp /tmp/capture.png docs/screenshots/main_window.png
```
