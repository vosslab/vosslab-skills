---
name: readme-docs
description: "Create or refresh `README.md` as a distinctive, welcoming, evidence-backed GitHub landing page for people unfamiliar with the project. Use when a README is missing, thin, overly stripped down, generic, stale, or hard to navigate; explain what the project does, why it is useful, who it serves, and how to get a meaningful first result, then provide project-specific proof, examples, and documentation routes. This skill owns `README.md` and routes deeper-doc or visual-asset work to the appropriate skill."
---

# README landing page

## Goal

Make `README.md` a useful front door for a first-time visitor. Explain what the
project does, why it matters, and how to try it. Give readers enough context and
proof to decide whether the project fits their needs, then route them to deeper
documentation.

Optimize for comprehension, successful onboarding, and a memorable project identity.
Give newcomers enough context, evidence, and guidance to understand the work before the
documentation links.

This skill is the sole owner of `README.md`. Other docs skills own their files under
`docs/`; this skill summarizes the most important user-facing information and links
to those authoritative details.

## Resource routing

The workflow below contains the required process. Load a supporting resource when its
decision applies:

- Use [assets/README_TEMPLATE.md](assets/README_TEMPLATE.md) when the README is
  missing, very thin, or needs a structural rewrite.
- Read [references/readme_best_practices.md](references/readme_best_practices.md) when
  choosing among unfamiliar project types or resolving a structure or content question.
- Read [references/landing_page_ideas.md](references/landing_page_ideas.md) when the
  page needs a stronger signature promise, proof artifact, or project-specific treatment.
- Apply [references/review_checklist.md](references/review_checklist.md) for a broad
  refresh or a final landing-page audit.
- Apply [references/scoring_rubric.md](references/scoring_rubric.md) for a broad refresh,
  an explicit scoring request, or a before-and-after quality comparison.

Adapt the template to repository evidence and resolve every placeholder before delivery.

## Landing-page standard

Answer these questions in the order a newcomer is likely to ask them:

1. What is this project?
2. Who is it for, and what problem does it solve?
3. Why would someone choose or use it?
4. What does it look like or produce?
5. How can someone get a meaningful first result?
6. Where can they learn more?

Establish purpose, audience, usefulness, and the strongest available proof before
`Quick start`. Depending on the project, lead into setup with a live demo, example,
screenshot, `Why this project`, `What it produces`, or `Key features` section.

Use the repository's actual audience and project type to choose sections. A CLI,
library, desktop app, browser experience, dataset, and internal developer tool need
different proof and onboarding paths.

## Core content

Include each item when repository evidence supports it:

- Project title and a plain-prose opening paragraph of at most 250 characters. Treat it
  as the source for GitHub's About description: state purpose, audience or use case,
  main benefit, and one distinguishing detail when space allows. Reserve the repo name
  for the H1 and use only plain prose in this paragraph. Place links, images, badges,
  code spans, HTML, raw URLs, and setup details after it.
- Audience or use-case context that explains why the project is useful.
- Key capabilities, benefits, or differentiators; prefer three to six concrete items.
- A verified quick start that reaches a real result after installation.
- One representative usage example and, when useful, expected output or behavior.
- A curated documentation map with one-line descriptions.

Also add high-value content when applicable:

- A live demo, screenshot, output sample, or small architecture visual.
- Prerequisites and compatibility constraints needed before the quick start.
- Project status, important limitations, and supported platforms.
- Concise closing routes for help, licensing, citation, or acknowledgments when the
  audience and repository evidence make them useful.
- A short contributor path when the project actively accepts contributions and repo
  policy supports it.

Treat examples, visuals, and status as core landing-page content when they help a
newcomer evaluate or use the project. Keep optional closing routes proportional to the
audience's needs.

## Make it distinctive

Dream big and build on the ambition already present in the repository. Find the
project-specific idea that deserves to lead the page: a striking output, a live
experience, a compact transformation, a teaching purpose, an unusual workflow, a
technical achievement, or a clear philosophy.

