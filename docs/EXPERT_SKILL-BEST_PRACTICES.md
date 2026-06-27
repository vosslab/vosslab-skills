# Expert skill best practices

Conventions for authoring domain-expert skills in this repo. An expert skill is
a specialist skill (suffix `-expert` or `-engineer`) that turns vague requests
in one field into explicit, evidence-backed tasks and drives a real project
rather than dispensing generic advice. Eight such skills share a common
skeleton: `geometry-expert`, `vision-expert`, `pyside6-engineer`,
`ui-ux-engineer`, `solid-js-expert`, `typescript-engineer`,
`bptools-writer-expert`, and `webwork-writer-expert`. This doc captures that
skeleton and the local-only reference-survey pattern that `geometry-expert`
pioneered, so a future author picks the right tool for the reference corpus at
hand.

The single most important decision is the corpus-format axis in section 15: a
gitignored, flat-text, maybe-absent book corpus needs a `reference_survey.md`; a
committed, linkable, heading-anchored guide set needs a routing index instead.
Classify the skill on that axis first, then follow the matching sections below.

## Required reference set

Parity is a required interface, not geometry-like depth. Every expert skill ships
the same universal set; the four book-backed skills add two more committed files.
This required-set definition is the standard the parity gate enforces.

Universal required set, present in all eight experts:

- `SKILL.md`: the thin entrypoint with a project-shape Workflow step.
- `agents/openai.yaml`: the OpenAI agent manifest (three `interface` keys).
- `references/task_selection.md`: routes an underspecified request to a path.
- `references/topic_index.md`: maps each user problem to the best reference.
- `references/project_workflow.md`: both the greenfield and existing-repo
  workflows for an outside target project.
- `references/testing_and_oracles.md`: how the skill proves the target improved.

Book-backed required extras, present only in the four skills with a local book
corpus (`geometry-expert`, `vision-expert`, `pyside6-engineer`, `ui-ux-engineer`):

- `references/reference_survey.md`: topic-to-book coverage map with bare-path
  references, validated grep terms, and coverage-strength ratings.
- `references/local_books.md`: the source-map guide for the corpus.

The gitignored `references/local-only/` corpus is part of the book-backed pattern
but lives locally and is absent on a clean clone, so the parity gate asserts only
the two committed files, never the physical corpus directory.

Corpus-format rationale: a gitignored, flat-text, maybe-absent book corpus needs
the `reference_survey.md` machine (bare-path references, grep routing,
coverage-strength ratings, graceful-absent fallback). A committed, linkable,
heading-anchored guide set needs a routing index instead, which the four
non-book skills satisfy through their committed `topic_index.md` front door.
Book-backed membership is an explicit allowlist of those four names, not inferred
from the corpus directory, so a missing `local-only/` on a clean clone never
flips a skill out of the set.

### Design intent: a complete tool for an outside target

Each expert skill is a complete tool to invoke on an outside TARGET project, new
or existing, to make that project better. The skill operates on the user's repo,
not on itself. `references/project_workflow.md` carries both a greenfield workflow
and an existing-repo workflow, and the `SKILL.md` project-shape Workflow step
detects which path applies before any edit to the target. The binding behavior:
the skill turns a vague request such as "use this skill to improve my repo" into
a concrete inspection, recommendation, implementation, and validation path. This
is a behavior requirement, not just a file requirement.

The parity gate `tests/test_expert_skill_parity.py` enforces this required set per
skill: the universal files plus the project-shape step for all eight, and the book
trio for the four book-backed names.

## Purpose and scope

An expert skill encodes hard-won judgment in a specialized field: how to frame a
task, which library or algorithm to reach for, what robustness traps to avoid,
and how to validate the result against an oracle. It is a domain-specialist
skill, not a process skill.

- Build an expert skill when the value is domain knowledge that a generalist
  agent lacks: geometry robustness, CV model selection, Qt widget architecture,
  SolidJS reactivity, TypeScript type design.
- Build a process skill instead when the value is a repeatable workflow that
  spans domains (planning, review, doc refresh). Process skills lead with a verb
  and live elsewhere in `skills/`; see [SKILL_NAMING.md](SKILL_NAMING.md).
- Actionable rule: if the leading token of the name would be unique domain
  vocabulary (`geometry`, `vision`, `pyside6`, `typescript`), it is an expert
  skill and belongs to the skeleton described here.

