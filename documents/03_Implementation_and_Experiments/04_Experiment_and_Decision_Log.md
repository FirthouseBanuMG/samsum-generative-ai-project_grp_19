# Experiment and Decision Log

*Experiment records and decision history*

Project: SAMSum-Based Intelligent Conversation Summarization and Action-Item Extraction

Document status: Chronological record; initial templates date from 15 October 2026, with subsequent results added in later sections.

Working rule: Record proposed choices as proposed until the team verifies them. Never report unrun experiments as results.

> Sections A-F preserve the initial starter templates and proposed entries; their `TBD` and `Pending` values are historical placeholders, not current experiment status. Recorded work begins in the dated sections that follow. For current status, use the [Master Project Plan](../01_Project_Planning/Master_Project_Plan.md) and [Assignment-to-Evidence Matrix](./03_Assignment_to_Evidence_Matrix.md).

# A. Experiment run record

| **Field** | **What to record** |
|----|----|
| Run ID | E1-01, E2-03, etc. |
| Date / owner | Actual date, owner, reviewer |
| Git commit | Commit hash used for the run |
| Dataset | Source, split, exact sample IDs |
| Model | Model ID and revision if available |
| Prompt | Prompt ID/version and full prompt path |
| Decoding | do_sample, temperature, top_k, top_p, max_new_tokens, seed where relevant |
| Environment | Python version and requirements-lock file/hash |
| Output | Path to raw generated output |
| Evaluation | Metric values and rubric scores; describe scoring method |
| Observation | What happened, including failures |
| Decision | Keep/change/reject and why |

# B. Prompt comparison log

| **Run ID** | **Prompt type** | **Main change** | **Fixed variables** | **Sample IDs** | **Observed quality** | **Decision** |
|----|----|----|----|----|----|----|
| E2-01 | Zero-shot | Baseline instruction | Model, decoding, inputs | TBD | Pending run | Pending |
| E2-02 | Few-shot | Add selected examples | Model, decoding, inputs | TBD | Pending run | Pending |
| E2-03 | Role/context | Add role and task context | Model, decoding, inputs | TBD | Pending run | Pending |
| E2-04 | Constraint-based | Add length/faithfulness/JSON constraints | Model, decoding, inputs | TBD | Pending run | Pending |

# C. Decoding comparison log

| **Run ID** | **Mode** | **Temperature** | **top_k/top_p** | **Repeat count** | **Quality / variability** | **Runtime** |
|----|----|----|----|----|----|----|
| E3-01 | Greedy | N/A or framework default | N/A | 1 | Pending run | Pending |
| E3-02 | Sampling | 0.2 | top_p=0.9 (proposed) | 3 | Pending run | Pending |
| E3-03 | Sampling | 0.7 | top_p=0.9 (proposed) | 3 | Pending run | Pending |

# D. Failure case log

| **Failure ID** | **Category** | **Input/sample ID** | **Actual output** | **Expected behavior** | **Impact** | **Mitigation** |
|----|----|----|----|----|----|----|
| F-01 | Hallucinated action item | TBD | Capture actual output | Only explicit action items | TBD | Prompt/schema/validation/human review |
| F-02 | Omission / loss of key fact | TBD | Capture actual output | Preserve key decisions | TBD | Prompt adjustment and rubric |
| F-03 | Invalid JSON or attribution error | TBD | Capture actual output | Schema-valid output / correct speaker | TBD | Parser, schema validation, safe fallback |

# E. Decision record

| **Decision ID** | **Date** | **Decision** | **Alternatives** | **Rationale/evidence** | **Owner** | **Revisit trigger** |
|----|----|----|----|----|----|----|
| D-001 | 15 Oct 2026 | Use SAMSum as the project dataset (confirm files) | AG News or another dataset | Project direction already selected; chat dialogues align with summary/action extraction | Team | If rubric or data access blocks use |
| D-002 | 15 Oct 2026 | Test Qwen2.5-1.5B-Instruct as candidate baseline | Other small causal LMs | Instruction-tuned causal LM; small enough to pilot, but CPU performance must be measured | Model owner | If model load or latency fails |

# F. Rules for honest reporting

- Never replace 'Pending run' with a guessed score.

- Record negative and inconclusive results; they are useful evidence.

- If a prompt or model changes, create a new run ID rather than overwriting prior results.

- Separate automatic metric results from human judgments.

- Keep final test-set results separate from prompt-selection results.

# Environment record guidance

