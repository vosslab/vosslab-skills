# CSS task selection

Turn "make this look better" into a rendered contract before choosing syntax.

## Route the request

| Request signal | Route | First question |
| --- | --- | --- |
| Flat, generic, or visually weak | Visual craft | Which content needs prominence and what visual character serves it? |
| Crowded, misaligned, overflowing, or order-dependent | Layout | What are the content regions, sizing constraints, and narrow-screen behavior? |
| Inconsistent colors, brand refresh, or light/dark request | Theming | Which semantic color roles and token boundaries are stable? |
| Jarring, missing, or excessive movement | Motion | What state change should movement explain, and what is the reduced-motion behavior? |

## Establish the contract

- Name target pages, components, states, viewport range, color scheme, and the
  visual result a screenshot must demonstrate.
- Inspect semantic HTML and existing CSS first; distinguish a structure problem
  from a presentation problem.
- Route layout primitive, selector, cascade, and feature questions through
  [topic_index.md](topic_index.md).
- Keep accessible color design in this skill. Route a measured contrast audit or
  numerical palette repair to `color-accessibility-expert`.
- Route task flow, affordances, interaction state, and usability judgment to
  `ui-ux-engineer`.
