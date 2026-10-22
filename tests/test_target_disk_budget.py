# This file is vendored. Local changes can and will be overwritten by propagation.

"""Keep the mandatory Rust target disk budget in pytest's base lane.

Run this guard with ``source source_me.sh && python3 -m pytest tests/``.
Cached Rust builds can grow until they fill the developer volume, so every Rust
repository receives this check. Continuous development must use that volume
responsibly, so this is not an optional or E2E-only check. If it fails, clean
stale ``target/`` artifacts before continuing development.
"""

# Standard Library
import os
import subprocess

# Local
import file_utils


MAX_TARGET_SIZE_KIB = 10 * 1024 * 1024


#============================================
def directory_size_kib(directory: str) -> int:
	"""Return physical directory usage in KiB, matching ``du -sh`` scope."""
	result = subprocess.run(
		["du", "-sk", directory],
		check=True,
		capture_output=True,
		text=True,
	)
	return int(result.stdout.split(maxsplit=1)[0])


#============================================
def test_target_disk_usage_stays_under_10_gib() -> None:
	"""Keep Rust build artifacts within the target directory budget."""
	repo_root = file_utils.get_repo_root()
	target_directory = os.path.join(repo_root, "target")
	if not os.path.isdir(target_directory):
		return
	actual_kib = directory_size_kib(target_directory)
	assert actual_kib <= MAX_TARGET_SIZE_KIB, (
		"target/ disk usage is "
		f"{actual_kib / (1024 * 1024):.1f} GiB; the budget is 10.0 GiB. "
		"Run `cargo clean` or remove stale target/ build artifacts before continuing."
	)