## Naming an expert skill

Expert skills use domain-noun-first ordering with an agent-form suffix. The
domain token at position 1 carries identity; the suffix names what the skill is.

- Use `-expert` for design-and-review specialists (`geometry-expert`,
  `vision-expert`) and `-engineer` for implement-and-refactor specialists
  (`pyside6-engineer`, `typescript-engineer`). Format authors take `-expert`
  too (`bptools-writer-expert`, `webwork-writer-expert`); the standard suffix set
  is `{-expert, -engineer}`. See the Retired names note below for the rename.
- Keep the first three characters unique across all active vosslab skills. This
  catches near-collisions like `web-` versus `webwork-`.
- The frontmatter `name:` must match the directory name exactly.
- Register the name and its rationale in the audit table of
  [SKILL_NAMING.md](SKILL_NAMING.md), and verify with
  `tools/list_loaded_skills.py --check <candidate>`.

## Directory and file layout

An expert skill is a directory under `skills/<name>/` with a thin entrypoint, a
references folder, and an OpenAI agent manifest.

- `skills/<name>/SKILL.md`: the entrypoint (frontmatter plus thin body).
- `skills/<name>/references/*.md`: committed guide files, one concern each.
- `skills/<name>/references/local-only/`: gitignored source corpora (large book
  conversions). Present locally, absent on a clean clone.
- `skills/<name>/agents/openai.yaml`: the OpenAI agent manifest. Mirror
  `skills/geometry-expert/agents/openai.yaml`.
- `agents/openai.yaml` is required by this repo's parity standard, and all eight
  expert skills now ship it. The earlier missing-manifest gap was closed when the
  `webwork-writer-expert` rename added its manifest; new expert skills must
  include the manifest.

### Retired names

- `bptools-writer` was renamed to `bptools-writer-expert`, and `webwork-writer`
  was renamed to `webwork-writer-expert`, standardizing on the
  `{-expert, -engineer}` suffix set. The old names are retired; reference the
  current names everywhere.

## SKILL.md file anatomy

The entrypoint is a YAML frontmatter block followed by a thin Markdown body. Keep
it short and push detail into the reference guides.

- Frontmatter carries exactly two keys that matter: `name` (equals the directory
  name) and `description` (a keyword-packed trigger under 1024 characters).
- Body section order, mirrored from `skills/geometry-expert/SKILL.md`: Overview,
  Workflow, Implementation defaults, Quality bar, Output expectations.
- Keep the entrypoint thin, roughly 70-100 lines. Each Workflow step routes to a
  `references/*.md` guide with a Markdown link rather than inlining the detail.
- Actionable rule: when a body section grows past a few bullets, move the prose
  into a reference guide and leave a one-line pointer with a link.

## Description as trigger

The `description` field is the only text loaded at startup, so it decides whether
the skill fires. Treat it as a trigger surface, not a summary.

- Pack concrete domain keywords plus their synonyms: name the algorithms,
  libraries, file types, and error symptoms a user would type.
- State both what the skill does and when to use it. The geometry description in
  `skills/geometry-expert/SKILL.md` lists primitives, library names, and failure
  modes, then a "Use when" clause.
- Actionable rule: read the description cold and ask whether a user describing
  the problem in their own words would hit at least one keyword. Add synonyms
  until the answer is yes.

## Reference guide files

Reference guides hold the detail the thin entrypoint defers. Each guide owns one
concern so the agent loads only what a step needs.

- One concern per guide, roughly 25-60 lines. Examples in
  `skills/geometry-expert/references/`: `task_selection.md`,
  `algorithm_design.md`, `robustness_and_numerics.md`, `testing_and_oracles.md`.
- Provide a `task_selection`-style guide for routing underspecified requests, one
  or more domain workflow guides, and a source-map guide
  (`local_books.md`) when the skill carries a local corpus.
- Actionable rule: a Workflow step in `SKILL.md` should name the guide it needs
  and link it, so detail lives in exactly one place.

## Large local-only references

Some domains have large book corpora that are too big to commit and meant to be
read locally. These go under `references/local-only/` and are gitignored by
design, because the books are large source material, not skill content to upload
to GitHub.

