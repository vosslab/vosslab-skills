"""
Skill leading tokens must not collide with harness or plugin reserved tokens.

Encodes rule 3 from `docs/SKILL_NAMING.md`. The reserved set ships with this
test (rather than being scraped from the live environment) so the gate
remains deterministic. Update this list when the harness or known plugins
change.
"""

import pathlib

import file_utils

REPO_ROOT = file_utils.get_repo_root()
SKILLS_DIR = pathlib.Path(REPO_ROOT) / "skills"

import install_lib.skill_discovery

# Harness built-in slash commands. Update when the harness changes.
HARNESS_RESERVED = {
	"init",
	"review",
	"simplify",
	"loop",
	"schedule",
	"update-config",
	"keybindings-help",
	"fewer-permission-prompts",
	"claude-api",
	"security-review",
}

# Leading tokens of currently-loaded plugin skills that the user has installed.
# These are the leading-token portions (before the first hyphen). Listed as a
# frozen reference set; update when plugin set changes.
PLUGIN_LEADING_TOKENS = {
	"brainstorming",
	"dispatching",
	"executing",
	"finishing",
	"frontend",  # frontend-design plugin
	"receiving",
	"requesting",
	"skill",  # skill-creator plugin
	"subagent",
	"systematic",
	"test",  # test-driven-development from superpowers
	"using",
	"verification",
	"writing",
}


#============================================
def leading_token(skill_name: str) -> str:
	"""Return the first hyphen-delimited token of a skill name."""
	if "-" in skill_name:
		return skill_name.split("-", 1)[0]
	return skill_name


#============================================
def active_skill_names() -> list[str]:
	"""Return names for every publishable skill across category folders."""
	discovery = install_lib.skill_discovery.collect_skill_files(pathlib.Path(REPO_ROOT), SKILLS_DIR)
	return sorted(skill_file.parent.name for skill_file in discovery.skill_files)


#============================================
def test_no_skill_uses_harness_reserved_leading_token() -> None:
	"""Active skill names must not lead with a harness-reserved token."""
	violations = []
	for name in active_skill_names():
		if leading_token(name) in HARNESS_RESERVED:
			violations.append(name)
	assert not violations, (
		f"{len(violations)} skill(s) lead with a harness-reserved token "
		f"(rename required): {', '.join(violations)}"
	)


#============================================
def test_no_skill_uses_plugin_reserved_leading_token() -> None:
	"""
	Active skill names must not lead with a token already used by a loaded
	plugin skill (per the frozen PLUGIN_LEADING_TOKENS list above).

	Each published skill must have a leading token distinct from this set.
	"""
	violations = []
	for name in active_skill_names():
		if leading_token(name) in PLUGIN_LEADING_TOKENS:
			violations.append(name)
	assert not violations, (
		f"{len(violations)} skill(s) lead with a token used by a loaded "
		f"plugin: {', '.join(violations)}"
	)
