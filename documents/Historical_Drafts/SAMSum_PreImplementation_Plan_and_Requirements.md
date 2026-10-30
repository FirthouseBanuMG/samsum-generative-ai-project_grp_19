**SAMSum Conversation Summarizer**

*Pre-Implementation Decisions and Answers to Section 4: Major Project Requirements*

PCAM\* ZG516 — Applied Generative AI \| Team of 4 \| Submission deadline: 25 October 2026

# How to use this document

This document settles the design decisions that can be made before implementation and provides draft answers for all 13 Major Project Requirements. It is a planning/report draft, not evidence that experiments have already been run. Add measured outputs, metrics, screenshots only where useful, and references after implementation. Do not present proposed outcomes as experimental results.

# A. Decisions to finalize before coding

- **Project title:** SAMSum-Based Intelligent Conversation Summarization and Action-Item Extraction.

- **Problem scope:** Summarize chat-style conversations and extract key points, explicit decisions, and action items only when supported by the dialogue. SAMSum contains everyday chat-style dialogues, not exclusively formal meetings.

- **Dataset:** Use the uploaded samsum-train.csv, samsum-validation.csv, and samsum-test.csv. Expected columns: id, dialogue, summary.

- **Model:** Start with Qwen/Qwen2.5-1.5B-Instruct as the candidate pretrained causal LLM. Confirm that it loads and generates acceptable output on the laptop. If inference is too slow, run the same experiment code in Google Colab.

- **Development subset:** Use 20–30 dialogues to develop prompts and verify code. Use the validation split to choose prompt/settings. Reserve 50–100 examples from the test split for final evaluation, if time permits; do not tune on those test examples.

- **Main application output:** JSON object with summary, key_points, decisions, and action_items. Each action item has task and assignee; assignee may be null.

- **Tool/function:** A deterministic validate_action_items function that checks required fields and returns validation results. It must be invoked in a demonstrable workflow; do not imply that the model directly performed an external action.

- **Evaluation:** At minimum: ROUGE, important-information coverage, factual consistency, and JSON validity. Also inspect action-item extraction quality where feasible.

- **Deadline plan:** Target an integrated, working implementation by 21 October 2026. Reserve 22–24 October for bug fixes, report polishing, reproducibility checks, and presentation rehearsal.

# B. Answers to the 13 Major Project Requirements

## 1. Problem Definition

Conversations often contain important facts, decisions, and commitments across multiple messages. Reviewing the entire conversation to identify the main points and follow-up tasks can take time.

This project will build a conversation summarization workflow for professionals, project teams, students, and other users who need a concise view of a dialogue. Input is a chat-style conversation; output is a concise summary, key points, explicit decisions, and action items with assignees only when supported by the text.

A generative LLM is appropriate because it can interpret context and produce abstractive summaries instead of relying only on fixed keyword rules. The project will test how prompts and decoding settings influence summary quality and reliability.

## 2. Dataset Understanding

The SAMSum dataset pairs chat-style dialogues with human-written reference summaries. The project uses the Kaggle version supplied by the team: https://www.kaggle.com/datasets/nileshmalode1/samsum-dataset-text-summarization

The uploaded CSV files contain id, dialogue, and summary. The uploaded split sizes are: train 14,732 rows; validation 818 rows; test 819 rows; total 16,369 rows. The training file has one missing dialogue, which should be handled and recorded during preprocessing.

Before experiments, inspect data types, missing values, duplicates, dialogue lengths, summary lengths, and representative examples. Use training data for exploration and few-shot example selection, validation data for prompt/settings development, and the test split only for final evaluation.

## 3. Generative Model Analysis

Autoregressive language models predict the next token from preceding context and can generate summaries from prompts. Encoder–decoder models, such as T5 or BART, encode the input and generate an output sequence, making them common for summarization. For a third family, select a generative-model family actually covered in CS1, such as variational autoencoders or generative adversarial networks, and compare its objective and generation mechanism with language models.

