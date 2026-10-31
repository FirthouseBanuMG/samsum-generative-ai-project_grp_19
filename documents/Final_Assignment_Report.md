# SAMSum-Based Intelligent Conversation Summarization and Action-Item Extraction

**PCAM* ZG516 – Applied Generative AI**  
**Group 19:** CHAUDHARI GANESH GOVIND; RAMNIWASH KUMAR; SONAL GUPTA; FIRTHOUSE BANU M G  
**Assignment 1 – Technical Report**

> Evidence note: The implementation, data-check results, and offline test status were rechecked on 31 October 2026; saved model outputs were not regenerated during that review. The report's last recorded render was on 29 October 2026. The reported Kaggle page is cited as the source; it lists the license as Unknown. Do not redistribute dataset files based on this citation. Exact archive provenance is not established. Results below are reported as observed; no unrun experiment is claimed.

## Abstract

This project studies how pretrained generative models can summarize short conversations and extract explicitly agreed action items. The system uses the SAMSum dialogue dataset, a pretrained Qwen2.5-1.5B-Instruct causal language model, reusable prompts, controlled decoding, JSON Schema validation, and an allowlisted validation function. Supporting comparisons include FLAN-T5-base and DistilBART-CNN, four prompt styles, and four decoding configurations. The saved experiments show that prompt structure and sampling affect the generated text, while the model-family comparison reports higher ROUGE scores for FLAN-T5-base on the selected 50 test dialogues. These metrics measure reference overlap, not factual correctness. Qualitative review found unsupported commitments and details, including action items that were structurally valid but not actually agreed in the source dialogue. Accordingly, the application treats generated content as a draft requiring human review. The work demonstrates a functioning set of project components, while the report identifies limitations in sample size, model comparability, held-out evaluation, and final presentation packaging.

## 1. Problem Definition and Motivation

### 1.1 User problem

People reviewing chat conversations may need a concise account of what happened, what was decided, and who explicitly agreed to do something. Manually scanning longer conversations is time-consuming, while a generic summary may omit decisions or incorrectly turn tentative suggestions into commitments.

### 1.2 Application

The application accepts a dialogue and returns:

- a concise natural-language summary;
- an `action_items` array with an owner, task, and optional due date; and
- a validation result indicating whether the output conforms to the expected JSON structure.

The intended user is someone who needs a quick, reviewable digest of a conversation. This is an assistive workflow, not an authoritative record. A human must verify the generated claims against the source dialogue before acting on them.

### 1.3 Why use a generative model?

Conversation summarization requires integrating information across turns, resolving references, and expressing salient facts in new language. A pretrained language model can generate such a concise paraphrase from dialogue context. However, fluency is not evidence of factual support. The system therefore adds explicit prompt constraints, output validation, and human-review guidance.

## 2. Dataset and Preparation

### 2.1 Dataset

The project uses SAMSum, a collection of messenger-style dialogues paired with human-written summaries [1, 2]. The data used in the repository has `id`, `dialogue`, and `summary` fields. The locally audited splits contain 14,732 training rows, 818 validation rows, and 819 test rows. Preprocessing preserves text without truncation or text normalization and excludes one training row with a missing or blank dialogue.

| Split | Raw rows | Processed rows | Observed project use |
|---|---:|---:|---|
| Train | 14,732 | 14,731 | Smoke tests and pipeline development |
| Validation | 818 | 818 | Development comparisons |
| Test | 819 | 819 | Used for a 50-sample model-family comparison; not an untouched holdout |

Validation and preprocessing scripts, processed CSVs, exclusion records, and metadata are present in the repository. The audit reports no shared IDs or exact dialogue-summary pairs between splits; it does not rule out semantic near-duplicates.

### 2.2 Sample selection and split use

The initial baseline uses three deliberately selected training examples: a simple request/agreement, advice with tentative action, and a longer multi-speaker discussion. These examples test basic workflow behavior and are not a representative sample for estimating general performance.

