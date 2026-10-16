# SAMSum Data Quality and Preparation Report

## 1. Audit status

Initial file audit completed through PowerShell on the project workspace.

## 2. Raw dataset files verified

| File | Size in bytes | Status |
|---|---:|---|
| samsum-train.csv | 9,401,418 | Present |
| samsum-validation.csv | 512,131 | Present |
| samsum-test.csv | 530,165 | Present |

Location: `data/raw/`

## 3. Validation script

- Script: `src/validate_dataset.py`
- File size: 1,781 bytes
- Status: Present
- Previous execution findings: train 14,732 rows, validation 818 rows, test 819 rows.
- One training record has a missing/blank dialogue; no duplicate IDs were reported in the initial validation.

## 4. Processed data audit

At the time of this audit, `data/processed/` contained no files.

## 5. Existing implementation documentation

- `03_Implementation_Guide.docx`
- `04_Experiment_and_Decision_Log.docx`

## 6. Decisions and limitations

- Original CSV files will be preserved unchanged.
- The invalid training record will be investigated and, if confirmed unusable, excluded only from downstream processing.
- The test split will remain untouched during prompt development and model selection.
- Cross-split duplicate checks and a formal preprocessing pipeline are still pending.
- This report records an initial audit; it does not claim that complete data engineering has been finished.

## 7. Next step

Review the existing validation script and rerun it to capture current, reproducible data-quality results before implementing preprocessing.

## 8. Review of the Existing Validation Script

The script `src/validate_dataset.py` currently checks:
- Presence of the required columns: id, dialogue, summary.
- Row counts and column names for each split.
- Missing values and blank dialogue/summary fields.
- Duplicate IDs within each split.
- Minimum, median and maximum dialogue character lengths.
- A representative example from each split.

Limitations identified:
- No cross-split duplicate or leakage check.
- No summary-length profiling.
- No machine-readable validation report is saved.
- The script reports missing files but does not fail the entire run.

Status: Initial validation exists; additional data-quality checks remain necessary.

## 9. Fresh Validation Results

Validation script executed successfully using the project virtual-environment Python.

| Split | Rows | Missing dialogue | Blank dialogue | Missing summary | Blank summary | Duplicate IDs |
|---|---:|---:|---:|---:|---:|---:|
| Train | 14,732 | 1 | 1 | 0 | 0 | 0 |
| Validation | 818 | 0 | 0 | 0 | 0 | 0 |
| Test | 819 | 0 | 0 | 0 | 0 | 0 |
| Total | 16,369 | 1 | 1 | 0 | 0 | 0 |

All splits contain the expected columns: id, dialogue, summary.

Dialogue character lengths:
- Train: minimum 31, median 401, maximum 5,492.
- Validation: minimum 57, median 386, maximum 2,950.
- Test: minimum 49, median 403, maximum 2,793.

Representative examples were printed by the script for all three splits.

Interpretation and limitations:
- One training record has a missing and blank dialogue; it requires explicit handling in preprocessing.
- No duplicate IDs were found within individual splits.
- Cross-split duplicate and leakage checks have not yet been performed.
- Original CSV files remain the source of truth and must not be overwritten.
- Validation data will support development comparisons; test data is reserved for final evaluation.

Evidence:
- Script: `src/validate_dataset.py`
- Execution: successful terminal run during the project workflow.

## 9. Fresh Validation Results

Validation script executed successfully using the project virtual-environment Python.

| Split | Rows | Missing dialogue | Blank dialogue | Missing summary | Blank summary | Duplicate IDs |
|---|---:|---:|---:|---:|---:|---:|
| Train | 14,732 | 1 | 1 | 0 | 0 | 0 |
| Validation | 818 | 0 | 0 | 0 | 0 | 0 |
| Test | 819 | 0 | 0 | 0 | 0 | 0 |
| Total | 16,369 | 1 | 1 | 0 | 0 | 0 |

All splits contain the expected columns: id, dialogue, summary.

Dialogue character lengths:
- Train: minimum 31, median 401, maximum 5,492.
- Validation: minimum 57, median 386, maximum 2,950.
- Test: minimum 49, median 403, maximum 2,793.

Representative examples were printed by the script for all three splits.

Interpretation and limitations:
- One training record has a missing and blank dialogue; it requires explicit handling in preprocessing.
- No duplicate IDs were found within individual splits.
- Cross-split duplicate and leakage checks have not yet been performed.
- Original CSV files remain the source of truth and must not be overwritten.
- Validation data will support development comparisons; test data is reserved for final evaluation.

Evidence:
- Script: `src/validate_dataset.py`
- Execution: successful terminal run during the project workflow.

## 10. Cross-Split Leakage Audit

Script: `src/check_split_leakage.py`

Result: Completed successfully.

