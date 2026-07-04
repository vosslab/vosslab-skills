// @ts-check
import eslint from "@eslint/js";
import tseslint from "typescript-eslint";
import globals from "globals";
import { fileURLToPath } from "node:url";
import path from "node:path";

// Consumer-owned local overrides. Ships once via the noexist bucket and is never
// overwritten by propagation, so repo-specific config (extra browser-context
// globs, per-tool globals, local rule tweaks) survives. Default export is [].
import localConfig from "./eslint.config.local.js";

// Avoid Node-version coupling: import.meta.dirname needs Node >=20.11.
// Use fileURLToPath + path.dirname to stay compatible with Node 18 LTS.
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export default tseslint.config(
  eslint.configs.recommended,
  ...tseslint.configs.recommendedTypeChecked,
  {
    // TypeScript source files (.ts/.tsx/.mts/.cts) -- full type-checked ruleset.
    // project list pins both tsconfigs so .ts files under src/, tests/, and tools/
    // all have type info available to typescript-eslint.
    files: ["**/*.{ts,tsx,mts,cts}"],
    languageOptions: {
      parserOptions: {
        project: ["./tsconfig.json", "./tsconfig.lint.json"],
        tsconfigRootDir: __dirname,
      },
      globals: { ...globals.browser, ...globals.node },
    },
    rules: {
      "@typescript-eslint/no-explicit-any": "error",
      "@typescript-eslint/no-unused-vars": "error",
      "@typescript-eslint/explicit-function-return-type": "error",
      "@typescript-eslint/no-floating-promises": "error",
      "no-var": "error",
      "prefer-const": "error",
      "no-implicit-coercion": "warn",
      eqeqeq: "error",
      "no-throw-literal": "error",
      "no-console": "warn",
    },
  },
  {
    // Plain JS / MJS / CJS files (eslint.config.js, tests/playwright/*.mjs helpers,
    // tools/*.mjs CLI utilities). These are intentionally NOT in any tsconfig project,
    // so typescript-eslint's type-checked rules would error on them. disableTypeChecked
    // turns those rules off while keeping the recommended non-typed rules active.
    files: ["**/*.{js,mjs,cjs}"],
    ...tseslint.configs.disableTypeChecked,
    languageOptions: {
      globals: { ...globals.node },
    },
  },
  {
    // Browser-context test runners: Playwright (tests/playwright/**) and non-browser
    // e2e (tests/e2e/**) .mjs files embed browser callbacks (page.evaluate) that
    // reference browser globals (window, document, getComputedStyle, etc.). Supply
    // globals.browser as readonly so no-undef does not flag them. Scoped to the test
    // trees only; node-only tools keep no-undef so real bugs still surface. Repo-specific
    // browser-context tool files belong in eslint.config.local.js, not here.
    files: ["tests/playwright/**", "tests/e2e/**"],
    languageOptions: {
      globals: { ...globals.browser },
    },
  },
  {
    // Node unit tests written in TypeScript (tests/**/*.{ts,mts}) drive the
    // node:test runner, whose test()/describe()/it() calls return promises the
    // runner awaits internally, so an unawaited call is the intended usage, not
    // a floating-promise bug. Tests also log progress freely. Relax these two
    // rules for the TypeScript test tree so node:test TS tests lint as tests,
    // not as production async code. Source under src/ and tools/ stays strict.
    // The canonical .mjs test path already skips typed rules via the
    // disableTypeChecked block above; this block gives the .ts test variant the
    // same treatment.
    files: ["tests/**/*.{ts,mts}"],
    rules: {
      "@typescript-eslint/no-floating-promises": "off",
      "no-console": "off",
    },
  },
  {
    // Repo-wide: allow underscore-prefixed identifiers to mark intentionally unused
    // args, vars, and caught errors. A visible, deliberate opt-out marker, not a silent
    // default. Overrides the no-unused-vars setting above for every file.
    rules: {
      "@typescript-eslint/no-unused-vars": [
        "error",
        {
          argsIgnorePattern: "^_",
          varsIgnorePattern: "^_",
          caughtErrorsIgnorePattern: "^_",
        },
      ],
    },
  },
  {
    // OTHER_REPOS/ is the universal sibling-repo checkout dir (gitignored repo-wide);
    // never lint sibling repos checked out there.
    ignores: ["dist/**", "node_modules/**", "OTHER_REPOS/**"],
  },
  // Consumer-owned overrides last so they can refine or override the canonical config.
  ...localConfig,
);
