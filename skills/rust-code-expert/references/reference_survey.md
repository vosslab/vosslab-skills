# Reference survey

This survey maps the nine local book conversions in `references/local-only/`
to Rust engineering topics. Use the named grep term to locate the cited
passage. The rating comes from the sampled passage and its titled treatment;
match counts only break ties between passages of comparable quality.

## Core language and project structure

### Ownership and borrowing

Coverage: strong.

- Book: `references/local-only/The_Rust_Programming_Language_3rd_Edition-2026.md`; section: "4 Understanding ownership" and "Ownership rules"; grep: `Ownership Rules`. The sampled passage defines the single-owner and drop-at-scope rules, connects them to stack and heap allocation, and introduces borrowing as the safe way to share access.
- Book: `references/local-only/Fluent_Rust_Crafting_Robust_Software_With_Idiomatic_Design_Principles-2024.md`; section: "Embracing Rust's ownership model"; grep: `Embracing Rust's Ownership Model`. The sampled treatment presents ownership as both syntax and design guidance for safe resource management.

### Lifetimes

Coverage: strong.

- Book: `references/local-only/The_Rust_Programming_Language_3rd_Edition-2026.md`; section: "Generic types, traits, and lifetimes" and "Lifetime elision"; grep: `Lifetime Elision`. The sampled passage derives the compiler's three elision rules, explains when ambiguity remains, and shows a struct whose reference requires a lifetime parameter.
- Book: `references/local-only/Refactoring_to_Rust-2025.md`; section: "2.3 Lifetimes" and "2.3.3 References and lifetimes"; grep: `References and lifetimes`. The chapter applies reference lifetime reasoning while moving an existing program into Rust.

### Traits and generics

Coverage: strong.

- Book: `references/local-only/The_Rust_Programming_Language_3rd_Edition-2026.md`; section: "Generic types, traits, and lifetimes"; grep: `GENERIC TYPES, TRAITS, AND LIFETIMES`. The dedicated chapter places generic types, trait bounds, and lifetime parameters together as Rust's reusable abstraction tools.
- Book: `references/local-only/Fluent_Rust_Crafting_Robust_Software_With_Idiomatic_Design_Principles-2024.md`; section: "Generics and traits: powering abstraction" and "Trait bounds and where clauses"; grep: `Trait Bounds and Where Clauses`. The sampled sections distinguish trait implementation, trait objects, and bounds, then use `where` clauses to make constraints readable.

### Result error handling

Coverage: strong.

- Book: `references/local-only/The_Rust_Programming_Language_3rd_Edition-2026.md`; section: "Recoverable errors with Result"; grep: `Handling Potential Failure with the Result Type`. The passage explains `Ok` and `Err`, shows why ignored results trigger a warning, and uses `match` to choose a failure path.
- Book: `references/local-only/Fluent_Rust_Crafting_Robust_Software_With_Idiomatic_Design_Principles-2024.md`; section: "Error propagation idioms"; grep: `Error Propagation Idioms`. The sampled material uses the `?` operator and error-type conventions to preserve context across several failing operations.

### Modules and crates

Coverage: strong.

- Book: `references/local-only/Speed_Up_Your_Python_with_Rust_Optimize_Python_performance-2021.md`; section: "Managing our code with crates and Cargo instead of pip" and "Structuring code over multiple files and modules"; grep: `Structuring code over multiple files and modules`. The chapter connects crate layout, `mod.rs`, and module interfaces to a package that is built for Python.
- Book: `references/local-only/Fluent_Rust_Crafting_Robust_Software_With_Idiomatic_Design_Principles-2024.md`; section: "Modules and visibility" and "Module organization best practices"; grep: `Module Organization Best Practices`. The sampled advice focuses on public boundaries and organization choices that keep a codebase idiomatic.

### Cargo and the toolchain

Coverage: strong.

- Book: `references/local-only/The_Rust_Programming_Handbook_An_end-to-end_guide_to_mastering_Rust_fundamentals-2025.md`; section: "Getting started with Rust" and "Using Cargo and Crates.io"; grep: `Stable versus Nightly Rust`. The dedicated opening chapter walks through installation, toolchain choice, `Cargo.toml`, dependency installation, builds, runs, and release builds.
- Book: `references/local-only/Rust_for_Data_Science_A_Rustacean_Odyssey_A_Sophisiticated_Guide_For_Rustaceans-2024.md`; section: "Mastering the Rust toolchain: Cargo, Rustfmt, and Clippy"; grep: `Mastering the Rust Toolchain`. The sampled section adds formatting and linting to the Cargo workflow, which is useful for an engineering baseline.

## Runtime safety and interoperability

### Concurrency and async

Coverage: strong for threads and channels; partial for current async runtime design.

- Book: `references/local-only/The_Rust_Programming_Language_3rd_Edition-2026.md`; section: "16 Fearless concurrency"; grep: `Transfer Data Between Threads with Message Passing`. The passage constructs an `mpsc` channel, moves its transmitter into a spawned thread, and explains how ownership transfers protect concurrent code.
- Book: `references/local-only/The_Rust_Programming_Language_3rd_Edition-2026.md`; section: "Fundamentals of asynchronous programming"; grep: `FUNDAMENTALS OF ASYNCHRONOUS PROGRAMMING`. The table of contents establishes a dedicated async treatment, while the sampled concurrency passage supplies the concrete ownership model. Use current runtime documentation on `docs.rs` for Tokio-specific APIs and scheduler behavior.

### Unsafe and raw pointers

