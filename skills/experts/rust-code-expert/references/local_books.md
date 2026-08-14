# Local books

Use this reading order to select from the nine local Rust conversions. Each
path is plain text inside a code span so it remains usable when the local-only
corpus is present and stays outside committed Markdown links. Consult
`reference_survey.md` for passage-based coverage ratings.

## Reading order

1. `references/local-only/The_Rust_Programming_Language_3rd_Edition-2026.md`
   Start with the comprehensive language treatment for ownership, borrowing,
   `Result`, traits, lifetimes, modules, Cargo, threads, and async. Grep
   `UNDERSTANDING OWNERSHIP`, `Lifetime Elision`, or `Transfer Data Between Threads with Message Passing`.
2. `references/local-only/Fluent_Rust_Crafting_Robust_Software_With_Idiomatic_Design_Principles-2024.md`
   Use this for idiomatic ownership design, error propagation, traits, module
   organization, and patterns that fit Rust. Grep `Error Propagation Idioms`,
   `Trait Bounds and Where Clauses`, or `Module Organization Best Practices`.
3. `references/local-only/Refactoring_to_Rust-2025.md`
   Use this for incremental migration, allocation-aware improvement, `unsafe`,
   raw pointers, C FFI, and advanced bindings. Grep `Refactoring vs. rewriting`,
   `Raw pointers`, or `Advanced FFI`.
4. `references/local-only/The_Rust_Programming_Handbook_An_end-to-end_guide_to_mastering_Rust_fundamentals-2025.md`
   Use this as a practical language and toolchain companion, especially for
   Cargo setup, release builds, `Result`, and concurrency. Grep `Using Cargo and Crates.io`,
   `The Result type`, or `Concurrency and Parallelism`.
5. `references/local-only/Command-Line_Rust_A_Project-Based_Primer_for_Writing_Rust_CLIs-2022.md`
   Use this first for executable command-line programs, argument design, clap,
   testable output, and user-visible errors. Grep `Adding clap as a Dependency`,
   `Using the Result Type`, or `Parsing and Validating the Command-Line Arguments`.
6. `references/local-only/Speed_Up_Your_Python_with_Rust_Optimize_Python_performance-2021.md`
   Use this for a Python-to-Rust performance migration, package layout, PyO3,
   and Python-facing command tools. Grep `Managing our code with crates and Cargo instead of pip`,
   `Building a Rust interface with the pyO3 crate`, or `Creating command-line tools for our package`.
7. `references/local-only/Design_Patterns_and_Best_Practices_in_Rust_Enhance_your_Rust_skills-2026.md`
   Use this after a core design works to replace object-oriented habits with
   Rust-appropriate ownership, trait, enum, module, and crate patterns. Grep
   `Trying to defeat the borrow checker`, `Using Clone and Rc Everywhere`, or `Rust alternatives: modules and crates as facades`.
8. `references/local-only/Practical_Rust_Projects_Build_Serverless_AI_Machine_Learning-2023.md`
   Use this as a project recipe source for clap-based CLIs, web services,
   serverless deployment, games, and WebAssembly-adjacent examples. Grep
   `Handling Complex Arguments with Clap`, `Handling Errors`, or `Installing the Rust Toolchain`.
9. `references/local-only/Rust_for_Data_Science_A_Rustacean_Odyssey_A_Sophisiticated_Guide_For_Rustaceans-2024.md`
   Use this for data-oriented crates, tooling with rustfmt and Clippy,
   concurrency, performance work, and Python extension examples. Grep
   `Mastering the Rust Toolchain`, `Performance Optimization and Load Testing`, or `Building Python Extensions in Rust`.

## Use current documentation for moving APIs

Use the books for concepts, architecture, and worked examples. Confirm current
Rust, Cargo, Tokio, clap, PyO3, maturin, and crate API details in official Rust
documentation or `docs.rs` before implementation.