| Comparison | Shared IDs | Shared exact dialogue-summary pairs |
|---|---:|---:|
| Train vs Validation | 0 | 0 |
| Train vs Test | 0 | 0 |
| Validation vs Test | 0 | 0 |

Interpretation:
- No shared IDs or exact dialogue-summary pairs were detected across the splits.
- This check does not detect near-duplicate dialogues or semantic overlap.
- The source CSV files were not modified.
- The test split remains reserved for final evaluation.

Evidence: successful execution output from `src/check_split_leakage.py`.

## 11. Proposed Preprocessing Policy

Status: Design approved for implementation, subject to inspection of invalid records.

1. Preserve all original CSV files unchanged.
2. Exclude rows with missing/blank dialogue from dialogue-based experiments; log their IDs and exclusion reasons.
3. Exclude rows with missing/blank reference summaries only from experiments requiring reference summaries; log the reasons.
4. Investigate duplicate IDs and stop for review rather than silently deleting records.
5. Preserve dialogue wording, punctuation, speaker labels and special markers unless a justified transformation is documented.
6. Do not use the test split for prompt tuning or model selection.
7. Record preprocessing configuration, exclusions, output row counts and validation results.
8. Inspect the known invalid training record before finalizing its handling.

These rules are provisional until the invalid record is inspected and the preprocessing output is validated.

## 12. Invalid Training Record Investigation

Inspection confirmed one training record with a missing dialogue.

- Record ID: `13828807`
- Dialogue: Missing (`NaN`)
- Reference summary: `problem with visualization of the content`
- Decision: Exclude this record from dialogue-based summarization experiments.
- Rationale: The source conversation is unavailable, so the record cannot support input-conditioned summarization or a reliable input-reference evaluation.
- Data preservation: Keep the original row unchanged in `data/raw/samsum-train.csv`; log its exclusion in preprocessing metadata.
- No dialogue reconstruction or fabricated input will be attempted.

## 13. Dialogue and Reference-Summary Length Profiling

Script: `src/profile_dataset.py`

| Split | Dialogue median (chars) | Dialogue p95 (chars) | Dialogue max (chars) | Summary median (chars) | Summary p95 (chars) | Summary max (chars) |
|---|---:|---:|---:|---:|---:|---:|
| Train | 401 | 1,292 | 5,492 | 96 | 235 | 300 |
| Validation | 386 | 1,217 | 2,950 | 96 | 239 | 300 |
| Test | 403 | 1,373 | 2,793 | 96 | 222 | 300 |

Interpretation:
- Reference summaries are substantially shorter than dialogues in character count.
- Dialogue lengths vary; the training split contains the longest observed dialogue.
- Character counts are not equivalent to tokenizer token counts.
- Input and output token limits will be selected only after profiling with the chosen model tokenizer.
- Raw CSV files were not modified.

## 14. Model-Tokenizer Length Profiling

Script: `src/profile_token_lengths.py`
Tokenizer: `Qwen/Qwen2.5-1.5B-Instruct`
Method: Tokenizer encoding with `add_special_tokens=False`.

| Split | Dialogue count | Dialogue median | Dialogue p95 | Dialogue max | Summary median | Summary max |
|---|---:|---:|---:|---:|---:|---:|
| Train | 14,731 | 114 | 343 | 1,051 | 23 | 86 |
| Validation | 818 | 110 | 329 | 698 | 22 | 78 |
| Test | 819 | 117 | 356 | 700 | 23 | 88 |

Interpretation:
- Dialogue token counts are substantially larger than reference-summary token counts.
- Some dialogues are considerably longer than the 95th percentile.
- These counts exclude special tokens and prompt-template overhead.
- No truncation limit has been finalized; limits must account for the final prompt and model context constraints.
- Raw CSV files were not modified.

Evidence: successful execution output from `src/profile_token_lengths.py`.

## 15. Approved Preprocessing Implementation Design

Status: Approved for implementation.

1. Preserve original CSV files under `data/raw/` unchanged.
2. Exclude training record `13828807` from processed dialogue-based experiments because its dialogue is missing.
3. Validate required columns and fail on unexpected duplicate IDs rather than silently removing records.
4. Preserve dialogue and summary text as supplied. Do not apply aggressive cleaning or truncation.
5. Save processed splits and an exclusion log under `data/processed/`.
6. Validate processed row counts, required columns, missing/blank text and ID uniqueness.
7. Record preprocessing configuration, exclusions and results in this report.
8. Retain validation data for development comparisons and reserve test data for final evaluation.

Implementation must be verified by execution and post-processing checks before the pipeline is considered complete.

## 16. Preprocessing Execution and Artifact Verification

Script: `src/preprocess_dataset.py`

Execution status: Successful. Output files and metadata were inspected.

