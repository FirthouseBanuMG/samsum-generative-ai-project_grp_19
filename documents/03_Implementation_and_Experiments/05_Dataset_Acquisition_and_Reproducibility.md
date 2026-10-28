# Dataset Acquisition and Reproducibility

## 1. Purpose

This guide documents how to prepare the SAMSum dataset for the group project, reproduce the existing preprocessing results, and avoid accidental data leakage.

The raw and processed CSV files are intentionally excluded from Git. Each group member must obtain the dataset from an appropriate source and verify its structure and licensing before using or redistributing it.

## 2. Source and redistribution checks

### Recorded source

The project team reports obtaining the files from the Kaggle dataset **“Samsum Dataset Text summarization”** by Nilesh Malode:

- Dataset page: <https://www.kaggle.com/datasets/nileshmalode1/samsum-dataset-text-summarization>
- Kaggle page identifier: `nileshmalode1/samsum-dataset-text-summarization`
- Page metadata reports dataset version `1` and last modified `2023-06-23`.
- Kaggle page metadata lists the license as **Unknown**.
- The page describes the dataset as created by Nilesh Malode; it does not by itself establish the upstream SAMSum release/version or the rights to redistribute the underlying corpus.
- The team reports this Kaggle page as its download source; an exact local download date and archive-to-CSV provenance record were not retained.

The scholarly SAMSum paper is cited in the final report for the underlying corpus. Before redistribution or submission of the data files, verify the upstream SAMSum terms and any applicable Kaggle uploader/license terms. Do not infer permission from public availability, and do not commit raw or processed data unless redistribution rights are confirmed and the team approves it.

## 3. Expected raw files

From the repository root, place the following CSV files in `data/raw/`:

| File | Expected rows |
|---|---:|
| `samsum-train.csv` | 14,732 |
| `samsum-validation.csv` | 818 |
| `samsum-test.csv` | 819 |

Expected columns are `id`, `dialogue`, and `summary`.

These row counts describe the dataset copy audited for this project. If a different version or export produces different counts, investigate and document the discrepancy rather than silently changing the expected values.

## 4. Verify the local files

Run these commands from the repository root:

```powershell
Get-FileHash .\data\raw\samsum-train.csv -Algorithm SHA256
Get-FileHash .\data\raw\samsum-validation.csv -Algorithm SHA256
Get-FileHash .\data\raw\samsum-test.csv -Algorithm SHA256
```

SHA-256 values recorded for the previously audited local copies:

| File | SHA-256 |
|---|---|
| `samsum-train.csv` | `03CA44B69042741F82603FA4C1FD66E919519637DCE7219D327F22947DB25B42` |
| `samsum-validation.csv` | `29A36F37B530AFF1616E6BAA0B146253F47FF6D02E2653FAA2FC3A8EBDB590F7` |
| `samsum-test.csv` | `7104369C1CF0658B0D42FF759B3D4E23A1762B5B67DE56E3E556CD5FA63C8AF3` |

These are fingerprints of the previously audited local files, not independently authenticated upstream checksums. A mismatch should trigger investigation of the dataset source, version, encoding, or export process.

## 5. Reproduce validation and preprocessing

Activate the project's virtual environment if necessary, then run:

```powershell
.\.venv\Scripts\python.exe -m data_processing.validate_dataset
.\.venv\Scripts\python.exe -m data_processing.profile_dataset
.\.venv\Scripts\python.exe -m data_processing.profile_token_lengths
.\.venv\Scripts\python.exe -m data_processing.verify_raw_dataset_integrity
.\.venv\Scripts\python.exe -m data_processing.preprocess_dataset
.\.venv\Scripts\python.exe -m data_processing.validate_processed_dataset
.\.venv\Scripts\python.exe -m data_processing.check_split_leakage
```

Review each command's output. Resolve errors before proceeding. Confirm the generated metadata and exclusions are consistent with the current source files.

Raw validation, profiling, integrity verification, and preprocessing read the raw files for audit/preparation; they do not train or evaluate a model. Model-generation and evaluation workflows use processed CSVs or baseline outputs created from the processed training split. The leakage-check runner compares the processed splits.

## 6. Previously observed data-quality results

The audited dataset contained 16,369 raw rows across the three splits. One training row had a missing or blank dialogue and was excluded from dialogue-based experiments.

Previously observed processed row counts:

| Split | Processed rows |
|---|---:|
| Train | 14,731 |
| Validation | 818 |
| Test | 819 |

The prior split audit found no shared IDs and no exact dialogue-summary pairs shared across splits. This does not rule out semantic near-duplicates.

The preprocessing policy preserves dialogue text without aggressive cleaning and records exclusions. Missing or blank reference summaries must be handled explicitly for reference-based evaluation rather than silently treated as valid examples.

These are previously recorded results. Re-run the validation scripts to confirm them against the files currently on the machine.

## 7. Split-use policy

- **Train:** pipeline development and any carefully controlled few-shot example selection.
- **Validation:** model, prompt, and decoding development and comparisons.
- **Test:** 50 examples have already been used for the model-family comparison. Treat those results as comparative/selection evidence, not as an untouched holdout, and do not continue tuning against that subset.

Record the split, sample IDs, model identifier, prompt, decoding parameters, generated outputs, and evaluation settings for each experiment.

## 8. Current baseline status

The repository contains a small CPU smoke-test run using `Qwen/Qwen2.5-1.5B-Instruct`. Its selected examples came from the training split and are intended for qualitative pipeline verification.

The recorded outputs include unsupported details in some summaries. The smoke test is therefore evidence that generation runs, not evidence of reliable summarization or a measured performance result.

See:
- `outputs/baseline_smoke_test/baseline_outputs.json`
- `outputs/baseline_smoke_test/run_metadata.json`
- `documents/03_Implementation_and_Experiments/04_Experiment_and_Decision_Log.md`

## 9. Reproducibility checklist

Before reporting results, confirm that:

- [ ] The dataset source, version, and license have been recorded.
- [ ] The raw files have been checked for expected columns and row counts.
- [ ] Validation and split-leakage checks have been run.
- [ ] Preprocessing exclusions and metadata have been reviewed.
- [ ] Train, validation, and test usage follows the documented policy.
- [ ] Model, prompt, decoding settings, sample IDs, and outputs are recorded.
- [ ] Generated summaries have been checked for unsupported claims.
- [ ] Performance claims are supported by a documented evaluation, not the smoke test alone.
