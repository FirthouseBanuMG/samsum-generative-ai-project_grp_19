**SAMSum-Based Intelligent Conversation Summarization
and Action-Item Extraction**

*Major Project Requirements — Plain and Crisp Draft*

# A. Key Decisions Before Implementation

> **Dataset:** Use the SAMSum train, validation, and test CSV files. Each contains an ID, dialogue, and reference summary.
>
> **Data check:** Check missing values and duplicate records before running experiments. One training dialogue is missing, so handle it explicitly.
>
> **Model:** Start with Qwen2.5-1.5B-Instruct through Hugging Face. Test it locally first; use Google Colab if local inference is too slow.
>
> **Data split:** Use train data for inspection, validation data for prompt selection, and a small held-out test sample for final evaluation. Do not tune prompts on the test sample.
>
> **Output:** Return valid JSON containing a summary, key points, decisions, and action items. Use null when an assignee is not stated.
>
> **Evaluation:** Check summary quality, factual consistency, important-information coverage, JSON validity, and action-item quality.
>
> **Target dates:** Aim to finish the implementation and freeze results by 21 October 2026. Keep 22–24 October for final checks before the 25 October deadline.

# B. Answers to the 13 Major Project Requirements

## 1. Problem Definition

- Build a system that summarizes conversations and extracts key points, decisions, and action items.

- The input is a conversation; the output is a concise, structured summary.

- The goal is to reduce manual effort while preserving important information.

## 2. Dataset Understanding

- Use the SAMSum dataset, which contains short, chat-style conversations and human-written summaries.

- Inspect the train, validation, and test splits; check missing values and duplicates.

- Use the dataset's reference summaries to compare generated summaries.

## 3. Compare Generative Model Families

- Compare at least three generative model families taught in CS1.

- For each family, briefly state how it generates text, its strengths, and its limitations.

- Explain why an autoregressive causal language model is suitable for generating summaries and structured outputs.

- Confirm the three families against the actual CS1 course material before finalizing this section.

## 4. LLM Architecture

- Tokenization converts the conversation into tokens.

- Embeddings represent tokens as vectors.

- Transformer attention helps the model relate different parts of the conversation.

- The language-modeling head predicts the next token; autoregressive generation repeats this process to create the output.

## 5. Baseline Model

- Load a pretrained causal language model from Hugging Face.

- Use a simple instruction asking it to summarize a conversation.

- Run at least three conversations and save the input, prompt, and output.

- Treat these as baseline examples, not proof of overall performance.

## 6. Prompt Engineering Comparison

- Test zero-shot prompting, few-shot prompting, role/context prompting, and constraint-based prompting.

- Keep the test conversation the same when comparing prompt styles.

- Compare clarity, completeness, factual accuracy, and output consistency.

- Also compare concise and detailed instructions.

## 7. Decoding Strategies

- Compare greedy decoding with sampling.

- Test temperature and at least one of top-k or top-p.

- Record settings and outputs so differences can be reviewed.

- Explain how each setting affects variation and reliability.

## 8. Prompting, RAG, and Fine-Tuning

- Explain prompting as giving instructions and examples to a pretrained model.

- Explain RAG as retrieving relevant information and providing it to the model.

- Explain fine-tuning/PEFT as adapting model weights for a task.

- Compare their data, compute, complexity, and expected benefits. Actual fine-tuning is optional unless approved.

## 9. Structured Output

- Require the model to return JSON with summary, key_points, decisions, and action_items.

- Each action item should include task and assignee; use null when the assignee is unknown.

- Validate the output with a JSON parser and a defined schema.

- If validation fails, record the error or try a controlled repair.

## 10. Tool or Function

- Create a small function that validates extracted action items.

- Define its input and output clearly.

- Demonstrate it on a model-generated JSON example.

- Report whether the function accepts the output or identifies errors.

## 11. Reusable Programmatic Prompt

- Create a prompt template with placeholders for the conversation and output style.

- Allow settings such as concise/detailed summary to be changed without rewriting the prompt.

- Run the same template on multiple conversations.

## 12. Evaluation and Failure Analysis

- Use at least four evaluation criteria.

- Suggested criteria: ROUGE, important-information coverage, factual consistency, JSON validity, and action-item quality.

- Record results in a table and explain the main patterns.

- Show at least three failure cases, such as missing details, invented information, or incorrect action-item assignments.

## 13. Responsible Use

- Do not include confidential or unnecessary personal information.

- Check summaries against the original conversation before relying on them.

- Flag uncertainty and avoid inventing decisions, tasks, or assignees.

- Explain that model outputs can be incorrect and require human review.

# C. Required Experiments

- E1 — Baseline: generate and save at least three outputs.

- E2 — Prompt comparison: test the four prompt styles and compare results.

- E3 — Decoding: compare greedy and sampling settings.

- E4 — Structured output: generate JSON and validate it.

- E5 — Tool/function: demonstrate the action-item validation function.

- E6 — Failure analysis: document at least three failure cases.

- E7 — Integrated system: combine the chosen prompt, model, output validation, and evaluation in a runnable notebook or demo.

# D. Suggested Team Responsibilities

- Member 1: dataset checks and baseline model.

- Member 2: prompt engineering and decoding experiments.

- Member 3: JSON schema, validation, and tool/function demo.

- Member 4: evaluation, failure analysis, report, and presentation integration.

- All members: review the final results and add an accurate individual contribution statement.

# E. Final Deliverables Checklist

- Report of 10–15 pages, excluding appendix and references.

- Executable Google Colab notebook or equivalent runnable implementation.

- Dataset and preprocessing record.

- Prompt log and decoding comparison table.

- JSON schema, sample outputs, and validation results.

- Tool/function demonstration.

- Evaluation table and failure-analysis examples.

- Presentation of 8–10 minutes.

- Individual contribution statements.

# Important Note

This is a concise planning draft. Update it with actual model outputs, measurements, and observed failures after running the experiments. Do not report planned results as completed results.
