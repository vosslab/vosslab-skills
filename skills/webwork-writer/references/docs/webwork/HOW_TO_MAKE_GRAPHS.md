# How to Make Graphs in WebWork PG/PGML

This guide covers creating graphs in PG/PGML problems using the local PG 2.17 renderer. It focuses on `PGgraphmacros.pl` for static display graphs, which is the recommended approach when the graph is informational (not an answer mechanism).

---

## Quick Decision: Which Graph Macro?

| Need | Macro | Notes |
|------|-------|-------|
| Display-only graph (titration curve, data plot) | `PGgraphmacros.pl` | GD bitmap image, no answer entry |
| Student clicks/draws on graph | `parserGraphTool.pl` | JS canvas, registers answer entry |

**Rule of thumb:** If students answer via RadioButtons or other PGML widgets (not by clicking the graph), use `PGgraphmacros.pl`. GraphTool's `ans_rule()` creates a phantom answer entry that can interfere with subsequent PGML answer evaluators.

---

## PGgraphmacros: Static Display Graphs

### Minimal Example

```perl
loadMacros(
  'PGstandard.pl',
  'MathObjects.pl',
  'PGML.pl',
  'PGgraphmacros.pl',
  'PGcourse.pl',
);

# Create graph: init_graph(xmin, ymin, xmax, ymax, ...)
$gr = init_graph(-1, 0, 10, 14,
  axes  => [0, 0],
  grid  => [11, 14],
  size  => [480, 400],
);

# Plot a function (string formula, not a code reference)
add_functions($gr,
  "2 + 3*sin(x) for x in <0,10> using color:blue and weight:2"
);

# Render as an image
$graph_img = image(insertGraph($gr), width => 480, height => 400, tex_size => 700);

BEGIN_PGML
Here is a graph:

[$graph_img]*
END_PGML
```

Key points:
- `init_graph` returns a GD graph object.
- `add_functions` takes a **string** formula with `for x in <min,max> using color:COLOR and weight:N`.
- `image(insertGraph($gr), ...)` produces an `<img>` HTML tag.
- Use `[$graph_img]*` in PGML (the `*` prevents HTML escaping).

### init_graph Parameters

```perl
$gr = init_graph($xmin, $ymin, $xmax, $ymax,
  axes  => [$x_origin, $y_origin],  # where axes cross
  grid  => [$x_divisions, $y_divisions],  # grid line count
  size  => [$width_px, $height_px],  # image dimensions
);
```

- `axes => [0, 0]` places the origin at (0, 0).
- `grid` controls the number of light grid lines (not tick labels).
- `size` sets the GD image dimensions in pixels.

### Adding Labels

```perl
# Axis labels at edges of plot area
$gr->lb(new Label($xmax, $ymin - 0.7, 'x-axis label', 'black', 'right', 'top'));
$gr->lb(new Label($xmin - 0.1, $ymax, 'y-axis', 'black', 'right', 'top'));

# Tick labels on y-axis
for $yv (0, 2, 4, 6, 8, 10, 12) {
  $gr->lb(new Label($xmin - 0.08, $yv, $yv, 'black', 'right', 'middle'));
}

# Tick labels on x-axis
for $xv (0, 1, 2, 3) {
  $gr->lb(new Label($xv, $ymin - 0.3, $xv, 'black', 'center', 'top'));
}
```

Label constructor: `new Label($x, $y, $text, $color, $h_align, $v_align)`

- `$h_align`: `'left'`, `'center'`, `'right'`
- `$v_align`: `'top'`, `'middle'`, `'bottom'`
- Labels are positioned in graph coordinates (not pixel coordinates).

### add_functions Syntax

The function string format:

```
"FORMULA for x in <XMIN,XMAX> using color:COLOR and weight:WEIGHT"
```

- `FORMULA`: A Perl math expression using `x` as the variable (e.g., `2*x**3 + x - 1`).
- `<XMIN,XMAX>`: Domain interval (angle brackets).
- `color:COLOR`: `blue`, `red`, `green`, `black`, etc.
- `weight:WEIGHT`: Line thickness in pixels (1, 2, 3, ...).

