# Lint and Render Checks

Primary lint path uses the local renderer API at http://localhost:3000.

## Renderer API (preferred)

- Ensure http://localhost:3000/health returns JSON status.
- Use the local helper script:
  - python3 references/scripts/lint_pg_via_renderer_api.py -i <file.pgml>
  - Add -r to print rendered HTML.
- The helper currently defaults to HTML responses. If you need structured lint fields,
  pass _format=json by adding it in the request or patching the helper.

## Manual curl (JSON response)

Send JSON and request JSON output:

curl -X POST "http://localhost:3000/render-api?_format=json&isInstructor=1" \
  -H "Content-Type: application/json" \
  -d '{"problemSource":"<PGML HERE>","problemSeed":1234,"outputFormat":"default"}'

Check fields:
- flags.error_flag
- debug.pg_warn
- debug.internal

## Other lint notes

- PGML parses once; avoid tag wrapper syntax inside Perl strings.
- Use [$var]* when a variable contains HTML spans.
- Avoid <table>, <tr>, <td> in PGML (blocked by whitelist).
