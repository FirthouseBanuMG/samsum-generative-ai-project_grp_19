**REFINED PROJECT PLAN**

**SAMSum-Based Conversation Summarization and Action-Item Extraction**

*Repository-aware implementation plan • Technical approach • Checklists • Deliverables*

# 1. Project Snapshot

- Objective: Convert a chat-style dialogue into a concise summary, key points, explicit decisions, and action items.

- Core method: Use a pretrained instruction-tuned causal LLM, compare prompt designs and decoding settings, validate structured JSON, and evaluate output quality.

- Scope: Prompt engineering and inference are the main implementation focus. Do not train a large model from scratch. Actual fine-tuning is optional only if approved and feasible.

- Candidate model: Qwen/Qwen2.5-1.5B-Instruct. Treat it as a candidate until a short local inference test confirms acceptable speed and memory usage.

- System: Windows 64-bit computer. Start with local inference; use a hosted notebook environment if local performance or memory is insufficient.

- Target: Freeze core implementation and results by 21 October 2026; reserve 22–24 October for fixes and rehearsal; submission deadline is 25 October 2026.

# 2. GitHub Repository and Working Agreement

**Team repository:** https://github.com/FirthouseBanuMG/samsum-generative-ai-project_grp_19

- Use the existing repository as the source of truth for code, documentation, experiment logs, and agreed project structure.

- Before creating new files or folders, inspect the current README, directory tree, requirements.txt, notebooks, .gitignore, and existing branches. Reuse working files instead of duplicating them.

- Repository contents have not yet been independently inspected for this revision. The inventory and commands below are a review checklist, not claims about files that already exist.

- Use one branch per workstream or feature. Commit small changes with clear messages; merge through pull requests or team review to avoid overwriting teammates' work.

- Do not commit secrets, personal data, large model weights, virtual environments, or duplicate raw datasets unless the team has explicitly agreed and repository policy allows it. Check .gitignore.

- Keep README setup instructions, requirements.txt, notebook paths, and final report consistent with the implementation.

# 3. Dataset and Model References

**Selected Kaggle dataset:** https://www.kaggle.com/datasets/nileshmalode1/samsum-dataset-text-summarization

