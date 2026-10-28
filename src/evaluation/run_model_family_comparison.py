
"""
Model-family comparison experiment for the SAMSum project.

Inference is intended to run in Google Colab with a GPU.
Uses the same three baseline dialogues and reference summaries.

Outputs:
  outputs/model_comparison/model_family_comparison.csv
  outputs/model_comparison/model_family_comparison.json
"""

import json
import time
from pathlib import Path

import pandas as pd

from project_paths import PROJECT_ROOT
from prompting.prompts import build_prompt


BASELINE_FILE = (
    PROJECT_ROOT
    / "outputs"
    / "baseline_smoke_test"
    / "baseline_outputs.json"
)

OUTPUT_DIR = PROJECT_ROOT / "outputs" / "model_comparison"
MAX_INPUT_TOKENS = 1024
MAX_NEW_TOKENS = 100

MODEL_CONFIGS = [
    {
        "model_name": "Qwen/Qwen2.5-1.5B-Instruct",
        "family": "causal_lm",
        "input_format": "constraint_based",
    },
    {
        "model_name": "google/flan-t5-base",
        "family": "seq2seq_instruction",
        "input_format": "constraint_based",
    },
    {
        "model_name": "sshleifer/distilbart-cnn-12-6",
        "family": "seq2seq_summarization",
        "input_format": "dialogue_only",
    },
]


def load_samples(path=BASELINE_FILE):
    """Load and validate the existing baseline samples."""
    if not path.exists():
        raise FileNotFoundError(f"Baseline file not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        records = json.load(file)

    if not isinstance(records, list) or not records:
        raise ValueError("Baseline JSON must contain a non-empty list.")

    required = {
        "sample_id",
        "dialogue",
        "reference_summary",
    }

    for index, record in enumerate(records):
        missing = required - record.keys()
        if missing:
            raise ValueError(
                f"Baseline record {index} is missing fields: {sorted(missing)}"
            )
        if not record["dialogue"].strip():
            raise ValueError(f"Empty dialogue in baseline record {index}.")

    return records


def prepare_input(dialogue, input_format):
    """Apply the input format appropriate for each model."""
    if not isinstance(dialogue, str) or not dialogue.strip():
        raise ValueError("Dialogue must be a non-empty string.")

    if input_format == "dialogue_only":
        return dialogue

    if input_format == "constraint_based":
        return build_prompt("constraint_based", dialogue)

    raise ValueError(f"Unsupported input format: {input_format}")


def generate_summary(model, tokenizer, dialogue, config):
    """Generate one summary and return it with the elapsed time."""
    import torch
    prompt = prepare_input(dialogue, config["input_format"])

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=MAX_INPUT_TOKENS,
    ).to(model.device)

    generation_kwargs = {
        "max_new_tokens": MAX_NEW_TOKENS,
        "do_sample": False,
        "num_beams": 1,
    }

    if tokenizer.pad_token_id is not None:
        generation_kwargs["pad_token_id"] = tokenizer.pad_token_id

    if config["family"] == "causal_lm":
        generation_kwargs["eos_token_id"] = tokenizer.eos_token_id

    if torch.cuda.is_available():
        torch.cuda.synchronize()

    start = time.perf_counter()

    with torch.inference_mode():
        output_ids = model.generate(**inputs, **generation_kwargs)

    if torch.cuda.is_available():
        torch.cuda.synchronize()

    elapsed = time.perf_counter() - start

    # Causal language models return the prompt plus generated tokens.
    if config["family"] == "causal_lm":
        prompt_length = inputs["input_ids"].shape[1]
        output_ids = output_ids[:, prompt_length:]

    summary = tokenizer.decode(
        output_ids[0],
        skip_special_tokens=True,
    ).strip()

    return summary, elapsed



def load_model(config):
    """Load a model with its appropriate Transformers architecture."""
    import torch
    from transformers import (
        AutoModelForCausalLM,
        AutoModelForSeq2SeqLM,
        AutoTokenizer,
    )

    tokenizer = AutoTokenizer.from_pretrained(config["model_name"])

    if config["family"] == "causal_lm":
        model_class = AutoModelForCausalLM
    elif config["family"] in {
        "seq2seq_instruction",
        "seq2seq_summarization",
    }:
        model_class = AutoModelForSeq2SeqLM
    else:
        raise ValueError(
            f"Unsupported model family: {config['family']}"
        )

    load_kwargs = {}
    if torch.cuda.is_available():
        load_kwargs["torch_dtype"] = torch.float16
        load_kwargs["device_map"] = "auto"

    model = model_class.from_pretrained(
        config["model_name"],
        **load_kwargs,
    )

    if not torch.cuda.is_available():
        model.to("cpu")

    model.eval()
    return tokenizer, model
   


def run_comparison(samples=None, model_configs=None):
    """Run each configured model on the same baseline samples."""
    import torch
    samples = samples if samples is not None else load_samples()
    model_configs = model_configs if model_configs is not None else MODEL_CONFIGS

    results = []

    for config in model_configs:
        print(f"\nLoading {config['model_name']} ...")
        tokenizer, model = load_model(config)

        try:
            for sample in samples:
                summary, elapsed = generate_summary(
                    model,
                    tokenizer,
                    sample["dialogue"],
                    config,
                )

                row = {
                    "sample_id": str(sample["sample_id"]),
                    "model_name": config["model_name"],
                    "model_family": config["family"],
                    "input_format": config["input_format"],
                    "reference_summary": sample["reference_summary"],
                    "generated_summary": summary,
                    "reference_word_count": len(
                        sample["reference_summary"].split()
                    ),
                    "generated_word_count": len(summary.split()),
                    "generation_seconds": round(elapsed, 3),
                    "max_new_tokens": MAX_NEW_TOKENS,
                    "do_sample": False,
                    "num_beams": 1,
                }
                results.append(row)

                print(
                    f"{sample['sample_id']} | {elapsed:.2f}s | {summary}"
                )
        finally:
            del model, tokenizer
            if torch.cuda.is_available():
                torch.cuda.empty_cache()

    return results


def save_results(results, output_dir=OUTPUT_DIR):
    """Save raw generations in CSV and JSON formats."""
    if not results:
        raise ValueError("No comparison results to save.")

    output_dir.mkdir(parents=True, exist_ok=True)

    csv_path = output_dir / "model_family_comparison.csv"
    json_path = output_dir / "model_family_comparison.json"

    pd.DataFrame(results).to_csv(
        csv_path,
        index=False,
        encoding="utf-8",
    )

    with json_path.open("w", encoding="utf-8") as file:
        json.dump(results, file, indent=2, ensure_ascii=False)

    return csv_path, json_path


if __name__ == "__main__":
    comparison_results = run_comparison()
    csv_file, json_file = save_results(comparison_results)

    print(f"\nSaved CSV: {csv_file}")
    print(f"Saved JSON: {json_file}")
    print(f"Total generations: {len(comparison_results)}")