Record only information needed to reproduce an experiment: Python and dependency versions, model identifier, dataset split and sample IDs, settings, and outputs. Use repository-relative paths in shared records. Keep personal hardware specifications, local absolute paths, drive-space readings, user-folder locations, and unrelated machine state out of project documentation.

# G. Data-use and evaluation protocol

**Decision date:** 16 October 2026
**Status:** Agreed working protocol; apply consistently to subsequent experiments.

## G.1 Dataset split usage

- **Training split:** Use selected examples for initial pipeline smoke tests. These outputs are qualitative debugging evidence, not independent evaluation results.
- **Validation split:** Reserve for controlled development experiments, prompt comparisons, and model/decoding selection.
- **Test split:** Reserve for final evaluation after the experimental protocol and configurations have been finalized.
- **Raw files:** Preserve the original dataset files without modification.
- **Preprocessing:** Use the documented processed splits and record exclusions and sample IDs.

## G.2 Exploratory validation inspection

Six validation examples were inspected during exploratory review: `13817023`, `13716628`, `13829420`, `13819648`, `13728448`, and `13814197`.

This inspection did not generate model outputs. These examples are not selected for the initial baseline smoke test. The attempted sample-manifest file was not found at the expected project path, so no manifest is assumed to exist.

## G.3 Rationale and safeguards

Training examples are used for initial pipeline verification to avoid consuming validation examples for this smoke test. Validation results may inform development decisions and therefore must not be represented as an untouched final test. Test-set evaluation should occur only after model, prompt, decoding, and evaluation choices are fixed.

**Retrospective update (28 October 2026):** A later 50-sample model-family comparison used the processed test split. Treat those results as comparative evidence, not a pristine final holdout, and do not continue tuning against that subset.

**Status:** Completed. The selected examples, rationale, and results are recorded in Sections H–I.

# H. Initial baseline smoke-test sample selection

**Date:** 16 October 2026
**Experiment:** `initial_baseline_smoke_test`
**Dataset split:** Processed training split
**Purpose:** Qualitative pipeline verification only; not a performance estimate.

| Sample ID | Conversation type | Selection rationale |
|---|---|---|
| `13818513` | Simple request and agreement | Check preservation of the key event and future action. |
| `13681000` | Advice and tentative action | Check whether a suggestion is distinguished from a confirmed decision. |
| `13728094` | Longer multi-speaker discussion | Check preservation of the main problem and advice without speaker confusion. |

**Manifest:** `data/processed/baseline_sample_manifest.json`

**Data-use safeguard:** These samples come from the training split. Validation and test examples are not used to generate outputs in this smoke test. The three examples are intentionally selected for pipeline verification and must not be presented as a representative evaluation sample.

**Status:** Sample selection recorded; baseline generation pending.

## I. Initial Baseline Smoke-Test Results

**Date:** 16 October 2026
**Experiment:** `initial_baseline_smoke_test`
**Model:** `Qwen/Qwen2.5-1.5B-Instruct`
**Execution device:** CPU
**Dataset split:** Training
**Decoding:** Greedy (`do_sample=False`), maximum 100 new tokens
**Samples:** `13818513`, `13681000`, `13728094`

### Execution outcome

The model loaded successfully and generated summaries for all three selected training examples. The results and run metadata were saved to:

- `outputs/baseline_smoke_test/baseline_outputs.json`
- `outputs/baseline_smoke_test/run_metadata.json`

Both files were verified to exist and parse as valid JSON. This was a qualitative pipeline smoke test, not a quantitative evaluation.

### Qualitative observations

1. **Sample `13818513`:** The generated summary captured the cookies and their planned delivery to Jerry the following day. It was broadly consistent with the reference.
2. **Sample `13681000`:** The generated summary included the Pomodoro suggestion but added unsupported details about moving belongings the next day and using post-it notes in a kanban-style system.
3. **Sample `13728094`:** The generated summary captured Rick's dissatisfaction and Naomi's advice, but added unsupported claims that Sam decided against confronting Rick and planned to address the situation later.

### Decision and limitations

- Retain the output artifacts as evidence of a successful end-to-end baseline run.
- Treat the unsupported details in samples `13681000` and `13728094` as initial hallucination observations to investigate in later experiments.
- Do not report an accuracy score or generalize model performance from three examples.
- This was the initial policy; the later 50-sample test comparison is disclosed above. Use validation data for controlled development and do not describe the used test subset as untouched.
- Record the prompt, decoding configuration, and observed failure cases for reproducibility.

**Status:** Initial baseline smoke test completed; controlled evaluation remains pending.

# J. Tool/Function-Calling Demonstration

**Date:** 25 October 2026

