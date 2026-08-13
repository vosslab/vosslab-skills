# Dimension-identification

Name the axes along which versions of this idea can vary. Each axis is a *dimension*; each possible value along an axis is a *property*. Together, dimensions define the space within which the idea lives.

## Procedure

1. **Ask the discriminating question.** "What could differ between two versions of this idea while both still count as instances of the same idea?" Each answer is a candidate dimension.
2. **For each candidate, list the possible values.** A dimension with only one possible value isn't really a dimension — drop it. A dimension with two values is binary; with many values, scalar or categorical.
3. **Test the dimension.** Pick a value other than the current one and substitute it (see `substitution.md`). If the result is a coherent variant of the original, the dimension is real.
4. **Stop when you have enough.** Five to ten dimensions is usually plenty for one expansion pass; you can return for more later.

## Quote from Grace

> Dimensions are the space of possible properties along an axis, and properties are the possible values for a dimension.

## Example dimensions Grace lists

| Dimension | Possible values |
|---|---|
| Naturalness | Natural / Man-made |
| Homogeneity | Homogenous / Heterogenous |
| Hierarchicalness | Hierarchical / Non-hierarchical |
| Longevity | Long-lived / Short-lived / Equally-lived (~human) / Variably-lived |
| Complexity | Complex / Simple |

These five aren't a fixed catalog — they're examples. The dimensions of *your* idea depend on *your* idea. The dimension-prompts in `methods/dimension-prompts/` are a starting battery; cross-apply them to surface candidates.

## Pairing

Dimension-identification is the foundation under substitution and negation. Both operate on dimensions. Without dimensions, neither operator has anything to swap.

A common pairing: identify dimensions → for each dimension, substitute every value → enumerate the resulting variants. (See the `dimensional-exhaustion` recipe.)