For computed coefficients, interpolate into the string:

```perl
$a = 0.5;
$b = -1.2;
$c = 3.0;
$d = 1.5;
$func_str = "$a*x**3 + $b*x**2 + $c*x + $d";
add_functions($gr, "$func_str for x in <0,3> using color:blue and weight:2");
```

### Multiple Curves

```perl
add_functions($gr,
  "$curve1 for x in <0,10> using color:blue and weight:2",
  "$curve2 for x in <0,10> using color:red and weight:2",
);
```

### Point-by-Point Curves with moveTo/lineTo

When a formula string cannot express the curve shape (e.g., parametric curves, physical models where x is not the independent variable), draw point-by-point:

```perl
$first_pt = 1;
for $i (0..400) {
  $t = $i / 400.0;
  # compute ($x_val, $y_val) from $t
  if ($first_pt) {
    $gr->moveTo($x_val, $y_val);
    $first_pt = 0;
  } else {
    $gr->lineTo($x_val, $y_val, 'blue', 2);
  }
}
```

This approach is essential for curves where the x-axis value is a computed function of the sweep variable rather than the independent variable itself. Use 300-400 points for smooth results.

### Dashed Lines

PGgraphmacros has no built-in dash style. Draw dashes manually as short line segments with gaps:

```perl
# Horizontal dashed line at y=$pka from x=0 to x=$xeq
for $d (0..29) {
  $x1d = $d * 0.10;
  $x2d = $x1d + 0.05;
  if ($x1d < $xeq) {
    if ($x2d > $xeq) { $x2d = $xeq; }
    $gr->moveTo($x1d, $pka);
    $gr->lineTo($x2d, $pka, 'gray', 1);
  }
}
```

Tune dash length (0.05) and gap (0.05) relative to graph coordinates. For vertical dashes, swap x/y in the loop.

### Dots and Stamps

```perl
# Filled circle at a point
$gr->stamps(closed_circle($x, $y, 'black'));

# Open circle
$gr->stamps(open_circle($x, $y, 'black'));
```

---

## Label Sizing: Why Labels Look Small and How to Fix It

**Labels in PGgraphmacros are GD bitmap text.** This has important consequences:

- `tex_size` on `image()` only affects TeX/PDF output, not HTML/GD output.
- TeX size commands (`\Large`, `\huge`) in label strings render as literal text in GD, not as formatting.
- `GD::Font->Giant` is accessible in the safe compartment (`$lb->font(GD::Font->Giant)`) but the largest GD bitmap font (9x15px) is still small.
- **Rendering at 2x and displaying at 1x makes labels half-size.** GD text is fixed-pixel; there is no "display DPI" concept.

### Pragmatic Approach for Readable Labels

Keep `size` at the final display dimensions (no 2x trick). Improve readability through layout:

```perl
# Slightly larger canvas
$gr = init_graph(-0.6, -1.2, 3.4, 12.5,
  axes => [0, 0],
  grid => [8, 5],
  size => [520, 420],
);

# Axis labels at edges (right-aligned at plot boundary)
$gr->lb(new Label(3.4, -0.7, 'OH- (equivalents)', 'black', 'right', 'top'));
$gr->lb(new Label(-0.1, 12.5, 'pH', 'black', 'right', 'top'));

# Fewer tick labels to reduce crowding
for $yv (0, 2, 4, 6, 8, 10, 12) {
  $gr->lb(new Label(-0.08, $yv, $yv, 'black', 'right', 'middle'));
}

$graph_img = image(insertGraph($gr), width => 520, height => 420, tex_size => 700);
```

Key techniques:
- **Widen graph bounds** beyond data range (`-0.6` to `3.4` instead of `0` to `3`) to create margin space for labels.
- **Place axis labels at edges** using `$xmax`/`$ymax` coordinates with `'right', 'top'` alignment.
- **Reduce tick label count** to avoid crowding (every 2 or 4 units instead of every 1).
- **Use high contrast** (black text on white background).

