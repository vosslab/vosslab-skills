# Testing and oracles

Use this reference when building the fixture corpus and oracle comparisons for any CV pipeline or algorithm.

## Fixture corpus

Include at least these cases in the fixture corpus for each task type:

### General (all tasks)

- Clean, representative example that the pipeline handles well.
- Hard negative where no target is present or the scene is empty.
- Domain-edge case: unusual lighting, extreme viewpoint, compression artifacts, or low resolution.
- Boundary case: object at image edge or partially cropped.
- Very small object (less than 5% of frame area).

### Detection

- Multiple overlapping instances of the same class.
- Instances with heavy occlusion (greater than 50% occluded).
- Instance touching the image border.
- Scene with no instances (true negative).

### Segmentation

- Mask that touches the image boundary.
- Two instances with touching or overlapping masks.
- Thin structure (wire, pole, hair strand) where mask continuity is fragile.
- Near-zero-area region.

### Tracking

- Object that exits and re-enters the frame.
- Two objects that cross paths (potential ID switch).
- Scene with stationary objects only (tests false track creation).
- Fast-moving object (motion blur present).

### OCR

- Clean printed text on uniform background.
- Skewed or rotated document.
- Low-contrast text on patterned background.
- Handwritten or stylized font.
- Multi-column or mixed-language layout.
- Compressed JPEG artifact.

### Classical filtering

- Uniform region (filter should not hallucinate structure).
- High-frequency texture (filter should not over-smooth).
- Binary image with thin features (morphological ops must not break connectivity).
- Near-zero signal (dark frame, empty mask).

## Oracles

Validate a custom component against a trusted oracle before declaring it correct.

- OpenCV (cv2): image I/O, geometric transforms, morphological ops, feature detection. Use as
  the reference implementation for classical CV components.
- scikit-image: filtering, thresholding, connected components, region properties. Use as a
  cross-check for preprocessing stages.
- Torchvision: standard data transforms, pretrained model outputs. Use to verify preprocessing
  matches what the model expects.
- COCO evaluation tools (pycocotools): mAP, IoU, precision-recall for detection and segmentation.
- MOT metric suite (motmetrics or TrackEval): MOTA, IDF1, HOTA for tracking evaluation.
- Tesseract or EasyOCR: reference transcription for OCR fixture verification.
- Brute force on small inputs: for detection, manually annotate 20-50 images and compare; for
  segmentation, check IoU against a hand-drawn mask on 10 representative crops.

For brute-force oracles: run both implementations on 50-200 representative inputs, compute the
metric, and assert agreement within a tolerance. Use a fixed random seed for reproducibility.

## Property and stress invariants

Test these invariants in addition to exact-output comparisons:

- Detection: IoU with ground truth is above threshold on held-out fixtures; no boxes with
  zero area or negative coordinates.
- Segmentation: mask coverage matches ground truth within expected tolerance; thin structures
  are preserved (connectivity not broken).
- Tracking: track IDs are consistent within a continuous visible span; MOTA and IDF1 are
  above a stated minimum on a reference clip.
- OCR: character error rate and word error rate are below threshold on the fixture set.
- Classical filtering: output has no introduced NaN, inf, or clipped values; PSNR is above
  a threshold when applied to a paired clean/noisy set.
- Feature matching: inlier ratio after RANSAC is above threshold on fixtures with known overlap;
  reprojection error is below 2 px on fixtures with known homography.

## Inspectable artifacts

Generate at least one inspectable artifact when the pipeline produces visual output:

- Overlay image: input drawn with predictions (boxes, masks, keypoints, track IDs) to reveal
  boundary handling and false positive/negative distribution.
- Confusion sample gallery: a small grid of false positives, false negatives, and borderline
  cases per class or failure mode.
- Precision-recall curve: plotted for the detection or segmentation threshold sweep.
- Track visualization: frame sequence with colored track trails and ID annotations.
- OCR diff: aligned expected vs predicted text highlighting character-level errors.
- Filter comparison: side-by-side input and filtered output for visual quality check.

## Proving improvement in an existing repo

This skill proves a target repo improved, not merely "better" in vague terms. The standard of
proof is:

1. Named held-out set. A fixed annotation file covering 50 or more images (or frames) that was
   not touched during development. This set is the ground truth reference for all before/after
   comparisons.
2. Named oracle. One of: COCO evaluation (pycocotools mAP/IoU), MOT metric suite (MOTA, IDF1),
   character error rate from a reference transcription, or a classical-CV baseline (threshold +
   contour) on the same inputs. The oracle is chosen before the change, not after.
3. Before snapshot. Run the oracle on the held-out set using the pipeline state before the
   change. Record the metric values in a comparison file or the PR description.
4. After snapshot. Run the same oracle on the same held-out set after the change. Record the
   metric values alongside the before values.
5. Hard-case overlays. Produce side-by-side overlay images for at least five cases that were
   failing before the change and are now passing. If no case changed status, state that
   explicitly; do not claim improvement that is not visible.

A task is considered proven when steps 1-5 are all present and the after metric is strictly
better than the before metric on the held-out set.

## Project locations

Place fixtures and artifacts in these standard locations:

- `tests/fixtures/vision/` for fixture files (input images, ground-truth annotations, expected outputs).
- `debug/vision/` for temporary debug artifacts generated during development.
- `docs/images/` for artifacts included in project documentation.
