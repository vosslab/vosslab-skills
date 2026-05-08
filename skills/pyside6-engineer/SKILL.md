---
name: pyside6-engineer
description: Design, implement, refactor, and review PySide6 desktop applications with strong widget architecture, signal-slot design, and state flow. Use when building or fixing Qt for Python windows, dialogs, forms, navigation shells, model-view tables, theming, or validation in Python GUI code.
mode: doer
execution: delegated
---

# PySide6 Engineer

## Overview

Use this skill to build desktop interfaces that are technically sound with PySide6.
Focus on widget architecture, signal-slot design, state management, and Qt best practices.
Use the official Qt for Python docs as the primary source for APIs, examples, and tool behavior.
For UI/UX review and design polish, use the `ui-ux-engineer` skill.

## Workflow

1. Classify the surface before coding.
- Decide whether the work belongs in Qt Widgets or Qt Quick first, then decide whether it should use a `QMainWindow`, `QWidget`, `QDialog`, wizard, dock layout, or model/view surface.
- Identify the primary user goal, the main workflow path, and the states that must be handled: loading, empty, valid, invalid, busy, success, and failure.
- Read [`references/official_qt_for_python_docs.md`](references/official_qt_for_python_docs.md) when you need the official entry points for installation, module lookup, tutorials, examples, or package tools.

2. Choose a structure that keeps state understandable.
- Prefer a small composition tree of widgets over a giant window class.
- Keep business logic separate from widget layout logic.
- Use signals, slots, and small controller-style helpers to avoid tightly coupling every widget to every other widget.
- Read [`references/pyside6_patterns.md`](references/pyside6_patterns.md) when choosing between common widget, dialog, navigation, threading, and model/view patterns.
- Read [`references/signals_slots.md`](references/signals_slots.md) when designing event flow, widget coordination, worker updates, or signal boundaries.

3. Build the UI from layout and hierarchy first.
- Prefer layouts over absolute positioning.
- Keep forms short, labels explicit, and primary actions visually dominant.
- Design for resizing from the start; do not assume one fixed window size.
- Read [`references/model_view.md`](references/model_view.md) before building non-trivial tables, trees, filtering, sorting, or custom cell rendering.

## Implementation defaults

- Prefer Qt Widgets for classic desktop productivity tools, forms, settings, inspectors, admin panels, and other dense business UIs.
- Use Qt Quick only when the product genuinely needs a more fluid, animated, or QML-centric surface and the request clearly points there.
- Prefer `QMainWindow` for multi-region applications with menus, toolbars, docks, or status bars.
- Prefer `QDialog` for short focused tasks that need confirmation or cancellation.
- Prefer `QStackedWidget` or a router/controller pattern for multi-step flows when tabs would expose too much complexity.
- Prefer Qt's model/view classes for tables, trees, and large changing datasets.
- Keep long-running work off the UI thread; use worker objects plus `QThread` or other Qt-safe async patterns.
- Treat stylesheets as a finishing layer, not a substitute for good widget choice and layout structure.
- Prefer official Qt tools when the task involves `.ui`, `.qrc`, or project-generation workflows instead of reinventing those steps by hand.
- Read [`references/designer_ui_workflow.md`](references/designer_ui_workflow.md) when `.ui` files, Qt Designer, or `pyside6-uic` are involved.
- Read [`references/deployment_and_packaging.md`](references/deployment_and_packaging.md) when the task includes packaging, shipping, or validating a distributable PySide6 app.

## Quality bar

- Favor stable patterns over clever widget tricks.
- Favor predictable state transitions over hidden side effects.
- Do not block the event loop with expensive work, sleeps, or synchronous network/file operations in click handlers.

## Output expectations

When using this skill, aim to produce:
- PySide6 code that is organized by responsibility and easy to extend.
- Explicit handling for validation, error messaging, empty states, and loading states.
- References to the relevant official Qt for Python docs when using unfamiliar APIs or package tools.

## Delegated execution

Under `manager-driven-execution`, this skill is assigned to a fresh subagent
with one bounded task, the relevant repo rules, and one verification step.
Do not continue the same subagent across unrelated follow-up work; dispatch a
new subagent for each atomic task. See
[docs/REPO_STYLE.md](../../docs/REPO_STYLE.md#core-philosophies).
