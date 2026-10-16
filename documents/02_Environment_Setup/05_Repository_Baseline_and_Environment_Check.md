*SAMSum Generative AI Group Project — Baseline Record 001*

Record date: 15 October 2026

Purpose: capture verified starting conditions before installing packages or changing the repository.

# 1. Verified facts from PowerShell

| **Check** | **Observed result** |
|----|----|
| Default \`python --version\` | Python 3.13.9 |
| Python launcher \`py -0p\` | Python 3.14 64-bit at \`C:\Users\RAMNIWAS\AppData\Local\Python\pythoncore-3.14-64\python.exe\`; Python 3.13 at \`C:\Users\RAMNIWAS\anaconda3\python.exe\` |
| Git | git version 2.55.0.windows.3 |
| Repository | \`samsum-generative-ai-project_grp_19\` |
| Remote | \`https://github.com/FirthouseBanuMG/samsum-generative-ai-project_grp_19.git\` |
| Current branch | \`main\` |
| Current commit | \`bc1b6bd\` — Initial commit |
| Working tree | Clean; up to date with \`origin/main\` |
| Visible files | \`README.md\` only, 188 bytes at time of inspection |

# 2. Interpretation

The Git repository is a clean initial scaffold, not yet an implementation repository. The only visible project file is README.md. No requirements file, notebooks, source package, dataset files, or tests were visible in the supplied directory listing. This conclusion is limited to the root listing shown; it is not a claim about hidden remote branches or files not fetched.

There are two Python interpreters. \`python\` resolves to Python 3.13.9 from Anaconda, while \`py -0p\` also lists a separate Python 3.14 installation. We should choose and record one interpreter for this project rather than mix package installations.

# 3. Next verification commands — run these exactly

python -c "import sys; print(sys.executable); print(sys.version)"

python -m pip --version

py -3.13 -c "import sys; print(sys.executable); print(sys.version)"

conda --version

conda info --envs

Get-Content README.md

# 4. Why these checks matter

| **Check** | **Reason** |
|----|----|
| Executable path | Shows which Python actually runs when you type \`python\`. |
| pip path | Confirms which interpreter receives installed packages. |
| Python 3.13 launcher check | Compares the launcher-selected interpreter with the default shell interpreter. |
| Conda checks | Tell us whether Anaconda is active and which environments already exist; avoids unnecessary reinstallations. |
| README content | Captures any project guidance before we create files. |

# 5. Do not do these yet

- Do not install PyTorch, Transformers, or the other ML packages yet.

- Do not create a new virtual environment until we choose the interpreter.

- Do not delete or overwrite README.md.

- Do not commit datasets, model weights, API keys, \`.venv\`, or generated caches.

# 6. Decision log

Decision D-003 — Pending: choose Python interpreter after the verification commands above.

Decision D-004 — Confirmed: retain the current clean \`main\` branch and add the documented project structure incrementally.

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
