# Model Family Comparison

## Purpose
Compare three pretrained models for SAMSum dialogue summarization.

## Models
- Qwen/Qwen2.5-1.5B-Instruct
- google/flan-t5-base
- sshleifer/distilbart-cnn-12-6

## Evaluation Scope
50 dialogue samples were evaluated with three models, producing 150 generated summaries.

## Metrics
- ROUGE-1
- ROUGE-2
- ROUGE-L
- Average generation time

## Main Finding
FLAN-T5-base achieved the highest ROUGE scores in this experiment.
DistilBART had the lowest average generation time.
These results apply to the tested configurations and do not establish
universal model superiority.

## Files
- model_family_comparison_report.docx: Report section with methodology,
  results, failure analysis, conclusion, and limitations.
- model_family_evaluation_50_samples.xlsx: Detailed evaluation workbook.

## Limitations
The models used different input formats. The 50-sample evaluation
contains three previously selected training examples and 47 additional
test samples. Automated quality indicators are screening aids, not
verified human ratings.

## Implementation
The experiment runner is maintained in:
src/run_model_family_comparison.py

Experiment outputs are maintained under:
outputs/model_comparison/
