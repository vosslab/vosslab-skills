# Writing patterns and voice

Use these patterns to diagnose reader problems after the clarity pass. They are examples, not
measured frequencies or authorship evidence. Some inherited examples illustrate a more specific
rewrite. Verify any details they would require before making a similar edit in real prose.

## Match a voice sample

Read the author's sample before editing. Notice sentence length and rhythm, level of formality,
paragraph openings, punctuation, recurring phrases, and transitions. Match those habits where they
fit the new piece. If the author writes short sentences or says "stuff," keep that register rather
than replacing it with longer sentences or more formal words. Without a sample, write for the
reader and genre. Ask for a sample if matching the author's voice is important.

## Preserve the author's voice

Start from the author's sentences, especially for personal judgments and observations. Keep
neutral reporting when it fits the job, and first person when it shows who decided or did
something. Fix repetition that makes a passage hard to follow. Keep parallel steps when they
help the reader compare. Treat an added reaction, anecdote, or attribution as a content change
that needs the author's input, not as a way to make prose sound human.

For an example from author feedback, see the Biostats email in
[ai-writing-checklist.md](ai-writing-checklist.md#what-to-keep-or-change). For the writing sample
study and McDonald's account, see [checklist-sources.md](checklist-sources.md#voice-and-human-judgment).


## CONTENT PATTERNS

### 1. Undue Emphasis on Significance, Legacy, and Broader Trends

**Words to watch:** stands/serves as, is a testament/reminder, a vital/significant/crucial/pivotal/key role/moment, underscores/highlights its importance/significance, reflects broader, symbolizing its ongoing/enduring/lasting, contributing to the, setting the stage for, marking/shaping the, represents/marks a shift, key turning point, evolving landscape, focal point, indelible mark, deeply rooted

**Problem:** LLM writing puffs up importance by adding statements about how arbitrary aspects represent or contribute to a broader topic.

**Before:**
> The Statistical Institute of Catalonia was officially established in 1989, marking a pivotal moment in the evolution of regional statistics in Spain. This initiative was part of a broader movement across Spain to decentralize administrative functions and enhance regional governance.

**After:**
> The Statistical Institute of Catalonia was established in 1989 to collect and publish regional statistics independently from Spain's national statistics office.


### 2. Undue Emphasis on Notability and Media Coverage

**Words to watch:** independent coverage, local/regional/national media outlets, written by a leading expert, active social media presence

**Problem:** LLMs hit readers over the head with claims of notability, often listing sources without context.

**Before:**
> Her views have been cited in The New York Times, BBC, Financial Times, and The Hindu. She maintains an active social media presence with over 500,000 followers.

**After:**
> In a 2024 New York Times interview, she argued that AI regulation should focus on outcomes rather than methods.


### 3. Superficial Analyses with -ing Endings

**Words to watch:** highlighting/underscoring/emphasizing..., ensuring..., reflecting/symbolizing..., contributing to..., cultivating/fostering..., encompassing..., showcasing...

**Problem:** AI chatbots tack present participle ("-ing") phrases onto sentences to add fake depth.

**Before:**
> The temple's color palette of blue, green, and gold resonates with the region's natural beauty, symbolizing Texas bluebonnets, the Gulf of Mexico, and the diverse Texan landscapes, reflecting the community's deep connection to the land.

**After:**
> The temple uses blue, green, and gold colors. The architect said these were chosen to reference local bluebonnets and the Gulf coast.


### 4. Promotional and Advertisement-like Language

**Words to watch:** boasts a, vibrant, rich (figurative), profound, enhancing its, showcasing, exemplifies, commitment to, natural beauty, nestled, in the heart of, groundbreaking (figurative), renowned, breathtaking, must-visit, stunning

**Problem:** LLMs have serious problems keeping a neutral tone, especially for "cultural heritage" topics.

**Before:**
> Nestled within the breathtaking region of Gonder in Ethiopia, Alamata Raya Kobo stands as a vibrant town with a rich cultural heritage and stunning natural beauty.

**After:**
> Alamata Raya Kobo is a town in the Gonder region of Ethiopia, known for its weekly market and 18th-century church.


### 5. Vague Attributions and Weasel Words

**Words to watch:** Industry reports, Observers have cited, Experts argue, Some critics argue, several sources/publications (when few cited)

**Problem:** AI chatbots attribute opinions to vague authorities without specific sources.

**Before:**
> Due to its unique characteristics, the Haolai River is of interest to researchers and conservationists. Experts believe it plays a crucial role in the regional ecosystem.

**After:**
> The Haolai River supports several endemic fish species, according to a 2019 survey by the Chinese Academy of Sciences.


### 6. Outline-like "Challenges and Future Prospects" Sections

**Words to watch:** Despite its... faces several challenges..., Despite these challenges, Challenges and Legacy, Future Outlook

**Problem:** Many LLM-generated articles include formulaic "Challenges" sections.

**Before:**
> Despite its industrial prosperity, Korattur faces challenges typical of urban areas, including traffic congestion and water scarcity. Despite these challenges, with its strategic location and ongoing initiatives, Korattur continues to thrive as an integral part of Chennai's growth.

**After:**
> Traffic congestion increased after 2015 when three new IT parks opened. The municipal corporation began a stormwater drainage project in 2022 to address recurring floods.


## LANGUAGE AND GRAMMAR PATTERNS

### 7. Overused "AI Vocabulary" Words

**High-frequency AI words:** Actually, additionally, align with, crucial, delve, emphasizing, enduring, enhance, fostering, garner, highlight (verb), interplay, intricate/intricacies, key (adjective), landscape (abstract noun), pivotal, showcase, tapestry (abstract noun), testament, underscore (verb), valuable, vibrant

**Marketing and blog clich&#233;s (same tell, different register):** at the end of the day, when it comes to, in a world where, moving forward, circle back, deep dive, game-changer, double down, take a step back, on the same page, make no mistake, it turns out, let me be clear, navigate (for challenges), lean into, unpack (before analysis), straightforward (to describe anything)

**Problem:** A cluster can make prose vague or repetitive. Keep a word that names the right thing.
See [checklist-sources.md](checklist-sources.md) for what corpus comparisons do and do not show.

**Before:**
> Additionally, a distinctive feature of Somali cuisine is the incorporation of camel meat. An enduring testament to Italian colonial influence is the widespread adoption of pasta in the local culinary landscape, showcasing how these dishes have integrated into the traditional diet.

**After:**
> Somali cuisine also includes camel meat, which is considered a delicacy. Pasta dishes, introduced during Italian colonization, remain common, especially in the south.


### 8. Avoidance of "is"/"are" (Copula Avoidance)

**Words to watch:** serves as/stands as/marks/represents [a], boasts/features/offers [a]

**Problem:** LLMs substitute elaborate constructions for simple copulas.

**Before:**
> Gallery 825 serves as LAAA's exhibition space for contemporary art. The gallery features four separate spaces and boasts over 3,000 square feet.

**After:**
> Gallery 825 is LAAA's exhibition space for contemporary art. The gallery has four rooms totaling 3,000 square feet.


### 9. Negative Parallelisms and Tailing Negations

**Problem:** Constructions like "Not only...but..." or "It's not just about..., it's..." are overused. So are clipped tailing-negation fragments such as "no guessing" or "no wasted motion" tacked onto the end of a sentence instead of written as a real clause.

**Before:**
> It's not just about the beat riding under the vocals; it's part of the aggression and atmosphere. It's not merely a song, it's a statement.

**After:**
> The heavy beat adds to the aggressive tone.

**Before (tailing negation):**
> The options come from the selected item, no guessing.

**After:**
> The options come from the selected item without forcing the user to guess.


### 10. Rule of Three Overuse

**Problem:** LLMs force ideas into groups of three to appear comprehensive.

**Before:**
> The event features keynote sessions, panel discussions, and networking opportunities. Attendees can expect innovation, inspiration, and industry insights.

**After:**
> The event includes talks and panels. There's also time for informal networking between sessions.


### 11. Elegant Variation (Synonym Cycling)

**Problem:** Rotating labels can make the reader think the writer means different things.

**Before:**
> The protagonist faces many challenges. The main character must overcome obstacles. The central figure eventually triumphs. The hero returns home.

**After:**
> The protagonist faces many challenges but eventually triumphs and returns home.


### 12. False Ranges

**Problem:** LLMs use "from X to Y" constructions where X and Y aren't on a meaningful scale.

**Before:**
> Our journey through the universe has taken us from the singularity of the Big Bang to the grand cosmic web, from the birth and death of stars to the enigmatic dance of dark matter.

**After:**
> The book covers the Big Bang, star formation, and current theories about dark matter.


### 13. Passive Voice and Subjectless Fragments

**Problem:** A sentence can hide the actor or bury the action in a noun. Use active voice when the actor is known and naming them makes the sentence clearer. Keep useful passives when the actor is unknown, irrelevant, or not the intended focus.

**Before:**
> No configuration file needed. The results are preserved automatically.

**After:**
> You do not need a configuration file. The system preserves the results automatically.


## STYLE PATTERNS

### 14. Punctuation and emphasis

**Problem:** Repeated asides can bury the main clause. Use commas, periods, or parentheses if
they make the point easier to follow. Keep a useful dash and an Oxford comma that fits the
author's or publication's style. Neither is a reason to infer authorship or apply a quota.

**Before:**
> The term is primarily promoted by Dutch institutions&#8212;not by the people themselves. You don't say "Netherlands, Europe" as an address&#8212;yet this mislabeling continues&#8212;even in official documents.

**After:**
> The term is primarily promoted by Dutch institutions, not by the people themselves. You don't say "Netherlands, Europe" as an address, yet this mislabeling continues in official documents.


### 15. Overuse of Boldface

**Problem:** AI chatbots emphasize phrases in boldface mechanically.

**Before:**
> It blends **OKRs (Objectives and Key Results)**, **KPIs (Key Performance Indicators)**, and visual strategy tools such as the **Business Model Canvas (BMC)** and **Balanced Scorecard (BSC)**.

**After:**
> It blends OKRs, KPIs, and visual strategy tools like the Business Model Canvas and Balanced Scorecard.


### 16. Inline-Header Vertical Lists

**Problem:** AI outputs lists where items start with bolded headers followed by colons.

**Before:**
> - **User Experience:** The user experience has been significantly improved with a new interface.
> - **Performance:** Performance has been enhanced through optimized algorithms.
> - **Security:** Security has been strengthened with end-to-end encryption.

**After:**
> The update improves the interface, speeds up load times through optimized algorithms, and adds end-to-end encryption.


### 17. Title Case in Headings

**Problem:** AI chatbots capitalize all main words in headings.

**Before:**
> ## Strategic Negotiations And Global Partnerships

**After:**
> ## Strategic negotiations and global partnerships


### 18. Emojis

**Problem:** AI chatbots often decorate headings or bullet points with emojis.

**Before:**
> &#128640; **Launch Phase:** The product launches in Q3
> &#128161; **Key Insight:** Users prefer simplicity
> &#9989; **Next Steps:** Schedule follow-up meeting

**After:**
> The product launches in Q3. User research showed a preference for simplicity. Next step: schedule a follow-up meeting.


### 19. Curly Quotation Marks

**Check:** Follow the destination's typography. An editor or word processor may supply curly
quotes. Keep correct punctuation rather than changing it to signal human authorship.


## COMMUNICATION PATTERNS

### 20. Collaborative Communication Artifacts

**Words to watch:** I hope this helps, Of course!, Certainly!, You're absolutely right!, Would you like..., let me know, here is a...

**Problem:** Text meant as chatbot correspondence gets pasted as content.

**Before:**
> Here is an overview of the French Revolution. I hope this helps! Let me know if you'd like me to expand on any section.

**After:**
> The French Revolution began in 1789 when financial crisis and food shortages led to widespread unrest.


### 21. Knowledge-Cutoff Disclaimers

**Words to watch:** as of [date], Up to my last training update, While specific details are limited/scarce..., based on available information...

**Problem:** AI disclaimers about incomplete information get left in text.

**Before:**
> While specific details about the company's founding are not extensively documented in readily available sources, it appears to have been established sometime in the 1990s.

**After:**
> The company was founded in 1994, according to its registration documents.


### 22. Sycophantic/Servile Tone

**Problem:** Overly positive, people-pleasing language.

**Before:**
> Great question! You're absolutely right that this is a complex topic. That's an excellent point about the economic factors.

**After:**
> The economic factors you mentioned are relevant here.


## FILLER AND HEDGING

### 23. Filler Phrases

**Before &#8594; After:**
- "In order to achieve this goal" &#8594; "To achieve this"
- "Due to the fact that it was raining" &#8594; "Because it was raining"
- "At this point in time" &#8594; "Now"
- "In the event that you need help" &#8594; "If you need help"
- "The system has the ability to process" &#8594; "The system can process"
- "It is important to note that the data shows" &#8594; "The data shows"


### 24. Excessive Hedging

**Problem:** Over-qualifying statements.

**Before:**
> It could potentially possibly be argued that the policy might have some effect on outcomes.

**After:**
> The policy may affect outcomes.


### 25. Generic Positive Conclusions

**Problem:** Vague upbeat endings.

**Before:**
> The future looks bright for the company. Exciting times lie ahead as they continue their journey toward excellence. This represents a major step in the right direction.

**After:**
> The company plans to open two more locations next year.


### 26. Stacked modifiers

**Words to watch:** third-party, cross-functional, client-facing, data-driven, decision-making, well-known, high-quality, real-time, long-term, end-to-end

**Problem:** Several modifiers in a row can obscure the object or action. Remove vague praise or
move a modifier into its own clause. Keep correct hyphens and technical compound terms.

**Before:**
> The cross-functional team delivered a high-quality, data-driven report on our client-facing tools. Their decision-making process was well-known for being thorough and detail-oriented.

**After:**
> The cross-functional team used data to report on our client-facing tools. The team was known for making decisions carefully.


### 27. Persuasive Authority Tropes

**Phrases to watch:** The real question is, at its core, in reality, what really matters, fundamentally, the deeper issue, the heart of the matter

**Problem:** LLMs use these phrases to pretend they are cutting through noise to some deeper truth, when the sentence that follows usually just restates an ordinary point with extra ceremony.

**Before:**
> The real question is whether teams can adapt. At its core, what really matters is organizational readiness.

**After:**
> The question is whether teams can adapt. That mostly depends on whether the organization is ready to change its habits.


### 28. Signposting and Announcements

**Phrases to watch:** Let's dive in, let's explore, let's break this down, here's what you need to know, now let's look at, without further ado

**Problem:** LLMs announce what they are about to do instead of doing it. This meta-commentary slows the writing down and gives it a tutorial-script feel.

**Before:**
> Let's dive into how caching works in Next.js. Here's what you need to know.

**After:**
> Next.js caches data at multiple layers, including request memoization, the data cache, and the router cache.


### 29. Fragmented Headers

**Signs to watch:** A heading followed by a one-line paragraph that simply restates the heading before the real content begins.

**Problem:** LLMs often add a generic sentence after a heading as a rhetorical warm-up. It usually adds nothing and makes the prose feel padded.

**Before:**
> ## Performance
>
> Speed matters.
>
> When users hit a slow page, they leave.

**After:**
> ## Performance
>
> When users hit a slow page, they leave.


## STYLE, RHYTHM, AND RHETORIC PATTERNS

### 30. Forced Metaphors and Figurative Overwriting

**Signs to watch:** original but strained metaphors, mixed metaphors, figurative substitutions where a plain word is clearer, a metaphor that gets explained right after it is used

**Problem:** Beyond the stock figurative words flagged in patterns 4 and 7, LLMs invent decorative metaphors that add imagery without adding meaning, then often explain them. Plain description is usually clearer and more honest. If the metaphor does not earn its place, cut it and say the literal thing.

**Before:**
> The codebase is a garden we must tend, pruning dead branches and planting seeds of innovation so the whole ecosystem can flourish. In other words, delete unused code and add features.

**After:**
> Delete unused code and add the features users are asking for.


### 31. Dramatic Fragmentation and Punchy Kickers

**Signs to watch:** two- or three-word subjectless sentences used for drama, staccato "X. And Y. And Z." runs, a short quotable line ending every paragraph or section, cutesy appositive fragments ("the catalog, honestly priced")

**Problem:** LLMs chop sentences into fragments for false emphasis and end sections with a quotable "mic-drop" line. It reads like ad copy or a motivational poster. If a line sounds like it belongs on a poster, cut it or fold it back into a real sentence with a subject. This is distinct from pattern 13 (which is about grammatical passive voice); here the tell is rhythm and showmanship, not a hidden actor.

**Before:**
> The catalog, honestly priced. Pay for what it does. Not promises. It just works. Every time.

**After:**
> The catalog is priced by usage, so you pay for the calls you actually make rather than a flat monthly fee.


### 32. Rhetorical Questions Answered Immediately

**Signs to watch:** "What if...?", "The question is...", "Ever wondered...?", a question immediately followed by its own answer, "Think about it."

**Problem:** LLMs pose a question only to answer it a beat later. The question adds no information and stalls the sentence. State the point directly.

**Before:**
> What makes an API good? It comes down to predictability. Think about it: developers want to know exactly what they will get back.

**After:**
> A good API is predictable, so developers know exactly what they will get back.


### 33. Sentence-Opener Tics

**Words to watch:** So..., Look,, habitual sentence-initial And/But, "I think"/"I believe" when stating a fact, adverb openers (Interestingly, Importantly, Notably, Crucially, Essentially, Ultimately)

**Problem:** LLMs lean on a small set of openers. Adverb openers tell the reader how to feel instead of earning it, and "So" or "Look" fake conversational warmth. Drop the opener and start with the substance.

**Before:**
> So, the results were mixed. Interestingly, adoption went up. Importantly, churn went up too. I think that means the feature still needs work.

**After:**
> The results were mixed: adoption rose, but churn rose alongside it, so the feature still needs work.


### 34. Reassurance Kickers

**Signs to watch:** And that's okay., And that's fine., There's nothing wrong with that., no shame in..., you're not alone, it's completely normal

**Problem:** LLMs tack on reassurance the reader never asked for. It softens the writing and assumes the reader needs comforting. Trust the reader: make the point and stop.

**Before:**
> You might not have a testing setup yet. And that's okay. Plenty of teams start without one, and there's nothing wrong with that.

**After:**
> Many teams start without a testing setup and add one once regressions begin costing real time.

---

## Attribution

The clarity pass draws on Zonder Labs' [Why is AI Slop so Frustrating to Read?](https://zonderlabs.com/slop). See [zonderlabs-clarity.md](zonderlabs-clarity.md) for source context and limits. This is a local extension, not independently validated research.

This skill is ported from [blader/humanizer](https://github.com/blader/humanizer) (MIT licensed), which is itself based on [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), maintained by WikiProject AI Cleanup. The patterns documented there come from observations of thousands of instances of AI-generated text on Wikipedia.

Original author: Siqi Chen ([@blader](https://github.com/blader)). Original repo: https://github.com/blader/humanizer (version 2.5.1). Ported to Hermes Agent with Hermes-native tool references (`read_file`, `patch`, `write_file`) and guidance for when to load the skill. The original 29 patterns come from the source, and the before/after examples (including the full worked example) are kept as demonstrations. Patterns 30-34 and the "marketing and blog clich&#233;s" list added to pattern 7 are Hermes additions and are not part of the upstream source. The skill's own instructional prose has also been lightly edited to follow its own guidance (for example, removing em dashes and negative parallelism from the narration) so the skill models the writing it asks for.

Key insight from Wikipedia: "LLMs use statistical algorithms to guess what should come next. The result tends toward the most statistically likely result that applies to the widest variety of cases."