### GD Font Sizes (for reference)

Available via `$label->font(GD::Font->NAME)`:

| Font | Pixel Size | Notes |
|------|-----------|-------|
| `Tiny` | 5x8 | Too small for most uses |
| `Small` | 6x12 | Default in most PG builds |
| `MediumBold` | 7x13 | Slightly larger |
| `Large` | 8x16 | |
| `Giant` | 9x15 | Largest available |

All are fixed-size bitmap fonts. The size difference between Small and Giant is modest.

---

## Worked Example: Triprotic Titration Curve

A single cubic polynomial **cannot** produce the correct titration curve shape for a molecule with three pKa values. A cubic has at most one inflection point, but a 3-pKa titration needs three sigmoid steps.

### Physical Speciation Model (Correct Shape)

Sweep pH and compute the equivalents of base (n_bar) from the charge balance:

```
n_bar = (Ka1*H^2 + 2*Ka1*Ka2*H + 3*Ka1*Ka2*Ka3)
      / (H^3 + Ka1*H^2 + Ka1*Ka2*H + Ka1*Ka2*Ka3)
```

This gives the exact titration curve: three sigmoid steps with buffer flats at half-equivalence points (0.5, 1.5, 2.5 eq) and steep transitions at equivalence points (1.0, 2.0 eq).

```perl
$Ka1_val = 10**(-$pKa1_num);
$Ka2_val = 10**(-$pKaR_num);
$Ka3_val = 10**(-$pKa2_num);

$num_pts = 400;
$ph_lo = 0.5;
$ph_hi = 12.5;
$first_pt = 1;
for $i (0..$num_pts) {
  $ph_sweep = $ph_lo + ($ph_hi - $ph_lo) * $i / $num_pts;
  $H_conc = 10**(-$ph_sweep);

  $denom = $H_conc**3
         + $Ka1_val * $H_conc**2
         + $Ka1_val * $Ka2_val * $H_conc
         + $Ka1_val * $Ka2_val * $Ka3_val;
  $nbar = ($Ka1_val * $H_conc**2
         + 2 * $Ka1_val * $Ka2_val * $H_conc
         + 3 * $Ka1_val * $Ka2_val * $Ka3_val) / $denom;

  if ($nbar >= 0 && $nbar <= 3.0) {
    if ($first_pt) {
      $gr->moveTo($nbar, $ph_sweep);
      $first_pt = 0;
    } else {
      $gr->lineTo($nbar, $ph_sweep, 'blue', 2);
    }
  }
}
```

Note: this sweeps pH (y-axis) uniformly and computes equivalents (x-axis) as the dependent variable. The `moveTo`/`lineTo` approach handles this naturally since x is not the sweep variable.

### Why Not a Cubic?

A cubic `ax^3 + bx^2 + cx + d` through four points (e.g., (0, 1.5), (1, pKa1), (2, pKaR), (3, 12)):
- Has only **one inflection point** -- a triprotic titration needs three sigmoid transitions.
- Anchors pKa values at integer equivalents (1, 2) instead of the correct half-equivalents (0.5, 1.5, 2.5).
- Produces a smooth bend, not the characteristic "staircase with shoulders" shape.

### Alternative: Stacked Logistic Sigmoids

If you do not need physical accuracy, three logistic functions centered at half-equivalents approximate the shape:

```perl
$k = 10;  # steepness
$y0 = 1.0;
$y_top = 11.5;

for $i (0..300) {
  $xx = 3.0 * $i / 300.0;
  $s1 = 1 / (1 + exp(-$k * ($xx - 0.5)));
  $s2 = 1 / (1 + exp(-$k * ($xx - 1.5)));
  $s3 = 1 / (1 + exp(-$k * ($xx - 2.5)));

  $ph = $y0
      + ($pKa1_num - $y0) * $s1
      + ($pKaR_num - $pKa1_num) * $s2
      + ($pKa2_num - $pKaR_num) * $s3
      + ($y_top - $pKa2_num) * $s3 * 0.20;

  # draw with moveTo/lineTo as above
}
```

