#!/usr/bin/env python3
"""Archive book sources that map uniquely to validated Markdown deliveries."""

# Standard Library
import re
import json
import pathlib
import argparse
import collections

# local repo modules
import validate_markdown_delivery


SOURCE_SUFFIXES = {
	".djvu",
	".docx",
	".epub",
	".htm",
	".html",
	".odt",
	".pdf",
	".txt",
}
SOURCE_PATTERN = re.compile(r"^source(?:_[a-z]+)?:\s*(.+?)\s*$")
TERMINAL_ISSUE_LIMIT = 30


#============================================
def inside(path: pathlib.Path, parent: pathlib.Path) -> bool:
	"""Return whether one path is the parent itself or one of its descendants."""
	contained = path == parent or parent in path.parents
	return contained


#============================================
def markdown_sources(markdown_path: pathlib.Path) -> list[str]:
	"""Return source basenames declared in one Markdown frontmatter block."""
	lines = markdown_path.read_text(encoding="utf-8", errors="replace").splitlines()
	if not lines or lines[0].strip() != "---":
		return []
	sources: list[str] = []
	for line in lines[1:]:
		if line.strip() == "---":
			break
		match = SOURCE_PATTERN.match(line)
		if match is None:
			continue
		value = match.group(1).strip().strip("\"'")
		basename = pathlib.PurePosixPath(value).name
		if basename:
			sources.append(basename)
	return sources


#============================================
def markdown_paths(root: pathlib.Path, archive: pathlib.Path) -> list[pathlib.Path]:
	"""Return Markdown delivery files outside the source archive."""
	paths = sorted(
		path for path in root.rglob("*.md")
		if path.is_file() and not inside(path, archive)
	)
	return paths


#============================================
def source_paths(root: pathlib.Path, archive: pathlib.Path) -> list[pathlib.Path]:
	"""Return active source-format files outside the archive."""
	paths = sorted(
		path for path in root.rglob("*")
		if path.is_file()
		and path.suffix.lower() in SOURCE_SUFFIXES
		and not inside(path, archive)
	)
	return paths


#============================================
def archived_source_paths(archive: pathlib.Path) -> list[pathlib.Path]:
	"""Return source-format files already inside the archive."""
	if not archive.exists():
		return []
	paths = sorted(
		path for path in archive.rglob("*")
		if path.is_file() and path.suffix.lower() in SOURCE_SUFFIXES
	)
	return paths


#============================================
def paths_by_name(paths: list[pathlib.Path]) -> dict[str, list[pathlib.Path]]:
	"""Group paths by basename for metadata matching."""
	grouped: dict[str, list[pathlib.Path]] = {}
	for path in paths:
		grouped.setdefault(path.name, []).append(path)
	return grouped


#============================================
def issue(code: str, message: str) -> dict[str, str]:
	"""Build one JSON-ready archive planning issue."""
	result = {"code": code, "message": message}
	return result


#============================================
def archive_plan(
		root: pathlib.Path, archive: pathlib.Path,
		) -> tuple[dict[str, object], list[tuple[pathlib.Path, pathlib.Path]]]:
	"""Build a safe archive plan from delivery validation and source metadata."""
	markdown_files = markdown_paths(root, archive)
	active_sources = source_paths(root, archive)
	archived_sources = archived_source_paths(archive)
	issues: list[dict[str, str]] = []
	mappings: list[tuple[pathlib.Path, str]] = []
	for markdown_path in markdown_files:
		validation = validate_markdown_delivery.validate_delivery(markdown_path)
		if validation["status"] != "PASS":
			issues.append(issue(
				"invalid-markdown",
				f"{markdown_path} has {validation['issue_count']} delivery issues",
			))
			continue
		declared_sources = markdown_sources(markdown_path)
		if not declared_sources:
			issues.append(issue(
				"missing-source-metadata",
				f"{markdown_path} has no source or source_* frontmatter field",
			))
			continue
		for source_name in declared_sources:
			mappings.append((markdown_path, source_name))
	mapping_counts = collections.Counter(source_name for _path, source_name in mappings)
	for source_name, count in sorted(mapping_counts.items()):
		if count > 1:
			issues.append(issue(
				"duplicate-mapping",
				f"{source_name} is declared by {count} Markdown files",
			))
	active_by_name = paths_by_name(active_sources)
	archived_by_name = paths_by_name(archived_sources)
	for source_name, paths in sorted(active_by_name.items()):
		if len(paths) > 1:
			issues.append(issue(
				"duplicate-active-source",
				f"{source_name} has {len(paths)} active paths",
			))
	for source_name, paths in sorted(archived_by_name.items()):
		if len(paths) > 1:
			issues.append(issue(
				"duplicate-archived-source",
				f"{source_name} has {len(paths)} archived paths",
			))
	moves: list[tuple[pathlib.Path, pathlib.Path]] = []
	already_archived: list[str] = []
	mapped_names = set(mapping_counts)
	for source_name in sorted(mapped_names):
		active_matches = active_by_name.get(source_name, [])
		archived_matches = archived_by_name.get(source_name, [])
		if len(active_matches) == 1 and not archived_matches:
			source = active_matches[0]
			target = archive / source.relative_to(root)
			if target.exists():
				issues.append(issue(
					"archive-collision", f"archive target already exists: {target}",
				))
			else:
				moves.append((source, target))
		elif not active_matches and len(archived_matches) == 1:
			already_archived.append(str(archived_matches[0]))
		elif not active_matches and not archived_matches:
			issues.append(issue(
				"missing-source", f"no source file matches metadata basename {source_name}",
			))
		elif active_matches and archived_matches:
			issues.append(issue(
				"active-and-archived",
				f"{source_name} exists in both active and archived locations",
			))
	unmapped_sources = [
		str(path) for path in active_sources if path.name not in mapped_names
	]
	report: dict[str, object] = {
		"root": str(root),
		"archive": str(archive),
		"status": "PASS" if not issues else "FAIL",
		"markdown_count": len(markdown_files),
		"mapped_source_count": len(mapped_names),
		"planned_move_count": len(moves),
		"already_archived_count": len(already_archived),
		"unmapped_active_count": len(unmapped_sources),
		"planned_moves": [
			{"source": str(source), "target": str(target)} for source, target in moves
		],
		"already_archived": already_archived,
		"unmapped_active_sources": unmapped_sources,
		"issues": issues,
	}
	return report, moves


