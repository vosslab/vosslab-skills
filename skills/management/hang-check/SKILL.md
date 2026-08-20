---
name: hang-check
description: "Watch running background agents for evidence of a genuine stall without killing healthy work. Use for hang checks, stuck or silent subagents, stalled agents, watchdog monitoring, or periodic status detection."
---

# Hang check

## Purpose

A dispatched subagent can hang: it stops making progress but never returns.
This skill installs a recurring check that catches a real hang while leaving
a slow-but-working agent alone. Judge on evidence, not the clock: elapsed
time alone is never proof of a hang, because a long compile, model load, or
remote wait looks identical to a stuck agent if you only watch the timer.

## When to use

- One or more background subagents are running and may run long.
- The user asks for a watchdog, hang check, or "tell me if an agent gets
  stuck."

Skip it when no background subagents are active, when driving a single
foreground task turn by turn, or when the user wants live per-event log
streaming (use the `Monitor` tool for that).

## Timer

Use `CronCreate` for the recurring check and `CronDelete` to remove it.

- Arm exactly one recurring job when the first watched subagent starts. One
  watchdog covers all active agents; do not arm a second.
- Every 10-15 minutes fits most work; shorten only if agents finish fast.
- The job prompt re-enters this skill: "Run hang-check: review each active
  subagent's status, recent output, and file activity; investigate any
  agent that looks stuck; remove the timer if no subagents remain active."
- Record the returned job ID for cleanup.
- `CronCreate` jobs auto-expire after 7 days; tell the user if the watched
  work could run longer.

## Evidence and decision

Each check, read up to three signals per active agent:

| Signal | How to read it |
| --- | --- |
| Agent status | `TaskList` / agent status: running, completed, or errored |
| Recent output | Latest lines (`TaskOutput` or output file) -- is it advancing? |
| File activity | New or changed files / mtimes in the work area, when relevant |

File activity is evidence only when the agent is expected to touch files. An
agent that is researching, reading, or waiting on a remote call may make no
file changes while healthy; do not treat missing file changes as a hang.

Advancing on any relevant signal means healthy: leave it alone. Quiet on
every relevant signal for an unusually long stretch relative to the task's
pace means suspect a hang: investigate, do not stop it yet. "Unusually long"
is relative to the task, not a fixed number.

## Investigate before stopping

Before touching a suspected-hung agent:

- Read its most recent output in full. A stack trace, a prompt waiting on
  input, or a "downloading..." line changes the diagnosis.
- Check whether it is legitimately blocked on a long operation.
- Check file mtimes when files are expected: a file touched seconds ago
  means work is happening even if stdout is quiet.

Only after the evidence confirms a genuine hang, `TaskStop` the agent. Do
not automatically re-dispatch it: decide whether to resume, replace, or
cancel the work. Re-dispatch is wrong when the task is obsolete, already
done by another agent, unsafe to repeat, or depends on non-idempotent
actions. Report what the evidence showed, not just the action taken.

## Cleanup

After each check, if no subagents remain active, remove the timer with
`CronDelete` using the recorded job ID and confirm with `CronList` so no
orphaned watchdog keeps firing. Re-arm only when new subagents are
dispatched.

## Workflow

1. Confirm one or more background subagents are active. If none, stop.
2. Arm one recurring `CronCreate` watchdog; record the job ID.
3. On each fire, read the relevant evidence signals for every active agent.
4. Leave advancing agents alone; flag agents quiet on every relevant signal.
5. Investigate each flagged agent before acting.
6. For a confirmed hang, `TaskStop`, then decide resume, replace, or cancel.
7. When no subagents remain active, `CronDelete` the timer; confirm with
   `CronList`.
