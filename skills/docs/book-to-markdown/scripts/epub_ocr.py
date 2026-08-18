#!/usr/bin/env python3
"""OCR image-scan EPUBs: extract page images in order, OCR each with Tesseract,
assemble one markdown file with page separators. Used for EPUBs whose text layer
is empty (all pages are scans) - the calibrated-ladder exception for EPUBs.
Requires Tesseract on PATH (rootless install: export PATH/LD_LIBRARY_PATH/
TESSDATA_PREFIX pointing at the tesseract root first).
Usage: python3 epub_ocr.py <input.epub> <output.md> <workdir>
"""
import sys, os, re, zipfile, subprocess

PAGE_IMAGE_PATTERN = re.compile(r"(\d+)\.(?:jpe?g|png|gif|webp)$", re.I)


def page_sort_key(name: str) -> int:
    # files like cover00519.jpeg or 00519.png - take the trailing digits
    m = PAGE_IMAGE_PATTERN.search(name)
    return int(m.group(1)) if m else 10**9


def main() -> None:
    epub, out_md, workdir = sys.argv[1], sys.argv[2], sys.argv[3]
    os.makedirs(workdir, exist_ok=True)
    try:
        subprocess.run(["tesseract", "--version"], capture_output=True, timeout=30)
    except (FileNotFoundError, OSError) as error:
        raise RuntimeError(
            "OCR requires Tesseract on PATH. Rootless install: download the "
            "tesseract-ocr .debs, extract with dpkg -x into a prefix, and export "
            "PATH/LD_LIBRARY_PATH/TESSDATA_PREFIX to that prefix."
        ) from error
    z = zipfile.ZipFile(epub)
    # Only images whose names carry a trailing page digit are scan pages; covers,
    # logos, and decorative art have no page number and are not OCR targets.
    imgs = sorted(
        [name for name in z.namelist() if PAGE_IMAGE_PATTERN.search(name)],
        key=page_sort_key,
    )
    print(f"pages to OCR: {len(imgs)}", flush=True)

    chunks = []
    for i, name in enumerate(imgs, 1):
        ext = os.path.splitext(name)[1].lower()
        tmp = os.path.join(workdir, f"page_{i:04d}{ext}")
        with open(tmp, "wb") as fh:
            fh.write(z.read(name))
        try:
            r = subprocess.run(["tesseract", tmp, "stdout", "--psm", "3"],
                               capture_output=True, text=True, timeout=120)
            text = r.stdout
        except Exception as e:
            text = f"\n[OCR ERROR page {i}: {e}]\n"
        chunks.append(f"\n\n<!-- PAGE {i} -->\n\n{text.strip()}")
        if i % 25 == 0:
            print(f"  ocr'd {i}/{len(imgs)}", flush=True)
        os.remove(tmp)

    title = os.path.splitext(os.path.basename(epub))[0]
    with open(out_md, "w") as fh:
        fh.write(f"---\ntitle: \"{title}\"\nsource: \"{os.path.basename(epub)}\"\nnote: \"OCR of image-scan EPUB\"\n---\n\n# {title}\n")
        fh.write("\n".join(chunks))
    print(f"DONE -> {out_md} ({os.path.getsize(out_md)} bytes)", flush=True)


if __name__ == "__main__":
    main()
