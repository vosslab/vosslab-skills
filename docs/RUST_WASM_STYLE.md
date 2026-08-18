# Rust WebAssembly style

Use this guide for Rust that ships as WebAssembly to a browser or a WASI runtime.
[RUST_STYLE.md](RUST_STYLE.md) owns Rust language and shared Cargo practice; this
document owns the runtime contract, host adapter, and delivered artifact.

## Start with the runtime contract

Record the target triple, runtime, supported browsers or runtime version, crate type,
package command, generated artifact location, host entry point, exported API, ownership,
error encoding, and delivery budgets before implementation. One explicit contract makes
the Rust core, generated bindings, and host application agree on what they exchange.

Choose the target for the host that runs the module:

- Use `wasm32-unknown-unknown` with `wasm-bindgen` and `wasm-pack` for a browser
  package. Build a `cdylib` adapter crate when its exports are consumed by JavaScript.
- Use `wasm32-wasip1` when a selected runtime provides the Preview 1 compatibility
  model. Test its required capabilities in that runtime.
- Use `wasm32-wasip2` when the selected component-capable runtime and deployment
  model call for WASI Preview 2. Confirm the runtime, component tooling, interfaces,
  and capability model together before choosing it.

Follow the manager-selected direct-dependency form from
[RUST_STYLE.md](RUST_STYLE.md#16-toolchain-and-dependencies): `version = "*"` or
`version = ">=LATEST"`. Confirm the current `wasm-bindgen`, `wasm-pack`, target, and
runtime guidance before selecting features or commands.

## Build a portable Rust core

Put deterministic domain computation in ordinary, host-neutral Rust with Rust types
and concrete `Result` errors. Native tests call this core directly. Keep the Wasm
adapter focused on converting values, invoking the core, and presenting results to the
host. This makes behavior portable and gives every boundary a clear owner.

- Export small, typed `wasm-bindgen` functions. Define accepted values, returned
  values, ownership transfer, mutation, and error encoding for each export.
- Use `web-sys` feature flags for the browser APIs the adapter calls and `js-sys` for
  JavaScript built-ins. Each enabled feature belongs to a documented browser capability.
- Convert strings, collections, typed arrays, and application data at one boundary.
  Measure transfer and allocation cost before introducing a lower-level representation.
- Convert core errors once into a stable JavaScript-facing form with actionable context.
  Preserve structured categories where the host needs programmatic recovery.
- Keep host callbacks, browser objects, and scheduler handles in the adapter. Pass
  owned domain values or safe borrows into the Rust core.

For an existing native crate, add a focused Wasm-facing crate or feature and preserve
the native entry points. Characterize the existing core first, expose one observable
export, then broaden the host API after its contract and proof are established.

## Deliver the browser package

Use the generated `wasm-bindgen` bindings as the JavaScript contract. Load the release
package from a minimal real browser page before connecting it to a larger frontend.
Keep generated package output separate from handwritten browser code so ownership is
obvious.

For Canvas or interactive rendering, use `requestAnimationFrame` as the browser
scheduler. Keep update and rendering responsibilities explicit, use a measured frame
budget, and record input, update, and draw timing for a fixed scene. A fixed-step
simulation paired with time-based rendering is often a useful starting point when
consistent simulation behavior matters.

Use browser developer tools, source maps, and console diagnostics while resolving
host integration behavior. Treat browser-visible output, a rendered known result, or
a reproducible harness result as the proof that the shipped package runs.

## Deliver the WASI module

Treat the selected runtime as part of the API. Name its version, required interfaces,
capabilities, command or component entry point, inputs, outputs, and exit behavior.
Give the module only the capabilities required by its contract, then run a minimal
release module in that exact runtime as an integration check.

Keep WASI I/O and runtime-specific bindings at the adapter boundary. The shared Rust
core remains directly callable by native tests and by the WASI entry point.

## Verify across the boundary

Use the same fixed fixture corpus through native Rust and the Wasm export. Compare
exact output, serialized structures, or a documented numeric tolerance. Cover the
boundary shapes the project exposes: empty input, boundary numbers, Unicode, large
buffers, error conversion, repeated calls, and scheduled browser updates.

Run the Rust baseline from the owning package or workspace:

```bash
cargo fmt --check
cargo check
cargo test
cargo clippy -- -D warnings
```

Then run a host proof that matches delivery:

- Browser: build the release package, load it in a browser, call an export, and
  assert the expected result. Inspect a known Canvas pixel, path, or screenshot when
  rendering is part of the contract.
- WASI: build the selected target, run the module or component in the selected
  runtime, and assert its output and exit behavior.
- Parity: run every deterministic fixture natively and through the Wasm boundary.

## Measure the release artifact

Measure the artifact the host receives, not only a development build. Record raw
`.wasm`, generated JavaScript, and compressed transfer sizes. When an interactive
surface matters, record startup, compilation or instantiation, and median plus worst
frame time for a fixed workload. Keep the command, browser or runtime, machine context,
input shape, and budget with the measurement.

Use a size-analysis tool and a browser performance trace to identify the largest real
contributors before choosing an optimization. Re-run native-versus-Wasm parity after
changes to representation, allocation, bundle composition, or scheduling.

## WebAssembly completion checklist

- The target triple, host runtime, package command, artifact, and supported host matrix
  are explicit.
- The host-neutral Rust core owns deterministic domain behavior and domain errors.
- The Wasm adapter owns conversion, host APIs, scheduling, and host-facing errors.
- `wasm-bindgen`, `web-sys`, and `js-sys` choices are limited to the documented boundary.
- Browser packages load in a real browser; WASI modules run in their selected runtime.
- Native and Wasm fixtures agree within the documented comparison rule.
- Release size and startup or frame-time measurements have a recorded budget.

## Current authoritative references

- [Rust browser target: `wasm32-unknown-unknown`](https://doc.rust-lang.org/rustc/platform-support/wasm32-unknown-unknown.html)
- [Rust WASI Preview 1 target](https://doc.rust-lang.org/rustc/platform-support/wasm32-wasip1.html)
- [Rust WASI Preview 2 target](https://doc.rust-lang.org/rustc/platform-support/wasm32-wasip2.html)
- [wasm-bindgen guide](https://wasm-bindgen.github.io/wasm-bindgen/)
- [wasm-pack documentation](https://wasm-bindgen.github.io/wasm-pack/)
- [MDN: WebAssembly](https://developer.mozilla.org/en-US/docs/WebAssembly)
- [MDN: `requestAnimationFrame`](https://developer.mozilla.org/en-US/docs/Web/API/Window/requestAnimationFrame)
