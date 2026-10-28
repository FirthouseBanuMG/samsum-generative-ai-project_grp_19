# SAMSum Group Major Project — Document Index

This is the central index for the SAMSum-based intelligent conversation summarization and action-item extraction project.

## Documentation policy

- **Markdown (`.md`) is the primary editable documentation format.**
- Original Word (`.docx`) documents are retained as archival copies until conversion and content verification are complete.
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
- The presentation speaking draft, slide source, and generated 10-slide PowerPoint are in `documents/`; a proposed speaker split and one-minute demo plan are ready for team confirmation.
- Prompt and decoding experiments, structured output validation, tool demonstration, and model comparison now have implementation and saved evidence.
- The SAMSum-specific concise-versus-detailed prompt comparison has also been run on the fixed baseline examples.
- The integrated notebook/demo completed a CPU run; report content/citations were reviewed and the current render is 14 pages total with an 11-page body. Final team approval, contribution confirmations, and presentation rehearsal remain.

## Primary project documents

### `01_Project_Planning/`
- `Master_Project_Plan.md` — current master plan, implementation status, 50-example model comparison, and remaining closeout actions.

### `02_Environment_Setup/`
- `Prerequisites_and_Environment_Setup.md` — **single current setup guide** covering software, prerequisites, dataset preparation, VS Code/Jupyter, application run, and tests.

### `03_Implementation_and_Experiments/`
- `01_High_Level_Architecture.md` — architecture and component flow.
- `02_Master_Phase_Plan.md` — phases, milestones, dependencies, and task status.
- `03_Assignment_to_Evidence_Matrix.md` — assignment requirements mapped to evidence.
- `03_Implementation_Guide.md` — implementation and execution instructions.
- `04_Experiment_and_Decision_Log.md` — experiment records, decisions, rationale, and observations.
- `Data_Quality_Report.md` — dataset audits, preprocessing, exclusions, and integrity checks.

### Assignment submission drafts
- `Final_Assignment_Report.md` — technical report with evidence, limitations, and references mapped to the assignment requirements.
- `Assignment_1_Presentation_Draft.md` — timed slide-by-slide speaking draft with a proposed speaker split and demo.
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

- Fourteen Word documents were converted to Markdown.
- All fourteen Markdown counterparts were present and non-empty during the initial integrity check.
- UTF-8 content checks passed for the assignment brief and experiment log.
- Full content, table, image, and formatting verification remains pending for the complete set.
- Word originals have not been deleted.

## Dataset Reproducibility

- [Dataset Acquisition and Reproducibility](03_Implementation_and_Experiments/05_Dataset_Acquisition_and_Reproducibility.md) — expected raw files, source and license checks, checksums, validation/preprocessing commands, split-use policy, and current baseline limitations.
