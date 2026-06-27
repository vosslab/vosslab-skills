# Renderer API guide

This document describes the HTTP API for rendering PG or PGML problems from scripts.

## Base URL and endpoints

- The renderer serves requests at `{SITE_HOST}{baseURL}{formURL}`.
- Defaults are `baseURL: ''` and `formURL: '/render-api'` in `render_app.conf.dist`.
- Primary render endpoint: `POST /`.
- Compatibility endpoint: `POST /render-api`.
- Health check: `GET /health`.

## Request format

- The renderer reads request parameters from form/query params and merges JSON bodies.
- When both are present, JSON values override form/query params.
- Use multipart form data or `application/x-www-form-urlencoded` for browser parity.
- Use JSON for API clients that prefer `Content-Type: application/json`.
- Required parameters include a source and a seed:
  - Provide one source, in this order of precedence:
    - `problemSourceURL`: URL to fetch JSON with a `raw_source` field.
    - `problemSource`: raw PG source string (can be base64 encoded).
    - `sourceFilePath`: file path relative to `Library/`, `Contrib/`, or `private/`.
  - `problemSeed`: integer seed for reproducible randomization.
- Parameter precedence is `problemSourceURL` then `problemSource` then `sourceFilePath`.
- If you do not have access to the renderer container filesystem, prefer `problemSource`
  over `sourceFilePath`. `sourceFilePath` must be readable inside the renderer container.

## Common parameters and defaults

| Key | Type | Default | Notes |
| --- | ---- | ------- | ----- |
| problemSeed | number | required | Seed for reproducible randomization. |
| outputFormat | string | `default` | Output style (also supports `static`, `ptx`, `raw`). |
| displayMode | string | `MathJax` | Math rendering mode (`MathJax` or `ptx`). |
| _format | string | `html` | Response structure (`html` or `json`). |

## Minimal request example (recommended)

```bash
curl -X POST "http://localhost:3000/render-api" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "sourceFilePath=private/myproblem.pg" \
  --data-urlencode "problemSeed=1234" \
  --data-urlencode "outputFormat=html"
```

## JSON request example

```bash
curl -X POST "http://localhost:3000/render-api" \
  -H "Content-Type: application/json" \
  -d '{
    "sourceFilePath": "private/myproblem.pg",
    "problemSeed": 1234,
    "outputFormat": "html"
  }'
```

## Response format

- Use `_format` to control response structure:
  - `_format: "html"` returns HTML content (default).
  - `_format: "json"` returns JSON describing the render.
- Errors return non-200 status codes with a JSON payload containing `message` and `status`.
- When `isInstructor=1`, JSON responses include an `inputs` echo of the resolved request parameters.

## Lint-critical response schema

The UI uses `_format: "json"`, which returns a JSON response shaped like this:

```json
{
  "renderedHTML": "<!doctype html>...",
  "debug": {
    "perl_warn": null,
    "pg_warn": ["..."],
    "debug": ["..."],
    "internal": ["..."]
  },
  "problem_result": {},
  "problem_state": {},
  "flags": {
    "error_flag": 0
  },
  "resources": {
    "regex": [],
    "alias": {},
    "assets": []
  },
  "JWT": {
    "problem": null,
    "session": null,
    "answer": null
  }
}
```

Conditional fields:

- When `isInstructor=1`, the response includes `answers`, `inputs`, and `pgcore`.
- When `includeTags=1`, the response includes `tags` and `raw_metadata_text`.

Lint notes:

- Translator errors and PG warnings are rendered into `renderedHTML` and are not returned as structured fields.
- `flags.error_flag` indicates a render error.
- `debug.pg_warn` contains warning strings from PG WARN_message.
- `debug.internal` and `debug.debug` contain internal and debug message strings.
- Line and column numbers are not structured fields; they may appear inside the warning or error text.

## Response examples

### HTML response (default)

```html
<!doctype html>
<html>
  <head>...</head>
  <body>...</body>
</html>
```

### JSON response (`_format: "json"`)

Fields vary by `outputFormat`. Example shape:

```json
{
  "inputs_ref": {
    "sourceFilePath": "private/myproblem.pg",
    "problemSeed": 1234,
    "outputFormat": "default"
  }
}
```

### Error response

```json
{
  "message": "[abc123] Failed to retrieve problem source.",
  "status": 500
}
```

## problemSourceURL expectations

When using `problemSourceURL`, the renderer fetches JSON and reads a `raw_source` field.
The `raw_source` value is used as-is, so provide plain PG source text.

Example response from your source service:

```json
{
  "raw_source": "DOCUMENT();\nloadMacros(\"PGstandard.pl\");\nTEXT(beginproblem());\nENDDOCUMENT();\n"
}
```

## problemSource base64 usage

The renderer accepts raw PG source in `problemSource`. If you send base64-encoded content, the renderer will
decode it before rendering. Only base64-encode when your transport or client requires it.

