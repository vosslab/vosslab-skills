---
name: stvc-podcast-update
description: "Use when updating a StVC podcast episode."
version: 0.1.0
author: Neil Voss, Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [podcast, youtube, stvc, workflow]
    related_skills: [youtube-channel-operations]
---

# Update a StVC podcast episode

Use this skill for "update episode N", podcast page changes, or thumbnail work. Confirm the
episode, video, channel, and requested scope before starting. Begin at
`~/wiki/podcast/index.md` or `~/wiki/podcast/README.md` for episode evidence and guides.

## Choose the workflow

Read `~/nsh/stvc-podcast-tools/docs/RECIPES.md` and select the recipe for the requested change.
Recipes cover a new thumbnail, likeness repair, finished artwork publication, title,
description, tags, chapters, a full update, a square playlist cover, a transcript or summary,
and recovery of unfinished work. The wiki request guide is `guides/stvc-request-recipes.md`.
Use the wiki's `guides/stvc-episode-update-runbook.md` and `guides/stvc-episode-update-checklist.md`
for setup and evidence. For supported operations and receipts, use the existing `stvc.py` CLI
and its `docs/USAGE.md`.

- For an episode update, scoped publication, or an uncertain result, read
  [episode_workflow.md](references/episode_workflow.md). It covers the production workspace,
  episode metadata, publication steps, and recovery from partial success.
- For thumbnail generation, visual feedback, likeness or wardrobe revisions, or reference
  delivery problems, read [thumbnail_review.md](references/thumbnail_review.md). For artwork
  publication, also follow the execution and completion sections of the episode workflow.
- Use `youtube-channel-operations` for scoped channel publishing or recovery, and
  `youtube-content` for transcript extraction and transformation when those tasks are needed.

## Verify the result

Carry authorized work through preparation, review, publication, and verification. Keep the
scope, spending, and private-data transfer boundaries from the request. Ground titles,
descriptions, and chapters in the recording. For artwork, inspect the final export before
upload and compare the served public thumbnail with the reviewed result.

Verify intended fields through fresh readback and check that unrelated fields were preserved.
For changed chapters, confirm the native chapter list on the watch page. Use the structured
receipt and a fresh readback to resolve ambiguous publication results before retrying.

Keep working artifacts and receipts in the production workspace. Retain the episode record,
source transcripts or captions, and selected final artwork in the wiki as the recipe directs.
Report completion after verifying the requested live result. Include the video URL, verified
changes, and any unresolved work.
