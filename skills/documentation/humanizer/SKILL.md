---
name: humanizer
description: "Humanize text: strip AI-isms and add real voice."
version: 2.5.2
author: Siqi Chen (@blader, https://github.com/blader/humanizer), ported by Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [writing, editing, humanize, anti-ai-slop, voice, prose, text]
    category: documentation
    homepage: https://github.com/blader/humanizer
---

# Humanizer: Remove AI Writing Patterns

Edit text for clarity and the author's voice. Use the patterns drawn from Wikipedia's "Signs of AI writing" guide and the clarity review from Zonder Labs as editing prompts, not as evidence of AI authorship.

**Key insight:** LLMs use statistical algorithms to guess what should come next. The result tends toward the most statistically likely completion, which is how the telltale patterns below get baked in.

## When to use this skill

Load this skill whenever the user asks to:
- "humanize", "de-AI", "de-slop", or "un-ChatGPT" a piece of text
- rewrite something so it doesn't sound like it was written by an LLM
- edit a draft (blog post, essay, PR description, docs, memo, email, tweet, resume bullet) to sound more natural
- match their voice in writing they're producing
- review text for AI tells before publishing

Also apply this skill to **your own** output when writing user-facing prose such as release notes, PR descriptions, docs, and summaries. Hermes's baseline voice already strips most of these, but a focused pass catches what slips through.

## How to use it in Hermes

The text usually arrives one of three ways:
1. **Inline.** The user pastes the text into the message. Work on it in place and reply with the rewrite.
2. **File.** The user points at a file. Use `read_file` to load it, then `patch` or `write_file` to apply edits. For a markdown doc in a repo, a targeted `patch` per section is cleaner than rewriting the whole file.
3. **Voice calibration sample.** The user provides a sample of their own writing (inline or by file path) and asks you to match it. Read the sample first, then rewrite. See the Voice Calibration section below.

Always show the rewrite to the user. For file edits, show a diff or the changed section instead of silently overwriting.

## Your task

When given text to humanize:

1. **Find the reader's problem.** Run the clarity pass below before checking surface patterns.
2. **Rewrite what needs work.** Fix a specific ambiguity, buried action, empty statement, or voice mismatch.
3. **Preserve meaning.** Keep actors, actions, attribution, negation, quantities, scope, conditions, and warranted uncertainty intact. Compare the final text with the author's original.
4. **Maintain voice.** Match the intended tone (formal, casual, technical, and so on). If a voice sample was provided, match it specifically.
5. **Keep authentic personality.** Use the author's own opinions and experiences, and keep quotes and facts grounded in the source.
6. **Check clarity and fidelity.** Ask who did what, what each reference means, where the point is, and what changed. Revise the remaining problems.

## Clarity before surface patterns

Apply these checks from Zonder Labs' [Why is AI Slop so Frustrating to Read?](https://zonderlabs.com/slop) to human writing too:

1. **Hidden actors and actions.** Put the known actor in the subject and the action in the verb when it helps. "The team's completion of the review was followed by its approval of the release" becomes "The team finished the review and approved the release." Keep the passive when the actor is unknown, irrelevant, or deliberately out of focus.
2. **Vague wording.** Resolve ambiguous references and replace abstract labels with concrete ones. Keep technical terms when they carry meaning. If "same numbers within 2%" does not identify what was measured, flag the missing detail rather than guessing.
3. **Empty statements and buried points.** Put the result, request, or decision first. Cut empty lead-ins and repetition. Keep conditions and uncertainty that qualify the claim.

Clarity, factual fidelity, the author's voice, and the genre take precedence over surface patterns. Keep useful passives, hedges, em dashes, and correct hyphenation when they fit. Use examples to learn editing moves, not to justify adding unsupported details or deliberate errors. Detector scores are neither editing targets nor authorship verdicts.

When updating this skill or researching AI-assisted writing, include original research blogs and independent writing and editing blogs alongside academic work. Read the original source, record its date and URL, and distinguish practical advice from empirical findings. Check methods and limitations before adopting numerical claims. Ordinary rewrites do not require web research. Read [references/zonderlabs-clarity.md](references/zonderlabs-clarity.md) for the source, its limits, and review cases.


## Voice Calibration (optional)

If the user provides a writing sample (their own previous writing), analyze it before rewriting:

1. **Read the sample first.** Note:
   - Sentence length patterns (short and punchy? Long and flowing? Mixed?)
   - Word choice level (casual? academic? somewhere between?)
   - How they start paragraphs (jump right in? Set context first?)
   - Punctuation habits (lots of dashes? Parenthetical asides? Semicolons?)
   - Any recurring phrases or verbal tics
   - How they handle transitions (explicit connectors? Just start the next point?)

2. **Match their voice in the rewrite.** Removing AI patterns is only half of it; swap in patterns from the sample as well. If they write short sentences, do not produce long ones. If they use "stuff" and "things," do not upgrade to "elements" and "components."

3. **When no sample is provided,** use natural, varied prose. See the linked writing-patterns reference for voice examples.

### How to provide a sample
- Inline: "Humanize this text. Here's a sample of my writing for voice matching: [sample]"
- File: "Humanize this text. Use my writing style from [file path] as a reference."


## Dates and times in everyday writing

When writing in Dr. Voss's voice:

- Use `5pm` and `9am` in everyday email, including subject lines: lowercase, no spaces, no
  periods. Preserve this format when editing his drafts.
- Omit zero minutes for whole hours (`5pm`); keep meaningful minutes (`5:30pm`).
- In short reminders, use `today at 5pm` or `Wednesday at 5pm` when the context is clear.
  Include the calendar date when readers need it to avoid ambiguity.
- Use readable dates such as `October 21` or `Oct 21`; omit the year when it is obvious.
- Preserve exact dates, time zones, and precision when they matter for deadlines, travel,
  cross-time-zone meetings, formal requirements, or machine-readable records. Follow any
  explicitly requested style guide.

Example: `We're meeting in person today (Nov 18) at 5pm.`

## Process
1. Read the original and any voice sample. Find the reader's problem with the clarity pass; consult [references/writing-patterns.md](references/writing-patterns.md) for relevant patterns and examples.
2. Draft the rewrite. Keep it natural and specific. Flag ambiguity rather than guessing.
3. Compare the draft with the original. Check meaning, tone, and any remaining clarity problems. Read it aloud to check the rhythm, then make the final edits.
4. Show the draft, a brief clarity and fidelity audit, and the final rewrite. For file edits, show the change. Summarize only when it helps.

Read [references/rewrite-example.md](references/rewrite-example.md) for a worked example of the draft, audit, and final rewrite.

## Where to update this skill

Edit this skill in `vosslab-skills`. Keep one active copy through the documentation category link. After retiring a duplicate, confirm `skill_view(name='humanizer')` resolves here.

## Attribution

See [references/writing-patterns.md](references/writing-patterns.md) for upstream credit and the original pattern catalog.
