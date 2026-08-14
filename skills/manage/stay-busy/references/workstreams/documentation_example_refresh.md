# Documentation example refresh workstream

**Purpose:** re-run every code example embedded in `docs/*.md` against
the current codebase, fix or flag broken examples. Catches doc rot
caused by code changes since the example was written.

## Templates

- Extract every fenced code block tagged `python` from `docs/*.md`.
  Run each in a fresh subprocess (`source source_me.sh && python3
  _temp_example_<n>.py`). Capture stdout / stderr. Report failures
  with `doc:line` location and the actual error. Output a Markdown
  table at `output/doc_examples_<name>.md`, columns: doc file, line,
  status (PASS / FAIL / SKIPPED), failure reason.
- For CLI examples (lines starting with `$ command ...`), execute the
  command in a `/tmp` scratch directory. Compare actual output to any
  documented expected output that follows the command.
- For import examples (`import X`, `from X import Y`), verify the
  imported module exists and the named symbols are exported.

**Artifact:** PASS / FAIL / SKIPPED Markdown table plus the captured
output of every failing example.

**Blocked fallback:** skip examples that need external resources
(network, API keys, files outside the repo) and list them under
`SKIPPED` with the missing-resource reason. Do not fail the
workstream because an external dependency was unreachable; produce
the partial result.
