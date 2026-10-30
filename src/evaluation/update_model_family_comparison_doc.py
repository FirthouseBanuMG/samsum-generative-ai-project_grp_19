
"""Generate the archived Word model-comparison report from saved results.

Run with ``python -m evaluation.update_model_family_comparison_doc`` after the
50-sample result files are available.
"""

from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT

from project_paths import PROJECT_ROOT

ROOT = PROJECT_ROOT
OUT = (
    ROOT / "documents" / "Implementation_and_Experiments"
    / "Model_Family_Comparison"
    / "model_family_comparison_report_updated.docx"
)

def set_cell(cell, value):
    cell.text = str(value)
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER

def main():
    doc = Document()
    section = doc.sections[0]
    section.top_margin = Inches(0.7)
    section.bottom_margin = Inches(0.7)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)

    styles = doc.styles
    styles["Normal"].font.name = "Arial"
    styles["Normal"].font.size = Pt(10)
    styles["Title"].font.name = "Arial"
    styles["Title"].font.size = Pt(20)

    title = doc.add_heading("Model-Family Comparison and Evaluation", 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run(
        "Project: SAMSum-Based Intelligent Conversation Summarization "
        "and Action-Item Extraction"
    ).italic = True

    doc.add_heading("Executive Summary", level=1)
    doc.add_paragraph(
        "Three pretrained models were evaluated on the same 50 unique "
        "SAMSum test-split dialogues, producing 150 generated summaries. "
        "FLAN-T5-base achieved the highest mean ROUGE-1, ROUGE-2, and "
        "ROUGE-L F1 scores and the lowest mean generation time in this "
        "recorded CPU experiment. These results describe the tested "
        "model-and-input configurations and do not establish universal "
        "model superiority."
    )

    doc.add_heading("1. Objective and Scope", level=1)
    doc.add_paragraph(
        "The experiment compares Qwen/Qwen2.5-1.5B-Instruct, "
        "google/flan-t5-base, and sshleifer/distilbart-cnn-12-6 for "
        "dialogue summarization. The evaluation uses 50 unique samples "
        "selected from data/processed/samsum-test-processed.csv with "
        "random seed 42. The three pilot IDs (13818513, 13681000, "
        "13728094) are excluded from sample selection. Each model "
        "generates one summary for each selected dialogue."
    )

    doc.add_heading("2. Methodology", level=1)
    doc.add_paragraph(
        "The runner is src/run_model_family_comparison_50.py. It selects "
        "50 test-split samples reproducibly, saves the selected IDs in "
        "sample_manifest.json, and records each generation to the "
        "evaluation output directory. The recorded run used CPU inference, "
        "a maximum input length of 1,024 tokens, max_new_tokens=100, "
        "do_sample=False, and num_beams=1. ROUGE-1, ROUGE-2, and ROUGE-L "
        "F1 were calculated using rouge_score with stemming."
    )
    doc.add_paragraph(
        "Input formatting differs by model: Qwen uses the constraint_based "
        "prompt, FLAN-T5 uses the constraint_based prompt, and DistilBART "
        "receives dialogue_only input. Because prompt formats and model "
        "families differ, this is a comparison of tested configurations, "
        "not a controlled isolation of architecture alone."
    )

    doc.add_heading("3. Quantitative Results", level=1)
    table = doc.add_table(rows=1, cols=6)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Light Shading Accent 1"
    headers = [
        "Model", "Samples", "ROUGE-1 F1", "ROUGE-2 F1",
        "ROUGE-L F1", "Mean sec/sample"
    ]
    for cell, value in zip(table.rows[0].cells, headers):
        set_cell(cell, value)

    results = [
        ("Qwen/Qwen2.5-1.5B-Instruct", 50, 0.220521, 0.072396, 0.158634, 21.68958),
        ("google/flan-t5-base", 50, 0.514008, 0.248225, 0.429139, 0.63586),
        ("sshleifer/distilbart-cnn-12-6", 50, 0.265467, 0.098079, 0.199712, 1.38020),
    ]
    for model, count, r1, r2, rl, seconds in results:
        row = table.add_row().cells
        values = [
            model, count, f"{r1:.6f}", f"{r2:.6f}",
            f"{rl:.6f}", f"{seconds:.5f}"
        ]
        for cell, value in zip(row, values):
            set_cell(cell, value)

    doc.add_paragraph(
        "Interpretation: FLAN-T5-base led on all three ROUGE metrics and "
        "had the lowest mean generation time. DistilBART was slower than "
        "FLAN-T5 in this run and had lower ROUGE scores. Qwen had the "
        "highest mean generation time. ROUGE measures lexical overlap "
        "with reference summaries; it is not a direct factuality measure."
    )

    doc.add_heading("4. Quality Review and Failure Analysis", level=1)
    doc.add_paragraph(
        "The main evaluation CSV contains the generated summaries and "
        "per-example ROUGE scores. Automated lexical-support, name-mismatch, "
        "coverage, or readability heuristics should be treated as screening "
        "signals only, not as verified human ratings or proof of factual "
        "consistency. A low ROUGE score may indicate omitted key information "
        "or a paraphrase with low lexical overlap; manual review is needed "
        "to distinguish these cases."
    )
    doc.add_paragraph(
        "Before final submission, manually inspect a representative set of "
        "summaries, including low-scoring examples and outputs from each "
        "model. Check factual support against the dialogue, speaker "
        "attribution, preservation of key events, repetition, and whether "
        "the output follows the intended summary format."
    )

    doc.add_heading("5. Conclusion", level=1)
    doc.add_paragraph(
        "Among the three tested configurations, FLAN-T5-base is the "
        "strongest preliminary choice based on the measured ROUGE scores "
        "and mean generation time. The conclusion is limited to this "
        "50-sample evaluation, this CPU environment, and the tested input "
        "formats. Further human evaluation is needed before making strong "
        "claims about factual consistency or overall summary quality."
    )

    doc.add_heading("6. Limitations and Reproducibility", level=1)
    limitations = [
        "The evaluation contains 50 samples; results may vary with a different sample or seed.",
        "The model input formats are not identical, so the experiment does not isolate architecture as the only variable.",
        "Generation times depend on hardware, software versions, model loading, and runtime conditions.",
        "ROUGE does not directly measure factual consistency, speaker attribution, or usefulness.",
        "The manifest and raw CSV should be retained so the evaluation can be reproduced and audited.",
    ]
    for item in limitations:
        doc.add_paragraph(item, style="List Bullet")

    doc.add_heading("7. Output Files", level=1)
    for item in [
        "outputs/model_comparison_50_samples/model_family_comparison.csv",
        "outputs/model_comparison_50_samples/model_family_comparison.json",
        "outputs/model_comparison_50_samples/model_family_metrics.csv",
        "outputs/model_comparison_50_samples/sample_manifest.json",
        "src/run_model_family_comparison_50.py",
    ]:
        doc.add_paragraph(item, style="List Bullet")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(OUT)
    print(f"Created: {OUT}")

if __name__ == "__main__":
    main()
