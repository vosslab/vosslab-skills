# UI and UX review logic

## Table of contents

- Foundational principles
- Value lenses
- First-pass questions
- Visual hierarchy
- Interaction quality
- Validation and errors
- State coverage
- Accessibility and keyboard support
- Common failure modes

## Foundational principles

- Simplicity: reduce effort, choices, and visual noise.
- User-centered design: optimize for user goals, context, and constraints rather than internal implementation structure.
- Visibility: make important actions and system status obvious.
- Consistency: reuse layout patterns, control behavior, naming, and visual language.
- Feedback: acknowledge actions and state changes promptly.
- Clarity: prefer understandable flow and wording over decorative styling.
- Accessibility: support keyboard access, readable contrast, and assistive technology compatibility.
- Usability: keep interactions easy to learn and easy to recover from.
- Efficiency: help users complete frequent tasks with minimal friction.
- Delight: add polish only after usefulness and clarity are solid.

## Value lenses

- Usefulness: solve a real user problem and prioritize features that create clear value.
- Desirability: make the interface appealing without hiding function behind style.
- Accessibility: ensure the experience works for users with different abilities and input methods.
- Credibility: use accurate content, stable behavior, and professional visual quality to build trust.
- Findability: organize content and navigation so important actions and information are easy to locate.
- Usability: keep controls intuitive, instructions clear, and workflows testable with real users.
- Value impact: make the benefit of the workflow obvious in time saved, reduced errors, or better outcomes.

## First-pass questions

- Can a user identify the screen purpose quickly?
- Is the main action obvious without reading everything?
- Is the information ordered by importance and task sequence?
- Does the layout reduce effort instead of exposing implementation structure?

## Visual hierarchy

- One primary action should dominate each surface.
- Group related controls with spacing before adding borders.
- Keep labels, helper text, and error text visually distinct.
- Use alignment to make scanning easy, especially in forms and settings panels.
- Avoid making every section equally loud.

## Interaction quality

- Make clickable elements look clickable.
- Show the result of each action quickly.
- Preserve user input during recoverable errors.
- Confirm destructive actions with specific language about consequences.
- Avoid surprise modal dialogs for routine feedback.

## Validation and errors

- Prevent invalid input with constrained controls when practical.
- Validate early enough to help, but not so early that the UI feels hostile.
- Write error text that tells the user what to fix next.
- Distinguish between field-level mistakes, workflow blockers, and system failures.

## State coverage

- Define intentional layouts for empty, loading, success, partial, and failure states.
- Empty states should explain what the user can do next.
- Loading states should indicate whether the UI is still responsive.
- Failure states should preserve context and offer retry or fallback paths when possible.

## Accessibility and keyboard support

- Ensure all primary actions are reachable by keyboard.
- Keep tab order aligned with reading and task order.
- Use explicit text labels for important actions instead of icon-only controls.
- Add tooltips only when they clarify behavior, not to hide missing labels.
- Prefer readable contrast and sufficiently large hit targets.

## Common failure modes

- Forms that require too much memory because labels, examples, and constraints are separated.
- Tables with important actions hidden in context menus only.
- Dialogs that ask generic questions like `Are you sure?` without naming the object or consequence.
- Busy indicators with no explanation of what is happening.
- Settings pages that mirror internal architecture instead of user goals.

## Source note

This review checklist incorporates and adapts general UI/UX principles from the GeeksforGeeks article "Principles of UI/UX Design" dated October 23, 2025:
[https://www.geeksforgeeks.org/techtips/principles-of-ui-ux-design/](https://www.geeksforgeeks.org/techtips/principles-of-ui-ux-design/)
