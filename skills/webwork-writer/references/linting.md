# Lint and Render Checks

Primary lint path uses the local renderer API at http://localhost:3000.

## Renderer API (preferred)

- Ensure http://localhost:3000/health returns JSON status.
- Use the local helper script:
  - `python3 references/scripts/lint_pg_via_renderer_api.py -i <file.pgml>`
    prints a human-readable lint report (default mode).
  - `python3 references/scripts/lint_pg_via_renderer_api.py -i <file.pgml> --json`
    prints the full renderer JSON response, pretty-printed and JWT-redacted,
    suitable for piping into `jq` or `json.loads`.
  - `python3 references/scripts/lint_pg_via_renderer_api.py -i <file.pgml> --html`
    prints the rendered HTML (the same `renderedHTML` string that appears
    inside the JSON payload).
- The helper always sends `_format=json` to the renderer, so all three modes
  read from the same structured response. Fields to check in `--json` mode:
  - `flags.error_flag`
  - `debug.pg_warn`
  - `debug.internal`
  - `debug.debug`
  - `renderedHTML`
- `--json` and `--html` are mutually exclusive. Default (no mode flag) is lint.
- `-t/--template` accepts `static`, `default`, or `debug` (default `debug`).

## Manual curl (JSON response)

Send JSON and request JSON output:

```
curl -X POST "http://localhost:3000/render-api?_format=json&isInstructor=1" \
  -H "Content-Type: application/json" \
  -d '{"problemSource":"<PGML HERE>","problemSeed":1234,"outputFormat":"debug"}'
```

Check fields:

- flags.error_flag
- debug.pg_warn
- debug.internal

## Other lint notes

- PGML parses once; avoid tag wrapper syntax inside Perl strings.
- Use [$var]* when a variable contains HTML spans.
- Avoid <table>, <tr>, <td> in PGML (blocked by whitelist).