**Alternative SAMSum dataset page (not used as this project's download source):** https://huggingface.co/datasets/Samsung/samsum

**Candidate model:** https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct

**Hugging Face Transformers docs:** https://huggingface.co/docs/transformers/index

**PyTorch installation guide:** https://pytorch.org/get-started/locally/

**Google Colab fallback:** https://colab.research.google.com/

- Dataset fields: id, dialogue, summary. The dialogue is input; the human-written summary is the reference output for evaluation.

- Previously supplied CSVs had 14,732 train rows, 818 validation rows, and 819 test rows. One training dialogue was missing. Recheck the current files and document how the missing record is handled.

- Use train data for inspection/examples, validation data for prompt and parameter selection, and a held-out sample of 50–100 test records for final evaluation. Do not tune prompts on the held-out test sample.

- SAMSum contains chat-style conversations, not only formal meetings. Keep the project description accurate: conversation summarization and action-item extraction.

# 4. Prerequisites and Software

| Tool | Purpose | Action / link |
|----|----|----|
| Python 3.11, 64-bit | Runs project code and libraries in an isolated environment. | https://www.python.org/downloads/ |
| Visual Studio Code | Code editor, terminal, debugging, notebook UI. | https://code.visualstudio.com/ |
| VS Code Python extension | Selects interpreter and supports Python debugging. | Install from VS Code Extensions. |
| VS Code Jupyter extension | Runs notebook cells and displays outputs. | Install from VS Code Extensions. |
| Git | Version control and collaboration. | https://git-scm.com/downloads |
| Python libraries | Model inference, data handling, evaluation, validation. | Install into the project's virtual environment. |

- Check installed software before reinstalling. Python 3.13 may coexist with Python 3.11; use a Python 3.11 virtual environment for this project to reduce compatibility risk.

- Anaconda, Docker, Node.js, Angular, a dedicated NVIDIA GPU, and a paid model API are not required to start.

# 5. First-Time Setup Checklist

## A. Inspect the repository

☐ Open the repository in GitHub and review README.md, current folders, requirements.txt, .gitignore, and notebooks.

☐ Clone the repository locally (or open the existing local clone); do not create a second project folder unnecessarily.

☐ Run git status and confirm there are no uncommitted changes before editing.

☐ Record the current file/folder structure so the plan can be aligned with what already exists.

## B. Verify software

- Open Command Prompt (Win + R → cmd) and run these commands one by one:

> python --version
> py --list
> code --version
> git --version

- Share the output with the team before installing anything. Reuse software that is already working.

## C. Create or activate a project environment

- From the repository root, create a virtual environment only if one is not already documented in the repo:

> py -3.11 -m venv .venv
> .venv\Scripts\activate
> python -m pip install --upgrade pip

- Select the .venv interpreter in VS Code. Do not commit the .venv directory.

- If the repository already has a tested requirements.txt, inspect and use it first. Do not blindly install a second, conflicting package list.

- If no dependency file exists, discuss and install the minimum required packages: torch, transformers, accelerate, pandas, numpy, jupyter, ipykernel, rouge-score, jsonschema, matplotlib, and scikit-learn.

- If PyTorch installation fails, use the official PyTorch selector. Verify imports before downloading model weights.

# 6. Repository Review Checklist — Align the Plan with Existing Code

| Inspect | What to confirm | Decision / action |
|----|----|----|
| README.md | Project scope, setup steps, run instructions, team conventions. | Update after the actual pipeline is agreed. |
| requirements.txt / pyproject.toml | Python version and dependency versions. | Keep one agreed dependency source; avoid duplicate package files. |
| notebooks/ | Existing data exploration, baseline, or experiment notebooks. | Extend useful notebooks; avoid duplicate notebooks with overlapping purposes. |
| src/ or scripts/ | Reusable model, prompt, validation, or evaluation code. | Reuse modules where present; create only missing modules. |
| data/ and .gitignore | Dataset storage and ignored files. | Keep original data unchanged; do not commit large data files unless agreed. |
| results/ or outputs/ | Existing output and evaluation formats. | Standardize prompt logs, metrics, and failure cases. |
| Issues / branches / commits | Task ownership and current progress. | Assign owners and avoid conflicting edits. |

# 7. Implementation Workplan — What, How, and Why

| Workstream | How we will implement it | Why it matters / evidence |
|----|----|----|
| 1\. Dataset profiling | Use pandas to check columns, split sizes, missing values, duplicates, dialogue lengths, and sample rows. | Find data issues early; save a concise dataset profile and preprocessing decisions. |
| 2\. Baseline inference | Load tokenizer and Qwen candidate with Hugging Face Transformers; run a simple summary prompt on at least three dialogues. | Establish a baseline. Record model ID, prompt, generation settings, inputs, and outputs. |
| 3\. Prompt comparison | Compare zero-shot, few-shot, role/context, and constraint-based prompts on the same examples; include concise vs detailed instructions. | Test whether prompt structure improves completeness, accuracy, and consistency. Save prompt log. |
| 4\. Decoding comparison | Compare greedy decoding with sampling; test temperature and at least one of top-k or top-p, changing one parameter at a time. | Measure changes in diversity and repeatability. Save the full settings and outputs. |
| 5\. Structured JSON | Request summary, key_points, decisions, and action_items. Each action item has task and assignee; unknown assignee is null. | Create machine-readable output that can be parsed and consumed by code. |
| 6\. Validator function | Implement a Python function to validate JSON keys/types and action-item fields. Test valid and invalid examples. | Demonstrate a callable tool/function and catch formatting errors. |
| 7\. Evaluation | Use ROUGE plus a defined manual rubric for information coverage, factual consistency, and action-item quality; measure JSON validity. | Multiple criteria reveal errors that text-overlap scores alone may miss. |
| 8\. Failure analysis | Record at least three real failures with dialogue ID, output, failure category, impact, and likely cause. | Provide evidence-based limitations and explain need for human review. |
| 9\. Integration | Combine selected prompt, model inference, validation, and evaluation in one runnable notebook or agreed demo. | Produce a reproducible end-to-end deliverable. |

# 8. Output Contract and Validation

- Proposed JSON structure; align with any schema already implemented in the repository before changing it:

> {
> "summary": "Short summary of the conversation",
> "key_points": \["Important point"\],
> "decisions": \["Decision explicitly stated"\],
> "action_items": \[
> {"task": "Follow-up task", "assignee": null}
> \]
> }

- Only include decisions and tasks supported by the dialogue. Use empty lists if none are present and null for an unknown assignee; never guess.

- Parse the response with Python's json module and validate required keys and types with a schema. JSON validity does not prove factual correctness.

# 9. Required Experiments and Evidence Checklist

☐ E1 — Baseline: save at least three model outputs with prompts and settings.

☐ E2 — Prompting: compare zero-shot, few-shot, role/context, and constraint-based prompting on matched examples.

☐ E3 — Decoding: compare greedy and sampling; include temperature and top-k or top-p.

☐ E4 — Structured output: save schema, valid/invalid examples, and validation results.

☐ E5 — Tool/function: demonstrate validator input, invocation, output, and failure message.

☐ E6 — Failure analysis: document at least three observed model failures.

☐ E7 — Integrated demo: run the full pipeline in the agreed notebook or demo.

☐ Keep prompt_log.csv, decoding_comparison.csv, evaluation_results.csv, and failure_cases.csv (or the equivalent existing repo format).

☐ Do not report planned scores as results or claim a prompt is better without evidence.

# 10. Evaluation Criteria

| Criterion | Method |
|----|----|
| ROUGE | Compare generated summaries with reference summaries. |
| Information coverage | Use a defined rubric to check whether important dialogue facts are retained. |
| Factual consistency | Compare generated claims with the original dialogue and mark unsupported claims. |
| JSON validity | Check parsing, required fields, and data types. |
| Action-item quality | Check whether tasks are supported and assignees are correct or null when unknown. |

- Use the same validation examples for fair prompt comparisons. Keep the held-out test sample for final evaluation only.

- Report sample size, metrics, rubric, results, and limitations. Do not rely on ROUGE alone.

# 11. Team Responsibilities and Git Workflow

| Owner | Suggested responsibility | Expected evidence |
|----|----|----|
| Member 1 | Repository/data review and baseline | Repository inventory, data profile, baseline outputs |
| Member 2 | Prompt and decoding experiments | Prompt log and decoding comparison |
| Member 3 | JSON schema and validator function | Schema, validation code, valid/invalid tests |
| Member 4 | Evaluation, failure analysis, report integration | Evaluation table, failure cases, report/slide draft |
| All members | Review and individual contribution statements | Verified results and accurate contribution notes |

- Agree on task owners and file names. Make small commits, review each other's changes, and keep the default branch runnable.

- Before finalizing, test the instructions on a clean environment or ask another team member to follow the README.

# 12. Timeline

| Date | Target |
|----|----|
| 15–16 Oct 2026 | Inspect repo, verify setup, validate dataset, run baseline. |
| 17–18 Oct 2026 | Complete prompt and decoding experiments; implement JSON/function validation. |
| 19–20 Oct 2026 | Evaluate outputs, document failures, integrate notebook, draft report and slides. |
| 21 Oct 2026 | Freeze code, evidence, and main results. |
| 22–24 Oct 2026 | Buffer for fixes, reruns, proofreading, and presentation rehearsal. |
| 25 Oct 2026 | Submission deadline. |

# 13. Final Deliverables Checklist

☐ 10–15-page report, excluding appendix and references.

☐ Runnable notebook or equivalent implementation, with setup instructions.

☐ Dataset/preprocessing record and prompt log.

☐ Decoding comparison table.

☐ JSON schema, sample outputs, and validation results.

☐ Tool/function demonstration.

☐ Evaluation table and at least three failure cases.

☐ 8–10-minute presentation.

☐ Individual contribution statements.

☐ README and dependency instructions verified against the actual repository.

# 14. Next Action

- First, inspect the repository's actual file tree, README, dependency file, notebooks, and recent commits. Then compare those findings with Sections 5–8 and revise the folder plan to match the code already present.

- I could not reliably retrieve the repository contents through the current web connection. The repository URL is included, but this document does not claim to have audited its current files. For a truly repo-specific revision, connect the GitHub integration or upload/paste the README and file tree.

- After the repository inventory is confirmed, freeze the agreed architecture and only then begin installing missing packages or creating new modules.

# Reference Links

**Team GitHub repository:** https://github.com/FirthouseBanuMG/samsum-generative-ai-project_grp_19

**SAMSum Kaggle dataset:** https://www.kaggle.com/datasets/nileshmalode1/samsum-dataset-text-summarization

**Alternative SAMSum dataset page (not used as this project's download source):** https://huggingface.co/datasets/Samsung/samsum

**Qwen2.5-1.5B-Instruct:** https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct

**Python downloads:** https://www.python.org/downloads/

**VS Code:** https://code.visualstudio.com/

**Git:** https://git-scm.com/downloads

**Transformers documentation:** https://huggingface.co/docs/transformers/index

**PyTorch installation:** https://pytorch.org/get-started/locally/

**Google Colab:** https://colab.research.google.com/

**Status note:** This is a refined, repository-aware planning draft. The project requirements and previously agreed dataset/model approach are preserved; repository-specific code inventory remains pending until the repository can be read.
