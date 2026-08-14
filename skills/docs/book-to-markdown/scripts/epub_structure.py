#!/usr/bin/env python3
"""Measure flat EPUB structure and create a source-preserving semantic candidate."""

# Standard Library
import re
import json
import pathlib
import zipfile
import argparse
import posixpath
import collections
import urllib.parse

# PIP3 modules
import lxml.etree


CONTAINER_PATH = "META-INF/container.xml"
EPUB_NAMESPACE = "http://www.idpf.org/2007/ops"
PROMINENT_SAMPLE_LIMIT = 5
CSS_RULE_PATTERN = re.compile(r"([^{}]+)\{([^{}]*)\}")
CSS_CLASS_PATTERN = re.compile(r"\.([A-Za-z_][A-Za-z0-9_-]*)")
LEADING_MARKER_PATTERN = re.compile(r"^(\s*)(?:[*+-]|\u2022)\s+")


#============================================
def local_name(tag: str) -> str:
	"""Return an XML tag without its namespace."""
	name = tag.rsplit("}", 1)[-1]
	return name


#============================================
def namespace_name(tag: str) -> str:
	"""Return the namespace prefix embedded in an ElementTree tag."""
	if tag.startswith("{"):
		namespace = tag.split("}", 1)[0] + "}"
	else:
		namespace = ""
	return namespace


#============================================
def normalized_text(element: lxml.etree._Element) -> str:
	"""Return visible element text with presentation whitespace collapsed."""
	text = " ".join("".join(element.itertext()).split())
	return text


#============================================
def archive_path(base_path: str, href: str) -> str:
	"""Resolve an EPUB-relative href to one normalized archive path."""
	clean_href = urllib.parse.unquote(href.split("#", 1)[0])
	base_directory = posixpath.dirname(base_path)
	resolved = posixpath.normpath(posixpath.join(base_directory, clean_href))
	return resolved


#============================================
def first_element(
		root: lxml.etree._Element, name: str,
		attribute: str | None = None, value: str | None = None,
		) -> lxml.etree._Element | None:
	"""Return the first descendant matching a local tag and optional attribute."""
	for element in root.iter():
		if local_name(element.tag) != name:
			continue
		if attribute is not None and element.attrib.get(attribute) != value:
			continue
		return element
	return None


#============================================
def parse_xml(entries: dict[str, bytes], path: str) -> lxml.etree._Element:
	"""Parse one required XML resource without DTDs or external entities."""
	if path not in entries:
		raise ValueError(f"EPUB is missing required entry: {path}")
	xml_bytes = entries[path]
	if re.search(br"<!DOCTYPE", xml_bytes, re.IGNORECASE):
		raise ValueError(f"EPUB XML must not contain a DOCTYPE declaration: {path}")
	parser = lxml.etree.XMLParser(
		resolve_entities=False,
		no_network=True,
		load_dtd=False,
		dtd_validation=False,
		recover=False,
		huge_tree=False,
		remove_comments=True,
		remove_pis=True,
	)
	root = lxml.etree.fromstring(xml_bytes, parser=parser)
	return root


#============================================
def metadata_value(root: lxml.etree._Element, name: str) -> str:
	"""Return one normalized Dublin Core metadata value when present."""
	element = first_element(root, name)
	value = normalized_text(element) if element is not None else ""
	return value


#============================================
def load_epub(epub_path: pathlib.Path) -> tuple[list[zipfile.ZipInfo], dict[str, bytes], bytes]:
	"""Load ordered EPUB entries and the archive comment."""
	with zipfile.ZipFile(epub_path) as archive:
		infos = archive.infolist()
		entries = {info.filename: archive.read(info.filename) for info in infos}
		comment = archive.comment
	return infos, entries, comment


