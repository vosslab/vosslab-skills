# Task selection

Route a request by its delivery target and the layer that owns the requested change.
Choose `wasm-rust-expert` for a Rust computation that compiles to WebAssembly,
crosses a wasm-bindgen boundary, uses wasm-pack, targets a browser or WASI runtime,
or calls browser APIs through web-sys or js-sys.

## Wasm-owned requests

- Own `wasm-bindgen` exports to JavaScript; verify an exported function through a browser or
  Node Wasm harness.
- Own wasm-pack browser packages and bundle-size work; build release output and record bytes.
- Own `wasm32-unknown-unknown` Canvas loops; capture a browser performance trace and measure
  frame time.
- Own a browser target added to a Rust crate; build the package and load its generated module.
- Own native-versus-Wasm simulation parity; run identical fixtures in both targets and compare.
- Own `web-sys` bindings for `CanvasRenderingContext2d`; render a known pixel, path, or frame.

## Positive ownership handoffs

- Route pure Rust language, ownership, borrow-checker, lifetime, trait, Cargo, Tokio, `Result`,
  unsafe, native CLI, and native-target tasks to `rust-code-expert`.
- Route TypeScript types, discriminated unions, typed JavaScript-facing application contracts,
  and `any` cleanup to `typescript-engineer`.
- Route Solid signals, stores, reactivity, components, and SolidStart server functions to
  `solid-js-expert`.
- Collaborate across the boundary by defining Wasm exports here and implementing framework-side
  state or component behavior in the owning front-end skill.

## Corpus-absent route

Start with [topic_index.md](topic_index.md), then consult the current wasm-bindgen guide,
Rust target documentation, MDN WebAssembly, browser documentation, or WASI documentation for
the selected runtime. Execute the route's native-versus-Wasm comparison, release build, or
browser harness to confirm the recommendation without the local corpus.