Use the template as a scaffold, then replace its generic shape with the project's own
story, terminology, evidence, and visual rhythm. Aim for a page that could only belong
to this project.

Make the ambition practical:

- Name the signature promise in one sentence.
- Choose the strongest proof artifact: live demo, GIF, screenshot, output sample,
  before-and-after example, benchmark, architecture visual, or worked scenario.
- Give the proof a descriptive project-specific heading and a short interpretation.
- Complete high-impact improvements that fit the current task and repository evidence.
- Turn remaining opportunities into dispatchable next steps with an owner, target
  files, required evidence, success criteria, and verification method.

The landing-page ideas resource provides an idea menu and completion-brief format when
the page needs a more distinctive treatment.

## Workflow

### 1. Read rules and evidence

- Read `AGENTS.md`, `docs/REPO_STYLE.md`, and `docs/MARKDOWN_STYLE.md` when present.
- Read the current `README.md` and evaluate both its content and structure from current
  repository evidence.
- For broad refreshes and scoring requests, score the current README with the routed
  rubric; record category evidence, open quality gates, and the two highest-value
  improvements.
- Inventory `docs/`, `LICENSE*`, package manifests, executable front doors, examples,
  tests, screenshots, releases, deployment workflows, and repository metadata.
- Derive the project name, audience, primary value, project type, install path, usage
  path, and status from evidence. Identify support and license evidence when the README
  would benefit from concise closing routes.
- Preserve strong existing explanations, examples, acknowledgments, and visuals that
  remain current, unique, and supported.

### 2. Design the newcomer journey

- Choose the primary audience and the smallest useful success they can achieve.
- Put identity, value, and the strongest proof near the top: a live demo for a browser
  app, a screenshot for a GUI, an output sample for a CLI, or a short code example for
  a library.
- Place `Quick start` after enough context for the reader to understand what the
  commands accomplish and why the result matters.
- Define the signature promise and select one distinctive treatment grounded in
  repository evidence. Use the routed landing-page ideas resource when the strongest
  treatment is unclear.
- Select the template sections that answer real newcomer questions. Reorder them when
  the project type calls for a different journey.

### 3. Write the opening

- Start with the project name.
- Follow with a plain-prose opening paragraph no longer than 250 characters. Explain
  what it does, who it helps, and why it is useful in audience language. Reserve the
  repo name for the H1. Place links, images, badges, code spans, HTML, raw URLs, setup
  details, internal names, and expanded terminology after this paragraph.
- Add a verified live link, a small set of meaningful badges, or visible proof that
  materially helps evaluation.
- Lead with project purpose and value; place repository maintenance, file inventories,
  and setup after readers understand the project.

### 4. Build a complete getting-started path

- State only prerequisites that affect the primary path.
- Give copy-pasteable install and run commands that are confirmed in repository files.
- Demonstrate actual functionality after installation.
- Show the expected result whenever it clarifies success.
- Keep advanced variants in `docs/` and make the primary README path self-contained.

### 5. Add orientation and proof

- Summarize key capabilities or use cases in concrete, outcome-oriented language.
- Include one representative example in the README even when `docs/USAGE.md` contains
  the full guide.
- Explain essential concepts, formats, engines, or compatibility constraints before
  they can surprise the reader.
- Use the managed screenshot block when the project has a visual interface, visual
  output, an existing `docs/screenshots/` directory, or the user requests screenshots.

Insert this exact placeholder for `screenshot-docs` to replace:

```markdown
<!-- screenshots:begin (managed by screenshot-docs) -->
<!-- screenshots:end -->
```

`screenshot-docs` owns visual capture, `docs/screenshots/`, embed syntax, alt text, and
content between the sentinels. This skill owns the surrounding README prose and the
sentinel lines. Keep the initial block empty so the capture pass has one canonical
replacement shape.

