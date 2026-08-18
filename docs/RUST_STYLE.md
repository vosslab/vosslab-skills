# Rust style

Language model and human guide to Rust in this repo. It applies to every `.rs` file
and every crate here.

Rust style here means: let the toolchain settle formatting, use the type system to
make invalid states unrepresentable, propagate errors as values, and keep `unsafe`
rare, small, and audited.

A concise definition:

> Idiomatic Rust for this repo is rustfmt-formatted, Clippy-clean, `Result`-first
> code. Errors propagate with `?` and are handled at a boundary. Invariants live in
> types, not in repeated runtime checks. Public API shape is designed with `pub use`
> rather than mirroring the private module tree. `unsafe` is wrapped in a safe
> abstraction, kept small, and checked with Miri. Tests live in `#[cfg(test)]`
> modules for units and in `tests/` for integration.

Repo-wide conventions live in `docs/REPO_STYLE.md`. Its core philosophies are cited
by name throughout this document.

## Rust quick-start rules

Use these rules to select the idiomatic Rust path quickly. Each points to the
full guidance below.

- **Format `.rs` files with rustfmt.** Use its four-space indentation. See section 1.
- **Shape the crate API with `pub use`.** Keep `lib.rs` as a concise facade over
  focused modules. See section 5.
- **Return `Result` and propagate with `?`.** Handle each error flow at its
  appropriate boundary. See section 6.
- **Model fallibility and absence in the type system.** Use `Result`, `Option`, and
  validated domain types. See sections 8 and 9.
- **Borrow first and make each clone intentional.** Accept the allocation cost when
  the caller needs a distinct owned value. See section 10.
- **The manager selects the repository's latest-first dependency form.** Use either
  `version = "*"` or `version = ">=LATEST"`; `Cargo.lock` records the exact
  resolution. See section 16.
- **`rust-version` is a toolchain floor, not a dependency update policy.** It
  takes a bare version such as `"1.97.1"`; Cargo rejects range operators in this
  field. See section 16.
- **`unsafe` marks a proof obligation.** The compiler keeps enforcing all other
  Rust rules while the programmer proves the unsafe boundary sound. See section 12.

## 1. Let rustfmt and Clippy own formatting

Rust has an official style guide, and rustfmt implements it. Its guiding principles
are, in priority order, readability, aesthetics, specifics such as version-control
friendliness, and ease of application.[^style-principles] The default formatting
conventions are spaces rather than tabs, four spaces per indentation level, and a
maximum line width of 100 characters.[^style-index]

This is the one place where Rust style deliberately parts company with
`docs/PYTHON_STYLE.md`. The tabs-not-spaces rule in that document is a Python rule
about `.py` files. For `.rs` files, rustfmt output is authoritative. Accept its layout
unchanged, and add a custom `rustfmt.toml` only when the repo records a specific
reason to diverge from community defaults.

rustfmt reformats code to the community style, and many collaborative projects use it
precisely to prevent arguments about which style to use.[^book-appd] That is the core
philosophy **Focus on important issues** in one sentence: formatting is bikeshedding, so
delegate it to a tool and spend the argument budget on design.

Use all four baseline gates from the owning package or workspace root:

```bash
cargo fmt --check
cargo check
cargo test
cargo clippy -- -D warnings
```

Use a focused `cargo test NAME` while iterating, then run the applicable package,
workspace, feature, and target commands before reporting completion. `--check`
verifies formatting without rewriting files; plain `cargo fmt` applies it.
`-D warnings` promotes every lint to an error so warnings cannot accumulate.

Two more tools from the same appendix:[^book-appd]

- `cargo fix` applies rustfix suggestions for compiler warnings that have an
  unambiguous correction, and also drives edition migration.
- `rust-analyzer` is the community-recommended language server, giving completion,
  jump-to-definition, and inline errors in an editor.

Good rule:

> rustfmt decides layout. Clippy decides idiom. You decide design.

## 2. Apply shared principles in Rust

Use Rust's language-native practices for the repository's shared principles:

- Format Rust with rustfmt's four-space indentation.
- Present a deliberate public API through a small `pub use` facade in `lib.rs`.
- Return `Result`, propagate errors with `?`, and handle them at the appropriate boundary.

The repo-wide philosophies carry over; language mechanics follow Rust's own tools and
idioms. In particular: **fix the design, not the symptom**, use explicit required
values, and prefer the durable fix (**long-term over short-term**). Rust gives the
compiler enough information to enforce many of those decisions.

## 3. Rust naming conventions

Rust naming follows RFC 430, catalogued in the Rust API Guidelines.[^api-naming]

