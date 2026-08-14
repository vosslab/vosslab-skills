# Topic index

Start here for every Rust request. Match the symptom to a preferred action,
then use the linked workflow and executable oracle.

| Trigger | Preferred action | Evidence | Local source when present |
| --- | --- | --- | --- |
| Borrow checker error | Map moves and borrows; return or borrow the value with the caller's responsibility | `cargo check` plus a behavior test | `references/local-only/The_Rust_Programming_Language_3rd_Edition-2026.md` |
| Lifetime or trait implementation | State the relationship in the API; use trait bounds near the generic boundary | `cargo check` plus compile and unit tests | `references/local-only/Fluent_Rust_Crafting_Robust_Software_With_Idiomatic_Design_Principles-2024.md` |
| `Result` propagation | Define a domain error and add context at application boundaries | focused `cargo test` and CLI exit assertion | `references/local-only/Command-Line_Rust_A_Project-Based_Primer_for_Writing_Rust_CLIs-2022.md` |
| Cargo, features, or Clippy | Inspect the workspace manifest and target feature graph | `cargo check`, `cargo test`, `cargo clippy -- -D warnings` | `references/local-only/The_Rust_Programming_Handbook_An_end-to-end_guide_to_mastering_Rust_fundamentals-2025.md` |
| Tokio async or concurrency | Define task ownership, cancellation, timeout, and shared-state rules | deterministic async test with Tokio time control | `references/local-only/The_Rust_Programming_Language_3rd_Edition-2026.md` |
| Unsafe or raw pointers | Encapsulate invariants in a small safe wrapper | safe-wrapper test plus Miri or sanitizer when available | `references/local-only/Refactoring_to_Rust-2025.md` |
| C FFI, PyO3, or Python performance | Keep the ABI boundary typed and narrow; test from the foreign caller | integration test through the binding | `references/local-only/Speed_Up_Your_Python_with_Rust_Optimize_Python_performance-2021.md` |
| CLI design | Define typed arguments, input validation, stdout, stderr, and exit codes | command-level integration tests | `references/local-only/Command-Line_Rust_A_Project-Based_Primer_for_Writing_Rust_CLIs-2022.md` |
| Performance regression | Measure a representative baseline before changing allocations or algorithms | benchmark or profile with recorded inputs | `references/local-only/Rust_for_Data_Science_A_Rustacean_Odyssey_A_Sophisiticated_Guide_For_Rustaceans-2024.md` |
| Idiomatic refactor | Express the design with ownership, enums, traits, and focused modules | tests plus Clippy | `references/local-only/Design_Patterns_and_Best_Practices_in_Rust_Enhance_your_Rust_skills-2026.md` |

## Official routes

Use the Rust Book for ownership, borrowing, lifetimes, traits, errors, and
concurrency; use the Rustonomicon for unsafe and FFI invariants; use the Cargo
Book for manifests, workspaces, profiles, and targets; use `docs.rs` for crate
APIs. Follow [project_workflow.md](project_workflow.md) for project shape and
[testing_and_oracles.md](testing_and_oracles.md) for the runnable oracle.

## Corpus-absent route

Use this index when the local corpus is absent. Select the official Rust Book,
Rustonomicon, Cargo Book, or `docs.rs` route above, then run `cargo check` and
the matching compiler, test, binding, CLI, or benchmark oracle.
