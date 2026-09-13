#!/usr/bin/env bash
#
# Render a spreadsheet or document artifact to a landscape PNG.
# Preparation, usage, and output contracts live in
# ../references/capture_local.md#document-and-spreadsheet-artifacts.

set -euo pipefail

output="${1:-}"
artifact="${2:-}"

#============================================
# Validate arguments.
if [ -z "${output}" ] || [ -z "${artifact}" ]; then
	echo "Usage: render_artifact_libreoffice.sh OUTPUT.png INPUT_ARTIFACT" >&2
	exit 1
fi
if [ ! -f "${artifact}" ]; then
	echo "Error: artifact not found: ${artifact}" >&2
	exit 1
fi

#============================================
# Resolve the soffice binary.
SOFFICE="soffice"
if ! command -v soffice > /dev/null 2>&1; then
	if [ -x "/opt/homebrew/bin/soffice" ]; then
		SOFFICE="/opt/homebrew/bin/soffice"
	else
		echo "Error: soffice not found on PATH or at /opt/homebrew/bin/soffice" >&2
		echo "Install LibreOffice (brew install --cask libreoffice) and re-run." >&2
		exit 1
	fi
fi

#============================================
# Copy the artifact to /tmp so LibreOffice writes its output there
# (required by the permission hook's scope for write-capable tools).
artifact_basename="$(basename "${artifact}")"
tmp_artifact="/tmp/${artifact_basename}"
cp "${artifact}" "${tmp_artifact}"

#============================================
# Convert the artifact to PDF with LibreOffice headless.
# One wide landscape page per sheet (page setup must be pre-applied by caller).
"${SOFFICE}" --headless --convert-to pdf --outdir /tmp "${tmp_artifact}"

# Derive the PDF path: LibreOffice replaces the extension with .pdf.
artifact_stem="${artifact_basename%.*}"
tmp_pdf="/tmp/${artifact_stem}.pdf"
if [ ! -f "${tmp_pdf}" ]; then
	echo "Error: expected LibreOffice output not found: ${tmp_pdf}" >&2
	exit 1
fi

#============================================
# Render page 1 of the PDF to a PNG with ImageMagick.
# -density 150: 150 dpi -- crisp without huge file size.
# -flatten on white: merge any transparency layer so the background is white.
# -trim: remove surrounding whitespace so the image is tight to the content.
# +repage: reset the canvas after trim.
# Resize so the longer edge is 1920 px max, matching the screenshot budget
# in references/postprocess.md, to keep the README embed reasonable.
tmp_png="/tmp/${artifact_stem}_render.png"
magick -density 150 "${tmp_pdf}[0]" \
	-background white -flatten \
	-trim +repage \
	-resize '1920x1920>' \
	"${tmp_png}"

#============================================
# Copy the finished PNG to the requested output path.
cp "${tmp_png}" "${output}"
echo "Wrote ${output}"
