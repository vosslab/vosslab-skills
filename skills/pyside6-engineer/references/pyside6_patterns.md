# PySide6 patterns

## Table of contents

- Window and container selection
- State and ownership
- Forms and dialogs
- Navigation patterns
- Model/view guidance
- Threading and responsiveness
- QGraphicsView scroll, zoom, and trackpad
- Styling and theming

## Window and container selection

- Use `QMainWindow` when the app needs menus, toolbars, docks, a central widget, or a status bar.
- Use a plain `QWidget` for focused embeddable panels or simple utility windows.
- Use `QDialog` for bounded tasks that should return accept/reject intent.
- Use `QWizard` only when the workflow is truly stepwise and each page reduces complexity.

## State and ownership

- Keep window classes responsible for composition and wiring, not deep business rules.
- Move durable state into a model or controller object when multiple widgets depend on it.
- Prefer explicit update methods such as `refresh_summary()` over ad hoc cross-widget mutation.
- Emit high-level signals like `project_selected` or `filters_changed` instead of passing widget references around.

## Forms and dialogs

- Group related fields under clear section labels.
- Keep labels close to controls and use sentence-style wording.
- Use placeholder text only as a hint, never as the sole label.
- Disable the primary action until the minimum valid state is reached when that improves clarity.
- Put validation messages near the field when possible and summarize cross-field errors near the main action.
- In dialogs, make the primary action label specific, such as `Save preset` instead of `OK`.

## Navigation patterns

- Use tabs for peer sections that users switch between frequently.
- Use side navigation for larger applications with distinct areas.
- Use stacked views for progressive workflows or modes where only one view should be active at a time.
- Keep the back path obvious when a view replaces another view.

## Model/view guidance

- Prefer `QTableView` plus a model for real datasets instead of populating `QTableWidget` with ad hoc logic.
- Use delegates when editing or rendering behavior differs by column.
- Keep sort/filter logic in proxy models when possible.
- Preserve selection and scroll position when refreshing data unless the refresh invalidates the view.

## Threading and responsiveness

- Never do expensive I/O or computation directly in the UI thread.
- Move work into a worker object and communicate results with signals.
- Show progress when the action takes long enough for the user to wonder whether the app stalled.
- Disable or debounce repeated triggers when duplicate actions would conflict.
- Always define what the UI should show while work is running, after success, and after failure.

## QGraphicsView scroll, zoom, and trackpad

- On macOS, trackpad two-finger swipe and mouse scroll wheel both emit `QWheelEvent`. Distinguish them using `event.phase()` and `event.hasPixelDelta()`:
  - Trackpad events carry scroll phases (`ScrollBegin`, `ScrollUpdate`, `ScrollEnd`, `ScrollMomentum`).
  - Mouse wheel clicks have `Qt.ScrollPhase.NoScrollPhase` and `hasPixelDelta()` returns `False`.
  - Do not rely on `pixelDelta().isNull()` alone. Qt reports null `pixelDelta` at `ScrollBegin` and `ScrollEnd` phases even for trackpad events, causing false negatives.
- For trackpad pan via scroll bars: when the scene fits inside the viewport (fit-to-view), the scroll bar range is zero and `setValue()` has no effect. Expand the scene rect with a tiny margin (e.g. 2% of image size) before panning so the scroll bars have nonzero range. Keep the margin minimal to prevent the user from scrolling content off screen.
- Reset the scene rect to image bounds before calling `fitInView()`, otherwise fit-to-view will fit to the expanded (margin-padded) rect.
- Use `setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)` so wheel zoom anchors around the cursor position.
- For zoom, prefer `self.scale(factor, factor)` for incremental adjustment or `self.setTransform(QTransform().scale(f, f))` for absolute zoom level.

## Styling and theming

- Start with spacing, alignment, typography scale, and widget choice before adding stylesheets.
- Keep color usage semantic: primary action, warning, error, success, informational accent.
- Keep contrast high enough for readability.
- Avoid dense borders and ornamental gradients unless the product already uses them consistently.
- Reuse a small set of spacing and size constants for visual rhythm.
