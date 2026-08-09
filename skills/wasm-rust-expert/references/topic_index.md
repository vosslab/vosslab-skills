# Topic index

Start here. Match the delivery problem to a target, toolchain, current-documentation route,
and executable oracle. Use [reference_survey.md](reference_survey.md) and
[local_books.md](local_books.md) for local conceptual detail when the corpus is available.

| Trigger or project problem | Preferred route | Current source | Executable oracle |
| --- | --- | --- | --- |
| Export Rust to JavaScript with wasm-bindgen | wasm-bindgen exports and generated bindings | wasm-bindgen guide | Call the export from a browser or Node Wasm harness with fixed fixtures. |
| Package a browser build with wasm-pack | wasm-pack release package | wasm-pack and Rust target docs | Build the package, load the generated module, and record package bytes. |
| Add a browser target to a Rust crate | `wasm32-unknown-unknown`, cdylib, wasm-pack adapter | Rust target docs and wasm-bindgen guide | Build native tests and the browser package from the same crate. |
| Bind CanvasRenderingContext2d through web-sys | web-sys feature-gated Canvas API | web-sys docs and MDN Canvas | Render a known draw call and inspect the browser result. |
| Debug a wasm32 Canvas game loop | requestAnimationFrame loop and fixed update step | MDN Web APIs and browser performance docs | Record a browser trace and measure frame time for a fixed scene. |
| Reduce a wasm-pack browser bundle | release profile, wasm-opt, size analysis | wasm-bindgen guide and MDN WebAssembly | Measure compressed and uncompressed bytes before and after the change. |
| Compare a simulation across native and Wasm | portable Rust core plus narrow adapter | Rust test docs and wasm-bindgen guide | Run identical inputs natively and through the Wasm export; compare outputs. |
| Choose a WASI runtime or target | current WASI target and runtime capability model | Rust target docs and WASI docs | Compile a minimal module and run it in the selected runtime. |
| Investigate browser memory or startup | host boundary, allocation, loading, and trace | MDN WebAssembly and browser devtools docs | Capture a performance or memory profile and record the measured value. |

## Corpus-absent route

Use this table when `references/local-only/` is absent. Open the named current source, build
the smallest release artifact for the selected target, and run the table's oracle. Treat the
observed native-versus-Wasm result, browser rendering result, runtime output, or measurement as
the evidence for the next implementation step.

## Probe coverage

This index owns the six routing probes for wasm-bindgen JavaScript exports, wasm-pack bundle
size, wasm32 Canvas loops, Rust crates gaining browser targets, native-versus-Wasm parity, and
web-sys Canvas bindings. Route TypeScript and Solid implementation requests through
[task_selection.md](task_selection.md).
