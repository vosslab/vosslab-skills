# Reference survey

This coverage map indexes the six local book conversions in
`references/local-only/`. Use it with [local_books.md](local_books.md) to select a
book, then grep the named flat-text file for the listed term. Each rating comes
from the named chapter and sampled teaching passage, not from a match count.

## How to use

- Start with a `strong` source, read its named chapter, and adapt its method to
  the project evidence.
- Use `partial` and `thin` sources as supporting context alongside project
  research and current authoritative guidance.
- When the corpus is absent or a topic needs normative platform requirements,
  use the W3C WCAG guidance and the target platform's human-interface
  guidelines, then apply first-principles accessibility and usability review.

## Topic-to-reference map

### Interaction design process

Coverage: strong.

- `references/local-only/Interaction_Design_Beyond_Human-Computer_Interaction-2023.md`
  Chapter 2, "Process of Interaction Design." grep `interaction design process`.
  The sampled opening defines the process as requirements discovery, design,
  prototyping, and evaluation, then teaches the iterative Discover, Define,
  Develop, Deliver cycle and stakeholder involvement.
- `references/local-only/Designing_the_User_Interface_Strategies_for_Effective_Human-Computer_Interaction-2018.md`
  Section 4.3, "The Design Process." grep `requirements analysis`. The sampled
  phases connect requirements, detailed design, implementation, and validation
  through use cases and prototypes.

### User research and requirements

Coverage: strong.

- `references/local-only/User_Experience_Methods_and_Tools_in_Human-Computer_Interaction-2025.md`
  Chapter 1, "Requirements Engineering and User Needs Analysis." grep
  `requirements engineering`. The sampled passage distinguishes system-focused
  requirements from broader user-needs analysis, gives elicitation,
  documentation, validation, and change-management stages, and explains how
  they fit sequential and iterative development.
- `references/local-only/User_Experience_Methods_and_Tools_in_Human-Computer_Interaction-2025.md`
  Chapter 2, "Ethnography, User Observation, and Interviews." grep
  `ethnography`. The sampled passage teaches field observation in natural
  settings, contextual interpretation, interviews, artifacts, and field-note
  practice for turning observations into design insights.

### Task analysis

Coverage: strong.

- `references/local-only/User_Experience_Methods_and_Tools_in_Human-Computer_Interaction-2025.md`
  Chapter 5, "Task Analysis and Modeling." grep `task analysis`. Its dedicated
  chapter supports modeling the work, actions, goals, and allocation of tasks
  before specifying interface behavior.

### Cognitive analysis

Coverage: partial.

- `references/local-only/Interaction_Design_Beyond_Human-Computer_Interaction-2023.md`
  Chapter 4, "Cognitive Aspects." grep `cognitive aspects`. The sampled chapter
  introduction connects attention, memory, and perception limits to designing
  for users' tasks; use the dedicated cognitive-guidelines book below when a
  concrete visual or memory decision is required.

### Perception and memory guidelines

Coverage: strong.

- `references/local-only/Designing_with_the_Mind_in_Mind_User_Interface_Design_Guidelines-2021.md`
  Chapter 1, "Our Perception is Biased." grep `perception`. The sampled chapter
  explains perception as an interpretation of the visual world, grounding
  layout, grouping, and signal choices in how users actually see.
- `references/local-only/Designing_with_the_Mind_in_Mind_User_Interface_Design_Guidelines-2021.md`
  Chapter 7, "Our Attention is Limited; Our Memory is Imperfect." grep
  `memory`. The dedicated treatment supplies constraints for reducing attention
  demand and supporting users with visible memory cues.
- `references/local-only/Designing_with_the_Mind_in_Mind_User_Interface_Design_Guidelines-2021.md`
  Chapter 9, "Recognition is Easy; Recall is Hard." grep `recognition`. The
  sampled chapter directs designers toward visible cues and recognition-based
  interaction when users must resume or choose an action.

### Usability evaluation and heuristics

Coverage: strong.

- `references/local-only/User_Experience_Methods_and_Tools_in_Human-Computer_Interaction-2025.md`
  Chapter 7, "Inspection Methods for Usability Evaluation." grep
  `heuristic evaluation`. The dedicated chapter provides an inspection path for
  finding issues before or alongside participant testing.
- `references/local-only/User_Experience_Methods_and_Tools_in_Human-Computer_Interaction-2025.md`
  Chapter 8, "Designing, Conducting, Analyzing, and Reporting Usability Testing
  Experiments." grep `usability testing`. The sampled contents and preface
  place participant testing, analysis, and reporting within the full UX-method
  toolkit.

### Interaction techniques and modalities

Coverage: strong.

- `references/local-only/Interaction_Techniques_and_Technologies_in_Human-Computer_Interaction-2025.md`
  Chapter 1, "Interaction Styles." grep `interaction styles`. The dedicated
  treatment starts technique selection with interaction styles, then connects
  those styles to suitable devices.
- `references/local-only/Interaction_Techniques_and_Technologies_in_Human-Computer_Interaction-2025.md`
  Chapter 2, "Multimodal Interaction." grep `multimodal interaction`. The
  sampled preface and chapter routing compare input and output modes and frame
  their trade-offs for particular interactive scenarios.
- `references/local-only/Interaction_Techniques_and_Technologies_in_Human-Computer_Interaction-2025.md`
  Chapter 6, "Gesture-Based Interaction." grep `gesture-based interaction`.
  The chapter provides a focused route for gesture design; Chapters 5 and 7
  extend the same book to haptics and voice.

### Accessibility and inclusive design

Coverage: strong.

- `references/local-only/Designing_the_User_Interface_Strategies_for_Effective_Human-Computer_Interaction-2018.md`
  Chapter 2, "Universal Usability." grep `accessibility`. The sampled opening
  makes diverse users, multiple display sizes, languages, and disability support
  part of interface quality, giving a broad inclusive-design rationale.
- `references/local-only/Interaction_Design_Beyond_Human-Computer_Interaction-2023.md`
  Section 1.8, "Accessibility and Inclusiveness." grep `accessibility`. The
  sampled learning objectives frame accessibility and inclusiveness as HCI
  concerns, but this passage does not provide a conformance procedure.

### Accessibility conformance and platform guidance

Coverage: partial for established practices and dated standards; use current
W3C and platform guidance for conformance.

- `references/local-only/Designing_the_User_Interface_Strategies_for_Effective_Human-Computer_Interaction-2018.md`
  Chapter 2, "Universal Usability." grep `Section 508`. The sampled material
  names accessibility policy while its chapter-level treatment emphasizes broad
  usability goals. Use W3C WCAG for current, testable success criteria and the
  target platform's human-interface guidelines for platform behavior.

### Evaluation-study design

Coverage: strong.

- `references/local-only/Interaction_Design_Beyond_Human-Computer_Interaction-2023.md`
  Chapter 15, "Evaluation Studies: From Controlled to Natural Settings." grep
  `controlled environment`. The sampled passage distinguishes early observation
  for context, tasks, and goals from later prototype evaluation, then contrasts
  natural settings with specified tasks in a usability laboratory.
- `references/local-only/User_Experience_Methods_and_Tools_in_Human-Computer_Interaction-2025.md`
  Chapter 8, "Designing, Conducting, Analyzing, and Reporting Usability Testing
  Experiments." grep `usability testing`. The dedicated chapter supplies the
  study lifecycle from design through analysis and reporting.

## Weak-coverage routing

Use the local books to establish inclusive-design intent and HCI method. Use
W3C WCAG and the target platform's human-interface guidelines to define current
accessibility conformance, semantics, focus behavior, input support, and
component-specific acceptance checks.
