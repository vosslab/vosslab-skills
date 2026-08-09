#!/usr/bin/env python3
"""Protect malformed Markdown pipe blocks as literal text for later repair."""

import json
import pathlib
import argparse
import dataclasses

import markdown_quality


#============================================
def fence_for(text: str) -> str:
	"""Return a backtick fence longer than any run inside the protected text."""
	longest = 0
	current = 0
	for character in text:
		if character == "`":
			current += 1
			longest = max(longest, current)
		else:
			current = 0
	marker = "`" * max(3, longest + 1)
	return marker


#============================================
def wrap_malformed_pipe_blocks(text: str) -> tuple[str, list[markdown_quality.TableIssue]]:
	"""Wrap detected malformed pipe blocks while preserving their text exactly."""
	issues = markdown_quality.find_malformed_pipe_blocks(text)
	if not issues:
		return text, issues
	lines = text.splitlines()
	output: list[str] = []
	line_index = 0
	for issue in issues:
		start = issue.line_start - 1
		end = issue.line_end
		output.extend(lines[line_index:start])
		marker = fence_for(issue.text)
		output.append(marker + "text")
		output.extend(lines[start:end])
		output.append(marker)
		line_index = end
	output.extend(lines[line_index:])
	wrapped = "\n".join(output)
	if text.endswith("\n"):
		wrapped += "\n"
	return wrapped, issues


#============================================
def parse_args() -> argparse.Namespace:
	"""Parse explicit input, output, and optional report paths."""
	parser = argparse.ArgumentParser(
		description="Wrap malformed pipe blocks as text without overwriting the source",
	)
	parser.add_argument("-i", "--input", dest="input_file", required=True, help="Markdown input")
	parser.add_argument(
		"-o", "--output", dest="output_file", required=True,
		help="Separate Markdown output",
	)
	parser.add_argument("-j", "--json-report", dest="json_report", help="Write a JSON repair report")
	args = parser.parse_args()
	return args


#============================================
def main() -> None:
	"""Write a separate protected candidate and an optional audit report."""
	args = parse_args()
	input_path = pathlib.Path(args.input_file)
	output_path = pathlib.Path(args.output_file)
	if input_path.resolve() == output_path.resolve():
		raise ValueError(
			"input and output must differ; review the protected candidate before replacement"
		)
	text = input_path.read_text(encoding="utf-8", errors="replace")
	wrapped, issues = wrap_malformed_pipe_blocks(text)
	output_path.write_text(wrapped, encoding="utf-8")
	report: dict[str, object] = {
		"input": str(input_path),
		"output": str(output_path),
		"wrapped_block_count": len(issues),
		"wrapped_blocks": [dataclasses.asdict(item) for item in issues],
	}
	print(f"Malformed pipe blocks wrapped: {len(issues)}")
	print(f"Output: {output_path}")
	if args.json_report:
		json_path = pathlib.Path(args.json_report)
		json_path.write_text(json.dumps(report, indent=2, ensure_ascii=True) + "\n", encoding="ascii")
		print(f"JSON report: {json_path}")


#============================================
if __name__ == "__main__":
	main()
