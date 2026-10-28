import json
import time
from pathlib import Path

import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

from project_paths import PROJECT_ROOT
from prompting.prompts import PROMPT_FUNCTIONS, build_prompt


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"

BASELINE_FILE = (
    PROJECT_ROOT
    / "outputs"
    / "baseline_smoke_test"
    / "baseline_outputs.json"
)

OUTPUT_DIR = PROJECT_ROOT / "outputs" / "prompt_experiments"

MAX_NEW_TOKENS = 100

# Use greedy decoding to keep the decoding settings
# consistent across all four prompt strategies.
DO_SAMPLE = False


# --------------------------------------------------
# LOAD EXISTING BASELINE EXAMPLES
# --------------------------------------------------

def load_baseline_examples(file_path):

    if not file_path.exists():
        raise FileNotFoundError(
            f"Baseline file not found: {file_path}"
        )

    with file_path.open("r", encoding="utf-8") as file:
        records = json.load(file)

    if not isinstance(records, list) or not records:
        raise ValueError(
            "Baseline JSON must contain a non-empty list."
        )

    required_fields = {
        "sample_id",
        "dialogue",
        "reference_summary",
    }

    for index, record in enumerate(records):

        missing = required_fields - set(record.keys())

        if missing:
            raise ValueError(
                f"Record {index} is missing fields: {sorted(missing)}"
            )

    return records


# --------------------------------------------------
# LOAD THE MODEL
# --------------------------------------------------

def load_model():

    print("\nLoading tokenizer...")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    print("Loading model on CPU...")

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype=torch.float32,
        low_cpu_mem_usage=True,
    )

    model.eval()

    print("Model loaded successfully.")

    return tokenizer, model


# --------------------------------------------------
# GENERATE ONE SUMMARY
# --------------------------------------------------

def generate_summary(dialogue, strategy, tokenizer, model):

    prompt_text = build_prompt(strategy, dialogue)

    messages = [
        {
            "role": "system",
            "content": (
                "You are a conversation summarization assistant. "
                "Follow the user's instructions accurately."
            ),
        },
        {
            "role": "user",
            "content": prompt_text,
        },
    ]

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
    )

    generation_start = time.time()

    with torch.inference_mode():

        output_ids = model.generate(
            **inputs,
            max_new_tokens=MAX_NEW_TOKENS,
            do_sample=DO_SAMPLE,
            pad_token_id=tokenizer.eos_token_id,
        )

    generation_seconds = time.time() - generation_start

    # Decode only newly generated tokens.
    new_tokens = output_ids[
        0,
        inputs["input_ids"].shape[1]:
    ]

    generated_summary = tokenizer.decode(
        new_tokens,
        skip_special_tokens=True,
    ).strip()

    return prompt, generated_summary, generation_seconds


# --------------------------------------------------
# RUN THE FOUR PROMPT EXPERIMENTS
# --------------------------------------------------

def main():

    print("=" * 60)
    print("SAMSum PROMPT COMPARISON EXPERIMENT")
    print("=" * 60)

    records = load_baseline_examples(BASELINE_FILE)

    print(f"Baseline examples loaded: {len(records)}")
    print(f"Prompt strategies: {len(PROMPT_FUNCTIONS)}")
    print(
        "Expected generations: "
        f"{len(records) * len(PROMPT_FUNCTIONS)}"
    )

    tokenizer, model = load_model()

    results = []

    total_start = time.time()

    for record in records:

        sample_id = str(record["sample_id"])
        dialogue = str(record["dialogue"])
        reference_summary = str(record["reference_summary"])

        for strategy in PROMPT_FUNCTIONS:

            print("\n" + "-" * 60)
            print(f"Sample ID: {sample_id}")
            print(f"Prompt strategy: {strategy}")

            prompt, generated_summary, generation_seconds = (
                generate_summary(
                    dialogue=dialogue,
                    strategy=strategy,
                    tokenizer=tokenizer,
                    model=model,
                )
            )

            print("Generated summary:")
            print(generated_summary)
            print(
                f"Generation time: {generation_seconds:.2f} seconds"
            )

            results.append(
                {
                    "sample_id": sample_id,
                    "prompt_strategy": strategy,
                    "dialogue": dialogue,
                    "reference_summary": reference_summary,
                    "generated_summary": generated_summary,
                    "summary_word_count": len(
                        generated_summary.split()
                    ),
                    "output_nonempty": bool(
                        generated_summary.strip()
                    ),
                    "generation_seconds": round(
                        generation_seconds, 3
                    ),
                    "rendered_prompt": prompt,
                    "decoding_strategy": "greedy",
                    "max_new_tokens": MAX_NEW_TOKENS,
                    "model_name": MODEL_NAME,
                }
            )

    total_seconds = time.time() - total_start

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    csv_path = OUTPUT_DIR / "prompt_comparison.csv"
    json_path = OUTPUT_DIR / "prompt_comparison.json"

    df = pd.DataFrame(results)

    df.to_csv(
        csv_path,
        index=False,
        encoding="utf-8",
    )

    json_path.write_text(
        json.dumps(
            results,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    print("\n" + "=" * 60)
    print("PROMPT EXPERIMENT COMPLETE")
    print("=" * 60)

    print(f"Total generated summaries: {len(results)}")
    print(f"Total experiment time: {total_seconds:.2f} seconds")
    print(f"CSV results: {csv_path}")
    print(f"JSON results: {json_path}")

    print("\nSummary counts by prompt strategy:")

    print(
        df.groupby("prompt_strategy").agg(
            number_of_summaries=("sample_id", "count"),
            nonempty_outputs=("output_nonempty", "sum"),
            average_generation_seconds=(
                "generation_seconds",
                "mean",
            ),
        ).round(2).to_string()
    )


if __name__ == "__main__":
    main()
