# Project workflow

Use this sequence on the target project after selecting a route in
[topic_index.md](topic_index.md).

## Detect project state

Inspect `Cargo.toml`, workspace members, `src/`, `tests/`, CI configuration,
target settings, and the current failing command. Treat an existing manifest,
source module, or test suite as an existing project; otherwise begin greenfield.

## Existing project path

1. Inventory the crate, owning module, public call sites, feature flags, target
   triples, error types, and current compiler or test evidence.
2. Write the value-flow contract: who creates, owns, borrows, mutates, and
   consumes each key value; name lifetime relationships at public boundaries.
3. Capture characterization tests for behavior that callers depend on.
4. Implement one small change in the owning module, preserving the established
   crate layout and error style.
5. Run `cargo fmt --check`, `cargo check`, focused `cargo test`, and
   `cargo clippy -- -D warnings`; add the route-specific oracle.

## Greenfield project path

1. Create the smallest package or workspace and choose library, binary, or
   binding ownership deliberately.
2. Define domain types, a `Result` error contract, one public operation, and a
   native target triple.
3. Add one success test and one meaningful error test before broadening the API.
4. Build the first vertical slice through `cargo run` or `cargo test`.
5. Add async runtime, FFI/PyO3, unsafe code, dependencies, and performance work
   only when their ownership and test contracts are explicit.

## Corpus-absent route

When books are absent, return through [topic_index.md](topic_index.md), consult
the official Rust Book, Rustonomicon, Cargo Book, or `docs.rs`, and execute
`cargo check` plus focused `cargo test` or the selected oracle before delivery.
