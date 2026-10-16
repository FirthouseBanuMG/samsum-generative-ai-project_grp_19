*Scope • rationale • architecture • milestones • ownership*

Project: SAMSum-Based Intelligent Conversation Summarization and Action-Item Extraction

Document status: Version 0.2 — updated 15 October 2026

Working rule: Record proposed choices as proposed until the team verifies them. Never report unrun experiments as results.

# 1. Purpose and working principles

This project will build and evaluate a reproducible, prompt-driven conversation summarization system using the SAMSum dialogue dataset. The system will generate concise summaries and extract action items into a validated machine-readable structure. The implementation is an educational prototype, not a production decision system.

Why this document exists: it is the source of truth for scope, decisions, ownership, deadlines, and deliverables. The implementation guide explains how to execute tasks; the experiment log records what actually happened.

# 2. Problem definition

Given a short, chat-style dialogue, produce (a) a faithful concise summary and (b) structured action items when the dialogue supports them. The system must avoid inventing people, deadlines, commitments, or decisions. If no action item is explicit, it should return an empty list rather than fabricate one.

# 3. Project goals and non-goals

- Goals: understand the dataset; establish a pretrained causal-LM baseline; compare prompt strategies and decoding settings; validate structured output; demonstrate a callable tool/function; evaluate quality and failure cases; document responsible-use controls.

- Goals: make the notebook reproducible, maintain a prompt/experiment log, and report evidence-based results.

- Non-goals: training a foundation model from scratch; building a production service; claiming clinical/legal-grade reliability; adding a vector database or RAG unless the team and rubric justify it.

- Fine-tuning/PEFT: compare conceptually with prompting and RAG. Implement only if the course rubric explicitly requires it and the team has time.

# 4. Dataset and model decisions

| **Item** | **Baseline decision** | **Why / validation needed** |
|----|----|----|
| Dataset | SAMSum; retain train/validation/test split | Chat-style dialogues with reference summaries; useful for summary generation. Confirm the exact downloaded files and column names before coding. |
| Primary data fields | id, dialogue, summary (verify) | The CSVs previously noted use these fields; confirm against the files in the repo before relying on them. |
| Model candidate | Qwen/Qwen2.5-1.5B-Instruct | Small instruction-tuned causal LM candidate; model card documents Transformers use. Must pass a local smoke test; CPU latency may be high. |
| Execution | Local Windows/CPU for setup and small tests; Colab GPU as fallback | Avoid assuming the laptop has a supported NVIDIA GPU. Keep code portable. |
| Final evaluation | Validation for prompt/config selection; held-out test subset for final report | Prevents tuning on the same examples used for final claims. |

# 5. Assignment requirement map

| **Requirement / experiment** | **Evidence we will retain** |
|----|----|
| Problem definition + dataset understanding | Problem statement, dataset card/columns/counts, examples, limitations. |
| Compare ≥3 generative model families covered in CS1 | Short comparison table with citations to course material. Team must verify which families were actually taught; do not guess. |
| Explain LLM architecture | Tokenization, embeddings, Transformer/attention, LM head, autoregressive generation explanation/diagram. |
| Pretrained causal-LM baseline | Runnable baseline code and ≥3 example outputs. |
| Prompting comparison | Zero-shot, few-shot, role/context-based, and constraint-based prompt variants. |
| Decoding comparison | Greedy vs sampling; temperature and at least one of top-k/top-p; settings and observed variability. |
| Prompting vs RAG vs fine-tuning/PEFT | Evidence-backed trade-off discussion; implementation only where required. |
| Structured output | JSON schema, valid/invalid examples, validation results. |
| Tool/function | Input/output schema, invocation example, and simulated or actual call result. |
| Reusable parameterized prompt | Prompt template/function with configurable parameters. |
| Evaluation and failure analysis | At least four criteria, scoring rubric, and at least three failure cases. |
| Responsible use | Privacy, hallucination, bias, omission, overreliance, and human-review controls. |
| Integrated demo | Runnable notebook/app and presentation walkthrough. |

# 6. Evaluation plan

- Use at least four criteria: factual faithfulness, coverage of key points, conciseness/readability, and action-item correctness/completeness. Add JSON validity as a separate technical criterion.

- Use ROUGE as a reference-overlap metric, not as the sole measure of quality. Include human rubric-based review of a manageable sample.

