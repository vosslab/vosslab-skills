// @ts-check
import eslint from "@eslint/js";
import tseslint from "typescript-eslint";
import globals from "globals";
import { fileURLToPath } from "node:url";
import path from "node:path";

// Avoid Node-version coupling: import.meta.dirname needs Node >=20.11.
// Use fileURLToPath + path.dirname to stay compatible with Node 18 LTS.
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export default tseslint.config(
	eslint.configs.recommended,
	...tseslint.configs.recommendedTypeChecked,
	{
		languageOptions: {
			parserOptions: {
				project: ["./tsconfig.json"],
				tsconfigRootDir: __dirname,
			},
			globals: { ...globals.browser, ...globals.node },
		},
		rules: {
			"@typescript-eslint/no-explicit-any": "error",
			"@typescript-eslint/no-unused-vars": "error",
			"@typescript-eslint/explicit-function-return-type": "warn",
			"@typescript-eslint/no-floating-promises": "error",
			"no-var": "error",
			"prefer-const": "error",
			"no-implicit-coercion": "warn",
			"eqeqeq": "error",
			"no-throw-literal": "error",
			"no-console": "warn",
		},
	},
	{
		ignores: ["dist/**", "node_modules/**", "*.config.js", "*.config.mjs"],
	},
);
