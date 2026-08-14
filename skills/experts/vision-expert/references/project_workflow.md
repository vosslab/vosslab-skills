# Project workflow

Use this reference when the skill is invoked on a target project, not while building vision-expert.

## Detect project state

Inspect the target repo before writing CV code:
- Search for CV source files (model loaders, inference scripts, pipeline scripts, OpenCV usage).
- Search for evaluation scripts, benchmark results, or metric logs.
- Search for architecture or design docs that describe the task, input format, or success criteria.

If any of these exist, follow the existing-pipeline path. If none exist, follow the greenfield path.

## Existing-pipeline path

1. Inspect the repo before proposing anything. Look for: model weight files or download scripts;
   pipeline stage scripts (preprocessing, inference, postprocessing); a validation or test split
   with annotations; evaluation logs or metric history; and any documented failure cases.
2. Identify the current design by inventorying pipeline stages and recording per-class baseline
   metrics. If no baseline exists, run the pipeline on the available evaluation split first and
   record the numbers. Do not propose changes before the baseline is documented.
3. Propose repo-specific changes tied to a concrete failing case. Each change targets one stage
   at a time and names the fixture or metric that will confirm improvement. Do not offer generic
   advice (for example "try a larger model") that is not tied to a specific observed failure.
4. Prove improvement with before/after evidence. For each change:
   - Record the metric on the held-out set before the change.
   - Apply the change to one stage only.
   - Record the metric again and produce hard-case overlays showing the before/after difference.
   - See [testing_and_oracles.md](testing_and_oracles.md) for oracle and artifact requirements.

## Greenfield path

1. Gather evidence before writing code. Define success in measurable terms: task type, success
   metric (mAP, IoU, CER, FPS), latency budget, and deployment constraints. Read
   [task_selection.md](task_selection.md) if the task type is underspecified. Seed a balanced
   100-500 image set with a held-out test split before any model touches the data.
2. Write a vision contract. Record in a dedicated doc (suggested: `docs/VISION_MODEL.md`):
   - Input resolution and aspect ratio; expected preprocessing.
   - Class taxonomy: all classes, their definitions, and ambiguous boundary cases.
   - FPS and latency budget at target hardware.
   - Miss-vs-false-alarm tolerance: which error is more costly and by how much.
   - Deployment environment: lighting, viewpoint range, expected background variation.
3. Choose the simplest viable pipeline against the vision contract:
   - Is the task geometric, threshold-based, or template-driven? Start with classical CV.
   - Does it require semantic understanding or invariance to lighting/viewpoint? Add a learned model.
   - What is the labeled-data budget? Low budget favors pretrained backbones with minimal fine-tuning.
   - Read [pipeline_design.md](pipeline_design.md) when the classical vs learned tradeoff is unclear.
4. Validate the first version before extending it. The milestone is complete only when all of these
   hold on the held-out test split:
   - End-to-end inference runs on the fixture inputs without error.
   - At least one evaluation metric (from the vision contract) is computed and recorded.
   - At least one visual inspection artifact (overlay image, annotated frame, confusion sample)
     is generated and reviewed, including representative failures.

## CV review checklist

Before closing any CV task, verify:
- The task type and success metric are documented and agreed.
- A baseline result exists and is recorded.
- Hard negatives and at least one domain-edge case are in the fixture corpus.
- Failures are inspected by category, not only averaged into a single score.
- Each pipeline stage has a defined input/output format.
- At least one inspectable artifact (overlay, confusion sample, or metric curve) is produced.
- Speed and memory are measured at expected input size, not only on tiny examples.
- The system has been reviewed on hard negatives and edge cases before declaring it ready.
