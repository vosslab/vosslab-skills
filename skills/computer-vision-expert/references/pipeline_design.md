# Pipeline design

Use this reference when deciding how much of the system should be classical CV, learned modeling, or a hybrid of both.

## Default structure

1. Input acquisition
2. Preprocessing
3. Core vision method
4. Postprocessing
5. Evaluation and visualization

## Classical CV is often enough when

- The scene is controlled.
- The object shape or color is predictable.
- The task is thresholding, edge finding, alignment, contour extraction, or template matching.
- Labeled data is scarce and fast iteration matters more than semantic generalization.

## Learned models are often worth it when

- Lighting, viewpoint, scale, or background varies substantially.
- The task requires semantic understanding.
- Hand-tuned heuristics break across domains.
- Enough labeled data or transfer-learning options exist.

## Hybrid patterns

- Use classical CV for crop generation before a learned classifier.
- Use a detector, then classical geometry or OCR downstream.
- Use segmentation, then domain-specific rules to compute measurements or pass/fail decisions.

## Design rules

- Define each stage's input and output format explicitly.
- Keep visualization hooks between stages.
- Make thresholding and postprocessing configurable and testable.
- Preserve enough metadata to reproduce failures later.

## Local reading order

- Start with [`Learning_OpenCV.txt`](Learning_OpenCV.txt) for broad OpenCV techniques and baseline pipeline ideas.
- Use [`OpenCV_Cookbook.txt`](OpenCV_Cookbook.txt) when you need a more recipe-oriented implementation pattern.
- Use [`Video_Object_Tracking.txt`](Video_Object_Tracking.txt) when temporal identity and tracking dominate the problem.
