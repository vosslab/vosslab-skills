# What shaped the checklist

Use this map when updating the checklist or explaining why a pattern is worth checking. The
editing instructions and examples are in [ai-writing-checklist.md](ai-writing-checklist.md).
Everyday edits do not require opening the external links. Keep Dr. Voss's original list in
[neil-approved-sources.md](neil-approved-sources.md). An article can justify trying a specific
edit without proving a general rule. A catalog can supply examples without saying how common
they are. Neither counts as human testing of this checklist.

## Clarity and structure

- **Zonder Labs, [Why is AI Slop so Frustrating to Read?](https://zonderlabs.com/slop)**
  (practitioner research): look for hidden actors and actions, vague wording, and empty statements
  or misplaced emphasis. These are reader problems even when a human wrote the text. Use E05-E08
  and E25. See [zonderlabs-clarity.md](zonderlabs-clarity.md) for examples and study limits.
- **Eugene Vinitsky, [Bluesky post and discussion](https://bsky.app/profile/eugenevinitsky.bsky.social/post/3mzv6k7hxo22s)**
  (practitioner discussion): Vinitsky describes getting stuck editing machine-drafted prose. The
  replies suggest fixing the outline before polishing and call out public-facing prose that reads
  like a changelog. Use E26 and C21. These are editing suggestions, not measured effects.
- **Bhat et al., [Reactive Writers](https://arxiv.org/abs/2603.10374)** (CHI 2026, human co-writing
  study): interviews with 19 participants and analysis of 1,291 sessions describe how suggestions
  in an opinionated co-writer seeded ideas before people finished forming their own. For E03/E26,
  record the author's intended argument before asking for new framing. The study did not test
  whether an outline fixes ordinary line edits or whether this checklist works.

## Voice and human judgment

- **Dennis D. McDonald, [On Using ChatGPT as a Writing & Research Assistant](https://www.ddmcd.com/managing-technology/thoughts)**
  (first-person essay): a movie review drafted from his notes carried over the ideas but lost his
  voice. He preferred having AI check his own writing for clarity, grammar, and spelling. Use E04
  and E27: keep the author's sentences where they work and leave personal reactions to the writer.
- **Zhang, Bu, and Dhillon, [Who Owns the Text?](https://arxiv.org/abs/2601.10236)** (preprint,
  human study): in a study of 176 participants, tailoring suggestions to a brief writing sample
  partly improved reported ownership compared with suggestions without that tailoring. The
  assisted and unaided conditions used different writing tasks, and ownership is not voice. For
  E04/C20, use a real same-genre sample rather than a persona label or generic style preset.
- **Dennis D. McDonald, [On the Rapid Integration of AI Tools into the Peer Review Process](https://www.ddmcd.com/managing-technology/evolving)**
  (commentary): separate routine checks such as citation and language review from judgments about
  novelty and significance. Use E28: show the evidence for a finding and leave consequential
  decisions to the responsible person. This is a recommendation, not a validation study.
- **Dr. Voss's Biostats email corrections** (direct author feedback): keep `5pm`, announce the
  meeting in the instructor's register, and distinguish the overdue form, optional progress, and
  an unconfirmed lesson. This supports E14-E16 and C19-C20 for his course email. It doesn't show
  how students interpreted either version; no reader comparison was run.

## Meaning and certainty

- **Abdulhai et al., [How LLMs Distort Our Written Language](https://arxiv.org/html/2603.18161v2)**
  (preprint, user study and separate essay revision experiment): heavier users more often said
  the essay didn't sound like them; in the revision experiment, even grammar-only instructions
  allowed changes to essay conclusions. For C19/E23, check the edited passage and its conclusion
  against the original. These essay results do not estimate how often email edits change meaning.
- **Baradziej, [Do large language models keep the hedge?](https://doi.org/10.3389/flang.2026.1953328)**
  (incident-report summarization study): six models summarizing 42 reports tended to harden claims
  without instructions; instructions to preserve uncertainty could instead soften them. For
  E20-E22, compare each final claim's certainty against the source in both directions. The study
  tested summaries, not line editing, and did not validate the humanizer.

## Punctuation and prevalence

- **Kevin Powell, [Bluesky post and discussion](https://bsky.app/profile/kevinpowell.co/post/3mzl3ln2io222)**
  (practitioner discussion): Powell notices that Oxford commas were discussed alongside dashes as
  signals. He later clarifies that he does not intend to change his writing. Use C14: preserve
  effective punctuation and the writer's or publication's conventions.
- **Pew Research Center, [How Much of the Internet Is Written With AI?](https://www.pewresearch.org/data-labs/2026/08/20/how-much-of-the-internet-is-written-with-ai/)**
  (observational study; [methodology](https://www.pewresearch.org/data-labs/2026/08/20/methodology-ai-content/)):
  Pew found changes across samples in the rates of em dashes, Oxford commas, some vocabulary, and
  negative parallelism. Its analysis used English-language Common Crawl pages and one Open Pangram
  threshold and checked agreement with a second Pangram model on a subset. The estimate for
  post-ChatGPT publications is for pages with detectable dates, not all new web pages. Corpus
  patterns cannot identify who wrote a draft. Pew did not test whether changing punctuation helps.
  Use C08, C09, C14, and C24. Preserve effective punctuation instead of applying quotas.

## Detection is a separate question

- **Pangram, [What is Pangram's model trained on?](https://www.pangram.com/knowledge-hub/what-is-pangrams-model-trained-on#initial-training-process)**
  (vendor documentation): Pangram describes training on human and generated samples, expanding
  training with hard-to-classify human examples, and using generated samples matched to human
  ones in content and style. This explains one vendor's approach; it does not independently
  establish accuracy on a new genre or text. Use C24.
- **Grammarly, [How Do AI Detectors Work?](https://www.grammarly.com/blog/ai/how-do-ai-detectors-work/#2)**
  (vendor explainer): some detectors use predictability and variation as signals. These examples
  are neither ingredients shared by all detectors nor targets for revision. False positives and
  false negatives are possible. Use C24.
- **GitHub, [AI content detection projects in Python](https://github.com/topics/ai-content-detection?l=python)**
  (project directory): use it to find candidate tools, then inspect each tool's purpose, inputs,
  language and genre coverage, evaluation, and data handling. A topic tag or star count does not
  validate a tool. Distinguish a style linter from an authorship classifier. Use C24.

## Pattern tools

- **Conor Bronsdon, [Avoid AI Writing](https://github.com/conorbronsdon/avoid-ai-writing)**
  (open-source editing skill): separate a candidate match, a finding supported by context, and an
  edit authorized by the user. Protect quotations, data, code, URLs, and identifiers in ordinary
  cleanup. Use E02 and C23. Borrow the review procedure and exceptions, not punctuation quotas
  or claims about human authorship.
- **Simon Willison, [LLM cliche highlighter](https://tools.simonwillison.net/llm-cliche-highlighter)**
  (pattern matcher): inspect repeated openers and sentence frames, staged reveals, stacked
  questions, and negation chains. Matches can also reflect intentional teaching, technical lists,
  or an author's style. Use C08, C09, C13, and C22. Use only non-sensitive examples in external
  tools unless the author and applicable policy permit sending the text.
- **Nan Xiao, [llm-cliches](https://github.com/nanxstats/llm-cliches)** (curated word lists): use
  examples to spot clusters of vague or overworked words. Keep necessary terms and ordinary words
  that fit. A list of examples is not an estimate of how often a model uses them. Use C02 and C22.
- **GitHub, [rewrite-ai-text](https://github.com/topics/rewrite-ai-text)** (project directory):
  find tools to compare, not evidence of better writing. The listings include two versions of
  [Puneeth Kotha's Humanizer Workbench](https://github.com/puneethkotha/humanizer-workbench),
  including [the aprempeh-tech version](https://github.com/aprempeh-tech/humanizer-workbench).
  Their rewrite, refine, and audit stages suggest reviewing wording separately from final
  fidelity. Check the result against the original after each substantive pass; neither a style
  preset nor a lower heuristic score establishes that the change helped. Use E20 and C24.