Note: the stacked-logistic curve does **not** pass exactly through pKa at each half-equivalence point. The speciation model is preferred for accuracy.

---

## GraphTool: Interactive Graphs (Use with Caution)

`parserGraphTool.pl` creates a JS-based interactive canvas where students can draw or place points.

### Known Issue: Answer Evaluator Interference

GraphTool's `ans_rule()` registers an answer entry (typically `AnSwEr0001`). This shifts the numbering of subsequent PGML answer blanks and can cause `"Unrecognized evaluator type ||"` errors on later RadioButtons or other PGML widgets.

**Workaround:** If you must use GraphTool alongside PGML answers:
- Place GraphTool in a `BEGIN_TEXT` block with `\{$gt->ans_rule()\}`.
- Use `LABELED_ANS($gt_ans_id, $gt_checker)` before the PGML block.
- Keep RadioButtons and other widgets in a separate `BEGIN_PGML` block.

**Better approach:** If the graph is display-only, use `PGgraphmacros.pl` instead.

### GraphTool Minimal Pattern (for reference)

```perl
loadMacros('parserGraphTool.pl');

$gt = GraphTool()->with(
  bBox        => [-1, 14, 14, -1],
  gridX       => 1,
  gridY       => 1,
  xAxisLabel  => 'x',
  yAxisLabel  => 'y',
  availableTools  => ['PointTool'],
  staticObjects   => ['{cubic,solid,(0,2),(4,3.8),(7,4.6),(12,12)}'],
);

BEGIN_TEXT
\{$gt->ans_rule()\}
END_TEXT

$gt_checker = AnswerEvaluator->new;
$gt_checker->install_evaluator(sub { ... });
LABELED_ANS($gt->ANS_NAME, $gt_checker);
```

---

## Variable Scoping Reminder

Do **not** use `my` on any variable that PGML needs to interpolate. PG runs in a safe compartment where `my` variables are invisible to PGML.

```perl
# WRONG - invisible to PGML
my $graph_img = image(insertGraph($gr), ...);

# RIGHT - package-level, visible to PGML
$graph_img = image(insertGraph($gr), ...);
```

See [PG_COMMON_PITFALLS.md](PG_COMMON_PITFALLS.md) for more scoping details.

---

## Sizing and Margins

The `size` parameter in `init_graph` sets the GD image pixel dimensions. The `width` and `height` in `image()` control the HTML display size. **Always keep these matched at 1x** -- rendering at 2x and displaying at 1x shrinks bitmap labels.

```perl
# Good: matched sizes, extra margin from wider bounds
$gr = init_graph(-0.6, -1.2, 3.4, 12.5,
  axes => [0, 0],
  grid => [8, 5],
  size => [520, 420],
);
$graph_img = image(insertGraph($gr), width => 520, height => 420, tex_size => 700);
```

To create margin space for labels without shrinking the data region, widen the graph bounds beyond the data range (e.g., `-0.6` to `3.4` for data spanning 0 to 3).

`tex_size` controls the image width in TeX/PDF output only (700 = 70% of text width). It has no effect on HTML/GD rendering.

---

## Macros Not Available in This Renderer

The following graph-related macros exist in the OPL but are **not** available in the local PG 2.17 renderer:

- `PGlateximage.pl` (LaTeX-to-image pipeline, requires LaTeX installation)
- `PGtikz.pl` (TikZ/pgfplots, requires LaTeX installation)

Stick to `PGgraphmacros.pl` for display graphs and `parserGraphTool.pl` for interactive graphs.

---

## Custom Colors with `new_color`

