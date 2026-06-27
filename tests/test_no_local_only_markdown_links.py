"""
No Markdown links into local-only directories in skill markdown files.

Rule: committed markdown in skills/ must not link to files inside a
`local-only/` directory. The `local-only/` books are intentionally gitignored;
a Markdown link implies a GitHub-browsable committed target, which is wrong.
Bare backtick paths are the intended format for referencing local-only files.

Good:
    Use `references/local-only/About_Face.txt` and grep for "posture".

Bad:
    [About Face](references/local-only/About_Face.txt)
    [id]: references/local-only/About_Face.txt

Pairs with `tests/test_skill_internal_links.py`, which skips gitignored link
targets. This test closes that gap by explicitly banning any Markdown link
whose URL contains a `local-only/` path segment, regardless of whether the
target file exists on disk.
"""

# Standard Library
import os
import re
import pathlib

# local repo modules
import file_utils

REPO_ROOT = file_utils.get_repo_root()
SKILLS_DIR = pathlib.Path(REPO_ROOT) / "skills"

# Inline markdown links: [text](url)
INLINE_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")

# Reference-style link definitions: [id]: url  (anchored at line start)
REF_LINK_RE = re.compile(r"^\s*\[[^\]]*\]:\s+(\S+)")

# Segment that marks a gitignored local-only directory
LOCAL_ONLY_SEGMENT = "local-only/"


#============================================
def url_is_local_only(url: str) -> bool:
	"""
	Return True if the url contains a local-only/ path segment.

	Strips an optional title suffix (separated by a space) and a fragment
	(after #) before checking, to match the same pre-processing done in
	test_skill_internal_links.py.

	Args:
		url: Raw URL string captured from a Markdown link match group.

	Returns:
		bool: True when the url path contains 'local-only/'.
	"""
	# Drop optional title after the url: [text](url "title")
	url_path = url.split(" ", 1)[0]
	# Drop fragment: [text](url#section)
	url_path = url_path.split("#", 1)[0]
	return LOCAL_ONLY_SEGMENT in url_path


#============================================
def scan_text_for_violations(text: str, label: str) -> list[str]:
	"""
	Scan markdown text for links into local-only/ directories.

	Checks each line for inline links ([text](url)) and reference-style
	link definitions ([id]: url). Returns one entry per violation in
	'label:line_no: ...' format so callers can name each violation clearly.

	Bare backtick mentions of local-only/ paths are not Markdown links and
	are not detected; only the two link syntaxes above are checked.

	Args:
		text: Markdown source text to scan.
		label: Prefix for violation messages (typically a relative file path).

	Returns:
		list[str]: Violation strings in 'label:line_no: description' format.
			Empty when no violations are found.
	"""
	violations = []
	for line_no, line in enumerate(text.splitlines(), start=1):
		# Check inline links: [text](url)
		for match in INLINE_LINK_RE.finditer(line):
			url = match.group(1)
			if url_is_local_only(url):
				violations.append(
					f"{label}:{line_no}: inline link into local-only/: {match.group(0)}"
				)
		# Check reference-style link definitions: [id]: url
		ref_match = REF_LINK_RE.match(line)
		if ref_match:
			url = ref_match.group(1)
			if url_is_local_only(url):
				violations.append(
					f"{label}:{line_no}: reference-style link into local-only/: {line.strip()}"
				)
	return violations


#============================================
def find_skill_markdown_files() -> list[pathlib.Path]:
	"""Return every .md file under skills/ as absolute Path objects."""
	matches = []
	for root, _, names in os.walk(SKILLS_DIR):
		for name in names:
			if name.endswith(".md"):
				matches.append(pathlib.Path(root) / name)
	return matches


#============================================
def test_live_skills_clean() -> None:
	"""
	Every markdown file under skills/ must have zero Markdown links into
	local-only/ directories.

	Reference local-only files by bare backtick path plus a grep term
	instead. This test scans both inline and reference-style link syntax
	across every skill .md file and names each violation as path:line.
	"""
	violations = []
	for skill_md in find_skill_markdown_files():
		# Skip dot-prefixed skill folders (config or scratch areas).
		skill_name = skill_md.parts[skill_md.parts.index("skills") + 1]
		if skill_name.startswith("."):
			continue
		text = skill_md.read_text(encoding="utf-8")
		label = str(skill_md.relative_to(REPO_ROOT))
		violations += scan_text_for_violations(text, label)
	assert not violations, (
		f"{len(violations)} local-only/ Markdown link(s) found in skills/:\n"
		+ "\n".join(violations[:50])
		+ (f"\n... and {len(violations) - 50} more" if len(violations) > 50 else "")
	)


#============================================
def test_inline_link_flagged() -> None:
	"""Inline link [text](references/local-only/x.txt) is detected as a violation."""
	text = (
		"# Test\n"
		"[About Face](references/local-only/About_Face.txt)\n"
	)
	violations = scan_text_for_violations(text, "test.md")
	assert violations, "Inline local-only/ link must be detected as a violation"


#============================================
def test_reference_link_flagged() -> None:
	"""Reference-style definition [id]: references/local-only/x.txt is detected."""
	text = (
		"# Test\n"
		"[book]: references/local-only/About_Face.txt\n"
	)
	violations = scan_text_for_violations(text, "test.md")
	assert violations, "Reference-style local-only/ link definition must be detected"


#============================================
def test_bare_path_allowed() -> None:
	"""Bare backtick path mention is not a Markdown link and must not be flagged."""
	text = (
		"# Test\n"
		'Use `references/local-only/About_Face.txt` and grep for "posture".\n'
	)
	violations = scan_text_for_violations(text, "test.md")
	assert not violations, f"Bare backtick path must not be flagged, got: {violations}"