### 6. Create the documentation map

- Link the core docs produced during a docset refresh by convention:
  `docs/CODE_ARCHITECTURE.md`, `docs/FILE_STRUCTURE.md`, `docs/INSTALL.md`, and
  `docs/USAGE.md`.
- Outside a coordinated docset refresh, link existing files and route substantive doc
  gaps to their owning skill.
- Include conditional docs such as `docs/TROUBLESHOOTING.md` when present and useful.
- Use path text for repo-local documentation links, followed by a one-line description.
- Curate for the audience: list three to eight docs directly; group a medium docset;
  for a large docset, show the core routes and an index.

### 7. Add relevant closing context

- State maturity or known limitations when they affect adoption.
- Add a concise help route when the audience is likely to need one.
- Add a concise `License` section when licensing information helps the intended reader.
  Name and link only legal terms stated by repository evidence.
- Prefer social links over a hard-coded email when repo rules request it.

### 8. Verify the landing page

- For broad refreshes and landing-page audits, apply the routed review checklist. For a
  focused update, use the core checks below.
- Run every quick-start and example command that is safe and practical.
- Check that commands, paths, claims, and live links match repo evidence. When the
  README names a license, verify its name and link against repository evidence.
- Resolve every template placeholder and publish headings, claims, and badges backed by
  repository evidence.
- Read the rendered order as a newcomer: identity and value first, proof and first
  success next, deeper routes and project details after that.
- Run the repository's Markdown link and ASCII checks when available.
- Run `tests/test_readme_first_paragraph.py` when present; it enforces the single H1,
  250-character About-field cap, plain-prose shape, and project-name placement in the H1.
- For broad refreshes and scoring requests, rescore the verified README with the routed
  rubric. Report the before and after totals, gate results, strongest gain, and remaining
  highest-value opportunity.

## Live demo and GitHub Pages

For a browser app, game, or interactive demo, place a confirmed live link near the
opening. Evidence includes a deployment workflow, a configured Pages domain, a known
deploy branch, or a URL supplied by the user. Prefer the configured URL. Construct
`https://<owner>.github.io/<repo>/` only when Pages deployment is confirmed.

## Content boundaries

Summarize instead of duplicating. The README should carry the value proposition,
primary onboarding path, representative example, and navigation context. Put exhaustive
API references, every configuration option, full architecture detail, and long
troubleshooting catalogs in their owned docs.

Let project complexity determine length. Preserve useful landing-page content and retain
current, supported material in the location where newcomers can use it best.

Follow repo documentation policy. Write `README.md`; route deeper-doc gaps to the skill
that owns each file. Keep the README useful with verified repository evidence while
those gaps remain open.

## Quality bar

- A reader unfamiliar with the repository can explain the project after the opening.
- The README communicates usefulness alongside relevant implementation or file-layout
  context.
- The quick start produces a meaningful result through a verified primary path.
- At least one example or visual proves what using the project is like when applicable.
- Installation, usage, proof, and documentation routes are easy to find. Optional
  closing information is concise, accurate, and useful to the intended audience.
- Deeper docs remain discoverable without making the README a bare link directory.
- Existing valuable content remains intact when it is current, supported, and well
  placed.
- The page has at least one unique project-specific element - heading, example, proof
  artifact, visual treatment, or narrative.

## Output

- An updated `README.md` with every template placeholder resolved.
- A short verification report covering commands run, links checked, and the verification
  status of unresolved claims.
- A short list of substantive missing docs for their owning skills.
- Dispatchable landing-page opportunities, each naming an owner, target files, evidence,
  success criteria, and verification method.
- For broad refreshes and scoring requests, an evidence-backed README score before and
  after the edit, including quality-gate results and the strongest category gain.

## Delegated execution

Under `delegate-manager-to-subagents`, assign this skill to a fresh subagent with one
bounded README task, the relevant repo rules, and one verification step. Use a new
subagent for an unrelated follow-up task.
