# Rust PyO3 style guide

Use this guide for Rust applications that expose a native Python module or embed
Python. Core Rust code follows [RUST_STYLE.md](RUST_STYLE.md); this document owns the
Python boundary, build shape, exceptions, interpreter-bound values, and integration
proof.

PyO3 APIs and packaging behavior move faster than Rust language concepts. Confirm
current names, features, Python support, and platform behavior in the
[PyO3 user guide](https://pyo3.rs/main/) before changing an adapter.

## Design the Python boundary

- Choose the direction first: a Python extension imported by Python, or a Rust
  application that embeds Python. The build and interpreter ownership differ.
- Keep parsing, geometry, scientific computation, and other domain logic in safe,
  Python-independent Rust. Give that core ordinary Rust types and concrete `Result`
  errors.
- Keep `#[pymodule]`, `#[pyfunction]`, and `#[pymethods]` adapters thin. Extract Python
  inputs once, call the Rust core, and convert the result once.
- Make the extension module name agree across `[lib].name`, `#[pymodule]`, and the
  Python import. Python loads the module initializer by that name.
- Name the public Python functions, classes, accepted values, returned values,
  exceptions, supported Python versions, target triples, and ownership transfer before
  implementation.
- Add Python dependencies to the adapter crate rather than to independent domain
  crates. This preserves a reusable and directly testable Rust core.

## Package and build shape

For an extension module, use `cdylib` so Python can load the shared library. Add
`rlib` when Rust tests, binaries, or workspace members also import the crate:

```toml
[lib]
crate-type = ["cdylib", "rlib"]
```

Apply the manager-selected `*` or `>=LATEST` dependency form from
[RUST_STYLE.md](RUST_STYLE.md#16-toolchain-and-dependencies). Keep `pyo3`,
`pyo3-build-config`, and `pyo3-ffi` on the current stable release whenever they are
direct dependencies in the same project.

Use current maturin guidance to configure extension linking and build the importable
artifact. Maturin supplies the platform-specific extension configuration; use the
current PyO3 FAQ guidance when a workspace needs an additional Rust-linkable crate
type
([PyO3 building and distribution](https://pyo3.rs/main/building-and-distribution)).

For embedding, select and test the intended Python installation. PyO3 configures
linking from that interpreter; an embedded application needs its shared library.
Use `auto-initialize` when the application expects PyO3 to start the interpreter on
its first `Python::attach` call. Inspect the selected configuration with
`PYO3_PRINT_CONFIG=1` when a build or target is surprising.

Choose the Python ABI policy deliberately:

- Use version-specific wheels when the adapter needs the full API of each supported
  interpreter.
- Use the current `abi3` or `abi3t` guidance when one wheel should cover several
  Python versions or free-threaded builds.
- Build and import the artifact on every supported operating-system, architecture,
  Python-version, and ABI combination.

Treat the current PyO3 build guide as the authority for linker settings, wheel tags,
cross-compilation, and supported interpreter versions.

## Shape the Python API

- Give Python users Python-shaped names, signatures, defaults, docstrings, and
  exceptions while keeping the Rust core idiomatic.
- Keep `Bound<'py, T>` values and Python borrows inside their `Python::attach` scope.
  Use an owned `Py<T>` handle only when a Python object must outlive that attachment.
- Convert collections and buffers at the boundary. Measure conversion and copying
  before adding zero-copy or unsafe paths.
- Keep Python callbacks and object access in the adapter. Pass ordinary owned values
  or safe borrows into the domain core.
- Document mutation, aliasing, thread, and lifetime behavior for every exposed class
  that holds Rust state.

## Translate errors for Python

Let the Rust core return its concrete domain error. Convert that error once in the
PyO3 adapter to a meaningful Python exception through `PyResult<T>`. Implement the
conversion beside the adapter when `From<DomainError> for PyErr` makes that mapping
reusable. A `PyResult` containing `Err(PyErr)` becomes a raised exception when it
crosses back into Python
([PyO3 error handling](https://pyo3.rs/main/function/error-handling)).

Map stable failure categories to stable Python exception classes. Include actionable
context while preserving the original Rust cause for diagnostics. Test the exception
class and the user-visible context through Python.

## Interpreter and task ownership

- Make the owner of the Python interpreter and each Python object explicit.
- Keep long-running, CPU-bound work in the Python-independent Rust core. Use the
  current PyO3 API to let other Python work proceed when the Rust operation does not
  access Python objects.
- Define thread-safety, cancellation, and shutdown behavior before combining PyO3
  with Tokio or native threads.
- Follow current PyO3 guidance for GIL-enabled, free-threaded, `abi3`, and `abi3t`
  interpreters; validate the actual interpreter variants the application supports.

## Prove the Python boundary

Run the Rust baseline from the owning package or workspace:

```bash
cargo fmt --check
cargo check
cargo test
cargo clippy -- -D warnings
```

Then build the real extension or embedded application and test it from Python:

- Import the compiled module by its shipped name.
- Exercise public functions and classes with representative valid inputs.
- Exercise invalid inputs and assert the Python exception class and useful context.
- Verify numeric values, strings, collections, buffers, and object lifetimes after
  crossing the language boundary.
- Run a clean package-install and import smoke test for every supported wheel target.
- Measure representative calls when performance motivates the Rust boundary. Record
  input shape, conversion cost, wall time, and throughput.

Rust-only unit tests prove the core. The Python integration path proves that module
initialization, linking, conversion, exceptions, and packaging work for the caller.

## PyO3 completion checklist

- The project is explicitly an extension module or an embedded-Python application.
- The extension import name agrees with `[lib].name` and `#[pymodule]`.
- Domain logic and domain errors remain Python-independent.
- The adapter converts inputs, outputs, and errors once at the boundary.
- `cdylib` produces the extension; `rlib` is present when Rust callers need it.
- Direct PyO3-family dependencies follow the repository's current version policy.
- The Python ABI and supported interpreter matrix are explicit.
- `Bound<'py, T>` values remain scoped; each owned `Py<T>` handle has a clear owner.
- Python exceptions preserve stable categories and actionable context.
- Rust baseline gates pass.
- The compiled artifact passes a Python import and behavior test.
