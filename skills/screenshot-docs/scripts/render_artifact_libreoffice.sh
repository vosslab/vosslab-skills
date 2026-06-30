#!/usr/bin/env bash
#
# render_artifact_libreoffice.sh - render a spreadsheet or document artifact
# to a full-width landscape PNG via LibreOffice headless + ImageMagick.
#
# The repo permission hook scopes ImageMagick and write tools to /tmp, so all
# intermediate work happens in /tmp; the finished PNG is then copied to the
# requested output path.
#
# For a spreadsheet artifact, the caller should pre-set landscape + fit-to-one-
# page-wide with openpyxl BEFORE calling this script, so no columns are clipped:
#
#   import openpyxl.worksheet.properties
#   ws.page_setup.orientation = "landscape"
#   ws.page_setup.fitToWidth = 1
#   ws.page_setup.fitToHeight = 0
#   ws.sheet_properties.pageSetUpPr = \
#       openpyxl.worksheet.properties.PageSetupProperties(fitToPage=True)
#   # optional: set full print area and narrow margins
#   ws.print_area = f"A1:{ws.cell(ws.max_row, ws.max_column).coordinate}"
#   ws.page_margins = openpyxl.worksheet.page.PageMargins(
#       left=0.25, right=0.25, top=0.25, bottom=0.25)
#
# soffice is commonly at /opt/homebrew/bin/soffice on macOS. If the bare
# `soffice` command is not found on PATH the script falls back to that path.
#
# Usage:
#   render_artifact_libreoffice.sh OUTPUT.png INPUT_ARTIFACT
#
# Examples:
#   render_artifact_libreoffice.sh /tmp/grid.png /tmp/schedule.xlsx
#   render_artifact_libreoffice.sh docs/screenshots/report.png /tmp/report.pdf

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
# Resize to 2000 px wide max to keep file size reasonable for a README embed.
tmp_png="/tmp/${artifact_stem}_render.png"
magick -density 150 "${tmp_pdf}[0]" \
	-background white -flatten \
	-trim +repage \
	-resize '2000x>' \
	"${tmp_png}"

#============================================
# Copy the finished PNG to the requested output path.
cp "${tmp_png}" "${output}"
echo "Wrote ${output}"
