# Model and view guidance

Use this reference before building non-trivial tables, trees, sorting, filtering, or editable collections in PySide6.

## Primary sources

- Qt 6 Model/View Programming:
  [https://doc.qt.io/qt-6/model-view-programming.html](https://doc.qt.io/qt-6/model-view-programming.html)
- Qt for Python modules index:
  [https://doc.qt.io/qtforpython-6/api.html](https://doc.qt.io/qtforpython-6/api.html)
- Qt for Python examples:
  [https://doc.qt.io/qtforpython-6/examples/index.html](https://doc.qt.io/qtforpython-6/examples/index.html)

## Default decisions

- Prefer `QTableView` or `QTreeView` plus a model for real application data.
- Use `QTableWidget` only for small, simple, local tables where convenience matters more than flexibility.
- Use `QSortFilterProxyModel` for sorting and filtering instead of baking that logic into widgets.
- Use delegates when a column needs custom rendering or editing behavior.

## Practical rules

- Keep the data model authoritative; views should present and edit, not own business data.
- Preserve selection, scroll position, and sort intent when refreshing data unless refresh invalidates them.
- Separate display formatting from raw values so sorting and editing remain correct.
- For large datasets, avoid eager rebuilding of every row on each update.
- If the user requests inline editing, define commit, cancel, and validation behavior explicitly.

## Common traps

- Populating `QTableWidget` with business logic until it becomes impossible to maintain.
- Rebuilding an entire model for small updates when signals can update the affected indexes.
- Encoding sort behavior in rendered strings instead of underlying typed data.
- Hiding important actions in delegates without any keyboard-accessible alternative.
