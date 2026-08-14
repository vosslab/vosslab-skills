# Test workstream

**Purpose:** extend coverage at edges, boundaries, or recently-changed
code.

## Templates

- Add pytest cases under `tests/test_<area>.py` covering: empty input,
  single-element input, max-size input, malformed input. Reuse fixtures;
  do not assert on tunable defaults (per `docs/PYTEST_STYLE.md`).
- Add round-trip invariant test for `<encoder>` and `<decoder>`. Random
  inputs seeded deterministically.
- Add boundary test that fails before `<fix commit>` and passes after.
  Bisect-friendly: name it `test_regression_<issue>.py`.

**Artifact:** test file path plus `pytest <file> -v` output captured to
`output/test_<name>.log`.

**Blocked fallback:** write skeleton test with `pytest.skip("reason")`
and a `NEEDS_CONTEXT` note explaining what evidence is missing.