- The skill ships the small committed survey; the user supplies the large books
  locally. Example corpus: `skills/vision-expert/references/local-only/` holds
  six computer-vision books.
- Reference a local-only book by bare backtick path plus a grep term, for example
  `` `references/local-only/About_Face.txt` `` searched for `posture`. Flat-text
  conversions have no headings, so route by book plus keyword.
- Actionable rule: never write a Markdown link into `local-only/`. A Markdown
  link implies a committed, GitHub-browsable target; these files are absent on a
  clean clone. Bare backtick paths are the intended format, enforced by
  `tests/test_no_local_only_markdown_links.py`.

## Evidence over reputation

A book's reputation is not evidence that it covers a given topic well. Convert
reputation into checked evidence by building a `reference_survey.md`.

- Build `references/reference_survey.md` that maps each domain topic to a book,
  a grep term, a chapter or section label, and a coverage-strength rating
  (`strong`, `partial`, `thin`, `not covered`).
- Verify every grep term actually hits its `local-only/*.txt` file before
  recording it. Name thin topics explicitly and route them to official library
  docs or an oracle instead of pretending a book covers them.
- See a real worked survey at the file path
  `skills/pyside6-engineer/references/reference_survey.md`, which maps three
  shared UX books through a Qt-engineering lens. Use the reference
  implementation at `skills/geometry-expert/references/reference_survey.md` as
  the structural model.
- Actionable rule: a survey row earns its place only when its grep term hits the
  book; an unverified term is a guess, not evidence.

## Graceful degradation and pattern boundary

The survey is committed, but the books it indexes may be absent on a clean clone.
The skill must still work when the corpus is missing or thin.

- State the fallback in each survey's "How to use" block: when a book is missing
  or its coverage is thin, route to official library or tool docs and fall back
  to an oracle, brute force, or first-principles reasoning.
- State the pattern boundary on the corpus-format axis, not "book versus no
  book". The `reference_survey.md` machine (bare-path references, grep routing,
  coverage-strength, graceful-absent fallback) fits a gitignored, flat-text,
  maybe-absent corpus.
- A committed, linkable, heading-anchored reference set needs a routing index
  instead: a table that maps each topic to a guide link. That is the
  committed-set analog of the survey. Examples:
  `skills/solid-js-expert/references/api-cheatsheet.md` and
  `skills/typescript-engineer/references/checklist.md`.
- Actionable rule: pick the survey when the corpus is gitignored and opaque; pick
  a routing index when the guides are committed and heading-anchored. Section 15
  classifies all eight experts on this axis.

## Project evidence first workflow

An expert skill drives a project, so it gathers evidence before it changes
behavior. The first Workflow steps detect the project shape and build evidence.

- Detect greenfield versus existing project and branch the workflow. Existing:
  inventory the code and capture characterization fixtures before edits.
  Greenfield: write the design source of truth first, then seed fixtures.
  See `skills/geometry-expert/references/project_workflow.md`.
- Build a test corpus or fixture set before feature code, and validate every
  result against a trusted oracle (a known-good library or brute force).
- The domain contract artifact is optional per domain. Geometry writes a
  `docs/GEOMETRY_MODEL.md` contract; a UX skill has no equivalent and should not
  invent one.
- Actionable rule: add a project-shape Workflow step that branches new versus
  existing before any step that edits domain code.

## Authoring voice and prompting

Write the skill the way the repo writes everything: positive prompting and plain
imperative voice.

- Tell the agent what to do, not what to avoid. Name the tool and move on:
  "use exact predicates on degenerate inputs", not "do not use naive floats".
- Small language models confuse negative phrasing with instructions, which
  produces flawed code. This follows the core philosophies in
  [REPO_STYLE.md](REPO_STYLE.md).
- Actionable rule: scan each Workflow step for "do not" and "avoid"; rewrite each
  as a direct instruction naming the preferred action.

## Markdown style compliance

Skill Markdown follows the repo Markdown style. The validation gate fails on
violations, so comply while authoring.

- ASCII and ISO-8859-1 only; escape symbols such as `&alpha;`. Sentence-case
  headings of three to six words. Use `-` for bullets.
- Backtick a path only when the link text would otherwise differ from the path.
  When linking another `docs/` file from here, use the bare filename in both the
  link text and the URL, for example [MARKDOWN_STYLE.md](MARKDOWN_STYLE.md).
