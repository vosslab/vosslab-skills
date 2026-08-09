# Testing and oracles

Build a fixture corpus around the host boundary and use the same computation in native Rust and
WebAssembly as the primary correctness oracle. Keep fixtures deterministic and name the command or
harness that produces each result.

## Native-versus-Wasm parity

1. Place deterministic computation in a host-neutral Rust module.
2. Run fixed fixtures through a native Rust test or executable.
3. Run the same fixtures through the Wasm export in a browser or Node harness.
4. Compare exact values, serialized structures, or documented numeric tolerances.
5. Save the fixture inputs and expected results near the target project's tests.

Use fixtures for empty input, boundary numbers, Unicode strings, large buffers, errors, repeated
calls, and browser-scheduled updates when the project exposes those surfaces.

## Browser and runtime checks

- Load the generated wasm-pack package in a minimal browser page and assert that one export runs.
- Render a known Canvas result for web-sys drawing work and inspect a screenshot or pixel value.
- Exercise requestAnimationFrame with a fixed scene for animation work and record frame durations.
- Run a minimal module in the selected WASI runtime and assert its expected output or exit status.
- Inspect browser console output and source-mapped stack traces while resolving integration failures.

## Measured delivery budgets

Measure the release artifact and use recorded results as the performance evidence.

- Record raw `.wasm`, generated JavaScript, and compressed transfer sizes for each release candidate.
- Capture a browser performance trace and record median and worst frame time for an interactive scene.
- Record startup, compile, or instantiation timing when first-use latency matters.
- Compare measurements against a stated budget and preserve the baseline with the command and environment.
- Re-run native-versus-Wasm parity after bundle, allocation, or scheduling changes.

## Corpus-absent route

Follow [topic_index.md](topic_index.md) to current wasm-bindgen, Rust target, MDN WebAssembly,
browser, or WASI documentation when local books are absent. Execute the native-versus-Wasm harness
and the relevant release-size, frame-time, browser-rendering, or runtime-output oracle to validate
the recommendation with current tooling.
