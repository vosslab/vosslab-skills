"""
Skill-internal markdown links must resolve to existing files.

Pairs with `tests/test_relative_paths.py` (which catches `..` paths that
exit the skill folder); this test catches the inverse failure mode where a
link points at a skill-internal subfolder but the target is missing.

Conservative scope to avoid false positives:

- Only checks links whose URL starts with a recognised skill-internal
  prefix (`references/`, `templates/`, `agents/`, `data/`, `examples/`)
  or is a same-skill `../SKILL.md` style reference. Bare `docs/X.md` and
  `agents/X.md` references are intentionally NOT checked because the
  vosslab convention treats them as repo-relative pointers (every repo
  ships those files; see `docs/SKILL_NAMING.md` rule 8 discussion).
- Skips external links (http://, https://, mailto:), absolute paths
  (/foo), anchor-only links (#section), and code/example URLs that don't
  end in a recognised file extension.
- Skips targets that are deliberately gitignored. Some skills reference
  large local files (book notes, datasets) that are intentionally not
  committed; the `.gitignore` is the source of truth for what's expected
  on disk vs. what users supply locally.
"""

import re
import os
import pathlib
import subprocess

import git_file_utils

REPO_ROOT = git_file_utils.get_repo_root()
SKILLS_DIR = pathlib.Path(REPO_ROOT) / "skills"

# Inline markdown links: [text](url)
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")

# Recognised skill-internal subfolder prefixes. Only links whose target path
# starts with one of these prefixes are checked for existence; anything else
# is assumed to be a repo-level reference, an external URL, or example
# content (e.g. SMILES strings) and skipped.
SKILL_INTERNAL_PREFIXES = (
	"references/",
	"templates/",
	"data/",
	"examples/",
	"agents/",  # only when relative to the skill folder
)

# File extensions we expect to find inside a skill. URLs without one of
# these extensions are skipped (covers placeholders like `URL`, chemistry
# strings like `C(=O)O`, and similar example content).
RECOGNISED_EXTENSIONS = (
	".md", ".py", ".sh", ".yaml", ".yml", ".json", ".html", ".js", ".ts",
	".tsx", ".css", ".txt", ".pg", ".pgml",
)


#============================================
def find_skill_markdown_files() -> list[pathlib.Path]:
	"""Return every `.md` file under skills/ as absolute Path objects."""
	matches = []
	for root, _, names in os.walk(SKILLS_DIR):
		for name in names:
			if name.endswith(".md"):
				matches.append(pathlib.Path(root) / name)
	return matches


#============================================
def skill_root_for(md_path: pathlib.Path) -> pathlib.Path:
	"""Return the skill folder skills/<name>/ that contains md_path."""
	current = md_path.parent
	while current.parent != SKILLS_DIR:
		current = current.parent
	return current


#============================================
def link_resolves_inside_skill(url: str, md_path: pathlib.Path) -> tuple[bool, pathlib.Path]:
	"""
	Resolve a markdown link relative to its containing file.

	Returns (resolves_inside, target_path). `resolves_inside` is True only
	when the resolved target sits inside the skill folder. External and
	absolute links return (False, _) since they aren't internal-link cases.
	"""
	url_path = url.split(" ", 1)[0]   # drop optional title
	url_path = url_path.split("#", 1)[0]  # drop fragment
	if not url_path:
		return False, md_path  # pure anchor; not an internal-file ref
	if url_path.startswith(("http://", "https://", "mailto:", "/")):
		return False, md_path
	target = pathlib.Path(os.path.normpath(md_path.parent / url_path))
	skill_root = skill_root_for(md_path)
	skill_root_sep = str(skill_root) + os.sep
	target_str = str(target)
	is_inside = target_str == str(skill_root) or target_str.startswith(skill_root_sep)
	return is_inside, target


#============================================
def is_gitignored(target: pathlib.Path) -> bool:
	"""
	Return True if the target path is matched by repo .gitignore rules.

	Skills can intentionally reference large local files (book notes,
	datasets) that are gitignored by pattern (e.g. `skills/*/references/*.txt`).
	Those missing-on-disk cases are not test failures.
	"""
	# git check-ignore exits 0 when the path matches an ignore rule, 1 when
	# it doesn't, and 128 on error. Use -q to suppress output.
	result = subprocess.run(
		["git", "check-ignore", "-q", str(target)],
		cwd=REPO_ROOT,
		capture_output=True,
	)
	return result.returncode == 0


#============================================
def is_skill_internal_target(url_path: str) -> bool:
	"""Return True if the URL path looks like a skill-internal reference."""
	if url_path.startswith(SKILL_INTERNAL_PREFIXES):
		return True
	# Same-skill upward reference: ../SKILL.md or ../references/X.md from a
	# subfolder. Crude check: starts with `../` and the rest still looks
	# skill-internal (recognised prefix or a bare `SKILL.md`).
	if url_path.startswith("../"):
		tail = url_path[3:]
		if tail == "SKILL.md" or tail.startswith(SKILL_INTERNAL_PREFIXES):
			return True
	return False


#============================================
def test_internal_links_resolve():
	"""
	For every markdown link inside a skill folder whose URL starts with a
	recognised skill-internal prefix and ends in a recognised file
	extension, the target file must exist.

	Repo-level references (bare `docs/X.md`, `agents/X.md`) are NOT
	checked here; the vosslab convention treats them as repo-relative
	pointers assumed to be present in any host repo.
	"""
	violations = []
	for skill_md in find_skill_markdown_files():
		# Skip dot-prefixed skills (config/scratch areas).
		if skill_md.parts[skill_md.parts.index("skills") + 1].startswith("."):
			continue
		text = skill_md.read_text(encoding="utf-8")
		for line_no, line in enumerate(text.splitlines(), start=1):
			for match in MARKDOWN_LINK_RE.finditer(line):
				url = match.group(1)
				url_path = url.split(" ", 1)[0].split("#", 1)[0]
				if not url_path:
					continue
				if not is_skill_internal_target(url_path):
					continue
				if not url_path.lower().endswith(RECOGNISED_EXTENSIONS):
					continue
				is_inside, target = link_resolves_inside_skill(url, skill_md)
				if not is_inside:
					continue
				if not target.exists():
					if is_gitignored(target):
						continue
					rel_md = skill_md.relative_to(REPO_ROOT)
					rel_target = target.relative_to(REPO_ROOT) if str(target).startswith(str(REPO_ROOT)) else target
					violations.append(f"{rel_md}:{line_no}: -> {rel_target} (not found)")
	assert not violations, (
		f"{len(violations)} broken skill-internal link(s):\n" +
		"\n".join(violations[:50]) +
		(f"\n... and {len(violations) - 50} more" if len(violations) > 50 else "")
	)
