SAMSum-Based Intelligent Conversation Summarization and Action-Item Extraction

Version 1.0 • Verified 15 October 2026

This is the current-state companion to the baseline record. It records observed results only; the candidate model has not yet been downloaded or run.

# Update 002 — Verified Windows Environment and D: Drive Status

Status recorded on 15 October 2026 from the user's PowerShell outputs. This section supersedes earlier proposed setup values where they differ, while preserving earlier baseline observations as historical records.

## Verified machine and repository

- Project root: D:\BITS-Projects\samsum-generative-ai-project_grp_19

- Laptop: Lenovo IdeaPad Slim 5; Intel Core Ultra 5 125H; 16 GB RAM; 1 TB SSD; Windows.

- Available D: drive space at the latest check: 173.41 GB free.

- Git repository: samsum-generative-ai-project_grp_19; branch main; latest commit bc1b6bd (Initial commit); branch up to date with origin/main.

- Python executable: D:\BITS-Projects\samsum-generative-ai-project_grp_19\\venv\Scripts\python.exe

- Python version: 3.13.9 (Anaconda-packaged interpreter used to create the repository-local virtual environment).

- CPU-only PyTorch: 2.13.0+cpu; torch.cuda.is_available() returned False.

- Verified package versions: NumPy 2.5.4; pandas 3.0.6; Transformers 5.19.0; Accelerate 1.15.0; jsonschema 4.26.0; rouge-score 0.1.2; Jupyter 1.1.1; ipykernel 7.4.0; matplotlib 3.11.2; scikit-learn 1.9.1; huggingface-hub 2.2.0.

- Verification: imports succeeded for torch, numpy, pandas, transformers, accelerate, and jsonschema; tensor test returned \[6, 8\]; pip check returned 'No broken requirements found.'

- requirements-lock.txt was created in the D: project root using pip freeze. It is currently untracked in Git; review it and add it to Git only after confirming .gitignore excludes .venv and generated caches.

- Jupyter kernel name: samsum-generative-ai; display name: Python (SAMSum Project). The kernel.json is stored under %APPDATA% on C:, which is normal, and its argv points to the Python executable under the D: project root.

- The destination copy's Git repository is accessible. A previous Move-Item attempt hit a permission error on the original C: .git folder. Do not delete the original C: folder until the D: copy and any needed files have been checked.

## Commands verified

> Set-Location "D:\BITS-Projects\samsum-generative-ai-project_grp_19"
>
> & "D:\BITS-Projects\samsum-generative-ai-project_grp_19\\venv\Scripts\python.exe" -c "import sys; print(sys.executable); print(sys.version)"
>
> & "D:\BITS-Projects\samsum-generative-ai-project_grp_19\\venv\Scripts\python.exe" -c "import torch, numpy, pandas, transformers, accelerate; print(torch.\_\_version\_\_, numpy.\_\_version\_\_, pandas.\_\_version\_\_, transformers.\_\_version\_\_, accelerate.\_\_version\_\_)"
>
> & "D:\BITS-Projects\samsum-generative-ai-project_grp_19\\venv\Scripts\python.exe" -m pip check
>
> Get-Content "\$env:APPDATA\jupyter\kernels\samsum-generative-ai\kernel.json"
>
> git -C "D:\BITS-Projects\samsum-generative-ai-project_grp_19" status
>
> git -C "D:\BITS-Projects\samsum-generative-ai-project_grp_19" log -1 --oneline

## Not yet verified — do not report as completed

- Qwen/Qwen2.5-1.5B-Instruct repository access check has not yet been run.

- Model download, tokenizer/model loading, and text generation have not yet been tested.

- SAMSum CSV files have not yet been confirmed inside the D: project repository.

- No summarization quality, ROUGE score, latency, memory use, or final test-set result has been measured.

- Confirm .gitignore exists and excludes .venv/, model caches, secrets, and generated artifacts before staging files.

## Next step — model access check (pending)

> & "D:\BITS-Projects\samsum-generative-ai-project_grp_19\\venv\Scripts\python.exe" -c "from huggingface_hub import model_info; m=model_info('Qwen/Qwen2.5-1.5B-Instruct'); print('Model:', m.id); print('Model accessible')"

Run this only after the environment is active in the D: project folder. If it fails, capture the full error before changing package versions. Do not download model weights or claim a successful model test until the command and a small generation test actually succeed.

# Update 003 — Model and Local Dataset Verified

Recorded 16 October 2026. This section supersedes the earlier pending statements in Update 002.

- Model repository access: PASS — Qwen/Qwen2.5-1.5B-Instruct.

- Model download and CPU inference: PASS — model loaded in 3.90 minutes; one short generation completed in 11.0 seconds. PyTorch 2.13.0+cpu; CUDA unavailable.

- Hugging Face Datasets 5.1.0 installed, but SAMSum is being read from the existing local Kaggle CSVs, not downloaded from Hugging Face.

- Local dataset files confirmed in data/raw: train 14,732 rows, validation 818, test 819. Required columns are id, dialogue, summary.

- Dataset validation: one missing/blank dialogue in train; no missing summaries; no duplicate IDs; validation and test have no missing dialogue/summary.

- Git ignore setup completed; .venv, raw/processed data, and outputs verified ignored. .gitignore, model_smoke_test.py, and requirements-lock.txt were untracked at last status.

- Current stop point: after dataset validation (Step 9). Do not claim that a development sample, prompt experiments, ROUGE evaluation, or test-set evaluation has been completed.
