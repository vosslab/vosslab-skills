# Reference survey

This survey maps the four local book conversions to Rust/WebAssembly work. Use
the listed grep term to locate the sampled passage. Ratings reflect passage and
section depth; book titles and match counts provide secondary context.

## How to use this survey

- Start with a strong or partial row for conceptual guidance and examples.
- Check current tool, target, and browser API behavior in the official docs
  before making an implementation decision.
- Use the wasm-bindgen guide and MDN WebAssembly documentation for every thin
  row, especially where current browser and WASI behavior matters.

## Topic-to-reference map

### wasm-bindgen and wasm-pack

Coverage: strong.

- `references/local-only/Practical_WebAssembly_Fundamentals_of_WebAssembly_Programming_with_Rust-2022.md`, Chapter 7, "Installing wasm-bindgen". grep `wasm-bindgen`.
  The sampled passage explains generated bindings, supported output targets,
  debug sections, and size-related flags.
- `references/local-only/Practical_WebAssembly_Fundamentals_of_WebAssembly_Programming_with_Rust-2022.md`, Chapter 8, "Introducing wasm-pack". grep `wasm-pack`.
  The chapter gives a dedicated packaging route through webpack, Parcel, and
  the package commands.
- `references/local-only/Ultimate_Rust_for_Systems_Programming_with_Rust_and_WebAssembly-2024.md`, Chapter 15, "Building and Testing WebAssembly Modules". grep `wasm-pack`.
  The sampled commands build for the web and run a headless browser test.

### web-sys and js-sys interop

Coverage: strong.

- `references/local-only/Practical_WebAssembly_Fundamentals_of_WebAssembly_Programming_with_Rust-2022.md`, Chapter 9, "Calling the JavaScript API via WebAssembly". grep `js-sys`.
  The passage distinguishes ECMAScript bindings, adds the dependency, and
  calls a JavaScript function from Rust.
- `references/local-only/Practical_WebAssembly_Fundamentals_of_WebAssembly_Programming_with_Rust-2022.md`, Chapter 9, "Crossing the Boundary between Rust and WebAssembly". grep `web-sys`.
  The chapter summary identifies `web-sys` as the route to web APIs and pairs
  it with wasm-bindgen for exchanging complex objects.
- `references/local-only/Game_Development_with_Rust_and_WebAssembly-2022.md`, Chapter 1, "Hello WebAssembly". grep `web-sys`.
  The sampled setup explains that `web-sys` supplies browser bindings for
  Canvas and `requestAnimationFrame`.

### Browser and WASI targets

Coverage: partial for `wasm32-unknown-unknown`; thin for WASI.

- `references/local-only/Practical_WebAssembly_Fundamentals_of_WebAssembly_Programming_with_Rust-2022.md`, Chapter 7, "Converting Rust into WebAssembly via Cargo". grep `wasm32-unknown-unknown`.
  The passage builds a `cdylib`, explains the target's minimal footprint, and
  instantiates the generated module from browser JavaScript.
- `references/local-only/Ultimate_Rust_for_Systems_Programming_with_Rust_and_WebAssembly-2024.md`, Chapter 15, "Installing Rust and WebAssembly Toolchain". grep `wasm32-unknown-unknown`.
  The sampled setup uses rustup to add the browser target before a Rust Wasm
  project is created.
- `references/local-only/Ultimate_Rust_for_Systems_Programming_with_Rust_and_WebAssembly-2024.md`, Chapter 15, "Advantages of WebAssembly". grep `WASI`.
  WASI receives a one-paragraph definition as a platform interface, without a
  target setup, component model, or capability workflow. Use the wasm-bindgen
  guide for browser targets and MDN WebAssembly plus current WASI documentation
  for runtime and target choices.

### Canvas rendering and game loops

Coverage: strong.

- `references/local-only/Game_Development_with_Rust_and_WebAssembly-2022.md`, Chapter 1, "Drawing to the canvas". grep `canvas`.
  The sampled passage selects the Canvas 2D context, explains its browser role,
  and builds a Rust-rendered triangle.
