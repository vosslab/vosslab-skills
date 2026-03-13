# Deployment and packaging

Use this reference when the task includes packaging, distribution, startup validation, or shipping a PySide6 desktop app.

## Primary sources

- Qt for Python deployment:
  [https://doc.qt.io/qtforpython-6/deployment/index.html](https://doc.qt.io/qtforpython-6/deployment/index.html)
- Qt for Python tools:
  [https://doc.qt.io/qtforpython-6/tools/index.html](https://doc.qt.io/qtforpython-6/tools/index.html)
- Qt for Python considerations:
  [https://doc.qt.io/qtforpython-6/considerations.html](https://doc.qt.io/qtforpython-6/considerations.html)

## Default decisions

- Treat deployment as part of the product, not an afterthought after UI coding.
- Validate startup on a clean machine or clean environment assumptions when possible.
- Keep asset, plugin, and platform dependencies explicit.

## Practical rules

- Verify the app can start without relying on an editor or development checkout layout.
- Check that icons, translations, plugins, and other bundled assets resolve correctly in packaged form.
- Confirm the app handles missing files, bad config, and first-run states gracefully.
- Record the packaging path and runtime assumptions clearly for future maintenance.

## Common traps

- Packaging a build that only works from the source tree.
- Missing Qt plugins or resources in the distributable.
- Assuming fonts, icons, or external tools exist on the target machine.
- Verifying only the happy path and not first-run or failure behavior.