- Keep a held-out final test subset (target 50–100 examples if runtime permits). Choose the final size after timing a pilot; document the exact IDs and selection method.

- For each failure case, preserve the input dialogue, model output, expected/reference interpretation, failure category, likely cause, and proposed mitigation.

# 7. Architecture (initial)

1.  Load and validate SAMSum splits; inspect missing values, duplicates, lengths, and representative dialogues.

2.  Build a parameterized prompt that asks for a concise summary and explicit action items only.

3.  Run a pretrained causal LM with a baseline decoding configuration.

4.  Run controlled prompt and decoding experiments; change one main factor at a time.

5.  Parse generated output; validate it against a JSON schema; handle malformed output safely.

6.  Expose the summarization function as a reusable tool with a documented input/output contract.

7.  Evaluate outputs using automatic metrics and a human rubric; analyze errors and responsible-use risks.

8.  Package notebook, requirements/version record, prompts, experiment logs, outputs, report, and demo.

# 8. Team workflow and ownership

There are four team members. Assign one accountable owner per workstream and a reviewer. Replace placeholders below at the first team meeting.

| **Workstream** | **Accountable owner** | **Reviewer / backup** | **Evidence** |
|----|----|----|----|
| Dataset + EDA | Member A (assign) | Member B (assign) | Dataset notes, validation checks, sample IDs |
| Model + prompt experiments | Member B (assign) | Member C (assign) | Prompt log, baseline and E1–E3 outputs |
| JSON + tool + integration | Member C (assign) | Member D (assign) | Schema, validator, tool invocation, E4–E5 |
| Evaluation + report + demo | Member D (assign) | All members review | E6–E7, report, slides, contribution statements |

All members must understand the end-to-end workflow and be able to explain at least one technical component. Keep contributions truthful and traceable in Git commits or the contribution statement.

# 9. Timeline (deadline: 25 October 2026)

| **Target date** | **Milestone** | **Exit condition** |
|----|----|----|
| 15 Oct | Reset and environment baseline | Repository reviewed; software versions recorded; smoke test passes. |
| 16–17 Oct | Dataset + baseline | Splits load; columns/quality documented; ≥3 baseline outputs saved. |
| 18–19 Oct | Prompt and decoding experiments | Four prompt variants and decoding comparisons logged. |
| 20 Oct | JSON schema + tool + failures | Schema validation and tool call demonstrated; ≥3 failure cases captured. |
| 21 Oct | Evaluation + integration freeze | Metrics/rubric completed; notebook runs end-to-end. |
| 22–24 Oct | Report, slides, rehearsal, fixes | Reproducibility check, 8–10 minute demo rehearsal, contribution statements. |
| 25 Oct | Submission | Final package checked against assignment requirements. |

# 10. Risks and controls

| **Risk** | **Control** |
|----|----|
| CPU model is too slow | Pilot on 3–5 records; cap test sample; use Colab GPU fallback without changing experiment definitions. |
| Prompt/model output is malformed | Use explicit JSON-only instruction, parser, schema validation, and a safe failure path. |
| Hallucinated action items | Require evidence from dialogue; allow empty list; human-review ambiguous cases. |
| Team member unavailable | Keep one owner and one reviewer per workstream; commit code and notes frequently. |
| Late scope creep | Do not add fine-tuning, RAG infrastructure, UI, or deployment unless required and core experiments are complete. |
| Unreproducible results | Record model ID, package versions, seed, prompt version, generation parameters, split and sample IDs. |

# 11. Definition of done

- Every required experiment has a recorded configuration and actual output.

- The notebook executes from a clean environment or clearly documents any platform-specific step.

- Final test data was not used for prompt tuning.

- At least four evaluation criteria and three failure cases are documented.

- The report (10–15 pages excluding appendices/references), 8–10 minute presentation/demo, runnable notebook, data/preprocessing notes, prompts, schema, tool demo, and individual contribution statements are ready.

- Every team member can explain the problem, model, prompts, evaluation, limitations, and their own contribution.

# 12. External references

- SAMSum dataset (Hugging Face): https://huggingface.co/datasets/Samsung/samsum

- SAMSum CSV source previously selected: https://www.kaggle.com/datasets/nileshmalode1/samsum-dataset-text-summarization

- Candidate model: https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct

- PyTorch installation guidance: https://pytorch.org/get-started/locally/

- Transformers documentation: https://huggingface.co/docs/transformers/

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
