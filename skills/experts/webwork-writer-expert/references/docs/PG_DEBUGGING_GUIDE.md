# PG debugging guide

Use these steps and error lookups when rendering a PG or PGML problem.
For detailed failure examples, see [PG_COMMON_PITFALLS.md](PG_COMMON_PITFALLS.md).

## Debugging Strategies

### Strategy 1: Check Line Numbers

When variables seem empty or undefined:
1. Find where variable is USED (grep for `$var_name`)
2. Find where variable is DEFINED (`$var_name = ...`)
3. Compare line numbers - definition must come first!

### Strategy 2: Isolate PGML Errors

When getting `'*' was not closed` or similar:
1. Comment out half the PGML block
2. Test - does error persist?
3. Binary search to find problematic line
4. Check for `*`, `**`, or `_` near variables

### Strategy 3: Test with Minimal Example

Create minimal test file:
```perl
# test.pgml
DOCUMENT();
loadMacros("PGstandard.pl", "PGML.pl");

$var = "test";

BEGIN_PGML
Test: [$var]
END_PGML

ENDDOCUMENT();
```

Add complexity incrementally until problem reproduces.

### Strategy 4: Check Renderer Output

Use `-r` flag to see actual HTML:
```bash
python3 lint_pg_via_renderer_api.py -i file.pgml -r > output.html
```

Then inspect:
- Are canvas elements present? (`grep '<canvas'`)
- Is HTML escaped? (look for `&lt;` instead of `<`)
- Are there JavaScript errors in console?

### Strategy 5: Grep for Patterns

Common checks:
```bash
# Find all variable definitions
grep '^\$' file.pgml

# Find PGML blocks
grep -n 'BEGIN_PGML\|END_PGML' file.pgml

# Find answer rules
grep 'ANS\|ans_rule' file.pgml

# Check for problematic asterisks
grep '\*\[' file.pgml
```

---

## Prevention Checklist

Before committing a new PG file:

- [ ] Variables defined before use (check line numbers)
- [ ] No `my` on variables referenced in PGML (`$rb`, `$popup`, display vars)
- [ ] No `\@` or `\%` references -- use `~~@`, `[@array]`, `~~%`, or `{%hash}`
- [ ] No `use` statements -- use `loadMacros()` for PG macros
- [ ] No `*` or `**` immediately around `[$variables]` in PGML
- [ ] HTML variables use `[$var]*` syntax (with the asterisk)
- [ ] No Perl loops inside `BEGIN_TEXT...END_TEXT` blocks
- [ ] Hash keys sorted before random selection
- [ ] Shuffling happens AFTER all items are defined
- [ ] `ans_rule()` created BEFORE `ANS()` call
- [ ] SMILES strings validated with Python RDKit
- [ ] Tested with renderer (`-r` flag) to verify HTML output
- [ ] HTML entities (`&deg;`, `&ndash;`, etc.) in Perl vars with `[$var]*`, not bare in PGML
- [ ] No PGML parsing errors in renderer warnings

---

## Quick Reference: Common Errors

| Error Message | Likely Cause | Fix |
|---------------|--------------|-----|
| `'*' was not closed` | Asterisks around variable in PGML | Remove `*` or use `**` (bold) |
| `'**' was not closed` | Bold markers around variable | Remove bold or move variable out |
| Empty output / no canvas | Variable used before defined | Move definition before usage |
| HTML shown literally | Missing `*` in `[$var]*` | Add asterisk: `[$var]*` |
| Answer always wrong | Answer field name mismatch | Use `ans_rule()` before `ANS()` |
| RadioButtons renders as text input | `my $rb = RadioButtons(...)` | Remove `my`: `$rb = RadioButtons(...)` |
| `Not an ARRAY reference` | `\@array` backslash ref in PG | Use `~~@array` or `[@array]` |
| `Not a HASH reference` | `\%hash` backslash ref in PG | Use `~~%hash` or `{%hash}` |
| `'require' trapped by operation mask` | `use Module` in PG source | Use `loadMacros()` or PG built-ins |
| `'eval "string"' trapped` | `eval $code` in PG | Restructure to avoid string eval |
| `'open' trapped by operation mask` | File I/O in PG | Not possible; use PG data macros |
| Variable shows empty in PGML | `my $var` instead of `$var` | Remove `my` for PGML-visible vars |
| Random order changes | Hash keys not sorted | Sort keys before selection |
| `'sort' trapped by operation mask` | `sort { ... }` in PG | Hardcode sorted order or manual insertion sort |
| `&amp;deg;` shown literally | `&deg;` directly in PGML text | Use `$var = "37&deg;C"` with `[$var]*` |
| Curves cover x-axis line | PGgraphmacros draws functions twice | Accept it; do not clamp values |
| Auto-labels on graph axes | `grid`/`ticks` options in `init_graph` | Use manual `v_grid`/`h_grid` + labels |
