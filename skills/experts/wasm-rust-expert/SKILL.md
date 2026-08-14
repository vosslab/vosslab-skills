---
name: wasm-rust-expert
description: "WebAssembly, wasm-bindgen, wasm-pack, web-sys, wasm32 targets, WASI, browser Canvas, and Wasm performance engineering. Use for Rust code that ships to browsers or Wasm runtimes; use rust-code-expert for pure Rust."
---

# Wasm Rust expert

## Overview

Use this skill to take a Rust-to-WebAssembly request from target selection through
browser integration, measurable performance work, and an executable comparison.
Start from the shipped runtime and browser boundary: target triple, package tool,
JavaScript bindings, browser APIs, and the computation that must agree with native Rust.
Keep Rust computation portable and make the browser adapter a narrow, typed boundary.
Use current wasm-bindgen, Rust target, MDN WebAssembly, browser, and WASI documentation
for version-sensitive behavior; local books add concepts and worked examples when present.

## Workflow

1. Classify the Wasm target and route the request.
- Name the runtime: browser, WASI, embedded host, or another WebAssembly environment.
- Name the integration surface: wasm-bindgen export, wasm-pack package, web-sys API,
  Canvas loop, JavaScript data exchange, target setup, or performance measurement.
- Consult [references/topic_index.md](references/topic_index.md) for the default tools,
  current-documentation route, and executable oracle.
- Read [references/task_selection.md](references/task_selection.md) when Rust, TypeScript,
  Solid, or WebAssembly ownership needs a precise handoff.

2. Detect the project shape and establish its Wasm contract.
- Inspect Cargo manifests, target configuration, generated package files, browser entry points,
  JavaScript or TypeScript bindings, and existing tests before changing code.
- Record the target triple, package command, host API boundary, supported browsers or runtime,
  data ownership, error surface, and performance budget in the project documentation.
- Read [references/project_workflow.md](references/project_workflow.md) for the greenfield
  wasm-pack path and the existing-crate browser-target path.

3. Build the smallest vertical slice and preserve a portable computation core.
- Put deterministic domain computation in an ordinary Rust module that native tests can call.
- Add a focused wasm-bindgen or WASI adapter that converts host values at one boundary.
- Build one observable browser or runtime path before expanding API breadth.

4. Add a native-versus-Wasm oracle before optimization.
- Run the same fixed inputs through native Rust and the Wasm export, then compare exact output
  or a documented numeric tolerance.
- Add boundary fixtures for empty values, Unicode strings, large buffers, error conversion,
  and browser scheduling when those surfaces apply.
- Read [references/testing_and_oracles.md](references/testing_and_oracles.md).

5. Measure the delivered artifact in its real host.
- Build the release package, record compressed and uncompressed bundle sizes, and inspect
  the largest contributors with a size-analysis tool when size matters.
- Capture browser performance traces and measure frame time, startup, or allocation behavior
  against a stated budget.
- Re-run the native-versus-Wasm oracle after each performance change.

6. Select current sources and close the loop.
- Use the local corpus through [references/local_books.md](references/local_books.md) and
  [references/reference_survey.md](references/reference_survey.md) when it is available.
- When the corpus is absent, follow [references/topic_index.md](references/topic_index.md)
  to current wasm-bindgen, Rust target, MDN WebAssembly, browser, or WASI documentation and
  execute the named native-versus-Wasm or browser oracle.

## Implementation defaults

- Use `wasm32-unknown-unknown` with wasm-bindgen and wasm-pack for browser packages.
- Use `web-sys` feature flags for browser APIs and `js-sys` for JavaScript built-ins.
- Keep the domain core host-neutral, then expose small typed exports with explicit ownership.
- Use `requestAnimationFrame` and a measured frame budget for Canvas or interactive rendering.
- Use release builds, size profiling, and browser network inspection before selecting a size fix.
- Use current Rust target and WASI documentation to choose a WASI target and runtime.
- Read [references/topic_index.md](references/topic_index.md) for corpus-absent current sources
  and a command or browser check that verifies each route.

## Quality bar

- State the target triple, host runtime, browser support, and package command.
- Keep each cross-language conversion explicit, typed, and covered by fixtures.
- Compare native and Wasm results for the same deterministic inputs.
- Measure bundle size and frame time or startup time in a release artifact.
- Present a browser-visible result, a runtime log, or a reproducible test output.
- Make one focused change tied to a failing oracle or a recorded measurement.

## Output expectations

When using this skill, aim to produce:
- A target classification and topic-index route, including the owning skill for adjacent work.
- A project-shape finding with the inspected file or command and the Wasm contract.
- A small implementation plan naming the Rust core, adapter boundary, package command, and host API.
- Native-versus-Wasm fixtures and their comparison command or browser harness.
- Release bundle-size and frame-time or startup measurements with a stated budget.
- A concrete next change and the check that confirms it.
