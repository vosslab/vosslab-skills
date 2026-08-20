# Animated README demonstrations

Use animation when a brief interaction communicates the project's value more clearly
than a static state. The output is a small one-play GIF stored beside static screenshots
under `docs/screenshots/`.

## Choose animation deliberately

Good GIF subjects:

- Dragging, drawing, sorting, or direct manipulation.
- A short command whose changing output is the point.
- A before-and-after transformation.
- A compact workflow with two or three visible steps.
- A transition or response that a still image communicates poorly.

Use a static PNG for stable layout, detailed text, charts, settings, or output readers
need time to inspect. Use a video with playback controls for a tutorial longer than 5
seconds. Prefer one strong GIF over several competing animations on the same page.

## Plan the demonstration

Write a one-sentence storyboard before recording:

> Start in [recognizable state], perform [one action], end with [visible result].

Prepare deterministic sample data, hide secrets and personal information, dismiss
notifications, size the window near 16:10, and place the pointer at its starting
position. Record only the app region needed to understand the action.

Target:

- Duration: 3 to 5 seconds, with 5 seconds as the autoplay ceiling and total playback
  limit.
- Width: 800 to 1200 px; default 960 px.
- Frame rate: 1 to 15 fps. Use 8 to 15 fps for smooth GUI or web motion, with
  12 fps as the default. Use 1 to 4 fps for deliberate terminal state changes.
- File size: about 5 MB or less.
- Content: one task with a clear initial state and final result.

## Record a local app

On macOS, use the system screen-recording UI (`Shift-Command-5`) to record a selected
region, or use `screencapture -v` and select the region interactively. Save the source
video under `/tmp`, for example `/tmp/project_demo.mov`.

Perform the storyboard once at a readable pace. Use steady pointer motion, calm visual
transitions, and continuous useful action. Re-record until the source sequence is clear.

## Record a web app

Prefer Playwright video recording so the viewport and action sequence are repeatable.
Create a repository-owned capture harness when the demonstration will be refreshed
after UI changes or new features. Follow the project's existing convention; suitable
locations include `scripts/capture_readme_demo.cjs` and
`tests/visual/capture_readme_demo.ts`. Reuse its established Playwright runner and
dependencies.

The harness should set deterministic sample state, viewport, action, completion
condition, and `/tmp` output path. For a CommonJS-based project, a compact harness can
look like this:

```javascript
// scripts/capture_readme_demo.cjs
const { chromium } = require("playwright");

const browser = await chromium.launch();
const context = await browser.newContext({
  viewport: { width: 1280, height: 800 },
  recordVideo: { dir: "/tmp", size: { width: 960, height: 600 } },
});
const page = await context.newPage();
const video = page.video();
await page.addInitScript(() => localStorage.clear());
await page.goto("http://localhost:8080/");
await page.getByRole("button", { name: "Run" }).click();
await page.getByText("Complete").waitFor();
await context.close();
await video.saveAs("/tmp/project_demo.webm");
await browser.close();
```

```bash
node scripts/capture_readme_demo.cjs
```

Replace the URL, locator, and wait condition with evidence from the app. Prefer a state
or DOM condition over a fixed timeout when one exists. `context.close()` finalizes the
recorded video under `/tmp`. Document the exact rerun command beside the harness or in
the repository's contributor documentation. Keep recordings and intermediate files in
`/tmp`, then copy only the verified final asset to `docs/screenshots/`.

Use a disposable helper under `/tmp` for exploratory capture work. Once the locator,
state setup, and completion condition are proven, promote a reusable workflow into the
repository's conventional capture-support location. Remove the exploratory helper when
the durable harness is ready.

Record the app's normal presentation motion. Then run the same interaction in a
separate Playwright context with `reducedMotion: "reduce"` and video recording omitted.
Confirm that the result remains understandable through stable UI state, adjacent prose,
or another equivalent cue. Capture a static fallback when that check identifies a
reader outcome that motion alone communicates.

## Convert and optimize

Use [../scripts/make_gif.sh](../scripts/make_gif.sh). It uses FFmpeg's palette pipeline,
removes audio, limits the animation to 5 seconds, and plays it once:

```bash
skills/documentation/screenshot-docs/scripts/make_gif.sh \
  /tmp/project_demo.mov \
  /tmp/project_demo.gif
```

Optional positional arguments set width, frame rate, and duration:

```bash
skills/documentation/screenshot-docs/scripts/make_gif.sh \
  /tmp/project_demo.mov \
  /tmp/project_demo.gif \
  960 12 4
```

Inspect the result before copying it:

```bash
open /tmp/project_demo.gif
ls -lh /tmp/project_demo.gif
cp /tmp/project_demo.gif docs/screenshots/project_demo.gif
```

When the size gate reports a result above 5 MB, reduce duration first, then frame rate,
then width while preserving legible text and pointer movement.

## Embed accessibly

Use descriptive alt text that states the demonstrated action and result:

```markdown
![Dragging a node reconnects the concept map in real time](docs/screenshots/concept_map_demo.gif)
```

Add nearby prose explaining the same action and result. Use one-play behavior and the
5-second ceiling because GitHub provides no native pause control for animated images.
Use calm transitions and task-relevant motion. Verify reduced-motion behavior in a
separate context and provide equivalent prose or a static state that communicates the
same result.

## Verify freshness

- Play the GIF from its first frame and confirm it stops on an understandable final
  frame within 5 seconds.
- Confirm the start and final states are both visible long enough to recognize.
- Confirm the frame contains only the intended app, public sample data, and relevant UI.
- Confirm alt text and adjacent prose explain the result on their own.
- Run the same freshness and pruning checks as for PNG screenshots.
