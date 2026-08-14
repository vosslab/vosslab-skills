# Task selection

Classify the request first, then choose the narrowest Rust route and its
executable proof. Use [topic_index.md](topic_index.md) for the detailed route.

## Rust ownership

Own core Rust language work: ownership, borrowing, the borrow checker,
lifetimes, traits, generics, enums, modules, `Result`, Cargo, Clippy, native
targets, CLI tools, Tokio services, unsafe code, FFI, PyO3, and performance.
Frame the task with the owning crate, public API, target triple, value flow,
error behavior, and acceptance command.

## Rust and WebAssembly routing

Select `rust-code-expert` for native binaries, libraries, services, Python
extensions, and compiler-guided core-language work. Select `wasm-rust-expert`
for `wasm-bindgen` JavaScript exports, `wasm-pack` browser packaging,
`wasm32-unknown-unknown`, `web-sys`, browser canvas, bundle-size work, and
native-versus-Wasm parity. This assigns all six Rust/WebAssembly routing probes
to their intended owner.

## Task questions

- Which crate and module own the change, and is the target an executable,
  library, Python extension, or native service?
- Which values move, borrow, mutate, or outlive the call, and which trait or
  generic constraint defines the API?
- Which failures are expected, and where should `Result` add context?
- Which target, feature flags, platform APIs, and runtime model must compile?
- Which command demonstrates the behavior: compiler diagnostic, `cargo test`,
  CLI invocation, binding test, sanitizer, or benchmark?

## Corpus-absent route

When local books are absent, start in [topic_index.md](topic_index.md), read
the official Rust Book, Rustonomicon, Cargo Book, or `docs.rs` as the topic
requires, then run `cargo check` and the selected `cargo test` or oracle.
