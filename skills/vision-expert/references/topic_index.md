# Topic index

This is the routing front door. Start here, match the user problem to a row,
then open the named guide or local book. Book paths are bare text; grep the named
file for the listed keyword to find the passage. Derived from [reference_survey.md](reference_survey.md).

## Problem routing table

| User problem / trigger | CV task | Default algorithm or library | Robustness risks | Best reference |
| --- | --- | --- | --- | --- |
| "Detect X in image" (object present or absent) | Classification / detection | YOLOv8 or RT-DETR for detection; ResNet/EfficientNet for classification | Class imbalance, domain shift, small objects near border | [pipeline_design.md](pipeline_design.md) |
| Small or occluded objects missed | Detection (small objects) | FPN backbone; tiled inference; NMS IoU threshold tuning | Scale mismatch, NMS suppressing small boxes, crowded scenes | [pipeline_design.md](pipeline_design.md) |
| Need per-pixel labels or masks | Segmentation | Mask R-CNN, SAM, or classical contour + threshold | Label ambiguity at boundaries, thin structures, overlapping instances | [pipeline_design.md](pipeline_design.md) |
| Rare class always missed or badly scored | Segmentation (class imbalance) | Focal loss, oversampling, class-weighted loss, balanced batch sampling | Minority class underrepresented, metric dominated by majority | [debugging_and_failure_analysis.md](debugging_and_failure_analysis.md) |
| IDs switch across frames | Tracking (re-ID / ID-drift) | DeepSORT, ByteTrack; appearance re-ID with re-entry logic | ID switches on occlusion, similar appearance, re-entry after gap | [task_selection.md](task_selection.md) |
| Tracker loses object during occlusion | Tracking (occlusion) | Kalman prediction; tracklet gap filling; confidence gating | ID drift, duplicate tracks, trajectory discontinuity | [debugging_and_failure_analysis.md](debugging_and_failure_analysis.md) |
| Extract text from clean images or documents | OCR (standard) | Tesseract, EasyOCR, or PaddleOCR with layout pre-step | Skew, font variety, segmentation failures, low contrast | [task_selection.md](task_selection.md) |
| Text garbled in degraded or historical docs | OCR (degraded docs) | Binarize + deskew before recognition; PaddleOCR layout analysis | Noise, skew, bleed-through, compressed artifacts, mixed scripts | [debugging_and_failure_analysis.md](debugging_and_failure_analysis.md) |
| Image quality or appearance looks wrong | Classical filtering | OpenCV GaussianBlur, morphological ops, CLAHE, bilateral | Over-smoothing, artifact amplification, scale mismatch | [pipeline_design.md](pipeline_design.md) |
| Feature matching or alignment fails | Feature detection / matching | SIFT, ORB, or AKAZE via OpenCV; homography with RANSAC | Repetitive textures, insufficient overlap, scale change | [pipeline_design.md](pipeline_design.md) |
| Camera geometry or calibration problem | Multi-view geometry | OpenCV calib3d (calibrateCamera, findEssentialMat, recoverPose) | Coplanar calibration target, radial distortion, few views | [reference_survey.md](reference_survey.md) |
| Uncertain which CV framing fits | Task selection | -- | Framing mismatch, underspecified success metric | [task_selection.md](task_selection.md) |

## Per-task detail

### Classification and detection

Default to a pretrained backbone with fine-tuning on domain data before building a
custom model. For detection, prefer anchor-free heads when object sizes vary widely.
Oracle: manual annotation of a held-out set; compare model output to human judgments
on hard cases. Books: `references/local-only/Computer_Vision_Algorithms_and_Applications.txt`
(grep `classification`, `detection`), `references/local-only/Learning_OpenCV.txt`
(grep `face detection`).

### Segmentation

Verify that masks are tight at boundaries and that thin structures (wires, poles,
hair) are not suppressed. For interactive or promptable segmentation, SAM provides
a strong starting point. Oracle: pixel-level IoU against a small manually verified
set. Book: `references/local-only/Computer_Vision_Algorithms_and_Applications.txt`
(grep `segmentation`).

### Tracking

Choose single-object or multi-object framing explicitly. For multi-object tracking,
separate detection from association; DeepSORT and ByteTrack decouple these stages.
Handle occlusion, re-entry, and track merge/split explicitly. Oracle: MOT metric
suite (MOTA, IDF1) on a small annotated video clip. Book:
`references/local-only/Video_Object_Tracking.txt`
(grep `tracking`, `Kalman`, `multi-object tracking`).