#============================================
def archive_processed_sources(
		root: pathlib.Path, archive: pathlib.Path, move: bool,
		) -> dict[str, object]:
	"""Audit mappings and optionally move only safe, validated source matches."""
	report, moves = archive_plan(root, archive)
	report["mode"] = "move" if move else "dry-run"
	report["moved_count"] = 0
	if report["status"] != "PASS" or not move:
		return report
	for source, target in moves:
		target.parent.mkdir(parents=True, exist_ok=True)
		source.rename(target)
	report["moved_count"] = len(moves)
	return report


#============================================
def print_report(report: dict[str, object]) -> None:
	"""Print compact archive evidence and bounded failures."""
	print(f"Processed-source archive: {report['status']}")
	print(f"Mode: {report['mode']}")
	print(f"Markdown files: {report['markdown_count']}")
	print(f"Mapped sources: {report['mapped_source_count']}")
	print(f"Planned moves: {report['planned_move_count']}")
	print(f"Already archived: {report['already_archived_count']}")
	print(f"Unmapped active sources left in place: {report['unmapped_active_count']}")
	if report["mode"] == "move":
		print(f"Sources moved: {report['moved_count']}")
	for item in list(report["issues"])[:TERMINAL_ISSUE_LIMIT]:
		print(f"- [{item['code']}] {item['message']}")


#============================================
def parse_args() -> argparse.Namespace:
	"""Parse the delivery root, archive path, and explicit mutation mode."""
	parser = argparse.ArgumentParser(
		description="Archive source files mapped to validated Markdown books",
	)
	parser.add_argument("input", help="Book processing root containing sources and Markdown")
	parser.add_argument(
		"-a", "--archive", dest="archive",
		help="Archive directory; defaults to INPUT/COMPLETED_SOURCE",
	)
	mode_group = parser.add_mutually_exclusive_group()
	mode_group.add_argument(
		"-m", "--move", dest="move", action="store_true",
		help="Move validated mapped sources into the archive",
	)
	mode_group.add_argument(
		"-n", "--dry-run", dest="move", action="store_false",
		help="Audit and print the plan without moving files",
	)
	parser.set_defaults(move=False)
	parser.add_argument("-j", "--json-report", dest="json_report", help="Write an ASCII JSON report")
	args = parser.parse_args()
	return args


#============================================
def main() -> int:
	"""Audit or apply one processed-source archive operation."""
	args = parse_args()
	root = pathlib.Path(args.input)
	archive = pathlib.Path(args.archive) if args.archive else root / "COMPLETED_SOURCE"
	report = archive_processed_sources(root, archive, args.move)
	print_report(report)
	if args.json_report:
		json_path = pathlib.Path(args.json_report)
		json_text = json.dumps(report, indent=2, ensure_ascii=True) + "\n"
		json_path.write_text(json_text, encoding="ascii")
		print(f"JSON report: {json_path}")
	exit_status = 0 if report["status"] == "PASS" else 1
	return exit_status


#============================================
if __name__ == "__main__":
	raise SystemExit(main())
