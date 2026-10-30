**GETTING STARTED GUIDE**

**SAMSum-Based Intelligent Conversation Summarization and Action-Item Extraction**

*Prerequisites • Software setup • Implementation plan • Checklists • Deliverables*

# 1. Project at a Glance

- Goal: Convert a chat-style conversation into a concise summary, key points, decisions, and action items.

- Approach: Use a pretrained causal/autoregressive language model through Hugging Face Transformers. Compare prompt designs and decoding settings; do not train a large model from scratch.

- Candidate model: Qwen/Qwen2.5-1.5B-Instruct. Test its speed and memory usage locally before committing to it.

- Execution: Develop in a Python notebook using VS Code. Use Google Colab as a fallback if local inference is too slow or memory-intensive.

- System: Windows 64-bit computer. CPU inference may be slow depending on available hardware.

- Team of four. Target implementation/results freeze: 21 October 2026; reserve 22–24 October for fixes and rehearsal; deadline: 25 October 2026.

- This is a plan. Report only results and measurements actually obtained.

# 2. Laptop and System Prerequisites

| Item | Requirement / plan |
|----|----|
| Computer | Windows 64-bit computer with sufficient memory and storage for the selected model and dataset. |
| Storage | Keep several GB free for packages, model files, dataset, notebook outputs, and results. |
| Internet | Needed for first-time downloads of packages, data, and model weights. |
| Permissions | Ability to install software and create project folders. |
| Compute | Start with CPU/local inference; use Colab if performance or memory is inadequate. Dedicated NVIDIA GPU is not required to begin. |

# 3. Software to Install or Verify

| Software | Purpose | Link / action |
|----|----|----|
| Python 3.11, 64-bit | Runs code and libraries in a separate virtual environment. | https://www.python.org/downloads/ |
| Visual Studio Code | Editor, terminal, debugging, notebook interface. | https://code.visualstudio.com/ |
| VS Code Python extension | Interpreter selection and Python debugging. | Install in VS Code Extensions. |
| VS Code Jupyter extension | Runs notebook cells and displays results. | Install in VS Code Extensions. |
| Git | Tracks code changes and supports team collaboration. | https://git-scm.com/downloads |
| Google Colab (backup) | Cloud notebook if local model inference is too slow. | https://colab.research.google.com/ |

- You may already have VS Code and Git from earlier projects. Verify before reinstalling.

- Install the Python version specified in the current project environment guide.

- Anaconda, Docker, Node.js, Angular, and a paid model API are not required for the planned workflow.

# 4. Dataset and Model Links

**Selected Kaggle dataset:** https://www.kaggle.com/datasets/nileshmalode1/samsum-dataset-text-summarization

