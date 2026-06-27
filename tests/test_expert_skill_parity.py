"""
Parity gate for the eight domain-expert skills.

Mechanically enforces the required-set parity standard: every expert skill ships
the same interface (a thin `SKILL.md`, an `agents/openai.yaml`, and the four
routing / workflow / testing guides), and the four book-backed skills
additionally ship the two committed corpus files. The gate catches future drift so "consistent"
stays true without a human re-reading every skill.

What is asserted per skill (problems are reported as `skill: missing <path>`
and similar, so a failure names the exact gap):

- Universal required files for all eight: `SKILL.md`, `agents/openai.yaml`, and
  `references/{task_selection,topic_index,project_workflow,testing_and_oracles}.md`.
- Book-backed extras for the four named (geometry, vision, pyside6, ui-ux): the
  two COMMITTED files `references/reference_survey.md` and
  `references/local_books.md`. The gitignored `references/local-only/` corpus is
  deliberately NOT asserted; it is absent on a clean clone.
- `agents/openai.yaml` parses as YAML and carries `interface.display_name`,
  `interface.short_description`, and `interface.default_prompt`.
- Each required guide passes a light content guard: non-trivial length, a
  top-level `# ` title, no placeholder tokens (TODO/TBD/FIXME/<placeholder>/
  lorem ipsum), and every intra-skill routing reference it cites resolves to a
  real file in that skill's `references/` (a `local-only/` book path is exempt
  because that corpus is gitignored). Each skill carries at least one routing
  reference somewhere in its required guides.
- `SKILL.md` references `project_workflow.md` (proxy for the project-shape step).

Routing-presence is enforced at skill granularity rather than per guide: the
gold-standard `geometry-expert` (the reference implementation, kept unchanged) carries no
file-path routing reference in its `task_selection.md`, `project_workflow.md`,
or `testing_and_oracles.md`, so a per-guide presence rule would fail the very
reference the gate must accept. The dangling-reference resolution check stays
per reference across every guide, which is where the real teeth are.

The guard intentionally never asserts specific headings or prose, so it stays
stable across content edits (see docs/PYTEST_STYLE.md "Brittle tests").
"""

# Standard Library
import re
import pathlib

# PIP3 modules
import yaml  # pyyaml
import pytest

# local repo modules
import file_utils

REPO_ROOT = pathlib.Path(file_utils.get_repo_root())
SKILLS_DIR = REPO_ROOT / "skills"

# Explicit roster: the eight expert skills and the four book-backed ones.
# Both are named allowlists, not inferred, so a missing gitignored local-only/
# corpus on a clean clone cannot flip a skill in or out of either set.
EXPERT_SKILLS = (
	"geometry-expert",
	"vision-expert",
	"pyside6-engineer",
	"ui-ux-engineer",
	"solid-js-expert",
	"typescript-engineer",
	"bptools-writer-expert",
	"webwork-writer-expert",
)
BOOK_BACKED_SKILLS = frozenset({
	"geometry-expert",
	"vision-expert",
	"pyside6-engineer",
	"ui-ux-engineer",
})

# Required guides every expert carries under references/.
REQUIRED_GUIDES = (
	"task_selection.md",
	"topic_index.md",
	"project_workflow.md",
	"testing_and_oracles.md",
)
# Committed corpus files the four book-backed skills add (NOT the local-only/ dir).
BOOK_BACKED_FILES = (
	"reference_survey.md",
	"local_books.md",
)
# The three interface keys the parity standard requires in agents/openai.yaml.
REQUIRED_INTERFACE_KEYS = (
	"display_name",
	"short_description",
	"default_prompt",
)

# Content-guard thresholds and patterns.
MIN_GUIDE_LINES = 6
PLACEHOLDER_TOKENS = ("todo", "tbd", "fixme", "<placeholder>", "lorem ipsum")
# Inline markdown link [text](url) and backtick `references/...` path.
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
BACKTICK_REF_RE = re.compile(r"`(references/[^`]+)`")


#============================================
def required_files(skill_name: str) -> list[str]:
	"""Return the references-relative required-file list for one skill."""
	files = ["SKILL.md", "agents/openai.yaml"]
	files += [f"references/{guide}" for guide in REQUIRED_GUIDES]
	if skill_name in BOOK_BACKED_SKILLS:
		files += [f"references/{name}" for name in BOOK_BACKED_FILES]
	return files


#============================================
def find_placeholder(text: str) -> str | None:
	"""Return the first placeholder token present in text, or None."""
	lowered = text.lower()
	for token in PLACEHOLDER_TOKENS:
		# Alphabetic tokens match on word boundaries so words like
		# "fixmestring" do not trip the guard; literal tokens match directly.
		if token.isalpha():
			if re.search(r"\b" + re.escape(token) + r"\b", lowered):
				return token
		elif token in lowered:
			return token
	return None


