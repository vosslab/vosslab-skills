# StVC episode execution and recovery

Use this guide when carrying out an episode update or reconciling a failed or uncertain stage.

## Episode knowledge and production workspace

Start discovery at `~/wiki/podcast/index.md` and `~/wiki/podcast/README.md`. The wiki retains
source transcripts/captions in the flat `transcripts/` collection and episode records in
`episodes/episodeNN.md`; Episodes 1-25 remain in grouped block notes. selected final art uses the
flat `thumbnails/episodeNN.jpg` collection. Shared
guidance stays under `guides/`, and host references under `hosts/`. Consult the cleanup
`path-map.json` in `/home/vosslab/nsh/wiki-cleanup-2026-10-30/`
when recovering a moved historical file.

Put new production candidates, masters, prompts, temporary references, previews, checklists and
review evidence in `/srv/samba/share/podcast-production/work/episodeN/`. Keep publication receipts
in `/srv/samba/share/podcast-production/logs/receipts/episodeN/`; playlist receipts use the
`playlist/` subdirectory. Keep credentials external. Copy only the retained episode knowledge and
selected final artwork into `~/wiki/podcast/thumbnails/episodeNN.jpg`; keep later episode records in
`~/wiki/podcast/episodes/episodeNN.md`, with Episodes 1-25 retained in grouped block notes, and
source transcripts/captions in `~/wiki/podcast/transcripts/`. The wiki index owns the
retention boundary; production history does not become permanent wiki content.

## Three connected homes

- **Wiki:** `~/wiki/podcast/README.md` connects episode evidence, editorial guidance, and the
  thumbnail workflow.
- **Skills:** this skill owns full episode/art orchestration; `youtube-channel-operations` owns
  scoped publishing/recovery; `youtube-content` owns transcript extraction and transformation. Load
  a companion with `skill_view(name="...")` when its work is needed. All three sources are under
  `~/.hermes/skills/media/<skill-name>/SKILL.md` and link back to the wiki and code.
- **Code:** `~/nsh/stvc-podcast-tools/` is the existing execution path. Read `docs/USAGE.md` and use
  `stvc.py thumbnail download/export/validate`, metadata setters, package preview/apply, and receipt
  verification after `source source_me.sh`. Use `thumbnail export` for already-lettered full-bleed
  art; `thumbnail compose` is the separate-band option. Creative generation remains the native image
  tool; visual review remains evidence-based agent work. `docs/COOKBOOK.md` and
  `devel/worked_examples.py` provide runnable synthetic offline examples of recovery decisions.
  Reuse these tools rather than rebuilding supported operations in scratch scripts.

## Read the authoritative docs

The user's preferred discovery entry point is `~/wiki/podcast/`, especially
`~/wiki/podcast/README.md`; the skill name need not appear in the request. That index, the series
overview, the runbook, and the thumbnail guide cross-reference this skill. When a request points to
that folder for episode updates or artwork, use this skill together with its linked wiki guides.

Use `read_file` on these paths; follow their current instructions rather than reconstructing the
workflow:

- `$HOME/wiki/podcast/guides/stvc-episode-update-runbook.md` - start here: setup, evidence,
  commands, recovery.
- `$HOME/wiki/podcast/guides/stvc-episode-update-checklist.md` - per-episode evidence and completion
  gate.
- `$HOME/nsh/stvc-podcast-tools/docs/USAGE.md` - exact CLI flags, defaults, receipts, and
  limitations.
- `$HOME/wiki/podcast/guides/stvc-youtube-episode-page-guide.md` - title, description, chapters,
  tags, manifest fields.
- For images: `guides/stvc-youtube-episode-thumbnail-guide.md` and
  `guides/stvc-nano-banana-thumbnails.md` - prompt through publication, references, realistic
  portrait treatment, and positive example prompts.
- For cast/copy: `stvc-host-backgrounds.md` and `stvc-new-viewer-welcome.md` at the wiki podcast
  root, and `guides/stvc-guest-intake.md`.

## Grounded gates and tests

- [ ] Start from the requested user-visible outcome and demonstrated failure. Keep a gate only when
      its failure identifies a consequential problem and leads to a concrete repair, recovery, or
      scoped stop.
- [ ] Compare edited metadata with reviewed intended values, using documented API normalization;
      preserve meaningful fields outside scope. Improvement does not require old/new content
      equivalence.
- [ ] Use the existing local asset hash to bind approved upload bytes. Assess generated likeness and
      public CDN artwork visually; source/generated and local/CDN pixel equality are different
      questions and normally irrelevant.
- [ ] Treat preview size, editorial counts, and retry batches as operational defaults. Use actual
      platform constraints and observed compatibility rather than arbitrary timing, version, or
      attempt-count gates.
- [ ] Prefer the existing commands, records, and fixed shared behavior. Add configuration or
      mechanisms only for a demonstrated need; preserve useful operation through contextual recovery
      and optional omissions.
