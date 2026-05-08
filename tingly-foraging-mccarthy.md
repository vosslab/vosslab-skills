# Plan: vosslab skill naming convention and collision audit

## Design philosophy

Apply the four canonical philosophies from
[docs/REPO_STYLE.md#core-philosophies](../../nsh/vosslab-skills/docs/REPO_STYLE.md):
long-term over short-term (the convention pays for itself across all future skill names);
fix the design, not the symptom (current pain is structural prefix sharing, not individual
bad names); fresh subagent per task (not invoked here -- single-doc + single-script work);
atomic task decomposition (each work package below is independently completable).

## 1. Objective

Publish a vosslab skill naming convention plus a tool that enumerates loaded skills, so
future skills (and any rename of existing skills) can be checked for prefix collisions
mechanically. Output: one new doc, one new tool script, two cross-reference touch-ups, one
changelog entry. A second milestone applies the accepted rename map to the existing skill
directories and updates references.

## 2. Scope

In scope:

- Author `docs/SKILL_NAMING.md` defining the rules: kebab-case format (refer to spec),
  front-loaded distinguisher, shared suffix families, no redundant `-skill`-style tokens,
  frontmatter `name` matches directory.
- Author `tools/list_loaded_skills.py` that enumerates currently loaded skill names from the
  filesystem (repo skills + `~/.claude/skills/` + `~/.claude/plugins/cache/<plugin>/<active-version>/skills/`)
  plus the manually maintained harness-built-ins list. Output: tab-separated skill/source
  rows by default (sorted, deduped), with a `--names-only` mode for one skill name per line.
- Audit the 22 current vosslab skills against the convention; record the result as a table
  inside `docs/SKILL_NAMING.md` (compliant / borderline / violator with proposed rename).
- Add cross-references from `docs/REPO_STYLE.md` (Naming section) and
  `skills/skill-writing-guide/SKILL.md` to `docs/SKILL_NAMING.md`.
- Add a changelog entry under today's date.

## 3. Non-goals (out of scope)

- Renaming is deferred until M2. M1 publishes the convention and audit first; M2 applies
  the accepted rename map with `git mv`, frontmatter updates, reference cleanup, and index
  regeneration if required.
- Redefining the manager / doer / reviewer mode taxonomy in `docs/SKILL_PHILOSOPHY_REVIEW.md`.
  The suffix families align with it but the taxonomy is untouched.
- Editing any `superpowers:*` skill or any other plugin source. Plugin name lists in this
  plan are read-only inputs.
- Adding skill-loading logic to the harness. The new tool is a standalone enumerator, not a
  loader.
- Enforcing the convention via a pytest. M2 relies on manual audit plus
  `tools/list_loaded_skills.py --check`; full lint enforcement remains out of scope.

## 4. Current state

Twenty-two vosslab skills under `skills/`, named ad-hoc. Concrete pain:

- Three skills share leading `manager-` (driven-execution, make-new-plan, review-existing-plan).
- Two skills cause short autocomplete ambiguity on `re...` (read-repo-rules,
  review-code-changes).
- One skill (`pdf-skill`) has a redundant `-skill` token and a frontmatter / directory-name
  mismatch documented in `docs/SKILL_PHILOSOPHY_REVIEW.md`.
- No central naming doc; new authors copy whichever sibling they happened to read.
- `superpowers:` plugin skills coexist in autocomplete with vosslab skills; user has already
  implicitly avoided `sub...` and `disp...` prefixes to dodge collisions but this is not
  written down anywhere.
- Harness built-ins (`init`, `review`, `simplify`, `loop`, `schedule`, `update-config`,
  `keybindings-help`, `fewer-permission-prompts`, `claude-api`, `security-review`) are
  short, single-token names that vosslab skills must not adopt as a leading token.

## 5. Architecture boundaries and ownership

- `docs/SKILL_NAMING.md` -- canonical naming convention. Owned by this repo's docs.
- `tools/list_loaded_skills.py` -- read-only enumerator. Owned by repo `tools/`.
- `docs/REPO_STYLE.md` -- root style doc. Existing "Naming" section gains a one-line link.
- `skills/skill-writing-guide/SKILL.md` -- existing skill-authoring guide. Gains a one-line
  link to the new convention.
- `docs/CHANGELOG.md` -- standard changelog touch.

External (read-only): `~/.claude/plugins/cache/`, `~/.claude/skills/` -- the tool walks
these but never writes.

### Mapping: milestones and workstreams to components and patches

Two milestones: M1 publishes the convention and tool; M2 applies the accepted rename map.

M1 workstreams map 1:1 to components:

- WS-A: convention-doc -> `docs/SKILL_NAMING.md` (Patch 1)
- WS-B: skill-enumerator -> `tools/list_loaded_skills.py` (Patch 2)
- WS-C: cross-references -> `docs/REPO_STYLE.md`, `skills/skill-writing-guide/SKILL.md`
  (Patch 3)
- WS-D: changelog -> `docs/CHANGELOG.md` (Patch 4)

M2 workstream:

- WS-E: rename-existing-skills -> `docs/SKILL_NAMING.md` (final map),
  `skills/<old>/ -> skills/<new>/` (git mv + frontmatter), repo-wide references,
  `docs/SKILLS_INDEX.md`, `docs/CHANGELOG.md` (Patches 5, 6, 7)

Components use durable terminology (`docs`, `tools`, `skills`).

## 6. Milestone plan

M1 publishes the convention and collision-checking tool. M2 applies the accepted rename
map to existing skills.

### M1: Skill naming convention published

- Depends on: none.
- Entry criteria: none.
- Exit criteria: all four patches landed; `tools/list_loaded_skills.py` runs cleanly under
  `source source_me.sh && python3 tools/list_loaded_skills.py` and prints a non-empty
  sorted list; `docs/SKILL_NAMING.md` lists every one of the 22 vosslab skills in its audit
  table; cross-reference links resolve on github.com.
- Deliverables: convention doc, enumerator script, two cross-references, changelog entry.
- Done checks: see Section 10 (acceptance) and Section 11 (test/verification).

### M2: Existing skill names corrected

- Depends on: M1.
- Entry criteria: `docs/SKILL_NAMING.md` exists; `tools/list_loaded_skills.py` runs cleanly;
  the audit table has proposed names for all violators.
- Exit criteria: all accepted renames are applied with `git mv`; each renamed skill's
  frontmatter `name` matches the new directory name; all repo references to renamed skills
  are updated; `docs/SKILLS_INDEX.md` is regenerated if required; changelog records the
  rename pass.
- Deliverables: renamed skill directories, corrected frontmatter names, updated references,
  regenerated index if applicable, changelog entry.
- Done checks: see Section 10 (acceptance) and Section 11 (test/verification).

## 7. Workstream breakdown

### WS-A: convention-doc

- Goal: Publish `docs/SKILL_NAMING.md` with rules, suffix families, audit table, and a
  reference to the enumerator.
- Owner: planner.
- Work packages: WP-A1, WP-A2 (2 packages).
- Interfaces: needs WS-B for the script reference; provides cross-link target for WS-C.
- Expected patches: 1 (Patch 1).

### WS-B: skill-enumerator

- Goal: Ship a small Python tool that lists loaded skill names from the filesystem.
- Owner: coder.
- Work packages: WP-B1 (1 package).
- Interfaces: needs nothing; provides script that WS-A documents.
- Expected patches: 1 (Patch 2).

### WS-C: cross-references

- Goal: Link existing style docs to the new convention so authors find it.
- Owner: planner.
- Work packages: WP-C1 (1 package).
- Interfaces: needs WS-A landed first.
- Expected patches: 1 (Patch 3).

### WS-D: changelog

- Goal: Record the convention publication in `docs/CHANGELOG.md`.
- Owner: planner.
- Work packages: WP-D1 (1 package).
- Interfaces: needs WS-A, WS-B, WS-C summaries.
- Expected patches: 1 (Patch 4).

### WS-E: rename-existing-skills (M2)

- Goal: Apply accepted skill renames so current skill names follow the convention.
- Owner: coder.
- Work packages: WP-E1, WP-E2, WP-E3 (3 packages).
- Interfaces: depends on WS-A and WS-B; updates docs touched by WS-A if rename choices
  differ from the audit table.
- Expected patches: 2-3, depending on the number of references updated.

Workstream count is below the manager-make-new-plan target range (4-8) because this is a
docs-and-script delivery, not a multi-coder milestone. Documented as an exception per
plan-quality-standard Section 2 ("if work is inherently serial").

## 8. Work package specs

### WP-A1: Draft convention rules and suffix family table

- Owner: planner.
- Touch points: `docs/SKILL_NAMING.md` (new file).
- Acceptance criteria:
  - File starts with sentence-case `# Skill naming convention` heading.
  - States the five rules: (1) front-load the distinguisher, no two vosslab skills share
    a 5+ char leading token; (2) use a shared suffix family from a documented table;
    (3) avoid prefixes that match any currently loaded plugin or harness skill name;
    (4) no redundant tokens (`-skill`, `-tool`, `-helper`); (5) frontmatter `name` matches
    directory name (cite skill spec).
  - Includes suffix-family table covering at minimum: `-engineer`, `-expert`, `-writer`,
    `-reviewer`, `-manager`, `-docs`, `-fix`, `-guide`, `-starter`, `-builder`.
  - Lists the harness built-ins that vosslab skills must not adopt as a leading token:
    `init`, `review`, `simplify`, `loop`, `schedule`, `update-config`, `keybindings-help`,
    `fewer-permission-prompts`, `claude-api`, `security-review`. Note that this list is
    advisory; re-audit when the harness updates.
  - Documents how to enumerate currently loaded skills, pointing to
    `tools/list_loaded_skills.py` (WP-B1).
  - ASCII-only per `docs/MARKDOWN_STYLE.md`.
- Verification commands:
  - `source source_me.sh && python3 tests/check_ascii_compliance.py docs/SKILL_NAMING.md`
- Dependencies: none (script reference is forward; written as a relative link before WP-B1
  lands).

### WP-A2: Audit and rename-mapping table

- Owner: planner.
- Touch points: `docs/SKILL_NAMING.md` (append the audit table).
- Acceptance criteria:
  - Table covers all 22 current vosslab skills (run `ls skills/ | wc -l` -> 22).
  - Each row has: current name, status (compliant / borderline / violator), proposed name
    (or "no change"), one-line rationale.
  - Violators identified at minimum (these have a concrete prefix-collision pain or a
    spec-rule violation called out in Section 4):
    `pdf-skill` (redundant `-skill` token + frontmatter mismatch);
    `manager-driven-execution`, `manager-make-new-plan`, `manager-review-existing-plan`
    (3-way prefix collision on `manager-`);
    `review-code-changes` and `read-repo-rules` (2-way prefix collision on `re-`).
  - Borderline (no current collision, but verb-first or no clear suffix family) with
    optional rename suggestions: `orchestrate-next-milestone` (verb-first; could move to
    `-manager` family), `python-code-review` (consistent suffix would be `-reviewer`),
    `web-game-parallel-build` (long name, no peer in a `-builder` family yet).
  - No proposed name shares a 5+ char leading token with any other vosslab proposed name,
    any currently loaded `superpowers:` skill, or any harness built-in (verified manually
    against the WP-B1 output).
  - Note in the table that renames themselves are deferred to a follow-up plan.
- Verification commands:
  - `ls /Users/vosslab/nsh/vosslab-skills/skills/ | wc -l` (must equal 22; confirm row count
    matches).
  - Manual eyeball of leading-token uniqueness against
    `python3 tools/list_loaded_skills.py` output.
- Dependencies: WP-B1 (script must exist for the eyeball verification step).

### WP-B1: Implement tools/list_loaded_skills.py

- Owner: coder.
- Touch points: `tools/list_loaded_skills.py` (new file, executable, shebang).
- Acceptance criteria:
  - Shebang `#!/usr/bin/env python3` on line 1; module docstring on line 2.
  - Tabs for indentation, ASCII only, snake_case filename per `docs/PYTHON_STYLE.md`.
  - Uses standard library only (`pathlib`, `argparse`, `sys`, etc.; no third-party imports).
  - Walks: `<repo>/skills/*/`, `~/.claude/skills/*/`,
    `~/.claude/plugins/cache/*/*/skills/*/`. Each leaf directory name with a sibling
    `SKILL.md` is one entry.
  - Cache walks must dedupe across plugin versions (e.g., superpowers 5.0.7 + 5.1.0 yield
    one row per skill name, not two).
  - Skips `~/.claude/plugins/marketplaces/` (those are listings, not loaded).
  - Includes a hardcoded harness-built-ins list (from WP-A1) in the output, marked with a
    `[harness]` source tag.
  - Default output format: `<name>\t<source>` lines, sorted by name, where `<source>` is
    one of `repo`, `personal`, `plugin:<plugin-name>`, `harness`.
  - `--names-only` flag prints just the names, one per line, sorted.
  - `--check <name>` flag prints any loaded names that collide with `<name>` and exits 1
    if any exist, 0 otherwise. Collision rule: split each name on the first hyphen and
    compare the leading hyphen-delimited token; report a collision when the candidate's
    leading token equals a loaded name's leading token AND that token is at least 5
    characters long. Example: `--check manager-foo` reports the three existing `manager-`
    skills because they share the 7-char leading token `manager`.
  - `argparse` follows minimalism rule (no flags beyond `--names-only` and `--check`).
- Verification commands:
  - `source source_me.sh && pyflakes tools/list_loaded_skills.py`
  - `source source_me.sh && python3 tools/list_loaded_skills.py | head -5` (non-empty,
    tab-separated).
  - `source source_me.sh && python3 tools/list_loaded_skills.py --names-only` (non-empty,
    sorted, one name per line).
  - `source source_me.sh && python3 tools/list_loaded_skills.py --check manager-foo` (lists
    `manager-driven-execution`, `manager-make-new-plan`, `manager-review-existing-plan`;
    exits non-zero).
  - `source source_me.sh && python3 tests/check_ascii_compliance.py tools/list_loaded_skills.py`
  - `chmod +x tools/list_loaded_skills.py && test -x tools/list_loaded_skills.py`.
- Dependencies: none.

### WP-C1: Add cross-reference links

- Owner: planner.
- Touch points: `docs/REPO_STYLE.md`, `skills/skill-writing-guide/SKILL.md`.
- Acceptance criteria:
  - In `docs/REPO_STYLE.md`, the existing "## Naming" section gains a one-line bullet
    linking to `[docs/SKILL_NAMING.md](SKILL_NAMING.md)` for skill-folder names. Link uses
    same-folder relative form per `docs/MARKDOWN_STYLE.md`.
  - In `skills/skill-writing-guide/SKILL.md`, the section that introduces the directory
    layout / frontmatter gains a one-line link to
    `[docs/SKILL_NAMING.md](../../docs/SKILL_NAMING.md)` (relative path from
    `skills/skill-writing-guide/`).
  - No other content in either file is altered.
- Verification commands:
  - `source source_me.sh && python3 tests/check_ascii_compliance.py docs/REPO_STYLE.md skills/skill-writing-guide/SKILL.md`
  - Manual: open both links and confirm they resolve to the new doc.
- Dependencies: WP-A1 (target file must exist).

### WP-D1: Append changelog entry

- Owner: planner.
- Touch points: `docs/CHANGELOG.md`.
- Acceptance criteria:
  - New entry under today's date heading (or new heading if today does not exist),
    following the date-block subsection order in `docs/REPO_STYLE.md` (Additions,
    Behavior changes, Fixes, Removals, Decisions, Tests).
  - Entry mentions Patch 1 (convention doc), Patch 2 (enumerator tool), Patch 3
    (cross-references), Patch 4 (this changelog entry); calls out that renames are
    deferred.
- Verification commands:
  - `source source_me.sh && python3 tests/check_ascii_compliance.py docs/CHANGELOG.md`
- Dependencies: WP-A1, WP-B1, WP-C1 (entry summarizes their patches).

### WP-E1: Finalize rename map

- Owner: planner.
- Touch points: `docs/SKILL_NAMING.md`.
- Acceptance criteria:
  - Final rename map is recorded for every violator.
  - Each rename has a one-line rationale.
  - No final name shares a 5+ character leading token with any other vosslab skill, loaded
    plugin skill, or harness built-in.
  - Open questions about `pdf-skill`, `parallel-plan`, and `gas-town-workflow` are resolved
    or explicitly marked as deferred.
- Verification commands:
  - `source source_me.sh && python3 tools/list_loaded_skills.py --names-only`
  - Manual check of final rename map against loaded skills and proposed vosslab names.
- Dependencies: M1.

### WP-E2: Rename skill directories and frontmatter

- Owner: coder.
- Touch points: `skills/*/`, renamed skill `SKILL.md` files.
- Acceptance criteria:
  - Each accepted rename is applied with `git mv`.
  - Each renamed skill's frontmatter `name` exactly matches the new directory name.
  - No old renamed directory remains under `skills/`.
  - No new directory uses a redundant suffix such as `-skill`, `-tool`, or `-helper`.
- Verification commands:
  - `find skills -mindepth 1 -maxdepth 1 -type d | sort`
  - `grep -R "name:" skills/*/SKILL.md`
  - `source source_me.sh && python3 tests/check_ascii_compliance.py skills/*/SKILL.md`
- Dependencies: WP-E1.

### WP-E3: Update references, index, and changelog

- Owner: coder.
- Touch points: repo docs, tests, scripts, `docs/SKILLS_INDEX.md`, `docs/CHANGELOG.md`.
- Acceptance criteria:
  - All references to old skill directory names are updated or intentionally preserved
    only in changelog/history context.
  - `docs/SKILLS_INDEX.md` is regenerated if the repo has a standard generator.
  - `docs/SKILL_NAMING.md` audit table reflects final names and no longer presents accepted
    renames as merely proposed.
  - Changelog records the rename pass under today's date.
- Verification commands:
  - `grep -R "manager-driven-execution\|manager-make-new-plan\|manager-review-existing-plan\|pdf-skill" .`
  - `source source_me.sh && python3 tests/check_ascii_compliance.py docs/CHANGELOG.md docs/SKILL_NAMING.md`
  - Run the repo's standard index-generation command if one exists
    (`source source_me.sh && python3 tools/build_skills_index.py`).
- Dependencies: WP-E2.

## 9. Patch plan and reporting

M1 patches:

- Patch 1: `docs/SKILL_NAMING.md` convention doc with rules, suffix table, audit table.
- Patch 2: `tools/list_loaded_skills.py` enumerator with `--names-only` and `--check`.
- Patch 3: `docs/REPO_STYLE.md` and `skills/skill-writing-guide/SKILL.md` cross-references.
- Patch 4: `docs/CHANGELOG.md` entry.

M2 patches:

- Patch 5: `docs/SKILL_NAMING.md` final rename map (audit table updated to "accepted").
- Patch 6: `git mv` of skill directories plus frontmatter `name` updates.
- Patch 7: reference updates across the repo, `docs/SKILLS_INDEX.md` regeneration, and
  `docs/CHANGELOG.md` rename-pass entry.

Each patch touches at most two components; no split needed.

## 10. Acceptance criteria and gates

- Documentation gate: all touched markdown files pass `tests/check_ascii_compliance.py`
  and render without broken relative links on github.com.
- Tool gate: `pyflakes tools/list_loaded_skills.py` is clean; the four verification
  invocations in WP-B1 succeed (one of them exits 1 by design for `--check manager-foo`).
- Audit gate: WP-A2 audit table contains exactly 22 rows for vosslab skills. Loaded-skill
  conflicts (proposed rename vs an existing loaded plugin or harness skill) are verified by
  running `--check <proposed-name>` for each proposed rename. Proposed-name vs
  proposed-name conflicts are verified manually by sorting the proposed-name column and
  eyeballing leading tokens; no automated check is in scope this plan.
- Release gate: changelog entry exists under today's heading.

## 11. Test and verification strategy

- Unit checks: pyflakes lint + ASCII compliance (existing per-file gates).
- Integration checks: run the new tool end-to-end on the user's machine; spot-check the
  output includes vosslab skills, superpowers skills, and harness built-ins.
- Smoke checks: `--check` against three known leading tokens (`manager-`, `re-`, `pdf-`)
  and confirm sensible output.
- Regression: none required; no existing code is modified beyond two additive cross-link
  bullets.
- Failure semantics: pyflakes failures, ASCII violations, or a `--names-only` empty list
  block patch closure.

## 12. Migration and compatibility

M1 is additive only: it adds the convention doc, enumerator tool, cross-references, and
changelog entry.

M2 performs the compatibility-affecting rename pass. Renames are applied with `git mv`,
frontmatter `name` updates, reference cleanup, and `docs/SKILLS_INDEX.md` regeneration if
required. Historical references may remain only in changelog or explicitly marked history
contexts.

Because skill folder names are user-facing invocation names, M2 is intentionally separated
from M1 and gated by the accepted rename map.

## 13. Risk register

| Risk | Impact | Trigger | Mitigation | Owner |
| --- | --- | --- | --- | --- |
| Audit table drifts from real `skills/` directory | Low | New skill added or one removed | Run `ls skills/` and recount before publish; tool's `--names-only` confirms set | planner |
| Harness built-ins list goes stale on harness upgrade | Low-medium | Harness ships a new built-in command | Doc states list is advisory and re-checked on upgrade; user can re-run audit | planner |
| Plugin cache holds multiple versions, dedup misses one | Low | Plugin upgrade leaves stale version on disk | Tool dedups by skill name across cache versions (WP-B1 acceptance criterion) | coder |
| Proposed renames in audit table conflict with later user feedback | Low | User picks different rename targets | Renames are deferred to a separate plan; this plan's audit table is a proposal, not a commitment | planner |
| `pdf-skill` frontmatter mismatch surfaces a load error before the rename plan lands | Low | Skill loader strict-checks `name` vs directory | Out of scope here; documented as known gap pointing to the rename plan | planner |

## 14. Rollout and release checklist

- [ ] M1 lands: convention doc, enumerator, cross-references, changelog.
- [ ] Final rename map is accepted.
- [ ] M2 lands: skill directories renamed with `git mv`.
- [ ] Renamed skill frontmatter `name` values match directory names.
- [ ] References and `docs/SKILLS_INDEX.md` are updated.
- [ ] Final verification commands pass.

No staged rollout, feature flag, or canary needed; M1 is documentation plus one read-only
tool, and M2 is a mechanical rename pass guarded by the M1 collision-check tool.

## 15. Documentation close-out

- `docs/SKILL_NAMING.md` is the canonical home for the convention going forward.
- `docs/CHANGELOG.md` records the publication.
- No archive note required; this is the first version of the convention.
- M2 owns the rename pass after the final rename map is accepted.

## 16. Open questions

These questions do not block M1 because no folders are renamed in M1. They must be
resolved or explicitly deferred in WP-E1 before M2 renames land.

- Final form of suffix-family table: include `-expert` as distinct from `-engineer`, or
  collapse? Current state: keep both (`computer-vision-expert` already uses `-expert`;
  collapse can happen in the rename plan if desired).
- Should `parallel-plan` and `gas-town-workflow` be flagged as borderline or compliant in
  the audit? They use one-off suffixes (`-plan`, `-workflow`) but are unique enough that no
  prefix collision exists. Default: borderline, "no change" recommended.
- Should the rename of `pdf-skill` target `pdf-engineer` (build-focused) or `pdf-writer`
  (content-focused)? Decision needed before the follow-up rename plan; recorded here as
  open and answered there.
