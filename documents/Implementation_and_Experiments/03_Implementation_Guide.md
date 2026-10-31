# SAMSum Implementation Guide

**Status verified:** 31 October 2026  
**Scope:** Current implementation, evidence locations, and commands for reproducing the project's core workflow. For environment installation details, use the [Environment Setup and Run Guide](../Environment_Setup/Prerequisites_and_Environment_Setup.md).

## 1. What is implemented

The project is an inference and evaluation prototype. It uses pretrained models; it does not train or fine-tune them.

| Area | Current implementation | Evidence and limits |
|---|---|---|
| Dataset handling | `src/data_processing/` validates, profiles, checks raw hashes, preprocesses into separate files, validates processed data, and checks exact cross-split IDs/pairs | Raw counts 14,732/818/819; processed counts 14,731/818/819. One blank-dialogue training row is recorded as excluded. Checks do not find semantic near-duplicates. |
| Baseline generation | `src/baseline/model_smoke_test.py` uses `Qwen/Qwen2.5-1.5B-Instruct` with greedy decoding on three selected training examples | `outputs/baseline_smoke_test/`; qualitative pipeline evidence, not a population performance estimate |
| Prompt experiments | `src/prompting/prompts.py` and `src/prompting/run_prompt_experiments.py` compare zero-shot, few-shot, role-based, and constraint-based prompting | Three training examples per strategy; manual rubric results are exploratory |
| Length comparison | `src/prompting/run_summary_detail_comparison.py` compares concise and detailed prompts on the same three examples | `outputs/summary_detail_comparison/`; concise outputs were shorter and had higher ROUGE on this small sample, not proof of better factual quality |
| Decoding experiments | `src/generation/run_decoding_experiments.py` compares greedy decoding with three sampling configurations | Fixed constraint prompt; sampling uses three seeds for each of the three training examples. More varied output is not necessarily more accurate. |
| Model comparison | `src/evaluation/run_model_family_comparison_50.py` evaluates Qwen, FLAN-T5-base, and DistilBART-CNN on seeded test-split examples; it records pre-truncation token counts and truncation flags, and supports excluding a previous manifest | `outputs/model_comparison_50_samples/`; inputs differ by model and the existing 50-example subset is no longer an untouched holdout |
| Structured output | `src/structured_output/schema.py` defines required JSON fields; `run_structured_output.py` extracts/parses, validates, retries once, and flags fallback | `summary`, `key_points`, `decisions`, and `action_items`; schema validity is structural, not factual |
| Coverage warning | `src/structured_output/coverage.py` flags a narrow pattern of missing first-person commitments | Warning does not repair output, block tool invocation, or guarantee completeness |
| Tool/function workflow | `src/tool_calling/run_tool_calling.py` validates an allowlisted JSON request and generates a final response after a valid tool result | Application-level JSON protocol, not native model-specific tool-call parsing; invalid tool results block follow-up generation |
| Integrated application | `src/integrated_demo/run_integrated_demo.py` accepts a training sample ID or supplied dialogue text/file, generates structured output, runs validation, and saves the result | `outputs/integrated_demo/demo_result.json`; sample `13818513` demonstrates a missed promise that the heuristic warns about |

## 2. Source layout

```text
src/
  baseline/          Baseline generation and evaluation preparation
  data_processing/  Raw/processed data checks and preprocessing
  evaluation/       Model comparison experiments and document utilities
  generation/       Decoding experiments
  integrated_demo/  CLI demo and console presentation formatting
  prompting/        Prompt templates and prompt experiments
  structured_output/ JSON schema, recovery, and coverage warning
  tool_calling/     Allowlisted application-level tool demonstration
  project_paths.py  Shared repository-root resolution
tests/              Offline tests for implemented logic
```

The notebook `notebooks/01_integrated_demo.ipynb` demonstrates the integrated workflow. Current documentation and outputs live under `documents/` and `outputs/`, respectively.

## 3. Data and experiment workflow

1. Put the three source CSVs in `data/raw/`; do not modify them.
2. Validate and profile the raw files, verify hashes against the recorded local baseline, and run preprocessing.
3. Use only `data/processed/` for generation and evaluation. The preprocessing metadata and `exclusions.json` record the single excluded training row.
4. Use training examples for the documented baseline and small prompt/decoding experiments. Validation is available for future development.
5. Treat the completed 50-example test comparison as comparative evidence only. Do not tune against it or call it an untouched final test.

Reproduce the dataset checks from the repository root:

