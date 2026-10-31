---
title: "SAMSum Conversation Summarization"
subtitle: "Assignment 1 | Applied Generative AI | Group 19"
author: "CHAUDHARI GANESH GOVIND; RAMNIWASH KUMAR; SONAL GUPTA; FIRTHOUSE BANU M G"
---

---

## 1. The problem | 0:40

- Decisions and commitments are spread across conversation turns.
- Goal: summarize the main events and extract explicitly agreed actions.
- Output is an assistive draft; a person must verify claims against the source.

---

## 2. Dataset and preparation | 0:50

- SAMSum dialogues with human-written summaries; fields: `id`, `dialogue`, `summary`.
- Processed: train 14,731; validation 818; test 819.
- One blank-dialogue training row excluded and logged; no text normalization or truncation.
- Reported source: Nilesh Malode, Kaggle, version 1 (page last updated 2023-06-23).
- Kaggle license: **Unknown**; dataset is not redistributed.

---

## 3. Generative-model families | 0:55

- Standard conceptual comparison: variational autoencoders (VAE), GANs, autoregressive Transformers.
- Encoder-decoder Transformers provide an additional sequence-to-sequence comparison.
- Empirical models: Qwen2.5-1.5B-Instruct, FLAN-T5-base, DistilBART-CNN.
- Empirical systems represent causal and encoder-decoder architectures, not three distinct families.
- Specific family coverage in CS1 lecture materials has not been independently confirmed.

---

## 4. How generation works | 0:55

- Dialogue + prompt -> tokenizer IDs -> token and position representations.
- Causal self-attention -> next-token scores over the vocabulary.
- Decoder selects a token; append it and repeat until generation stops.
- Greedy, temperature, top-p and top-k affect token selection.
- Fluent output is not proof of factual accuracy.

---

## 5. Prompt and decoding experiments | 1:15

- Four prompts: zero-shot, few-shot, role/context, constraint-based.
- Few-shot scored highest in the small, manually rated three-example comparison.
- Decoding: greedy and three sampling configurations (temperature/top-p or top-k).
- Sampling increased diversity and sometimes introduced unsupported details.
- Findings are exploratory; n=3 is not a general performance estimate.

---

## 6. Model comparison | 1:05

- Qwen2.5-1.5B-Instruct: ROUGE-1 0.221; ROUGE-2 0.072; ROUGE-L 0.159.
- FLAN-T5-base: ROUGE-1 0.514; ROUGE-2 0.248; ROUGE-L 0.429.
- DistilBART-CNN-12-6: ROUGE-1 0.265; ROUGE-2 0.098; ROUGE-L 0.200.

- 50 test-split dialogues; greedy decoding; input formats differed.
- Test subset has already informed model comparison/selection: not an untouched holdout.
- ROUGE measures reference overlap, not factuality or action-item correctness.

---

## 7. Structured output and tool | 1:00

- JSON: summary, key points, decisions, action items (owner/task/optional due).
- Parse and validate; retry invalid output once; flag fallback for review.
- Allowlisted application-level `validate_summary_output` function.
- Schema validation checks structure, not truth.
- A narrow first-person-commitment heuristic raises some omission warnings.

---

## 8. Failure analysis and safeguards | 1:00

- The model omitted Amanda's explicit promise to bring cookies the next day.
- The new heuristic flags this example but does not repair it or guarantee completeness.
- Other runs converted tentative suggestions into decisions or added unsupported details.
- Safeguards: prompt constraints, schema checks, explicit warnings, human review.

---

## 9. Takeaways and remaining actions | 0:45

- End-to-end workflow and experiments run; latest offline test run passed 66 tests.
- The last recorded report render (29 October) was 14 pages total (11-page body); limitations are disclosed.
- Kaggle license: Unknown; dataset is not redistributed.
- Collect each member's short contribution confirmation.
- Rehearse with the one-minute demo; target 9:25 total.
