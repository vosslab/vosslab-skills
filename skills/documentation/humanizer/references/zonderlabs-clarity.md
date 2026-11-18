# Zonder Labs: clarity before surface tells

Source: Zonder Labs, [Why is AI Slop so Frustrating to Read?](https://zonderlabs.com/slop), published November 9, 2026; read November 16, 2026.

Source type: original research / practitioner blog, not established here as peer-reviewed research. The article draws on Joseph M. Williams and Joseph Bizup's *Style: The Basics of Clarity and Grace*, fifth edition. The editing guidance below paraphrases the article; the new examples are constructed, not study observations or verified facts about any project.

## What to use

The article focuses on work messages readers must understand, rather than disposable social posts. Its useful distinction is between recognizing an AI-like surface and identifying a real communication problem. A detector score or an em dash does not tell us whether the reader can understand the point.

### Hidden characters and actions

Identify who or what does something, then find the action. Prefer putting the actor in the grammatical subject and the action in the verb when that makes the sentence easier to follow. Watch for actions buried in nouns ("arrival", "request", "implementation") and vague verbs such as "occurred" or "was performed".

Constructed example:

- Before: "The team's completion of the review was followed by its approval of the release."
- After: "The team finished the review and approved the release."

The source explicitly says this alignment is not a strict rule. Preserve a useful passive when the actor is unknown, irrelevant, or deliberately outside the sentence's focus. Never assign an actor just to make the grammar active.

### Vague wording

Look for ambiguous pronouns, stacked nouns, unexplained compressed labels, odd word combinations, and words that sound precise without identifying anything. Use the ordinary name for the thing. Keep specialist terms when they carry needed meaning, and explain them if the intended reader needs help.

Constructed example:

- Before: "The database readiness check sits at the user-session entry boundary, before authentication."
- After: "The app checks whether the database is ready before authenticating the user."
- Condition: use that rewrite only if the context establishes that the app performs the check. If the actor is unknown, "The database is checked before the user is authenticated" can be more honest.

If "the same numbers within 2%" does not identify whether the numbers are runtimes or outputs, ask or flag that missing detail. Do not silently pick a quantity, baseline, unit, mechanism, or cause.

### Empty statements and misplaced emphasis

State the point readers need before qualifications or side issues. Delete sentences that add no information; keep conditions and dependencies that change what readers should do. Distinguish a result, a plan, and a promise. Do not turn one into another while shortening it.

Constructed example:

- Before: "It is important to note that, following completion of the poll, the team will provide the result."
- After: "The team will report the result when the poll finishes."

Shorter is not always clearer. A second sentence may be needed to preserve a separate dependency, exception, or uncertainty.

## What the measurements do and do not show

The article reports sentence-level "unclear" rates of 54% for AI articles, 10% for human articles, 78% for Claude Code, and 11% for Stack Overflow, using its three-fault taxonomy. These are the authors' reported results for their samples, not universal estimates, independent replication, or evidence about Dr. Voss's prose.

The public article as read does not give enough detail to independently audit sample sizes and selection, model versions, annotation instructions and annotator counts, agreement statistics, or uncertainty intervals. It asserts strong human agreement without reporting an agreement statistic in the article. Genre/task differences and sampling may affect the comparisons. Fault categories can overlap; their rates must not be added as though they were exclusive.

The article separately compares clarity with AI-detection results and says it used IdeaLens. That does not validate the detector's accuracy or make its scores editorial targets. Use the taxonomy as an editing heuristic, not a validated scoring instrument or an authorship test. No causal claim about model training or optimization follows from the displayed comparisons alone.

## Accepting future blogs and practitioner research

Dr. Voss requests more blogs and original research blogs from non-academics because this area moves quickly. When refreshing this skill or researching AI-assisted writing:

- Search beyond journals and preprint servers. Actively include independent writers, editors, developers, and practitioner research blogs; academic affiliation is neither a requirement nor a substitute for evidence.
- Read the original post, not just a roundup or search snippet. Record title, author/organization, URL, publication/update date when available, access date, and source type.
- Separate a useful editing observation from an empirical result. For research claims, inspect samples, comparison conditions, model/tool versions, annotation methods, data/code availability, limitations, commercial interests, and contrary evidence. State what is missing.
- Use concrete before/after examples and transparent methods to judge whether advice transfers to the current task. A clear example can justify trying a heuristic without proving a general performance claim.
- Label practical advice as editorial guidance. Do not present it as peer-reviewed evidence, give it a made-up effect size, or reject it merely because it is not peer reviewed.
- Update the skill when a source supplies a useful distinction or correction, not merely another list of banned words. Preserve the author's meaning and genre, and keep a traceable source link.

This is a source-selection policy for skill updates and writing research, not a requirement to browse the web during every rewrite or permission to change research cron jobs.

## Review cases

These constructed cases are qualitative checks, not a measured evaluation of editing quality:

| Input / known context | Acceptable handling | Reject |
|---|---|---|
| "The team's completion of the review was followed by its approval of the release." | "The team finished the review and approved the release." | Inventing a reviewer, date, or approval condition. |
| "The request was rejected." Actor unknown. | Keep the passive, or flag the unknown actor if it matters. | "The server rejected the request." |
| "Same numbers within 2%." No quantity identified. | Flag which numbers, baseline, and comparison are meant. | Silently changing "numbers" to "runtime". |
| "It is important to note that the treatment may reduce symptoms in this sample." | "The treatment may reduce symptoms in this sample." | "The treatment reduces symptoms." |
| "The trial was double-blind." | Keep the precise technical description; explain it only if needed. | Removing useful terminology or a grammatical hyphen to look less AI-like. |
| "The team will report after the poll, provided the data pass validation." | "The team will report when the poll finishes if the data pass validation." | Dropping validation, or claiming the team has already reported. |
| A sourced sentence contains an em dash but is already clear. | Leave it unless the user's style calls for a change. | Treating punctuation as proof of AI authorship. |
