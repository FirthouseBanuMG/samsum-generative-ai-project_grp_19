**SAMSum-Based Intelligent Conversation Summarization
and Action-Item Extraction Using Prompt Engineering**

*Major Project Plan — Clear, Technical, and Implementation-Focused*

# 1. Project Overview

- Problem: Conversations contain useful information, but manually finding the main points, decisions, and follow-up tasks takes time.

- Proposed solution: Build a conversation summarization pipeline using a pretrained causal language model (LLM). The system will generate a concise summary and extract key points, decisions, and action items.

- Main question: How do prompt design and decoding settings affect summary quality, factual consistency, and output reliability?

- Scope: Focus on prompting, inference, structured output, validation, and evaluation. Training a large model from scratch is out of scope.

# 2. Dataset and Model Links

**Kaggle SAMSum dataset (selected dataset):** https://www.kaggle.com/datasets/nileshmalode1/samsum-dataset-text-summarization

**Hugging Face SAMSum dataset page (alternative access/reference):** https://huggingface.co/datasets/Samsung/samsum

**Candidate model — Qwen2.5-1.5B-Instruct:** https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct

**Hugging Face Transformers documentation:** https://huggingface.co/docs/transformers/index

- Dataset fields: id, dialogue, summary. The dialogue is the model input; the human-written summary is the reference for evaluation.

- Initial data check: inspect row counts, missing values, duplicates, and sample records. The supplied training CSV has one missing dialogue; exclude or handle that row explicitly and record the decision.

- Split usage: use train data to inspect examples, validation data to select prompts/settings, and a held-out sample of 50–100 test records for final evaluation. Do not tune prompts using the held-out test sample.

- Execution plan: test the small candidate model on the Lenovo laptop first. If inference is too slow or memory use is excessive, run the same notebook in Google Colab.

# 3. Answers to the Major Project Requirements

## 1. Problem Definition

- What we will do: Define the task as converting a chat dialogue into a concise summary plus key points, decisions, and action items.

- How: Specify the input, expected output fields, intended users, and success criteria before coding.

- Why: A clear task definition keeps the project focused and makes the experiments measurable.

## 2. Dataset Understanding

- What we will do: Profile the SAMSum train, validation, and test files and inspect representative conversations.

- How: Use pandas to check shapes, column names, missing values, duplicates, dialogue lengths, and sample summaries.

- Why: Data issues can distort evaluation, and understanding the dialogue style helps us design suitable prompts.

- Output: A short dataset profile and a record of any rows removed or corrected.

## 3. Compare Generative Model Families

- What we will do: Compare at least three generative model families covered in CS1, using the course's terminology.

- How: For each family, describe its generation mechanism, strengths, limitations, and suitability for dialogue summarization.

- Why this model type: A causal/autoregressive LLM generates text token by token and can follow instructions while producing both natural-language summaries and structured output.

- Before finalizing: Confirm which three families were actually covered in CS1; do not add an unstudied family just to reach three.

## 4. Explain the LLM Architecture

- What we will explain: tokenization, token embeddings, positional information, Transformer self-attention, the language-modeling head, and autoregressive generation.

- How: Trace one dialogue through the model: text → tokens → vector representations → Transformer layers → next-token probabilities → generated output.

- Why: This explains how the selected model uses context and generates a summary, rather than treating it as a black box.

## 5. Build the Baseline

- What we will do: Load the pretrained Qwen2.5-1.5B-Instruct model and tokenizer using Hugging Face Transformers.

- How: Apply a simple prompt such as “Summarize this conversation,” run at least three dialogues, and save the input and generated output.

- Why: The baseline gives us a reference point against which prompt and decoding improvements can be compared.

- Record: model ID, software/runtime details, prompt, generation settings, and outputs.

## 6. Compare Prompting Strategies

- What we will test: zero-shot, few-shot, role/context-based, and constraint-based prompts.

- How: Use the same selected dialogues across prompt variants; change the instruction style while keeping other settings as consistent as practical.

- Why: This isolates whether examples, role/context, or explicit output constraints improve completeness and factual accuracy.

- Also compare: concise versus detailed instructions, since the task requires structured summaries and action items.

## 7. Compare Decoding Strategies

- What we will test: greedy decoding versus sampling, plus temperature and at least one of top-k or top-p.

- How: Keep the prompt and test dialogue fixed, change one decoding setting at a time, and record the generated outputs and parameters.

- Why: Decoding controls how the next token is selected; it can change output diversity, repeatability, and the risk of unsupported details.

- Record: do_sample, temperature, top_k/top_p, max_new_tokens, and any other settings used.

## 8. Compare Prompting, RAG, and Fine-Tuning/PEFT

- What we will do: Compare the approaches conceptually and justify the approach used in this project.

- How: Explain that prompting changes instructions, RAG supplies retrieved context, and fine-tuning/PEFT adapts model parameters.

- Why: The comparison shows the trade-off between implementation effort, compute, extra data, and potential task adaptation.

