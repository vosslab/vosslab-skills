# Troubleshooting

## Skill file not found

- Confirm the path exists: `ls skills/<category>/<skill-name>/SKILL.md`.
- Check spelling and case of the skill name.

## Missing docs links

- Ensure `docs/` files referenced by `README.md` exist.
- Keep doc filenames in all caps (for example, `INSTALL.md`, `USAGE.md`).

## Outdated local copy

- Refresh your clone:

```bash
git pull --ff-only
```

## Existing destination replaced

The Git repository is authoritative. Final installation approval replaces a mismatched skill or
agent destination with the current repository source or generated native agent. Move unrelated
content outside the platform destination before running `python3 install_skills.py`.

## Stale installed entry

The installer keeps no hidden ownership state. It treats a symlink whose target resolves inside
this clone as its own and unlinks it when no current skill or agent claims it, so renamed or
removed skills disappear on the next run for the same platform. Generated agent files (Codex TOML,
Cursor and OpenCode Markdown) carry no ownership marker; remove an obsolete generated agent file
manually.

## Broken links after moving

Installed skills and authored Claude agents use absolute links to the repository clone. After
moving or renaming the clone, run `python3 install_skills.py` again from the new repository root to
refresh those links.