## J.1 Implementation

- **Model:** `Qwen/Qwen2.5-1.5B-Instruct`
- **Execution device:** CPU.
- **Implementation:** `src/tool_calling/run_tool_calling.py`
- **Tests:** `tests/test_tool_calling.py`
- **Saved evidence:** `outputs/tool_calling/tool_calling_demo.json`
- **Dataset:** SAMSum training sample `13818513`.
- **Runtime:** Approximately 14.2 seconds for the demonstration, including model generation.

The model generated a JSON request for the allowlisted Python tool `validate_summary_output`. The application parsed the request, checked the tool name and arguments, and executed the validator against the generated summary and action items.

**Protocol limitation:** This is an application-level JSON tool-call protocol, not native model-specific tool-call parsing. The application now appends the successful tool result to the model conversation and generates a final user-facing response. Invalid schema results block follow-up generation. The output also receives a deterministic notice that schema checks establish structure only and human review is required.

## J.2 Verification results

| Check | Observed result |
|---|---|
| Python compilation | Passed |
| Valid tool request | Passed |
| Schema-invalid output | Rejected |
| Unknown tool name | Rejected |
| Unexpected arguments | Rejected |
| Malformed JSON request | Rejected |
| Offline test suite after refactor | 32/32 project tests passed; includes mocked successful and blocked follow-up cases |
| Model-generated tool request | Generated and executed |
| JSON Schema validation | Passed for the demonstration output |
| Tool-result-to-model follow-up | Generated final response after valid tool result |
| Evidence file | Refreshed at the path listed above |

## J.3 Observed output and failure analysis

**Sample ID:** `13818513` (training split)

**Dialogue:** Amanda baked cookies, asked Jerry if he wanted some, Jerry agreed, and Amanda said she would bring some the next day.

The generated summary captured the main event and planned delivery. However, the generated action items included:

- Amanda: "Prepare cookies"
- Jerry: "Eat cookies"

These are not explicit commitments in the dialogue. The validator accepted the output because the JSON structure matched the schema.

**Finding:** Schema validity does not establish factual accuracy or whether an action item is supported by the dialogue.

**Mitigation:** Keep `human_review_required` set to `true`; review generated summaries and action items against the original dialogue; improve prompting and evaluate factual faithfulness separately from structural validity.

The saved evidence includes the raw request, parsed request, tool result, and final model response. The final response is accompanied by a deterministic notice explaining that schema validation checks structure only and human review is required.

## J.4 Technical decisions and limitations

1. Keep tool execution restricted to explicitly allowlisted tool names.
2. Validate request arguments before executing a tool.
3. Validate generated structured output with the existing JSON Schema validator.
4. Retain negative tests for malformed requests, unknown tools, incorrect arguments, and schema-invalid output.
5. Do not treat a successful schema check as proof of factual correctness.
6. Do not claim native model-specific tool calling. The tool-result-to-model follow-up is now implemented and is covered by offline tests.

**Status:** The model-backed round-trip was rerun and saved, and the complete 32-test suite passed. The added failure-path test verifies that invalid tool results block final-response generation. Semantic faithfulness remains a separate review and evaluation responsibility.

# K. Expanded Structured Output Contract

**Date:** 27 October 2026
**Experiment:** E4 schema expansion
**Implementation:** `src/structured_output/schema.py`, `src/prompting/prompts.py`, `src/structured_output/run_structured_output.py`
**Outputs:** `outputs/structured_output/structured_outputs.json`, `outputs/structured_output/structured_output_log.csv`

The E4 output contract now requires four fields: `summary`, `key_points`, `decisions`, and `action_items`. Key points and decisions are arrays of non-empty strings; action items remain objects with required `owner` and `task` strings and optional `due`. Prompts and the corrective retry instruct the model to use empty lists when appropriate and to distinguish tentative suggestions from decisions. Tool validation uses the same expanded schema.

The structured experiment was rerun on the original three training-split baseline examples. All three responses were valid JSON and passed the expanded schema on the first attempt; no repair or fallback was needed. This confirms structural compatibility only. All three generated outputs had an empty action-items list, despite explicit commitments in the dialogues. For sample `13728094`, the model claimed Sam decided to speak to Rick, although the dialogue leaves Sam uncertain. The result demonstrates that schema validation does not establish factual completeness or decision accuracy.

Focused regression tests for schema validation, recovery, and tool argument handling passed: 21 tests. The integrated demonstration and notebook were rerun with the expanded schema; the generated result was saved to `outputs/integrated_demo/demo_result.json`. Human review remains required.

