# Signals and slots

Use this reference when designing event flow, decoupling widgets, or moving work off the UI thread.

## Primary sources

- Qt 6 Signals and Slots:
  [https://doc.qt.io/qt-6/signalsandslots.html](https://doc.qt.io/qt-6/signalsandslots.html)
- Qt for Python basic tutorial:
  [https://doc.qt.io/qtforpython-6/tutorials/basictutorial/signals_and_slots.html](https://doc.qt.io/qtforpython-6/tutorials/basictutorial/signals_and_slots.html)
- QThread:
  [https://doc.qt.io/qt-6/qthread.html](https://doc.qt.io/qt-6/qthread.html)

## Default decisions

- Emit semantic signals like `filters_changed`, `save_requested`, or `job_finished` instead of leaking widget details.
- Keep slots small and predictable.
- Prefer one-directional update flow where practical: user action, signal, state update, UI refresh.
- For background work, send results back to the UI with signals instead of mutating widgets from worker code.

## Practical rules

- Treat signals as interface contracts between components.
- Avoid webs of cross-connected widgets that all mutate each other.
- Name signals after domain events, not implementation details.
- Be explicit about what happens on start, progress, success, cancellation, and failure.
- Disconnect or scope connections carefully when widgets are short-lived or dynamically replaced.

## Common traps

- Long-running work inside a slot connected directly to a click.
- Emitting too many low-level signals instead of one meaningful event.
- Updating UI objects from worker threads.
- Using signals to hide state ownership instead of clarifying it.