```powershell
.\.venv\Scripts\python.exe -m data_processing.validate_dataset
.\.venv\Scripts\python.exe -m data_processing.verify_raw_dataset_integrity
.\.venv\Scripts\python.exe -m data_processing.preprocess_dataset
.\.venv\Scripts\python.exe -m data_processing.validate_processed_dataset
.\.venv\Scripts\python.exe -m data_processing.check_split_leakage
```

Inspect command output and generated metadata before continuing. These commands recreate or update processed artifacts; preserve the raw source files.

## 4. Run the integrated demo

From the repository root, with the project environment and processed training CSV available:

```powershell
.\.venv\Scripts\python.exe -m integrated_demo.run_integrated_demo --sample-id 13818513
```

The CLI accepts a training-split sample ID or a supplied dialogue using `--dialogue` or `--dialogue-file`. The demo loads Qwen, generates and validates structured JSON, runs the narrow coverage heuristic, and builds an allowlisted validation request in application code. Only schema-valid output that did not use fallback proceeds to the validator. A valid tool result is sent back to the model for a final response; a failed check blocks that follow-up. Coverage warnings are appended after successful generation and do not block tool use.

The demo writes a machine-readable record to `outputs/integrated_demo/demo_result.json`. Training-split sample text is included; supplied text is omitted by default and represented by a SHA-256 fingerprint. The console renderer displays the summary, key points, decisions, action items, and review warnings as a readable table. Model weights may download on first run; CPU generation can take several minutes.

The original sample-ID mode remains the default. To process a supplied dialogue locally, pass text or a UTF-8 file:

```powershell
.\.venv\Scripts\python.exe -m integrated_demo.run_integrated_demo --dialogue-file path\to\dialogue.txt
```

By default, the saved record omits user-supplied dialogue text and keeps only its SHA-256 fingerprint; use `--save-input` only when retaining the source text is appropriate. For a CUDA runtime, explicitly pass `--device cuda`; `--device auto` selects CUDA when available and otherwise CPU. CPU remains the default. On Colab or another hosted runtime, do not submit private conversations unless the data owner has approved that processing location.

## 5. Run automated tests

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

The latest local run passed all **66 tests**. The suite validates application logic offline; it does not load model weights or prove semantic factuality.

## 6. Interpreting the evidence

- The Kaggle listing used by the team reports version 1 and license **Unknown**. Do not claim redistribution rights; dataset files are not tracked in the repository.
- ROUGE measures lexical overlap with reference summaries, not factual accuracy, attribution, or action-item correctness.
- The prompt rubric has only three examples per strategy.
- The 50-sample model comparison used test-split examples and different input formats across models.
- The comparison runner records the pre-truncation token count and a truncation flag for each generation; inspect flagged examples before interpreting their scores.
- JSON Schema and the allowlisted tool validate structure. They do not determine whether claims are supported by the dialogue.
- Human review against the source conversation is required before acting on generated summaries or action items.

### Reserve a separate sample for final comparison and human review

The existing 50-example test manifest records the subset already used for model selection. After model, prompt, and evaluation choices are frozen, create a disjoint run and separate human-review files with:

```powershell
.\.venv\Scripts\python.exe -m evaluation.run_model_family_comparison_50 --samples 50 --seed 2026 --exclude-manifest outputs\model_comparison_50_samples\sample_manifest.json
```

This writes to the new `outputs/final_evaluation/` directory, excludes every ID in the earlier manifest, and refuses to overwrite a non-empty reserved output directory. Reviewers should independently score the two blinded CSVs against the dialogue without seeing `review_key.json`. After completing every rating, summarize them with:

```powershell
.\.venv\Scripts\python.exe -m evaluation.summarize_human_reviews --reviewer-1 outputs\final_evaluation\human_review_reviewer_1.csv --reviewer-2 outputs\final_evaluation\human_review_reviewer_2.csv --review-key outputs\final_evaluation\review_key.json --output outputs\final_evaluation\human_review_summary.csv
```

The review summary reports mean scores and simple exact-agreement/mean-absolute-difference statistics; it is descriptive, not a chance-corrected reliability measure. Preparing or running this evaluation does not itself constitute completed human review. Keep evaluation outputs local unless dataset sharing rights have been established.

## 7. Verification record

On 31 October 2026, the raw dataset validator, recorded SHA-256 integrity check, processed-dataset validator, and cross-split ID/exact-pair checker passed. The raw hashes matched the project's 16 October local baseline; this does not establish upstream authenticity. The 45-test offline suite passed. Saved model-backed outputs document the CPU demo and experiments; this verification pass did not rerun model inference.
