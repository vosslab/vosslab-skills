# Locate optional book sources

The skill carries concise paraphrases and verified search routes. Full books stay
in the gitignored `references/local-only/` directory and are optional. The source
collection for this survey is `~/nsh/MARKDOWN_BOOKS/game_design/`.

## Corpus and source map

These filenames preserve the supplied editions. Paths are relative to the skill root.

| Key | Author and title | Local corpus path |
| --- | --- | --- |
| Koster | Raph Koster, A Theory of Fun for Game Design (2013) | `references/local-only/A_Theory_of_Fun_for_Game_Design-2013.md` |
| Swink | Steve Swink, Game Feel: A Game Designer's Guide to Virtual Sensation (2009) | `references/local-only/Game_Feel_A_Game_Designers_Guide_to_Virtual_Sensation-2009.md` |
| Fullerton | Tracy Fullerton, Game Design Workshop, third edition (2014) | `references/local-only/Game_Design_Workshop_3rd_Edition-2014.md` |
| Schell | Jesse Schell, The Art of Game Design, third edition (2019) | `references/local-only/The_Art_of_Game_Design_3rd_Edition-2019.md` |

Use [reference_survey.md](reference_survey.md) to choose a term and section.
Search one book with `rg -n -i -F` and inspect surrounding body text rather than
accepting a table-of-contents match as the evidence. Swink's conversion contains
long extracted lines; use bounded text excerpts when a line would flood output.

## When sources are absent

Use the committed decision guidance and the target project's observable behavior.
The books and sibling game repositories are enrichment, not prerequisites. State
when an attribution cannot be checked locally; use available primary documentation
for current platform details rather than treating an older book as an API reference.

Book discussion of human playtesting informs design questions, while this skill's
independent-completion policy comes from the user's direction. Agent assessment
does not replace empirical evidence of human enjoyment or learning. Treat historical
neuroscience claims and numeric response thresholds as claims to verify, not defaults.
