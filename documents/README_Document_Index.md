# SAMSum Group Major Project — Document Index

This is the central index for the SAMSum-based intelligent conversation summarization and action-item extraction project.

## Documentation policy

- **Markdown (`.md`) is the source of truth for project documentation.**
- Word copies of active project guides and reports are removed after their useful content is consolidated into Markdown. The original assignment brief and selected historical Word archives are retained as source records, not as editable project documentation.
- Files under `Historical_Drafts/` are historical references, not automatically current project decisions.
- The original assignment brief's `.docx` is retained as the source artifact; its Markdown conversion is the searchable reading copy.
- Do not treat a converted file as fully verified solely because it exists and is non-empty.
- Keep dataset files in `data/raw/` and processed datasets in `data/processed/`, not in this documentation folder.

## Current project status

- Local SAMSum dataset validation and preprocessing have been completed. Raw-integrity, processed-data, and split-leakage checks passed on 31 October 2026.
- Raw dataset counts: 14,732 training rows (one blank dialogue), 818 validation rows, and 819 test rows.
- Processed dataset counts: 14,731 training rows, 818 validation rows, and 819 test rows.
- The initial smoke test for `Qwen/Qwen2.5-1.5B-Instruct` passed on CPU.
- Initial model smoke testing is not a substitute for baseline evaluation.
- Validation examples were inspected during exploratory review but were not used to generate baseline outputs.
- Initial pipeline verification examples should be selected from the training split.
- The validation split is available for controlled development. A 50-example test subset has already been used for model-family comparison and is not an untouched final holdout.
- The presentation speaking draft, slide source, and generated 10-slide PowerPoint are in `documents/`; a proposed speaker split and one-minute demo plan are ready for team confirmation.
- Prompt and decoding experiments, structured output validation, tool demonstration, and model comparison now have implementation and saved evidence.
- The SAMSum-specific concise-versus-detailed prompt comparison has also been run on the fixed baseline examples.
- The latest offline test suite passed all 66 tests. A separate fresh CPU run of the integrated CLI and notebook also completed on 31 October; the demo continues to flag the known commitment omission.
- The report's last recorded render is 14 pages total with an 11-page body (29 October 2026); re-render after report content or layout changes. Final team approval, contribution confirmations, and presentation rehearsal remain.

## Recommended reading and review order

1. Read the [original assignment brief](Reference_Material/Original_Group_Major_Project_Assignment_Brief.md) to establish requirements.
2. Read the [master project plan](Project_Planning/Master_Project_Plan.md) for current scope, evidence, and closeout status.
3. Follow the [environment setup guide](Environment_Setup/Prerequisites_and_Environment_Setup.md) to reproduce the project environment and data workflow.
4. Review the [architecture](Implementation_and_Experiments/01_High_Level_Architecture.md), [dataset acquisition guide](Implementation_and_Experiments/05_Dataset_Acquisition_and_Reproducibility.md), and [data quality report](Implementation_and_Experiments/Data_Quality_Report.md).
5. Review the [experiment and decision log](Implementation_and_Experiments/04_Experiment_and_Decision_Log.md), [model comparison](Implementation_and_Experiments/Model_Family_Comparison/README.md), and [assignment evidence matrix](Implementation_and_Experiments/03_Assignment_to_Evidence_Matrix.md).
6. Review the [technical report](Final_Assignment_Report.md), [presentation notes](Assignment_1_Presentation_Draft.md), [presentation transcript](Assignment_1_Presentation_Transcript.md), and [slide source](Assignment_1_Presentation_Slides.md).
7. Complete the [individual contribution statements](Individual_Contribution_Statements_Template.md) with each member's own confirmed wording; rehearse and record the actual presentation timing.

## Primary project documents

### `Project_Planning/`
- `Master_Project_Plan.md` — current master plan, implementation status, 50-example model comparison, and remaining closeout actions.

### `Environment_Setup/`
- `Prerequisites_and_Environment_Setup.md` — **single current setup guide** covering software, prerequisites, dataset preparation, VS Code/Jupyter, application run, and tests.

### `Implementation_and_Experiments/`
- `01_High_Level_Architecture.md` — architecture and component flow.
- `02_Master_Phase_Plan.md` — phases, milestones, dependencies, and task status.
- `03_Assignment_to_Evidence_Matrix.md` — assignment requirements mapped to evidence.
- `03_Implementation_Guide.md` — implementation and execution instructions.
- `04_Experiment_and_Decision_Log.md` — experiment records, decisions, rationale, and observations.
- `05_Dataset_Acquisition_and_Reproducibility.md` — dataset source, checksums, preprocessing, and split-use policy.
- `Model_Family_Comparison/README.md` — evaluation protocol, results, limitations, and review guidance.
- `Data_Quality_Report.md` — dataset audits, preprocessing, exclusions, and integrity checks.

### Assignment submission drafts
- `Final_Assignment_Report.md` — technical report with evidence, limitations, and references mapped to the assignment requirements.
- `Assignment_1_Presentation_Draft.md` — timed slide-by-slide speaking draft with a proposed speaker split and demo.
- `Assignment_1_Presentation_Transcript.md` — full timed script for all four presenters, including a one-minute demo segment.
- `Individual_Contribution_Statements_Template.md` — simplified template for each member's short, personally confirmed statement.

### `Reference_Material/`
- `Original_Group_Major_Project_Assignment_Brief.md` — Markdown conversion of the original assignment brief; the source `.docx` is retained in this folder.

### `Templates_and_Repository_Baseline/`
- `README_TEMPLATE.md` — repository README template.
- Other files in this folder provide reusable templates and baseline records.

### `Historical_Drafts/`
Markdown conversions of earlier project plans, requirements, and checklists are retained for historical reference. Use the primary documents above for current execution unless a specific historical decision is explicitly adopted.

## Conversion and verification status

- Word documents were converted to Markdown for searchable project documentation.
- Active implementation-guide, experiment-log, and model-comparison report content is maintained in Markdown; redundant active Word copies have been removed.
- UTF-8 content checks passed for the assignment brief and experiment log.
- The original assignment brief and historical Word archives remain as source records. Their Markdown versions are used for project documentation.
- Full content, table, image, and formatting verification remains pending for the historical conversions.

## Dataset Reproducibility

- [Dataset Acquisition and Reproducibility](Implementation_and_Experiments/05_Dataset_Acquisition_and_Reproducibility.md) — expected raw files, source and license checks, checksums, validation/preprocessing commands, split-use policy, and current baseline limitations.
