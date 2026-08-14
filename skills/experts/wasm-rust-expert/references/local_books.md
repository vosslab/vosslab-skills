# Local books

Use this reading order to select a local book conversion for Rust/WebAssembly
work. The detailed coverage ratings and fallback routes are in
[reference_survey.md](reference_survey.md). Each path is intentionally bare so
the runtime can open the gitignored local corpus directly.

## Reading order

1. `references/local-only/Practical_WebAssembly_Fundamentals_of_WebAssembly_Programming_with_Rust-2022.md`
   Start here for the browser toolchain, wasm-bindgen, wasm-pack, JavaScript
   boundaries, linear memory, Binaryen, and Twiggy. grep `wasm-bindgen`,
   `wasm-pack`, `linear memory`, `Twiggy`.
2. `references/local-only/Game_Development_with_Rust_and_WebAssembly-2022.md`
   Use this for Canvas rendering, `web-sys`, `js-sys`, browser game loops,
   fixed time steps, performance traces, and memory profiling. grep `canvas`,
   `RequestAnimationFrame`, `browser debugger`, `Checking memory`.
3. `references/local-only/Ultimate_Rust_for_Systems_Programming_with_Rust_and_WebAssembly-2024.md`
   Use Chapter 15 for a second project setup and concise explanations of the
   Wasm target, wasm-pack build and test commands, and WASI context. grep
   `wasm32-unknown-unknown`, `wasm-pack`, `WASI`.
4. `references/local-only/Creative_Projects_for_Rust_Programmers_Build_exciting_projects-2020.md`
   Use this as older, project-oriented context for Yew applications, a
   Quicksilver game, and general Rust allocation examples. grep `Introducing
   Wasm`, `animation loop architecture`, `Allocating memory`.

## Current-documentation route

Use the wasm-bindgen guide and MDN WebAssembly documentation for current APIs,
WASI targets and runtimes, allocator choices, browser source maps, load-time
measurement, and browser compatibility. The local books supply conceptual
grounding and worked examples; the official documentation supplies current
behavior.
