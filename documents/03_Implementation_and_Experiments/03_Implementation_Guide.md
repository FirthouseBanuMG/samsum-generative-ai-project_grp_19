*Step-by-step build sequence • what • how • why • evidence*

Project: SAMSum-Based Intelligent Conversation Summarization and Action-Item Extraction

Document status: Original implementation sequence, version 0.2 (15 October 2026). This sequence is retained as planning history; it is not a current task-status checklist.

For current run commands, use the [Environment Setup and Run Guide](../02_Environment_Setup/Prerequisites_and_Environment_Setup.md). For completed work and remaining closeout items, use the [Master Project Plan](../01_Project_Planning/Master_Project_Plan.md) and [Assignment-to-Evidence Matrix](./03_Assignment_to_Evidence_Matrix.md). Actual experiment outcomes are recorded in the [Experiment and Decision Log](./04_Experiment_and_Decision_Log.md).

The steps and suggested repository structure below preserve the original planning snapshot. Several proposed tasks are now complete, and the proposed layout is not the current repository layout. Do not use the snapshot to infer current status or copy its proposed paths.

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
├── documents/ \# Markdown-first plans, setup guides, and experiment evidence
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

# Environment reproducibility

Follow the current [Environment Setup and Run Guide](../02_Environment_Setup/Prerequisites_and_Environment_Setup.md) from the repository root. It describes the supported software, dependency installation, dataset preparation, application run, and tests.

For experiment records, capture the project-relevant Python and dependency versions, model identifier, dataset split and sample IDs, settings, and results. Use repository-relative paths in shared records. Do not include personal hardware details, local absolute paths, free-space readings, user-folder locations, or unrelated machine state.

Run environment checks from the repository root:

```powershell
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m pytest tests
```
