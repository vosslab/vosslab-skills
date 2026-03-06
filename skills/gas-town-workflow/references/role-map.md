# Role authority and escalation map

Role mapping between Gas Town theatrical names and Claude Code agent types, with authority boundaries and escalation targets.

## Role table

| Gas Town role | Agent | Authority boundary | Escalation target |
| --- | --- | --- | --- |
| Crew | coder | Production code, small doc updates | architect (design), planner (ambiguity) |
| Refinery | integrator | Merge, rebase, conflict resolution | human (failed merge after retry) |
| Witness | monitor | Observe, detect stalls, report | orchestrator, then human |
| Deacon | scheduler | Trigger workflows, retry, sync | (does not diagnose; monitor does that) |
| Dogs | maintainer | Cleanup, lint, index regen | (no arch decisions, no features) |
| -- | reviewer | Read-only code review, plan auditing | planner (plan drift) |
| -- | tester | Tests, coverage, validation | coder (production bug found) |
| -- | architect | Cross-cutting design approval | human (unresolvable design conflict) |
| -- | planner | Plans and docs only | architect (architecture decision needed) |
| -- | orchestrator | Parallel task coordination | human (systemic failure) |

## Authority boundaries

### coder (Crew)

- Writes production code and minimal doc updates.
- Prefers small diffs and frequent commits.
- Does not perform architectural redesign.
- Does not approve its own work; all changes go through reviewer.
- Tools: Bash, Glob, Grep, Read, Edit, Write, WebFetch, WebSearch, Skill, TaskCreate, TaskGet, TaskUpdate, TaskList

### integrator (Refinery)

- Merges completed work from branches.
- Resolves merge conflicts.
- Does not write new production code.
- Tools: Bash, Glob, Grep, Read, Edit, Write, TaskGet, TaskUpdate, TaskList, SendMessage

### monitor (Witness)

- Observes task progress and detects stalls.
- Reports problems to orchestrator or human.
- Does not modify code or implement fixes.
- Read-only access to code.
- Tools: Bash, Glob, Grep, Read, TaskGet, TaskUpdate, TaskList, SendMessage

### scheduler (Deacon)

- Triggers recurring workflows and retries failed tasks.
- Does not diagnose problems (monitor does that).
- Does not write code.
- Tools: Bash, Glob, Grep, Read, TaskCreate, TaskGet, TaskUpdate, TaskList, SendMessage

### maintainer (Dogs)

- Handles cleanup, lint maintenance, and index regeneration.
- No architectural decisions.
- No feature work.
- Tools: Bash, Glob, Grep, Read, Edit, Write, Skill, TaskGet, TaskUpdate, TaskList

### reviewer

- Read-only code review and plan auditing.
- Cannot modify production code.
- Verifies implementation matches approved plans.
- Tools: Bash, Glob, Grep, Read, WebFetch, WebSearch, Skill, TaskCreate, TaskGet, TaskUpdate, TaskList

### tester

- Generates tests, extends coverage, validates behavior.
- Only modifies files under `tests/`.
- Tools: Bash, Glob, Grep, Read, Edit, Write, TaskGet, TaskUpdate, TaskList, SendMessage

### architect

- Approves or rejects cross-cutting design changes.
- Technical authority for architectural decisions.
- Tools: Bash, Glob, Grep, Read, Edit, Write, WebFetch, WebSearch, Skill, TaskCreate, TaskGet, TaskUpdate, TaskList, SendMessage

### planner

- Creates plans and documentation.
- Never writes production code or tests.
- Proposes plans but defers architecture decisions to architect.
- Tools: Bash, Glob, Grep, Read, Edit, Write, WebFetch, WebSearch, Skill, TaskCreate, TaskGet, TaskUpdate, TaskList

### orchestrator

- Coordinates parallel tasks using task lists.
- Splits work into subagents and synthesizes results.
- Tools: Bash, Glob, Grep, Read, Edit, Write, WebFetch, WebSearch, Skill, TaskCreate, TaskGet, TaskUpdate, TaskList
