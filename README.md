# SAMSum-Based Intelligent Conversation Summarization and Action-Item Extraction

**Course:** Applied Generative AI — Major Project  
**Group:** 19

This project investigates pretrained generative language models for conversation summarization and action-item extraction using the SAMSum dialogue dataset.

## Project status

- Dataset audit, preprocessing, and the 31 October 2026 raw-integrity, processed-data, and split-leakage checks completed locally.
- The offline test suite passed all 45 tests on 31 October 2026. This verification did not rerun model inference.
- The initial qualitative `Qwen/Qwen2.5-1.5B-Instruct` CPU smoke test and integrated demo have saved outputs under `outputs/`.
- Controlled prompt and decoding experiments, structured-output validation, an application-level tool demonstration, and the 50-sample model comparison have implementation under `src/` and saved evidence under `outputs/`.
- The technical report source, integrated notebook/demo, presentation materials, and contribution-statement template are present. The last recorded report render was 29 October 2026 (14 pages total, 11-page body); re-render after content or layout changes. Member-confirmed contribution statements and an actual presentation rehearsal remain.

The initial smoke test uses three training examples for pipeline verification. It is not a formal performance evaluation.
The integrated CLI selects a dialogue by ID from the processed training split; it does not accept arbitrary dialogue text.

## Repository structure

```text
data/
  raw/                 Downloaded source CSV files (not tracked by Git)
  processed/           Validated processed CSV files (not tracked by Git)
documents/             Project plans, assignment brief, experiment log
notebooks/             Project notebooks, including the integrated demo
outputs/
  baseline_smoke_test/ Initial baseline outputs and run metadata
src/
  baseline/             Baseline generation and evaluation preparation
  data_processing/      Dataset validation, profiling and preprocessing
  evaluation/           Model comparison and evaluation reporting
  generation/           Decoding experiments
  prompting/            Reusable prompts and prompt experiments
  structured_output/    JSON schema, parsing and validation
  tool_calling/         Allowlisted tool workflow
  integrated_demo/       Integrated demo and presentation helpers
  project_paths.py      Shared repository path constants
tests/                 Project tests
pyproject.toml          Installable src-layout package configuration
requirements-lock.txt  Python dependency versions
```

## Environment setup

The complete current guide—required software, Python environment, dependencies,
dataset preparation, VS Code/Jupyter setup, application run, and tests—is
[Environment Setup and Run Guide](documents/Environment_Setup/Prerequisites_and_Environment_Setup.md).
It is written for Windows PowerShell and uses the verified Python 3.13 CPU setup.

## Dataset setup

The raw and processed datasets are intentionally excluded from Git. The reported Kaggle listing shows version 1 and license **Unknown**. Cite that information as recorded; the project does not claim redistribution rights and does not include dataset files.

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

The processed test split has since been used for a 50-sample model-family
comparison. Treat those results as comparative/selection evidence, not as an
untouched final holdout; do not continue tuning against that same subset.

## Dataset validation and preprocessing

The maintained Python code is organized into logical packages directly
under `src/`. Run modules from the repository root using the
virtual-environment interpreter.

Validate the raw splits:

```powershell
.\.venv\Scripts\python.exe -m data_processing.validate_dataset
```

Profile raw data for preparation only (these scripts read but do not modify
the original CSVs):

```powershell
.\.venv\Scripts\python.exe -m data_processing.profile_dataset
```

```powershell
.\.venv\Scripts\python.exe -m data_processing.profile_token_lengths
```

Check raw files against the recorded local integrity baseline:

```powershell
.\.venv\Scripts\python.exe -m data_processing.verify_raw_dataset_integrity
```

Create processed splits:

```powershell
.\.venv\Scripts\python.exe -m data_processing.preprocess_dataset
```

Validate the processed splits:

```powershell
.\.venv\Scripts\python.exe -m data_processing.validate_processed_dataset
```

Check cross-split ID and exact-pair leakage on the **processed** splits:

```powershell
.\.venv\Scripts\python.exe -m data_processing.check_split_leakage
```

Run these in order. Check each script's output before proceeding. Do not silently change the exclusion policy or overwrite source CSVs.

## Run the initial model smoke test

After the raw and processed training CSVs are available, run:

```powershell
.\.venv\Scripts\python.exe -m baseline.model_smoke_test
```

The script loads `Qwen/Qwen2.5-1.5B-Instruct`, runs the initial training-split examples, and writes:

- `outputs/baseline_smoke_test/baseline_outputs.json`
- `outputs/baseline_smoke_test/run_metadata.json`

The first run may download model files and take several minutes on CPU.

The generated summaries include unsupported details in some examples. Treat them as qualitative debugging evidence, not as proof of model accuracy.

## Decoding comparison experiment (E3)

Compare greedy decoding against sampling configurations (temperature with top-p and with top-k) on the baseline dialogues, keeping the prompt fixed. Sampling runs are repeated with recorded seeds so output variability can be measured.

```powershell
.\.venv\Scripts\python.exe -m generation.run_decoding_experiments
```

Outputs are written to `outputs/decoding_experiments/`:

- `decoding_comparison.json` / `decoding_comparison.csv` — every run with its decoding config, seed and summary.
- `decoding_variability_summary.csv` — distinct outputs and mean word overlap per decoding config (repeatability vs diversity).

