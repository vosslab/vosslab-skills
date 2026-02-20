# Parallel Plan Templates

## Stream Brief Template

Use this when dispatching each stream.

```text
Stream Name:
Goal:
Scope Boundary:
Owned Files/Dirs:
Inputs Available Now:
Blocked By:
Expected Interfaces or Contracts Produced:
Must Not Touch:
Validation Commands:
Research Depth: normal|deep
Run ID: <orchestrator-run-id>
Temp Report Root: <orchestrator-chosen-root>
Temp Report Path: <orchestrator-chosen-root>/<run-id>/<stream-name>.<unique-suffix>.report.md
Handoff Size Budget: <=1 KB and 3-6 bullets
Delivery Contract:
- handoff status
- handoff report_path
- handoff summary (3-6 bullets)
- handoff validation status (pass|fail)
- full report written to Temp Report Path
```

## Stream Handoff Template

Use this exact compact message for the orchestrator handoff.

```text
Status: complete|blocked|failed
Report Path: <orchestrator-assigned-report-path>
Summary:
- ...
- ...
- ...
Validation Status: pass|fail
Blocking Issues:
- none|...
```

## Stream Report File Template

Write this shape to the report file path assigned by orchestrator.

```text
Assumptions:
- ...

Decisions:
- ...

Concrete Next Steps:
1. ...
2. ...

Changed Files:
- /abs/path/file_a
- /abs/path/file_b

Validation Performed:
- command: ...
  result: pass|fail
```

## Unified Plan Template

Use this after collecting all stream reports.

```text
Inputs:
- <orchestrator-assigned-report-path-a>
- <orchestrator-assigned-report-path-b>

Ordered Plan:
1. ...
2. ...

Checkpoints:
- CP1: entry criteria, completion criteria, verification command
- CP2: entry criteria, completion criteria, verification command

Integration Risks:
- risk: ...
  mitigation: ...
  fallback: ...
```

## Anti-Pattern Checks

Reject or rework plans that show any of these:
- Streams editing the same file without explicit serialization.
- Streams blocked on outputs from other streams but dispatched together.
- Sequential dispatch labeled as parallel.
- Missing validation commands per stream.
- Missing checkpoint pass/fail criteria in the unified plan.
- Introducing a task database without explicit persistence/query requirements.
- Full stream reports pasted inline to the orchestrator.
- Reusing fixed report paths across runs or across streams.
- Missing or unreadable report paths.
- Handoff summaries that exceed the budget.
- Deep research streams that return full findings inline instead of using report files.
