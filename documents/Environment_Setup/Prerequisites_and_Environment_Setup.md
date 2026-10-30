# SAMSum Project — Environment Setup and Run Guide

This is the single current guide for the software, prerequisites, dataset setup, and commands needed to run the project on Windows.

**Verification update (31 October 2026):** The documented dataset validation, raw-file integrity, processed-split validation, and leakage checks passed against the local files. The offline test suite passed all 45 tests. The model-backed demo is separate and requires the processed training data and downloaded model weights.

## 1. What you need

### Required

- **Windows 10/11, 64-bit**, and **PowerShell**.
- **Python 3.10 or later, 64-bit** is declared by the project package metadata. The commands below use Python 3.13; Python 3.13.9 is the environment verified for this project.
- **Git for Windows** to clone the repository.
- **Internet access** to install Python packages, obtain SAMSum data independently, and download pretrained model files the first time you run inference.
- Enough free disk space for the virtual environment, dataset files, and model cache. The first model load downloads large weights; check free space before running it.
- The SAMSum CSV files listed in [Dataset setup](#5-dataset-setup). They are not included in Git.

### Recommended

- **Visual Studio Code**, with the Microsoft **Python** and **Jupyter** extensions for editing Python and running the integrated notebook.
- A computer with enough memory and storage for the selected model, dependencies, and dataset. CPU execution works, but generation speed depends on available hardware.

### Optional

- Microsoft Word to inspect the rendered report and confirm pagination.
- [Pandoc](https://pandoc.org/installing.html) to convert the Markdown report to Word format.
- An NVIDIA GPU is **not required** for the documented CPU workflow. GPU acceleration is optional and requires a compatible PyTorch installation.

Anaconda/Miniconda, Docker, Node.js, a paid model API, and a vector database are not required.

## 2. Software baseline

| Software / package | Requirement | Purpose |
|---|---|---|
| Windows | 10/11, 64-bit | Development platform |
| Python | 3.10+ per package metadata; 3.13.9 verified | Project interpreter |
| Git for Windows | Current supported release | Source control |
| Python packages | Install from `requirements-lock.txt` and `pyproject.toml` | Inference, data processing, validation, evaluation, and tests |
| Visual Studio Code extensions | Python and Jupyter (recommended) | Editing and notebook execution |

Use the repository's dependency files as the source of truth for package versions. CPU inference is supported; runtime depends on the computer and model.

## 3. Get the project

If the repository is not already on your computer, open PowerShell and run:

```powershell
git clone https://github.com/FirthouseBanuMG/samsum-generative-ai-project_grp_19.git
Set-Location .\samsum-generative-ai-project_grp_19
```

If it is already present, open PowerShell at the repository root instead. Confirm that you are in the folder containing `pyproject.toml`, `requirements-lock.txt`, and `src\`.

## 4. Create and install the Python environment

Run the following from the repository root. This uses the Python 3.13 registered with the Windows Python launcher and does not require activating the environment.

```powershell
py -3.13 --version
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.\.venv\Scripts\python.exe -m pip install -e ".[test]"
.\.venv\Scripts\python.exe -m pip check
```

The test extra installs the project's test dependency and makes the package available for `python -m package.module` commands.

For scripts that read or generate the optional Excel/Word evaluation documents, install the additional project extra:

```powershell
.\.venv\Scripts\python.exe -m pip install -e ".[evaluation-documents]"
```

The test and document extras can be installed together with `-e ".[test,evaluation-documents]"`.

Verify the key packages and CPU/GPU status:

```powershell
.\.venv\Scripts\python.exe -c "import torch, transformers, pandas, jsonschema; print('torch', torch.__version__); print('transformers', transformers.__version__); print('pandas', pandas.__version__); print('jsonschema', jsonschema.__version__); print('CUDA available:', torch.cuda.is_available())"
```

The command reports installed package versions and whether CUDA is available. CUDA availability varies by computer and PyTorch installation; it is not required for the documented CPU workflow.

### Use with Visual Studio Code

1. Open the repository folder in VS Code.
2. Select **Python: Select Interpreter** from the Command Palette.
3. Choose `.\.venv\Scripts\python.exe`.
4. Open `notebooks\01_integrated_demo.ipynb` and select that same environment as the notebook kernel.

PowerShell activation is optional. If you choose to activate the environment, run `.\.venv\Scripts\Activate.ps1`; otherwise keep using the explicit `.venv` interpreter path in the commands below.

## 5. Dataset setup

The raw and processed datasets are excluded from Git. The team reports using Kaggle's [“Samsum Dataset Text summarization”](https://www.kaggle.com/datasets/nileshmalode1/samsum-dataset-text-summarization), version 1. Kaggle lists the license as **Unknown**. This guide records that information; it does not claim redistribution permission. Obtain the data independently and do not redistribute dataset files based on this project.

Place the three CSV files in `data\raw\`:

| Filename | Expected rows |
|---|---:|
| `samsum-train.csv` | 14,732 |
| `samsum-validation.csv` | 818 |
| `samsum-test.csv` | 819 |

Each CSV is expected to contain `id`, `dialogue`, and `summary` columns. Keep the downloaded originals unchanged. The preprocessing pipeline excludes and logs one training row with a blank dialogue; it creates separate processed CSVs under `data\processed\`.

From the repository root, validate, prepare, and verify the data in this order:

```powershell
.\.venv\Scripts\python.exe -m data_processing.validate_dataset
.\.venv\Scripts\python.exe -m data_processing.verify_raw_dataset_integrity
.\.venv\Scripts\python.exe -m data_processing.preprocess_dataset
.\.venv\Scripts\python.exe -m data_processing.validate_processed_dataset
.\.venv\Scripts\python.exe -m data_processing.check_split_leakage
```

Inspect each command's output before continuing. For the complete source, checksum, profiling, and split-use details, see [Dataset Acquisition and Reproducibility](../Implementation_and_Experiments/05_Dataset_Acquisition_and_Reproducibility.md). The 50-example model comparison already used the test split; do not describe it as an untouched final holdout or continue tuning against those examples.

## 6. Run the application

From the repository root, run the integrated demo on the default processed training example:

```powershell
.\.venv\Scripts\python.exe -m integrated_demo.run_integrated_demo
```

Choose another ID that exists in `data\processed\samsum-train-processed.csv`:

```powershell
.\.venv\Scripts\python.exe -m integrated_demo.run_integrated_demo --sample-id 13818513
```

The demo loads the selected conversation, runs the pretrained Qwen model, parses and validates structured JSON, invokes the allowlisted validation function, and produces a final response when validation succeeds. The console and notebook present the summary, key points, decisions, action items, and review warnings in a readable table; the full machine-readable record is saved to `outputs\integrated_demo\demo_result.json`. The first run may download model weights and take several minutes on CPU. An internet connection and sufficient free disk space are needed for that download.

Generated text can omit or invent details. JSON Schema checks structure, not factual accuracy; read the dialogue and review the warning before relying on an output.

## 7. Run tests

Run the automated test suite from the repository root:

```powershell
.\.venv\Scripts\python.exe -m pytest tests
```

The tests cover offline validation and application logic; running this command does not run the full model-backed demo. Verification on 31 October 2026 completed with **45 tests passing**.

## 8. Optional: open the notebook or render the report

To run the integrated notebook, open `notebooks\01_integrated_demo.ipynb` in VS Code, choose the project `.venv` kernel, and execute its cells in order. The processed dataset and model download are still required.

To render the Markdown report to Word, install Pandoc separately if it is not already available, then run:

```powershell
pandoc documents\Final_Assignment_Report.md --from gfm+yaml_metadata_block --to docx --output documents\Final_Assignment_Report.docx
```

Word or another compatible editor is needed to check final pagination and layout. Pandoc and Word are document-review tools; they are not required to run the Python application or tests.

## 9. Troubleshooting

- **Wrong Python version:** Run `py -0p`; recreate `.venv` with `py -3.13 -m venv .venv` if it was created from another interpreter.
- **`No module named ...`:** Use `.\.venv\Scripts\python.exe` for commands and select that same interpreter in VS Code.
- **Dataset file not found:** Confirm the three CSVs are in `data\raw\` with the exact filenames above, then run preprocessing.
- **Model download is slow or fails:** Check internet access and free disk space, then retry. Do not put access tokens or credentials in notebooks or source control.
- **CPU generation is slow:** This is expected for a 1.5B-parameter model on CPU. Run one dialogue at a time; model generation is separate from the lightweight automated tests.
- **Dependency installation fails:** Keep the full error, Python version, and pip version. Do not change pinned dependencies blindly.
- **VS Code uses the wrong notebook kernel:** Select `.\.venv\Scripts\python.exe` as the interpreter and notebook kernel.

## 10. Repository safety

The repository ignores `.venv/`, raw and processed data, generated outputs, and local model caches. Before committing, check:

```powershell
git status --short
git check-ignore .venv data\raw data\processed outputs .cache_huggingface
```

Never commit dataset files, downloaded model weights/cache, secrets, or local environment contents.
