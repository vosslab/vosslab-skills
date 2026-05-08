# Skill naming convention

This is the vosslab-wide convention for naming Agent Skills so skill folder
names stay distinct, predictable, and free of collisions with plugin skills
and Claude Code harness built-ins. Apply it to every skill under `skills/`
in this repo and any sibling vosslab repos that ship skills.

## Rules

1. **Front-load the distinguisher.** The first two hyphen-delimited tokens of a
   skill name carry its identity. Tokens 3+ are not a recall surface: users
   who type `/<name>` into the skill menu remember the first two tokens of
   the slash command, not the suffix.
2. **First-3-character prefix uniqueness.** No two active vosslab skills may
   share the same first three characters. This is a stricter form of rule 1
   that catches near-collisions like `web-` vs `webwork-`. Skills prefixed
   with `old-` are exempt (deprecation marker).
3. **Avoid plugin and harness leading tokens.** Do not use a leading token
   that overlaps with a currently-loaded plugin skill or a harness built-in
   (see the reserved list below). Use
   `tools/list_loaded_skills.py --check <candidate>` and
   `tools/list_loaded_skills.py --collisions` to verify.
4. **No redundant tokens** such as `-skill`, `-tool`, or `-helper`.
5. **Frontmatter `name:` must match the directory name** exactly.
6. **Verb-first for process skills, domain-noun-first for specialists.**
   - **Process / cross-cutting skills** (those whose leading token would be
     a generic process verb like `manager`, `review`, `audit`, `read`,
     `execute`, `plan`): use verb-first ordering. The leading verb is the
     user's recall anchor. Examples: `blueprint-plan-drafter`,
     `delegate-manager-to-subagents`, `audit-code-reviewer`.
   - **Domain-specialist skills** (those whose leading token is unique
     domain vocabulary like `bptools`, `webwork`, `typescript`, `pyside6`,
     `computer-vision`): use agent-form suffix (`-writer`, `-engineer`,
     `-expert`, `-builder`). The domain token at position 1 already carries
     identity; the suffix names what the skill is. Examples:
     `bptools-writer`, `typescript-engineer`, `computer-vision-expert`.
   - Long names are fine when the extra tokens add searchable keywords
     (`delegate-manager-to-subagents`, `blueprint-plan-drafter`,
     `old-manager-review-existing-plan`). What matters is that the first
     two tokens carry identity; tokens 3+ are bonus keywords.
7. **`old-` prefix marks deprecated skills.** Use `old-<original-name>` for
   skills retained for occasional reference but no longer recommended for
   daily use. Old-skills are exempt from rules 2 and 3.
8. **Skill markdown files must not use `..` paths to leave the skill
   folder.** `..` references that exit the skill (e.g.
   `[name](../other-skill/SKILL.md)` or `[docs/X.md](../../docs/X.md)`)
   break when the skill is loaded outside this repo (personal overlay,
   marketplace plugin cache). Use plain backticked names instead
   (`` `audit-code-reviewer` ``, `` `docs/PYTHON_STYLE.md` ``). Internal
   `..` references that stay within the skill folder (e.g. `../SKILL.md`
   from a `references/` subdirectory) are fine because the skill's own
   layout travels with it. See `tests/test_relative_paths.py`.

## Suffix families

| Suffix | Role | Example skills |
| --- | --- | --- |
| `-builder` | Builds or assembles a deliverable end to end | `html-game-parallel-builder` |
| `-docs` | Creates or refreshes documentation artifacts | `arch-docs`, `install-usage-docs`, `readme-docs` |
| `-drafter` | Authors a first-pass artifact (plan, spec, blueprint) | `blueprint-plan-drafter` |
| `-engineer` | Implements or refactors code in a domain | `typescript-engineer`, `pyside6-engineer`, `ui-ux-engineer` |
| `-expert` | Designs and reviews work in a specialized field | `computer-vision-expert` |
| `-fixer` | Trims and standardizes a single named artifact in place | `agents-md-fixer` |
| `-guide` | Reads or explains rules and reference material | `skill-writing-guide`, `pdf-guide` |
| `-manager-to-X` / `-manager` | Coordinates plans, milestones, or delegated execution. Verb-first variants encode WHAT the manager does (`delegate-`, `draft-`, `review-`); only one skill may lead with a bare `manager-` token. | `delegate-manager-to-subagents` |
| `-reader` | Reads or summarizes content | `repo-rules-reader` |
| `-reviewer` | Reviews code or output for quality | `audit-code-reviewer` |
| `-starter` | Generates first-pass scaffolding | `unit-test-starter` |
| `-writer` | Authors content in a specific format | `bptools-writer`, `webwork-writer` |

Singleton suffix families are acceptable when the skill's role is clearly
distinct (e.g. `-builder`, `-fixer`, `-starter`). What matters is that the
first two tokens identify the skill, not that the suffix has multiple members.

## Reserved leading tokens (harness built-ins)

