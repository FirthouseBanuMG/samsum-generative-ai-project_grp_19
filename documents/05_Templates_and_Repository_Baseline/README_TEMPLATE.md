# SAMSum-Based Intelligent Conversation Summarization and Action-Item Extraction

Applied Generative AI major project, Group 19.

## Current local project path
`D:\BITS-Projects\samsum-generative-ai-project_grp_19`

## Project goal
Summarize chat-style SAMSum dialogues and extract only explicitly supported action items into validated structured output.

## Environment status (15 October 2026)
- Python 3.13.9 in repository-local `.venv`
- PyTorch 2.13.0+cpu; CPU execution selected; CUDA unavailable in the current environment
- NumPy 2.5.4; pandas 3.0.6; Transformers 5.19.0; Accelerate 1.15.0
- Jupyter kernel: `Python (SAMSum Project)`
- `pip check`: no broken requirements found
- Qwen model access/load/generation: pending; do not claim results until tested

## Reproduce the current environment
Run from the project root in PowerShell. Use the explicit `.venv` Python path; activation is not required.

```powershell
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m pip freeze
```

The local `requirements-lock.txt` records the installed environment. Review it before committing. Ensure `.gitignore` excludes `.venv/`, `.env` files, model caches, generated outputs, and large model weights.

## Data and experiment integrity
- Keep original SAMSum CSVs unchanged.
- Record source, split, sample IDs, model ID/revision, prompt version, decoding parameters, package lock, and Git commit for every run.
- Use validation data for prompt/configuration selection; reserve a separate held-out test subset for final reporting.
- Report only measured results. No baseline generation, latency, memory, or metric result has been verified yet.

## Required outputs
Runnable notebook; dataset/preprocessing notes; at least three baseline examples; four prompt variants; decoding comparison; JSON schema and validation; callable function/tool demonstration; evaluation using at least four criteria; at least three real failure cases; responsible-use controls; report; presentation; individual contribution statements.