The proposed solution uses a causal LLM because the assignment specifically requires a pretrained Hugging Face causal language model and the task requires coherent natural-language generation. Confirm the third family against course material rather than assuming which families were taught.

## 4. LLM Architecture

Tokenization converts the prompt and dialogue into token IDs. Embeddings map token IDs into vector representations; positional information represents token order. Transformer self-attention models contextual relationships among tokens. The language-model head produces scores for possible next tokens. Autoregressive generation repeatedly selects or samples the next token using the preceding context until a stopping condition is reached.

In this project, the dialogue and prompt form the context, and generated tokens form the summary or JSON response.

## 5. Baseline System

Load a pretrained Hugging Face causal LLM and tokenizer, initially Qwen/Qwen2.5-1.5B-Instruct if hardware testing succeeds. Apply a simple prompt: “Summarize the conversation in a concise paragraph. Use only information supported by the conversation. Do not invent facts.”

Generate and save at least three baseline outputs. Record model name, generation settings, environment, dialogue ID, reference summary, generated summary, and inference time. The baseline is not complete until the code has been executed.

## 6. Prompt Engineering

Compare four prompts on the same dialogue IDs: (a) zero-shot: summarize without examples; (b) few-shot: include a small number of dialogue-summary examples; (c) role/context-based: instruct the model to act as a conversation summarization assistant and identify main points; (d) constraint-based: specify concise output, preserve important facts, do not infer unsupported decisions, and follow the requested schema.

Save the exact prompt text and output for each variant. Compare quality and reliability using the same examples, and explain why each prompt instruction was chosen.

## 7. Decoding Study

Compare greedy decoding with sampling. Greedy decoding selects the highest-scoring next token. Sampling draws from a probability distribution; temperature changes the distribution's sharpness, while top-k or top-p restricts candidate tokens.

Keep prompt and dialogue IDs fixed while changing decoding settings. Record settings and outputs. Compare factual consistency, coverage, readability, and variability. Do not assume that higher temperature or a particular setting is better before measuring.

## 8. Adaptation Decision: Prompting, RAG, and PEFT

Prompting changes instructions/context without changing model weights and is the simplest approach for the required prompt experiments. RAG retrieves external information and adds it to the model context; it is not essential when the dialogue itself is the source of truth. Fine-tuning changes model weights, while PEFT updates a smaller set of parameters or adds trainable components, requiring more setup and compute.

Use prompting as the primary approach because it aligns with the assignment's focus and deadline. Discuss RAG and PEFT as alternatives and justify not implementing them unless the instructor requires otherwise. Actual fine-tuning is optional according to the assignment brief.

## 9. Structured Output

Use a JSON schema with summary (string), key_points (list of strings), decisions (list of strings), and action_items (list of objects containing task and assignee). The assignee may be null if it cannot be identified from the conversation.

Parse the generated text and validate required keys and data types. Record invalid outputs and demonstrate error handling or a retry. Ensure the model does not fabricate decisions, tasks, or assignees.

## 10. Tool / Function Calling

Implement validate_action_items(action_items), a deterministic function that checks whether each action item has a non-empty task and an assignee that is either a supported participant name or null. Return a structured result with valid/invalid status and reasons.

Demonstrate one invocation using model-generated JSON. This is a simulated tool-assisted workflow; it does not assign real tasks or update an external system. Document the input and output schema.

## 11. Programmatic Prompting

Create a reusable prompt-building function with parameters such as dialogue, summary_style (concise/detailed), and output_format (plain text/JSON). The function should return the complete prompt string.

Demonstrate the same function with different parameter values. Pass JSON-mode outputs through validation before calling the action-item function.

## 12. Evaluation

