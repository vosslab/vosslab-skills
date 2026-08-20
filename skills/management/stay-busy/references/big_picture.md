# Big picture

Deep narrative for the `stay-busy` skill. SKILL.md carries the short framing
and the operational rules; this file carries the why, the lifecycle, the
worked example, the composition map, and the philosophy mapping.

## Origin story

The skill was created from one user request, paraphrased here as the seed
scenario:

> Now what should we do, that last job we asked the manager to do took 10
> minutes. Let's give them like a month's worth of testing, implementation
> to do that has exhaustive profiling. Perhaps generate cluttered scenes
> to see if things can be resolved. Stress test the layout manager. Also
> maybe push for NEW3? And then finally create a new report, long drawn
> out. Want to keep the manager busy. The manager sits idle so give them
> work to do. They spend 2 minutes making a plan and then sit idle for
> another 2 days. If we are not sure of the next step, we can give the
> manager multiple things to try and see which works best.

The project-specific phrases (cluttered scenes, layout manager, NEW3) are
artifacts of the originating session. The skill generalizes that situation
into a portable principle: **when stuck, find a solution.** When the
manager has no obvious next plan task, the answer is more dispatched work,
not idle. The rest of this document, and SKILL.md, stays language-neutral
so the same rules apply to any project.

## Why this skill exists

The dominant failure mode is unattended idle. The user closes the laptop,
leaves for the day, or queues an overnight session. The manager finishes
the obvious plan tasks in the first hour and stops. The user returns to a
chat log full of "I was about to do X but wanted to check first" rather
than finished artifacts.

The deferred-work-as-slack-fill thesis: every project has a backlog of
testing, exploration, and evidence-gathering that gets skipped under time
pressure. Exhaustive parameter sweeps. Stress galleries past nominal load.
Multi-methodology comparisons. Regression bisects against known
intermittent failures. Benchmark variance characterization. Read-only
audits of subsystems that were never reviewed. Long-form synthesis
reports. Next-version scoping.

None of that work is urgent. All of it is valuable. The manager has more
time than the project has obvious work, so the right move is to inflate
scope by roughly two orders of magnitude into the deferred-work backlog.
A 10-minute obvious task expands into a multi-day exploration suite.

## Lifecycle position

stay-busy fires inside the `delegate-manager-to-subagents` loop, at the
point where the manager would otherwise idle:

```
+--------------------+
|  approved plan     |
|  loaded            |
+---------+----------+
          |
          v
+--------------------+     +---------------------+
|  manager dispatches|<----+  ready tasks?       |
|  ready tasks       |     +---------------------+
+---------+----------+              ^
          |                         |
          v                         |
+--------------------+              |
|  reviews handoffs  |              |
|  read-only         |              |
+---------+----------+              |
          |                         |
          v                         |
+--------------------+              |
|  ready tasks       | yes -> dispatch next
|  remain?           |
+---------+----------+
          | no
          v
+--------------------+
|  finish-before-    | finish first, THEN expand
|  expanding check   |
+---------+----------+
          | clean
          v
+--------------------+
|  stay-busy fires   | <-- this skill
|  generates N       |
|  workstreams       |
+---------+----------+
          |
          v
+--------------------+
|  manager dispatches|---loop---^
|  the new           |
|  workstreams       |
+--------------------+
```

stay-busy never executes work itself. It is a workstream generator. The
manager remains the dispatcher.

## Worked overnight example

User closes the laptop at 11pm with the message: "going to bed, please
complete something." Manager has finished the day's planned tasks and is
at a "no obvious next plan task" point. stay-busy fires in away-mode.

Tier signal: plan had 6 tasks (medium), away-mode bumps to large (7-10).
Manager generates 8 workstreams, each with a status label and artifact
path requirement:

1. **Writeup** -- Synthesize the day's completed plan tasks into
   `output/report_session_<date>.md`: per-task summary, evidence
   inventory, residual risks.
2. **A/B/C comparison** -- Implement three candidate algorithms for
   `<subsystem>` as independent prototypes. Acceptance: same input set,
   same correctness bar. Comparison report at
   `output/proto_compare_<subsystem>.md`.
3. **Side-quest experiment** -- Prototype an alternative approach to
   `<problem>` in a single file under `experiments/`. Label `SIDE QUEST`
   in the TaskList. Output: prototype path + one-paragraph verdict.
4. **Audit** -- Read-only style and contract sweep over `src/<module>/`.
   Output: Markdown table of `path:line` rows at
   `output/audit_<module>.md`.
5. **Stress matrix** -- Run `<generator>` across 5 input sizes, record
   pass/fail and timing to `output/stress_<generator>.csv`.
6. **Output gallery** -- Capture `<renderer>` output across 4
   configurations using Playwright. Save to
   `tests/playwright/screenshots/gallery_<date>/`.
7. **Regression bisect** -- Bisect known intermittent failure in
   `<test>` between `<known-good ref>` and HEAD. Output: bisect log +
   first-bad commit.
8. **Benchmark variance** -- Time `<entry point>` over 20 runs on a
   representative input. Record best/median/worst to
   `output/bench_<entry>.json`.

Manager dispatches these in two batches per the parallelism limit. During
the night, workstream 2 (A/B/C comparison) surprises the manager:
algorithm B beats A on 4 of 5 metrics but loses badly on the 5th. The
manager does not message the user. Instead, the manager dispatches a
follow-up workstream:

