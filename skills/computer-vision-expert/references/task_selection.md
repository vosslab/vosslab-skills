# Task selection

Use this reference when the request says "computer vision" but the actual task is still fuzzy.

## Common task types

- Classification: assign one or more labels to an image or crop.
- Detection: find objects and draw boxes around them.
- Segmentation: assign a mask to objects or regions.
- Keypoints and pose: predict landmarks or skeletal structure.
- Tracking: keep identities over time in video.
- OCR: extract text from images or documents.
- Measurement: estimate lengths, areas, counts, or geometric properties.
- Anomaly detection: identify rare or unexpected visual defects.
- Retrieval or similarity: find visually similar images or regions.

## Decision rules

- If the user cares only whether something is present, start with classification.
- If the user cares where something is, use detection or segmentation.
- If boundaries matter for area, overlap, or precise edits, use segmentation.
- If time consistency matters, the task is not just detection; it likely also needs tracking.
- If the output must drive physical measurement, calibration and geometry matter as much as recognition.

## Clarifying questions to answer internally

- What is the unit of prediction: frame, object, pixel, track, or document field?
- What are the costly mistakes: misses, false alarms, drift, bad masks, or latency?
- Is the environment controlled or highly variable?
- Is the output consumed by a human reviewer, another model, or an automated system?
