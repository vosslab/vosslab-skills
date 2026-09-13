# Skill corpus Astra audit

## Scope and authority

**Fact.** The index defines 40 publishable skills ([docs/SKILLS_INDEX.md](../../SKILLS_INDEX.md#L7)).
Shared discovery excludes the 41st raw entrypoint, deprecated `old-python-code-review`
([install_lib/skill_discovery.py](../../../install_lib/skill_discovery.py#L239-L245)); it appears
only as plan-requested inventory evidence.

**Fact.** Repo policy governs evidence, positive prompting, grounded gates, atomic ownership, and
completion ([docs/REPO_STYLE.md](../../REPO_STYLE.md#L8-L30)); human guidance prioritizes KISS and
the smallest ownership-correct implementation
([docs/HUMAN_GUIDANCE.md](../../HUMAN_GUIDANCE.md#L11-L18)). External-review guidance requires
source-of-truth checks, labeled reasoning, grounded/test-light gates, and positive omission
([ChatGPT_External_Plan_Reviewer_Guidance.md](../../../ChatGPT_External_Plan_Reviewer_Guidance.md#L23-L37),
[ChatGPT_External_Plan_Reviewer_Guidance.md](../../../ChatGPT_External_Plan_Reviewer_Guidance.md#L57-L75),
[ChatGPT_External_Plan_Reviewer_Guidance.md](../../../ChatGPT_External_Plan_Reviewer_Guidance.md#L77-L101)).

**Fact.** The plan adopts A1-A6 and D1-D4 with repository policy taking precedence (`plan-moonlit-noodling-horizon.md:8-24`).

**Limitation.** The plan supplies no URL or local copy of the named post
(`plan-moonlit-noodling-horizon.md:3-6`), and official OpenAI searches did not retrieve it. This
report tests the plan's A1-A6 summary without treating it as verified quotation. The optional book
corpus changed no verdict and was omitted.

## Method

**Fact.** Each live description received two intended and two adjacent requests. `P2` means both
intended requests select it; `N0`-`N2` counts neighboring requests that also select it when read
cold. A sound result is `P2/N0`.

**Fact.** `Lines` is `wc -l`; `chars` is `wc -m`, including newlines (plain `wc` reports bytes in
column three); `Refs` counts committed Markdown beneath `references/`, excluding `local-only/`. `Load` is
blanket (`B`), contextual (`C`), or neither (`-`). `Dup` flags generic delegation (`D`), within-file
repetition (`I`), the expert skeleton (`S`), or consumer-specific detail (`C`). These are cost
signals, not gates.

**Interpretation.** A neighboring hit matters when a routine edit does not need the skill's
specialized judgment. The cases use common work, such as centering one element or adding one type
annotation, rather than unrelated prompts.

## Glossary

| Term | Meaning |
| --- | --- |
| Astra heuristics | A1-A6 as summarized by the plan; adopted inputs, not verified quotations. |
| Live skill | Included by shared discovery; deprecated entries are inventory evidence only. |
| Trigger surface | Startup-loaded frontmatter `description` that decides applicability. |
| Entrypoint | One `SKILL.md`, including frontmatter and body; subject to the paired budget. |
| Reference / route | Conditional support file / linked instruction that selects when to read it. |
| Blanket (`B`) / contextual (`C`) load | Reading required every invocation / only on a named condition. |
| Context cost | Lines introduced after a trigger; a comparative proxy, not a token count. |
| Intended / neighboring request | Work that needs the skill / adjacent work that does not need its judgment. |
| `P2/N0` | Both intended requests select the skill; neither neighboring request does. |
| D1 / D4 | Keep, Narrow, Move, Automate, or Remove / deliverable, checks, and authorization boundary. |

## Trigger behavior

**Fact.** Thirteen of 17 expert descriptions and three other live descriptions over-trigger in the
fixed matrix. The other 24 live descriptions are `P2/N0`. Sources are the current frontmatter
descriptions.

The table contains every over-trigger. `Now -> proposed` is the result after re-judging the same
four cases against the recommended description.

| Skill | Intended requests | Neighboring requests that fire | Now -> proposed | Recommended description | Source |
| --- | --- | --- | --- | --- | --- |
| `pdf-guide` | review pagination; create print PDF | read this PDF | P2/N1 -> P2/N0 | Use when PDF rendering, pagination, or visual page layout is part of correctness while reading, creating, or reviewing a PDF. | [SKILL.md](../../../skills/documentation/pdf-guide/SKILL.md#L3) |
| `css-creative-expert` | debug cascade; design responsive theme | center one div; rename custom property | P2/N2 -> P2/N0 | Use when CSS-specific composition, cascade behavior, responsive layout, theming, or motion requires design or diagnostic judgment. | [SKILL.md](../../../skills/experts/css-creative-expert/SKILL.md#L3) |
| `geometry-expert` | robust intersection; Delaunay degeneracy | add type hint; rename point | P2/N2 -> P2/N0 | Use when computational-geometry robustness, topology, predicates, intersections, tessellation, motion planning, or realizability determines correctness. | [SKILL.md](../../../skills/experts/geometry-expert/SKILL.md#L3) |
| `glass-expert` | prove live glass; debug sampling | add Swift return type; rename toolbar label | P2/N2 -> P2/N0 | Use when Apple Liquid Glass behavior requires backdrop sampling, surface placement, morphing, capture evidence, or glass-specific contrast judgment. | [SKILL.md](../../../skills/experts/glass-expert/SKILL.md#L3) |
| `human-interact-expert` | design usability study; task analysis | move one button; rewrite tooltip | P2/N2 -> P2/N0 | Use when selecting or conducting an HCI method, usability evaluation, user study, task analysis, or evidence-based interaction assessment. | [SKILL.md](../../../skills/experts/human-interact-expert/SKILL.md#L3) |
| `podman-expert` | debug rootless network; design Quadlet | format Containerfile; rename service | P2/N2 -> P2/N0 | Use when designing or diagnosing a Podman runtime, build, networking, storage, pod, Quadlet, registry, or macOS machine workflow. | [SKILL.md](../../../skills/experts/podman-expert/SKILL.md#L3) |
| `postgresql-expert` | tune EXPLAIN; design PITR | format SQL; rename fixture table | P2/N2 -> P2/N0 | Use when PostgreSQL-specific schema, query-plan, indexing, MVCC, maintenance, replication, recovery, pooling, or migration judgment is central. | [SKILL.md](../../../skills/experts/postgresql-expert/SKILL.md#L3) |
| `pyside6-engineer` | model-view table; threaded signals | rename widget; add annotation | P2/N2 -> P2/N0 | Use when PySide6-specific widget architecture, signals and slots, model-view design, threading, window behavior, or GUI testing requires Qt judgment. | [SKILL.md](../../../skills/experts/pyside6-engineer/SKILL.md#L3) |
| `rust-code-expert` | unsafe FFI; Tokio cancellation | fix unused import; rename local | P2/N2 -> P2/N0 | Use when Rust-specific ownership, lifetimes, traits, Result flow, async/Tokio, unsafe, FFI, Cargo, or native-target design determines the solution. | [SKILL.md](../../../skills/experts/rust-code-expert/SKILL.md#L3) |
| `solid-js-expert` | signal tracking; server action | rename component; copy-edit JSX | P2/N2 -> P2/N0 | Use when SolidJS or SolidStart reactivity, routing, server/client boundaries, data mutation, component semantics, or React migration determines the solution. | [SKILL.md](../../../skills/experts/solid-js-expert/SKILL.md#L3) |
| `typescript-engineer` | branded boundary; conditional type | add return annotation; rename interface | P2/N2 -> P2/N0 | Use when strict TypeScript type design or compiler diagnosis is central: inference, generics, mapped or conditional types, branded types, overloads, declarations, or module-boundary contracts. | [SKILL.md](../../../skills/experts/typescript-engineer/SKILL.md#L3) |
| `ui-ux-engineer` | heuristic evaluation; redesign error states | center modal; fix label typo | P2/N2 -> P2/N0 | Use when a requested interface review or redesign requires product-level hierarchy, interaction, accessibility, forms, navigation, states, or responsive UX judgment. | [SKILL.md](../../../skills/experts/ui-ux-engineer/SKILL.md#L3) |
| `vision-expert` | tune segmentation; evaluate OCR | add docstring; rename image variable | P2/N2 -> P2/N0 | Use when computer-vision pipeline design or evaluation is central: image processing, detection, segmentation, tracking, OCR, datasets, robustness, or model selection. | [SKILL.md](../../../skills/experts/vision-expert/SKILL.md#L3) |
| `wasm-rust-expert` | browser parity; choose WASI target | format Rust module; rename JS binding | P2/N2 -> P2/N0 | Use when Rust/WebAssembly boundary design, wasm-bindgen or web-sys integration, WASI targeting, browser Canvas, parity, or Wasm performance is central. | [SKILL.md](../../../skills/experts/wasm-rust-expert/SKILL.md#L3) |
| `html-game-parallel-builder` | parallel game build; multi-lane launch | fix one CSS bug; run one smoke test | P2/N2 -> P2/N0 | Use when the user requests a parallel multi-agent build or major workstream for a modular TypeScript browser game, including integrated serving, smoke testing, export, or Pages delivery. | [SKILL.md](../../../skills/management/html-game-parallel-builder/SKILL.md#L3) |
| `repo-rules-reader` | explicit invocation; rules receipt | start coding; review one file | P2/N2 -> P2/N0 | Load repository rules when the user explicitly invokes this skill or requests a rule-orientation and read-receipt task. | [SKILL.md](../../../skills/orientation/repo-rules-reader/SKILL.md#L3) |

**Fact.** The other 24 live skills are the `K`/`P2/N0` control group in the linked inventory below; their source descriptions start at line 3.

**Interpretation.** Trigger breadth is the highest-impact corpus defect. The failing expert
descriptions enumerate whole technology domains, so they cannot distinguish specialized judgment
from routine edits. Process descriptions are generally more selective.

## Per-skill summary

The first five columns are facts or measurements. `Done` is an interpretation of D4 completion.
`D1 / top fix` is the recommendation. `K` keeps the trigger; `N` narrows it.

| Skill | Lines/chars/refs | Trig | Load | Dup | Done | D1 / top fix | Evidence |
| --- | ---: | --- | --- | --- | --- | --- | --- |
| `agents-md-fixer` | 165/7,277/0 | K | - | D,I | yes | Narrow repeated bare-path rule | [SKILL.md](../../../skills/documentation/agents-md-fixer/SKILL.md#L1-L165) |
| `arch-docs` | 111/4,794/0 | K | C | D | partial | Narrow completion; move delegation | [SKILL.md](../../../skills/documentation/arch-docs/SKILL.md#L1-L111) |
| `book-to-markdown` | 65/2,139/4 | K | C | - | partial | Narrow completion contract | [SKILL.md](../../../skills/documentation/book-to-markdown/SKILL.md#L1-L65) |
| `docset-updater` | 162/8,567/0 | K | C | D,I | yes | Narrow dependency order to one owner | [SKILL.md](../../../skills/documentation/docset-updater/SKILL.md#L1-L162) |
| `news-release-docs` | 102/4,909/2 | K | C | D | yes | Move generic delegation | [SKILL.md](../../../skills/documentation/news-release-docs/SKILL.md#L1-L102) |
| `pdf-guide` | 67/2,521/0 | N | - | - | yes | Narrow trigger | [SKILL.md](../../../skills/documentation/pdf-guide/SKILL.md#L1-L67) |
| `readme-docs` | 276/13,982/4 | K | C | D,I | yes | Narrow repeated About rule | [SKILL.md](../../../skills/documentation/readme-docs/SKILL.md#L1-L276) |
| `screenshot-docs` | 280/13,779/6 | K | C | D,I | yes | Narrow repeated sentinel handoff | [SKILL.md](../../../skills/documentation/screenshot-docs/SKILL.md#L1-L280) |
| `see-also-docs` | 218/9,966/1 | K | C | D | yes | Move generic delegation | [SKILL.md](../../../skills/documentation/see-also-docs/SKILL.md#L1-L218) |
| `setup-install-usage-docs` | 136/6,135/0 | K | C | D | partial | Narrow completion; move delegation | [SKILL.md](../../../skills/documentation/setup-install-usage-docs/SKILL.md#L1-L136) |
| `bptools-writer-expert` | 114/6,255/20 | K | B | D | yes | Move delegation; keep live reads | [SKILL.md](../../../skills/experts/bptools-writer-expert/SKILL.md#L1-L114) |
| `color-accessibility-expert` | 226/12,752/6 | K | C | D | yes | Move delegation; keep re-audit | [SKILL.md](../../../skills/experts/color-accessibility-expert/SKILL.md#L1-L226) |
| `css-creative-expert` | 102/5,480/6 | N | C | S | yes | Narrow trigger | [SKILL.md](../../../skills/experts/css-creative-expert/SKILL.md#L1-L102) |
| `geometry-expert` | 100/5,274/8 | N | C | S | yes | Narrow trigger | [SKILL.md](../../../skills/experts/geometry-expert/SKILL.md#L1-L100) |
| `glass-expert` | 99/5,817/12 | N | C | S | yes | Narrow trigger; review maintenance route | [SKILL.md](../../../skills/experts/glass-expert/SKILL.md#L1-L99) |
| `human-interact-expert` | 94/5,187/6 | N | C | S | yes | Narrow trigger | [SKILL.md](../../../skills/experts/human-interact-expert/SKILL.md#L1-L94) |
| `podman-expert` | 95/5,362/6 | N | C | S | yes | Narrow trigger | [SKILL.md](../../../skills/experts/podman-expert/SKILL.md#L1-L95) |
| `postgresql-expert` | 90/5,385/6 | N | C | S | yes | Narrow trigger | [SKILL.md](../../../skills/experts/postgresql-expert/SKILL.md#L1-L90) |
| `pyside6-engineer` | 78/6,261/12 | N | C | D,S | yes | Narrow trigger; move delegation | [SKILL.md](../../../skills/experts/pyside6-engineer/SKILL.md#L1-L78) |
| `rust-code-expert` | 100/5,943/6 | N | C | S | yes | Narrow trigger | [SKILL.md](../../../skills/experts/rust-code-expert/SKILL.md#L1-L100) |
| `solid-js-expert` | 126/8,677/19 | N | C | D | yes | Narrow trigger; retain routed guides | [SKILL.md](../../../skills/experts/solid-js-expert/SKILL.md#L1-L126) |
| `svg-creator-expert` | 131/7,429/9 | K | C | S | yes | Keep | [SKILL.md](../../../skills/experts/svg-creator-expert/SKILL.md#L1-L131) |
| `typescript-engineer` | 250/14,638/25 | N | C | D,C | yes | Narrow trigger; move generic delegation | [SKILL.md](../../../skills/experts/typescript-engineer/SKILL.md#L1-L250) |
| `ui-ux-engineer` | 79/4,337/8 | N | C | S | yes | Narrow trigger | [SKILL.md](../../../skills/experts/ui-ux-engineer/SKILL.md#L1-L79) |
| `vision-expert` | 83/6,071/8 | N | C | S | yes | Narrow trigger | [SKILL.md](../../../skills/experts/vision-expert/SKILL.md#L1-L83) |
| `wasm-rust-expert` | 91/5,468/6 | N | C | S | yes | Narrow trigger | [SKILL.md](../../../skills/experts/wasm-rust-expert/SKILL.md#L1-L91) |
| `webwork-writer-expert` | 114/5,640/33 | K | B | D | yes | Move delegation; keep required reads | [SKILL.md](../../../skills/experts/webwork-writer-expert/SKILL.md#L1-L114) |
| `delegate-manager-to-subagents` | 68/2,791/4 | K | - | - | yes | Keep | [SKILL.md](../../../skills/management/delegate-manager-to-subagents/SKILL.md#L1-L68) |
| `gas-town-workflow` | 213/9,141/2 | K | C | - | yes | Keep role-specific workflow | [SKILL.md](../../../skills/management/gas-town-workflow/SKILL.md#L1-L213) |
| `hang-check` | 91/4,031/0 | K | - | - | yes | Keep evidence-based stall rule | [SKILL.md](../../../skills/management/hang-check/SKILL.md#L1-L91) |
| `html-game-parallel-builder` | 276/12,882/11 | N | B | C | yes | Narrow trigger | [SKILL.md](../../../skills/management/html-game-parallel-builder/SKILL.md#L1-L276) |
| `parallel-plan` | 187/10,296/1 | K | C | I,C | partial | Move live agent catalog | [SKILL.md](../../../skills/management/parallel-plan/SKILL.md#L1-L187) |
| `stay-busy` | 281/11,882/26 | K | C | I | yes | Narrow repeated finish-obvious text | [SKILL.md](../../../skills/management/stay-busy/SKILL.md#L1-L281) |
| `repo-rules-reader` | 27/1,031/0 | N | B | - | no | Narrow trigger; define completion | [SKILL.md](../../../skills/orientation/repo-rules-reader/SKILL.md#L1-L27) |
| `blueprint-plan-drafter` | 162/8,656/6 | K | B | - | yes | Move fixed reads behind contextual routes | [SKILL.md](../../../skills/planning/blueprint-plan-drafter/SKILL.md#L1-L162) |
| `ideonomy-plain` | 135/10,761/0 | K | C | I | no | Narrow completion and guardrails | [SKILL.md](../../../skills/planning/ideonomy-plain/SKILL.md#L1-L135) |
| `ideonomy-rich` | 221/13,673/0 | K | C | I | yes | Narrow repeated guardrails | [SKILL.md](../../../skills/planning/ideonomy-rich/SKILL.md#L1-L221) |
| `distill-plan-goal` | 83/4,419/2 | K | C | - | yes | Rename public identity to `make-goal` | [SKILL.md](../../../skills/planning/make-goal/SKILL.md#L1-L83) |
| `audit-code-reviewer` | 190/9,274/0 | K | B | I | yes | Automate or route repeated style checks | [SKILL.md](../../../skills/quality/audit-code-reviewer/SKILL.md#L1-L190) |
| `unit-test-starter` | 166/7,902/0 | K | B | D,I | yes | Automate style rules; move delegation | [SKILL.md](../../../skills/quality/unit-test-starter/SKILL.md#L1-L166) |
| `old-python-code-review` (deprecated) | 57/3,123/0 | legacy | B | I | yes | Automate repeated style rules | [SKILL.md](../../../skills/quality/old-python-code-review/SKILL.md#L1-L57) |

## High-impact findings

### Excessive mandatory context

**Fact.** `repo-rules-reader` fires before coding/review/delegation and mandates `AGENTS.md`, every
`docs/*_STYLE.md`, and the latest changelog
([SKILL.md](../../../skills/orientation/repo-rules-reader/SKILL.md#L3-L23)). Reproducible measurement
`wc -l AGENTS.md docs/*_STYLE.md` is 3,724 lines; the current latest block is 69 more
([docs/CHANGELOG.md](../../CHANGELOG.md#L1-L69)), for 3,793 loaded lines.
`blueprint-plan-drafter` front-loads five repo guides, six fixed references, and two conditional inputs
([SKILL.md](../../../skills/planning/blueprint-plan-drafter/SKILL.md#L68-L81)).

**Fact.** WebWork requires three documents totaling 1,620 lines because of renderer-lint failures
([SKILL.md](../../../skills/experts/webwork-writer-expert/SKILL.md#L12-L29)); Bptools requires its
guide plus live `bptools.py` because framework signatures drift
([SKILL.md](../../../skills/experts/bptools-writer-expert/SKILL.md#L13-L34)).

**Interpretation.** The general loads should become contextual. The two writer safeguards are
correctness controls for silent domain failures and should remain.

### Duplication and consumer drift

**Fact.** `Delegated execution` appears in 15 skills, not 18; ten use the same near-verbatim paragraph
([SKILL.md](../../../skills/documentation/arch-docs/SKILL.md#L105-L111),
[SKILL.md](../../../skills/documentation/news-release-docs/SKILL.md#L96-L102),
[SKILL.md](../../../skills/experts/webwork-writer-expert/SKILL.md#L108-L114)). Its owner defines
manager responsibility and completion
([SKILL.md](../../../skills/management/delegate-manager-to-subagents/SKILL.md#L8-L68)).

**Fact.** Within-file repeats include README's opening cap
([SKILL.md](../../../skills/documentation/readme-docs/SKILL.md#L60-L68),
[SKILL.md](../../../skills/documentation/readme-docs/SKILL.md#L145-L151)), AGENTS bare paths
([SKILL.md](../../../skills/documentation/agents-md-fixer/SKILL.md#L92-L120)), docset dispatch
([SKILL.md](../../../skills/documentation/docset-updater/SKILL.md#L32-L57),
[SKILL.md](../../../skills/documentation/docset-updater/SKILL.md#L68-L94)), and test fragility
([SKILL.md](../../../skills/quality/unit-test-starter/SKILL.md#L10-L35),
[SKILL.md](../../../skills/quality/unit-test-starter/SKILL.md#L152-L158)).

**Fact.** `parallel-plan` embeds 14 roles despite directing catalog inspection
([SKILL.md](../../../skills/management/parallel-plan/SKILL.md#L55-L78)); TypeScript embeds four shell
commands and a fixed `tsc` fallback
([SKILL.md](../../../skills/experts/typescript-engineer/SKILL.md#L45-L49),
[SKILL.md](../../../skills/experts/typescript-engineer/SKILL.md#L238-L242)).

**Recommendation.** Move generic delegation and live consumer data to their owners. Keep one local
statement of each rule and retain domain-specific return contracts.

### Claims disproved by evidence

**Fact.** The suspect large references are routed, so removing them would change live paths. Solid
routes all large framework guides
([SKILL.md](../../../skills/experts/solid-js-expert/SKILL.md#L82-L108)); TypeScript routes both
`game-type-patterns.md` and `divergence-map.md`
([SKILL.md](../../../skills/experts/typescript-engineer/SKILL.md#L93-L101),
[SKILL.md](../../../skills/experts/typescript-engineer/SKILL.md#L181-L211)); Glass routes
`skill_maintenance.md`
([SKILL.md](../../../skills/experts/glass-expert/SKILL.md#L58-L70)); and the Bptools indexes route
both named plan files
([topic_index.md](../../../skills/experts/bptools-writer-expert/references/topic_index.md#L14-L22),
[topic_index.md](../../../skills/experts/bptools-writer-expert/references/topic_index.md#L52-L56)).

**Fact.** `skills/planning/make-goal/` disagrees with `name: distill-plan-goal`
([SKILL.md](../../../skills/planning/make-goal/SKILL.md#L1-L3)). The existing test explicitly
requires equality
([tests/test_skill_frontmatter.py](../../../tests/test_skill_frontmatter.py#L70-L83)); a current
focused run fails on this mismatch. The preliminary assumption that it passed is false.

**Recommendation.** Keep the existing `make-goal` directory and rename the frontmatter/public skill
identity to `make-goal`. Update callers and generated metadata in the same follow-up work package.

**Fact.** Expert guidance prescribes a five-section, roughly 70-100-line entrypoint
([docs/EXPERT_SKILL-BEST_PRACTICES.md](../../EXPERT_SKILL-BEST_PRACTICES.md#L130-L143)), but the
parity gate enforces only a `project_workflow.md` route, not those headings
([tests/test_expert_skill_parity.py](../../../tests/test_expert_skill_parity.py#L270-L277)). Twelve
of 17 experts currently carry both `Quality bar` and `Output expectations` headings. Against the
proposed paired ceiling, 15 of 40 live entrypoints exceed 150 physical lines, 15 exceed 8,000
characters, and 17 violate at least one limit. `ideonomy-plain` and `solid-js-expert` fail only the
character limit, while `agents-md-fixer` and `unit-test-starter` fail only the line limit
([SKILL.md](../../../skills/planning/ideonomy-plain/SKILL.md#L1-L135),
[SKILL.md](../../../skills/experts/solid-js-expert/SKILL.md#L1-L126),
[SKILL.md](../../../skills/documentation/agents-md-fixer/SKILL.md#L1-L165),
[SKILL.md](../../../skills/quality/unit-test-starter/SKILL.md#L1-L166)).

**Fact.** Meeting the paired ceiling requires moving at least 1,023 lines and 48,926 characters out
of the 17 over-budget entrypoints; the per-file measurements above are the reproducible inventory.

**Fact.** `tests/test_skill_body_size.py` already discovers live entrypoints through shared
discovery, but it only warns beyond 300 lines or 24,000 characters
([tests/test_skill_body_size.py](../../../tests/test_skill_body_size.py#L1-L43)). Current maxima are
281 lines and 14,638 characters in different entrypoints, so the test passes without warning
([SKILL.md](../../../skills/management/stay-busy/SKILL.md#L1-L281),
[SKILL.md](../../../skills/experts/typescript-engineer/SKILL.md#L1-L250)).

**Recommendation (user-directed).** Adopt inclusive 150-line and 8,000-character caps for each live
`SKILL.md`, including frontmatter and newlines; paired limits prevent long-line evasion. Exclude
references because they load contextually. Preserve the keep list while fixing all 17 violations,
then make `tests/test_skill_body_size.py` fail with both measurements. A failure means move
conditional detail to routed references; if that loses required behavior, revise the authority
before adding an exception. Land the gate only when green, and prioritize trigger correctness over
budget conformance.

### Authoring authority needs refinement

**Fact.** Expert guidance currently calls the description "keyword-packed," tells authors to list
domain vocabulary, and says to add synonyms until an underspecified request hits
([docs/EXPERT_SKILL-BEST_PRACTICES.md](../../EXPERT_SKILL-BEST_PRACTICES.md#L135-L157)). It also
prescribes five body sections and only a rough line target
([docs/EXPERT_SKILL-BEST_PRACTICES.md](../../EXPERT_SKILL-BEST_PRACTICES.md#L130-L143)).
**Interpretation.** This advice aligns with the measured domain-wide descriptions and repetition.

**Recommendation.** Put the universal 150-line/8,000-character `SKILL.md` caps in
`docs/REPO_STYLE.md` and make `tests/test_skill_body_size.py` their executable check. Retain 70-100
lines in `docs/EXPERT_SKILL-BEST_PRACTICES.md` as an expert design target, point to the universal
ceiling, select for specialized judgment rather than keyword breadth, require routed Workflow and
D4 completion, and make other headings conditional on distinct behavior. Keep reference size
advisory; route quality and one-concern ownership matter more than unloaded character count.

**Fact (reproduced runtime evidence, 2026-09-12).** The changelog records a former whole-tree
ideonomy ASCII exception
([docs/CHANGELOG-2026-08a.md](../../CHANGELOG-2026-08a.md#L93-L100)); current `tests/conftest.py` has
no exclusion ([tests/conftest.py](../../../tests/conftest.py#L41-L52)). The exposed full gate reports
`10 failed, 690 passed`: `negation-cascade.md` (5), rich `SKILL.md` (508), and rich `rendering/`
README (19), atlas (402), chart (291), cycle (55), dictionary (921), list (28), scale (117), and tree
(105). This is runtime evidence from `pytest tests/test_ascii_compliance.py`.

**Interpretation.** The former whole-tree exception created a false-green gate. The rich rendering
guides use glyphs as functional vocabulary, but that does not justify Unicode in an entrypoint.

**Recommendation (user-directed scope extension).** Require every file named `SKILL.md` to be ASCII,
including deprecated and archived copies. Move rich glyph examples from the entrypoint and make
style-only tables ASCII. Because the test is vendored, list only exact, justified UTF-8 reference
paths in repo-local `REPO_HYGIENE_FILTERS["ascii_compliance"]`
([tests/conftest.py](../../../tests/conftest.py#L22-L39)); use no wildcard or `SKILL.md` entry. Verify
the gate collects every `SKILL.md` and passes.

## Hypothesis results

| Hypothesis | Verdict and decision |
| --- | --- |
| H1 | **Confirmed by the [trigger matrix](#trigger-behavior).** Thirteen expert and three other descriptions over-trigger; narrowed text preserves tested positives and removes neighboring hits. |
| H2 | **Confirmed, corrected scope.** Fifteen instances are evidenced by representative duplicates and the [owner](../../../skills/management/delegate-manager-to-subagents/SKILL.md#L8-L68); keep domain return contracts. |
| H3 | **Weakened.** Guidance requires five sections ([source](../../EXPERT_SKILL-BEST_PRACTICES.md#L130-L143)), but parity checks only routing ([gate](../../../tests/test_expert_skill_parity.py#L270-L277)); pilot before removal. |
| H4 | **Weakened.** False-hit cases and the 3,793-line cost are confirmed, but zero behavior loss is not; pilot the narrowed trigger before adoption. |
| H5 | **Rejected.** Named references are actively routed by [Solid](../../../skills/experts/solid-js-expert/SKILL.md#L82-L108) and the other linked sources above. |
| H6 | **Confirmed.** Required reads prevent recorded failures ([docs/CHANGELOG-2026-06a.md](../../CHANGELOG-2026-06a.md#L925-L934)); keep short positive prerequisites with same-session reuse. |

## Ranked fixes

This ranking is a **Recommendation**. Likely needless-load frequency comes first, then context,
contradiction severity, and repair ease; deltas estimate entrypoint lines. Evidence is linked above.

1. `repo-rules-reader` - **Narrow** trigger behind a pilot. Delta 0; a false hit loads 3,793 lines.
2. `pdf-guide` - **Narrow** to visual PDF correctness. Delta 0; ordinary reading is frequent.
3. `css-creative-expert` - **Narrow** to CSS-specific design/diagnosis. Delta 0.
4. `typescript-engineer` - **Narrow** to type design/compiler diagnosis. Delta 0.
5. `ui-ux-engineer` - **Narrow** to requested product-level UX judgment. Delta 0.
6. `html-game-parallel-builder` - **Narrow** to requested parallel builds or major workstreams.
   Delta 0; avoids its 276-line entrypoint on a small fix.
7. `solid-js-expert` - **Narrow** to Solid-specific semantics. Delta 0; keep routed references.
8. `rust-code-expert` - **Narrow** to Rust-specific design/diagnosis. Delta 0.
9. `postgresql-expert` - **Narrow** to PostgreSQL-specific design/diagnosis. Delta 0.
10. ASCII entrypoints - **Move** rich glyph examples out of `SKILL.md`; keep exact justified
    reference exclusions in `conftest.py`. Expected delta: about -40 to -70 entrypoint lines.
11. `distill-plan-goal` - **Keep** its directory/body and correct the public identity to `make-goal`.
    Delta 0; the existing failing gate supplies the correction path.
12. Corpus entrypoint budget - **Automate** inclusive 150-line and 8,000-character maxima for live
    `SKILL.md` files after the 17 repairs. Expected aggregate delta: at least -1,023 lines; references
    are exempt.

## Keep list

Each item is a **Recommendation** to retain a rule that prevents a named failure.

| Keep | Failure prevented |
| --- | --- |
| [WebWork proof](../../../skills/experts/webwork-writer-expert/SKILL.md#L43-L54) | Blank, misgraded, or renderer-invalid PGML. |
| [Bptools live API read](../../../skills/experts/bptools-writer-expert/SKILL.md#L19-L29) | Drifted signatures and anti-cheat flags. |
| [Glass visual evidence](../../../skills/experts/glass-expert/SKILL.md#L10-L17) | Compile-only claims about sampling or legibility. |
| [Color re-audit](../../../skills/experts/color-accessibility-expert/SKILL.md#L70-L78) | Reporting a replacement before actual colors pass. |
| [Fresh reviewer](../../REPO_STYLE.md#L23-L30) | Stale context weakening independent judgment. |
| [Expert parity](../../../tests/test_expert_skill_parity.py#L16-L44) | Incomplete packages and unresolved routes. |
| [ASCII policy](../../MARKDOWN_STYLE.md#L15-L18) | Source incompatible with target tools and channels. |

## Follow-up plan outline

The following is a **Recommendation** for a separate plan, with one fresh owner per work package.

| # | Atomic work package |
| ---: | --- |
| 1 | Update `docs/REPO_STYLE.md` with the universal budget. Refine expert guidance for judgment-specific triggers, routing, D4, and optional sections; change parity only for pilot-proven behavior. |
| 2 | Narrow documentation/orientation triggers: `pdf-guide`, `repo-rules-reader`. |
| 3 | Narrow interface triggers: CSS, Solid, TypeScript, UI/UX, parallel game builder. |
| 4 | Narrow systems triggers: Podman, PostgreSQL, Rust, Wasm. |
| 5 | Narrow scientific/desktop triggers: geometry, Glass, HCI, PySide6, vision. |
| 6 | Consolidate generic delegation and repetition; move consumer catalogs such as `parallel-plan` roles to discovery; preserve domain contracts. |
| 7 | Rename the public/frontmatter identity to `make-goal`, keep its directory, update callers, and verify frontmatter. |
| 8 | Make every `SKILL.md` and style-only table ASCII; put exact justified UTF-8 reference paths only in `conftest.py`. |
| 9 | Reduce live entrypoints to at most 150 lines/8,000 characters; then harden `test_skill_body_size.py` using shared discovery and both measured counts. |
| 10 | Regenerate plugin manifests and `docs/SKILLS_INDEX.md` after identity/path edits. |
| 11 | Run the four-case pilot three times before/after: typo, bounded bug, ambiguity, permission boundary; report majority and dissent. |
| 12 | Run focused frontmatter, size, Codex YAML, link, prefix, discovery, index, manifest, ASCII, whitespace, and parity gates. |

## Housekeeping

**Fact.** `ChatGPT_External_Plan_Reviewer_Guidance.md` is an untracked root Markdown file. Repo style
places durable Markdown documentation under `docs/` with SCREAMING_SNAKE_CASE names
([docs/REPO_STYLE.md](../../REPO_STYLE.md#L283-L295)).

**Recommendation.** Give it the tracked canonical home `docs/EXTERNAL_PLAN_REVIEWER_GUIDANCE.md` in
the follow-up and update consumers. This audit changes no skill.
