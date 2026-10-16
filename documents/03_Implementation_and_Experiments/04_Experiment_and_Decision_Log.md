*Reusable recording templates • fill with actual evidence*

Project: SAMSum-Based Intelligent Conversation Summarization and Action-Item Extraction

Document status: Version 0.2 — updated 15 October 2026

Working rule: Record proposed choices as proposed until the team verifies them. Never report unrun experiments as results.

# A. Experiment run record

| **Field** | **What to record** |
|----|----|
| Run ID | E1-01, E2-03, etc. |
| Date / owner | Actual date, owner, reviewer |
| Git commit | Commit hash used for the run |
| Dataset | Source, split, exact sample IDs |
| Model | Model ID and revision if available |
| Prompt | Prompt ID/version and full prompt path |
| Decoding | do_sample, temperature, top_k, top_p, max_new_tokens, seed where relevant |
| Environment | Python version and requirements-lock file/hash |
| Output | Path to raw generated output |
| Evaluation | Metric values and rubric scores; describe scoring method |
| Observation | What happened, including failures |
| Decision | Keep/change/reject and why |

# B. Prompt comparison log

| **Run ID** | **Prompt type** | **Main change** | **Fixed variables** | **Sample IDs** | **Observed quality** | **Decision** |
|----|----|----|----|----|----|----|
| E2-01 | Zero-shot | Baseline instruction | Model, decoding, inputs | TBD | Pending run | Pending |
| E2-02 | Few-shot | Add selected examples | Model, decoding, inputs | TBD | Pending run | Pending |
| E2-03 | Role/context | Add role and task context | Model, decoding, inputs | TBD | Pending run | Pending |
| E2-04 | Constraint-based | Add length/faithfulness/JSON constraints | Model, decoding, inputs | TBD | Pending run | Pending |

# C. Decoding comparison log

| **Run ID** | **Mode** | **Temperature** | **top_k/top_p** | **Repeat count** | **Quality / variability** | **Runtime** |
|----|----|----|----|----|----|----|
| E3-01 | Greedy | N/A or framework default | N/A | 1 | Pending run | Pending |
| E3-02 | Sampling | 0.2 | top_p=0.9 (proposed) | 3 | Pending run | Pending |
| E3-03 | Sampling | 0.7 | top_p=0.9 (proposed) | 3 | Pending run | Pending |

# D. Failure case log

| **Failure ID** | **Category** | **Input/sample ID** | **Actual output** | **Expected behavior** | **Impact** | **Mitigation** |
|----|----|----|----|----|----|----|
| F-01 | Hallucinated action item | TBD | Capture actual output | Only explicit action items | TBD | Prompt/schema/validation/human review |
| F-02 | Omission / loss of key fact | TBD | Capture actual output | Preserve key decisions | TBD | Prompt adjustment and rubric |
| F-03 | Invalid JSON or attribution error | TBD | Capture actual output | Schema-valid output / correct speaker | TBD | Parser, schema validation, safe fallback |

# E. Decision record

| **Decision ID** | **Date** | **Decision** | **Alternatives** | **Rationale/evidence** | **Owner** | **Revisit trigger** |
|----|----|----|----|----|----|----|
| D-001 | 15 Oct 2026 | Use SAMSum as the project dataset (confirm files) | AG News or another dataset | Project direction already selected; chat dialogues align with summary/action extraction | Team | If rubric or data access blocks use |
| D-002 | 15 Oct 2026 | Test Qwen2.5-1.5B-Instruct as candidate baseline | Other small causal LMs | Instruction-tuned causal LM; small enough to pilot, but CPU performance must be measured | Model owner | If model load or latency fails |

# F. Rules for honest reporting

- Never replace 'Pending run' with a guessed score.

- Record negative and inconclusive results; they are useful evidence.

- If a prompt or model changes, create a new run ID rather than overwriting prior results.

- Separate automatic metric results from human judgments.

- Keep final test-set results separate from prompt-selection results.

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

# G. Data-use and evaluation protocol

