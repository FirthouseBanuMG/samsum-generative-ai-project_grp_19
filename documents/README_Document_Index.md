# SAMSum Group Major Project — Document Index

This is the central index for the SAMSum-based intelligent conversation summarization and action-item extraction project.

## Documentation policy

- **Markdown (`.md`) is the primary editable documentation format.**
- Retained Word (`.docx`) files are source documents or generated deliverables; a Markdown counterpart does not imply exact layout or content parity.
- Files under `99_Historical_Drafts/` are historical references, not automatically current project decisions.
- The original assignment brief is retained as a reference source.
- Do not treat a converted file as fully verified solely because it exists and is non-empty.
- Keep dataset files in `data/raw/` and processed datasets in `data/processed/`, not in this documentation folder.

## Current project status

- Local SAMSum dataset validation and preprocessing have been completed.
- Raw dataset counts: 14,732 training rows (one blank dialogue), 818 validation rows, and 819 test rows.
- Processed dataset counts: 14,731 training rows, 818 validation rows, and 819 test rows.
- The initial smoke test for `Qwen/Qwen2.5-1.5B-Instruct` passed on CPU.
- Initial model smoke testing is not a substitute for baseline evaluation.
- Validation examples were inspected during exploratory review but were not used to generate baseline outputs.
- Initial pipeline verification examples should be selected from the training split.
- The validation split is available for controlled development. A 50-example test subset has already been used for model-family comparison and is not an untouched final holdout.
- The presentation speaking draft, slide source, and generated 10-slide PowerPoint are in `documents/`; speaker assignments and a timed rehearsal remain team-owned.
- Prompt and decoding experiments, structured output validation, tool demonstration, and model comparison now have implementation and saved evidence.
- The SAMSum-specific concise-versus-detailed prompt comparison has also been run on the fixed baseline examples.
- The integrated notebook/demo completed a CPU run; report content/citations were reviewed and the current render is 14 pages total with an 11-page body. Team approval, contribution confirmations, presentation rehearsal, and submission confirmation remain.

## Recommended reading and review order

1. Read the [original assignment brief](04_Reference_Material/Original_Group_Major_Project_Assignment_Brief.md) to establish requirements.
2. Read the [master project plan](01_Project_Planning/Master_Project_Plan.md) for current scope, evidence, and closeout status.
3. Follow the [environment setup guide](02_Environment_Setup/Prerequisites_and_Environment_Setup.md) to reproduce the project environment and data workflow.
4. Review the [architecture](03_Implementation_and_Experiments/01_High_Level_Architecture.md), [dataset acquisition guide](03_Implementation_and_Experiments/05_Dataset_Acquisition_and_Reproducibility.md), and [data quality report](03_Implementation_and_Experiments/Data_Quality_Report.md).
5. Review the [experiment and decision log](03_Implementation_and_Experiments/04_Experiment_and_Decision_Log.md), [model comparison](03_Implementation_and_Experiments/05_Model_Family_Comparison/README.md), and [assignment evidence matrix](03_Implementation_and_Experiments/03_Assignment_to_Evidence_Matrix.md).
6. Review the [technical report](Final_Assignment_Report.md), [presentation notes](Assignment_1_Presentation_Draft.md), and [slide source](Assignment_1_Presentation_Slides.md).
7. Complete the [individual contribution statements](Individual_Contribution_Statements_Template.md) with each member's own confirmed wording; rehearse and record the actual presentation timing.

## Primary project documents

### `01_Project_Planning/`
- `Master_Project_Plan.md` — current master plan, implementation status, 50-example model comparison, and remaining closeout actions.

### `02_Environment_Setup/`
- `Prerequisites_and_Environment_Setup.md` — **single current setup guide** covering software, prerequisites, dataset preparation, VS Code/Jupyter, application run, and tests.

### `03_Implementation_and_Experiments/`
- `01_High_Level_Architecture.md` — architecture and component flow.
- `02_Master_Phase_Plan.md` — phases, milestones, dependencies, and task status.
- `03_Assignment_to_Evidence_Matrix.md` — assignment requirements mapped to evidence.
- `03_Implementation_Guide.md` — original implementation sequence and evidence rules; current run commands are in the environment guide.
- `04_Experiment_and_Decision_Log.md` — experiment records, decisions, rationale, and observations.
- `05_Dataset_Acquisition_and_Reproducibility.md` — reported source, license caveat, integrity fingerprints, and reproducible data workflow.
- `05_Model_Family_Comparison/README.md` — protocol, results, limitations, and rerun caution for the 50-sample comparison.
- `Data_Quality_Report.md` — chronological dataset audits, preprocessing, exclusions, and integrity checks.

### Assignment submission drafts
- `Final_Assignment_Report.md` — technical report with evidence, limitations, and references mapped to the assignment requirements.
- `Assignment_1_Presentation_Draft.md` — timed slide-by-slide speaking draft with a proposed speaker split and demo.
- `Assignment_1_Presentation_Slides.md` — Markdown source for the generated slide deck.
- `Individual_Contribution_Statements_Template.md` — simplified template for each member's short, personally confirmed statement.

### `04_Reference_Material/`
- `Original_Group_Major_Project_Assignment_Brief.md` — Markdown conversion of the original assignment brief.
- The original `.docx` remains available as the source document.

### `05_Templates_and_Repository_Baseline/`
- `README_TEMPLATE.md` — repository README template.
- Other files in this folder provide reusable templates and baseline records.

### `99_Historical_Drafts/`
Markdown conversions of earlier project plans, requirements, and checklists are retained for historical reference. Use the primary documents above for current execution unless a specific historical decision is explicitly adopted.

## Conversion and verification status

- Eight retained Word documents have Markdown counterparts: the implementation guide, experiment log, assignment brief, and five historical planning/checklist documents.
- Three additional Word files are model-comparison deliverables or archived versions and have no same-name Markdown counterpart.
- Markdown is the maintained editable text. Exact Word-to-Markdown content, table, image, and formatting parity has not been established for the complete set.
- The original assignment brief and historical Word documents are retained as references; generated Word deliverables should be reviewed or regenerated when their Markdown sources change.

## Dataset Reproducibility

- [Dataset Acquisition and Reproducibility](03_Implementation_and_Experiments/05_Dataset_Acquisition_and_Reproducibility.md) — expected raw files, source and license checks, checksums, validation/preprocessing commands, split-use policy, and current baseline limitations.
