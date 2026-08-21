# Platform skills completion report

status: complete
primary_targets: [claude, codex]
compatibility_targets: [cursor, opencode]
installation_model: source-backed items are symlinks; native generated agents are regular files
generated_outputs: [skills_index, plugin_manifests, agents_index]

## Permanent tests retained

- Fast pytest covers durable parser, discovery, adapter, target-containment, sidecar-diagnostic,
  replacement, and symlink behavior with inline data or `tmp_path`. It performs no network requests
  or subprocess CLI round trips.
- `tests/e2e/e2e_primary_adapter_contract.py` covers the guided primary install, verifies that every
  written leaf is a planned skill or agent, and repeats the interview without installer state. It
  remains outside pytest because it drives the real CLI and filesystem.
- Generator `--check` commands remain product validation entry points; the executions recorded
  below are one-time rebuild evidence rather than additional permanent tests.

## Checks intentionally not retained

- The platform-answer parser pytest duplicated the guided CLI E2E.
- The compatibility lifecycle leg duplicated the same installer path and is recorded only as a
  one-time rebuild check.
- The optional `tests/e2e/run_all.sh` added a permanent runner for only one E2E.
- Duplicate-target diagnostic priority, a tunable sidecar-length assertion, and category
  collection/tautology checks did not satisfy the permanent-test checklist.
- Thin file-wrapper parsing, tunable category-order validation, overlapping missing-sidecar
  diagnostics, and private state-parser cases were implementation checks rather than durable
  behavioral contracts. Receipt, version, ownership, hash, and pruning checks were removed with
  the unnecessary hidden-state design.
- A redundant operating-system symlink behavior case and a repeated-interview wording assertion
  were removed during the independent audit; installer link behavior remains covered directly.

## One-time rebuild evidence

- `source source_me.sh && python3 -m pytest tests/ -q`: PASS (3,708 passed).
- `python3 tests/e2e/e2e_primary_adapter_contract.py` from the repository root on Python 3.12:
  PASS without sourcing the development environment (guided linked primary install and state-free
  repeat interview).
- `source source_me.sh && python3 tools/build_skills_index.py --check`: PASS (38 published skills;
  1 retired skill skipped).
- `source source_me.sh && python3 tools/build_plugin_manifest.py --check`: PASS (manifest version
  26.8.0).
- `source source_me.sh && python3 tools/build_agents_index.py --check`: PASS.
- `source source_me.sh && python3 tools/openai_sidecars.py --check`: PASS (39 tracked skill
  sources).
- `bash -n devel/setup_typescript.sh devel/setup_playwright.sh && npm pkg get name version
  scripts`: PASS (valid shell syntax, repository identity, and only existing script targets).
- `git diff --check`: PASS.

## Residual risk

Cursor and OpenCode have deterministic adapter checks and one-time synthetic installation proof,
but no permanent lifecycle E2E or live-client runtime guarantee. Absolute source links require the
repository clone to remain at its installed location.