# L. Concise-versus-Detailed Prompt Comparison

**Date:** 27 October 2026
**Experiment:** SAMSum summary length comparison
**Runner:** `src/prompting/run_summary_detail_comparison.py`
**Prompts:** `concise_summary_prompt` and `detailed_summary_prompt` in `src/prompting/prompts.py`
**Outputs:** `outputs/summary_detail_comparison/summary_detail_comparison.csv`, `summary_detail_comparison.json`, and `summary_detail_metrics.csv`

## L.1 Controlled variables

- Three baseline training examples: `13818513`, `13681000`, `13728094`
- Model: `Qwen/Qwen2.5-1.5B-Instruct`
- Same system message, tokenizer chat template, greedy decoding, and `max_new_tokens=100`
- Only requested summary detail/length varied: one sentence versus 3–5 sentences
- Both prompt variants shared instructions to use only supported facts, preserve uncertainty, distinguish suggestions from decisions, and avoid invented details

## L.2 Aggregate observations

| Style | Samples | Average words | Average sentences | Mean ROUGE-1 F1 | Mean ROUGE-L F1 |
|---|---:|---:|---:|---:|---:|
| Concise | 3 | 15.667 | 1.000 | 0.460 | 0.411 |
| Detailed | 3 | 42.333 | 3.333 | 0.294 | 0.275 |

The detailed condition generated longer text. The concise condition had higher reference-overlap scores for these three examples only. This is exploratory evidence, not proof that concise summaries are generally better; ROUGE does not measure factual accuracy.

## L.3 Qualitative failure observation

For dialogue `13728094`, both styles claimed that Sam decided to speak to Rick, despite Sam expressing uncertainty and considering letting the issue go. Length constraints did not eliminate unsupported decision claims. The detailed output included more context, but also more opportunity for unsupported additions. Human review remains necessary.

**Status:** Experiment executed and outputs saved. Focused prompt tests passed. No broad quality conclusion is drawn from the three-example sample.

# M. 50-Sample Model-Family Comparison

**Date:** 28 October 2026
**Experiment:** Comparative evaluation of Qwen, FLAN-T5, and DistilBART
**Detailed protocol:** [Model Family Comparison](05_Model_Family_Comparison/README.md)

## M.1 Protocol and sample

- **Dataset:** `data/processed/samsum-test-processed.csv`
- **Split:** Test
- **Sample:** 50 unique dialogues, selected with seed 42
- **Excluded pilot IDs:** `13818513`, `13681000`, `13728094`
- **Generations:** 150 total (one per model for each dialogue)
- **Execution:** CPU; greedy decoding (`do_sample=False`, `num_beams=1`)
- **Limits:** 1,024 input tokens; 100 new output tokens
- **Inputs:** Qwen and FLAN-T5 received constraint-based prompts; DistilBART received dialogue-only input.

The sample IDs are preserved in `outputs/model_comparison_50_samples/sample_manifest.json`. Because this comparison used test-split examples to compare/select models, these examples are no longer an untouched final holdout.

## M.2 Results

| Model | Samples | ROUGE-1 F1 | ROUGE-2 F1 | ROUGE-L F1 | Mean seconds/sample |
|---|---:|---:|---:|---:|---:|
| `Qwen/Qwen2.5-1.5B-Instruct` | 50 | 0.220521 | 0.072396 | 0.158634 | 21.68958 |
| `google/flan-t5-base` | 50 | 0.514008 | 0.248225 | 0.429139 | 0.63586 |
| `sshleifer/distilbart-cnn-12-6` | 50 | 0.265467 | 0.098079 | 0.199712 | 1.38020 |

FLAN-T5-base had the highest ROUGE scores and lowest recorded mean generation time in this run. ROUGE measures lexical overlap, not factual accuracy or action-item correctness. Different input formats mean this experiment compares the tested model configurations; it does not isolate architecture effects.

## M.3 Evidence and interpretation

- Aggregate metrics: `outputs/model_comparison_50_samples/model_family_metrics.csv`
- Per-example outputs and scores: `outputs/model_comparison_50_samples/model_family_comparison.csv` and `model_family_comparison.json`
- Sample IDs and seed: `outputs/model_comparison_50_samples/sample_manifest.json`
- Runner: `src/evaluation/run_model_family_comparison_50.py`
- Full methodology and limitations: [Model Family Comparison](05_Model_Family_Comparison/README.md)

Treat these results as comparative evidence, not an independent final test result. Do not tune prompts, models, or settings against these same 50 examples or rerun them as a new independent test.
