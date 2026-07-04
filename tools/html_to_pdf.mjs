// tools/html_to_pdf.mjs - CLI tool to render HTML to PDF via Chromium.
// Usage: node tools/html_to_pdf.mjs --input <file-or-url> --output <path.pdf> [--landscape]

import { chromium } from "playwright";
import { parseArgs } from "node:util";
import { resolve, parse, format } from "node:path";
import { pathToFileURL } from "node:url";
import { existsSync } from "node:fs";
import { cwd } from "node:process";

async function main() {
  const options = {
    input: { type: "string" },
    output: { type: "string" },
    landscape: { type: "boolean", default: false },
  };

  const args = parseArgs({ options, strict: true });
  const { input, output, landscape } = args.values;

  // Validate required flags
  if (!input) {
    console.error("Error: --input flag is required");
    process.exit(1);
  }

  // Derive output filename from input if not provided
  let outputPath;
  if (output) {
    outputPath = output;
  } else {
    // Check if input is a URL (http/https/file scheme)
    if (
      input.startsWith("http://") ||
      input.startsWith("https://") ||
      input.startsWith("file://")
    ) {
      console.error("Error: --output flag is required when input is a URL");
      process.exit(1);
    }

    // Derive output from input: same directory + same basename + .pdf extension
    const parsed = parse(input);
    // Check if input already ends with .pdf to avoid overwriting
    if (parsed.ext.toLowerCase() === ".pdf") {
      console.error(`Error: input file already has .pdf extension, cannot derive output: ${input}`);
      process.exit(1);
    }
    outputPath = format({
      dir: parsed.dir || ".",
      name: parsed.name,
      ext: ".pdf",
    });
  }

  // Resolve input URL or file path
  let url;
  if (input.startsWith("http://") || input.startsWith("https://") || input.startsWith("file://")) {
    url = input;
  } else {
    // Resolve relative paths against cwd
    const filePath = resolve(cwd(), input);
    if (!existsSync(filePath)) {
      console.error(`Error: input file not found: ${filePath}`);
      process.exit(1);
    }
    url = pathToFileURL(filePath).href;
  }

  // Launch browser and generate PDF
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({
    viewport: { width: 1440, height: 1200 },
  });

  await page.emulateMedia({ media: "screen" });
  await page.goto(url, { waitUntil: "networkidle" });

  await page.pdf({
    path: outputPath,
    format: "Letter",
    landscape,
    margin: {
      top: "0.6in",
      right: "0.6in",
      bottom: "0.6in",
      left: "0.6in",
    },
    printBackground: true,
    scale: 1,
  });

  await browser.close();
  console.log(`PDF generated: ${outputPath}`);
}

await main();
