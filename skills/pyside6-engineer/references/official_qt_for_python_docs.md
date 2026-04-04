# Official Qt for Python docs

Use the official Qt for Python docs as the primary source for PySide6 APIs, tutorials, examples, and package tools.

## Core entry points

- Getting Started:
  [https://doc.qt.io/qtforpython-6/gettingstarted.html](https://doc.qt.io/qtforpython-6/gettingstarted.html)
  Use for installation, the Widgets-vs-Qt-Quick split, first-app structure, and high-level next steps.
- Modules API:
  [https://doc.qt.io/qtforpython-6/api.html](https://doc.qt.io/qtforpython-6/api.html)
  Use for the supported Qt module list and module index when you need the canonical API surface.
- Tutorials:
  [https://doc.qt.io/qtforpython-6/tutorials/index.html](https://doc.qt.io/qtforpython-6/tutorials/index.html)
  Use for guided walkthroughs, including Qt Widgets, Qt Widgets UI, Qt Quick, Qt Creator, and debugging flows.
- Examples:
  [https://doc.qt.io/qtforpython-6/examples/index.html](https://doc.qt.io/qtforpython-6/examples/index.html)
  Use for concrete patterns before inventing architecture from scratch; especially useful for layouts, dock widgets, model/view, drag-and-drop, and widget gallery references.
- Tools:
  [https://doc.qt.io/qtforpython-6/tools/index.html](https://doc.qt.io/qtforpython-6/tools/index.html)
  Use for package tool behavior and the correct wrappers to run.

## Tool guidance

- Use `pyside6-designer` when designing widget UIs visually and generating `.ui` files.
- Use `pyside6-uic` to generate Python from `.ui` files.
- Use `pyside6-rcc` for `.qrc` resource files.
- Use `pyside6-project` when the task benefits from a `.pyproject`-driven build flow for `.ui`, `.qrc`, or `.qmltype` assets.
- Use the `pyside6-*` wrappers, not raw tool executables found inside `site-packages`, because the wrappers set up the environment correctly.

## Practical selection rules

- If the user asks for a classic desktop app, default to Qt Widgets unless there is evidence that Qt Quick is the better fit.
- If the user mentions `.ui` files, Qt Designer, or Qt Creator forms, prefer the official Designer and `pyside6-uic` workflow.
- If the user wants a pattern that sounds standard, check the official examples index before inventing a custom approach.
- If an API name or module placement is uncertain, verify it against the Modules API page before coding.