Example JSON payload with base64 content:

```json
{
  "problemSource": "RE9DVU1FTlQoKTsKTG9hZE1hY3JvcygiUEdzdGFuZGFyZC5wbCIpOwpURVhUKGJlZ2lucHJvYmxlbSgpKTsKRU5ERE9DVU1FTlQoKTsK",
  "problemSeed": 1234,
  "outputFormat": "default"
}
```

## Rendering and display options

- `outputFormat`: controls the problem output style (`default`, `static`, `ptx`, `raw`).
- `displayMode`: controls math display (`MathJax` or `ptx`).
- `language`: locale identifier (default `en`).

## Interaction options

- `hidePreviewButton`: hide the preview answers button.
- `hideCheckAnswersButton`: hide the submit answers button.
- `showCorrectAnswersButton`: enable the show correct answers button.

## Content options

- `isInstructor`: enable instructor view and features (preferred over `permissionLevel`).
- `showHints`: show hints when available.
- `showSolutions`: show solutions when available.
- `hideAttemptsTable`: hide the attempts table.
- `showSummary`: show the summary under the attempts table.
- `showComments`: render author comments.
- `showFooter`: show renderer footer information.
- `includeTags`: include tags in JSON responses.

## JWT endpoints

- `POST /render-api/jwt` returns a problem JWT based on the request parameters.
- `POST /render-api/jwe` returns a JWE-encrypted problem JWT.
- When a `problemJWT` is provided, its values override request parameters.

### JWT flow example

1) Request a JWT for a specific problem:

```bash
curl -X POST "http://localhost:3000/render-api/jwt" \
  -H "Content-Type: application/json" \
  -d '{
    "sourceFilePath": "private/myproblem.pg",
    "problemSeed": 1234,
    "outputFormat": "default"
  }'
```

2) Use the returned token in a render request:

```bash
curl -X POST "http://localhost:3000/render-api" \
  -H "Content-Type: application/json" \
  -d '{
    "problemJWT": "<JWT_FROM_STEP_1>"
  }'
```

## Linting guidance

If you are building a linter against this API, use the JSON response and a layered
approach to detect problems.

### Recommended parsing rules

- Check top-level `errors` or `warnings` fields if your integration maps them in.
- Message keys are often one of `message`, `error`, `warning`, `detail`, `stderr`.
- Line keys commonly include `line`, `lineNumber`, `lineno`, `row`.
- Column keys commonly include `column`, `col`, `columnNumber`, `colNumber`.
- If no line or column is provided, default to `1:1`.
- Consider scanning message text for `Line N` or `line N column M` patterns.

### How to detect errors for linting

Use a conservative, layered approach:

1) Check `flags.error_flag` in the JSON response.
2) Scan `debug.pg_warn` for warning strings.
3) Scan `debug.internal` and `debug.debug` for renderer diagnostics.
4) If none are present, scan `renderedHTML` for the warning blocks rendered by the UI
   (for example the "Translator errors" or "Warning messages" sections).

This matches how the renderer reports errors today: some are structured, some are only embedded in the HTML.

## UI request payloads

The editor UI in `public/js/navbar.js` uses multipart form data and base64 encodes `problemSource`.

### Render from editor

Fields posted to `POST /render-api` when clicking "Render contents of editor":

- `_format`: `json`
- `showComments`: `1`
- `sourceFilePath`: from the file path input
- `problemSeed`: from the seed input
- `outputFormat`: selected template ID (for example `default`, `static`, `debug`)
- `problemSource`: base64 of the editor contents
- `clientDebug`: `1` when outputFormat is `debug`
- `isInstructor`: `1` when the "Instructor" checkbox is checked
- `clientDebug`: `1` when the "Debug" checkbox is checked

### Submit/preview from rendered problem

Fields posted to `POST /render-api` when submitting answers from the iframe:

- `_format`: `json`
- `isInstructor`: `1`
- `includeTags`: `1`
- `showComments`: `1`
- `sourceFilePath`: from the file path input
- `problemSeed`: from the seed input
- `outputFormat`: selected template ID
- `problemSource`: base64 of the editor contents
- One of `previewAnswers`, `submitAnswers`, or `showCorrectAnswers` from the clicked button
- Any checked checkboxes from the UI (for example `isInstructor`, `clientDebug`)

### Load and save

- Load: `POST /render-api/tap` with `sourceFilePath`.
- Save: `POST /render-api/can` with `problemSource` (base64) and `writeFilePath`.

## UI equivalent curl

This mirrors the UI render request. Use your own `problemSource` base64 content.

```bash
curl -X POST "http://localhost:3000/render-api" \
  -H "Accept: application/json" \
  -F "_format=json" \
  -F "showComments=1" \
  -F "sourceFilePath=private/example.pg" \
  -F "problemSeed=1234" \
  -F "outputFormat=default" \
  -F "problemSource=BASE64_PG_SOURCE"
```