The model-family comparison uses 50 unique test-split dialogues selected with seed 42, excluding three pilot IDs. Its outputs are retained with a sample manifest. The test data has therefore been consumed for comparative evidence; report these results as exploratory model-comparison/selection evidence, not as an independent final holdout. Do not continue tuning prompts or configurations against this subset.

### 2.3 Data provenance

The local processed artifacts were inspected directly. They are named `samsum-train-processed.csv`, `samsum-validation-processed.csv`, and `samsum-test-processed.csv`; the companion `preprocessing_metadata.json` records the source filenames, expected columns, row counts, no text transformation/truncation, and one excluded training row. The three processed files were independently validated again on 31 October 2026: all have the columns `id`, `dialogue`, and `summary`; row counts are 14,731, 818, and 819; IDs are unique; and required text fields passed validation. The split audit found no shared IDs or exact dialogue-summary pairs.

The team reports obtaining the files from the Kaggle dataset [“Samsum Dataset Text summarization” by Nilesh Malode](https://www.kaggle.com/datasets/nileshmalode1/samsum-dataset-text-summarization) [2]. The Kaggle page metadata identifies version 1 (page last modified 23 June 2023) and lists the license as **Unknown**. This records the reported download page, but the local processed files do not establish which exact Kaggle archive produced the CSVs, the download date, or the upstream SAMSum release/version. The Kaggle page identifies Nilesh Malode as the uploader/creator of that page; the underlying corpus is attributed to the SAMSum paper cited in References. For this assignment, report the Kaggle information as listed and do not redistribute dataset files. Local SHA-256 values provide fingerprints only relative to the recorded local baseline, not upstream authenticity.

## 3. Generative-Model Families and Model Choice

The assignment asks for a comparison of at least three generative-model families and a justification for using a causal language model. The conceptual comparison below covers variational autoencoders, generative adversarial networks, and autoregressive Transformers, with encoder-decoder Transformers included for comparison. The project’s empirical experiment compares three pretrained systems, but those systems represent only two broad neural text-generation architectures: Qwen is a causal/autoregressive language model; FLAN-T5 and DistilBART are encoder-decoder sequence-to-sequence models. The empirical comparison should therefore not be presented as three distinct architecture families.

| Family | Basic idea | Strength for this task | Limitation for this task |
|---|---|---|---|
| Variational autoencoder (VAE) [6] | Encodes data into a latent distribution and decodes samples from that representation | Useful for learning compact latent representations and generating diverse samples | A generic VAE is not naturally instruction-following and requires task-specific conditioning/training to produce faithful dialogue summaries |
| Generative adversarial network (GAN) [7] | A generator produces samples while a discriminator distinguishes generated from real samples | Effective for some continuous or perceptual generation tasks | Discrete token sequences and controllable, faithful multi-turn summarization are difficult to optimize with the standard adversarial objective |
| Autoregressive Transformer / causal LM [8] | Predicts the next token conditioned on preceding tokens; generation proceeds token by token | Naturally supports text continuation, instruction prompts, and structured text generation | May hallucinate, is sensitive to prompt/decoding choices, and can be slow on CPU |
| Encoder-decoder Transformer [9] | Encodes the input sequence and generates an output sequence conditioned on its representation | Direct sequence-to-sequence formulation suits summarization | Output quality and instruction-following behavior depend on model training and input format; not the causal-LM baseline specified by the assignment |

The Qwen causal LM is suitable for the required baseline because it is pretrained, instruction-tuned, supports autoregressive text output, and can be guided by reusable task prompts [3]. It is not assumed to be the best-performing model for this dataset. The empirical comparison below found stronger ROUGE overlap from FLAN-T5-base on the selected sample [4]. The conceptual family comparison and empirical model comparison answer different questions and should remain clearly distinguished. The team selected the standard VAE, GAN, and autoregressive Transformer families for the conceptual comparison, with encoder-decoder Transformers for contrast. The specific lecture coverage of each family was not independently verified, so the report does not claim that each was explicitly taught.

## 4. LLM Architecture and Generation

### 4.1 Tokenization and embeddings

The input dialogue and prompt are converted by the model tokenizer into token IDs. Tokens may be whole words, word fragments, punctuation, or special control tokens. The model maps each token ID to a learned embedding vector. Token and position information together give the model a representation of both content and order. The project uses the Qwen tokenizer’s chat template to serialize system and user messages consistently.

### 4.2 Transformer and self-attention

Transformer layers repeatedly update token representations using self-attention and feed-forward transformations. Attention lets a token’s representation incorporate relevant information from other positions. In a causal language model, a causal mask prevents a position from attending to future tokens, preserving the left-to-right prediction setup. This mechanism allows generated text to condition on earlier dialogue and generated tokens.

### 4.3 Language-model head and autoregressive decoding

At each generation step, the language-model head maps the final hidden state to scores over the vocabulary. A softmax distribution represents the next-token probabilities. The decoder selects a token according to the decoding strategy, appends it to the context, and repeats until a stopping token or output limit is reached. Greedy decoding chooses the highest-scoring token at each step. Sampling draws from a probability distribution modified by settings such as temperature, top-p, or top-k.

In this project the flow is: dialogue plus prompt → tokenizer/chat template → pretrained model → next-token generation → decoded text → JSON extraction and schema validation. JSON Schema checks the output’s form, not whether its claims are supported by the dialogue.

## 5. Application Architecture and Baseline

The workflow has five main stages:

1. Validate and preprocess the SAMSum data.
2. Build a reusable prompt using one of four prompt strategies.
3. Generate text using a pretrained model with selected decoding settings.
4. Parse/validate structured output and, when demonstrating the callable tool, execute only the allowlisted validation function.
5. Review the content against the dialogue and record evaluation results and failures.

The baseline uses `Qwen/Qwen2.5-1.5B-Instruct` on CPU, greedy decoding, and a maximum of 100 new tokens. It produced three retained outputs from the training split. The first example broadly captured Amanda’s offer to bring cookies to Jerry. The other examples include unsupported details: the model turns tentative suggestions into commitments in the procrastination dialogue and overstates Sam’s decision in the roommate discussion. This baseline verifies that the pipeline runs; three examples do not establish an accuracy estimate.

## 6. Prompt-Engineering Experiments

Four prompt variants were implemented and run on the same three baseline dialogues: zero-shot, few-shot, role/context-based, and constraint-based. The comparison uses a fixed model and greedy decoding. The human rubric scores relevance, coverage, factual consistency, and output reliability on a 1–5 scale.

| Prompt strategy | n | Relevance | Coverage | Factual consistency | Output reliability |
|---|---:|---:|---:|---:|---:|
| Zero-shot | 3 | 4.67 | 4.00 | 3.33 | 3.33 |
| Few-shot | 3 | 5.00 | 4.33 | 3.67 | 3.67 |
| Role-based | 3 | 4.67 | 4.00 | 3.33 | 3.33 |
| Constraint-based | 3 | 4.67 | 4.00 | 3.33 | 4.00 |

Few-shot prompting had the highest average scores in this small comparison; constraint-based prompting had the same relevance/coverage/factual-consistency scores as zero-shot and role-based, with higher output reliability. Because the sample is only three dialogues and the rubric is manually scored, these results are exploratory and do not establish a general prompt ranking. Reported generation times are from CPU runs and vary substantially; they are not treated as a stable benchmark.

### 6.1 Concise versus detailed summaries

A separate controlled comparison used the same three training-split baseline dialogues, the same Qwen model, the same system message, greedy decoding, and a 100-token generation limit. Only the requested length/detail instruction changed: concise asked for one sentence; detailed asked for 3–5 sentences. Both prompt styles shared the same factuality and uncertainty instructions.

| Style | n | Average words | Average sentences | Average ROUGE-1 F1 | Average ROUGE-L F1 |
|---|---:|---:|---:|---:|---:|
| Concise | 3 | 15.667 | 1.000 | 0.460 | 0.411 |
| Detailed | 3 | 42.333 | 3.333 | 0.294 | 0.275 |

The detailed prompt produced longer outputs, as intended. On these three examples, concise summaries had higher average lexical overlap with the SAMSum references. This small result does not establish that concise summaries are generally more accurate or useful. Manual inspection found unsupported decisions in both conditions: for example, both styles incorrectly state that Sam decides to speak with Rick. Full generated text, prompt versions, and per-example metrics are saved in `outputs/summary_detail_comparison/`; the comparison runner is `src/prompting/run_summary_detail_comparison.py`.

## 7. Decoding Experiments

The decoding experiment holds the constraint-based prompt, model, dialogue, and maximum output length fixed while varying generation configuration. Greedy decoding is compared with sampling at temperature 0.3 and top-p 0.9, sampling at temperature 1.0 and top-p 0.9, and sampling at temperature 0.8 and top-k 50. Sampling uses three recorded seeds per example. The retained variability summary reports distinct outputs and mean pairwise Jaccard word overlap. Greedy produces one deterministic output per input, while the sampling configurations produce multiple outputs with lower overlap, demonstrating increased diversity.

The experiment also illustrates a quality trade-off: higher variability can produce unsupported or distorted details. For example, one sampled cookies summary incorrectly says cookies were shared at dinner and that more would be brought the next day. Sampling diversity is not itself an improvement in factual quality.

## 8. Adaptation Strategy: Prompting, RAG, Fine-Tuning, and PEFT

| Strategy | What changes | Potential benefit | Cost/limitation for SAMSum here |
|---|---|---|---|
| Prompting | Instructions, examples, and constraints in the input | Fast to iterate; no weight updates; directly supports task/format instructions | Sensitive to prompt wording; does not guarantee factuality |
| Retrieval-augmented generation (RAG) | Retrieves external passages and includes them in model context | Useful when answers depend on a changing or external knowledge base | SAMSum summarization is grounded in the dialogue already supplied; external retrieval may add irrelevant or misleading context |
| Full fine-tuning | Updates many or all model parameters on task examples | Can adapt model behavior to a domain/task with sufficient representative data and compute | More compute/data and risk of overfitting; not necessary to demonstrate the core assignment workflow |
| PEFT (e.g., adapters/LoRA) | Updates a small set of added or selected parameters | Lower training/storage cost than full fine-tuning while adapting behavior | Still requires training data, setup, evaluation, and compute; can overfit and does not guarantee factuality |

Prompting is the most appropriate primary strategy for this project: the task is well-specified by the input dialogue, the group can compare prompt changes directly, and available compute is CPU-only. RAG is not needed for the core summarization input. Fine-tuning/PEFT remain possible future work, not a requirement for this assignment, and should only be attempted with a separate leakage-safe evaluation design.

## 9. Structured Output and Tool/Function Calling

The structured output contract has four required top-level fields: `summary` (string), `key_points` (list of strings), `decisions` (list of strings), and `action_items` (list of objects). Each action item contains a non-empty `owner` and `task`; `due` is optional and may be a string or `null`. Empty lists represent no identified key points, decisions, or agreed actions. The prompt instructs the model to distinguish suggestions and tentative intentions from decisions. The schema rejects missing required fields, incorrect types, and additional properties. The implementation extracts JSON, parses it, validates it, retries once when necessary, and flags a fallback for human review if repair fails.

After expanding the schema, the structured-output experiment was rerun on the same three training examples. All three responses parsed and passed schema validation on the first attempt. This is format-compliance evidence only: the model returned empty `action_items` for all three examples, including dialogues with an explicitly stated future action, and it incorrectly stated that Sam decided to speak to Rick in one response. Required fields therefore do not guarantee complete or factually supported content.

The callable function `validate_summary_output` validates a proposed output object. The model emits an application-level JSON request; the application checks the tool name and exact argument shape, then calls the allowlisted Python function. Tests cover a valid request, schema-invalid data, unknown tool names, unexpected arguments, and malformed JSON. This is an application-level tool protocol, not native model-specific tool-call parsing. In the integrated demonstration, a valid tool result is returned to the model to produce the final response; invalid tool validation blocks that follow-up.

The saved tool example is an important failure case: the model proposes “Prepare cookies” for Amanda and “Eat cookies” for Jerry even though the dialogue only says Amanda will bring cookies and Jerry accepts them. The schema accepts the output because its structure is valid. Structural validation must therefore be paired with semantic review.

## 10. Evaluation Results

### 10.1 Model comparison

Three pretrained systems were compared on the same 50 test dialogues with greedy decoding and a maximum of 100 new tokens [3–5]. Qwen and FLAN-T5 receive a constraint-based prompt; DistilBART receives dialogue-only input. Because input formats differ, the experiment compares tested model configurations rather than isolating architecture alone.

| Model | ROUGE-1 F1 | ROUGE-2 F1 | ROUGE-L F1 | Mean seconds/sample |
|---|---:|---:|---:|---:|
| Qwen2.5-1.5B-Instruct | 0.2205 | 0.0724 | 0.1586 | 21.69 |
| FLAN-T5-base | 0.5140 | 0.2482 | 0.4291 | 0.64 |
| DistilBART-CNN-12-6 | 0.2655 | 0.0981 | 0.1997 | 1.38 |

FLAN-T5-base had the highest lexical-overlap scores and lowest mean runtime in this run. ROUGE [10] measures overlap with reference summaries; it does not independently measure factual support, action-item correctness, or human usefulness. Timing is hardware/runtime-specific.

### 10.2 Evaluation criteria and interpretation

The prompt comparison’s four human criteria are relevance, coverage, factual consistency, and output reliability. The model comparison additionally reports ROUGE-1/2/L F1 and generation time. These evidence types are complementary: rubric review examines task-oriented aspects on three examples, whereas ROUGE provides a reference-overlap measure on 50 samples. Neither alone is a complete factuality evaluation.

### 10.3 Evaluation limitations

- Prompt scoring uses only three examples per strategy.
- The model comparison uses 50 examples from the test split and differing input formats.
- The project has no large-scale human factuality annotation.
- ROUGE does not measure hallucinations or whether an action item was explicitly agreed.
- The selected 50-example result must be described with the experiment’s test-split usage and selection protocol; do not claim a pristine holdout if any tuning or selection used those results.
- CPU timings are specific to the recorded machine and software versions.

## 11. Failure Analysis

| Case | Observed failure | Why it matters | Practical mitigation |
|---|---|---|---|
| Baseline sample `13681000` | Generated content overstates Kim’s tentative intentions and adds details not supported by the dialogue (including a firm commitment/post-it plan). | Suggestions and tentative intentions can be converted into facts or commitments. | Use explicit uncertainty/commitment constraints; review generated claims against the dialogue; include a faithfulness rubric. |
| Baseline sample `13728094` | Summary says Sam decides against confrontation and plans to address the situation later, stronger than the dialogue’s uncertainty. | A summary can alter a speaker’s decision even while preserving the general topic. | Preserve uncertainty and speaker attribution; compare each decision claim with its source turn. |
| Structured-output sample `13728094` | The expanded JSON output states that Sam decides to discuss the matter with Rick, although the dialogue says Sam is unsure and may let it go; it also leaves `action_items` empty. | Adding explicit `decisions` and `action_items` fields does not prevent unsupported decisions or omissions. | Require human review of both positive and empty fields; score decision accuracy and action-item recall separately. |
| Tool demo sample `13818513` | JSON-valid action items claim Amanda will “Prepare cookies” and Jerry will “Eat cookies,” neither of which is an explicit agreed action. | Schema validation can pass a semantically unsupported result. | Keep human review mandatory; validate factual support separately; avoid treating inferred next steps as commitments. |
| Sampling example `13818513` | One high-temperature sample adds dinner and a promise to bring more cookies, unsupported by the conversation. | Diverse decoding can add plausible but fabricated details. | Use deterministic decoding where consistency matters; compare sampled outputs and flag unsupported claims. |
| Integrated demo sample `13818513` | The model still produces “Amanda baked cookies for Jerry” with an empty action list, omitting the explicit delivery commitment, while passing schema validation. A narrow first-person-commitment heuristic now flags this omission and adds a review warning; it does not repair or prove completeness. | Schema validity does not detect omissions; the heuristic only recognizes a limited pattern and can miss other forms. | Keep human review mandatory; inspect the coverage warning, and evaluate completeness separately from JSON validity. |

These are concrete examples, not estimates of failure frequency. The application should not be used to create authoritative records without human verification.

## 12. Responsible Use and Reliability

**Hallucination and attribution:** The model may invent facts, deadlines, commitments, or speaker intentions. Use concise prompts that distinguish suggestions from decisions, validate output structure, and require human review of content.

**Privacy:** The experiments use a public research dataset. For real deployments, obtain authorization before processing private conversations, minimize retained text, restrict access, and avoid sending sensitive content to services without an approved data-handling agreement.

**Data leakage:** Keep train, validation, and test roles distinct. The model-family comparison uses a test subset; document its role and do not tune on it while claiming an untouched final evaluation. Do not include private conversation data in prompts or few-shot examples without consent.

**Misuse and over-reliance:** Generated summaries may be mistaken for verbatim records or used to assign tasks that participants did not accept. Mark outputs as AI-generated drafts, preserve source-dialogue traceability where practical, and require a person to confirm action items.

**Reliability controls:** Reject malformed or schema-invalid outputs; allowlist tool names and validate arguments; log raw outputs and recovery events; do not treat successful JSON validation as proof of truth; and surface fallback/review status.

## 13. Implementation and Reproducibility

The repository includes preprocessing and validation scripts, reusable prompt functions, experiment runners for baseline/prompt/decoding/model comparisons, structured-output helpers, tool-call code, tests, and saved outputs. The pinned dependency file is `requirements-lock.txt`; raw and processed dataset files are intentionally not tracked. Reproduce the environment and acquire the dataset according to [the dataset and reproducibility guide](./Implementation_and_Experiments/05_Dataset_Acquisition_and_Reproducibility.md).

The integrated demonstration is available in [`notebooks/01_integrated_demo.ipynb`](../notebooks/01_integrated_demo.ipynb) and can also be run as `python -m integrated_demo.run_integrated_demo`. The workflow returns the tool result to the model for a final user-facing response. Both the CLI and notebook were rerun on CPU using sample `13818513` and the project environment; the evidence is saved under `outputs/integrated_demo/`. The model continued to omit the explicit delivery commitment despite the stronger prompt. The narrow heuristic in `src/structured_output/coverage.py`, called by the structured-generation runner, catches this sample's omission and adds a visible review warning, but does not correct the generated content or establish general factual completeness. A real run may require internet access to download model files and can take several minutes on CPU. Run the existing tests from the project root using the configured environment before submission.

## 14. Limitations and Future Work

This project uses a small instruction-tuned causal LM as its required baseline, not a model trained specifically for the task. Prompt ratings are based on three examples; the comparison of models has 50 samples and differing input formats; and the observed failures are qualitative. ROUGE is a proxy for lexical similarity, not factual correctness. The tool demonstration validates schema compliance but does not ground claims. The current tool protocol is application-level JSON rather than native tool calling.

Future work could use a larger validation-only prompt study, blinded human annotation for factual consistency and action-item support, consistent input formats across model families, and an evaluation split that remains untouched until all development choices are frozen. A PEFT experiment could be added only if data and compute support it and the resulting model is evaluated without leakage.

## 15. Conclusion

The project implements the central workflow required for a small generative-AI summarization application: dataset preparation, a pretrained causal-LM baseline, prompt and decoding comparisons, structured JSON validation, a callable validation tool, and evaluation artifacts. The experiments show that stronger lexical overlap or valid JSON does not ensure faithful summaries or supported action items. The system should therefore be presented as an assistive prototype with human review, explicit limitations, and a transparent account of the test-split evaluation. The Kaggle page lists the license as Unknown; this report records that information and does not claim redistribution rights. Before submission, each member should confirm their concise contribution statement, and the group should rehearse and time the presentation.

## References and Project Artifacts

1. Gliwa, B., Mochol, I., Biesek, M., and Wawer, A. (2019). “SAMSum Corpus: A Human-annotated Dialogue Dataset for Abstractive Summarization.” Proceedings of the 2nd Workshop on New Frontiers in Summarization, 70–79. https://doi.org/10.18653/v1/D19-5409.
2. Malode, N. (2023). “Samsum Dataset Text summarization,” Kaggle dataset, version 1 (page metadata last updated 23 June 2023). https://www.kaggle.com/datasets/nileshmalode1/samsum-dataset-text-summarization. Kaggle lists the license as Unknown; this citation records the reported download page, not redistribution permission. Page metadata checked 28 October 2026.
3. Qwen Team. “Qwen2.5-1.5B-Instruct.” Hugging Face model card. https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct. Accessed 29 October 2026.
4. Google. “FLAN-T5-base.” Hugging Face model card. https://huggingface.co/google/flan-t5-base. Accessed 29 October 2026.
5. “DistilBART-CNN-12-6.” Hugging Face model card. https://huggingface.co/sshleifer/distilbart-cnn-12-6. Accessed 29 October 2026.
6. Kingma, D. P., and Welling, M. (2014). “Auto-Encoding Variational Bayes.” International Conference on Learning Representations. https://arxiv.org/abs/1312.6114.
7. Goodfellow, I., et al. (2014). “Generative Adversarial Nets.” Advances in Neural Information Processing Systems 27. https://papers.nips.cc/paper/5423-generative-adversarial-nets.
8. Vaswani, A., et al. (2017). “Attention Is All You Need.” Advances in Neural Information Processing Systems 30. https://papers.nips.cc/paper/7181-attention-is-all-you-need.
9. Lewis, M., et al. (2020). “BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension.” Proceedings of ACL 2020. https://doi.org/10.18653/v1/2020.acl-main.703.
10. Lin, C.-Y. (2004). “ROUGE: A Package for Automatic Evaluation of Summaries.” Text Summarization Branches Out, 74–81. https://aclanthology.org/W04-1013/.
11. Experiment code, outputs, data-quality records, and project documentation are linked in the repository sections cited in this report.

## Appendix A — Submission Checks

- [x] Record the reported Kaggle source URL, page version 1, Kaggle uploader, and underlying SAMSum paper citation.
- [x] Cite the reported Kaggle source/version and disclose that the listed license is Unknown; do not claim redistribution rights or redistribute dataset files.
- [x] Check that the in-text source references resolve to the numbered bibliography entries and that model/metric claims have references.
- [x] The 29 October 2026 render was 14 pages total, with an 11-page body before references/appendices. Re-render after report content or layout changes to verify the submitted copy still meets the 10–15-page requirement.
- [x] Latest offline test suite passed 66 tests; this check did not rerun model inference.
- [x] Disclose that the 50-sample test-split comparison is comparative evidence, not an untouched holdout; do not continue tuning on it.
- [x] Use the standard VAE, GAN, and autoregressive Transformer family set as directed; avoid asserting that each was explicitly taught without course notes/slides.
- [x] Execute the integrated notebook/demo in the project environment on CPU; inspect the saved result and commitment-warning output.
- [x] Add the group roster from the assignment brief.
- [x] Generate a 10-slide PowerPoint presentation from the reviewed slide outline.
- [ ] Have each member review, complete, and personally confirm the contribution notes in the group template.
- [ ] Rehearse and time the presentation to 8–10 minutes.
- [ ] Ensure all members can explain the complete workflow and limitations.
