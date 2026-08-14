# Testing and oracles

Choose a runnable oracle from [topic_index.md](topic_index.md) before calling a
Rust change complete.

## Compiler and tooling baseline

Run these from the owning workspace root:

```bash
cargo fmt --check
cargo check
cargo test
cargo clippy -- -D warnings
```

Use a focused `cargo test <name>` while iterating, then run the applicable
workspace or target command before reporting completion.

## Route-specific oracles

- Ownership, borrowing, lifetimes, and traits: compile the intended caller and
  cover the valid value flow with unit or integration tests.
- `Result` and CLI behavior: assert returned errors, stdout, stderr, and exit
  status with representative invalid input.
- Tokio: use deterministic synchronization, bounded timeouts, and test-owned
  channels or clocks to assert task results and cancellation behavior.
- Unsafe and FFI: test the safe wrapper's invariant; run Miri or a sanitizer
  when the target toolchain supports it; exercise the foreign caller directly.
- PyO3: build the extension and run a Python integration test against its
  public function, types, and exceptions.
- Performance: record baseline command, input shape, machine constraints, and
  measured wall time, throughput, allocations, or flamegraph evidence.

## Corpus-absent route

Use [topic_index.md](topic_index.md) to choose the route when local books are
absent, confirm details in the official Rust Book, Rustonomicon, Cargo Book, or
`docs.rs`, then execute `cargo check`, `cargo test`, and the compiler, binding,
CLI, sanitizer, or benchmark oracle that matches the change.
