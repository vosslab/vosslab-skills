# Rendering SVG for image inspection

This is a side route for turning an authored SVG into PNG evidence. It supports the
drawing and revision loop; the authored SVG remains the source deliverable.

## Primary route: rsvg-convert

Use `rsvg-convert` when available to produce a deterministic local PNG that an image
inspection tool or agent can evaluate. Write previews to a temporary workspace by
default, and use a project location when the project requests durable previews.

```bash
rsvg-convert --width 640 --output preview-640.png asset.svg
rsvg-convert --width 160 --output preview-160.png asset.svg
```

The default background is transparent. When the delivery background matters, render
another proof with the target CSS color:

```bash
rsvg-convert --width 640 --background-color '#ffffff' \
  --output preview-white.png asset.svg
```

Inspect the PNGs with `view_image` or an available image-inspection agent. Use the
large render to find geometry, overlap, clipping, and shading defects; use the
thumbnail to judge recognition, silhouette, line hierarchy, and detail survival.
Re-render after each meaningful SVG revision.

## Fallback route: Playwright

Use Playwright second as an alternate renderer, when librsvg and the target browser
disagree, or when CSS, fonts, scripting, animation, or the real HTML embed mode affects
the result. Use the project's installed Playwright and browser for the inspection
environment.

When `$screenshot-docs` is available, use it for Playwright setup, served-page
capture, deterministic viewport behavior, transient PNG placement, and durable
capture-harness conventions. Skills are runtime capabilities, so invoke or read
`$screenshot-docs` by name.

For the narrower case of a standalone SVG, navigate to its file URL, size the root
element from its `viewBox`, and capture the SVG locator:

```js
import { resolve } from "node:path";
import { pathToFileURL } from "node:url";
import { chromium } from "playwright";

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();
await page.goto(pathToFileURL(resolve("asset.svg")).href);

const svg = page.locator("svg");
await svg.evaluate((node, width) => {
  const viewBox = node.viewBox.baseVal;
  node.style.display = "block";
  node.style.width = `${width}px`;
  node.style.height = `${width * viewBox.height / viewBox.width}px`;
}, 640);
await svg.screenshot({
  animations: "disabled",
  omitBackground: true,
  path: "preview-playwright.png",
  scale: "css",
});
await browser.close();
```

See the [Playwright locator screenshot API](https://playwright.dev/docs/api/class-locator#locator-screenshot)
for current element-capture and screenshot options.

For an SVG used by an application, capture it from the real rendered page. Render
both normal and thumbnail sizes, then send
the PNGs through the same inspection step used for `rsvg-convert`. Two renderers are
useful evidence when browser behavior is in question, but `rsvg-convert` remains the
normal SVG-to-PNG path.
