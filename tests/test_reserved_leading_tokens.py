"""
Skill leading tokens must not collide with harness or plugin reserved tokens.

Encodes rule 3 from `docs/SKILL_NAMING.md`. The reserved set ships with this
test (rather than being scraped from the live environment) so the gate
remains deterministic. Update this list when the harness or known plugins
change.
"""

import pathlib

import git_file_utils

REPO_ROOT = git_file_utils.get_repo_root()
SKILLS_DIR = pathlib.Path(REPO_ROOT) / "skills"

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
	"skill",  # skill-creator plugin (also matches our skill-writing-guide)
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
	"""Return non-old-* skill directory names."""
	return sorted(
		d.name for d in SKILLS_DIR.iterdir()
		if d.is_dir() and not d.name.startswith("old-")
	)


#============================================
def test_no_skill_uses_harness_reserved_leading_token():
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
def test_no_skill_uses_plugin_reserved_leading_token():
	"""
	Active skill names must not lead with a token already used by a loaded
	plugin skill (per the frozen PLUGIN_LEADING_TOKENS list above).

	Note: `skill-writing-guide` legitimately leads with `skill` because the
	plugin `skill-creator` only collides on first 6 characters; this is
	tracked as accepted-known in `docs/SKILL_NAMING.md`. If you need
	another such allowance, add it to `KNOWN_ALLOWED` below with a reason.
	"""
	# Each entry is (skill_name, reason-for-allowance).
	known_allowed = {
		"skill-writing-guide": "User-confirmed acceptable; collides on 'skill' lead with plugin skill-creator",
	}
	violations = []
	for name in active_skill_names():
		if name in known_allowed:
			continue
		if leading_token(name) in PLUGIN_LEADING_TOKENS:
			violations.append(name)
	assert not violations, (
		f"{len(violations)} skill(s) lead with a token used by a loaded "
		f"plugin: {', '.join(violations)}"
	)