- Do not use `..` paths inside a skill's Markdown to leave the skill folder; use
  plain backticked names so the skill travels when loaded as a plugin.
- Actionable rule: follow [MARKDOWN_STYLE.md](MARKDOWN_STYLE.md) and confirm with
  the ASCII and link tests in the validation gate below.

## Registration and regeneration

A new or renamed skill must register in the generated indexes and the repo docs.
The manifests are generated; edit the source and regenerate.

- Regenerate the platform manifests and the skills index after adding a skill:
  `source source_me.sh && python3 tools/build_plugin_manifest.py` writes
  `.claude-plugin/plugin.json`, and `tools/build_skills_index.py` writes
  `docs/SKILLS_INDEX.md`. Do not hand-edit those outputs.
- Add one line to the `## Documentation` list in `README.md` and one dated entry
  in `docs/CHANGELOG.md` describing the addition.
- Actionable rule: body-only edits to a SKILL.md leave the frontmatter
  byte-identical, so the generated manifests show no drift and need no
  regeneration; only a frontmatter change requires regenerating.

## Validation gate tests

Run the full skill validation gate from the repo root with
`source source_me.sh && python3 -m pytest <test>`. Ten tests guard expert-skill
changes:

- `tests/test_skill_frontmatter.py`: frontmatter is well-formed and intact.
- `tests/test_skill_prefix_uniqueness.py`: no first-three-character collision.
- `tests/test_skill_internal_links.py`: internal skill links resolve.
- `tests/test_codex_yaml_skill_parse.py`: each `agents/openai.yaml` parses.
- `tests/test_skills_index_in_sync.py`: `docs/SKILLS_INDEX.md` matches source.
- `tests/test_plugin_manifest_drift.py`: `.claude-plugin/plugin.json` matches.
- `tests/test_ascii_compliance.py`: Markdown is ASCII or ISO-8859-1.
- `tests/test_markdown_links.py`: every local Markdown link resolves.
- `tests/test_no_local_only_markdown_links.py`: no Markdown link targets a
  `local-only/` path (bare backtick mentions stay allowed).
- `tests/test_expert_skill_parity.py`: each expert skill carries the required
  reference set (universal files plus a project-shape step; the book trio for the
  four book-backed skills).

Actionable rule: run the gate before reporting a skill change complete, and treat
any manifest drift as diagnostic evidence (inspect whether a frontmatter actually
changed) before regenerating.

## Applicability across eight experts

All eight experts now carry the universal required set (SKILL.md with a
project-shape step, `agents/openai.yaml`, and the four reference guides). The
book trio (`reference_survey.md`, `local_books.md`, and the gitignored
`local-only/` corpus) lives only in the four book-backed skills. The table below
classifies every expert on the corpus-format axis: a gitignored, opaque book
corpus needs a `reference_survey.md`; a committed, structured guide set needs a
linkable routing index. All eight fall cleanly on one side.

| Skill | Universal set | Corpus format | Book trio / routing mechanism |
| --- | --- | --- | --- |
| `geometry-expert` | yes | gitignored book corpus | book trio; `reference_survey.md` reference implementation |
| `vision-expert` | yes | gitignored book corpus | book trio; survey added by this pattern |
| `pyside6-engineer` | yes | gitignored book corpus | book trio; survey added by this pattern |
| `ui-ux-engineer` | yes | gitignored book corpus | book trio; survey added by this pattern |
| `solid-js-expert` | yes | committed guide set | routes via `topic_index.md`; survey not applicable |
| `typescript-engineer` | yes | committed guide set | routes via `topic_index.md`; survey not applicable |
| `bptools-writer-expert` | yes | committed guide set | routes via `topic_index.md`; survey not applicable |
| `webwork-writer-expert` | yes | committed guide set | routes via `topic_index.md`; survey not applicable |

- The four gitignored-corpus skills carry book conversions under
  `references/local-only/` and exploit them through a committed survey plus a
  graceful-absent fallback.
- The four committed-set skills carry heading-anchored guides that are always
  present, so their analog is the committed `topic_index.md` routing front door.
  No survey is added to them.
- Actionable rule: before authoring references for a new expert skill, decide
  which row it joins; that choice determines whether you write a survey or a
  routing index. The universal required set is mandatory regardless of the row.
