# Make the landing page distinctive

Use this guide to move from a correct README to a memorable project landing page. Build
on the repository's existing ambition, choose one signature idea, and finish it with
specific evidence.

## Find the signature promise

Complete this sentence from repository evidence:

> This project is especially worth exploring because it ________.

Look for the answer in outputs, demos, examples, domain goals, unusual workflows,
performance characteristics, educational value, interoperability, design philosophy,
or a capability that required substantial engineering.

Translate implementation details into a reader-facing promise:

| Evidence in the repo | Landing-page promise |
| --- | --- |
| Many export engines | Move one source through the formats your workflow needs |
| A browser-only build | Try the complete experience with no account or backend |
| A geometry solver | Turn sparse human guidance into a stable computed result |
| A large content bank | Explore broad coverage through a guided, searchable entry point |
| Strong local automation | Reach a repeatable result through one canonical command |
| Careful failure handling | Understand limitations and recover with clear next steps |

## Choose signature proof

Match the promise with the strongest artifact already present or practical to create:

- Interactive product: verified live link plus one focused workflow GIF.
- Visual app: hero screenshot plus a caption explaining the meaningful state.
- CLI: command, representative input, and readable output together.
- Generator or converter: before-and-after artifacts or a compact transformation table.
- Library: a small example whose return value demonstrates the central abstraction.
- Data or research project: sample, provenance, scope, and one reproducible result.
- Educational project: learner goal, representative activity, and educator reuse path.
- Multi-package repo: a decision guide explaining which package serves each need.
- Infrastructure or developer tool: the pain point, integration point, and verified time
  or complexity saved.

Give the proof a project-specific heading when that improves the story. Examples:

- `See the map take shape`
- `From question bank to LMS package`
- `What the virtual camera produces`
- `Choose your first protocol`
- `One source, seven export targets`

## Add a human point of view

Use the project's real voice and priorities. Explain the motivation, design philosophy,
teaching goal, or practical constraint that shaped the work. A concise point of view
helps readers remember why the project exists and distinguishes it from a feature list.

Ground every current-behavior claim in evidence. Present future ambition as a roadmap,
status note, or explicit next step.

## Build the strongest practical version

Complete improvements in this order:

1. Clarify the signature promise.
2. Surface or create the strongest available proof artifact.
3. Connect the proof to a meaningful first-success path.
4. Polish headings, captions, examples, and visual rhythm so they fit this project.
5. Add concise status, limitations, help, licensing, or provenance context when it
   materially serves the audience.

Use the general README template as raw material. Choose, rename, combine, and reorder
sections around the project's story and audience.

## Dispatch unfinished opportunities

When an excellent idea requires additional scope, turn it into a task another owner can
execute immediately:

```text
Outcome: [the landing-page improvement readers will experience]
Owner: [readme-docs, screenshot-docs, another skill, or a named project role]
Target files: [exact paths]
Evidence: [repo behavior, command, page, or artifact to use]
Work: [specific artifact or edit to create]
Success criteria: [observable finished state]
Verification: [exact command, render check, or interaction]
```

Strong example:

```text
Outcome: Show the editor's drag-to-adjust workflow near the README opening.
Owner: screenshot-docs
Target files: README.md, docs/screenshots/concept_map_demo.gif
Evidence: the running editor and its existing Honeybees example
Work: record one node drag and the live edge reroute in a 3-5 second GIF
Success criteria: the start state, action, and final layout are readable under 5 MB
Verification: replay the loop, check alt text and prose, run the Markdown link test
```
