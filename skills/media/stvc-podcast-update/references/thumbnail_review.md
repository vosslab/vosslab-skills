# StVC thumbnail review and repair

Use this guide for artwork requests, including thumbnail generation, cast or wardrobe revisions,
reference delivery, and likeness review.

Follow the wiki's `guides/stvc-youtube-episode-thumbnail-guide.md` and
`guides/stvc-nano-banana-thumbnails.md` for the image workflow and prompt examples.

## Respond to feedback

Use `~/nsh/stvc-podcast-tools/docs/TROUBLESHOOTING.md` when the user rejects facial
realism/likeness/integration, requests explicit X/Y/Z content, or reports a failed stage. It maps
feedback to inspection, concrete recovery, positive prompt examples, and verification. For X/Y/Z,
record each requested element and relationship, give it a visible role, and verify it in the actual
output. Describe the desired image positively; review the full result and then resume the matching
recipe. The wiki entry is `~/wiki/podcast/guides/stvc-request-recipes.md`.

For persistent painted-face style lock, use the portrait-board-only recovery in
`docs/TROUBLESHOOTING.md` under "Recover painted-face style lock". Inspect the liked composition,
describe its positions/actions/wardrobe/project shapes/lettering in text, and generate from original
portraits as the sole image input. This removes the stylized image's influence while preserving the
concept. Verify likeness, scene preservation and head/body integration separately; this is a
regenerated interpretation, not pixel-preserving editing.

### Discuss or revise culturally informed wardrobe

1. Distinguish a historical/style question from an instruction to revise artwork. Answer curiosity
   and offer a concrete styling direction without generating or replacing an accepted thumbnail;
   speculative preferences attributed to a host do not establish that host's approval.
2. Inspect the accepted image before proposing wardrobe changes. Identify the visible garments and
   coverage, then describe a scoped change that preserves the liked composition, recognizable face,
   and existing coverage. Do not invent details hidden by the crop.
3. For historical questions, retrieve dated evidence and distinguish presence in America from
   presence in the Western frontier, and classic Old West dates from later homesteading. Separate
   evidence about religious practice from evidence about clothing; a pioneer's biography does not
   establish what she wore. State when a proposed outfit is a modern thematic interpretation rather
   than a documented reconstruction.
4. Translate the theme into specific garments without treating religion as a uniform. For a modest
   Western look, consider a felt cowboy hat over the existing headscarf, loose long sleeves, and a
   longer Western vest or duster; preserve hair and neck coverage shown in the reference unless a
   change is requested. Treat these as design options, not a declaration of religious compliance or
   the host's personal standards. If an edit is requested, verify the actual clothing coverage,
   unobstructed likeness, and accessory fit in the generated image before publication.
5. Once the user requests the discussed revision, use the accepted artwork as composition authority
   and the inspected labeled original-photo board as identity authority. Map each person's requested
   role to concrete wardrobe, expression and props while preserving the successful scene, headline
   and anatomy. Translate film-character inspiration into the host's own eccentric styling rather
   than substituting an actor's face; a heroic cowboy role does not require adding weapons or
   replacing the scientific activity with an action scene. Inspect the native candidate, then export
   and review the full-size and mobile versions before a thumbnail-only publication. Preserve the
   previous accepted image in production, verify the replacement on the public CDN, and update only
   the selected wiki artwork and relevant episode knowledge.

## Likeness and integration

The target is recognizable, lifelike hosts convincingly integrated into the scene. Evaluate likeness
and integration separately and require both; a request for faithful likeness does not by itself
request unchanged source pixels. Use `/srv/samba/share/wiki/podcast/great-faces.jpg` as the user's
preferred face/integration example, `decent-faces.jpg` as the intermediate example, and
`bad-photoshop-faces.jpg` as the rejected pasted-face treatment. These examples establish rendering
quality, not episode layout or cast. Improve head/body integration with matched light direction,
color temperature, perspective, neck contact shadows, and edge softness. An accepted result stays
published unless another revision is requested. When realism is requested, prompt positively for
lifelike adult anatomy, continuous skin tones, natural texture, believable materials, and motivated
lighting. Compare the actual image beside the labeled photographic reference board and preferred
rendering example, separately from technical validation and upload acceptance. Check that defining
identity cues are used correctly, not merely present somewhere: eyeglasses held as a prop do not
replace glasses normally worn on the face. Recover that scoped cue while preserving successful
integration and the other hosts. Use an independent reviewer when available or an equivalent
evidence-based assessment; reviewer availability alone is not a blocker. Evaluate the requested face
realism within the intended imaginative game world; a literal photographic setting or forensic
identity proof is a different requirement. Keep review findings actionable: significant likeness
drift, insufficient face realism, broken anatomy, incorrect headline, or important content covered
by the duration badge. Judge mobile legibility against the promotional purpose: the headline, faces
and requested role cues must read, but small scientific marks need not be individually countable
unless the thumbnail is explicitly a counting puzzle. A reviewer's off-scope objection is not a new
acceptance criterion; record why it does not require a revision. Decorative scenery in the badge
corner alone is not a blocker.

When a host rejects a likeness, do not infer or prompt an ethnicity from appearance or a name. Use
the wiki's original photograph and describe only observable features. A reference-guided generator
still redraws faces: never call its output an unchanged original-photo composite. If it keeps
altering facial proportions, change the reference or composition strategy while retaining the
likeness requirement. Deterministic original-photo compositing is a separate technique, not
automatic recovery or proof of visual success. Use it when unchanged source pixels are explicitly
requested or the composite actually meets both likeness and integration criteria; document source
hash, placement, mask, and any color adjustment. Review duplicate features, seams, scale, lighting
and public served pixels. Do not silently trade away integration to satisfy pixel provenance.