- `references/local-only/Game_Development_with_Rust_and_WebAssembly-2022.md`, Chapter 3, "Creating a game loop". grep `game loop`.
  The chapter supplies a dedicated browser game architecture and integrates the
  loop with drawing and input.
- `references/local-only/Game_Development_with_Rust_and_WebAssembly-2022.md`, Chapter 3, "RequestAnimationFrame". grep `RequestAnimationFrame`.
  The sampled implementation binds a Rust closure to browser scheduling and
  leads into a fixed-time-step update design.

### Memory and allocation

Coverage: partial for linear memory and JavaScript sharing; thin for allocator
selection and production allocation measurement.

- `references/local-only/Practical_WebAssembly_Fundamentals_of_WebAssembly_Programming_with_Rust-2022.md`, Chapter 10, "Analyzing the memory model in the WebAssembly module". grep `linear memory`.
  The passage explains linear memory, mutable shared buffers, and the cost of
  crossing between JavaScript and WebAssembly.
- `references/local-only/Practical_WebAssembly_Fundamentals_of_WebAssembly_Programming_with_Rust-2022.md`, Chapter 10, "Creating a memory object in JavaScript to use in the Rust application". grep `alloc`.
  The example transfers a typed array through a pointer and length, then
  demonstrates explicit allocation and release responsibilities.
- `references/local-only/Game_Development_with_Rust_and_WebAssembly-2022.md`, Chapter 1, "The wee allocator". grep `wee allocator`.
  The book introduces a smaller allocator in a game template, but it does not
  establish current allocator tradeoffs or benchmark methods. Use the
  wasm-bindgen guide and MDN WebAssembly documentation for current guidance.

### Bundle size and load time

Coverage: partial for size reduction; thin for end-to-end load-time analysis.

- `references/local-only/Practical_WebAssembly_Fundamentals_of_WebAssembly_Programming_with_Rust-2022.md`, Chapter 10, "Minimizing the WebAssembly modules". grep `opt-level`.
  The sampled recipe measures a smaller binary after size optimization, LTO,
  `wee_alloc`, and `wasm-opt`.
- `references/local-only/Practical_WebAssembly_Fundamentals_of_WebAssembly_Programming_with_Rust-2022.md`, Chapter 10, "Analyzing the WebAssembly module with Twiggy". grep `Twiggy`.
  The passage introduces a code-size profiler and its call-graph-oriented
  commands for finding large functions and monomorphizations.
- `references/local-only/Game_Development_with_Rust_and_WebAssembly-2022.md`, Chapter 2, "Adding animation". grep `load times`.
  The passage compares asset-loading choices and their upfront-load tradeoff,
  but it does not teach a browser network or Web Vitals measurement workflow.
  Use MDN WebAssembly documentation for loading strategy and browser tooling.

### Browser debugging

Coverage: strong for a browser game; partial for general Wasm source debugging.

- `references/local-only/Game_Development_with_Rust_and_WebAssembly-2022.md`, Chapter 1, "Hello WebAssembly". grep `console_error_panic_hook`.
  The sampled setup routes Rust panics to the browser console and keeps the
  diagnostic dependency in a development configuration.
- `references/local-only/Game_Development_with_Rust_and_WebAssembly-2022.md`, Chapter 9, "Browser debugger". grep `browser debugger`.
  The passage records a Chrome Performance trace, identifies a dropped frame,
  and connects the trace to a DOM style recalculation.
- `references/local-only/Game_Development_with_Rust_and_WebAssembly-2022.md`, Chapter 9, "Checking memory". grep `Checking memory`.
  The chapter uses browser memory profiling to distinguish reclaimed heap use
  from unbounded growth. Use the wasm-bindgen guide and MDN WebAssembly
  documentation for current source maps and non-game debugging workflows.

## Weak-coverage routes

The corpus gives only thin treatment to WASI, current allocator decisions,
end-to-end loading metrics, browser source maps, and changing browser APIs.
Use the wasm-bindgen guide and MDN WebAssembly documentation as primary sources
for those decisions, then use the books for the stable concepts above.
