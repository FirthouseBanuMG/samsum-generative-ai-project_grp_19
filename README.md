# SAMSum-Based Intelligent Conversation Summarization and Action-Item Extraction

**Course:** Applied Generative AI — Major Project  
**Group:** 19

This project investigates pretrained generative language models for conversation summarization and action-item extraction using the SAMSum dialogue dataset.

## Project status

- Dataset audit and preprocessing completed locally.
- Initial qualitative smoke test completed with `Qwen/Qwen2.5-1.5B-Instruct` on CPU.
- Baseline outputs and run metadata are available under `outputs/baseline_smoke_test/`.
- Controlled prompt comparisons, structured action-item extraction, model-family comparison, and final evaluation remain to be completed unless recorded in subsequent experiment evidence.

The initial smoke test uses three training examples for pipeline verification. It is not a formal performance evaluation.

## Repository structure

```text
data/
  raw/                 Downloaded source CSV files (not tracked by Git)
  processed/           Validated processed CSV files (not tracked by Git)
documents/             Project plans, assignment brief, experiment log
experiments/            Experiment-related resources
notebooks/             Project notebooks
outputs/
  baseline_smoke_test/ Initial baseline outputs and run metadata
src/                   Dataset validation, profiling and preprocessing scripts
tests/                 Project tests
model_smoke_test.py    Initial pretrained-model smoke test
requirements-lock.txt  Python dependency versions
```

## Prerequisites

- Git
- Python compatible with the project's pinned dependencies
- Internet access for obtaining the dataset and downloading the pretrained model
- Sufficient RAM and disk space for the model and Python dependencies

The initial smoke test was run on Windows with Python 3.13.9 and CPU-only PyTorch. GPU acceleration is not required for that smoke test.

## Set up the environment

Run these commands from the repository root in PowerShell.

Create a virtual environment:

```powershell
python -m venv .venv
```

Install the recorded dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
```

Verify the installed packages:

```powershell
.\.venv\Scripts\python.exe -m pip check
```

If installation fails, record the Python version and complete error before changing pinned dependencies.

## Dataset setup

The raw and processed datasets are intentionally excluded from Git. Each team member must obtain the SAMSum dataset from its original source and review the applicable license terms.

Place the downloaded CSV files in `data/raw/` using these filenames:

- `samsum-train.csv`
- `samsum-validation.csv`
- `samsum-test.csv`

Expected source columns are `id`, `dialogue`, and `summary`.

The locally audited source split counts were:

| Split | Raw rows | Processed rows |
|---|---:|---:|
| Train | 14,732 | 14,731 |
| Validation | 818 | 818 |
| Test | 819 | 819 |

One training record with a missing or blank dialogue was excluded during preprocessing. See `data/processed/exclusions.json` and `data/processed/preprocessing_metadata.json` on the machine where preprocessing was run; these local data artifacts are not currently tracked by Git.

Do not use the test split for prompt selection or iterative development.

## Dataset validation and preprocessing

The relevant scripts are under `src/`. Run them from the repository root using the virtual-environment interpreter.

Validate the raw splits:

```powershell
.\.venv\Scripts\python.exe src\validate_dataset.py
```

Check cross-split leakage:

```powershell
.\.venv\Scripts\python.exe src\check_split_leakage.py
```

Profile the dataset:

```powershell
.\.venv\Scripts\python.exe src\profile_dataset.py
```

Profile token lengths:

```powershell
.\.venv\Scripts\python.exe src\profile_token_lengths.py
```

Create processed splits:

```powershell
.\.venv\Scripts\python.exe src\preprocess_dataset.py
```

Validate the processed splits:

```powershell
.\.venv\Scripts\python.exe src\validate_processed_dataset.py
```

Run these in order. Check each script's output before proceeding. Do not silently change the exclusion policy or overwrite source CSVs.

## Run the initial model smoke test

After the raw and processed training CSVs are available, run:

```powershell
.\.venv\Scripts\python.exe model_smoke_test.py
```

The script loads `Qwen/Qwen2.5-1.5B-Instruct`, runs the initial training-split examples, and writes:

- `outputs/baseline_smoke_test/baseline_outputs.json`
- `outputs/baseline_smoke_test/run_metadata.json`

The first run may download model files and take several minutes on CPU.

The generated summaries include unsupported details in some examples. Treat them as qualitative debugging evidence, not as proof of model accuracy.

## Experiment and data-use policy

- Training split: initial pipeline checks and few-shot demonstrations.
- Validation split: controlled prompt/model development and selection.
- Test split: final evaluation only after the experimental protocol is fixed.
- Record prompt text, decoding settings, model identifier, sample IDs, outputs, and evaluation criteria.
- Do not claim improvements without comparable experimental evidence.
- Do not assume generated summaries or extracted action items are correct without validation.

## Documentation

Start with these documents:

- [Document index](documents/README_Document_Index.md)
- [Assignment brief](documents/04_Reference_Material/Original_Group_Major_Project_Assignment_Brief.md)
- [Master project plan](documents/01_Project_Planning/01_Master_Project_Plan.md)
- [Environment setup guide](documents/02_Environment_Setup/02_Prerequisites_and_Environment_Setup.md)
- [Implementation guide](documents/03_Implementation_and_Experiments/03_Implementation_Guide.md)
- [Assignment-to-evidence matrix](documents/03_Implementation_and_Experiments/03_Assignment_to_Evidence_Matrix.md)
- [Experiment and decision log](documents/03_Implementation_and_Experiments/04_Experiment_and_Decision_Log.md)
- [Data quality report](documents/03_Implementation_and_Experiments/Data_Quality_Report.md)

Markdown files are the primary editable documentation. Word documents are retained as archival copies.

## Team contribution and collaboration

Before starting a task, check the project plan and experiment log. Coordinate changes to shared scripts and notebooks with the group, record experiment settings and results, and update the relevant documentation. Each member should document their actual contribution for the final submission.

## Known handover limitation

The dataset CSVs and processed metadata are not included in this repository. Teammates must obtain the source dataset and regenerate the processed files locally before running the model smoke test. Dataset redistribution should not be assumed permitted without checking the applicable terms.
