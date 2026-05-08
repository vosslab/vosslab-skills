# Skill naming convention

This is the vosslab-wide convention for naming Agent Skills so skill folder
names stay distinct, predictable, and free of collisions with plugin skills
and Claude Code harness built-ins. Apply it to every skill under `skills/`
in this repo and any sibling vosslab repos that ship skills.

## Rules

1. Front-load the distinguisher. The leading hyphen-delimited token must be
   unique across vosslab skills when it is 5 or more characters.
2. Use a shared suffix family from the table below so the role of each skill
   is obvious at a glance.
3. Avoid leading tokens that match any currently loaded plugin skill or
   Claude Code harness built-in.
4. No redundant tokens such as `-skill`, `-tool`, or `-helper`.
5. The frontmatter `name:` must match the directory name exactly. See
   [skills/skill-writing-guide/SKILL.md](../skills/skill-writing-guide/SKILL.md).
6. Prefer agent-form suffixes that name what the skill *is* (typically ending in `-er`/`-or`/`-ist`), not what it *does*.
   Verb-form suffixes (`-fix`, `-refresh`) are discouraged. The `-docs` artifact-form suffix is a documented exception for skills whose entire purpose is producing one or two documentation artifacts.

## Suffix families

| Suffix | Role | Example skills |
| --- | --- | --- |
| `-builder` | Builds or assembles a deliverable end to end | web-game-parallel-builder |
| `-updater` | Updates an existing artifact set when drift detected | docset-updater |
| `-docs` | Creates or refreshes documentation artifacts | arch-docs, install-usage-docs, readme-docs (artifact-form exception) |
| `-engineer` | Implements or refactors code in a domain | typescript-engineer, pyside6-engineer, ui-ux-engineer |
| `-expert` | Designs and reviews work in a specialized field | computer-vision-expert |
| `-fixer` | Trims and standardizes a single named artifact in place | agents-md-fixer |
| `-guide` | Reads or explains rules and reference material | skill-writing-guide, pdf-guide |
| `-manager` | Coordinates plans, milestones, or execution | execution-manager, planning-manager, plan-review-manager, milestone-manager |
| `-reader` | Reads or summarizes content | repo-rules-reader |
| `-reviewer` | Reviews code or output for quality | python-reviewer, audit-code-reviewer |
| `-starter` | Generates first-pass scaffolding | unit-test-starter |
| `-writer` | Authors content in a specific format | bptools-writer, webwork-writer |

## Reserved leading tokens (harness built-ins)

The tokens `init`, `review`, `simplify`, `loop`, `schedule`, `update-config`,
`keybindings-help`, `fewer-permission-prompts`, `claude-api`, and
`security-review` are reserved by the Claude Code harness. Do not use them
as the leading token of a vosslab skill. This list is advisory and should
be re-audited whenever the harness updates its built-in skill set.

## Enumerating loaded skills

Use [../tools/list_loaded_skills.py](../tools/list_loaded_skills.py) to
inspect which skills are currently visible and to check a candidate name
for collisions.

```bash
source source_me.sh && python3 tools/list_loaded_skills.py --names-only
source source_me.sh && python3 tools/list_loaded_skills.py --check my-new-skill
```

The tool collapses same-content duplicates (for example, when this repo is
also installed as a personal overlay) and flags genuine name collisions.

## Audit table

| Skill | Status | Previous name | Rationale |
| --- | --- | --- | --- |
| agents-md-fixer | compliant | (new) | New `-fixer` suffix family for in-place trim/standardize of a named artifact (`AGENTS.md`); sibling-in-spirit to `readme-docs`. |
| arch-docs | compliant | (unchanged) | Clean `-docs` suffix, unique leading token. |
| audit-code-reviewer | accepted-rename | review-code-changes | Resolves `re-` prefix collision; avoids harness `review` token; "audit" matches the skill's self-description. |
| bptools-writer | compliant | (unchanged) | Domain-specific leading token, `-writer` suffix. |
| computer-vision-expert | compliant | (unchanged) | Distinct domain token, `-expert` suffix. |
| docset-updater | accepted-rename | docset-refresh | Agent-form suffix `-updater` matches the skill's update-if-drifted behavior; verb-form `-refresh` deprecated per rule 6. |
| execution-manager | accepted-rename | manager-driven-execution | Resolves 3-way `manager-` collision; moves to `-manager` suffix family. |
| gas-town-workflow | borderline-no-change | (unchanged) | Repo-specific brand name; `-workflow` is not a shared family but the leading token is unique. |
| install-usage-docs | compliant | (unchanged) | Clean `-docs` suffix, unique compound leading token. |
| milestone-manager | accepted-rename | orchestrate-next-milestone | Verb-first replaced by noun + `-manager` suffix. |
| parallel-plan | borderline-no-change | (unchanged) | `-plan` is not a shared family, but the leading token is distinct and the skill is an in-flight nudge, not a planner. |
| pdf-guide | accepted-rename | pdf-skill | Drops redundant `-skill` token; fits `-guide` family; resolves frontmatter mismatch. |
| plan-review-manager | accepted-rename | manager-review-existing-plan | Resolves `manager-` collision; suffix family preserved. |
| planning-manager | accepted-rename | manager-make-new-plan | Resolves `manager-` collision; verb-noun front-load is more scannable. |
| pyside6-engineer | compliant | (unchanged) | Framework token plus `-engineer` suffix. |
| python-reviewer | accepted-rename | python-code-review | Suffix `-review` was inconsistent; `-reviewer` matches family. |
| readme-docs | accepted-rename | readme-fix | Joins `-docs` family alongside `arch-docs` and `install-usage-docs`; verb-form `-fix` deprecated per rule 6. |
| repo-rules-reader | accepted-rename | read-repo-rules | Resolves `re-` collision with the original `review-code-changes`; `-reader` suffix matches the action and pairs with `-writer` family. |
| skill-writing-guide | compliant | (unchanged) | Clear `-guide` suffix, unique leading token. |
| typescript-engineer | compliant | (unchanged) | Language token plus `-engineer` suffix. |
| ui-ux-engineer | compliant | (unchanged) | Domain token plus `-engineer` suffix. |
| unit-test-starter | compliant | (unchanged) | Unique leading token, `-starter` suffix. |
| web-game-parallel-builder | accepted-rename | web-game-parallel-build | Keeps `parallel-` mid-token (defining trait); fits `-builder` suffix family. |
| webwork-writer | compliant | (unchanged) | Domain token plus `-writer` suffix. |

Counts (plan-scope, 23): 10 compliant, 2 borderline-no-change, 11 accepted-rename. `agents-md-fixer` (added in parallel work) is listed as a 24th row, compliant under rule 6.

Milestone M2 of plan tingly-foraging-mccarthy.md applied this rename map;
this table is the post-rename canonical record.