**Alternative SAMSum dataset page (not used as this project's download source):** https://huggingface.co/datasets/Samsung/samsum

**Candidate model: Qwen2.5-1.5B-Instruct:** https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct

**Hugging Face Transformers documentation:** https://huggingface.co/docs/transformers/index

**PyTorch installation guide:** https://pytorch.org/get-started/locally/

- Kaggle login may be required to download the selected dataset. Follow current dataset/model terms.

- CSV fields: id, dialogue, summary. The dialogue is input; the human-written summary is the reference for evaluation.

- Previously inspected CSVs contained 14,732 train, 818 validation, and 819 test rows; one training dialogue was missing. Recheck the files and document how missing data is handled.

- SAMSum contains chat-style conversations, not only formal business meetings. Describe the task as conversation summarization and action-item extraction.

# 5. Recommended Project Folder Structure

samsum-genai-project/
├── data/raw/ \# Original CSV files (keep unchanged)
├── data/processed/ \# Cleaned/sample data if needed
├── notebooks/
│ └── samsum_project.ipynb \# Main runnable notebook
├── src/
│ ├── prompts.py \# Reusable prompt templates
│ ├── output_validation.py \# JSON and action-item checks
│ └── evaluation.py \# Evaluation helpers
├── results/
│ ├── prompt_log.csv
│ ├── decoding_comparison.csv
│ ├── evaluation_results.csv
│ └── failure_cases.csv
├── report/
├── presentation/
├── requirements.txt
└── README.md

- Keep original CSVs unchanged and save generated outputs/measurements separately for reproducibility.

# 6. Setup Checklist — Follow in Order

## A. Verify installed software

☐ Open Command Prompt (Win + R → cmd); run: python --version

☐ Run: py --list (lists installed Python versions on Windows).

☐ Run: code --version

☐ Run: git --version

☐ Copy the outputs before installing anything; do not reinstall working software.

## B. Create project folder and virtual environment

- Create a folder such as D:\SAMSum-GenAI-Project and open it in VS Code.

- Open Terminal → New Terminal and run:

> py -3.11 -m venv .venv
> .venv\Scripts\activate
> python -m pip install --upgrade pip

- If py -3.11 fails, install Python 3.11 (64-bit), reopen VS Code, and retry.

- Select the interpreter inside .venv in VS Code; use it for the project terminal and notebook.

## C. Install extensions and Python libraries

- Install the Python and Jupyter extensions from VS Code Extensions.

- With the virtual environment activated, run:

> python -m pip install torch transformers accelerate pandas numpy
> python -m pip install jupyter ipykernel rouge-score jsonschema matplotlib scikit-learn

- If PyTorch installation fails, follow the official PyTorch installation selector linked above.

- Save installed package versions: python -m pip freeze \> requirements.txt

- Create a notebook and select the .venv Python kernel.

## D. Verify imports

> python -c "import torch, transformers, pandas, numpy; print(torch.\_\_version\_\_); print(transformers.\_\_version\_\_); print('CUDA:', torch.cuda.is_available())"

- CUDA may show False on a laptop without a supported NVIDIA GPU; CPU execution can still work.

- Do not download model weights until package imports pass.

# 7. Dataset Preparation Checklist

☐ Place the three CSV files in data/raw/ and keep the originals unchanged.

☐ Load each file with pandas and confirm columns id, dialogue, summary.

☐ Print split sizes and inspect representative rows.

☐ Check missing values and duplicate IDs/records; record any rows excluded or corrected.

☐ Use 20–30 dialogues for initial development and debugging.

☐ Use validation examples to compare prompts and settings.

☐ Reserve 50–100 held-out test dialogues for final evaluation; do not tune prompts on them.

☐ Record the data profile and preprocessing decisions in the report.

# 8. Implementation Plan — What, How, and Why

| Stage | How we will implement it | Why it matters |
|----|----|----|
| 1\. Baseline | Load model and tokenizer with Transformers; use a simple summarization prompt on at least three dialogues. | Creates a reference point for later comparisons. |
| 2\. Prompt experiments | Compare zero-shot, few-shot, role/context, and constraint-based prompts on the same examples. | Tests whether instructions/examples improve completeness and factual consistency. |
| 3\. Decoding | Compare greedy decoding with sampling; test temperature and at least one of top-k or top-p. Change one setting at a time. | Shows how generation settings affect variation and reliability. |
| 4\. JSON output | Request summary, key_points, decisions, and action_items; each action item has task and assignee. | Makes output machine-readable and easier to validate. |
| 5\. Validation function | Write a Python function to check required JSON fields and action-item types; test valid and invalid examples. | Demonstrates a programmatic tool and catches malformed output. |
| 6\. Evaluation | Measure ROUGE; assess information coverage, factual consistency, JSON validity, and action-item quality. | Multiple criteria are needed because text overlap alone cannot detect every error. |
| 7\. Failure analysis | Record at least three actual failures, e.g. omitted facts, invented details, wrong assignee, invalid JSON. | Makes limitations concrete and supports responsible-use discussion. |
| 8\. Integrated notebook | Combine model, prompt template, generation, validation, evaluation, and example outputs. | Provides a reproducible end-to-end deliverable. |

# 9. Prompt Template and JSON Design

- Create a reusable prompt function with placeholders for the dialogue and summary style (concise or detailed).

- Tell the model not to invent information. Use empty lists if no decisions or action items are present.

> {
> "summary": "Short summary of the conversation",
> "key_points": \["Important point"\],
> "decisions": \["Decision explicitly stated"\],
> "action_items": \[
> {"task": "Follow-up task", "assignee": null}
> \]
> }

- Parse output using Python's json module and validate keys/types using a schema. Record invalid output instead of silently accepting it.

- Only include decisions and tasks supported by the dialogue. Use null for unknown assignees; never guess.

# 10. Required Experiments and Evidence Checklist

☐ E1 — Baseline: save at least three prompts, settings, and generated outputs.

☐ E2 — Prompt comparison: compare all four required prompt styles on the same examples.

☐ E3 — Decoding: compare greedy and sampling; include temperature and top-k or top-p.

☐ E4 — Structured output: save schema, valid/invalid examples, and validation results.

☐ E5 — Tool/function: show validator input, output, and invocation for valid and invalid cases.

☐ E6 — Failure analysis: document at least three real failures and likely causes.

☐ E7 — Integrated system: execute the complete pipeline in the notebook.

☐ Maintain a prompt log with dialogue ID, prompt type, model, decoding parameters, output, and observations.

☐ Do not invent scores or claim one prompt is better until actual results support the conclusion.

# 11. Evaluation Plan

| Criterion | How to evaluate |
|----|----|
| ROUGE | Compare generated summaries with reference summaries using ROUGE scores. |
| Important-information coverage | Use a defined rubric to check whether important facts from the dialogue are retained. |
| Factual consistency | Compare output claims with the source dialogue and mark unsupported claims. |
| JSON validity | Measure whether output parses and contains required fields with correct data types. |
| Action-item quality | Check task support and assignee correctness; unknown assignees should be null. |

- Use the same evaluation sample for fair prompt comparisons. Do not tune the system using the held-out final test sample.

- Record sample size, metrics, manual rubric, results, and limitations.

# 12. Responsible Use and Limitations

- Use the supplied dataset; do not put confidential real conversations into the model.

- Outputs may omit facts, invent details, or assign tasks incorrectly.

- Check generated summaries against the original dialogue before relying on them.

- JSON validation checks format, not factual correctness.

- Report limitations and real failure examples honestly.

# 13. Suggested Team Responsibilities

| Owner | Responsibility | Evidence |
|----|----|----|
| Member 1 | Dataset checks and baseline | Data profile, preprocessing notes, baseline outputs |
| Member 2 | Prompt and decoding experiments | Prompt log and decoding comparison table |
| Member 3 | JSON schema and tool/function | Schema, validation code, valid/invalid demonstrations |
| Member 4 | Evaluation and integration | Evaluation table, failure cases, report/slides integration |
| All members | Review and contribution statements | Verified results and accurate account of individual work |

- Agree on shared file names and one final notebook. Each member must describe their actual contribution.

# 14. Timeline

| Date | Target |
|----|----|
| 15–16 Oct 2026 | Verify software, create environment, inspect data, run baseline. |
| 17–18 Oct 2026 | Complete prompt/decoding experiments and implement JSON/function validation. |
| 19–20 Oct 2026 | Evaluate outputs, document failures, integrate notebook, draft report and slides. |
| 21 Oct 2026 | Freeze implementation and main results. |
| 22–24 Oct 2026 | Buffer for fixes, reruns, proofreading, and presentation rehearsal. |
| 25 Oct 2026 | Submission deadline. |

# 15. Final Submission Checklist

☐ 10–15-page report, excluding appendix and references.

☐ Runnable Google Colab notebook or equivalent implementation.

☐ Dataset/preprocessing record and prompt log.

☐ Decoding comparison table.

☐ JSON schema, sample outputs, and validation results.

☐ Tool/function demonstration.

☐ Evaluation table and at least three failure cases.

☐ 8–10-minute presentation.

☐ Individual contribution statements.

☐ Verify all reported scores and conclusions against actual experiment outputs.

# 16. First Action to Take Now

- Open Command Prompt (Win + R → cmd).

- Run these commands one by one and copy the output:

> python --version
> py --list
> code --version
> git --version

- Share the output before installing anything. We will identify what is already installed and avoid duplicate setup.

- Then create the project folder and virtual environment using Section 6.

# 17. Reference Links

**Python:** https://www.python.org/downloads/

**VS Code:** https://code.visualstudio.com/

**Git:** https://git-scm.com/downloads

**Jupyter:** https://jupyter.org/

**PyTorch:** https://pytorch.org/get-started/locally/

**Hugging Face Transformers:** https://huggingface.co/docs/transformers/index

**SAMSum Kaggle:** https://www.kaggle.com/datasets/nileshmalode1/samsum-dataset-text-summarization

**Alternative SAMSum dataset page (not used as this project's download source):** https://huggingface.co/datasets/Samsung/samsum

**Qwen2.5-1.5B-Instruct:** https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct

**Google Colab:** https://colab.research.google.com/

**Planning note:** This document describes the proposed implementation. Verify current package compatibility and actual model performance during setup, and document any changes.
