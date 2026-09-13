# Human guidance

<!-- VENDORED HEADER: START -->
Record the durable guidance Neil Voss states, or approves for preservation here, in his own words:
first person or close paraphrase, one to three lines per bullet. Material he supplies as a source
may inform [DESIGN_DECISIONS.md](DESIGN_DECISIONS.md) once it is settled, and an entry of uncertain
origin belongs there too. Rules: [REPO_STYLE.md](REPO_STYLE.md).
[PROPAGATED HEADER - ENTRIES BELOW ARE YOURS]
<!-- VENDORED HEADER: END -->

## Decision priority

- Treat this repository as development infrastructure. Keep its indexing subsystem at the root in
  `index_lib/`, and provide one launcher because I run all indexing scripts together.
- Treat KISS (Keep It Simple, Stupid) as a top-level priority.
- Prefer the smallest ownership-correct implementation that satisfies the current request.
- Add abstractions, compatibility layers, configuration, and permanent tests only for a
  demonstrated current need.
- Installers modify only the requested installed content. Do not add receipts, hidden state,
  hidden configuration, or unrelated filesystem writes.
- Treat the Git repository as the latest install source and platform destinations as stale copies;
  do not add installer version comparison or ownership tracking.
- Install Codex categories as live links under `.codex/skills/<category>`. Keep Claude skill links
  flat under `.claude/skills/<skill>`. Use `.cursor/skills` for Cursor and
  `.config/opencode/skills` for OpenCode instead of the shared `.agents/skills` compatibility root.
- Use the current operating-system home as the installer root. Do not expose an alternate-home
  interview question or command-line flag solely for testing; isolate E2E runs with standard
  `HOME` instead.
- Build `docs/RELATED_PROJECTS.md` for visitors seeking comparable or adjacent projects and
  resources. Choose entries that share the repository's audience, user problem, or workflow;
  treat implementation technologies as context.
