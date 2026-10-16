Decision D-003 • SAMSum Group Project • 15 October 2026 (updated after environment verification)

# 1. Verified observations

| **Check** | **Verified value** |
|----|----|
| Default interpreter | C:\Users\RAMNIWAS\anaconda3\python.exe |
| Python | 3.13.9, 64-bit, packaged by Anaconda |
| pip | 25.3 in Anaconda base, Python 3.13 |
| Python launcher | \`py -3.13\` resolves to the same Anaconda interpreter |
| Conda | 26.1.1; only \`base\` environment listed |
| Git | 2.55.0.windows.3 |
| Repository | \`samsum-generative-ai-project_grp_19\`, branch \`main\`, commit \`bc1b6bd\` |
| Working tree | Clean before environment setup |
| README | Confirms Applied Generative AI major project using SAMSum and a pretrained LLM for structured conversation summarization |

# 2. Decision D-003 — use Python 3.13.9 in a repository-local venv

Decision: retain the working Python 3.13.9 interpreter and create \`.venv\` inside the repository. Do not install project dependencies into Anaconda \`base\`. This avoids affecting unrelated projects and gives the SAMSum repository a separate dependency environment.

Why not Python 3.14? It is also installed, but we do not need to switch interpreters when Python 3.13.9 is already working and is within the documented Python range for PyTorch and Transformers. We will still test actual package compatibility before freezing versions.

# 3. Next action: create the project environment

Run these commands from \`D:\BITS-Projects\samsum-generative-ai-project_grp_19\` in PowerShell. First add a \`.gitignore\` so the virtual environment is not committed:

@(".venv/","\_\_pycache\_\_/","\*.py\[cod\]",".ipynb_checkpoints/",".env",".env.\*","!.env.example","data/processed/","outputs/","\*.log","models/","\*.safetensors","\*.pt","\*.pth","\*.bin") \| Set-Content .gitignore

python -m venv .venv

.\\venv\Scripts\Activate.ps1

python -c "import sys; print(sys.executable); print(sys.version)"

python -m pip --version

# 4. Expected result

The Python executable should now be under the repository path, for example \`...\samsum-generative-ai-project_grp_19\\venv\Scripts\python.exe\`. \`pip --version\` should also point inside \`.venv\`. Exact paths may differ if the repository folder is moved.

# 5. If PowerShell blocks activation

Do not change the machine-wide execution policy. Use the virtual environment's interpreter directly:

.\\venv\Scripts\python.exe -m pip --version

If that command works, we can continue using \`.\\venv\Scripts\python.exe\` for package commands without activating the environment.

# 6. Completion criteria

- The \`.gitignore\` file exists.

- The \`.venv\` directory exists.

- \`sys.executable\` points inside the repository's \`.venv\` directory.

- \`pip --version\` points inside \`.venv\`.

- ML libraries have been installed and verified in the D: project-local .venv. See Update 002 for the actual versions and current model-testing status.

# 7. Reference

PyTorch Windows installation and Python compatibility: https://pytorch.org/get-started/locally/

Transformers installation: https://huggingface.co/docs/transformers/main/installation

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
