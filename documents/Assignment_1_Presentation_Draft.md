# Assignment 1 Presentation Draft — 8–10 minutes

**Project:** SAMSum-Based Intelligent Conversation Summarization and Action-Item Extraction  
**Group 19:** CHAUDHARI GANESH GOVIND; RAMNIWASH KUMAR; SONAL GUPTA; FIRTHOUSE BANU M G  
**Status:** Speaking notes and proposed speaker handoffs, reviewed 31 October 2026. The 10-slide PowerPoint is generated from `Assignment_1_Presentation_Slides.md`. The proposed slide timing is 8:25; a one-minute live or saved-output demo brings the total to about 9:25. The team still needs to confirm speakers and rehearse.

## Slide 1 — The problem (0:40)

**On slide**
- Conversations contain decisions and commitments spread across turns.
- We built a summarization and action-item extraction prototype using SAMSum.
- Output: concise summary + structured action items.

**Speaker note:** Introduce the need for a concise digest and emphasize that generated output remains a draft for human review.

## Slide 2 — Dataset and task (0:50)

**On slide**
- SAMSum dialogues paired with reference summaries.
- Train: 14,731 processed; validation: 818; test: 819.
- One blank-dialogue training row excluded and logged.
- Reported source: Kaggle SAMSum dataset, version 1; Kaggle lists license as Unknown.

**Speaker note:** Describe fields (`id`, `dialogue`, `summary`) and preprocessing. Cite Nilesh Malode's Kaggle dataset page and the underlying SAMSum paper. Clearly state that Kaggle lists the license as Unknown; do not claim redistribution rights or redistribute the dataset files.

## Slide 3 — Generative-model choices (0:55)

**On slide**
- Conceptual landscape: VAE, GAN, autoregressive Transformer.
- Empirical systems: Qwen2.5-1.5B-Instruct, FLAN-T5-base, DistilBART-CNN.
- Qwen is causal; FLAN-T5 and DistilBART are encoder-decoder systems.
- Selected standard comparison families; the exact families in CS1 lecture materials were not supplied.

**Speaker note:** Explain why next-token generation is suitable for flexible text and structured output. The conceptual comparison uses standard VAE, GAN, and autoregressive Transformer families; the empirical systems represent only causal and encoder-decoder architectures. Do not claim that each family was explicitly covered in a lecture.

## Slide 4 — How the LLM generates a summary (0:55)

**On slide**
- Dialogue/prompt → tokenizer IDs → embeddings + position
- Causal Transformer self-attention → vocabulary logits
- Greedy or sampling decoder → next token → repeat

**Speaker note:** Explain causal masking and the language-model head in a few sentences. Remind the audience that fluency does not guarantee faithfulness.

## Slide 5 — Prompt and decoding experiments (1:15)

**On slide**
- Four prompts: zero-shot, few-shot, role-based, constraint-based.
- Few-shot had highest average ratings on three pilot examples.
- Greedy vs temperature/top-p and temperature/top-k sampling.

**Speaker note:** State the four human rubric dimensions and the small n. Explain that sampling increased diversity but could introduce unsupported details.

## Slide 6 — Model comparison (1:05)

**On slide**

| Model | ROUGE-1 | ROUGE-2 | ROUGE-L |
|---|---:|---:|---:|
| Qwen2.5-1.5B-Instruct | 0.221 | 0.072 | 0.159 |
| FLAN-T5-base | 0.514 | 0.248 | 0.429 |
| DistilBART-CNN-12-6 | 0.265 | 0.098 | 0.200 |

- 50 test dialogues; greedy decoding.
- Comparative evidence only; not an untouched final holdout.
- Input formats differ; ROUGE is not factuality.

**Speaker note:** Report observed values without claiming a controlled architecture-only comparison. State that 50 examples from the test split were used to compare/select models, so the subset is no longer an independent final holdout; do not imply otherwise.

## Slide 7 — Structured output and tool function (1:00)

**On slide**
- JSON schema: summary + action items (owner/task/optional due).
- Parse, validate, retry once, flag fallback for review.
- Narrow explicit-commitment omission warning; human review still required.
- Allowlisted `validate_summary_output` application-level tool.

**Speaker note:** Clarify that schema validation checks format, not meaning. The heuristic catches only a narrow class of first-person commitment omissions: on the cookies example the model still omits Amanda's commitment, and the warning surfaces it rather than repairing the output. The function-call protocol is application-level JSON, not native tool-call parsing.

## Slide 8 — Failures and safeguards (1:00)

**On slide**
- Tentative intentions became firm commitments.
- Unsupported action items passed schema validation.
- Sampling sometimes added plausible but false details.
- The integrated cookies example omitted Amanda's explicit delivery commitment.
- Controls: prompt constraints, schema validation, a narrow coverage warning, and human review.

**Speaker note:** Walk through one example and explain why a person must compare claims with the source conversation. Mention privacy and consent for any future private-data use.

## Slide 9 — Conclusion and limitations (0:45)

**On slide**
- Core workflow and experiments are implemented.
- Strong reference overlap did not prove factual correctness.
- Small prompt sample, CPU timings, and test-split caveat limit conclusions.
- Remaining: member contribution confirmations, presentation rehearsal, and course submission.

**Speaker note:** Close with the main learning: reliable GenAI needs evaluation and controls, not only a prompt and a fluent model.

## Proposed speaker handoffs and demonstration

| Presenter | Slides / segment | Approximate speaking time |
|---|---|---:|
| CHAUDHARI GANESH GOVIND | Slides 1–2 and 9 | 2:15 |
| RAMNIWASH KUMAR | Slides 3–4 and 6; integrated demo | 3:55 |
| FIRTHOUSE BANU M G | Slide 5 | 1:15 |
| SONAL GUPTA | Slides 7–8 | 2:00 |
| **Total** | **Slides plus one-minute demo** | **9:25** |

The proposed distribution is only a starting point; confirm each speaker with the team. For the one-minute demo, show the processed dialogue input, the generated structured output, the schema/tool result, and the visible completeness warning. The saved cookies example is a clear demonstration: the model omits Amanda's commitment, and the heuristic flags it without repairing it. Keep `outputs/integrated_demo/demo_result.json` ready as a fallback if live generation is slow or fails. Avoid a code walkthrough.

## Rehearsal and team confirmation

- Slide allocations total approximately 8 minutes 25 seconds; with the planned demo, target approximately 9 minutes 25 seconds.
- The speaker allocation is proposed and has not been confirmed by the team.
- Timing is an estimate, not a completed timed rehearsal.
- Rehearse with the integrated notebook open and ensure all members can explain the complete workflow and limitations.
