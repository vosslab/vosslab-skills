---
name: rust-code-expert
description: "Engineer idiomatic Rust with ownership, borrow checker, lifetimes, traits, cargo, clippy, async/Tokio, unsafe, FFI/PyO3, Result error handling, CLI tools, and performance. Use for Rust code, native targets, or Rust API design."
---

# Rust code expert

## Overview

Use this skill for small, compilable Rust changes with explicit ownership, an error contract, a target triple, and executable proof.
Own core Rust language work, Cargo workflow, and native-target delivery.
Route browser and WebAssembly targets to `wasm-rust-expert`.
Start with [references/task_selection.md](references/task_selection.md) to classify the request, then use
[references/topic_index.md](references/topic_index.md) for focused guidance, a local source, and an oracle.

## Workflow

1. Classify the Rust task and name its contract.
- Identify the crate, binary or library boundary, target triple, public API,
  inputs, outputs, ownership transfer, error type, and performance concern.
- Match borrow checker, lifetime, trait, Cargo, Tokio, unsafe, FFI/PyO3,
  Result, CLI, or performance work in [references/topic_index.md](references/topic_index.md).
- Select `wasm-rust-expert` for `wasm-bindgen`, `wasm-pack`, `web-sys`,
  `wasm32-unknown-unknown`, browser bundles, browser canvas, and native-versus-Wasm parity.
2. Detect the project shape and establish the work surface.
- Inspect `Cargo.toml`, `Cargo.lock`, `src/`, workspace members, existing tests,
  target-specific configuration, CI commands, and the failing compiler output.
- Existing project: name the owning module, public call sites, current tests, and the narrowest behavior to preserve.
- Greenfield project: create the smallest crate, domain and error types, an entry point, and one executable success path.
- Read [references/project_workflow.md](references/project_workflow.md) for
  the project-shaped sequence and artifact locations.
3. Model ownership before editing implementation details.
- Draw the value flow: creator, borrower, mutator, consumer, and lifetime
  relationship at each API edge.
- Express invalid states with enums, compose behavior with traits, and expose
  fallible operations as `Result` with contextual errors.
- Keep unsafe, FFI, and PyO3 boundaries small, documented, and wrapped by a
  safe Rust-facing API.
4. Implement one focused vertical slice.
- Make the smallest change that fulfills the contract in the owning module.
- Prefer direct ownership and borrowing, explicit trait bounds, and standard
  library types before adding dependencies.
- Confirm the crate API and compatible version in `docs.rs`, then use `cargo add`
  and record feature and target requirements in `Cargo.toml`.
5. Build executable evidence as the change develops.
- Run `cargo fmt --check`, `cargo check`, focused `cargo test`, and
  `cargo clippy -- -D warnings` from the relevant workspace root.
- Use compiler diagnostics as the first ownership and type oracle, then add a
  deterministic unit, integration, CLI, FFI, or performance test.
- Read [references/testing_and_oracles.md](references/testing_and_oracles.md)
  to choose the required oracle and measurement.
6. Review the delivered behavior.
- Confirm the command, library API, or binding returns actionable errors with useful `Result` context.
- Recheck feature flags, platform assumptions, public documentation, and
  benchmark conditions before reporting a performance conclusion.

## Implementation defaults

- Prefer ownership-first APIs that return owned values, immutable borrows, or
  scoped mutable borrows according to the caller's responsibility.
- Use enums and trait implementations to represent domain alternatives and
  shared behavior; keep generic bounds close to the API they constrain.
- Use `thiserror` for library error types and `anyhow` for application-level
  context when the target already uses those patterns.
- Build CLI tools with a typed argument structure, validated inputs, stable
  stdout, actionable stderr, and explicit process exit behavior.
- Use Tokio for asynchronous I/O or concurrency, and make cancellation,
  timeouts, and task ownership visible in the API.
- Encapsulate unsafe operations in a small module with invariants, preconditions,
  and safe tests at the boundary.
- Confirm Rust, Cargo, Tokio, clap, PyO3, maturin, and crate APIs in official
  documentation or `docs.rs` before relying on version-sensitive details.
- Load [references/local_books.md](references/local_books.md) and
  [references/reference_survey.md](references/reference_survey.md) when the
  local corpus is present.

## Quality bar

- Compile every affected target and keep `cargo clippy -- -D warnings` clean.
- State the ownership and lifetime model in code, comments, or API names where
  a reader needs it to use the interface correctly.
- Make error behavior observable with `Result` tests, exit-status assertions,
  or binding-level exception checks.
- Validate unsafe, FFI, and PyO3 seams with a safe wrapper test and a boundary
  invariant.
- Measure performance with a representative workload and report the command,
  data shape, baseline, and result.
- Follow [references/topic_index.md](references/topic_index.md) when the local
  corpus is absent, consult the official Rust Book, Rustonomicon, Cargo Book,
  or `docs.rs`, and run the compiler plus the selected test or oracle.

## Output expectations

When using this skill, produce:
- The target shape, owning crate and module, native target, and selected topic route.
- A concise ownership, lifetime, trait, and error-handling rationale for the change.
- A file- and symbol-specific implementation or recommendation, including safe boundary invariants for unsafe, FFI, or PyO3 work.
- Executed Cargo commands, test or oracle results, and performance measurements
  when performance is in scope.
- A clear next step when an external API, target platform, or benchmark input needs user confirmation.
