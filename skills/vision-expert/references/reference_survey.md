# Reference survey

This is the committed coverage map for the 6 local-only book conversions in
`references/local-only/`. It is the source of truth for routing CV topics to the
right local text. Each topic lists the books that cover it, a reliable grep term
(validated against the conversions), and the coverage strength. The books are flat
text with no headings, so locate a passage by grepping the named file for a listed
term. See [local_books.md](local_books.md) for a brief annotated list of the same books.

## How to use this survey

- Pick the topic, open the strongest book listed, and grep it for the term.
- When the survey marks coverage thin or partial, treat the books as secondary and
  lean on official library docs (OpenCV, PyTorch, Tesseract, COLMAP), trusted
  benchmarks, and brute-force or oracle testing.
- For implementation tasks, verify current library APIs from official docs or the
  installed package before writing API-level code. For conceptual planning, name
  the library and its role without API detail.
- When a book file is absent (gitignored, clean clone), skip it and go directly to
  the official docs or an oracle; the survey routes stay valid, the books are optional.

## Topic-to-reference map

### Task selection

Coverage: strong (Computer_Vision_Algorithms_and_Applications), partial (Learning_OpenCV).

- `references/local-only/Computer_Vision_Algorithms_and_Applications.txt` broad taxonomy
  of CV tasks and applications. grep `classification`, `segmentation`, `detection`.
- `references/local-only/Learning_OpenCV.txt` task framing in OpenCV-tool terms
  (feature-based vs model-based, practical scope). grep `feature detection`.

### Classical filtering

Coverage: strong.

- `references/local-only/Learning_OpenCV.txt` smoothing, edge detection, spatial filters
  with practical OpenCV recipes. grep `Gaussian`, `edge detection`.
- `references/local-only/OpenCV_Cookbook.txt` morphological operators and threshold
  recipes ready to adapt. grep `morpholog`, `threshold`.
- `references/local-only/Computer_Vision_Algorithms_and_Applications.txt` theory behind
  image formation and filtering. grep `Gaussian`.

### Detection and segmentation

Coverage: strong.

- `references/local-only/Computer_Vision_Algorithms_and_Applications.txt` broad coverage
  of detection architectures, semantic segmentation, and instance segmentation concepts.
  grep `detection`, `segmentation`.
- `references/local-only/Learning_OpenCV.txt` OpenCV-specific detectors, cascade
  classifiers, and practical face and object detection patterns. grep `face detection`.
- `references/local-only/OpenCV_Cookbook.txt` feature-based detection recipes.
  grep `feature detection`, `SIFT`.

### Tracking

Coverage: strong.

- `references/local-only/Video_Object_Tracking.txt` dedicated text on single-object
  and multi-object tracking, tracker families, benchmarks, and evaluation protocols.
  grep `tracking`, `Kalman`, `correlation filter`, `optical flow`, `multi-object tracking`.

### Multi-view geometry

Coverage: thin (Multiple_View_Geometry extraction unreliable; Algebraic_Curves partial).

- `references/local-only/Multiple_View_Geometry.txt` intended source for epipolar
  geometry, homographies, camera calibration, and stereo. The present text extraction
  is unreliable; do not rely on it for content lookup until the source is re-exported.
  grep `epipolar` to spot-check extraction quality before trusting any passage.
- `references/local-only/Algebraic_Curves_in_Multiple-View_Geometry.txt` algebraic
  treatment of multi-view curves and projective geometry. grep `projective`, `trifocal`.
- For implementation, route to official OpenCV calib3d docs, COLMAP documentation,
  and the installed package references; treat these books as secondary support.

### OCR

Coverage: partial (Computer_Vision_Algorithms_and_Applications brief intro); thin elsewhere.

- `references/local-only/Computer_Vision_Algorithms_and_Applications.txt` survey-level
  introduction to optical character recognition. grep `optical character`.
- `references/local-only/OpenCV_Cookbook.txt` a text detection recipe using OpenCV.
  grep `text detection`.
- For implementation, route to Tesseract, EasyOCR, or PaddleOCR official docs and
  treat the books as background context only.

## Weak-coverage decision (in scope, books secondary)

Multi-view geometry and OCR are in scope for this skill but thin in the local books.
For these topics, route to official library docs (OpenCV calib3d, COLMAP, Tesseract,
EasyOCR), trusted benchmarks, brute-force oracles, and first-principles reasoning.
Treat the local books as secondary support when the text is present and legible.