| Split | Source rows | Processed rows | Excluded rows |
|---|---:|---:|---:|
| Train | 14,732 | 14,731 | 1 |
| Validation | 818 | 818 | 0 |
| Test | 819 | 819 | 0 |
| Total | 16,369 | 16,368 | 1 |

Artifacts verified:
- `data/processed/samsum-train-processed.csv`
- `data/processed/samsum-validation-processed.csv`
- `data/processed/samsum-test-processed.csv`
- `data/processed/exclusions.json`
- `data/processed/preprocessing_metadata.json`

The exclusion log records training ID `13828807` with reason `missing_or_blank_dialogue`.

The metadata records the required columns, source/output paths, row counts, exclusion counts, no text transformation, no truncation and no modification of source files.

Limitation: Independent post-processing checks across all saved CSVs are still required before declaring the pipeline fully verified.

## 17. Independent Post-Processing Validation

Script: `src/validate_processed_dataset.py`

Execution result: All assertions passed.

| Split | Expected rows | Actual rows | Required columns | Unique IDs | Valid dialogue and summary |
|---|---:|---:|---|---|---|
| Train | 14,731 | 14,731 | PASS | PASS | PASS |
| Validation | 818 | 818 | PASS | PASS | PASS |
| Test | 819 | 819 | PASS | PASS | PASS |

Checks performed:
- Required columns are present.
- Row counts match expected values.
- IDs are non-null and unique within each processed split.
- Dialogues and summaries are non-null and non-blank.

Conclusion: All processed splits passed these independent checks. Cross-split exact-duplicate checks were performed on the raw data earlier; near-duplicate detection remains outside the current audit scope.

## 18. Raw Dataset SHA-256 Integrity Baseline

SHA-256 hashes were recorded on 16 October 2026 as a baseline for detecting future changes to the raw dataset files. These hashes were not captured before the earlier preprocessing steps, so they establish a baseline from this point onward rather than proving historical integrity.

| Raw file | SHA-256 |
|---|---|
| samsum-train.csv | 03CA44B69042741F82603FA4C1FD66E919519637DCE7219D327F22947DB25B42 |
| samsum-validation.csv | 29A36F37B530AFF1616E6BAA0B146253F47FF6D02E2653FAA2FC3A8EBDB590F7 |
| samsum-test.csv | 7104369C1CF0658B0D42FF759B3D4E23A1762B5B67DE56E3E556CD5FA63C8AF3 |

**Purpose:** Recalculate these hashes after future data-processing changes and compare them with this baseline. The original raw CSV files must remain unchanged.

## 19. Raw Dataset Integrity Verification

**Verification date:** 16 October 2026

All three raw CSV files were re-hashed using SHA-256 and compared against the baseline recorded in Section 18.

| File | Result |
|---|---|
| samsum-train.csv | PASS |
| samsum-validation.csv | PASS |
| samsum-test.csv | PASS |

**Conclusion:** All three files match the recorded baseline. No hash differences were detected. This confirms integrity relative to the baseline established in Section 18; it does not establish integrity before that baseline was recorded.

## 20. Experimental Data-Use and Baseline Sample Policy

### Dataset split responsibilities

| Split | Permitted use in this project |
|---|---|
| Training | Initial pipeline smoke tests and qualitative debugging |
| Validation | Controlled prompt, model, and decoding configuration comparisons |
| Test | Final evaluation after the experimental protocol and configurations are fixed |

The raw CSV files remain unchanged. Preprocessed files are separate artifacts. The training smoke test is not a quantitative performance evaluation, and the test split must not be used to select prompts or configurations.

### Initial baseline sample selection

Three examples were selected from the processed training split for the initial `Qwen/Qwen2.5-1.5B-Instruct` pipeline smoke test.

| Sample ID | Selection purpose |
|---|---|
| `13818513` | Simple request and agreement |
| `13681000` | Advice and tentative action |
| `13728094` | Longer, multi-speaker discussion |

The selection manifest is `data/processed/baseline_sample_manifest.json`. The generation results and run metadata are stored in `outputs/baseline_smoke_test/baseline_outputs.json` and `outputs/baseline_smoke_test/run_metadata.json`.

### Initial qualitative observations

The first sample was broadly consistent with its reference summary. The second and third generated summaries included details not supported by their dialogues. These observations demonstrate potential faithfulness failures but do not establish a general model error rate or comparative performance.

### Limitations and safeguards

- Three examples are sufficient for an initial pipeline smoke test, not for a reliable performance estimate.
- The six validation examples previously inspected were not used for generation in this baseline run.
- No test examples were used for baseline generation.
- Subsequent comparisons should record sample selection, prompts, decoding settings, generated outputs, and evaluation criteria.
- Any quantitative claims must be supported by a documented evaluation protocol and results.

**Status:** Initial baseline generation completed; controlled validation experiments and final test evaluation remain pending.
