# Environment Setup — Executed Command Checklist (through Step 9)

Project path: `D:\BITS-Projects\samsum-generative-ai-project_grp_19`

Use PowerShell from the project root. Commands below are a record of the workflow; not all are intended to be rerun.

## Environment and model

```powershell
.\.venv\Scripts\python.exe -m pip install -U huggingface_hub
.\.venv\Scripts\python.exe -c "from huggingface_hub import model_info; m=model_info('Qwen/Qwen2.5-1.5B-Instruct'); print('Model:', m.id); print('Model accessible')"
.\.venv\Scripts\python.exe .\model_smoke_test.py
```

Verified: Python 3.13.9 in the project venv; PyTorch 2.13.0+cpu; CUDA unavailable; Transformers 5.19.0; Accelerate 1.15.0; NumPy 2.5.4; pandas 3.0.6; jsonschema 4.26.0; rouge-score 0.1.2; Jupyter 1.1.1; ipykernel 7.4.0; matplotlib 3.11.2; scikit-learn 1.9.1. Hugging Face Datasets 5.1.0 was installed later. `pip check` previously reported no broken requirements before Datasets was installed.

Smoke test passed. Model load time: 3.90 minutes. Sample generation time: 11 seconds. Windows cache symlink and unauthenticated-Hub warnings were non-fatal.

## Git repository and folders

`.gitignore` was created with rules to ignore `.venv/`, `data/raw/`, `data/processed/`, `models/`, `outputs/`, logs, caches, and local secrets. Verified with `git check-ignore data/raw data/processed models outputs`; `data/raw`, `data/processed`, and `outputs` were reported ignored.

Project directories created: `data/raw`, `data/processed`, `notebooks`, `src`, `src/prompts`, `src/schemas`, `src/evaluation`, `tests`, `experiments`, and `outputs`.

## Local dataset validation

Files in `data/raw/`: `samsum-train.csv`, `samsum-validation.csv`, `samsum-test.csv`.

```powershell
.\.venv\Scripts\python.exe .\src\validate_dataset.py
```

Observed results:
- Train: 14,732 rows; columns `id`, `dialogue`, `summary`; one missing/blank dialogue; no missing summaries; no duplicate IDs; dialogue median length 401 characters.
- Validation: 818 rows; no missing dialogue or summary; no duplicate IDs; dialogue median length 386 characters.
- Test: 819 rows; no missing dialogue or summary; no duplicate IDs; dialogue median length 403 characters.
- Total rows: 16,369.

Original CSVs remain unchanged. Any cleaning should happen in preprocessing code, not by editing the raw files. The test split should remain untouched during prompt development.

## Next step — intentionally not executed

Create a reproducible 100-row training development sample after the user asks to resume. Do not claim that sample or subsequent evaluation has been completed.