#============================================
def manifest_and_spine(
		entries: dict[str, bytes],
		) -> tuple[str, lxml.etree._Element, dict[str, dict[str, str]], list[str]]:
	"""Resolve the package document, manifest, and ordered content spine."""
	container_root = parse_xml(entries, CONTAINER_PATH)
	rootfile = first_element(container_root, "rootfile")
	if rootfile is None or "full-path" not in rootfile.attrib:
		raise ValueError("EPUB container does not identify a package document")
	opf_path = rootfile.attrib["full-path"]
	opf_root = parse_xml(entries, opf_path)
	manifest: dict[str, dict[str, str]] = {}
	for element in opf_root.iter():
		if local_name(element.tag) != "item":
			continue
		item_id = element.attrib["id"]
		manifest[item_id] = {
			"href": element.attrib["href"],
			"media_type": element.attrib["media-type"],
			"properties": element.attrib.get("properties", ""),
		}
	spine_paths: list[str] = []
	for element in opf_root.iter():
		if local_name(element.tag) != "itemref":
			continue
		item = manifest[element.attrib["idref"]]
		spine_paths.append(archive_path(opf_path, item["href"]))
	return opf_path, opf_root, manifest, spine_paths


#============================================
def nav_path(opf_path: str, manifest: dict[str, dict[str, str]]) -> str | None:
	"""Return the EPUB 3 navigation document path when declared."""
	for item in manifest.values():
		properties = item["properties"].split()
		if "nav" in properties:
			return archive_path(opf_path, item["href"])
	return None


#============================================
def navigation_facts(
		entries: dict[str, bytes], path: str | None,
		) -> tuple[int, str | None]:
	"""Return TOC entry count and the declared body-matter document."""
	if path is None:
		return 0, None
	root = parse_xml(entries, path)
	toc_entries = 0
	body_start: str | None = None
	epub_type = f"{{{EPUB_NAMESPACE}}}type"
	for navigation in root.iter():
		if local_name(navigation.tag) != "nav":
			continue
		navigation_types = navigation.attrib.get(epub_type, "").split()
		if "toc" in navigation_types:
			toc_entries = sum(1 for item in navigation.iter() if local_name(item.tag) == "a")
		if "landmarks" not in navigation_types:
			continue
		for link in navigation.iter():
			if local_name(link.tag) != "a":
				continue
			link_types = link.attrib.get(epub_type, "").split()
			if "bodymatter" in link_types:
				body_start = archive_path(path, link.attrib["href"])
				break
	return toc_entries, body_start


#============================================
def css_properties(entries: dict[str, bytes], css_paths: list[str]) -> dict[str, dict[str, str]]:
	"""Return simple class declarations from stylesheets bundled in the EPUB."""
	styles: dict[str, dict[str, str]] = {}
	for path in css_paths:
		css_text = entries[path].decode("utf-8", errors="replace")
		for selector_text, declaration_text in CSS_RULE_PATTERN.findall(css_text):
			properties: dict[str, str] = {}
			for declaration in declaration_text.split(";"):
				if ":" not in declaration:
					continue
				name, value = declaration.split(":", 1)
				properties[name.strip().lower()] = value.strip().lower()
			for class_name in CSS_CLASS_PATTERN.findall(selector_text):
				styles.setdefault(class_name, {}).update(properties)
	return styles


#============================================
def font_size_em(properties: dict[str, str]) -> float | None:
	"""Normalize a CSS font size to an approximate em value."""
	value = properties.get("font-size", "")
	match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)(em|rem|px|%)", value)
	if match is None:
		return None
	size = float(match.group(1))
	unit = match.group(2)
	if unit == "px":
		size /= 16.0
	elif unit == "%":
		size /= 100.0
	return size


#============================================
def is_bold(properties: dict[str, str]) -> bool:
	"""Return whether a CSS declaration requests visibly bold text."""
	weight = properties.get("font-weight", "")
	if weight in {"bold", "bolder"}:
		return True
	if weight.isdigit() and int(weight) >= 600:
		return True
	return False


#============================================
def prominent_style(properties: dict[str, str], descendant_bold: bool) -> bool:
	"""Return whether a paragraph style is visually plausible as a heading."""
	size = font_size_em(properties)
	if size is None:
		return False
	prominent = size >= 1.5 or (size >= 1.3 and (is_bold(properties) or descendant_bold))
	return prominent


