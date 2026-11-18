# This file is vendored. Local changes can and will be overwritten by propagation.

"""Offline package.json convention checks for TypeScript projects."""

import importlib.util
import pathlib

import file_utils


REPO_ROOT = pathlib.Path(file_utils.get_repo_root())
CHECKER_PATH = REPO_ROOT / "devel" / "check_typescript_package_policy.py"

SPEC = importlib.util.spec_from_file_location("package_policy", CHECKER_PATH)
PACKAGE_POLICY = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(PACKAGE_POLICY)


#============================================
def test_every_eligible_tracked_manifest_obeys_policy() -> None:
	"""The consumer's root or nested TypeScript manifest obeys the stable policy."""
	paths = PACKAGE_POLICY.updater.iter_package_jsons(str(REPO_ROOT))
	assert paths
	violations = []
	for path in paths:
		violations.extend(PACKAGE_POLICY.check_manifest(path))
	assert violations == []