This runs many generations on CPU and can take a long time. Run it once and keep the outputs.

## Structured JSON output experiment (E4)

Generate machine-readable output (`summary`, `key_points`, `decisions`, and `action_items`) for each baseline dialogue, validate it against a JSON schema, and demonstrate recovery from invalid JSON (one corrective retry, then a flagged fallback).

```powershell
.\.venv\Scripts\python.exe -m structured_output.run_structured_output
```

Outputs are written to `outputs/structured_output/`:

- `structured_outputs.json` — per-sample raw output, parse/validation result, recovery status, final object, plus a deliberate malformed case run through the validator.
- `structured_output_log.csv` — compact valid/invalid/recovered summary.

The schema and helpers live in `structured_output.schema`.
Validation logic can be checked quickly without loading the model:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_structured_schema.py
```

The structured result includes `summary`, `key_points`, `decisions`, and `action_items`.

## Tool round trip and integrated demo (E5/E7)

Run the model-backed application-level tool workflow:

```powershell
.\.venv\Scripts\python.exe -m tool_calling.run_tool_calling
```

The runner records the model's JSON request, the allowlisted schema-validation
tool result, and a final model response conditioned on that result in
`outputs/tool_calling/tool_calling_demo.json`. It blocks the follow-up when
validation fails. This is an application-level JSON protocol, not native
model-specific tool calling. Schema validity is structural only; human review
is still required.

Run the complete application workflow on one training example:

```powershell
.\.venv\Scripts\python.exe -m integrated_demo.run_integrated_demo --sample-id 13818513
```

Run the offline regression tests:

```powershell
.\.venv\Scripts\python.exe -m pytest tests
```

## Concise versus detailed prompt comparison

Compare one-sentence summaries against 3–5 sentence summaries on the same three baseline training dialogues, using a fixed Qwen model and greedy decoding:

```powershell
.\.venv\Scripts\python.exe -m prompting.run_summary_detail_comparison
```

Outputs are written to `outputs/summary_detail_comparison/`. The experiment records full prompts and generations, word/sentence counts, and ROUGE-1/ROUGE-L overlap. It is an exploratory three-example comparison, not a general quality claim.

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
- [Assignment brief](documents/Reference_Material/Original_Group_Major_Project_Assignment_Brief.md)
- [Master project plan](documents/Project_Planning/Master_Project_Plan.md)
- [Environment setup guide](documents/Environment_Setup/Prerequisites_and_Environment_Setup.md)
- [Implementation guide](documents/Implementation_and_Experiments/03_Implementation_Guide.md)
- [Assignment-to-evidence matrix](documents/Implementation_and_Experiments/03_Assignment_to_Evidence_Matrix.md)
- [Experiment and decision log](documents/Implementation_and_Experiments/04_Experiment_and_Decision_Log.md)
- [Data quality report](documents/Implementation_and_Experiments/Data_Quality_Report.md)

Markdown is the source of truth for project documentation. Redundant Word copies of active guides and reports have been consolidated and removed. The original assignment brief and selected historical Word archives remain as source records.

## Team contribution and collaboration

Before starting a task, check the project plan and experiment log. Coordinate changes to shared scripts and notebooks with the group, record experiment settings and results, and update the relevant documentation. Each member should document their actual contribution for the final submission.

## Known handover limitation

The dataset CSVs and processed metadata are not included in this repository. Teammates must obtain the source dataset and regenerate the processed files locally before running the model smoke test. The reported Kaggle page lists the license as Unknown. The project cites that listing and does not claim redistribution rights; dataset files are not included in Git.

## Reproducibility and remaining work

The raw and processed SAMSum CSV files are excluded from Git. See the [dataset acquisition and reproducibility guide](documents/Implementation_and_Experiments/05_Dataset_Acquisition_and_Reproducibility.md) for expected files, verification steps, preprocessing commands, and split-use policy.

The current Qwen baseline is a small qualitative smoke test, not a formal performance evaluation. Its outputs include examples of unsupported details, so they must not be presented as proof of reliable summarization.

Prompt, decoding, structured-output, tool-call, and model-comparison experiments have code and saved results. Prompt evaluation uses three examples per strategy; the model comparison uses 50 test-split examples and must be described with its exact split-use protocol. ROUGE is not a factuality metric.

The integrated notebook and `integrated_demo.run_integrated_demo` implement the full application flow, including a model follow-up after the tool result. The notebook and CLI display the structured result as a readable table of summary, key points, decisions, action items, and review notes; the complete machine-readable record is saved to `outputs/integrated_demo/demo_result.json`. The notebook and CLI have been rerun on CPU with training sample `13818513`; the model omitted the planned delivery commitment while passing JSON Schema validation, so human review remains essential.

Before submitting, keep the reviewed report within the 10–15-page body limit (latest render: 11 pages), collect each member's short contribution statement and confirmation, rehearse and time the presentation/demo to 8–10 minutes, then submit through the course process and retain confirmation. See the [technical report](documents/Final_Assignment_Report.md), [presentation plan](documents/Assignment_1_Presentation_Draft.md), [contribution statement template](documents/Individual_Contribution_Statements_Template.md), and [assignment-to-evidence matrix](documents/Implementation_and_Experiments/03_Assignment_to_Evidence_Matrix.md).