#============================================
def paragraph_facts(
		entries: dict[str, bytes], spine_paths: list[str], styles: dict[str, dict[str, str]],
		) -> tuple[int, collections.Counter[str], dict[str, list[str]], set[str]]:
	"""Count native headings and collect bounded paragraph-class samples."""
	heading_count = 0
	class_counts: collections.Counter[str] = collections.Counter()
	class_samples: dict[str, list[str]] = {}
	descendant_bold_classes: set[str] = set()
	for path in spine_paths:
		root = parse_xml(entries, path)
		for element in root.iter():
			name = local_name(element.tag)
			if re.fullmatch(r"h[1-6]", name):
				heading_count += 1
			if name != "p":
				continue
			text = normalized_text(element)
			paragraph_classes = element.attrib.get("class", "").split()
			descendant_bold = any(
				is_bold(styles.get(class_name, {}))
				for child in element.iter()
				if child is not element
				for class_name in child.attrib.get("class", "").split()
			)
			for class_name in paragraph_classes:
				class_counts[class_name] += 1
				if descendant_bold:
					descendant_bold_classes.add(class_name)
				samples = class_samples.setdefault(class_name, [])
				if text and text not in samples and len(samples) < PROMINENT_SAMPLE_LIMIT:
					samples.append(text)
	return heading_count, class_counts, class_samples, descendant_bold_classes


#============================================
def inspect_epub(epub_path: pathlib.Path) -> dict[str, object]:
	"""Measure semantic and presentation structure without changing the EPUB."""
	_infos, entries, _comment = load_epub(epub_path)
	opf_path, opf_root, manifest, spine_paths = manifest_and_spine(entries)
	navigation_path = nav_path(opf_path, manifest)
	toc_entries, body_start = navigation_facts(entries, navigation_path)
	if body_start in spine_paths:
		body_index = spine_paths.index(body_start)
		measured_paths = spine_paths[body_index:]
	else:
		measured_paths = spine_paths
	css_paths = [
		archive_path(opf_path, item["href"])
		for item in manifest.values()
		if item["media_type"] == "text/css"
	]
	styles = css_properties(entries, css_paths)
	(
		heading_count, class_counts, class_samples, descendant_bold_classes,
	) = paragraph_facts(entries, measured_paths, styles)
	candidates: list[dict[str, object]] = []
	for class_name, count in class_counts.items():
		properties = styles.get(class_name, {})
		effective_bold = is_bold(properties) or class_name in descendant_bold_classes
		if not class_samples.get(class_name) or not prominent_style(properties, effective_bold):
			continue
		candidate: dict[str, object] = {
			"class": class_name,
			"count": count,
			"font_size_em": font_size_em(properties),
			"bold": effective_bold,
			"samples": class_samples[class_name],
		}
		candidates.append(candidate)
	candidates.sort(key=lambda item: str(item["class"]))
	candidates.sort(key=lambda item: float(item["font_size_em"]), reverse=True)
	status = "REVIEW" if heading_count == 0 and candidates else "PASS"
	report: dict[str, object] = {
		"input": str(epub_path),
		"status": status,
		"title": metadata_value(opf_root, "title"),
		"creator": metadata_value(opf_root, "creator"),
		"date": metadata_value(opf_root, "date"),
		"spine_document_count": len(spine_paths),
		"measured_document_count": len(measured_paths),
		"native_heading_count": heading_count,
		"navigation_entry_count": toc_entries,
		"body_start": body_start,
		"prominent_paragraph_classes": candidates,
	}
	return report


#============================================
def resolve_body_start(spine_paths: list[str], requested: str | None) -> str:
	"""Resolve a body-start path or unique basename against the spine."""
	if requested is None:
		raise ValueError(
			"heading repair needs an EPUB bodymatter landmark or --body-start"
		)
	clean_requested = urllib.parse.unquote(requested.split("#", 1)[0])
	matches = [
		path for path in spine_paths
		if path == clean_requested or pathlib.PurePosixPath(path).name == clean_requested
	]
	if len(matches) != 1:
		raise ValueError(f"body start must match exactly one spine document: {requested}")
	return matches[0]


