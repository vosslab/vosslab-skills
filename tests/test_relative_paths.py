"""
Forbid `..` relative paths that exit a skill's own folder.

Skills get loaded from many places: the repo's own `skills/<name>/`, the user's
personal overlay at `~/.claude/skills/<name>/`, marketplace plugin caches at
`~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/skills/<name>/`, and
symlinked installs. A markdown link like `[audit-code-reviewer](../audit-code-reviewer/SKILL.md)`
or `[docs/PYTHON_STYLE.md](../../docs/PYTHON_STYLE.md)` only resolves when the
skill lives under this repo's tree; in every other install location the `..`
walks past the install boundary into something unrelated.

The rule: skill markdown files (`skills/**/*.md`) must not contain any
markdown link whose target resolves OUTSIDE the skill's own folder.
Internal `..` references that stay within the skill (e.g. `../SKILL.md`
from a `references/` subdirectory) are fine because the skill's own layout
travels with it.

Use plain backticked names (`` `audit-code-reviewer` ``) for cross-skill
references and remove links to repo-level docs/agents files.

This test scans every tracked `.md` under `skills/` and fails on any
`[text](url)` link whose resolved target sits above the containing skill's
root directory.
"""

import re
import os
import pathlib

import git_file_utils

REPO_ROOT = git_file_utils.get_repo_root()
SKILLS_DIR = pathlib.Path(REPO_ROOT) / "skills"

# Match standard markdown inline links: [text](url). The url is captured.
# Reference-style links ([text][label]) are not relative-path concerns and are
# not matched here.
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


#============================================
def find_skill_markdown_files() -> list[pathlib.Path]:
	"""
	Return every `.md` file under skills/ as absolute Path objects.
	"""
	matches = []
	for root, _, names in os.walk(SKILLS_DIR):
		for name in names:
			if name.endswith(".md"):
				matches.append(pathlib.Path(root) / name)
	return matches


#============================================
def skill_root_for(md_path: pathlib.Path) -> pathlib.Path:
	"""
	Return the skill folder that contains md_path: skills/<skill-name>/.
	"""
	# md_path is somewhere under SKILLS_DIR; walk up until the parent is SKILLS_DIR.
	current = md_path.parent
	while current.parent != SKILLS_DIR:
		current = current.parent
	return current


#============================================
def link_exits_skill(url: str, md_path: pathlib.Path) -> bool:
	"""
	Return True if a markdown link target resolves to a path outside the
	skill's own folder.

	External (http/https/mailto) and absolute-path links are considered
	non-relative and never flagged. Anchor-only links (#section) are also
	skipped.
	"""
	# Drop optional title: `(url "title")` -> `url`
	url_path = url.split(" ", 1)[0].strip()
	# Drop fragment: `path#anchor` -> `path`
	url_path = url_path.split("#", 1)[0]
	if not url_path:
		# Pure anchor link, ignore.
		return False
	# Skip absolute URLs and absolute filesystem paths.
	if url_path.startswith(("http://", "https://", "mailto:", "/")):
		return False
	# Resolve target relative to the file's directory; refuse to follow
	# symlinks (use os.path.normpath, not Path.resolve).
	target = (md_path.parent / url_path)
	target_normalized = pathlib.Path(os.path.normpath(target))
	skill_root = skill_root_for(md_path)
	# If target_normalized is not under skill_root, the link exits the skill.
	skill_root_str = str(skill_root) + os.sep
	target_str = str(target_normalized)
	if not (target_str == str(skill_root) or target_str.startswith(skill_root_str)):
		return True
	return False


#============================================
def find_external_dotdot_links(text: str, md_path: pathlib.Path) -> list[tuple[int, str]]:
	"""
	Return (line_number, url) for `[text](url)` links whose target exits the
	skill folder via `..`. Only flags links that actually contain `..`.
	"""
	violations = []
	for line_no, line in enumerate(text.splitlines(), start=1):
		for match in MARKDOWN_LINK_RE.finditer(line):
			url = match.group(1)
			url_path = url.split(" ", 1)[0].strip()
			if ".." not in url_path.split("/"):
				continue
			if link_exits_skill(url, md_path):
				violations.append((line_no, url_path))
	return violations


#============================================
def test_no_dotdot_paths_exiting_skill():
	"""
	Skill markdown files must not contain markdown links whose target
	resolves outside the skill's own folder.
	"""
	files = find_skill_markdown_files()
	all_violations: list[str] = []
	for skill_md in files:
		text = skill_md.read_text(encoding="utf-8")
		exits = find_external_dotdot_links(text, skill_md)
		for line_no, url in exits:
			rel = skill_md.relative_to(REPO_ROOT)
			all_violations.append(f"{rel}:{line_no}: {url}")
	if all_violations:
		header = (
			f"Found {len(all_violations)} markdown link(s) whose `..` paths "
			f"exit the skill folder. These break when the skill is loaded "
			f"outside this repo. Replace cross-skill links like "
			f"`[name](../name/SKILL.md)` with backticked names like `name`."
		)
		body = "\n".join(all_violations[:50])
		more = f"\n... and {len(all_violations) - 50} more" if len(all_violations) > 50 else ""
		assert False, f"{header}\n{body}{more}"