Treat `great-faces.jpg` as a final rendered example for output-quality comparison. Follow the wiki's
actual source recipe: a labeled original-photo identity board plus an actual project/gameplay
screenshot for a new scene; the candidate plus a needed correction board for an edit. Original
portraits establish identity, episode evidence establishes the project, and the finished example
helps assess rendering and integration. Review facial rendering, likeness, and integration
separately; successful integration alone leaves a rejected rendering unresolved.

For more than three faces, use one labeled original-photo identity board within the route's actual
image-input cap, and explicitly map each identity to its scene position and action. Distinguish
unique people from intentional repeated appearances. Episode 35's demonstrated
five-identity/seven-appearance recipe is in `~/wiki/podcast/guides/stvc-nano-banana-thumbnails.md`,
"More than three faces: demonstrated Episode 35 recipe"; this is not a three-face provider limit or
an unlimited-cast guarantee. After a targeted identity-cue repair, inspect related hands and props
too: adding worn glasses can leave a second pair held in a hand. Describe the desired complete
action positively (glasses worn, hands on steering control), then verify the actual output. Record a
user-tolerated inconsistency without regenerating an accepted image unless requested.

For an all-cast likeness revision, inspect alternate wiki-listed originals before reusing the same
board; a clearer frontal portrait can materially improve the input over a webcam crop. The user
rejected `episode35/all-faces-original-board-v2.jpg` as insufficient for new Episode 36 work;
rebuild an episode-specific board from inspected originals rather than treating that historical
board as an approved default. Verify the actual identities in a saved board, not just its filename
or prior manager's description. Give the rebuilt original-photo board primary identity authority and
the existing artwork composition authority. If the requested Nano Banana pass still changes rejected
facial geometry, preserve the candidate and diagnose the reference/scene conflict rather than
automatically pasting original-photo masks. Consider a fresh coherent scene from the original
portraits instead of repeatedly locking an unsuccessful scene; retain episode requirements and
spending limits. Review final integration beside both the source board and the preferred rendering
example; intentional repeated stunt appearances are not accidental duplicate-face defects.
Distinguish a generated pass followed by original-pixel compositing from a claim that generation
preserved original pixels. Reaching an actual resource limit establishes an unresolved attempt, not
that better output is impossible.

For a host-specific likeness repair, lock the already-approved people, scene, props, and lettering
in the prompt, and name the sole person whose face may change. Use the original portrait of that
host as the identity authority; preserve its face orientation, proportions, hair, glasses, age cues,
and natural asymmetry rather than accepting a generic attractive approximation. If the generation
route has limited reference-image slots or an individual reference cannot be delivered promptly, use
an existing approved labeled composite board containing that host; do not delay a scoped repair on
redundant rehosting. Independently inspect the generated export and the public CDN image. Model
visual assessment is evidence, not final authority over personal likeness: if the depicted host
rejects the likeness, treat that as an unresolved quality failure, perform the next authorized
targeted revision, and do not report the thumbnail as complete merely because it passed technical or
agent review.

Start with one candidate and revise observed consequential defects within the existing spending/time
authorization. When successive edits retain a painted or generic facial treatment, stop
reference-editing that candidate: build or verify a labeled board from the original portraits,
generate a fresh coherent scene from that board, and specify the retained composition, cast
positions, actions, world elements, and lettering in the brief. Use the failed candidate only as a
composition reference when its identity rendering is not being inherited by the route; otherwise it
can perpetuate the defect. Inspect the new native output before exporting or publishing. Continue a
concrete authorized recovery while it makes useful progress; use actual resource/authority limits
and evidence of stalled progress to decide when to stop, rather than treating a fixed attempt count
as proof of impossibility. Preserve completed metadata while image work continues. Keep the current
live image until a suitable replacement is ready and report any unresolved required visual outcome
accurately.

## Current local reference delivery

- [ ] Inspect the installed image-source resolver before hosting references. The current
      `tools/image_generation_tool.py` `_inline_fal_sources` resolves local source paths into
      guarded inline data URLs on the local backend and fits their combined payload to the managed
      gateway budget.
- [ ] Prefer native `image_generate` with inspected local original-photo and project-image paths
      when that resolver is installed. Existing public-host-portrait transfer permission still
      applies; local input sends image bytes to the configured image provider.
- [ ] If direct HTTPS reference fetches are rejected by FAL despite successful local GETs, retry
      using this supported local-source delivery rather than rehosting repeatedly or changing the
      billing route. Save exact arguments and returned result; successful native generation
      establishes that source delivery worked.
- [ ] Keep older direct-URL recipes as historical fallbacks for installations without local
      inlining; verify the installed implementation instead of treating the older local-path warning
      as current fact.

## Image provider availability

When image generation is absent from the current tool catalog, distinguish tool exposure from
provider readiness. An existing Image Studio runner's `--check` proves registration/model only, not
authentication. Check `hermes portal info` and `hermes portal tools` before paid invocation; a
configured Nous model can coexist with a logged-out Portal. Retain prepared art and complete
independent metadata when login is genuinely unavailable. Keep the configured billing route and
credentials unchanged; provider restoration is a separate authorization decision.
