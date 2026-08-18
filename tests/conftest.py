# Standard Library
import sys
import pathlib

# local repo modules
import file_utils


# Pytest owns the repository import environment. Tests can import shared tools
# and book-conversion modules without depending on shell-specific PYTHONPATH.
REPO_ROOT = pathlib.Path(file_utils.get_repo_root())
TEST_IMPORT_PATHS = (
	REPO_ROOT,
	REPO_ROOT / "tools",
	REPO_ROOT / "skills" / "docs" / "book-to-markdown" / "scripts",
)
for import_path in reversed(TEST_IMPORT_PATHS):
	path_text = str(import_path)
	if path_text not in sys.path:
		sys.path.insert(0, path_text)


# Exclude both end-to-end tiers from pytest collection. tests/playwright/
# holds browser-driven tests (Playwright), and tests/e2e/ holds heavier
# shell/Python whole-system runners. Both run outside pytest -- see
# docs/PLAYWRIGHT_USAGE.md and docs/E2E_TESTS.md.
collect_ignore = ["e2e", "playwright"]

# REPO_HYGIENE_FILTERS is the repo-local hygiene-exclusion registry (Layer 2).
# file_utils.discover_files reads it from this conftest, which is the right
# home because propagation only merges the collect_ignore block above into this
# file; the rest of conftest survives and may differ per repo. Vendored files
# (file_utils.py and every tests/test_*.py) get overwritten by propagation,
# so they must hold no repo-specific data. Put repo-specific exclusions here.
#
# Shape and rules:
#   - It is a dict: key -> list of repo-relative POSIX glob patterns.
#   - Keys are "all" or a vendored test key. A test key is the test filename
#     stem with the leading "test_" removed (test_pyflakes_code_lint.py ->
#     "pyflakes_code_lint", test_ascii_compliance.py -> "ascii_compliance").
#   - Patterns match repo-relative POSIX paths via fnmatch.fnmatchcase
#     (case-sensitive). A match excludes the file from that test.
#   - "all" patterns apply to every test; a test-key list applies only when
#     that test_key is passed to discover_files.
#   - Recursive directory exclusions need an explicit /** because fnmatch's *
#     does not cross "/". Use "temp_scripts/**" to exclude a whole subtree.
#
# Example entries:
#   REPO_HYGIENE_FILTERS = {
#       "all": ["temp_scripts/**", "TEMPLATE.py"],
#       "ascii_compliance": ["human_readable-*.html"],
#       "pyflakes_code_lint": ["devel/scratch_*.py"],
#   }
REPO_HYGIENE_FILTERS = {
	# These skills use intentional Unicode typography and terminal-art source data.
	"ascii_compliance": ["skills/plan/ideonomy-*/**"],
	# Converted book corpus data, not authored source code.
	"source_file_line_limit": ["skills/**/references/local-only/**"],
}

# === OPTIONAL_HELPERS_MENU ===
# See meta/docs/PROPAGATION_RULES.md for the managed-block propagation contract.
# This block is an optional helpers menu appended once by propagation and
# never overwritten on subsequent propagation runs. Uncomment a recipe below
# to enable it for this repo. Every line here is a comment by default so an
# untouched consumer behaves exactly as it did before propagation added this
# block.
#
# Import paths are configured unconditionally at the top of this file, so they
# are no longer a per-test or shell-setup responsibility.
#
# --- Recipe 1: redirect matplotlib config dir to a per-repo tmp location ---
# Prevents matplotlib from writing to the home-directory config cache during
# tests, which can cause cross-repo pollution or permission errors in CI.
# Set MPLCONFIGDIR to a writable tmp path before matplotlib is imported.
# Note: PYTHONUNBUFFERED and PYTHONDONTWRITEBYTECODE are handled by
# source_me.sh and belong there, not here.
#
#	import os
#	import tempfile
#	os.environ.setdefault("MPLCONFIGDIR", tempfile.mkdtemp(prefix="mpl_"))
