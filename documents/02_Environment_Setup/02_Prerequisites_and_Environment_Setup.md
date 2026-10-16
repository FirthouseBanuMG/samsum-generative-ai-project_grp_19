*Windows • VS Code • Python • CPU-first with Colab fallback*

Project: SAMSum-Based Intelligent Conversation Summarization and Action-Item Extraction

Document status: Version 0.2 — updated 15 October 2026

Working rule: Record proposed choices as proposed until the team verifies them. Never report unrun experiments as results.

# 1. Known machine and approach

Known laptop: Lenovo IdeaPad Slim 5, Intel Core Ultra 5 125H, 16 GB RAM, 1 TB SSD, Windows 64-bit. This is adequate for data inspection, notebook development, JSON validation, and small inference pilots. A 1.5B model may be slow on CPU; GPU acceleration is not assumed.

# 2. Software baseline

| **Component** | **Target / policy** | **Why** | **Verification** |
|----|----|----|----|
| Windows | Existing 64-bit Windows | Primary local development environment. | winver |
| Python | Use existing Python 3.13.9 if it is installed and healthy; otherwise install a supported 64-bit Python 3.13.x release | Already recorded on this laptop/project context; supported by current Transformers package metadata. Avoid installing multiple versions blindly. | py -0p and python --version |
| VS Code | Current stable release | Editor, terminal, Git, notebook workflow. | code --version |
| VS Code extensions | Python (Microsoft), Jupyter (Microsoft) | Interpreter selection and notebook execution. | Extensions panel |
| Git | Current stable release | Version control and team collaboration. | git --version |
| PyTorch | Initial target torch==2.13.0; CPU wheel for CPU-first setup | Tensor operations and model inference. Recheck available wheel for the chosen Python before installing. | python -c "import torch; print(torch.\_\_version\_\_); print(torch.cuda.is_available())" |
| Transformers | Initial target transformers==5.19.0 (verified installed version) | Load tokenizer and pretrained causal LM. | python -c "import transformers; print(transformers.\_\_version\_\_)" |
| Accelerate | Compatible 1.x release; record exact installed version after smoke test | Model loading/inference helpers. | python -c "import accelerate; print(accelerate.\_\_version\_\_)" |
| pandas / NumPy | Compatible current releases; pin exact installed versions after smoke test | CSV handling and data inspection. | Import/version check |
| Jupyter / ipykernel | Compatible current releases; pin exact installed versions after smoke test | Notebook execution. | Notebook kernel runs |
| rouge-score | 0.1.2 | Reference-overlap evaluation metric. | Import and sample metric test |
| jsonschema | Compatible current 4.x release | Validate structured output. | Schema validation test |
| matplotlib / scikit-learn | Compatible current releases, only as needed | Plots and optional analysis helpers. | Import/version check |

