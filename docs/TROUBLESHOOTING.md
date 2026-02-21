# Troubleshooting

## Skill file not found

- Confirm the path exists: `ls skills/<skill-name>/SKILL.md`.
- Check spelling and case of the skill name.

## Missing docs links

- Ensure `docs/` files referenced by `README.md` exist.
- Keep doc filenames in all caps (for example, `INSTALL.md`, `USAGE.md`).

## Outdated local copy

- Refresh your clone:

```bash
git pull --ff-only
```
