# README review checklist

Use this checklist after drafting and before final verification. It distills repeated
strengths and failure patterns observed across a mixed local corpus of CLI tools,
libraries, desktop apps, browser games, research software, educational projects, and
multi-package repositories.

## Opening

- Does the first paragraph say what the project does, who it serves, and why it is
  useful?
- Is the opening plain prose of at most 250 characters, with the repo name reserved for
  the H1 and rich Markdown placed afterward?
- Can a reader understand the page from the context it provides?
- Is an adoption-blocking status such as experimental, archived, deprecated, or known
  not to work visible before setup instructions?
- For a multi-product repository, does the opening distinguish each product and explain
  when to use it?

## Proof and motivation

- Does an app or game offer a verified live link when one exists?
- Does a visual product show its interface or output near the top?
- Does an output-producing tool explain or show what it creates?
- Are capabilities framed as user outcomes rather than internal modules?
- Would a short GIF explain a key interaction better than multiple static images?
- Does the page contain a signature promise and proof that feel specific to this
  project?

## First success

- Does `Quick start` reach a useful outcome after installation?
- Does the quick start use canonical repo front doors?
- Are required credentials, devices, runtimes, or platform constraints stated before
  the command that needs them?
- Is expected output or success behavior clear?
- For a potentially destructive or externally connected tool, is the safe dry-run path
  shown before the mutating path when one exists?

## Information balance

- Does user-facing orientation appear before a large documentation index?
- Does purpose and proof appear before `Quick start`? A first example can establish both
  when its meaning is clear to a newcomer.
- Does the README include at least one representative example before routing to full
  usage docs?
- Are style guides and maintainer-process docs grouped away from the primary user path?
- Does a long README summarize advanced reference material and route it to owned docs?
- Are important existing explanations, examples, status warnings, and credits preserved?

## Adoption context

- Is the current project status honest and evidence-backed?
- Are limitations that affect adoption easy to find?
- When a help route would materially serve the audience, is it concise and verified?
- When the README makes a license claim, does it name and link the applicable license,
  including a relevant code and non-code split?
- Are upstream projects, funding, citations, or acknowledgments included when they help
  readers understand the project's provenance?

## Presentation and maintenance

- Do headings describe familiar reader tasks and follow a coherent order?
- Are badges limited to meaningful, current signals?
- Do images have descriptive alt text and nearby explanatory context?
- Are commands, paths, links, screenshots, and claims current?
- Are there any template placeholders, empty sections, duplicated paths, or stale
  instructions?
- Could the current headings, examples, and visuals plausibly belong to many unrelated
  projects? If so, add one project-specific treatment from
  [landing_page_ideas.md](landing_page_ideas.md).

## Common repair map

| Symptom | Repair |
| --- | --- |
| One sentence followed by `Documentation` | Add motivation, proof, and a first-success path before the doc map |
| Quick start only installs dependencies | Add the smallest real run and expected result |
| Long ungrouped docs list | Curate and group by newcomer tasks, then internals and process |
| Feature list names modules | Rewrite as capabilities, use cases, or outcomes |
| Visual app has no visual | Add a live link, current PNG, or one focused GIF |
| Complex tool reads like a reference manual | Keep one representative workflow and route advanced material to docs |
| Status or limitation appears late | Move adoption-blocking information near the opening |
| `See LICENSE` without a link or name | Name the evidenced license and link its file |
| Existing README content disappears wholesale | Restore valuable, current content and reorganize it |
