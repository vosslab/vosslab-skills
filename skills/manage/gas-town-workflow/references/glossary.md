# Gas Town glossary

Gas Town terminology mapped to Claude Code task equivalents.

## Core principles

### MEOW (Molecular Expression of Work)

Breaking large goals into detailed instructions for agents. Supported by tasks, convoys, and templates. MEOW ensures work is decomposed into trackable, atomic units that agents can execute autonomously.

**Claude Code equivalent:** Use TaskCreate to break work into single-responsibility tasks with clear done-when criteria. Each task should be completable by one agent in one session.

### GUPP (Gas Town Universal Propulsion Principle)

"If there is work on your Hook, YOU MUST RUN IT." Agents autonomously proceed with available work without waiting for external input. GUPP is the heartbeat of autonomous operation.

**Claude Code equivalent:** When a task is assigned to you (owner set to your name), start it immediately. Do not wait for confirmation or additional instructions.

### NDI (Nondeterministic Idempotence)

The overarching goal ensuring useful outcomes through orchestration of potentially unreliable processes. Persistent tasks and oversight agents guarantee eventual workflow completion even when individual operations fail.

**Claude Code equivalent:** Tasks persist across agent sessions. Monitor and scheduler agents ensure stalled work is detected and retried. Design workflows to tolerate individual agent failures.

## Environments

### Town

The management headquarters. In Claude Code terms, this is the team coordination layer -- the team lead agent and its task list.

### Rig

A project-specific repository under management. In Claude Code terms, this is the working directory where agents operate.

## Roles

### Polecat

Worker agent with persistent identity but ephemeral sessions. Works in isolated git worktrees.

**Claude Code equivalent:** A coder or tester agent spawned for a specific task. The agent session is ephemeral but the task and its history persist.

### Crew

Long-lived, named agents for persistent collaboration. Maintain context across sessions.

**Claude Code equivalent:** The coder agent type. Writes production code based on approved plans.

### Refinery

Manages the merge queue for a rig. Merges changes from workers, handles conflicts.

**Claude Code equivalent:** The integrator agent. Responsible for merge, rebase, and conflict resolution.

### Witness

Patrol agent that oversees workers. Monitors progress, detects stuck agents, triggers recovery.

**Claude Code equivalent:** The monitor agent. Observes task progress, detects stalls, reports problems. Read-only on code.

### Deacon

Daemon beacon running continuous patrol cycles. Ensures worker activity, monitors system health.

**Claude Code equivalent:** The scheduler agent. Triggers recurring workflows and retries tasks flagged as blocked or stalled by the monitor. Does not diagnose problems -- that is the monitor's job.

### Dogs

The Deacon's crew of maintenance agents handling background tasks like cleanup and health checks.

**Claude Code equivalent:** The maintainer agent. Handles cleanup, lint maintenance, and index regeneration. No architectural decisions, no feature work.

### Mayor

Chief-of-staff agent responsible for initiating convoys, coordinating work distribution, and notifying users.

**Claude Code equivalent:** The orchestrator or parallelizer agent. Coordinates parallel task execution and manages team communication.

## Work units

### Bead

Git-backed atomic work unit. The fundamental unit of work tracking.

**Claude Code equivalent:** A Claude Task created with TaskCreate. Has a subject, description, status, owner, and dependency relationships.

### Hook

A special pinned bead for each agent. The agent's primary work queue.

**Claude Code equivalent:** The agent's role-filtered view of TaskList. An agent checks TaskList for unblocked tasks matching its role and claims the next one.

### Convoy

Primary work-order wrapping related beads. Groups related tasks together.

**Claude Code equivalent:** A set of related Claude Tasks with dependency relationships (addBlockedBy, addBlocks). Usually created together with subject-line role tags.

### Slinging

Assigning work to agents.

**Claude Code equivalent:** TaskCreate followed by TaskUpdate with `owner` set to the target agent's name. The agent sees the task on its next TaskList check.

### Nudging

Real-time messaging between agents.

**Claude Code equivalent:** SendMessage with type "message" to a specific teammate by name.

### Formula

TOML-based workflow source template. Defines reusable patterns for common operations.

**Claude Code equivalent:** Convoy templates in [convoy-templates.md](convoy-templates.md). Ready-made task sequences for common workflows.

### Molecule

Durable chained bead workflows. Multi-step processes where each step is tracked.

**Claude Code equivalent:** A convoy with sequential dependencies. Each task blocks the next, forming a chain.

### Wisp

Ephemeral bead destroyed after runs. Lightweight work items for transient operations.

**Claude Code equivalent:** A lightweight task used for scratch or transient coordination. In most Claude Code workflows, completed tasks persist rather than being deleted. Treat wisps as a conceptual category (short-lived, low-ceremony tasks) rather than a deletion mechanism.

### Patrol

Ephemeral loop maintaining system heartbeat. Patrol agents continuously cycle through health checks.

**Claude Code equivalent:** The monitor agent periodically checking TaskList and TaskGet to detect stalled or stuck tasks.

### Handoff

Agent session refresh. Transfers work state to a new session when context fills.

**Claude Code equivalent:** An agent completing its turn, going idle, and being resumed or replaced by the team lead when new work is ready.

---
