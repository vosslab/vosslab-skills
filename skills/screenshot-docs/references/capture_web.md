# Web capture recipe

How to capture screenshots of a running web app using Playwright and store
them in `docs/screenshots/` following the conventions in
[embedding.md](embedding.md).

## Prerequisites

Install Playwright and the Chromium browser binary before running any web
capture. Run these commands once from the repo root:

```bash
npm install --save-dev playwright
npx playwright install chromium
```

If the repo ships `devel/setup_playwright.sh`, that script automates the
above steps (idempotent, Chromium only):

```bash
bash devel/setup_playwright.sh
```

See the official Playwright docs at https://playwright.dev/docs/screenshots for
full install details and screenshot options.

## Recipe overview

Three steps cover every web capture:

1. Start a local server for the web app.
2. Run the Playwright template to navigate, optionally interact, and
   capture a full-page screenshot.
3. Copy the captured PNG from `/tmp` into `docs/screenshots/`.

## Step 1 - start a local server

For a static HTML or built TypeScript app, serve it with Python's built-in
HTTP server. Open a second terminal or background the process:

```bash
# Serve the repo root on port 8080
python3 -m http.server 8080

# Or serve a built dist/ folder
python3 -m http.server 8080 --directory dist
```

Note the server URL (`http://localhost:8080`) for the next step.

For the `TYPESCRIPT/concept-map-maker` smoke fixture (a browser-only web
app with no build step required for a quick capture), serve the project
directory:

```bash
cd /path/to/concept-map-maker
python3 -m http.server 8080
```

The URL passed to the Playwright template becomes `http://localhost:8080/`.

## Step 2 - run the Playwright template

Use the template at
[scripts/screenshot_web.mjs](../scripts/screenshot_web.mjs).
Pass the target URL and the output PNG path as command-line arguments.
The template saves the PNG to the path you specify.

```bash
# Capture a plain page - writes to /tmp first
node skills/screenshot-docs/scripts/screenshot_web.mjs \
    http://localhost:8080/ \
    /tmp/concept_map_main.png
```

For a flow that requires a click before the interesting state appears,
duplicate `screenshot_web.mjs` into your repo's `tests/playwright/` folder
and add the interaction steps between `page.goto()` and `page.screenshot()`.
See https://playwright.dev/docs/input for click and wait patterns.

Example with an interaction step added in a local copy:

```javascript
// Navigate to the page
await page.goto(url);
// Click to open the concept editor panel
await page.click('#open-editor-btn');
await page.waitForTimeout(500);
// Capture the editor state
await page.screenshot({ path: outputPath, fullPage: true });
```

## Step 3 - copy into docs/screenshots/

After the capture writes the PNG to `/tmp`, copy it into the committed
screenshots folder following [embedding.md](embedding.md):

```bash
cp /tmp/concept_map_main.png docs/screenshots/concept_map_main.png
```

Crush large PNGs before committing when the file exceeds 500 KB:

```bash
optipng -o3 docs/screenshots/concept_map_main.png
```

## Worked example - concept-map-maker smoke fixture

The `TYPESCRIPT/concept-map-maker` project is a browser-only web app with no
server-side component, making it a clean smoke fixture for web capture.

```bash
# 1. Start the local server from the project directory
cd /path/to/concept-map-maker
python3 -m http.server 8080 &
server_pid=$!

# 2. Capture with the template
cd /path/to/vosslab-skills
node skills/screenshot-docs/scripts/screenshot_web.mjs \
    http://localhost:8080/ \
    /tmp/concept_map_main.png

# 3. Copy into docs
cp /tmp/concept_map_main.png /path/to/concept-map-maker/docs/screenshots/concept_map_main.png

# Stop the server
kill $server_pid
```

Embed the result in `README.md`:

```markdown
![Concept map editor showing the main canvas](docs/screenshots/concept_map_main.png)
```

## Embed the captured screenshot

See [embedding.md](embedding.md) for the full embed syntax,
storage conventions, and size-budget rules. The short version:

- Store in `docs/screenshots/` at the target repo root.
- Use lowercase_underscore filenames with `.png` extension.
- Write descriptive alt text that names what the screenshot shows.