9. **Variance follow-up** -- Re-run algorithm B vs A on metric 5 across
   10 seeds to determine whether the loss is signal or noise. Output:
   `output/proto_compare_<subsystem>_metric5_variance.json` plus an
   amended verdict in the comparison report.

Morning report: user wakes to 9 inspectable artifacts, one of which
contains a manager-authored "decided to investigate metric 5 variance
before recommending B because the 4-vs-1 split looked anomalous"
paragraph. Zero pending questions. Zero "I was about to do X but..."
prompts.

## What slack time is for

The four anchor activities the user named map onto the existing twelve
workstream types in
[workstream_templates.md](workstream_templates.md):

| Anchor activity (user phrasing) | Workstream types |
| --- | --- |
| Write up results | report; cleanup (changelog grooming) |
| A/B testing | alternative prototype; benchmark/profiling |
| Side-quest experiments | alternative prototype (labeled `SIDE QUEST`); failure investigation |
| Audit the codebase | audit; cleanup |
| (additional slack-time work) | stress and clutter; screenshot/evidence; regression/bisect; next-iteration push; test; implementation |

A few notes on why each anchor is slack-time work:

- **Writeups** get skipped because the project ships first, documents
  later. The away-mode shape is the long-form 25-100 page findings report
  (TypeScript: HTML rendered to PDF with embedded Playwright screenshots;
  Python: Markdown). See the report-workstream section of
  [workstream_templates.md](workstream_templates.md).
- **A/B testing** gets skipped because the team picks one approach and
  ships. The away-mode shape is A/B/C/D side-by-side with a comparative
  metrics table, run by independent subagents and synthesized by a final
  report subagent.
- **Side-quest experiments** get skipped because their value is uncertain.
  The away-mode shape is a single-file prototype with a written verdict.
  The `SIDE QUEST` annotation keeps the manager from confusing the work
  with production-bound output.
- **Audits** get skipped because no one wakes up wanting to read code.
  The away-mode shape is a read-only sweep of K subsystems with a
  Markdown table of findings. Audits never edit code; the report becomes
  input for a future implementation workstream.

## Two failure modes, rule-by-rule

Each SKILL.md rule prevents either passive waiting (PW) or reckless motion
(RM):

| Rule | Prevents |
| --- | --- |
| Big picture: "when stuck, find a solution" | PW |
| Big picture: "success = completed work, failure = pending questions" | PW |
| When to use: "stepping away from the keyboard" trigger | PW |
| Away mode: tier bump + expansive scope | PW |
| Away mode: "suppress confirmation-seeking" | PW |
| Manager decision authority: "react to findings without asking" | PW |
| Manager decision authority: "do more testing is the default" | PW |
| Default-to-safe-work: "do not stand by" | PW |
| Default-to-safe-work: "do not detour into unrelated housekeeping" | RM |
| Workstream scale: tier cap | RM |
| Finish before expanding | RM |
| Side quest discipline: random busywork forbidden | RM |
| Evidence artifact requirement | RM (catches fake progress) |
| Boundaries: ask-only list (architecture/contract/deletion) | RM |
| Boundaries: metric-gaming forbidden list | RM |
| What the skill must not do | RM |

PW count vs RM count is intentionally balanced. A skill that only
addressed PW would push the manager into reckless busywork. A skill that
only addressed RM would make the manager cautious to the point of idle.
The pair is the contract.

## Composition map

| Skill | Direction | Interface |
| --- | --- | --- |
| delegate-manager-to-subagents | host | stay-busy emits a TaskList of workstream-shaped tasks plus the standard output template; manager dispatches |
| parallel-plan | upstream | when a parallel-plan output exists, respect its workstream IDs, dependency graph, and max-parallel-doers count; do not invent conflicting workstreams |
| blueprint-plan-drafter | upstream | the plan file feeds the tier signal (plan length) and the finish-before-expanding check (unfinished plan tasks) |
| audit-code-reviewer | downstream | an audit workstream may delegate to this skill for a full multi-pass audit; for single-pass review the [workstreams/audit.md](workstreams/audit.md) template is enough |

## Mapping to core philosophies

`docs/REPO_STYLE.md` lists five core philosophies. stay-busy operationalizes
three of them directly:

- **Finish the obvious.** Named explicitly in SKILL.md's Core principle.
  The finish-before-expanding rule and the situation-to-action table both
  enforce this: take the next safe step rather than stopping at a task
  boundary.
- **Atomic task decomposition.** Each workstream is one atomic
  dispatchable unit with one owner, one outcome, and one verification
  step. The workstream templates in
  [workstream_templates.md](workstream_templates.md) enforce this shape.
- **Fix the design, not the symptom.** The metric-gaming forbidden list
  in [boundaries.md](boundaries.md) is the test-artifact expression of
  this philosophy: do not change the diagnostic so it passes, do not
  weaken tests, do not hide failures.

The other two philosophies live elsewhere:

- **Long-term over short-term** is honored by `blueprint-plan-drafter`
  (durable plans) and `delegate-manager-to-subagents` (no quick patches
  by the manager).
- **Fresh subagent per task** is honored by
  `delegate-manager-to-subagents` (one dispatch per atomic task), which
  stay-busy hands tasks to.

stay-busy is not the right home for those two; they are dispatched and
plan-creation rules, not anti-idle rules.
