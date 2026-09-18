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

## Testing and gates

- Keep plan gates and requirements grounded in reality. Avoid arbitrary thresholds.
- Plans making improvements should not expect byte-identical output.
- I want robust software: it continues to function despite imperfect inputs, data, state, or
  behavior. Handle imperfections according to their context and impact, with graceful recovery
  that preserves useful operation whenever possible.
- Apply KISS aggressively. Prefer the smallest coherent design that satisfies actual
  requirements and known failure modes. Complexity must earn its place.
- Prefer adaptability over speculative edge-case handling. Design clear boundaries, stable
  domain concepts, and replaceable components so unexpected cases can be handled later.
- Treat tests as liabilities as well as assets. A permanent test must protect behavior that is
  intentionally stable, important to preserve, and plausibly subject to regression. Test
  contracts over implementation details. When in doubt, remove the test.
- Use temporary tests and one-time checks freely to prove implementation work. Keep them in
  `tests/_temp/`, outside the permanent suite and Git tracking; promote one only when the
  behavior itself deserves permanent protection.
- New behavior gates require a failure plan. If a gate's failure would not change the
  implementation or identify a real correctness problem, the gate is noise.
- Review testing plans against `docs/REPO_STYLE.md`, `docs/PYTEST_STYLE.md`, and other repo
  guidance. If a test requires a hack I did not ask for, question the test first.
- Audits and reviews should ask for fewer tests, not more.

## Prompting

- Prioritize positive prompting. Small LMs mishandle negative instructions and may flip them
  into positive actions. Phrase instructions as "Do X" or "Use Y".
- "Leave git to the manager" is a negative prompt in disguise; omit git entirely and encourage
  the wanted behavior instead. Name unwanted tools only when truly needed. Positive prompting
  plus omission beats a negative boundary.
