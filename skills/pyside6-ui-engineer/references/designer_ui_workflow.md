# Designer and .ui workflow

Use this reference when the task mentions Qt Designer, `.ui` files, `pyside6-uic`, `QUiLoader`, or resource compilation.

## Primary sources

- Qt for Python tools:
  [https://doc.qt.io/qtforpython-6/tools/index.html](https://doc.qt.io/qtforpython-6/tools/index.html)
- Using `.ui` files with Qt for Python:
  [https://doc.qt.io/qtforpython-6/tutorials/basictutorial/uifiles.html](https://doc.qt.io/qtforpython-6/tutorials/basictutorial/uifiles.html)
- Getting started:
  [https://doc.qt.io/qtforpython-6/gettingstarted.html](https://doc.qt.io/qtforpython-6/gettingstarted.html)

## Default decisions

- Prefer Qt Designer plus `pyside6-uic` when the UI is form-heavy and benefits from visual iteration.
- Prefer handwritten widgets when the interface is highly dynamic, strongly code-driven, or easier to express directly in Python.
- Use the `pyside6-*` wrappers rather than internal package binaries.

## Practical rules

- Keep generated UI code separate from hand-written behavior code.
- Do not hand-edit generated files if regeneration is part of the workflow.
- If loading `.ui` files dynamically, define where runtime loading is preferable to code generation.
- Use `pyside6-rcc` for `.qrc` resource workflows when assets need Qt resource integration.
- If a project uses `pyside6-project`, follow that build flow instead of inventing a parallel one.

## Common traps

- Mixing generated code and business logic in the same file.
- Treating Designer output as the final architecture instead of a presentation layer.
- Forgetting to regenerate Python after `.ui` changes.
- Hard-coding resource paths that should live in Qt resources.
