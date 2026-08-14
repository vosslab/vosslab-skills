#!/usr/bin/env bash

# Convert a short source video into a palette-optimized animated GIF for README use.

set -euo pipefail

if [[ $# -lt 2 || $# -gt 5 ]]; then
	printf 'Usage: %s INPUT_VIDEO OUTPUT_GIF [WIDTH] [FPS] [DURATION_SECONDS]\n' "$0" >&2
	exit 2
fi

input_path=$1
output_path=$2
width=${3:-960}
fps=${4:-12}
duration=${5:-5}

if [[ ! -f "$input_path" ]]; then
	printf 'Input video does not exist: %s\n' "$input_path" >&2
	exit 2
fi

if [[ "$output_path" != *.gif ]]; then
	printf 'Output path must end in .gif: %s\n' "$output_path" >&2
	exit 2
fi

if ! command -v ffmpeg >/dev/null 2>&1; then
	printf 'ffmpeg is required to create an animated GIF.\n' >&2
	exit 127
fi

if ! [[ "$width" =~ ^[1-9][0-9]*$ && "$fps" =~ ^[1-9][0-9]*$ ]]; then
	printf 'WIDTH and FPS must be positive integers.\n' >&2
	exit 2
fi

if (( width < 800 || width > 1200 )); then
	printf 'WIDTH must be from 800 through 1200 pixels.\n' >&2
	exit 2
fi

if (( fps < 1 || fps > 15 )); then
	printf 'FPS must be from 1 through 15.\n' >&2
	exit 2
fi

if ! [[ "$duration" =~ ^[1-5]$ ]]; then
	printf 'DURATION_SECONDS must be an integer from 1 through 5.\n' >&2
	exit 2
fi

output_dir=${output_path%/*}
if [[ "$output_dir" == "$output_path" ]]; then
	output_dir=.
fi
output_name=${output_path##*/}

if [[ ! -d "$output_dir" ]]; then
	printf 'Output directory does not exist: %s\n' "$output_dir" >&2
	exit 2
fi

temp_dir=$(mktemp -d "${output_dir}/.${output_name}.tmp.XXXXXX")
temp_path="${temp_dir}/${output_name}"

cleanup() {
	rm -rf -- "$temp_dir"
}
trap cleanup EXIT HUP INT TERM

ffmpeg -hide_banner -loglevel error -y \
	-i "$input_path" \
	-t "$duration" \
	-an \
	-filter_complex \
	"fps=${fps},scale=${width}:-1:flags=lanczos,split[frames][palette_input];[palette_input]palettegen=max_colors=128:stats_mode=diff[palette];[frames][palette]paletteuse=dither=bayer:bayer_scale=3:diff_mode=rectangle" \
	-loop -1 \
	"$temp_path"

file_size=$(wc -c < "$temp_path")
max_file_size=$((5 * 1024 * 1024))
if (( file_size > max_file_size )); then
	printf 'GIF exceeds the 5 MB budget: %s bytes. Reduce duration, FPS, or width.\n' \
		"$file_size" >&2
	exit 1
fi

mv -f -- "$temp_path" "$output_path"
printf 'Wrote animated GIF: %s\n' "$output_path"
