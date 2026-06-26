# Post-processing screenshots before committing

Apply these steps after capturing a screenshot and before copying it into
`docs/screenshots/`.

## Hook constraint: process under /tmp

The repo permission hook scopes image tools (`optipng`, `pngcrush`, `convert`,
`magick`, and similar) to `/tmp` paths only. Process all images while they
live under `/tmp`, then copy the finished PNG into `docs/screenshots/` with `cp`.

```
Capture -> /tmp/capture.png
Optimize -> /tmp/capture_opt.png   (still under /tmp)
Copy     -> docs/screenshots/main_window.png
```

## Size budget

Keep each PNG under 500 KB. Anything over 1 MB requires a written justification
in the PR description or CHANGELOG entry (for example, a high-resolution diagram
that must stay sharp). Match the budget documented in
`skills/screenshot-docs/references/embedding.md`.

## Optimize with optipng

Run `optipng` on the `/tmp` file before copying:

```bash
optipng -o3 /tmp/capture.png
cp /tmp/capture.png docs/screenshots/main_window.png
```

Use `-o3` for a good balance between compression level and speed. Use `-o7`
for maximum compression on large files where build time permits.

## Optimize with pngcrush

Use `pngcrush` as an alternative when `optipng` is unavailable:

```bash
pngcrush -rem allb -reduce /tmp/capture.png /tmp/capture_crushed.png
cp /tmp/capture_crushed.png docs/screenshots/main_window.png
```

## Resize with convert (ImageMagick)

Resize an oversized screenshot under `/tmp` before optimizing:

```bash
convert /tmp/capture.png -resize 1280x800 /tmp/capture_resized.png
optipng -o3 /tmp/capture_resized.png
cp /tmp/capture_resized.png docs/screenshots/main_window.png
```

The `>` suffix limits resize to images larger than the target dimension:

```bash
convert /tmp/capture.png -resize '1280x800>' /tmp/capture_resized.png
```

Both `convert` and `magick` refer to ImageMagick; use whichever is on the PATH.
Both are scoped to `/tmp` paths by the hook, so keep all intermediate files
under `/tmp` until the final `cp`.

## Crop with Python Pillow

Pillow is available in `pip_requirements.txt` as `pillow`. Use it for
crop or resize when ImageMagick is unavailable or when a Python pipeline
already has the image in memory.

Example crop to a bounding box:

```python
import PIL.Image
img = PIL.Image.open('/tmp/capture.png')
# crop(left, upper, right, lower)
cropped = img.crop((0, 0, 1280, 800))
cropped.save('/tmp/capture_cropped.png')
```

Run the script with `python3 _temp_crop.py`, then copy:

```bash
cp /tmp/capture_cropped.png docs/screenshots/main_window.png
```

## Summary workflow

```bash
# 1. Capture into /tmp (see embedding.md for capture commands)
screenshot --window "App Name" /tmp/capture.png

# 2. Resize if needed (ImageMagick, still under /tmp)
convert /tmp/capture.png -resize '1280x800>' /tmp/capture.png

# 3. Optimize in place under /tmp
optipng -o3 /tmp/capture.png

# 4. Copy finished PNG into the committed folder
cp /tmp/capture.png docs/screenshots/main_window.png
```
