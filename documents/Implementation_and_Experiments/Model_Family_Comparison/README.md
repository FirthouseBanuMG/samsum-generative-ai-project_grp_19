
# Model Family Comparison

**Evidence status:** The results below are from the saved 28 October 2026 CPU run. The experiment was not rerun during the 31 October documentation and offline-verification pass.

## Purpose

Compare three pretrained models for SAMSum dialogue summarization using a reproducible 50-sample evaluation.

## Models

- `Qwen/Qwen2.5-1.5B-Instruct`
- `google/flan-t5-base`
- `sshleifer/distilbart-cnn-12-6`

## Evaluation Scope

- Dataset: `data/processed/samsum-test-processed.csv`
- Sample size: 50 unique test-split dialogues
- Random seed: 42
- Pilot IDs excluded: `13818513`, `13681000`, `13728094`
- Total generations: 150 (50 per model)
- Device: CPU for the recorded run
- Maximum input length: 1,024 tokens
- Maximum new output tokens: 100
- Decoding: `do_sample=False`, `num_beams=1`
- ROUGE-1, ROUGE-2, and ROUGE-L F1 were calculated with `rouge_score` and stemming.

## Input Formats

| Model | Input format |
|---|---|
| Qwen | Constraint-based prompt |
| FLAN-T5 | Constraint-based prompt |
| DistilBART | Dialogue only |

The input formats differ, so the results compare the tested model configurations rather than isolating model architecture alone.

## Results

| Model | ROUGE-1 F1 | ROUGE-2 F1 | ROUGE-L F1 | Mean seconds/sample |
|---|---:|---:|---:|---:|
| `Qwen/Qwen2.5-1.5B-Instruct` | 0.220521 | 0.072396 | 0.158634 | 21.68958 |
| `google/flan-t5-base` | 0.514008 | 0.248225 | 0.429139 | 0.63586 |
| `sshleifer/distilbart-cnn-12-6` | 0.265467 | 0.098079 | 0.199712 | 1.38020 |

FLAN-T5-base achieved the highest scores on all three ROUGE metrics and the lowest average generation time in this experiment. ROUGE measures lexical overlap with reference summaries and does not directly establish factual correctness.

## Report and evidence files

This README is the Markdown comparison report, including the protocol, results, interpretation, review guidance, and limitations. The redundant Word report was consolidated here and removed.

- `model_family_evaluation_50_samples.xlsx`: Evaluation workbook with model summary, detailed generations, methodology notes, and sample manifest.
- `src/evaluation/run_model_family_comparison_50.py`: Reproducible 50-sample evaluation runner.
- `outputs/model_comparison_50_samples/model_family_comparison.csv`: Detailed evaluation results.
- `outputs/model_comparison_50_samples/model_family_comparison.json`: Results in JSON format.
- `outputs/model_comparison_50_samples/model_family_metrics.csv`: Aggregated model metrics.
- `outputs/model_comparison_50_samples/sample_manifest.json`: Selected sample IDs and seed.

## Limitations

- Results are based on 50 samples and may vary with a different sample or seed.
- The 50-sample subset was drawn from the test split and has already been used for model-family comparison; it is not an untouched final holdout. Do not continue tuning against it.
- Input formats differ between models.
- Generation time depends on hardware and runtime conditions.
- ROUGE is not a factuality metric.
- Manual review is needed to assess factual support, speaker attribution, key-event coverage, and summary quality.
- Automated quality checks are screening aids, not human evaluations.

## Quality review guidance

The saved evaluation CSV contains generated summaries and per-example ROUGE scores. Any automated lexical-support, name-mismatch, coverage, or readability checks are screening signals only; they are not human ratings or proof of factual consistency.

Before making claims about summary quality, manually inspect examples from each model, including low-scoring examples. Check whether each statement is supported by the dialogue, speakers are attributed correctly, key events are retained, the summary avoids repetition, and the requested format is followed. This guidance describes a review still needed; it does not claim that a complete manual evaluation has been performed.

## Reproducibility

From the project root, with the project virtual environment active:

```powershell
python -m evaluation.run_model_family_comparison_50 --samples 50 --seed 42
```

The run writes outputs to `outputs/model_comparison_50_samples/`.