- [ ] For code changes, read the repository's `docs/REPO_STYLE.md`, `docs/PYTEST_STYLE.md`,
      `tests/TESTS_README.md`, and `devel/DEVEL_README.md`. Use the permanent-test checklist before
      retaining coverage: stable important behavior, plausible regression, precise enough for the
      contract, actionable failure, and lasting value beyond implementation proof. Extend an
      existing test when sufficient; use ignored `tests/_temp/` for one-time checks and remove or
      promote them at closeout.
- [ ] Treat executable worked examples as teaching material, editorial comparisons as visual
      evidence, and live publication checks as operational evidence. Each proves its own scope;
      synthetic examples do not establish a working provider or published outcome.
- [ ] Phrase instructions around desired actions and omit irrelevant alternatives. Keep explicit
      boundaries for real authority, privacy, and data-integrity risks.

## Robust completion

Use the runbook's robustness policy as the canonical decision contract. Preserve useful operation
when inputs or state are imperfect: classify the impact, choose the best safe recovery, record the
assumption, and continue the next implied step. Each gate earns its place by identifying a real
correctness problem and specifying a concrete recovery or terminal decision.

Routine milestones belong to the manager and reviewing agents, supported by existing validators and
live readback. Carry an authorized update through publication without renewed human editorial
approvals. Establish real scope and spending authorization at entry. The user explicitly authorizes
rehosting existing already-public host portraits in public, unlisted storage for current and future
podcast references; reuse that permission and the local reference registry. Newly private photos or
unrelated personal material remain separate transfer decisions. Keep actual denials and privacy
boundaries intact, and continue independent authorized work when one action is blocked.

Reuse explicit user-confirmed cast and corrected manifests. Treat uncertain optional names, mascot
details, and guest biographies as omissions, not reasons to invent another participant or stop
publication. Recover likeness references from existing approved portraits or adequate public episode
artwork; document a weaker reference basis. Ask only when a required fact remains unrecoverable and
materially affects the requested result.

## Recovery without optional dependencies

For routine execution and invisible Open WebUI approval prompts, follow the "Use the established
execution path" checklist in `~/nsh/stvc-podcast-tools/docs/TROUBLESHOOTING.md`. Use focused
repository commands after `source source_me.sh`, dedicated file tools, and
`stvc.py thumbnail download` for generated or public-CDN image bytes. Carry routine authorized
stages through existing review and readback. Diagnose a real runtime gate at its exact scope and
preserve its stop instructions; task authorization and tool acknowledgment are distinct.

An episode-update request owns the end-to-end outcome, not just preparation. Use the established
`stvc.py` commands for download, export, validation, preview, apply, verify, and fetch. Review
existing images directly with the image tool or give their existing paths to a reviewing agent.
Comparison-sheet generation is optional presentation work, never a publication dependency; keep ad
hoc inline-interpreter image manipulation out of the normal path.

An actual denied/timed-out action stays paused until renewed authorization; preserve its exact scope
and respect the tool's stop instructions. Record what did and did not run. Once authorized to
resume, continue from retained artifacts rather than redoing generation or reopening confirmed cast.
Optional artifact failure does not establish a defect in the final image. Preserve global safety
settings; broad allowlists or disabling approvals are not pipeline repairs.

`apply` and `verify` can exit 2 when a thumbnail was accepted and still needs visual readback. Read
the JSON result and receipt. Run subsequent read-only fetch/CDN inspection as separate commands
instead of chaining them with `&&` after that expected status. Never turn this exit code into a
duplicate upload. If a normal apply returns metadata mismatch with thumbnail pending, first run
read-only verification. Once metadata matches, establish from the normal return path and operation
evidence that thumbnail dispatch never occurred; then reapply the same reviewed plan so metadata is
a noop and only the outstanding image is uploaded. A generic tool-loop warning based on exit 2 does
not override the structured receipt; inspect actual state rather than treating
accepted-but-unverified as failed. Completion uses fresh intended-field comparison and preservation
checks, plus public image inspection for artwork scope and description/link/chapter checks for the
corresponding page scope.

## Execute

For the user's preapproved start-to-finish requirement, first read
`~/nsh/stvc-podcast-tools/docs/UNATTENDED_PIPELINE.md`. Use the supported `captions`, `transcript`,
`reference board`, `reference upload`, and WebP `thumbnail export` operations for preparation. Run
`source source_me.sh` once separately, then one
`python3 /home/vosslab/nsh/stvc-podcast-tools/stvc.py ...` command per terminal call. Workers use
these same commands and file tools, not inline Python or shell snippets. The scoped allowlist covers
named application entry points; global smart approvals remain enabled. A routine approval prompt is
a pipeline defect to repair, not a recurring human milestone. Actual denials remain pauses until
renewed authority. Native image/browser/vision tools own generation and review. Read the complete
timestamped transcript output before writing copy.