#============================================
def strip_leading_marker(element: lxml.etree._Element) -> bool:
	"""Remove a visual list marker from the first text slot in one promoted heading."""
	if element.text:
		replaced = LEADING_MARKER_PATTERN.sub(r"\1", element.text, count=1)
		if replaced != element.text:
			element.text = replaced
			return True
	for child in element:
		if strip_leading_marker(child):
			return True
		if child.tail:
			replaced = LEADING_MARKER_PATTERN.sub(r"\1", child.tail, count=1)
			if replaced != child.tail:
				child.tail = replaced
				return True
	return False


#============================================
def promote_paragraph(element: lxml.etree._Element, level: int) -> None:
	"""Convert one paragraph element to a semantic XHTML heading."""
	strip_leading_marker(element)
	element.tag = f"{namespace_name(element.tag)}h{level}"


#============================================
def parse_level_rules(values: list[str], label: str) -> dict[str, int]:
	"""Parse repeated NAME=LEVEL CLI rules and reject ambiguous entries."""
	rules: dict[str, int] = {}
	for value in values:
		if "=" not in value:
			raise ValueError(f"{label} rule must use NAME=LEVEL: {value}")
		name, level_text = value.rsplit("=", 1)
		name = " ".join(name.split())
		if not name or not level_text.isdigit():
			raise ValueError(f"{label} rule must use NAME=LEVEL: {value}")
		level = int(level_text)
		if not 1 <= level <= 6:
			raise ValueError(f"{label} heading level must be 1-6: {value}")
		if name in rules and rules[name] != level:
			raise ValueError(f"conflicting {label} rule: {name}")
		rules[name] = level
	return rules


#============================================
def repair_entries(
		entries: dict[str, bytes], spine_paths: list[str], body_start: str,
		class_rules: dict[str, int], text_rules: dict[str, int],
		) -> dict[str, object]:
	"""Promote evidence-selected body paragraphs and return an audit record."""
	start_index = spine_paths.index(body_start)
	class_counts: collections.Counter[str] = collections.Counter()
	text_counts: collections.Counter[str] = collections.Counter()
	modified_paths: list[str] = []
	promotion_count = 0
	for path in spine_paths[start_index:]:
		root = parse_xml(entries, path)
		modified = False
		for element in root.iter():
			if local_name(element.tag) != "p":
				continue
			classes = element.attrib.get("class", "").split()
			matched_classes = [name for name in classes if name in class_rules]
			levels = {class_rules[name] for name in matched_classes}
			if len(levels) > 1:
				raise ValueError(f"conflicting class levels on paragraph in {path}")
			text = normalized_text(element)
			if levels:
				level = levels.pop()
				for class_name in matched_classes:
					class_counts[class_name] += 1
			elif text in text_rules:
				level = text_rules[text]
				text_counts[text] += 1
			else:
				continue
			promote_paragraph(element, level)
			promotion_count += 1
			modified = True
		if modified:
			entries[path] = lxml.etree.tostring(
				root, encoding="utf-8", xml_declaration=True,
			)
			modified_paths.append(path)
	unused_classes = sorted(set(class_rules) - set(class_counts))
	unused_text = sorted(set(text_rules) - set(text_counts))
	if unused_classes or unused_text:
		raise ValueError(
			f"heading rules matched nothing: classes={unused_classes}, text={unused_text}"
		)
	repair: dict[str, object] = {
		"body_start": body_start,
		"modified_documents": modified_paths,
		"class_promotions": dict(sorted(class_counts.items())),
		"text_promotions": dict(sorted(text_counts.items())),
		"promotion_count": promotion_count,
	}
	return repair


