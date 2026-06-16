# USAGE.md

How to run the tools in this repository.

## reset_repo.py

`reset_repo.py` is the bootstrap entry point for a new consumer repo cloned from this
template. It runs an interactive interview (project type, code license, docs license,
PyPI intent, stage, commit), writes the `REPO_TYPE` marker, installs license files,
seeds `pyproject.toml` when PyPI is requested, runs propagation, and removes
template-meta paths.

### Normal use (interactive)

```bash
source source_me.sh && python3 reset_repo.py
```

The script interviews you in your terminal. No flags are required for normal use.

### CLI flags

| Flag | Description |
| --- | --- |
| `--config <file>` | Supply interview answers from a JSON file (testing/reproducibility mode) |
| `--dry-run` | Log planned actions without writing any files |
| `-h` | Show help and exit |

### Config mode (testing/reproducibility interface)

`--config` is intended for automated testing and reproducible resets, not for
routine human use. Pass a JSON file with the interview answers:

```bash
source source_me.sh && python3 reset_repo.py --config my_config.json
```

Config mode is non-interactive: the script reads answers from the file and proceeds
without prompting. This replaces the interactive interview for the run.

#### JSON schema

| Key | Required | Values | Notes |
| --- | --- | --- | --- |
| `project_type` | YES | `python` / `p`, `typescript` / `t`, `rust` / `r`, `other` / `o` | Short alias or full token |
| `code_license` | YES | SPDX identifier or alias (e.g. `MIT`, `m`, `GPL-3.0`, `g`) | Resolved via `resolve_license` |
| `docs_license` | no | SPDX identifier or alias | Default: `CC-BY-4.0` |
| `pypi` | no | `true` / `false` | Default: `false`; Python-only |
| `stage` | no | `true` / `false` | Default: `true` |
| `commit` | no | `true` / `false` | Default: `false` |

#### Minimal example

```json
{
  "project_type": "python",
  "code_license": "GPL-3.0"
}
```

#### Full example

```json
{
  "project_type": "typescript",
  "code_license": "MIT",
  "docs_license": "CC-BY-4.0",
  "stage": false,
  "commit": false
}
```

### Folder-name guard

The script refuses to run when the repo root directory is named exactly
`starter-repo-template`. This protects the template development checkout from
accidental destruction.

If you see this error, clone or rename the repo to your project name first:

```
This repo is named starter-repo-template. Clone or rename it to the consumer project name before running reset.
```

The guard checks the folder name only; it does not inspect remotes or origin URLs.

### Outside a git repo

Running `reset_repo.py` outside a git repository exits with a clear message
instead of a raw subprocess traceback.

## E2E test harness

For the clone-based reset E2E harness (LOCAL and REMOTE modes), see
[E2E_TESTS.md](E2E_TESTS.md) and the inline documentation in
`tests/meta/e2e/e2e_reset_routing.py`. The harness is template-meta:
it lives under `tests/meta/e2e/` and is removed by reset.

Run all offline E2E tests:

```bash
bash tests/meta/e2e/run_all.sh
```

Run a single E2E test:

```bash
source source_me.sh && python3 tests/meta/e2e/e2e_reset_routing.py
```
