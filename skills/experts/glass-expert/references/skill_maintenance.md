# Skill maintenance

Use this guide when asked to refresh, update, or audit glass-expert itself.
Liquid Glass is a moving target: Apple retunes the material and its chrome
every OS release (announced at WWDC each June), and authoritative
documentation trails the announcements by weeks to months. Every factual
claim in this skill carries an implicit as-of date.

## Volatility map

What goes stale, and where it lives:

| Content | Guide | Staleness driver |
| --- | --- | --- |
| API names, availability, opt-out keys | [api_quick_reference.md](api_quick_reference.md) | New SDK each WWDC; core glass surface stable since WWDC25 |
| Chrome behavior (toolbar, sidebars, corners) | [design_placement.md](design_placement.md), [toolbar_best_practices.md](toolbar_best_practices.md) | Retuned every OS release; HIG updates land late |
| Expected appearance per backdrop | [testing_and_oracles.md](testing_and_oracles.md) matrix | Material retuning (diffusion, edge treatment, self-opacity) |
| Capture mechanics and permissions | [capture_paths.md](capture_paths.md) | `screencapture` and Screen Recording permission changes |
| Seed views | `assets/GlassSurface.swift`, `assets/GlassEvidenceView.swift` | Must compile against each new SDK; availability annotations |
| Contrast rules and accessibility flags | [color_and_contrast.md](color_and_contrast.md) | Slowest-moving; WCAG thresholds stable |

## Annual refresh procedure

Run after each WWDC (June) and again when the OS ships (fall):

1. Search the web for "what's new in SwiftUI WWDC <year>" and the new OS
   name plus "Liquid Glass changes"; the skill author's training data always
   trails the current cycle, so verify by search and fetch, never from
   memory.
2. Diff the API table in [api_quick_reference.md](api_quick_reference.md)
   against Apple's current SwiftUI documentation; every row must still
   resolve to a live API.
3. Fetch the HIG Toolbars and Materials pages once Apple updates them for
   the new OS; fold changes into
   [toolbar_best_practices.md](toolbar_best_practices.md) and
   [design_placement.md](design_placement.md).
4. Rebuild the seed views against the new SDK; run the evidence protocol
   with `GlassEvidenceView` on the new OS and check each row of the
   expected-appearance matrix still describes what a correct capture shows.
5. Update version-specific statements (the "26 and 27" comparisons) so the
   newest release is named and the oldest supported one still holds.
6. Refresh the pending watchlist below: close finished items, date new ones.

## Pending watchlist

Dated items known to be unresolved when last touched; close or refresh each
on the next maintenance pass.

- [ ] Golden Gate HIG update (noted 2026-07): the human interface guidelines
  had not yet been republished for macOS 27. When they land, fetch the
  Toolbars and Materials pages and reconcile
  [toolbar_best_practices.md](toolbar_best_practices.md) against them.
- [ ] macOS 27 final release notes (noted 2026-07, beta 3 current): re-verify
  the uniform-toolbar auto-adoption claim and any scroll edge effect
  additions against the shipped SDK in the fall.

## Source ranking

Verify claims top-down; a lower source never overrides a higher one:

1. Apple developer documentation (developer.apple.com/documentation) and SDK
   headers -- the only acceptable source for API claims.
2. WWDC session videos and Apple sample code (the Landmarks toolbar sample).
3. Apple HIG -- best-practices authority once updated for the release.
4. Established community writeups (Swift with Majid, Create with Swift,
   Hacking with Swift) -- fast and usually right; verify API names against
   source 1 before recording them.
5. News coverage (MacRumors, 9to5Mac) -- behavior and announcement facts
   only, never API claims.

## Editing rules

- Keep one concern per guide; an update lands in the guide that owns the
  topic, and cross-guide duplication is a bug.
- Body-only edits to `SKILL.md` need no manifest regeneration; a frontmatter
  change (name, description) requires regenerating via the repo's manifest
  tools.
- Run the repo test gate (`pytest tests/`) after any edit; new files must be
  git-staged for the link checker to see them.
- Record the update in the repo's `docs/CHANGELOG.md`.
- The sibling doc `templates/swift/docs/LIQUID_GLASS.md` in the
  starter-repo-template repo covers the same domain for propagated repos;
  when a fact changes here, check whether that doc needs the same fix.