#============================================
def repair_epub(
		input_path: pathlib.Path, output_path: pathlib.Path,
		class_rules: dict[str, int], text_rules: dict[str, int],
		body_start: str | None = None,
		) -> dict[str, object]:
	"""Write a separate EPUB whose selected body paragraphs are semantic headings."""
	if input_path.resolve() == output_path.resolve():
		raise ValueError("input and output EPUB paths must differ")
	if output_path.exists():
		raise FileExistsError(f"output EPUB already exists: {output_path}")
	if not class_rules and not text_rules:
		raise ValueError("heading repair needs at least one class or text rule")
	infos, entries, comment = load_epub(input_path)
	opf_path, _opf_root, manifest, spine_paths = manifest_and_spine(entries)
	navigation_path = nav_path(opf_path, manifest)
	_toc_entries, landmark_body_start = navigation_facts(entries, navigation_path)
	requested_body_start = body_start if body_start is not None else landmark_body_start
	resolved_body_start = resolve_body_start(spine_paths, requested_body_start)
	repair = repair_entries(
		entries, spine_paths, resolved_body_start, class_rules, text_rules,
	)
	output_path.parent.mkdir(parents=True, exist_ok=True)
	with zipfile.ZipFile(output_path, "x") as archive:
		archive.comment = comment
		for info in infos:
			archive.writestr(info, entries[info.filename])
	repair["input"] = str(input_path)
	repair["output"] = str(output_path)
	return repair


#============================================
def print_report(report: dict[str, object]) -> None:
	"""Print a compact structure report and bounded class samples."""
	print(f"EPUB structure: {report['status']}")
	print(f"Title: {report['title']}")
	print(f"Spine documents: {report['spine_document_count']}")
	print(f"Measured body documents: {report['measured_document_count']}")
	print(f"Native headings: {report['native_heading_count']}")
	print(f"Navigation entries: {report['navigation_entry_count']}")
	print(f"Body start: {report['body_start'] or 'not declared'}")
	candidates = list(report["prominent_paragraph_classes"])
	print(f"Prominent paragraph classes: {len(candidates)}")
	for candidate in candidates:
		samples = list(candidate["samples"])
		preview = samples[0] if samples else ""
		print(
			f"- {candidate['class']}: count={candidate['count']}, "
			f"size={candidate['font_size_em']}em, bold={candidate['bold']}; {preview}"
		)


#============================================
def parse_args() -> argparse.Namespace:
	"""Parse one EPUB, optional repair rules, and report paths."""
	parser = argparse.ArgumentParser(
		description="Measure EPUB headings and promote selected styled body paragraphs",
	)
	parser.add_argument("input", help="Source EPUB to inspect")
	parser.add_argument("-o", "--output", dest="output_file", help="Separate repaired EPUB")
	parser.add_argument(
		"-c", "--heading-class", dest="heading_classes", action="append", default=[],
		help="Promote one body paragraph class with CLASS=LEVEL",
	)
	parser.add_argument(
		"-t", "--heading-text", dest="heading_texts", action="append", default=[],
		help="Promote exact body paragraph text with TEXT=LEVEL",
	)
	parser.add_argument(
		"-b", "--body-start", dest="body_start",
		help="Spine path or basename when the EPUB has no bodymatter landmark",
	)
	parser.add_argument("-j", "--json-report", dest="json_report", help="Write an ASCII JSON report")
	args = parser.parse_args()
	return args


#============================================
def main() -> None:
	"""Measure one EPUB and optionally write a source-preserving semantic candidate."""
	args = parse_args()
	input_path = pathlib.Path(args.input)
	report = inspect_epub(input_path)
	print_report(report)
	class_rules = parse_level_rules(args.heading_classes, "class")
	text_rules = parse_level_rules(args.heading_texts, "text")
	if args.output_file:
		repair = repair_epub(
			input_path, pathlib.Path(args.output_file), class_rules, text_rules,
			body_start=args.body_start,
		)
		report["repair"] = repair
		print(f"Headings promoted: {repair['promotion_count']}")
		print(f"Repaired EPUB: {repair['output']}")
	elif class_rules or text_rules:
		raise ValueError("heading rules require --output")
	if args.json_report:
		json_path = pathlib.Path(args.json_report)
		json_text = json.dumps(report, indent=2, ensure_ascii=True) + "\n"
		json_path.write_text(json_text, encoding="ascii")
		print(f"JSON report: {json_path}")


#============================================
if __name__ == "__main__":
	main()