**Decision date:** 16 October 2026
**Status:** Agreed working protocol; apply consistently to subsequent experiments.

## G.1 Dataset split usage

- **Training split:** Use selected examples for initial pipeline smoke tests. These outputs are qualitative debugging evidence, not independent evaluation results.
- **Validation split:** Reserve for controlled development experiments, prompt comparisons, and model/decoding selection.
- **Test split:** Reserve for final evaluation after the experimental protocol and configurations have been finalized.
- **Raw files:** Preserve the original dataset files without modification.
- **Preprocessing:** Use the documented processed splits and record exclusions and sample IDs.

## G.2 Exploratory validation inspection

Six validation examples were inspected during exploratory review: `13817023`, `13716628`, `13829420`, `13819648`, `13728448`, and `13814197`.

This inspection did not generate model outputs. These examples are not selected for the initial baseline smoke test. The attempted sample-manifest file was not found at the expected project path, so no manifest is assumed to exist.

## G.3 Rationale and safeguards

Training examples are used for initial pipeline verification to avoid consuming validation examples for this smoke test. Validation results may inform development decisions and therefore must not be represented as an untouched final test. Test-set evaluation should occur only after model, prompt, decoding, and evaluation choices are fixed.

**Next action:** Select three training examples, record their IDs and selection rationale, and run the initial baseline smoke test.

# H. Initial baseline smoke-test sample selection

**Date:** 16 October 2026
**Experiment:** `initial_baseline_smoke_test`
**Dataset split:** Processed training split
**Purpose:** Qualitative pipeline verification only; not a performance estimate.

| Sample ID | Conversation type | Selection rationale |
|---|---|---|
| `13818513` | Simple request and agreement | Check preservation of the key event and future action. |
| `13681000` | Advice and tentative action | Check whether a suggestion is distinguished from a confirmed decision. |
| `13728094` | Longer multi-speaker discussion | Check preservation of the main problem and advice without speaker confusion. |

**Manifest:** `data/processed/baseline_sample_manifest.json`

**Data-use safeguard:** These samples come from the training split. Validation and test examples are not used to generate outputs in this smoke test. The three examples are intentionally selected for pipeline verification and must not be presented as a representative evaluation sample.

**Status:** Sample selection recorded; baseline generation pending.

## I. Initial Baseline Smoke-Test Results

**Date:** 16 October 2026
**Experiment:** `initial_baseline_smoke_test`
**Model:** `Qwen/Qwen2.5-1.5B-Instruct`
**Execution device:** CPU; CUDA unavailable
**Dataset split:** Training
**Decoding:** Greedy (`do_sample=False`), maximum 100 new tokens
**Samples:** `13818513`, `13681000`, `13728094`

### Execution outcome

The model loaded successfully and generated summaries for all three selected training examples. The results and run metadata were saved to:

- `outputs/baseline_smoke_test/baseline_outputs.json`
- `outputs/baseline_smoke_test/run_metadata.json`

Both files were verified to exist and parse as valid JSON. This was a qualitative pipeline smoke test, not a quantitative evaluation.

### Qualitative observations

1. **Sample `13818513`:** The generated summary captured the cookies and their planned delivery to Jerry the following day. It was broadly consistent with the reference.
2. **Sample `13681000`:** The generated summary included the Pomodoro suggestion but added unsupported details about moving belongings the next day and using post-it notes in a kanban-style system.
3. **Sample `13728094`:** The generated summary captured Rick's dissatisfaction and Naomi's advice, but added unsupported claims that Sam decided against confronting Rick and planned to address the situation later.

### Decision and limitations

- Retain the output artifacts as evidence of a successful end-to-end baseline run.
- Treat the unsupported details in samples `13681000` and `13728094` as initial hallucination observations to investigate in later experiments.
- Do not report an accuracy score or generalize model performance from three examples.
- Keep the test split reserved for final evaluation. Use the validation split for controlled prompt and configuration comparisons.
- Record the prompt, decoding configuration, and observed failure cases for reproducibility.

**Status:** Initial baseline smoke test completed; controlled evaluation remains pending.
