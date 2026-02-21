#!/usr/bin/env python3
"""Build docs/SKILLS_INDEX.md from skills/**/SKILL.md files."""

from __future__ import annotations

import argparse
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_ROOT = REPO_ROOT / "skills"
OUTPUT_PATH = REPO_ROOT / "docs" / "SKILLS_INDEX.md"


def collect_skill_stats(skill_files: list[Path]) -> dict[str, int]:
    """Count repository and system skills for run summaries."""
    system_count = 0
    for skill_file in skill_files:
        if skill_file.relative_to(SKILLS_ROOT).parts[0] == ".system":
            system_count += 1
    total_count = len(skill_files)
    repo_count = total_count - system_count
    return {
        "skills_processed": total_count,
        "repository_skills": repo_count,
        "system_skills": system_count,
    }


def extract_description(text: str) -> str:
    """Extract short skill description from frontmatter or Description section."""
    if text.startswith("---\n"):
        lines = text.splitlines()
        for line in lines[1:]:
            if line.strip() == "---":
                break
            if not line.lower().startswith("description:"):
                continue
            value = line.split(":", 1)[1].strip()
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            if value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            if value:
                return normalize_space(value)

    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.strip().lower() == "## description":
            for candidate in lines[i + 1 :]:
                candidate = candidate.strip()
                if candidate:
                    return normalize_space(candidate)

    return "See skill file for details."


def first_sentence(text: str) -> str:
    """Return first sentence-like chunk for list readability."""
    normalized = normalize_space(text)
    if not normalized:
        return "See skill file for details."

    parts = normalized.split(". ", 1)
    sentence = parts[0].strip()
    if not sentence.endswith("."):
        sentence += "."
    return sentence


def normalize_space(text: str) -> str:
    return " ".join(text.strip().split())


def collect_skill_files() -> list[Path]:
    return sorted(
        SKILLS_ROOT.rglob("SKILL.md"),
        key=lambda p: p.relative_to(SKILLS_ROOT).as_posix().lower(),
    )


def render_index(skill_files: list[Path]) -> str:
    stats = collect_skill_stats(skill_files)
    lines = [
        "# Skills index",
        "",
        "Compact index of skills in this repository. Each item links to the skill definition and gives a short purpose summary.",
        "",
        f"Total skills: {stats['skills_processed']}",
        f"Repository skills: {stats['repository_skills']}",
        f"System skills: {stats['system_skills']}",
        "",
    ]

    for skill_file in skill_files:
        skill_name = skill_file.parent.relative_to(SKILLS_ROOT).as_posix()
        rel_link = "../" + skill_file.relative_to(REPO_ROOT).as_posix()
        description = first_sentence(extract_description(skill_file.read_text(encoding="utf-8")))
        lines.append(f"- [{skill_name}/SKILL.md]({rel_link}): {description}")

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Build docs/SKILLS_INDEX.md")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit nonzero if docs/SKILLS_INDEX.md is out of date.",
    )
    args = parser.parse_args()

    if not SKILLS_ROOT.is_dir():
        raise SystemExit(f"Missing skills directory: {SKILLS_ROOT}")

    skill_files = collect_skill_files()
    stats = collect_skill_stats(skill_files)
    rendered = render_index(skill_files)

    if args.check:
        current = OUTPUT_PATH.read_text(encoding="utf-8") if OUTPUT_PATH.exists() else ""
        if current != rendered:
            print(f"Out of date: {OUTPUT_PATH}")
            print(
                "Stats: "
                + f"skills_processed={stats['skills_processed']}, "
                + f"repository_skills={stats['repository_skills']}, "
                + f"system_skills={stats['system_skills']}"
            )
            return 1
        print(f"Up to date: {OUTPUT_PATH}")
        print(
            "Stats: "
            + f"skills_processed={stats['skills_processed']}, "
            + f"repository_skills={stats['repository_skills']}, "
            + f"system_skills={stats['system_skills']}"
        )
        return 0

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(rendered, encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH}")
    print(
        "Stats: "
        + f"skills_processed={stats['skills_processed']}, "
        + f"repository_skills={stats['repository_skills']}, "
        + f"system_skills={stats['system_skills']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
