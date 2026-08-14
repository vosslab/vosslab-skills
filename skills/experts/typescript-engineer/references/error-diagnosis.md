# Error diagnosis

Use this file first when TypeScript reports compiler errors.

## Workflow

1. Run the focused type check, preferably `tsc --noEmit`.
2. Capture the exact diagnostic, including `ts(...)` code when present.
3. Identify whether the problem is assignability, inference, missing narrowing, overload mismatch,
   circular reference, or configuration.
4. If it is configuration or module resolution, stop and say this skill is not the right tool.
5. Load the matching rule file for the category.
6. Make the smallest type-level change that preserves runtime behavior.
7. Re-run the type check.

## Common categories

- Not assignable: compare the expected type, actual type, and where widening occurred.
- Possibly undefined or null: narrow earlier or make optionality explicit.
- Excess property: check whether the object is intended to be exact or the target type is wrong.
- Circular reference: break recursive aliases with interfaces, named helpers, or simpler recursion.
- Overload mismatch: inspect each overload and the implementation signature.

## Review check

- Do not patch the symptom with `as any`.
- Explain why the compiler was right or why the type model was too narrow.