#============================================
def routing_references(text: str) -> list[str]:
	"""
	Return every intra-skill routing reference cited by a guide.

	Two citation shapes count, matching the repo's link conventions:
	- a backtick `references/<path>` path (resolved from the skill root), and
	- a Markdown link whose URL is a bare same-folder filename (no slash, not an
	  external scheme or pure anchor), resolved inside references/.

	Each item is returned as a references-relative POSIX path. A bare
	`references/` folder token, a `local-only/` book path, or an extension-less
	URL is dropped here; `local-only/` exemption is applied by the caller.
	"""
	found = []
	# Backtick references/<path> paths resolve from the skill root.
	for match in BACKTICK_REF_RE.finditer(text):
		rest = match.group(1)[len("references/"):]
		if not rest or rest.endswith("/"):
			continue
		# Only treat tokens with a filename extension as file references.
		if "." not in pathlib.PurePosixPath(rest).name:
			continue
		found.append(rest)
	# Same-folder Markdown links: bare filename, no directory separator.
	for match in MARKDOWN_LINK_RE.finditer(text):
		url = match.group(1).split()[0].split("#", 1)[0]
		if not url or "/" in url:
			continue
		if url.startswith(("http://", "https://", "mailto:")):
			continue
		if "." not in url:
			continue
		found.append(url)
	return found


#============================================
def is_exempt_reference(rel_ref: str) -> bool:
	"""Local-only book paths are gitignored, so a citation to one is exempt."""
	return rel_ref.startswith("local-only/")


#============================================
def check_openai_yaml(refs_root: pathlib.Path, skill_name: str) -> list[str]:
	"""Return interface-schema problems for a skill's agents/openai.yaml."""
	problems = []
	yaml_path = refs_root.parent / "agents" / "openai.yaml"
	# Presence is checked by check_required_files; only validate when readable.
	if not yaml_path.is_file():
		return problems
	parsed = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
	interface = parsed.get("interface") if isinstance(parsed, dict) else None
	if not isinstance(interface, dict):
		problems.append(f"{skill_name}: agents/openai.yaml missing interface block")
		return problems
	for key in REQUIRED_INTERFACE_KEYS:
		value = interface.get(key)
		if not (isinstance(value, str) and value.strip()):
			problems.append(f"{skill_name}: agents/openai.yaml missing interface.{key}")
	return problems


#============================================
def check_guide_content(refs_root: pathlib.Path, skill_name: str, guide: str) -> list[str]:
	"""
	Return content-guard problems for one required guide.

	Checks length, a top-level title, placeholder tokens, and that every routing
	reference the guide cites resolves to a real file in references/.
	"""
	problems = []
	guide_path = refs_root / guide
	if not guide_path.is_file():
		return problems  # presence reported separately
	text = guide_path.read_text(encoding="utf-8")
	if len(text.splitlines()) <= MIN_GUIDE_LINES:
		problems.append(f"{skill_name}: references/{guide} too short to be a real guide")
	first_line = next((line for line in text.splitlines() if line.strip()), "")
	if not first_line.startswith("# "):
		problems.append(f"{skill_name}: references/{guide} missing top-level '# ' title")
	token = find_placeholder(text)
	if token is not None:
		problems.append(f"{skill_name}: references/{guide} contains placeholder '{token}'")
	for rel_ref in routing_references(text):
		if is_exempt_reference(rel_ref):
			continue
		if not (refs_root / rel_ref).exists():
			problems.append(
				f"{skill_name}: references/{guide} cites missing references/{rel_ref}"
			)
	return problems


#============================================
def check_required_files(skill_dir: pathlib.Path, skill_name: str) -> list[str]:
	"""Return a `skill: missing <path>` problem for each absent required file."""
	problems = []
	for rel in required_files(skill_name):
		if not (skill_dir / rel).is_file():
			problems.append(f"{skill_name}: missing {rel}")
	return problems


#============================================
def check_skill(skill_dir: pathlib.Path, skill_name: str) -> list[str]:
	"""
	Run the full parity gate for one skill directory and return all problems.

	Pure function over a directory path so the synthetic fixtures below can
	exercise it against constructed skill trees, not just the live skills.
	"""
	problems = list(check_required_files(skill_dir, skill_name))
	refs_root = skill_dir / "references"
	problems += check_openai_yaml(refs_root, skill_name)
	# Every required guide gets the content guard.
	guides = list(REQUIRED_GUIDES)
	if skill_name in BOOK_BACKED_SKILLS:
		guides += list(BOOK_BACKED_FILES)
	for guide in guides:
		problems += check_guide_content(refs_root, skill_name, guide)
	# Skill-level routing presence: at least one required guide must route.
	has_routing = False
	for guide in guides:
		guide_path = refs_root / guide
		if guide_path.is_file() and routing_references(guide_path.read_text(encoding="utf-8")):
			has_routing = True
			break
	if not has_routing:
		problems.append(f"{skill_name}: no intra-skill routing reference in any required guide")
	# Light SKILL.md check: project-shape step cites project_workflow.md.
	skill_md = skill_dir / "SKILL.md"
	if skill_md.is_file() and "project_workflow.md" not in skill_md.read_text(encoding="utf-8"):
		problems.append(f"{skill_name}: SKILL.md does not reference project_workflow.md")
	return problems