Version policy: the values above are a proposed baseline, not a claim that the complete environment has already been tested. After installation, run the smoke test, save \`pip freeze\` to \`requirements-lock.txt\`, and commit that lock file. Do not upgrade packages during final experiments without logging and rerunning checks.

# 3. Not required for the initial scope

- Anaconda/Miniconda, Docker, Node.js, a paid model API, a dedicated NVIDIA GPU, vector database, or fine-tuning infrastructure.

- Do not download model weights manually into Git. Hugging Face will cache them locally; do not commit caches or large model files.

# 4. Repository setup

Repository: https://github.com/FirthouseBanuMG/samsum-generative-ai-project_grp_19

1.  Open PowerShell and navigate to the folder where the project should live.

2.  Clone the existing repository only if it is not already present: \`git clone https://github.com/FirthouseBanuMG/samsum-generative-ai-project_grp_19.git\`

3.  Enter the repository: \`cd samsum-generative-ai-project_grp_19\`

4.  Inspect before changing anything: \`git status\`, \`git branch --show-current\`, \`git log -5 --oneline\`, \`Get-ChildItem\`.

5.  If the repo already has requirements, notebooks, or data, review them before overwriting. Keep existing work until it is understood.

6.  Create/activate a virtual environment from the project root: \`py -3.13 -m venv .venv\` then \`.\\venv\Scripts\Activate.ps1\`.

7.  Upgrade packaging tools inside the environment: \`python -m pip install --upgrade pip setuptools wheel\`.

8.  Install dependencies from the approved \`requirements.txt\` after confirming its contents and Python compatibility.

# 5. Proposed initial requirements.txt

Start with a conservative dependency list; after the first clean smoke test, freeze exact versions in a separate lock file.

torch==2.13.0
transformers==5.19.0 (verified installed version)
accelerate\>=1.0,\<2.0
pandas\>=2.2,\<4.0
numpy\>=1.26,\<3.0
jupyter\>=1.1,\<2.0
ipykernel\>=6.29,\<8.0
rouge-score==0.1.2
jsonschema\>=4.23,\<5.0
matplotlib\>=3.9,\<4.0
scikit-learn\>=1.6,\<2.0

Important: if pip cannot find a compatible PyTorch wheel for the Python interpreter, stop and use the official PyTorch selector rather than randomly changing versions. The current PyTorch website provides CPU-specific installation commands.

# 6. Smoke-test checklist

- [ ] \`python --version\` shows the intended interpreter.

- [ ] \`python -m pip --version\` points inside \`.venv\`.

- [ ] \`python -c "import torch, transformers, pandas, numpy, jsonschema; print('imports ok')"\` succeeds.

- [ ] PyTorch tensor operation succeeds.

- [ ] VS Code is using \`.venv\` as the interpreter and notebook kernel.

- [ ] One tiny model/tokenizer load and one short generation completes; record elapsed time and memory behavior.

- [ ] \`python -m pip freeze \> requirements-lock.txt\` is saved after successful tests.

- [ ] \`git status\` confirms \`.venv\`, model cache, secrets, and large generated files are not staged.

# 7. Troubleshooting rules

- PowerShell blocks activation: use the current terminal's approved execution-policy guidance; do not disable security controls globally.

- Wrong Python in VS Code: use “Python: Select Interpreter” and choose the repository \`.venv\`.

- Model download failure: verify network access and retry; do not place access tokens in notebooks or commits.

- Slow CPU inference: first test a single short dialogue; reduce max_new_tokens and batch size, then use Colab GPU if needed.

- Dependency conflict: capture the full error, Python version, pip version, and requirements; do not blindly install/uninstall packages.

# 8. Official references

- Python releases: https://www.python.org/downloads/

- VS Code Python environments: https://code.visualstudio.com/docs/python/environments

- PyTorch local installation selector: https://pytorch.org/get-started/locally/

- PyTorch previous versions: https://pytorch.org/get-started/previous-versions/

- Transformers on PyPI: https://pypi.org/project/transformers/

- Candidate model card: https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct

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

# Update 003 — Setup Progress Through Step 9

Recorded 16 October 2026 from commands and outputs supplied during the project setup conversation. This section is the current status and supersedes earlier statements that model loading, Git ignore setup, and local dataset placement were pending.

## Verified environment and model

- Project root: D:\BITS-Projects\samsum-generative-ai-project_grp_19.

- Python: 3.13.9, invoked reliably through .\\venv\Scripts\python.exe (PowerShell activation is not required).

- PyTorch: 2.13.0+cpu; CUDA unavailable, as expected for the CPU-first setup.

- Qwen/Qwen2.5-1.5B-Instruct repository access succeeded. Tokenizer and model weights downloaded successfully; the model loaded on CPU in 3.90 minutes and generated one test summary in 11.0 seconds.

- The smoke-test summary correctly captured the meeting change to 3:30 in the cafeteria and John bringing the project notes. This verifies a single example only; it is not a dataset-level quality result.

- Installed Hugging Face Datasets 5.1.0. The dataset was NOT downloaded from Hugging Face because the project already has local Kaggle CSVs.

- Hugging Face cache warnings on Windows indicate symlinks are unavailable and caching may use extra disk space; they did not prevent model loading. The unauthenticated Hub warning also did not prevent download.

## Repository setup completed

- Created .gitignore. It excludes .venv/, Python cache files, Jupyter checkpoints, data/raw/, data/processed/, models/, outputs/, logs, MLflow artifacts, .env secrets, and editor/OS files.

- Created directories: data/raw, data/processed, notebooks, src, src/prompts, src/schemas, src/evaluation, tests, experiments, outputs.

- Git check-ignore confirmed .venv, data/raw, data/processed, and outputs are ignored. The models path was not printed because it does not exist yet; its rule is present in .gitignore.

- At the last Git status, .gitignore, model_smoke_test.py, and requirements-lock.txt were untracked. Do not commit until the ignore rules and files have been reviewed.

- The requirements-lock.txt was generated before installing datasets; regenerate it after setup is stable so it includes the final installed package set.

## Local SAMSum files and validation

Files copied into data/raw (original CSVs are preserved unchanged):

- data/raw/samsum-train.csv — 14,732 rows; columns id, dialogue, summary; one missing/blank dialogue; no missing summaries; no duplicate IDs.

- data/raw/samsum-validation.csv — 818 rows; columns id, dialogue, summary; no missing dialogue or summary; no duplicate IDs.

- data/raw/samsum-test.csv — 819 rows; columns id, dialogue, summary; no missing dialogue or summary; no duplicate IDs.

- Total across the three splits: 16,369 rows. Median dialogue lengths reported by validation: train 401 characters, validation 386, test 403.

- The single unusable training row will be excluded during preprocessing and recorded; do not modify the raw CSV. Keep validation and test separate, and do not use the test split for prompt tuning.

## Executed commands — key commands to reproduce

Run these from the repository root in PowerShell. Use the explicit interpreter path rather than relying on environment activation.

> \# Confirm Hugging Face model repository access
>
> .\\venv\Scripts\python.exe -c "from huggingface_hub import model_info; m=model_info('Qwen/Qwen2.5-1.5B-Instruct'); print('Model:', m.id); print('Model accessible')"
>
> \# Install and verify the dataset loader
>
> .\\venv\Scripts\python.exe -m pip install datasets
>
> .\\venv\Scripts\python.exe -c "import datasets; print('Datasets version:', datasets.\_\_version\_\_)"
>
> \# Run the CPU model smoke test (model_smoke_test.py was created using a PowerShell here-string)
>
> .\\venv\Scripts\python.exe .\model_smoke_test.py
>
> \# Create project directories
>
> \$folders = @("data\raw", "data\processed", "notebooks", "src", "src\prompts", "src\schemas", "src\evaluation", "tests", "experiments", "outputs")
>
> foreach (\$folder in \$folders) { New-Item -ItemType Directory -Path \$folder -Force \| Out-Null }
>
> \# Check raw dataset files
>
> Get-ChildItem .\data\raw
>
> \# Run local CSV validation
>
> .\\venv\Scripts\python.exe .\src\validate_dataset.py
>
> \# Verify ignore rules
>
> Get-Content .gitignore
>
> git status --short
>
> git check-ignore .venv data/raw data/processed models outputs

## Current stopping point

STOPPED AFTER DATASET VALIDATION (Step 9). No development sample has been created yet; prepare_dev_sample.py has not been run. Next work should resume only when requested, beginning with the proposed 100-row training development sample. No model evaluation, ROUGE scoring, prompt comparison, or final test-set evaluation has been performed.

Not yet done: refresh requirements-lock.txt after all dependency changes; review README and untracked files; commit source/configuration only after review; build notebook; run systematic prompt experiments; evaluate on a held-out test subset.