The tokens `init`, `review`, `simplify`, `loop`, `schedule`, `update-config`,
`keybindings-help`, `fewer-permission-prompts`, `claude-api`, and
`security-review` are reserved by the Claude Code harness. Do not use them
as the leading token of a vosslab skill. This list is advisory and should
be re-audited whenever the harness updates its built-in skill set.

## Plugin tokens to avoid

Loaded `superpowers:*` plugin skills (and similar marketplace plugins) carry
their own leading tokens. As of 2026-05-08 the loaded set includes:
`brainstorming`, `dispatching-parallel-agents`, `executing-plans`,
`finishing-a-development-branch`, `receiving-code-review`,
`requesting-code-review`, `subagent-driven-development`,
`systematic-debugging`, `test-driven-development`, `using-git-worktrees`,
`using-superpowers`, `verification-before-completion`, `writing-plans`,
`writing-skills`. Avoid leading tokens that share 3+ characters with any of
these (e.g. `execute-`, `executing-`, `subagent-`, `dispatching-`,
`writing-`).

## Enumerating loaded skills

Use `tools/list_loaded_skills.py` to inspect which skills are currently
visible and to check a candidate name for collisions.

```bash
source source_me.sh && python3 tools/list_loaded_skills.py
source source_me.sh && python3 tools/list_loaded_skills.py --collisions
source source_me.sh && python3 tools/list_loaded_skills.py --names-only
source source_me.sh && python3 tools/list_loaded_skills.py --check my-new-skill
```

The default output tabulates every loaded skill with a `Prefix collisions`
column listing other skills sharing 3+ leading characters. The `--collisions`
flag filters that output to only the colliding rows. The `--check` flag
exits non-zero when the supplied candidate name shares a leading
hyphen-token (5+ chars) with another skill or has a content collision.

## Audit table (post-2026-05-08 reset)

| Skill | Status | Previous name | Rationale |
| --- | --- | --- | --- |
| `agents-md-fixer` | compliant | (new) | `-fixer` suffix family for in-place trim/standardize of a named artifact (`AGENTS.md`). |
| `arch-docs` | compliant | (unchanged) | Clean `-docs` suffix, unique leading token. |
| `audit-code-reviewer` | compliant | review-code-changes | First-2 "audit code" reads as the activity; user-confirmed acceptable. |
| `blueprint-plan-drafter` | accepted-rename | planning-manager / manager-make-new-plan | Verb-first; first-2 "blueprint plan" carries the artifact + domain; `manager-` lead retired. |
| `bptools-writer` | compliant | (unchanged) | Domain-specific leading token, `-writer` suffix. |
| `computer-vision-expert` | compliant | (unchanged) | Distinct domain token, `-expert` suffix. |
| `delegate-manager-to-subagents` | accepted-rename | execution-manager / manager-driven-execution | Verb-first; first-2 "delegate manager"; "subagents" keyword in token 4 for searchability. |
| `docset-updater` | compliant | docset-refresh | Agent-form suffix matches update-if-drifted behavior. |
| `gas-town-workflow` | borderline-no-change | (unchanged) | Repo-specific brand name; leading token unique. |
| `html-game-parallel-builder` | accepted-rename | web-game-parallel-builder | Drops `web-` collision with `webwork-`; `html` is short, evergreen. |
| `install-usage-docs` | compliant | (unchanged) | Clean `-docs` suffix, unique compound leading token. |
| `old-manager-review-existing-plan` | deprecated | plan-review-manager / manager-review-existing-plan | `old-` prefix marks for occasional use; original verb-first form preserved. |
| `old-orchestrate-next-milestone` | deprecated | milestone-manager / orchestrate-next-milestone | `old-` prefix marks for occasional use. |
| `old-python-code-review` | deprecated | python-reviewer / python-code-review | `old-` prefix marks for occasional use. |
| `parallel-plan` | borderline-no-change | (unchanged) | Leading token distinct; in-flight nudge skill. |
| `pdf-guide` | compliant | pdf-skill | Drops redundant `-skill` token. |
| `pyside6-engineer` | compliant | (unchanged) | Framework token plus `-engineer` suffix. |
| `readme-docs` | compliant | readme-fix | Joins `-docs` family. |
| `repo-rules-reader` | compliant | read-repo-rules | `-reader` suffix; user-confirmed acceptable. |
| `skill-writing-guide` | compliant | (unchanged) | Clear `-guide` suffix, unique leading token. |
| `typescript-engineer` | compliant | (unchanged) | Language token plus `-engineer` suffix. |
| `ui-ux-engineer` | compliant | (unchanged) | Domain token plus `-engineer` suffix. |
| `unit-test-starter` | compliant | (unchanged) | Unique leading token, `-starter` suffix. |
| `webwork-writer` | compliant | (unchanged) | Domain token plus `-writer` suffix. |

Counts (24 active skills): 14 compliant or borderline-no-change, 7
accepted-rename, 3 deprecated (`old-` prefix). The post-rename canonical
record matches the output of
`tools/list_loaded_skills.py --names-only` on the repo.
