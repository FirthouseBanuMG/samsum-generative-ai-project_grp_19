*Step-by-step build sequence • what • how • why • evidence*

Project: SAMSum-Based Intelligent Conversation Summarization and Action-Item Extraction

Document status: Version 0.2 — updated 15 October 2026

Working rule: Record proposed choices as proposed until the team verifies them. Never report unrun experiments as results.

# How to use this guide

Complete steps in order. Each step has an objective, implementation action, reason, and evidence to save. Do not mark a step complete until the output has been run and checked.

## Step 0 — Inspect the existing GitHub repository

How: review README, folders, notebooks, dependency files, data handling, commits, and current status before editing.

Why: avoid duplicating work or deleting an existing teammate's implementation.

Evidence to save: Evidence: repository inventory, current branch, commit hash, issues/blockers.

## Step 1 — Create a reproducible Python environment

How: create \`.venv\`, install approved requirements, run import and model smoke tests, save \`requirements-lock.txt\`.

Why: team members should be able to reproduce results and diagnose environment differences.

Evidence to save: Evidence: Python/package versions, smoke-test output, elapsed model load/generation time.

## Step 2 — Load and audit SAMSum

How: read train/validation/test files; verify columns, row counts, missing values, duplicates, dialogue/summary lengths, and sample records.

Why: establish that the input data is correct and understand the task before modeling.

Evidence to save: Evidence: dataset source/version, split counts, schema, missing-value table, examples, preprocessing decisions.

## Step 3 — Establish the pretrained baseline

How: load the selected causal LM and tokenizer; write a simple prompt; generate outputs for at least three representative dialogues.

Why: obtain a baseline before adding prompt complexity.

Evidence to save: Evidence: model ID, revision if available, prompt text/version, generation parameters, input IDs, outputs, runtime.

## Step 4 — Compare prompt strategies (E2)

How: compare zero-shot, few-shot, role/context-based, and constraint-based prompts. Keep the model and decoding settings fixed.

Why: isolate the effect of prompt design instead of mixing several changes.

Evidence to save: Evidence: prompt variants, examples used, outputs, rubric scores, observations.

## Step 5 — Compare decoding settings (E3)

How: compare greedy decoding against sampling; test temperature and at least one of top-k/top-p. Use the same dialogues and prompts.

Why: show the trade-off between repeatability and output diversity.

Evidence to save: Evidence: complete generation config, repeated outputs for sampling, quality/variability notes.

## Step 6 — Add structured JSON output (E4)

How: define a JSON schema with \`summary\` (string) and \`action_items\` (array of objects); validate parsed model output; handle invalid JSON without crashing.

Why: downstream systems need predictable structure and explicit error handling.

Evidence to save: Evidence: schema file, valid and invalid examples, validation logs, recovery behavior.

## Step 7 — Build a reusable prompt and callable function (E5)

How: implement a function such as \`summarize_dialogue(dialogue, style, max_summary_sentences, decoding_config)\` with documented input/output schema.

Why: separate reusable application logic from notebook experimentation and demonstrate tool/function use.

Evidence to save: Evidence: function signature, input validation, invocation example, output, error case.

## Step 8 — Evaluate systematically

How: select a validation sample for prompt selection and a separate held-out test sample for final reporting. Use at least four criteria and ROUGE as a supporting metric.

Why: one attractive example is not evidence of overall quality; held-out evaluation reduces selection bias.

Evidence to save: Evidence: sample IDs/selection method, rubric, scores, metric code, limitations.

## Step 9 — Analyze failure cases (E6)

How: capture at least three failures, e.g. invented action, omitted key fact, wrong speaker attribution, malformed JSON, or overlong summary.

Why: a credible GenAI project must describe where the model fails, not only happy paths.

Evidence to save: Evidence: dialogue, generated result, expected interpretation, error category, root-cause hypothesis, mitigation.

## Step 10 — Integrate and reproduce (E7)

How: run the full notebook from a clean kernel; ensure paths are relative; verify outputs and README instructions.

Why: integration catches hidden state and environment assumptions.

Evidence to save: Evidence: clean-run checklist, final notebook, dependency lock, saved experiment outputs.

## Step 11 — Prepare report and presentation

How: write from actual evidence; include method, comparisons, metrics, failures, limitations, responsible-use controls, and contribution statements.

Why: the report and demo should explain decisions and findings, not merely show code.

Evidence to save: Evidence: 10–15-page report excluding appendices/references; 8–10-minute demo; final checklist.

# Suggested repository structure

samsum-generative-ai-project_grp_19/
├── README.md
├── requirements.txt
├── requirements-lock.txt \# generated after smoke test
├── .gitignore
├── docs/
│ ├── 01_Master_Project_Plan.docx
│ ├── 02_Prerequisites_and_Environment_Setup.docx
│ ├── 03_Implementation_Guide.docx
│ ├── 04_Experiment_and_Decision_Log.xlsx or .csv
│ └── decisions/
├── data/
│ ├── raw/ \# source files; commit only if allowed/appropriate
│ └── processed/ \# generated files; normally ignored
├── notebooks/
│ ├── 01_dataset_audit.ipynb
│ ├── 02_baseline_and_prompts.ipynb
│ ├── 03_decoding_and_json.ipynb
│ └── 04_evaluation_and_failures.ipynb
├── src/
│ ├── prompting.py
│ ├── summarizer.py
│ ├── output_schema.json
│ └── evaluation.py
├── experiments/
│ ├── prompt_log.csv
│ ├── decoding_results.csv
│ └── failure_cases.csv
├── outputs/ \# generated outputs; ignore unless curated artifacts
├── report/
└── presentation/

# Experiment naming convention

Use IDs E1–E7 from the assignment. Each run should record: run_id, date/time, owner, commit hash, dataset split and sample IDs, model ID, prompt version, decoding parameters, package-lock reference, output path, evaluation criteria, results, interpretation, and decision.

# Implementation quality rules

- One main variable changes per controlled comparison.

- Never tune on the held-out test sample.

- Save raw model output before parsing or cleaning it.

- Do not silently repair invalid JSON; log the failure and the repair/fallback path.

- Keep secrets, tokens, personal data, \`.venv\`, model caches, and large generated artifacts out of Git.

- Use relative paths and set random seeds where applicable; record that sampling can still vary.

- Mark all results as pending until the experiment actually runs.

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
