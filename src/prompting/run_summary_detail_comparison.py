"""Compare concise and detailed prompts on the fixed baseline training examples.

Run with ``python -m prompting.run_summary_detail_comparison``; saves outputs
and descriptive word-count and ROUGE metrics.
"""

import json
import re
import time
from pathlib import Path

import pandas as pd
import torch
from rouge_score import rouge_scorer
from transformers import AutoModelForCausalLM, AutoTokenizer

from project_paths import PROJECT_ROOT
from prompting.prompts import (
    SUMMARY_DETAIL_PROMPTS,
    build_summary_detail_prompt,
)


MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"
BASELINE_FILE = (
    PROJECT_ROOT
    / "outputs"
    / "baseline_smoke_test"
    / "baseline_outputs.json"
)
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "summary_detail_comparison"
MAX_NEW_TOKENS = 100
SYSTEM_PROMPT = (
    "You are a conversation summarization assistant. "
    "Follow the user's instructions accurately."
)


def load_baseline_examples(file_path: Path = BASELINE_FILE) -> list[dict]:
    """Load and validate the fixed training examples used by this comparison."""
    if not file_path.is_file():
        raise FileNotFoundError(f"Baseline examples not found: {file_path}")

    records = json.loads(file_path.read_text(encoding="utf-8"))
    if not isinstance(records, list) or not records:
        raise ValueError("Baseline examples must be a non-empty JSON list.")

    required = {"sample_id", "dialogue", "reference_summary"}
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            raise ValueError(f"Baseline record {index} must be a JSON object.")
        missing = required - set(record)
        if missing:
            raise ValueError(
                f"Baseline record {index} is missing fields: {sorted(missing)}"
            )
        for field in ("dialogue", "reference_summary"):
            if not isinstance(record[field], str) or not record[field].strip():
                raise ValueError(
                    f"Baseline record {index} has an empty {field}."
                )
    return records


def load_model():
    """Load the same pretrained causal LM used by the prompt experiments."""
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype=torch.float32,
        low_cpu_mem_usage=True,
    )
    model.eval()
    return tokenizer, model


def generate_summary(
    dialogue: str,
    style: str,
    tokenizer,
    model,
) -> tuple[str, str, float]:
    """Generate one greedy summary and return prompt, text, and elapsed time."""
    user_prompt = build_summary_detail_prompt(style, dialogue)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]
    rendered_prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )
    inputs = tokenizer(rendered_prompt, return_tensors="pt")

    start = time.perf_counter()
    with torch.inference_mode():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=MAX_NEW_TOKENS,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )
    elapsed = time.perf_counter() - start

    new_tokens = output_ids[0, inputs["input_ids"].shape[1]:]
    output = tokenizer.decode(new_tokens, skip_special_tokens=True).strip()
    return rendered_prompt, output, elapsed


def calculate_metrics(results: list[dict]) -> list[dict]:
    """Add word/sentence counts and reference-overlap metrics."""
    scorer = rouge_scorer.RougeScorer(
        ["rouge1", "rougeL"],
        use_stemmer=True,
    )
    for row in results:
        scores = scorer.score(
            row["reference_summary"],
            row["generated_summary"],
        )
        row["rouge1_f1"] = scores["rouge1"].fmeasure
        row["rougeL_f1"] = scores["rougeL"].fmeasure
        row["summary_word_count"] = len(row["generated_summary"].split())
        row["summary_sentence_count"] = len(
            [
                sentence
                for sentence in re.split(
                    r"(?<=[.!?])\s+",
                    row["generated_summary"].strip(),
                )
                if sentence
            ]
        )
    return results


def main() -> None:
    records = load_baseline_examples()
    print(f"Fixed dialogue count: {len(records)}")
    print(f"Styles: {', '.join(SUMMARY_DETAIL_PROMPTS)}")
    print(f"Expected generations: {len(records) * len(SUMMARY_DETAIL_PROMPTS)}")
    print("Fixed settings: Qwen2.5-1.5B-Instruct, greedy, max_new_tokens=100")

    tokenizer, model = load_model()
    results = []
    for record in records:
        for style in SUMMARY_DETAIL_PROMPTS:
            print(f"\n{record['sample_id']} | {style}")
            rendered_prompt, output, elapsed = generate_summary(
                dialogue=record["dialogue"],
                style=style,
                tokenizer=tokenizer,
                model=model,
            )
            print(output)
            results.append({
                "sample_id": str(record["sample_id"]),
                "dataset_split": record.get("dataset_split", "train"),
                "summary_style": style,
                "dialogue": record["dialogue"],
                "reference_summary": record["reference_summary"],
                "generated_summary": output,
                "generation_seconds": round(elapsed, 3),
                "rendered_prompt": rendered_prompt,
                "model_name": MODEL_NAME,
                "decoding_strategy": "greedy",
                "max_new_tokens": MAX_NEW_TOKENS,
            })

    calculate_metrics(results)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    details_path = OUTPUT_DIR / "summary_detail_comparison.csv"
    json_path = OUTPUT_DIR / "summary_detail_comparison.json"
    summary_path = OUTPUT_DIR / "summary_detail_metrics.csv"

    frame = pd.DataFrame(results)
    frame.to_csv(details_path, index=False, encoding="utf-8")
    json_path.write_text(
        json.dumps(results, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    summary = (
        frame.groupby("summary_style", sort=False)
        .agg(
            sample_count=("sample_id", "nunique"),
            average_word_count=("summary_word_count", "mean"),
            average_sentence_count=("summary_sentence_count", "mean"),
            average_rouge1_f1=("rouge1_f1", "mean"),
            average_rougeL_f1=("rougeL_f1", "mean"),
            average_generation_seconds=("generation_seconds", "mean"),
        )
        .round(3)
        .reset_index()
    )
    summary.to_csv(summary_path, index=False, encoding="utf-8")

    print("\nSummary comparison (descriptive; n=3):")
    print(summary.to_string(index=False))
    print(f"\nSaved generations: {details_path}")
    print(f"Saved JSON: {json_path}")
    print(f"Saved summary metrics: {summary_path}")


if __name__ == "__main__":
    main()
