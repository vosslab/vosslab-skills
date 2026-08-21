"""Plan and apply skill and agent installations from repository data."""

from __future__ import annotations

# Standard Library
import os
import pathlib
import shutil
from dataclasses import dataclass

# local repo modules
import install_lib.agent_catalog
import install_lib.install_target_data
import install_lib.skill_discovery


@dataclass(frozen=True)
class InstallItem:
	"""One skill or agent installed beneath a platform destination."""

	kind: str
	name: str
	source: pathlib.Path | None
	destination: pathlib.Path
	contents: bytes | None = None


#============================================
def _require_safe_path(
	home_root: pathlib.Path,
	path: pathlib.Path,
	*,
	allow_leaf_symlink: bool = False,
) -> None:
	"""Require path containment and reject symlinked ancestor directories."""
	# ASVS 5.3.2: validate user-selected filesystem paths before any write.
	home = home_root.resolve()
	try:
		relative = path.relative_to(home)
	except ValueError as error:
		raise ValueError(f"path escapes selected home root: {path}") from error
	current = home
	for index, component in enumerate(relative.parts):
		current = current / component
		if current.is_symlink():
			is_leaf = index == len(relative.parts) - 1
			if allow_leaf_symlink and is_leaf:
				continue
			raise ValueError(f"symlink destination is unsafe: {current}")


#============================================
def _safe_mkdir(home_root: pathlib.Path, path: pathlib.Path) -> None:
	"""Create a contained platform directory after validating its ancestors."""
	_require_safe_path(home_root, path)
	path.mkdir(parents=True, exist_ok=True)
	_require_safe_path(home_root, path)


#============================================
def _item_sources(
	repo_root: pathlib.Path,
	target: install_lib.install_target_data.InstallTarget,
) -> list[tuple[str, str, pathlib.Path | None, bytes | None]]:
	"""Return linked skills and authored or rendered platform agents."""
	discovery = install_lib.skill_discovery.collect_skill_files(repo_root, repo_root / "skills")
	if target.target_id == "codex":
		categories = sorted({path.parent.parent for path in discovery.skill_files})
		items = [("skills", path.name, path, None) for path in categories]
	else:
		items = [("skills", path.parent.name, path.parent, None) for path in discovery.skill_files]
	agent_sources = install_lib.agent_catalog.adapter_agent_sources(repo_root, target.adapter)
	for name, source, contents in agent_sources:
		items.append(("agents", name, source, contents))
	return items


#============================================
def selected_targets(
	repo_root: pathlib.Path,
	platforms: list[str],
) -> dict:
	"""Select explicitly requested installation platforms."""
	targets = install_lib.install_target_data.load_targets(repo_root / "install_targets")
	if not platforms:
		raise ValueError("select at least one installation platform")
	unknown = sorted(set(platforms) - set(targets))
	if unknown:
		raise ValueError(f"unknown platform selection: {', '.join(unknown)}")
	selected = {name: targets[name] for name in platforms}
	return selected


#============================================
def build_plan(
	repo_root: pathlib.Path,
	home_root: pathlib.Path,
	platforms: list[str],
) -> dict:
	"""Build a side-effect-free installation plan for selected platforms."""
	home = home_root.resolve()
	targets = selected_targets(repo_root, platforms)
	plans = []
	for target in targets.values():
		items = []
		for kind, name, source, contents in _item_sources(repo_root, target):
			destination_root = install_lib.install_target_data.resolve_target_destination(
				home, target, kind
			)
			destination = destination_root / name
			_require_safe_path(home, destination, allow_leaf_symlink=True)
			if source is None and contents is None:
				raise ValueError(f"missing generated agent content: {name}")
			items.append(InstallItem(kind, name, source, destination, contents))
		plans.append({"target": target, "items": items})
	return {
		"home_root": str(home),
		"plans": plans,
	}


#============================================
def _symlink_target(path: pathlib.Path) -> pathlib.Path:
	"""Return one symlink's normalized target without requiring it to exist."""
	target = pathlib.Path(os.readlink(path))
	if not target.is_absolute():
		target = path.parent / target
	return target.resolve(strict=False)


#============================================
def _link_matches(path: pathlib.Path, source: pathlib.Path) -> bool:
	"""Return whether path is a symlink to the expected repository source."""
	return path.is_symlink() and _symlink_target(path) == source.resolve()


#============================================
def _install_item_matches(item: InstallItem) -> bool:
	"""Return whether a destination already represents the requested item."""
	if item.source is not None:
		return _link_matches(item.destination, item.source)
	if item.destination.is_symlink() or not item.destination.is_file():
		return False
	return item.destination.read_bytes() == item.contents


#============================================
def _remove_destination(path: pathlib.Path) -> None:
	"""Remove one explicitly approved destination without following links."""
	if path.is_symlink() or path.is_file():
		path.unlink()
	elif path.is_dir():
		shutil.rmtree(path)


#============================================
def _install_item(home_root: pathlib.Path, item: InstallItem) -> None:
	"""Install one skill link, agent link, or generated native agent file."""
	_safe_mkdir(home_root, item.destination.parent)
	if item.source is not None:
		item.destination.symlink_to(
			item.source.resolve(),
			target_is_directory=item.source.is_dir(),
		)
	else:
		if item.contents is None:
			raise ValueError(f"missing generated agent content: {item.name}")
		item.destination.write_bytes(item.contents)


#============================================
def apply_plan(plan: dict) -> dict:
	"""Install repository skills and agents as the authoritative current source."""
	home = pathlib.Path(plan["home_root"])
	changes: list[dict] = []
	for target_plan in plan["plans"]:
		for item in target_plan["items"]:
			if _install_item_matches(item):
				continue
			if item.destination.exists() or item.destination.is_symlink():
				_remove_destination(item.destination)
			_install_item(home, item)
			action = "link" if item.source is not None else "generate"
			relative = item.destination.relative_to(home).as_posix()
			changes.append({"action": action, "path": relative})
	return {"changes": changes}