### OCR

Treat the OCR pipeline as three stages: layout detection, line/word segmentation,
and text recognition. Deskew and binarize before recognizing. Oracle: character
error rate and word error rate on a manually transcribed sample. Books:
`references/local-only/Computer_Vision_Algorithms_and_Applications.txt`
(grep `optical character`), `references/local-only/OpenCV_Cookbook.txt`
(grep `text detection`). For implementation route to Tesseract, EasyOCR, or
PaddleOCR official docs.

### Classical filtering

Use Gaussian blur for noise reduction, bilateral filter when edges must be
preserved, and morphological ops for binary cleanup and connected components.
Match the kernel size to the object scale in the image. Oracle: visual inspection
plus a metric (PSNR or SSIM) on a paired clean/noisy set. Books:
`references/local-only/Learning_OpenCV.txt`
(grep `Gaussian`, `edge detection`), `references/local-only/OpenCV_Cookbook.txt`
(grep `morpholog`, `threshold`).

### Feature matching and homography

Use ORB for speed, SIFT for accuracy, AKAZE for robustness to scale change. Filter
matches with Lowe's ratio test and RANSAC. Oracle: reprojection error on known
correspondences. Book: `references/local-only/OpenCV_Cookbook.txt`
(grep `feature detection`, `SIFT`), `references/local-only/Learning_OpenCV.txt`
(grep `feature detection`).

### Multi-view geometry and calibration

Use a large, sharp checkerboard and at least 15 diverse views covering the full
field of view. Verify reprojection error per-view, not only the mean. For stereo,
verify epipolar constraint residuals. Route to OpenCV calib3d docs for API detail;
see [reference_survey.md](reference_survey.md) for local-book coverage notes.

## Alias and trigger vocabulary

- Detection: object detection, bounding box, find objects, count objects.
- Segmentation: mask, pixel labels, semantic segmentation, instance segmentation, panoptic.
- Tracking: track, follow, identity, multi-object tracking, MOT, SOT.
- OCR: text, read text, document, extract fields, license plate, invoice.
- Filtering: denoise, smooth, sharpen, morphological, threshold, CLAHE.
- Feature matching: align, stitch, register, homography, SIFT, ORB.
- Calibration: camera matrix, distortion, intrinsics, stereo, epipolar.

## Book source map (which book for this problem)

- Broad CV task taxonomy and deep learning methods: `references/local-only/Computer_Vision_Algorithms_and_Applications.txt` (grep `classification`, `segmentation`).
- OpenCV implementation recipes: `references/local-only/Learning_OpenCV.txt` (grep `feature detection`, `Gaussian`).
- Fast implementation patterns: `references/local-only/OpenCV_Cookbook.txt` (grep `morpholog`, `threshold`).
- Tracking algorithms and benchmarks: `references/local-only/Video_Object_Tracking.txt` (grep `tracking`, `optical flow`).
- Multi-view geometry (thin extraction): `references/local-only/Multiple_View_Geometry.txt` (grep `epipolar` to check extraction quality first).
- Algebraic multi-view theory: `references/local-only/Algebraic_Curves_in_Multiple-View_Geometry.txt` (grep `projective`, `trifocal`).
- Where coverage is thin (OCR implementation, calibration API, modern detectors),
  route to official library docs (Tesseract, EasyOCR, OpenCV calib3d, PyTorch Hub).

## New project by shape (greenfield routing)

- Detection pipeline: backbone + YOLOv8 or Faster R-CNN. First fixture: ten images
  with ground-truth boxes, confirmed by mAP baseline and visual overlay.
- Segmentation pipeline: SAM or Mask R-CNN. First fixture: five images with tight
  ground-truth masks, checked by IoU and boundary visualization.
- Tracking pipeline: DeepSORT or ByteTrack. First fixture: a 30-frame clip with
  one occlusion event, annotated track IDs, evaluated by MOTA.
- Classical CV pipeline: OpenCV thresholding and contour pipeline. First fixture:
  three images (clean, noisy, edge case), verified by contour count and area.
- OCR pipeline: Tesseract or EasyOCR with deskew pre-step. First fixture: five
  document crops with known text, verified by character error rate.
- Camera calibration: OpenCV calibrateCamera. First fixture: 15 checkerboard
  images with known pattern size, verified by reprojection error under 0.5 px.
