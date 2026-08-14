# News template

This is a writing shape for `docs/NEWS.md`, not a file to copy verbatim.
`NEWS.md` is short, curated release highlights and announcements, not a full
changelog and not the full version log. Keep it terse: a few lines per release
that a user skimming announcements would care about. Write substantive content
or omit the subsection; never emit an empty heading.

## Shape

```
# News

## vYY.MM.PATCH - YYYY-MM-DD
### Highlights
### Upgrade notes
```

## Section guidance

- `# News`: one `#` title, sentence case, appears once at the top.
- `## vYY.MM.PATCH - YYYY-MM-DD`: one block per release, reverse-chronological
  (newest first). The heading shape must be exactly `## v<version> - YYYY-MM-DD`
  so it stays compatible with `devel/make_release.py`. Use the repo CalVer
  shape (`0Y.0M.PATCH`, for example `26.06.1`); see the versioning rules in
  `docs/REPO_STYLE.md`.
- `### Highlights`: the few most user-facing wins of the release, in plain
  language. Curated, not exhaustive: pick the headline items, leave the fuller
  list to `docs/RELEASE_HISTORY.md`. Prefer 2 to 5 short bullets.
- `### Upgrade notes`: short, action-oriented guidance only when a real upgrade
  step exists (a breaking change, a required config edit, a migration). Omit
  this subsection entirely when there is no upgrade action for the user.

## Rules

- ASCII only; escape any UTF-8 symbols (for example `&alpha;`).
- Sentence-case headings; ATX style with a space after the hashes.
- Omit any subsection that has no real content. Do not write a hollow doc.
- Use relative links for repo-local files; keep link text equal to the path.
- This file is shorter and more curated than `release_history_template.md`.
  NEWS carries headlines and upgrade actions; RELEASE_HISTORY carries the full
  fixes and compatibility detail. Keep the two outputs distinct so `NEWS.md`
  and `RELEASE_HISTORY.md` never read identically.