| Item | Convention |
| --- | --- |
| Crates and modules | `snake_case` |
| Types, traits, enum variants | `UpperCamelCase` |
| Functions, methods, local variables | `snake_case` |
| Macros | `snake_case!` |
| Statics and constants | `SCREAMING_SNAKE_CASE` |
| Type parameters | Single uppercase letter, for example `T` |
| Lifetimes | Short lowercase, for example `'a` |

In `UpperCamelCase`, an acronym counts as one word: write `Uuid`, not `UUID`.

Conversion methods carry cost information in their prefix, and readers rely on
it.[^api-naming]

- `as_` is a free conversion between borrowed views, for example `str::as_bytes`.
- `to_` is a potentially expensive conversion, typically borrowed to owned, for
  example `str::to_lowercase`.
- `into_` consumes the receiver, for example `String::into_bytes`.

Picking the wrong prefix is a correctness-adjacent bug: it misreports allocation and
ownership to every caller.

File naming follows `docs/REPO_STYLE.md`: lowercase ASCII, underscores between words,
no CamelCase in filenames. `CamelCase` is reserved for type names inside the file.

## 4. Crate and module layout

A package holds one or more crates: at most one library crate at `src/lib.rs`, and
any number of binary crates at `src/main.rs` and `src/bin/*.rs`. Modules form a tree
rooted at the crate root, and everything is private to its parent by default until
marked `pub`, as described in the Rust book chapter
[Control Scope and Privacy with Modules](https://doc.rust-lang.org/book/ch07-02-defining-modules-to-control-scope-and-privacy.html).

Use this filename map:

| Path | Cargo or module role |
| --- | --- |
| `src/main.rs` | Default binary crate root; use a thin stub that calls descriptive modules |
| `src/lib.rs` | Library crate root; use a thin facade for crate docs, modules, and public re-exports |
| `src/bin/name.rs` | Additional binary crate root; use a thin stub when the command has substantial behavior |
| `src/name.rs` | Descriptive module declared as `mod name;` |
| `src/name/child.rs` | Child module declared from `name.rs` |
| `tests/name.rs` | Descriptive integration test crate compiled separately by Cargo |

`docs.rs` names Rust's hosted crate-documentation service. Write crate front-page
documentation with `//!` in the crate root, store extended prose under `docs/`, and
give ordinary Rust modules responsibility-specific filenames. Use Cargo's canonical
filenames for Cargo-defined roots and descriptive filenames for every project-defined
module or test.

### Generic filenames are routing stubs

Treat every generic filename as an index into descriptively named implementation
files. Limit a routing stub to:

- crate or module attributes and a brief `//!` overview;
- `mod` declarations and a small set of intentional `pub use` re-exports;
- entry-point wiring that calls a descriptive application or command module; and
- test-module declarations that route to focused behavior tests.

Place functions, domain types, `impl` blocks, algorithms, data tables, substantial
tests, and long examples in files named for the responsibility they own. When a
routing file gains behavior, create the owning descriptive module first and make the
routing file point to it.

The 999-line maximum is the final ceiling for descriptive implementation modules.
Keep routing stubs at the naturally small size produced by the responsibilities above.

Before changing an existing project, name the owning crate and module, public callers,
enabled features, target triple, error type, and current failing command. Trace each
key value from creator through borrower or mutator to consumer, including lifetime
relationships at public boundaries. Make the smallest complete change in the owning
module and preserve the established crate layout and error style. Capture a
characterization test first when public callers depend on behavior that is changing.

For a new project, choose library, binary, service, or Python-extension ownership
deliberately. Define domain types, a `Result` error contract, one target triple, one
success test, and one meaningful error test before broadening the API.

Practical rules:

- Use 999 physical lines as the inclusive maximum for every tracked authored Rust
  file. Split by responsibility early so each module remains easy to navigate and
  review.
- Keep crate roots as concise stubs: `main.rs` wires the program, while `lib.rs`
  declares the module tree, carries crate-level documentation, and presents the public
  API. Move domain behavior and long guides into clearly named modules or documents.
- Start every module private. Add `pub` when an outside caller genuinely needs the
  item, not preemptively. Privacy is the cheapest form of **design for adaptability**:
  a private item can be changed without breaking anyone.
- Split a module into its own file when it grows past comfortable reading length
  ([Separating Modules into Different Files](https://doc.rust-lang.org/book/ch07-05-separating-modules-into-different-files.html)).
  Use `src/thing.rs` for the module and `src/thing/child.rs` for its children. Preserve
  `src/thing/mod.rs` in an existing consistent tree; use the named-file layout for new
  modules.
- Keep the tree shallow. This matches `docs/REPO_STYLE.md` on repository structure:
  prefer small single-purpose units and short paths.
- Use `use` to bring the parent of a function into scope rather than the function
  itself, so call sites read `module::function(...)` and the origin stays visible
  ([Bringing Paths Into Scope with the use Keyword](https://doc.rust-lang.org/book/ch07-04-bringing-paths-into-scope-with-the-use-keyword.html)).
  Bring types, traits, structs, and enums in
  by full name. This is the same instinct as the `docs/PYTHON_STYLE.md` preference for
  `import os` over `from os import path`, and here it is also the community idiom.
- Use explicit imports in production modules. Reserve the glob form
  `use super::*;` for `#[cfg(test)]` modules, where it is the accepted convention
  ([Test Organization](https://doc.rust-lang.org/book/ch11-03-test-organization.html)).

For multi-crate projects, use a Cargo workspace so member crates share one
`Cargo.lock` and one `target/` directory
([Cargo Workspaces](https://doc.rust-lang.org/book/ch14-03-cargo-workspaces.html)). Reach for a
workspace when crates are separately meaningful, not merely to create folders.

## 5. Shape the public API with `pub use`

The internal structure that makes sense while writing a crate is often inconvenient
for callers. A caller should not have to write
`use my_crate::some_module::another_module::UsefulType;` to reach a type that is
central to the crate. Re-export with `pub use` instead, producing a
public structure that differs from the private one, without rearranging internals
(the Rust book, [Publishing a Crate to Crates.io](https://doc.rust-lang.org/book/ch14-02-publishing-to-crates-io.html),
section "Exporting a Convenient Public API with `pub use`").

```rust
// src/lib.rs
mod kinds;
mod utils;

// Flatten the two items callers actually reach for.
pub use crate::kinds::PrimaryColor;
pub use crate::utils::mix;
```

This is the explicit exception to the `docs/PYTHON_STYLE.md` rule banning re-export
facades in `__init__.py`. That rule exists because Python's `__init__.py` is a file
coders do not inspect when hunting bugs, so logic hidden there disguises problems.
Rust's `lib.rs` is the opposite: it is the crate root, the first file a reader opens,
and the generated `cargo doc` front page reflects exactly what it re-exports. Shape
the Rust API according to Rust conventions.

The rule survives in spirit, though. A `pub use` line is an API decision, not a
convenience dumping ground:

- Re-export the small set of items that are genuinely the crate's front door.
- Keep implementation logic, conditional imports, and runtime lookup tables in their
  owning modules. Let `lib.rs` remain the public map of the crate.
- Every `pub use` is a public commitment. Removing one is a breaking change.

## 6. Errors are values, and `?` is the propagation tool

Rust splits failure into unrecoverable (`panic!`) and recoverable (`Result<T, E>`).
Returning `Result` is the good default choice
when defining a function that might fail, because it hands the calling code the
decision. Choosing to panic makes that decision on the caller's behalf, and there is
no way back from it
([To panic! or Not to panic!](https://doc.rust-lang.org/book/ch09-03-to-panic-or-not-to-panic.html)).

`docs/PYTHON_STYLE.md` says to avoid `try`/`except`. Translate that into
"propagate `Result` explicitly". The Python rule targets a control-flow construct that swallows
context and encourages broad catches. Rust's `Result` is the opposite: it is a value
in the type signature, visible to every caller, and marked for compiler diagnostics
when unused. The correct Rust translation of the Python rule is:

> `?` propagates. You handle at the boundary.

```rust
// Propagate: the function's signature already advertises that it can fail.
fn load_config(path: &Path) -> Result<Config, ConfigError> {
    let text = std::fs::read_to_string(path)?;
    let config = toml::from_str(&text)?;
    Ok(config)
}
```

In practice:

- Use `?` for the whole call chain; it replaces a `match` whose only job is to return
  `Err(e)` unchanged.
- Handle each error flow at its appropriate outer boundary: `main`, a request
  handler, a task entry point, or a foreign-language adapter. That boundary decides
  how to report, retry, translate, or exit.
- Preserve errors from genuinely failable operations. Use a default only when the
  fallback is part of the domain contract; an incidental `unwrap_or_default()` hides
  the failure.
- Reserve `panic!` for a broken invariant, a violated function contract, or a state
  your code cannot continue from. A contract violation always
  indicates a caller-side bug, calling code has no reasonable way to recover,
  and such contracts belong in the API documentation
  ([To panic! or Not to panic!](https://doc.rust-lang.org/book/ch09-03-to-panic-or-not-to-panic.html),
  section "Guidelines for Error Handling").
- When failure is expected in normal operation, for example malformed parser input or
  an HTTP rate-limit response, return `Result`.

## 7. Choose the error type by crate role

Choose the error type from the crate's role and its callers.

- **Library crates: a concrete error type.** Callers must be able to branch on the
  failure mode, so define an enum, one variant per distinguishable failure, and
  implement `std::error::Error`. `thiserror` derives that boilerplate without adding
  anything to your public type signature. Preserve the cause with `#[from]` or
  `#[source]` so the chain survives.

```rust
#[derive(Debug, thiserror::Error)]
pub enum ConfigError {
    #[error("config file not readable: {path}")]
    Unreadable { path: PathBuf, #[source] source: std::io::Error },
    #[error("config file is not valid TOML")]
    Malformed(#[from] toml::de::Error),
}
```

- **Application crates: contextual errors.** When no downstream API matches on the
  error, `anyhow::Result<T>` plus `.context("...")` gives the user a readable failure
  chain with little ceremony.

Keep `anyhow` at application boundaries and expose concrete errors from libraries.
This preserves structured matching for every downstream caller. Follow the existing
crate's error style when it already satisfies that contract.

Add either crate to `Cargo.toml` explicitly. `docs/REPO_STYLE.md` requires all
dependencies to be declared, not worked around.

## 8. When `unwrap` and `expect` are acceptable

Examples, prototypes, and tests commonly use `expect` where full recovery would hide
the behavior being demonstrated
([To panic! or Not to panic!](https://doc.rust-lang.org/book/ch09-03-to-panic-or-not-to-panic.html),
section "Examples, Prototype Code, and Tests").

Production code may also know an invariant the compiler cannot prove. Use `expect`
there and state the invariant in its message
([To panic! or Not to panic!](https://doc.rust-lang.org/book/ch09-03-to-panic-or-not-to-panic.html),
section "When You Have More Information Than the Compiler").

```rust
let home: IpAddr = "127.0.0.1"
    .parse()
    .expect("Hardcoded IP address should be valid");
```

Write the `expect` message as the assertion that must hold. Use `Result` or `Option`
when failure or absence is a legitimate state; reserve `expect` for a proven invariant
whose violation is a programming error. This is **fix the design, not the symptom**.

## 9. Encode invalid states out of existence

This is the most important section in this guide, and it is the Rust expression of
the core philosophy **fix the design, not the symptom**.

Scattering validation checks through every function is verbose
and annoying, and Rust's type system can do those checks for you. A parameter
typed `u32` cannot be negative. A parameter typed `T` rather than `Option<T>` cannot
be absent, so the function body has one case instead of two, and code trying to pass
nothing will not compile.

Take it one step further with a custom type whose constructor is the only way in
([To panic! or Not to panic!](https://doc.rust-lang.org/book/ch09-03-to-panic-or-not-to-panic.html),
section "Custom Types for Validation"):

```rust
pub struct Guess {
    value: i32,
}

impl Guess {
    /// Returns None when the value is outside 1..=100.
    pub fn new(value: i32) -> Option<Guess> {
        if !(1..=100).contains(&value) {
            return None;
        }
        Some(Guess { value })
    }

    pub fn value(&self) -> i32 {
        self.value
    }
}
```

The field is private, so no code outside this module can construct or mutate a
`Guess` that is out of range. Every downstream function taking a `Guess` gets the
range invariant for free and never re-checks it. This is the newtype pattern, which
also serves type safety and abstraction
([Advanced Types](https://doc.rust-lang.org/book/ch20-03-advanced-types.html)) and lets you
implement external traits on external types
([Advanced Traits](https://doc.rust-lang.org/book/ch20-02-advanced-traits.html)).

Apply it whenever a bare primitive is carrying a rule:

- `UserId(u64)` rather than a `u64` that must not be zero.
- `Email(String)` rather than a `String` that must contain an at-sign.
- `NonEmpty<Vec<T>>` rather than a `Vec<T>` that callers must remember to check.

Good rule:

> If two call sites re-check the same condition, the condition belongs in a type.

The payoff is **design for adaptability**. When the rule changes, it changes in one
constructor, and the compiler finds every construction site.

## 10. Ownership, traits, and concurrency

Ownership is the design surface, not an obstacle to route around.

- Borrow by default. Take `&T` when you only read, `&mut T` when you mutate, and `T`
  when the function genuinely consumes the value.
- Prefer slice parameters over owned collections: `&str` over `&String`, `&[T]` over
  `&Vec<T>`. This accepts strictly more callers at no cost
  ([The Slice Type](https://doc.rust-lang.org/book/ch04-03-slices.html)).
- The rules of references still bind everywhere: at any time you may have either one
  mutable reference or any number of immutable ones, and references must always be
  valid ([References and Borrowing](https://doc.rust-lang.org/book/ch04-02-references-and-borrowing.html)).
- Reach for `clone()` deliberately, with a reason. A clone that exists only to escape
  a borrow error is a symptom, and the fix is usually to shorten the borrow, split the
  struct, or restructure the call. A clone that exists because two owners genuinely
  need the data is fine. Say which one it is when it is not obvious.
- `Rc<T>` for shared ownership on one thread, `Arc<T>` across threads, and interior
  mutability (`RefCell<T>`, `Mutex<T>`) only when shared mutation is genuinely
  required
  ([Rc, the Reference Counted Smart Pointer](https://doc.rust-lang.org/book/ch15-04-rc.html),
  [RefCell and the Interior Mutability Pattern](https://doc.rust-lang.org/book/ch15-05-interior-mutability.html),
  [Shared-State Concurrency](https://doc.rust-lang.org/book/ch16-03-shared-state.html)).
  Each carries runtime cost and additional invariants, so make the ownership reason
  visible in the type or API.
- Rely on lifetime elision for relationships the compiler already understands. The
  three elision rules cover the overwhelming majority of function signatures
  ([Validating References with Lifetimes](https://doc.rust-lang.org/book/ch10-03-lifetime-syntax.html)).
  Write explicit lifetimes when a public signature relates returned or stored
  references to inputs, or when elision is ambiguous. Treat the annotation as a
  design statement about which value owns the data.

### Traits and generics

- Use an enum for a closed set of domain alternatives and a trait when implementations
  should remain open to other modules or crates.
- Use generics for static dispatch and trait objects for runtime-selected,
  heterogeneous implementations. Choose from the caller's ownership and extension
  needs rather than from object-oriented habit.
- Keep simple trait bounds beside the generic parameter. Use a `where` clause when
  several bounds or lifetime relationships read more clearly there, and expose only
  the capabilities the function actually requires.

### Async task ownership

- Move task-owned values into `tokio::spawn` and retain the `JoinHandle` whenever the
  result, panic, or cancellation matters to the caller.
- Make task ownership, shutdown, cancellation, and timeouts visible at the API
  boundary. Use bounded channels when queued work needs backpressure.
- Let a dedicated task own a resource that requires asynchronous mutation, and send
  it commands through channels
  ([Tokio channels](https://tokio.rs/tokio/tutorial/channels)).
- Keep synchronous lock guards scoped outside `.await`. Use an async mutex when the
  protected operation itself must span `.await`
  ([Tokio shared state](https://tokio.rs/tokio/tutorial/shared-state)).

## 11. Prefer iterators, `match`, and `let...else`

- Prefer iterator adapters over manual index loops. They remove the index-arithmetic
  bug class and read as a pipeline
  ([Processing a Series of Items with Iterators](https://doc.rust-lang.org/book/ch13-02-iterators.html)).
  A published benchmark of loops against iterators finds iterators fast enough that
  clarity should decide
  ([Performance in Loops vs. Iterators](https://doc.rust-lang.org/book/ch13-04-performance.html)).
  If a hot path
  matters, follow the core philosophy **use the scientific method** and measure with a
  benchmark rather than assuming.
- Keep adapter chains readable. A chain doing real work across several lines should be
  a named function, the same judgment `docs/PYTHON_STYLE.md` applies to `lambda`.
- `match` is exhaustive, and that is a feature. When you add an enum variant, the
  compiler shows you every site that must change. Use a catch-all `_` arm only when
  the remaining variants truly are interchangeable; a `_` arm silently absorbs every
  future variant and forfeits the exhaustiveness guarantee
  ([The match Control Flow Construct](https://doc.rust-lang.org/book/ch06-02-match.html),
  sections "Matches Are Exhaustive" and "Catch-All Patterns and the _ Placeholder").
- Use `let...else` to keep the happy path unindented
  ([Concise Control Flow with if let and let...else](https://doc.rust-lang.org/book/ch06-03-if-let.html)).
  This is the direct Rust answer to rightward drift, which the
  official style guide lists as a specific concern.[^style-principles]

```rust
let Some(config) = load_optional_config()? else {
    return Ok(Defaults::new());
};
// config is in scope, unindented, for the rest of the function.
```

- Use `if let` when one variant matters and the rest do not need naming.

## 12. Keep `unsafe` small, wrapped, and checked

`unsafe` marks operations whose soundness the compiler cannot prove, including raw
pointer access, unsafe calls, mutable or external statics, unions, target features,
unsafe trait implementations, unsafe attributes, and `extern` declarations. The 2024
edition requires `unsafe extern` blocks. All other type, ownership, and borrow checks
remain active
([Unsafety](https://doc.rust-lang.org/reference/unsafety.html),
[Unsafe extern blocks](https://doc.rust-lang.org/edition-guide/rust-2024/unsafe-extern.html)).

Repo policy:

- Use safe Rust by default. Introduce `unsafe` only at a boundary whose invariant
  requires it.
- When it is needed, keep the blocks small. The reasoning is practical: because
  memory-safety errors must be inside an `unsafe` block, small blocks make the search
  space small.
- Wrap `unsafe` in a safe abstraction that exposes a safe API, so `unsafe` does not
  leak into every call site. Parts of the standard library are exactly this: audited
  safe abstractions over unsafe code.
- Write a `// SAFETY:` comment above every `unsafe` block stating the invariant that
  makes it sound. An `unsafe` block whose invariant nobody wrote down cannot be
  reviewed.
- Run supported tests with Miri, the official interpreter for detecting many forms of
  undefined behavior. Use a sanitizer or target-specific boundary test when Miri
  cannot execute the platform or foreign call
  ([Unsafe Rust](https://doc.rust-lang.org/book/ch20-01-unsafe-rust.html), section
  "Using Miri to Check Unsafe Code").

```bash
rustup +nightly component add miri
cargo +nightly miri test
```

- For anything beyond a small wrapper, read the Rustonomicon, the official guide to
  unsafe Rust.[^nomicon]

Good rule:

> Every `unsafe` block has a written invariant, a safe wrapper, and executable proof
> through Miri, a sanitizer, or the real boundary.

### FFI boundaries

- Keep the ABI adapter narrow and typed. Convert pointers, buffers, handles, and
  foreign errors at the edge; keep domain logic in safe Rust.
- Document who allocates, owns, mutates, and frees each foreign value, plus its valid
  lifetime, thread, layout, and nullability contract.
- Test the safe wrapper and the foreign caller against the same ownership and error
  contract. Python extension crates follow [RUST_PYO3_STYLE.md](RUST_PYO3_STYLE.md);
  browser and WebAssembly crates follow [RUST_WASM_STYLE.md](RUST_WASM_STYLE.md).

## 13. Document the public API

Documentation comments use `///` before the item, or `//!` inside the item for
module- and crate-level docs, and support Markdown. `cargo doc` runs rustdoc and
writes HTML into `target/doc` (the Rust book,
[Publishing a Crate to Crates.io](https://doc.rust-lang.org/book/ch14-02-publishing-to-crates-io.html),
section "Making Useful Documentation Comments").

```rust
/// Adds one to the number given.
///
/// # Examples
///
/// ```
/// let answer = my_crate::add_one(5);
/// assert_eq!(6, answer);
/// ```
pub fn add_one(x: i32) -> i32 {
    x + 1
}
```

In practice:

- Document every `pub` item. A public item without docs is an undocumented promise.
- Use the conventional sections: `# Examples`, `# Errors` for what the `Err` variants
  mean, `# Panics` for the contract whose violation panics, and `# Safety` for
  `unsafe` functions. Section 6 requires the panic contract to be documented; this is
  where it goes.
- Put copyable, runnable examples on the crate front page and on public workflows
  whose use, errors, or safety contract benefits from demonstration. Reuse a workflow
  example across related types rather than repeating it on every field or variant.
- Code blocks in doc comments are compiled and run by `cargo test`, keeping examples
  synchronized with the public API.
- `cargo doc --open` is the fastest review of whether the public API reads well from
  the outside.

This is the same instinct as the `docs/REPO_STYLE.md` documentation rules: keep docs
current, and remove or replace stale ones. Rust just gives you a test runner for them.

## 14. Rust test layout

The Rust community splits tests into two categories. Unit tests are small and focused,
test one module in isolation, and can reach private interfaces. Integration tests are
entirely external to the library, use only the public API, and exercise several
modules together
([Test Organization](https://doc.rust-lang.org/book/ch11-03-test-organization.html)).

**Unit tests** live in the same file as the code, in a module named `tests` annotated
`#[cfg(test)]`. The attribute means the test code compiles only under `cargo test`,
not `cargo build`, which saves compile time and keeps tests out of the shipped
artifact.

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn adds_two() {
        assert_eq!(add_two(2), 4);
    }
}
```

**Integration tests** live in a top-level `tests/` directory next to `src/`. Cargo
compiles each file there as its own crate, and they need no `#[cfg(test)]` because
they are already outside the build. Shared helpers go in
`tests/common/mod.rs` so Cargo does not treat them as a test crate.

Note the deliberate parallel with `docs/E2E_TESTS.md`: `tests/` at the repo root is
the slow outer tier there too. In a Rust repo, `cargo test` runs unit tests,
integration tests, and doc tests in one pass, so keep individual tests fast enough
that the whole pass stays worth running.

Testing guidance that carries over from `docs/PYTEST_STYLE.md`: assert on behavior.
Assert on a collection size, default, or function name only when that exact fact is
the user-visible contract under test.

Match the executable proof to the boundary:

- Ownership, lifetime, and trait changes compile the intended caller and test the
  valid value flow.
- `Result` and CLI tests assert returned errors, stdout, stderr, and exit status.
- Tokio tests use deterministic synchronization, bounded timeouts, and test-owned
  channels or clocks to verify results and cancellation.
- Unsafe and FFI tests exercise the safe wrapper invariant through the foreign caller
  and add Miri or a sanitizer when supported.
- Language-binding tests build the shared artifact and exercise it from the foreign
  caller. PyO3 projects follow [RUST_PYO3_STYLE.md](RUST_PYO3_STYLE.md).
- WebAssembly tests build the target artifact and exercise it through the browser or
  JavaScript-facing boundary. WebAssembly projects follow
  [RUST_WASM_STYLE.md](RUST_WASM_STYLE.md).
- Performance work records the baseline command, input shape, machine constraints,
  and measured wall time, throughput, allocations, or profile evidence.

## 15. Keep binary roots thin

When `main` starts growing, split the program into a binary crate and a library crate.
Move reusable behavior into focused library modules. Let `lib.rs` declare those
modules and re-export the intended API, including a `run` function when that fits the
application. Keep `main.rs` as a small call into a descriptive command or application
module
([Refactoring to Improve Modularity and Error Handling](https://doc.rust-lang.org/book/ch12-03-improving-error-handling-and-modularity.html)).

The library split makes reusable logic easy to unit test, while a command-level
integration test exercises the compiled binary's arguments, stdout, stderr, and exit
status. What remains in `main` is short wiring that is easy to review. This matches
the `docs/PYTHON_STYLE.md` rule that `main()` is a backbone calling single-task
subfunctions.

Send errors to standard error, not standard output, using `eprintln!`. A CLI whose
error text lands in a redirected output file is a broken CLI
([Writing Error Messages to Standard Error](https://doc.rust-lang.org/book/ch12-06-writing-to-stderr-instead-of-stdout.html)).

```rust
fn main() {
    let config = Config::build(std::env::args()).unwrap_or_else(|err| {
        eprintln!("Problem parsing arguments: {err}");
        std::process::exit(1);
    });

    if let Err(e) = my_crate::run(config) {
        eprintln!("Application error: {e}");
        std::process::exit(1);
    }
}
```

Use a typed `clap` argument structure for a nontrivial CLI. Validate inputs before
calling the domain core, keep stdout stable for successful results, write actionable
diagnostics to stderr, and assign explicit exit behavior. Argparse minimalism from
`docs/PYTHON_STYLE.md` applies to the interface: add a flag when users change it
between runs; keep internal timeouts, buffer sizes, and retry counts in the design.

## 16. Toolchain and dependencies

**Edition and compiler.** Use the current edition for new crates and migrate existing
crates with `cargo fix --edition`. Set the latest stable compiler as the minimum
supported Rust version:

```toml
[package]
rust-version = "1.97.1"
```

`rust-version` is a bare minimum version; Cargo rejects range operators in this
field. Refresh it with each stable toolchain update. Workspaces declare it once under
`[workspace.package]` and use `rust-version.workspace = true` in member packages
([Rust version](https://doc.rust-lang.org/cargo/reference/rust-version.html),
[Editions](https://doc.rust-lang.org/book/appendix-05-editions.html)).

**Profiles.** Use Cargo's standard `dev` and `release` profiles. Tune `[profile.*]`
only from a measured need, per **use the scientific method**
([Release profiles](https://doc.rust-lang.org/book/ch14-01-release-profiles.html)).

**Dependencies.** Use the latest stable release available for every direct
dependency. Advance major, minor, and patch components whenever a newer stable
release exists. Confirm the current crate API and feature flags in `docs.rs` or the
crate's official guide. Write each direct dependency in `Cargo.toml` with the one
repository-wide form selected by the manager:

| Form | Example | Contract |
| --- | --- | --- |
| Explicit floor | `version = ">=0.29.0"` | Latest known version is the minimum; newer versions remain eligible |
| Wildcard | `version = "*"` | Every stable version remains eligible |

Both forms intentionally allow future major, minor, and patch releases. Application
repositories use `Cargo.lock` as the exact tested resolution between refreshes in
either mode. A future package intended for crates.io uses the explicit-floor form
because crates.io rejects bare wildcard requirements. Reserve an exact `=...`
requirement for a temporary upstream constraint, and record its reason and removal
condition
([Version requirement syntax](https://doc.rust-lang.org/cargo/reference/specifying-dependencies.html#version-requirement-syntax)).

**Refresh sequence.** `Cargo.toml` describes compatible ranges; `Cargo.lock` records
the exact resolved graph. Keep both current:

1. Apply the manager-selected repository form consistently. Refresh each `>=LATEST`
   floor to the current latest stable release; wildcard requirements stay `*`.
2. Run `cargo update`, then review the resolved versions, release notes, and features.
3. Run `cargo check`, `cargo test`, and `cargo clippy -- -D warnings`.

Repeat the sequence whenever dependencies change and immediately for a reported
vulnerability. `cargo update` honors the manifest ranges, so the manifest must first
express the selected latest-first policy
([Cargo.toml versus Cargo.lock](https://doc.rust-lang.org/cargo/guide/cargo-toml-vs-cargo-lock.html),
[cargo update](https://doc.rust-lang.org/cargo/commands/cargo-update.html)).

**Derives.** Prefer the standard derivable traits over hand-written impls where they
fit: `Debug` for programmer output, `PartialEq` and `Eq`, `PartialOrd` and `Ord`,
`Clone` and `Copy`, `Hash`, and `Default`
([Appendix C: Derivable Traits](https://doc.rust-lang.org/book/appendix-03-derivable-traits.html)).
A hand-written impl of one of
these should have a reason, because a derive cannot drift out of sync with the fields.

## 17. Rust completion checklist

- `cargo fmt --check`, `cargo check`, `cargo test`, and
  `cargo clippy -- -D warnings` all pass for the affected package or workspace.
- The owning crate and module, public callers, features, target, value flow, and error
  contract are explicit.
- Formatting matches rustfmt output.
- Naming follows RFC 430, including `as_` / `to_` / `into_` cost prefixes.
- Every tracked authored `.rs` file contains at most 999 physical lines; canonical
  crate roots and entry points stay concise stubs for descriptive owning modules.
- Generic filenames contain routing declarations and entry wiring; descriptive files
  own functions, types, implementations, algorithms, data, examples, and behavior tests.
- Modules are private by default and the tree is shallow.
- `lib.rs` shapes the public API with `pub use`; owning modules contain the logic.
- Fallible functions return `Result`; `?` propagates; one boundary handles.
- Library errors are a concrete enum; binary errors may be opaque.
- Every `unwrap` or `expect` outside tests has a documented invariant.
- Invariants live in types, not in repeated runtime checks.
- Borrows are preferred to clones, and each clone has a reason.
- `match` arms are exhaustive; `_` is used only where future variants are equivalent.
- Safe Rust is the default; each `unsafe` block is small, wrapped,
  `// SAFETY:`-commented, and Miri-checked.
- Every `pub` item has documentation; the crate front page and non-obvious public
  workflows have runnable examples.
- Unit tests are `#[cfg(test)]`; integration tests are in `tests/`.
- The selected test oracle exercises the real CLI, async, unsafe, FFI, binding, or
  performance boundary when one is affected.
- `main` is thin, logic is in the library, and errors go to stderr.
- The edition is current and `rust-version = "1.97.1"` states the toolchain floor.
- Direct dependencies consistently use the manager-selected repository form: `*` or
  `>=LATEST`, where `LATEST` is the stable version available at refresh time.
- `Cargo.lock` resolves the current reviewed manifest and passes dependency security checks.

## References

Every source cited here is freely readable online. Three carry most of the weight:

- [The Rust Programming Language](https://doc.rust-lang.org/book/), the official book,
  linked by chapter page. Section names are quoted so the passage is easy to find on the
  page; the guidance above is paraphrased.
- [The Rust Style Guide](https://doc.rust-lang.org/stable/style-guide/), the normative
  source for formatting.
- [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/), the normative
  source for public API design and naming.

[^style-principles]: The Rust Style Guide, "Guiding principles and rationale." https://doc.rust-lang.org/stable/style-guide/principles.html
[^style-index]: The Rust Style Guide, formatting conventions (4 spaces, no tabs, 100-character maximum width). https://doc.rust-lang.org/stable/style-guide/
[^api-naming]: Rust API Guidelines, "Naming" (RFC 430 casing conventions and conversion prefixes). https://rust-lang.github.io/api-guidelines/naming.html
[^book-appd]: The Rust Programming Language, Appendix D, "Useful Development Tools" (rustfmt, rustfix, Clippy, rust-analyzer). https://doc.rust-lang.org/book/appendix-04-useful-development-tools.html
[^nomicon]: The Rustonomicon, the official guide to unsafe Rust. https://doc.rust-lang.org/nomicon/