Default GD named colors (`red` = #FF0000, `green` = #00FF00, `blue` = #0000FF)
have poor contrast ratios on white and are not colorblind-safe. Define accessible
colors after `init_graph`:

```perl
$gr->new_color('accessible_blue', 0, 63, 255);   # #003fff, 6.66:1
$gr->new_color('accessible_red', 183, 67, 0);     # #b74300, 5.50:1
$gr->new_color('accessible_teal', 0, 119, 95);    # #00775f, 5.52:1
```

Use these names anywhere a color is expected: `$fn->color('accessible_blue')`,
`new Label(..., 'accessible_red', ...)`, `$gr->lineTo(..., 'accessible_teal', 2)`.

Blue/orange/teal avoids the red-green confusion axis for colorblind users while
meeting the 5.5:1 WCAG contrast target. See
[COLOR_CONTRAST_ACCESSIBILITY.md](COLOR_CONTRAST_ACCESSIBILITY.md) for the full
14-color palette.

### Default GD named colors (for reference)

| Name | RGB | Contrast vs white |
| --- | --- | --- |
| `black` | 0, 0, 0 | 21:1 |
| `white` | 255, 255, 255 | 1:1 |
| `red` | 255, 0, 0 | 4.0:1 (fails) |
| `green` | 0, 255, 0 | 1.4:1 (fails) |
| `blue` | 0, 0, 255 | 8.6:1 |
| `yellow` | 255, 255, 0 | 1.1:1 (fails) |
| `orange` | 255, 100, 0 | 3.0:1 (fails) |
| `gray` | 180, 180, 180 | 2.0:1 (fails) |

---

## Drawing Curves with Fun Objects

For complex curve shapes (Gaussians, Gumbel distributions, custom models), use
parametric `Fun` objects instead of `add_functions` string syntax:

```perl
my $fn = new Fun(
    sub { my $t = shift; return $t; },      # x(t)
    sub {                                    # y(t)
        my $t = shift;
        my $z = ($t - $optimum) / $sigma;
        my $val = $peak * exp(-0.5 * $z * $z);
        return $val;
    },
    $gr,
);
$fn->domain(-2, 14);   # extend past visible range (GD clips at boundary)
$fn->steps(400);        # 400 sample points for smooth curves
$fn->weight(2);         # line thickness in pixels
$fn->color('accessible_blue');
```

---

## Controlling Aspect Ratio

The **coordinate range** in `init_graph` determines the graph shape. The pixel
`size` sets resolution only. A coordinate range with equal x and y spans
produces a square graph regardless of pixel dimensions.

```perl
# widescreen: x spans ~13 units, y spans ~8 units
$gr = init_graph(-0.8, -1.1, 12.3, 7,
    axes => [0, 0],
    size => [520, 300],
);
```

To make a graph wider, increase the x range relative to y (or decrease the y
range). Adjust peak heights to fit the reduced y range.

---

## Avoiding Auto-Labels: Manual Grid and Ticks

Both `grid` and `ticks` options in `init_graph` auto-generate numeric labels at
axis endpoints and the first grid delta. These labels cannot be suppressed.
Additionally, `grid` overrides `ticks` -- you cannot use both via `init_graph`.

**Solution:** Skip both options and draw grid lines, ticks, and labels manually:

```perl
$gr = init_graph(-0.8, -1.1, 12.3, 7,
    axes => [0, 0],
    size => [520, 300],
);

# manual grid lines at chosen positions
$gr->v_grid('gray', 2, 4, 6, 8, 10, 12);
$gr->h_grid('gray', 2, 4, 6);

# manual tick marks (tiny -- hardcoded at 2px, see limitations below)
$gr->h_ticks(0, 'black', 2, 4, 6, 8, 10, 12);
$gr->v_ticks(0, 'black', 2, 4, 6);

# manual tick labels
for (my $x = 2; $x <= 12; $x += 2) {
    $gr->lb(new Label($x, -0.3, "$x", 'black', 'center', 'middle'));
}

# axis labels
$gr->lb(new Label(6, -0.7, 'pH', 'black', 'center', 'middle'));
$gr->lb(new Label(-0.4, 3.2, 'Enzyme Activity', 'black',
    'center', 'middle', 'vertical'));
```

Use small negative xmin/ymin margins to create space for labels.

---

## Degree Symbol in Graph Labels

Graph labels render into GD bitmaps, not HTML. Use Perl `\x{B0}` (Latin-1
degree sign):

```perl
$gr->lb(new Label(39, -0.9, "Temperature (\x{B0}C)",
    'black', 'center', 'middle'));
```

For degree symbols in PGML text (outside the graph), use HTML entities in a Perl
variable with `[$var]*` passthrough. See
[PG_COMMON_PITFALLS.md](PG_COMMON_PITFALLS.md).

---

## Avoiding Peak Labels on Grid Lines

If curve peaks land on grid line positions, the label letter overlaps the dashed
line. Use values that avoid grid positions:

```perl
# grid lines at even integers (2, 4, 6, 8, 10, 12)
# use odd base values + random offset so peaks miss grid lines
my @pH_pool = (3, 5, 7, 9, 11);
my $offset = $local_random->random(1, 8, 1) / 10.0;
$pH = $pH + $offset;  # e.g., 5.3 instead of 6.0
```

---

## Known PGgraphmacros Limitations

### Functions always draw on top of everything

WWPlot renders functions **twice** (lines 492 and 573 of `WWPlot.pm`) -- once
before and once after axes, grids, and tick marks. Curves always cover the
axis line and tick marks.

**Impact:** Near-zero curve tails cover the x-axis. There is no workaround.
Do not clamp curve values to float above the axis -- this creates a visible
colored band and is scientifically inaccurate. Accept that tails cover the axis.

### Tick marks are tiny and outward-pointing

`h_ticks`/`v_ticks` hardcode a 2-pixel nudge (`WWPlot.pm` line 455). Ticks
always point outward, not inward as recommended by the
[APS H-18 guidelines](https://journals.aps.org/authors/axis-labels-and-scales-on-graphs-h18).
The tick size and direction cannot be changed through the API.

### No font larger than `giant`

GD built-in bitmap fonts: `tiny` (5x8), `small` (6x12), `mediumbold` (7x13,
default), `large` (8x16), `giant` (9x15). For larger text, TrueType fonts via
`GD::Image->stringFT()` (not exposed by PGgraphmacros) or TikZ would be needed.

### Grid overrides ticks in `init_graph`

The source contains `"draw ticks -- grid over rides ticks"`. If you pass both
`grid` and `ticks` options, only grid is drawn. Use manual `v_grid`/`h_grid`
plus manual `h_ticks`/`v_ticks` calls to get both.

---

## Style Reference

- [APS H-18: Axis Labels and Scales on Graphs](https://journals.aps.org/authors/axis-labels-and-scales-on-graphs-h18) -- tick marks inward, labels below ticks, units in parentheses
- [COLOR_CONTRAST_ACCESSIBILITY.md](COLOR_CONTRAST_ACCESSIBILITY.md) -- WCAG contrast ratios

---

## Reference Examples

- [enzyme_ph_activity_graph.pgml](../../problems/biochemistry-problems/enzymes/enzyme_ph_activity_graph.pgml) -- Gaussian curves, manual grid, accessible colors, vertical y-axis label
- [enzyme_temp_activity_graph.pgml](../../problems/biochemistry-problems/enzymes/enzyme_temp_activity_graph.pgml) -- Gumbel curves, degree symbol, two-pass normalization

---

## Related Documentation

- [PG_2_17_RENDERER_MACROS.md](PG_2_17_RENDERER_MACROS.md) - Full list of available macros
- [PG_COMMON_PITFALLS.md](PG_COMMON_PITFALLS.md) - Variable scoping, PGML parsing, degree symbols
- [WEBWORK_PROBLEM_AUTHOR_GUIDE.md](WEBWORK_PROBLEM_AUTHOR_GUIDE.md) - Overall problem structure