Coverage: strong.

- Book: `references/local-only/Refactoring_to_Rust-2025.md`; section: "3.1 Unsafe Rust" and "3.1.1 Raw pointers"; grep: `Raw pointers`. The sampled passage distinguishes `*const` from `*mut`, identifies offset and dereference as the unsafe operations, and assigns the safety proof to the developer.
- Book: `references/local-only/The_Rust_Programming_Language_3rd_Edition-2026.md`; section: "Unsafe Rust"; grep: `unsafe`. The language reference book supplies the wider safety boundary around the low-level examples.

### FFI and Python interop

Coverage: strong for FFI and partial for PyO3 integration.

- Book: `references/local-only/Refactoring_to_Rust-2025.md`; section: "3.2 C Foreign Function Interface" and "Advanced FFI"; grep: `C Foreign Function Interface`. The sampled chapters build a C-callable Rust library, use a `cdylib`, explain C strings, and then expose an NGINX handler with `extern "C"`, bindings, and raw pointers.
- Book: `references/local-only/Speed_Up_Your_Python_with_Rust_Optimize_Python_performance-2021.md`; section: "Building a Rust interface with the pyO3 crate"; grep: `pyO3 crate`. The sampled project builds a pip-installable extension, organizes Rust source across files, and wraps callable functions for Python.
- Book: `references/local-only/Rust_for_Data_Science_A_Rustacean_Odyssey_A_Sophisiticated_Guide_For_Rustaceans-2024.md`; section: "Bridging and FFI" and "Building Python extensions in Rust"; grep: `Building Python Extensions in Rust`. The passage demonstrates a `#[pymodule]` extension boundary for Python data work.

### Current PyO3 ABI and packaging APIs

Coverage: not covered for current PyO3 ABI and packaging APIs.

- Book: `references/local-only/Speed_Up_Your_Python_with_Rust_Optimize_Python_performance-2021.md`; section: "Building a Rust interface with the pyO3 crate"; grep: `pyO3 crate`. The sampled example teaches the architecture of a Python extension. Its packaging commands and API version are historical; use current documentation as the compatibility authority.
- Route API names, `abi3` choices, maturin configuration, and interpreter-support claims to the PyO3 and maturin documentation on `docs.rs` and their official guides. Use the books to frame the boundary and current documentation to implement it.

## Delivery and improvement work

### CLI construction

Coverage: strong.

- Book: `references/local-only/Command-Line_Rust_A_Project-Based_Primer_for_Writing_Rust_CLIs-2022.md`; section: "Accessing the command-line arguments", "Adding clap as a dependency", and "Parsing command-line arguments using clap"; grep: `Adding clap as a Dependency`. The sampled project begins with `std::env::args`, reads compiler diagnostics about `Display`, separates Cargo arguments with `--`, and then adopts clap for robust parsing.
- Book: `references/local-only/Practical_Rust_Projects_Build_Serverless_AI_Machine_Learning-2023.md`; section: "Building a command-line program" and "Handling complex arguments with Clap"; grep: `Handling Complex Arguments with Clap`. The project-oriented treatment supplies a second route from a small CLI to structured arguments and errors.

### Performance work

Coverage: partial.

- Book: `references/local-only/Refactoring_to_Rust-2025.md`; section: "1.4.1 Performance" and "2.4 Preallocating strings to aid performance"; grep: `Preallocating strings to aid performance`. The sampled material makes performance a migration decision and demonstrates a concrete allocation reduction.
- Book: `references/local-only/Rust_for_Data_Science_A_Rustacean_Odyssey_A_Sophisiticated_Guide_For_Rustaceans-2024.md`; section: "Performance optimization and load testing"; grep: `Performance Optimization and Load Testing`. The topic is dedicated to data workloads, but it needs project-specific profiling evidence before generalizing changes.

### Idiomatic refactoring

Coverage: strong.

- Book: `references/local-only/Refactoring_to_Rust-2025.md`; section: "1.1 What is refactoring?", "Refactoring vs. rewriting and the size of deployments", and "2.1 Ownership and borrowing"; grep: `Refactoring vs. rewriting`. The sampled treatment gives a staged migration rationale, asks when Rust is worth the change, and uses ownership and error enums as concrete refactoring constraints.
- Book: `references/local-only/Design_Patterns_and_Best_Practices_in_Rust_Enhance_your_Rust_skills-2026.md`; section: "Anti-pattern: designing for object orientation", "Anti-pattern: using Clone and Rc everywhere", and "Replacing traditional design patterns"; grep: `Trying to defeat the borrow checker`. The passages turn common Java- and C++-shaped habits into Rust-specific alternatives based on enums, traits, ownership, modules, and crates.

## Routing tiers

- Start core language questions with `references/local-only/The_Rust_Programming_Language_3rd_Edition-2026.md`, then use `references/local-only/Fluent_Rust_Crafting_Robust_Software_With_Idiomatic_Design_Principles-2024.md` for idiomatic structure and error propagation.
- Use `references/local-only/Refactoring_to_Rust-2025.md` for staged migrations, low-level FFI, and raw-pointer reasoning.
- Use `references/local-only/Command-Line_Rust_A_Project-Based_Primer_for_Writing_Rust_CLIs-2022.md` for command-line programs and `references/local-only/Speed_Up_Your_Python_with_Rust_Optimize_Python_performance-2021.md` for Python extensions.
- Verify compiler, Cargo, runtime, crate, and binding APIs in official Rust documentation and `docs.rs` before making API-level implementation claims.
