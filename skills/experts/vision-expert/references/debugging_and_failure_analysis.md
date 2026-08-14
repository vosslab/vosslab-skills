# Debugging and failure analysis

Use this reference when a CV pipeline works "sometimes" but the failure pattern is unclear.

## Debugging order

1. Verify the task framing and evaluation metric.
2. Inspect raw inputs and annotations.
3. Inspect preprocessing outputs.
4. Inspect predictions visually.
5. Group failures by cause.
6. Change one major variable at a time.

## Common failure buckets

- Label noise or ambiguous ground truth
- Resolution or crop mismatch
- Domain shift between training and deployment
- Class imbalance
- Thresholding or postprocessing errors
- Calibration or perspective problems
- Motion blur, occlusion, glare, or compression artifacts
- Temporal instability in video

## Useful artifacts

- Confusion matrices for class problems
- Precision-recall curves for detection thresholds
- Side-by-side overlays for masks, boxes, or keypoints
- Small galleries of false positives, false negatives, and borderline cases
- Per-scenario metrics by lighting, camera, site, or device

## Rules of thumb

- If errors cluster by environment, suspect data coverage before architecture.
- If the model is confident and wrong, inspect labels and preprocessing.
- If the model is uncertain everywhere, inspect task framing and data quality.
- If latency is too high, profile the full pipeline, not only model inference.
