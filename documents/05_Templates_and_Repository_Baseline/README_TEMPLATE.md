# SAMSum-Based Intelligent Conversation Summarization and Action-Item Extraction

Applied Generative AI major project, Group 19.

## Project location
Open the repository root on your computer.

## Project goal
Summarize chat-style SAMSum dialogues and extract only explicitly supported action items into validated structured output.

## Environment status
- Use the Python version and dependencies specified by the project setup guide.
- A repository-local `.venv` is recommended.
- CPU execution is supported; performance varies by hardware.
- Record environment checks and model test results without including personal machine details or local absolute paths.

## Reproduce the environment
Run from the repository root in PowerShell. Use the explicit `.venv` Python path; activation is not required.

```powershell
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m pip freeze
```

The repository's dependency files record the required package versions. Ensure `.gitignore` excludes `.venv/`, `.env` files, model caches, generated outputs, and large model weights.

## Data and experiment integrity
- Keep original SAMSum CSVs unchanged.
- Record source, split, sample IDs, model ID/revision, prompt version, decoding parameters, package lock, and Git commit for every run.
- Use validation data for prompt/configuration selection; reserve a separate held-out test subset for final reporting.
- Report only measured results. No baseline generation, latency, memory, or metric result has been verified yet.

## Required outputs
Runnable notebook; dataset/preprocessing notes; at least three baseline examples; four prompt variants; decoding comparison; JSON schema and validation; callable function/tool demonstration; evaluation using at least four criteria; at least three real failure cases; responsible-use controls; report; presentation; individual contribution statements.
