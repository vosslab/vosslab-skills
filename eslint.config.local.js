// eslint.config.local.js - consumer-owned ESLint overrides.
//
// Add repo-specific ESLint config objects here: extra browser-context globs,
// per-tool globals, or local rule tweaks. This file ships once via the noexist
// bucket and is never overwritten by propagation, so your edits survive. The
// canonical eslint.config.js imports and spreads this array AFTER its own config,
// so entries here refine or override the canonical rules.
//
// Example: give two named node tools browser globals for page.evaluate() use,
// without loosening no-undef across all tools.
//
//   import globals from "globals";
//   export default [
//     {
//       files: ["tools/scene_to_png.mjs", "tools/svg_picker/**"],
//       languageOptions: { globals: { ...globals.browser } },
//     },
//   ];
//
// Default: no local overrides.
export default [];