#============================================
@pytest.mark.parametrize("skill_name", EXPERT_SKILLS)
def test_expert_skill_parity(skill_name: str) -> None:
	"""Every live expert skill satisfies the required-set parity standard."""
	skill_dir = SKILLS_DIR / skill_name
	problems = check_skill(skill_dir, skill_name)
	assert not problems, "parity gaps:\n" + "\n".join(problems)


# ---------------------------------------------------------------------------
# Synthetic fixtures: prove the gate FAILS on a missing file, a placeholder
# guide, and a dangling routing reference. These build a valid skill tree under
# tmp_path, then mutate one thing per case.
# ---------------------------------------------------------------------------

GOOD_GUIDE_BODY = (
	"\n\nFrame the request, then route through the topic index.\n\n"
	"## Section\n\n"
	"- one consideration\n- another consideration\n- a third consideration\n"
	"- a fourth consideration\n- a fifth consideration\n"
)


#============================================
def write_guide(refs_root: pathlib.Path, name: str, *, routing_to: str | None) -> None:
	"""Write a content-guard-passing guide, optionally citing a same-folder file."""
	body = f"# {name.replace('_', ' ').title()}{GOOD_GUIDE_BODY}"
	if routing_to is not None:
		body += f"\nSee [{routing_to}]({routing_to}) for the routing table.\n"
	(refs_root / name).write_text(body, encoding="utf-8")


#============================================
def build_valid_skill(skill_dir: pathlib.Path) -> None:
	"""Construct a non-book-backed skill tree that passes the parity gate."""
	refs_root = skill_dir / "references"
	(skill_dir / "agents").mkdir(parents=True)
	refs_root.mkdir(parents=True)
	skill_dir.joinpath("SKILL.md").write_text(
		"# Synthetic skill\n\nWorkflow: detect project shape via "
		"references/project_workflow.md before editing.\n",
		encoding="utf-8",
	)
	interface = {
		"interface": {
			"display_name": "Synthetic Expert",
			"short_description": "A constructed skill for the parity test",
			"default_prompt": "Use $synthetic to do the thing.",
		}
	}
	skill_dir.joinpath("agents", "openai.yaml").write_text(
		yaml.safe_dump(interface), encoding="utf-8"
	)
	# topic_index routes to task_selection; others carry their own real link.
	write_guide(refs_root, "task_selection.md", routing_to="topic_index.md")
	write_guide(refs_root, "topic_index.md", routing_to="task_selection.md")
	write_guide(refs_root, "project_workflow.md", routing_to="topic_index.md")
	write_guide(refs_root, "testing_and_oracles.md", routing_to="topic_index.md")


#============================================
def test_synthetic_valid_skill_passes(tmp_path: pathlib.Path) -> None:
	"""The constructed baseline skill reports no parity problems."""
	skill_dir = tmp_path / "synthetic-expert"
	build_valid_skill(skill_dir)
	assert check_skill(skill_dir, "synthetic-expert") == []


#============================================
def test_synthetic_missing_file_fails(tmp_path: pathlib.Path) -> None:
	"""Removing a required guide is reported as a missing-file problem."""
	skill_dir = tmp_path / "synthetic-expert"
	build_valid_skill(skill_dir)
	(skill_dir / "references" / "project_workflow.md").unlink()
	problems = check_skill(skill_dir, "synthetic-expert")
	assert any("missing references/project_workflow.md" in p for p in problems)


#============================================
def test_synthetic_placeholder_guide_fails(tmp_path: pathlib.Path) -> None:
	"""A placeholder-only guide trips the no-placeholder guard."""
	skill_dir = tmp_path / "synthetic-expert"
	build_valid_skill(skill_dir)
	(skill_dir / "references" / "task_selection.md").write_text(
		"# Task selection\n\nTODO: write this guide later.\n", encoding="utf-8"
	)
	problems = check_skill(skill_dir, "synthetic-expert")
	assert any("placeholder 'todo'" in p for p in problems)


#============================================
def test_synthetic_dangling_reference_fails(tmp_path: pathlib.Path) -> None:
	"""A guide citing a non-existent same-folder file is reported as dangling."""
	skill_dir = tmp_path / "synthetic-expert"
	build_valid_skill(skill_dir)
	write_guide(skill_dir / "references", "topic_index.md", routing_to="nonexistent.md")
	problems = check_skill(skill_dir, "synthetic-expert")
	assert any("cites missing references/nonexistent.md" in p for p in problems)