Use at least four criteria: (1) ROUGE to measure overlap with the reference summary; (2) important-information coverage, assessed with a documented checklist or manual rubric; (3) factual consistency, checking unsupported or contradicted claims; and (4) JSON validity, measuring parse/schema success. Action-item extraction quality can be an additional criterion.

Use the same held-out examples for comparisons. Report sample size and the calculation method for every metric. Document at least three actual failure cases, including the dialogue, generated output, expected behavior, failure category, and a proposed mitigation. Candidate categories include omitted information, unsupported claims, incorrect participant attribution, invalid JSON, and missed action items. Only report failures actually observed.

## 13. Responsible Use

Potential risks include hallucinated facts, omission of important details, incorrect attribution of tasks, privacy exposure, and over-reliance on generated summaries. Controls include using only public dataset examples, avoiding confidential or personally identifiable conversations, validating JSON, leaving uncertain assignees unknown, preserving the original dialogue for review, and requiring human review before consequential use.

Document limitations and do not claim perfect factual accuracy.

# C. Proposed JSON schema

{
"summary": "Concise conversation summary",
"key_points": \["Important point supported by the dialogue"\],
"decisions": \[\],
"action_items": \[
{"task": "Action supported by the dialogue", "assignee": null}
\]
}

# D. Required experiments and evidence checklist

- **E1 — Baseline:** One simple prompt and at least 3 generated outputs.

- **E2 — Prompt comparison:** Four prompt variants and a comparison table.

- **E3 — Decoding:** Greedy decoding plus sampling with temperature and at least one of top-k/top-p; include output examples.

- **E4 — Structured output:** Schema, validation code, valid JSON example, and invalid-output handling.

- **E5 — Tool/function:** Function input/output schema and one demonstrated invocation.

- **E6 — Failure analysis:** At least 3 observed failure cases and analysis table.

- **E7 — Final system:** Integrated notebook and 8–10-minute demo.

# E. Four-member division of work

| Member | Owns | Deliverable |
|----|----|----|
| Member 1 | Dataset and baseline | Preprocessing record, model loading, 3 baseline outputs |
| Member 2 | Prompt and decoding experiments | Four prompt variants, decoding table and outputs |
| Member 3 | JSON and tool/function workflow | Schema, validation, reusable template, function invocation |
| Member 4 | Evaluation and report integration | Metrics, failure cases, report consolidation and demo plan |

# F. Timeline and buffer

- **15 Oct —** Confirm model, sample IDs, JSON schema, repository, and task owners.

- **16–17 Oct —** Dataset checks, baseline generation, prompt variants, and decoding tests.

- **18 Oct —** Integrate JSON validation and tool/function invocation; begin evaluation.

- **19–20 Oct —** Complete evaluation, failure analysis, report, and presentation draft.

- **21 Oct —** Internal freeze: execute the full notebook and check every required deliverable.

- **22–24 Oct —** Buffer for fixes, reproducibility, report polish, and rehearsal.

- **25 Oct —** Submission deadline.

# G. Final deliverables from the assignment brief

- Technical report of approximately 10–15 pages, excluding appendices and references.

- Working Google Colab notebook or equivalent executable implementation.

- Dataset description and preprocessing record.

- Prompt experiment log and decoding comparison table.

- Structured-output schema and sample validated outputs.

- Tool/function specification and demonstration.

- Evaluation and failure-analysis table.

- 8–10 minute group demonstration/presentation.

- Individual contribution statement confirmed by every member.

# H. References and verification notes

Assignment brief: PCAM\* ZG516 — Applied Generative AI, Group Major Project / Assignment 1, Sections 4–10.

Dataset: SAMSum Kaggle dataset selected by the team: https://www.kaggle.com/datasets/nileshmalode1/samsum-dataset-text-summarization

Candidate model: Qwen/Qwen2.5-1.5B-Instruct: https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct

Before submission, verify the dataset license/redistribution conditions and the model license. Confirm the third generative-model family against the actual CS1 course materials. Add dates of access and any further sources used.
