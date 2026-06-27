# Skills index

Compact index of skills in this repository. Each item links to the skill definition and gives a short purpose summary.

Total skills: 26

- [agents-md-fixer/SKILL.md](../skills/agents-md-fixer/SKILL.md): Trim `AGENTS.md` aggressively to a small pointer file (prefer ~15 lines, hard cap ~50) that points into `docs/*.md` with bare paths instead of restating rules.
- [arch-docs/SKILL.md](../skills/arch-docs/SKILL.md): Create or refresh `docs/CODE_ARCHITECTURE.md` and `docs/FILE_STRUCTURE.md` from current repo evidence.
- [audit-code-reviewer/SKILL.md](../skills/audit-code-reviewer/SKILL.md): Parallel multi-reviewer audit launched before merge or release; not for single-pass review.
- [blueprint-plan-drafter/SKILL.md](../skills/blueprint-plan-drafter/SKILL.md): Create forward-looking implementation plans from scratch for coding teams without writing code.
- [bptools-writer-expert/SKILL.md](../skills/bptools-writer-expert/SKILL.md): Create, edit, and validate biology-problems bptools Python question generators and supporting YAML content.
- [delegate-manager-to-subagents/SKILL.md](../skills/delegate-manager-to-subagents/SKILL.md): Use only when the user has an approved plan AND wants the main agent to manage execution through subagents instead of editing files directly.
- [docset-updater/SKILL.md](../skills/docset-updater/SKILL.md): Refresh the whole repo doc set in one pass by invoking the per-doc skills in dependency order (`arch-docs`, `setup-install-usage-docs`, `readme-docs`, `screenshot-docs`, `agents-md-fixer`), then audit any remaining `docs/` files those skills do not own.
- [gas-town-workflow/SKILL.md](../skills/gas-town-workflow/SKILL.md): Gas Town style multi-agent coordination with role-mapped task routing and convoy-based work decomposition.
- [geometry-expert/SKILL.md](../skills/geometry-expert/SKILL.md): Design, implement, debug, and review computational geometry algorithms in any language, including convex hull, polygon triangulation, Delaunay triangulation, Voronoi diagrams, polygon boolean clipping and overlay, segment intersection and sweep line, proximity and nearest-neighbor queries, point location, spatial data structures (k-d tree, BVH, R-tree, quadtree), arrangements, mesh processing, and distance/intersection queries in 2D, 3D, and nD.
- [html-game-parallel-builder/SKILL.md](../skills/html-game-parallel-builder/SKILL.md): Use when building a TypeScript browser game from modular `src/*.ts` files with parallel subagents to reduce wall-clock time.
- [old-python-code-review/SKILL.md](../skills/old-python-code-review/SKILL.md): Single-pass Python correctness, security, and style review on demand; not for multi-reviewer audits before merge (use audit-code-reviewer for that).
- [parallel-plan/SKILL.md](../skills/parallel-plan/SKILL.md): In-flight nudge to split current work into independent tracks for parallel subagent dispatch; does not create new plans (use blueprint-plan-drafter for that).
- [pdf-guide/SKILL.md](../skills/pdf-guide/SKILL.md): Use when tasks involve reading, creating, or reviewing PDF files where rendering and layout matter; prefer visual checks by rendering pages (Poppler) and use Python tools such as `reportlab`, `pdfplumber`, and `pypdf` for generation and extraction.
- [pyside6-engineer/SKILL.md](../skills/pyside6-engineer/SKILL.md): Design, implement, refactor, and review PySide6 desktop applications with strong widget architecture, signal-slot design, and state flow.
- [readme-docs/SKILL.md](../skills/readme-docs/SKILL.md): Standardize `README.md` to match repo conventions: brief purpose, quick start, links to `docs/`, and a screenshots placeholder for the screenshot-docs skill.
- [repo-rules-reader/SKILL.md](../skills/repo-rules-reader/SKILL.md): Read specified repo rule files (AGENTS.md, docs/REPO_STYLE.md, docs/PYTHON_STYLE.md,.
- [screenshot-docs/SKILL.md](../skills/screenshot-docs/SKILL.md): Capture screenshots of a running app and embed them into README.md and docs/ to make GitHub landing pages novice-friendly.
- [setup-install-usage-docs/SKILL.md](../skills/setup-install-usage-docs/SKILL.md): Create or refresh minimal `docs/INSTALL.md` and `docs/USAGE.md` stubs from repo evidence.
- [skill-writing-guide/SKILL.md](../skills/skill-writing-guide/SKILL.md): Guide for authoring Agent Skills (SKILL.md).
- [solid-js-expert/SKILL.md](../skills/solid-js-expert/SKILL.md): Design, build, debug, and review SolidJS applications and their full stack -- core reactivity (`createSignal`, `createMemo`, `createEffect`, `createResource`), stores, control-flow components (`<For>`, `<Show>`, `<Switch>`), Solid Router, SolidStart, and Solid Meta.
- [stay-busy/SKILL.md](../skills/stay-busy/SKILL.md): Use when the user invokes /stay-busy, asks to keep a manager/orchestrator/subagents busy, complains that an agent is waiting too much, or when an active delegate-manager-to-subagents workflow is about to idle despite safe evidence-producing follow-on work.
- [typescript-engineer/SKILL.md](../skills/typescript-engineer/SKILL.md): Resolve TypeScript errors, eliminate `any`, and design modular, strict TypeScript types including generics, conditional types, mapped types, template literal types, branded or opaque types, and deep inference.
- [ui-ux-engineer/SKILL.md](../skills/ui-ux-engineer/SKILL.md): Review, improve, and engineer UI/UX quality in any framework.
- [unit-test-starter/SKILL.md](../skills/unit-test-starter/SKILL.md): Generate thorough Python 3 pytest unit tests across a repo by scanning Python files.
- [vision-expert/SKILL.md](../skills/vision-expert/SKILL.md): Design, implement, debug, and review computer vision systems in Python, including image processing, detection, segmentation, classification, tracking, OCR, camera pipelines, and dataset-driven evaluation.
- [webwork-writer-expert/SKILL.md](../skills/webwork-writer-expert/SKILL.md): Create, edit, and lint WeBWorK PG/PGML questions following docs/webwork guidance, HTML whitelist constraints, and renderer-based lint checks.