- Scope decision: Use prompting as the main method. Actual fine-tuning is optional unless the instructor approves and time/resources permit it.

## 9. Produce Structured JSON

- What we will do: Ask the model to return JSON with summary, key_points, decisions, and action_items.

- How: Define a schema; each action item contains task and assignee. Use null when the dialogue does not identify an assignee.

- Why: Structured output can be checked by code and reused by downstream applications more reliably than free-form text.

- Validation: Parse the response with Python's json module and validate required fields and data types. Record invalid outputs rather than silently accepting them.

## 10. Implement a Tool/Function

- What we will do: Implement a deterministic Python function that validates extracted action items.

- How: Give it the generated JSON/action-item list; check required keys, task text, and assignee type; return a clear pass/fail result and validation messages.

- Why: This demonstrates how a generative system can use a programmatic tool to check its output.

- Demonstration: Run the function on at least one valid output and one deliberately invalid example. This is a local function demo, not an external API integration.

## 11. Create a Reusable Programmatic Prompt

- What we will do: Store the prompt as a reusable template rather than hard-coding a different prompt for every dialogue.

- How: Use placeholders for the dialogue, summary style (concise/detailed), and required JSON structure.

- Why: A parameterized template makes experiments repeatable and reduces accidental differences between runs.

- Output: A function that accepts a dialogue and settings and returns the assembled prompt.

## 12. Evaluate Quality and Analyze Failures

- What we will do: Evaluate outputs with at least four criteria and report the observed results.

- How: Use ROUGE for reference-summary overlap; manually assess important-information coverage and factual consistency; measure JSON validity; and assess action-item quality.

- Why: No single metric captures all aspects of summarization. Text overlap alone cannot reliably detect invented facts or missing decisions.

- Failure analysis: Document at least three real examples, such as omitted information, unsupported details, incorrect assignee, or invalid JSON. Include the input, output, issue, and likely cause.

## 13. Responsible Use

- What we will do: Identify risks such as hallucinated facts, omitted decisions, incorrect task ownership, and exposure of sensitive conversation content.

- How: Use only the supplied dataset, check outputs against source dialogues, avoid inventing unknown assignees, and require human review for consequential use.

- Why: Summaries can sound convincing while being inaccurate; validation and review reduce, but do not eliminate, this risk.

# 4. Required Experiments and Evidence

| Experiment | What we must show |
|----|----|
| E1 — Baseline | Generate at least three outputs with a simple prompt; save prompt, settings, and output. |
| E2 — Prompt comparison | Compare the four prompt styles on the same examples and summarize differences. |
| E3 — Decoding | Compare greedy and sampling settings; include temperature and top-k or top-p. |
| E4 — JSON validation | Show valid and invalid outputs and the validation result. |
| E5 — Tool/function | Demonstrate the action-item validator with at least one valid and one invalid case. |
| E6 — Failure analysis | Document at least three actual model failure cases and explain the likely cause. |
| E7 — Integrated system | Run the selected prompt, model, JSON validation, action-item validator, and evaluation in one notebook/demo. |

# 5. Proposed Output Schema

**The model should return JSON in this general format:**

> {
> "summary": "Short summary of the conversation",
> "key_points": \["Important point 1", "Important point 2"\],
> "decisions": \["Decision explicitly stated"\],
> "action_items": \[
> {"task": "Follow-up task", "assignee": null}
> \]
> }

- Only include decisions and action items supported by the dialogue. If none are present, return an empty list.

- Use null for an unknown assignee; do not guess who owns a task.

# 6. Team Responsibilities (Suggested)

| Owner | Suggested responsibility |
|----|----|
| Member 1 | Dataset inspection, preprocessing record, and baseline model. |
| Member 2 | Prompt variants and decoding experiments. |
| Member 3 | JSON schema, parser/schema validation, and action-item function. |
| Member 4 | Evaluation, failure analysis, report integration, and presentation. |
| All members | Review final evidence and write an accurate individual contribution statement. |

# 7. Timeline and Final Deliverables

- 15–16 October: confirm requirements, inspect dataset, and get the baseline running.

- 17–18 October: complete prompt and decoding experiments; implement JSON validation and the tool function.

- 19–20 October: evaluate outputs, record failure cases, and integrate the notebook.

- 21 October: freeze results and complete the main report/presentation draft.

- 22–24 October: reserve for fixes, reruns, proofreading, and presentation rehearsal.

- 25 October: submission deadline.

## Final deliverables checklist

- 10–15-page report, excluding appendix and references.

- Runnable Google Colab notebook or equivalent implementation.

- Dataset/preprocessing record and prompt log.

- Decoding comparison table.

- JSON schema, example outputs, and validation evidence.

- Tool/function demonstration.

- Evaluation table and at least three failure cases.

- 8–10-minute presentation and individual contribution statements.

# Important Notes

- This document describes the planned method, not completed results. Add measured scores and actual examples only after running the experiments.

- Before writing Requirement 3, confirm the exact three generative model families covered in CS1.

- Check the course's approval process for the dataset and register SAMSum with the instructor if required.
