# README landing-page practices

## Contents

- [Purpose](#purpose)
- [First-screen test](#first-screen-test)
- [Content hierarchy](#content-hierarchy)
- [Project-type emphasis](#project-type-emphasis)
- [Quick-start quality](#quick-start-quality)
- [Examples and visuals](#examples-and-visuals)
- [Distinctive project identity](#distinctive-project-identity)
- [README versus deeper docs](#readme-versus-deeper-docs)
- [Evidence and maintenance](#evidence-and-maintenance)
- [Source notes](#source-notes)

## Purpose

A repository README is usually the project's front door. Write it for someone arriving
with only the context visible on the project page.

The opening should establish three facts quickly:

- What the project does.
- Why it is useful and who benefits from it.
- How to get a meaningful first result.

Installation and usage instructions, examples, proof, and project status form a
credible landing page when they apply. Detailed docs can live elsewhere, but the README
must provide enough context for readers to understand and evaluate those links. Add
concise help or license routes when they materially serve the intended audience.

## First-screen test

Before scrolling far, a visitor should see:

- The project name and a plain-language value proposition.
- The intended audience or problem being solved.
- The strongest available proof: a live demo, screenshot, output sample, or compact
  example.
- A clear next action such as trying the demo or following the quick start.

The opening paragraph is also the source for GitHub's About description in this repo
family. Keep it at 250 Python characters or fewer. Use only plain prose, reserve the
repository name for the H1, and place rich Markdown and URLs after it. Aim for: what it
is + who or use case + main benefit + one distinguishing detail.

Place badges after the opening as supporting metadata. Select badges that convey useful,
current facts such as build status, package version, supported platform, or license.

## Content hierarchy

Use this default order, then adapt it to the project:

1. Identity and value proposition.
2. Visual proof, live demo, or representative example.
3. Reasons to use the project: capabilities, use cases, or differentiators.
4. Quick start: prerequisites, installation, first meaningful run, expected result.
5. Basic usage and a route to advanced documentation.
6. Status and limitations that affect adoption.
7. Concise help, maintenance, contribution, license, or acknowledgment routes when they
   materially serve the audience.

Predictable headings reduce hunting. Prefer familiar labels such as `Quick start`,
`Installation`, `Usage`, `Examples`, and `Documentation` for core reader tasks. Use a
domain-specific heading when it is clearer, and familiar concise labels for optional
closing routes.

Put `Quick start` after the reader understands what the project is good for. For an
unfamiliar or visual project,
motivation, a live demo, an example, `What it produces`, or `Why this project` often
belongs first. For a narrowly scoped developer utility whose value is obvious from a
small code example, the example itself can provide that context before installation.

## Project-type emphasis

| Project type | Show early | First success |
| --- | --- | --- |
| CLI | Example command and output | Run one useful command |
| Library | Small import or API example | Produce a real return value |
| Web app or game | Live demo and screenshot | Open or run the experience |
| Desktop app | Screenshot and supported platforms | Launch and complete one task |
| Service or API | Request and response example | Start locally and make one request |
| Dataset or research repo | Scope, provenance, and sample | Inspect or reproduce one result |
| Developer tooling | Problem solved and integration point | Run the tool on a small target |

## Quick-start quality

A good quick start is a short success path that continues beyond installation.

- Name prerequisites before commands that depend on them.
- Prefer commands readers can copy and paste.
- Use the repository's canonical entry point.
- Demonstrate implemented functionality with the smallest realistic input.
- Show or describe expected output whenever it clarifies success.
- Link to detailed alternatives after the primary path works.

If the full setup is necessarily complex, explain the shape of the process, point to the
complete install guide, and continue to a small demonstration of project value.

## Examples and visuals

Examples answer "what will this do for me?" more convincingly than feature labels.
Choose one example that represents the project's main value. Explain enough input and
output context for a newcomer to understand it.

Use screenshots for visual products and output artifacts for tools that create visual
results. Pair visuals with text so the page remains accessible and understandable from
prose alone. Keep screenshots current through the `screenshot-docs` managed
block.

Use a short animated GIF when motion is the evidence: a drag-and-drop interaction, a
state transition, a compact command workflow, or a before-and-after transformation.
Prefer a static image for layout, fine detail, text-heavy output, or any state a reader
benefits from studying. Keep animation focused on one task and accompany it with a
written explanation of the same action and result.

## Distinctive project identity

A polished README should feel authored for its project. Identify the signature promise,
pair it with the strongest evidence, and use project-specific headings, examples,
captions, and voice. A reusable template supplies coverage; the repository supplies the
story.

Read [landing_page_ideas.md](landing_page_ideas.md) for proof-artifact options, an
ambition-to-evidence ladder, and a dispatchable task format for improvements that need a
separate owner.

## README versus deeper docs

Keep in the README:

- Project identity, audience, motivation, and value.
- The primary onboarding path.
- One or more representative examples.
- Essential constraints that affect adoption.
- A curated map of deeper documentation.
- Concise help and license routes when they materially serve the audience.

Move to deeper docs:

- Exhaustive installation variants.
- Complete CLI or API reference material.
- Long configuration catalogs.
- Full architecture and file-by-file explanations.
- Large troubleshooting inventories.

The distinction is summary versus depth, not useful versus unnecessary. A README that
only links outward forces newcomers to reconstruct the project before they understand
why they should care.

## Evidence and maintenance

- Verify commands against executable scripts, manifests, or automated workflows.
- Verify claims against current behavior and supported platforms.
- Link repository files with relative URLs so links work in clones and across branches.
- When the README names a license, use an explicit repository declaration and link the
  applicable file.
- Preserve useful existing prose and examples that remain current and well placed.
- Publish sections with substantive, evidenced content and remove empty placeholders.

## Source notes

This guide locally distills the following external guidance so the skill can apply it
without reopening the web on every run:

- [GitHub Docs: About the repository README file](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
  identifies the README as an early visitor touchpoint and recommends explaining what
  the project does, why it is useful, how to start, where to get help, and who maintains
  it. It also documents relative links and GitHub's generated heading outline.
- [Standard Readme](https://github.com/RichardLitt/standard-readme) treats the README as
  the normal entry point to code and emphasizes why to use the project, installation,
  usage, predictable sections, maintainers, and licensing.
- [READMINE](https://mhucka.github.io/readmine/) recommends a plain-language
  introduction for readers unfamiliar with the domain, explicit prerequisites,
  copy-pasteable installation, a smallest working quick start, representative usage,
  help, limitations, and licensing.
- [GitHub Docs: Best practices for repositories](https://docs.github.com/en/repositories/creating-and-managing-repositories/best-practices-for-repositories)
  recommends a README for every repository so people can understand and navigate the
  work.
- [Readme Best Practices](https://github.com/jehna/readme-best-practices) demonstrates
  a reusable scaffold with installation, development, features, configuration, links,
  and licensing, led by a short animated walkthrough that shows the promised workflow.
- [freeCodeCamp: How to Write a Good README File](https://www.freecodecamp.org/news/how-to-write-a-good-readme-file/)
  frames the page around what, why, and how; it adds motivation, the problem solved,
  differentiators, installation, usage examples, and visual aids.
- [Shaun Codes: README Rules](https://medium.com/@fulton_shaun/readme-rules-structure-style-and-pro-tips-faea5eb5d252)
  reinforces a clear overview, demo, installation, usage, features, license, consistent
  headings, visual rhythm, and removal of stale instructions.
- [DEV Community: How to Write a Great README](https://dev.to/eva_clari_289d85ecc68da48/how-to-write-a-great-readme-for-your-github-project-555p)
  highlights screenshots for interface states, short GIFs for workflows, help and
  troubleshooting routes, beginner-friendly language, and continuous maintenance.
- [Sidra Gillani: Best Practices for Writing README Files](https://medium.com/@sidragillani/best-practices-for-writing-readme-files-for-github-projects-fe89f76d0e02)
  treats the README as a project homepage and reinforces features, installation, usage,
  technologies, contribution routes, licensing, screenshots, GIFs, and current content.
- [Markdown Visualizer: How to Write a Perfect GitHub README](https://markdownvisualizer.com/blog/write-github-readme)
  provides a broad section checklist and emphasizes descriptive alt text, key workflow
  screenshots, API examples when applicable, license links, and acknowledgments.

These are design inputs, not rigid specifications. Repository evidence, audience, and
local rules decide the final section set and order.
