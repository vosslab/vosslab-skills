# Project workflow

Use this workflow on the target project. Inspect the repository first, identify its current
delivery shape, and record the command and artifact that establish the finding.

## Shared Wasm contract

Record these decisions in the target project's existing architecture document or a focused
Wasm design note:

- Target triple and host runtime, such as browser with `wasm32-unknown-unknown` or a WASI runtime.
- Cargo crate type, package command, generated package location, and browser entry point.
- Exported functions, input and output types, error encoding, and ownership across the boundary.
- Browser APIs, web-sys feature flags, supported browsers, and fallback behavior.
- Native-versus-Wasm fixture format plus the expected comparison tolerance.
- Release bundle-size budget and interactive frame-time or startup budget.

## Greenfield wasm-pack project

1. Create a Rust library crate with `cdylib` output and add wasm-bindgen plus the needed web-sys
   features.
2. Add the browser target with rustup and use wasm-pack to build a browser package.
3. Implement one deterministic Rust computation with an ordinary native unit test.
4. Expose one narrow wasm-bindgen function, create a minimal browser entry point, and call it.
5. Add fixtures that run the same computation natively and through the browser or Node Wasm harness.
6. Build release output, record compressed and uncompressed package sizes, then measure startup or
   frame time in browser performance tooling.
7. Expand browser APIs, Canvas rendering, or application integration after the vertical slice passes.

## Existing Rust crate gaining a browser target

1. Inventory Cargo workspaces, public APIs, feature flags, native tests, build scripts, and existing
   JavaScript or TypeScript consumers.
2. Identify the host-neutral computation module and add characterization tests for its current behavior.
3. Add a Wasm-facing crate or feature with `cdylib`, wasm-bindgen, the browser target, and wasm-pack
   packaging while keeping native entry points intact.
4. Introduce a small adapter that owns conversion between Rust values and JavaScript or web-sys types.
5. Run fixed fixtures through the native API and Wasm export, then compare results before changing
   algorithms or performance settings.
6. Build the release browser package, load it from a minimal host page, and record size plus measured
   startup or frame time.
7. Grow the browser surface one verified export or API boundary at a time.

## Corpus-absent route

Use [topic_index.md](topic_index.md) to select current wasm-bindgen, Rust target, MDN WebAssembly,
browser, or WASI documentation when local books are absent. Execute a release wasm-pack build and
the matching browser, runtime, or native-versus-Wasm oracle before accepting the workflow change.