1. Confirm the exact episode/video/channel and requested scope. For lightweight latest-episode
   discovery, fetch the official playlist Atom feed at
   `https://www.youtube.com/feeds/videos.xml?playlist_id=PLAYLIST_ID`; use its entry ID, title,
   publication time, and thumbnail URL as discovery evidence. Do not treat feed order as publication
   eligibility: reconcile the candidate against the channel state and its scheduled/live status
   before choosing an episode. Resume its checklist under
   `/srv/samba/share/podcast-production/work/episodeN/reviews/` or create one from the template;
   archived state copies remain historical evidence.
2. Use `terminal` from the repository after `source source_me.sh`. Follow the runbook with `stvc.py`
   and its dedicated setters; use `launchers/set_tags.py` for tags-only changes. Keep commands and
   editorial conventions owned by their docs.
3. Ground copy and chapters in recording evidence. Treat automatic transcript speaker labels and
   adjacent greetings as attribution evidence only, not proof of a participant's identity:
   corroborate cast names against the visible recording, roster references, or a supplied portrait
   before adding a name to the manifest. Describe desired imagery positively; use the preferred
   portrait references and compare facial rendering as a separate quality check. When preparing a
   newly supplied portrait, build a labeled original-photo board, visually inspect that every face
   and defining hair/identity feature has usable framing, and correct the source crop before public
   reference hosting or generation. A board filename and manifest do not prove that the reference is
   fit for likeness work.
4. Before approving a thumbnail, inspect its final 1280x720 export with YouTube's lower-right
   duration-badge safe area in mind. Move or shorten text that could be obscured; technical image
   validation alone does not establish publishability. Do not use a watch-page player as proof of
   listing-tile badge placement, because the player does not render the standard static duration
   overlay; retain the safe-area review as the decisive check. After upload, fetch the served CDN
   image with a cache-busting query and compare recognizable composition, headline, cast, and safe
   area with the accepted export; normal CDN resizing and recompression do not require pixel
   equality.
5. Carry authorized updates through preparation, agent review, publication, and verification.
   Routine milestones use agent assessments and existing validators. Dry runs are optional
   diagnostics. Preserve explicit scope, tool-denial, and private-data-transfer boundaries.
6. If a factual correction changes cast, copy, or other manifest data after an earlier write, update
   the authoritative episode manifest and rendered copy, publish only the corrected intended fields,
   and verify against that corrected artifact. Do not call an earlier draft a full match after its
   source facts changed.
7. Keep production candidates, native masters, original-photo/gameplay references, review copies and
   upload derivatives in `/srv/samba/share/podcast-production/work/episodeN/`; put operation
   receipts in `/srv/samba/share/podcast-production/logs/receipts/episodeN/`. Retain episode records
   in `~/wiki/podcast/episodes/episodeNN.md`; Episodes 1-25 remain in grouped block notes; source
   transcripts/captions are collected under `~/wiki/podcast/transcripts/`; save selected final art
   as `~/wiki/podcast/thumbnails/episodeNN.jpg`. Keep `episode.json`, `info.json`, publishing
   manifests, and pipeline copies in the production workspace. Preserve rejected candidates and
   their quality findings in production records without presenting them as accepted references.
   Resume the first unfinished stage after a failure. Reconcile uncertain writes through a fresh
   `stvc.py fetch` readback and compare every intended field. Normalize the documented YouTube
   representations before declaring a mismatch: a terminal description newline can be removed and
   tags can be reordered, so compare description after terminal-newline normalization and tags as an
   exact set plus count. Do not retry a setter solely for those representations; a fresh readback
   may already prove the intended state. A setter receipt that reports verification is not the final
   completion gate if independent readback was not obtained.

## Completion gate

After publication, read back the fields in scope and verify preservation of unrelated meaningful
state. For a full episode update, the intended description is nonempty; a thumbnail-only correction
preserves the existing description rather than introducing a new content prerequisite. For artwork,
compare the current public image with the accepted scene and preferred face style, allowing normal
resizing/recompression. When publishing or changing chapters, open the public watch page, expand the
description, and open the native chapter panel or "View all" list; confirm every intended chapter
title and timestamp there, because description text alone does not prove native chapter navigation.
For a thumbnail-only revision, verify preservation of the existing snippet, status and content
details through fresh API readback rather than repeating the full description/chapter editorial
review; unchanged metadata does not require republication. Reuse adequate fresh evidence across
checklist rows; record the exact unresolved surface and continue independent useful work.

Report COMPLETE only when the requested live outcome is verified. A prepared draft, accepted upload,
or finished subagent is intermediate progress. Report the video URL, verified changes, and exact
remaining work. Repair demonstrated documentation gaps in the canonical docs so the next agent can
repeat the workflow.
