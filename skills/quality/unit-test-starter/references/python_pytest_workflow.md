# Python pytest workflow

Read this reference for a multi-module or repository-wide coverage pass after
reading the target repository's pytest policy and configuration.

## Discover the boundary

1. Determine the repository root using the repository's normal workspace
   convention. Discover candidate Python files in a stable order, for example:

   ```bash
   rg --files -g "*.py" | sort
   ```

2. Exclude generated, vendored, archived, virtual-environment, build, and
   dependency directories according to repository evidence. Do not infer a
   whole-repository mandate from a request that names only one module.
3. Inspect existing tests and configuration before choosing a test-file name or
   import pattern. Follow an established mapping when one exists; otherwise use
   an ASCII-safe, unambiguous repository-relative test name.

## Make imports safe

Prefer the repository's normal import form. Create or extend `tests/conftest.py`
only when a shared import path or test-environment setting is genuinely needed.
Keep it small and repository-wide. If an imported library writes caches or
configuration outside test-owned paths, set its environment variables early to
a pytest-managed temporary location.

Never make import failures disappear through per-test path changes. When a
module has unavoidable unsafe import-time behavior, leave it uncovered by this
fast lane and explain the boundary in the completion report.

## Choose behavior that earns coverage

For each safe candidate, identify stable behavior that the code and repository
make meaningful:

- typical inputs and a genuine boundary or empty case;
- explicit validation failures or exceptions;
- encode/decode, parsing, or domain invariants;
- filesystem behavior wholly owned by `tmp_path`.

Avoid reproducing implementation logic in a test. Mock time, randomness, or
environment only when the resulting deterministic contract is intentional.
Do not test real network calls, sockets, external services, or subprocesses in
the pytest lane. Do not create a placeholder test or a module-wide skip simply
to satisfy a one-to-one source-file mapping.

## Build and run incrementally

Use `pytest.mark.parametrize` when a small input/output table clarifies a single
contract. Keep assertions close to the behavior and use stable exception-message
matching only when the message is contractual.

Run the repository's focused command after each coherent test addition. A common
form is:

```bash
source source_me.sh && python3 -m pytest tests/test_package__module.py
```

The repository's documented command wins. Keep a concise record of each module,
the behavior covered, behavior deliberately left out, and the reason. Before
finishing a broad pass, run the appropriate complete fast lane when its cost is
proportionate to the change.
