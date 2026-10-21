"""
Decoding comparison experiment (E3) for the SAMSum project.

Holds the prompt strategy and samples fixed and varies only the decoding
settings, comparing greedy decoding against sampling configurations that
use temperature together with top-p or top-k. Sampling configurations are
run several times with recorded seeds so output variability can be
measured (repeatability vs diversity).

Outputs:
  outputs/decoding_experiments/decoding_comparison.{csv,json}
  outputs/decoding_experiments/decoding_variability_summary.csv
"""

import json
import time
from itertools import combinations
from pathlib import Path

import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

from prompts import build_prompt


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"

BASELINE_FILE = (
    PROJECT_ROOT
    / "outputs"
    / "baseline_smoke_test"
    / "baseline_outputs.json"
)

OUTPUT_DIR = PROJECT_ROOT / "outputs" / "decoding_experiments"

# Fixed factors: one prompt strategy and a fixed generation length so the
# only variable across runs is the decoding configuration.
PROMPT_STRATEGY = "constraint_based"
MAX_NEW_TOKENS = 100

# Seeds used for repeated sampling runs (also fixes the number of repeats).
SAMPLING_SEEDS = [11, 22, 33]

SYSTEM_PROMPT = (
    "You are a conversation summarization assistant. "
    "Follow the user's instructions accurately."
)

# Decoding configurations. Greedy is deterministic (one run); the sampling
# configurations cover temperature with top-p and with top-k.
DECODING_CONFIGS = [
    {
        "name": "greedy",
        "params": {"do_sample": False},
        "is_sampling": False,
    },
    {
        "name": "sampling_temp_low",
        "params": {"do_sample": True, "temperature": 0.3, "top_p": 0.9},
        "is_sampling": True,
    },
    {
        "name": "sampling_temp_high",
        "params": {"do_sample": True, "temperature": 1.0, "top_p": 0.9},
        "is_sampling": True,
    },
    {
        "name": "sampling_topk",
        "params": {"do_sample": True, "temperature": 0.8, "top_k": 50},
        "is_sampling": True,
    },
]


# --------------------------------------------------
# LOAD EXISTING BASELINE EXAMPLES
# --------------------------------------------------

def load_baseline_examples(file_path):

    if not file_path.exists():
        raise FileNotFoundError(f"Baseline file not found: {file_path}")

    with file_path.open("r", encoding="utf-8") as file:
        records = json.load(file)

    if not isinstance(records, list) or not records:
        raise ValueError("Baseline JSON must contain a non-empty list.")

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
# GENERATION
# --------------------------------------------------

def generate_once(dialogue, params, tokenizer, model, seed=None):
    """Generate a single summary with the given decoding parameters.

    When a seed is provided it is set before generation so sampling runs
    are reproducible.
    """

    prompt_text = build_prompt(PROMPT_STRATEGY, dialogue)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt_text},
    ]

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )
    inputs = tokenizer(prompt, return_tensors="pt")

    if seed is not None:
        torch.manual_seed(seed)

    start = time.time()
    with torch.inference_mode():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=MAX_NEW_TOKENS,
            pad_token_id=tokenizer.eos_token_id,
            **params,
        )
    generation_seconds = time.time() - start

    new_tokens = output_ids[0, inputs["input_ids"].shape[1]:]
    summary = tokenizer.decode(new_tokens, skip_special_tokens=True).strip()

    return summary, generation_seconds


# --------------------------------------------------
# VARIABILITY METRIC
# --------------------------------------------------

def word_overlap(text_a, text_b):
    """Jaccard overlap of the word sets of two summaries."""

    set_a = set(text_a.lower().split())
    set_b = set(text_b.lower().split())

    if not set_a and not set_b:
        return 1.0

    union = set_a | set_b
    return len(set_a & set_b) / len(union) if union else 0.0


def mean_pairwise_overlap(summaries):
    """Mean Jaccard word overlap across all pairs of summaries."""

    pairs = list(combinations(summaries, 2))
    if not pairs:
        return 1.0
    return sum(word_overlap(a, b) for a, b in pairs) / len(pairs)


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():

    print("=" * 60)
    print("SAMSum DECODING COMPARISON EXPERIMENT (E3)")
    print("=" * 60)

    records = load_baseline_examples(BASELINE_FILE)
    print(f"Baseline examples loaded: {len(records)}")
    print(f"Prompt strategy (fixed): {PROMPT_STRATEGY}")

    tokenizer, model = load_model()

    results = []
    total_start = time.time()

    for record in records:
        sample_id = str(record["sample_id"])
        dialogue = str(record["dialogue"])

        for config in DECODING_CONFIGS:
            # Sampling configs repeat with distinct seeds; greedy runs once.
            seeds = SAMPLING_SEEDS if config["is_sampling"] else [None]

            for repeat_index, seed in enumerate(seeds):
                print("\n" + "-" * 60)
                print(f"Sample {sample_id} | {config['name']} "
                      f"| repeat {repeat_index} | seed {seed}")

                summary, generation_seconds = generate_once(
                    dialogue=dialogue,
                    params=config["params"],
                    tokenizer=tokenizer,
                    model=model,
                    seed=seed,
                )

                print(summary)
                print(f"Generation time: {generation_seconds:.2f}s")

                results.append({
                    "sample_id": sample_id,
                    "decoding_config": config["name"],
                    "params_json": json.dumps(config["params"]),
                    "repeat_index": repeat_index,
                    "seed": seed,
                    "generated_summary": summary,
                    "summary_word_count": len(summary.split()),
                    "generation_seconds": round(generation_seconds, 3),
                    "model_name": MODEL_NAME,
                    "max_new_tokens": MAX_NEW_TOKENS,
                    "prompt_strategy": PROMPT_STRATEGY,
                })

    total_seconds = time.time() - total_start

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(results)
    csv_path = OUTPUT_DIR / "decoding_comparison.csv"
    json_path = OUTPUT_DIR / "decoding_comparison.json"
    df.to_csv(csv_path, index=False, encoding="utf-8")
    json_path.write_text(
        json.dumps(results, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    # Variability summary per (sample, decoding_config).
    variability_rows = []
    for (sample_id, config_name), group in df.groupby(
        ["sample_id", "decoding_config"]
    ):
        summaries = group["generated_summary"].tolist()
        variability_rows.append({
            "sample_id": sample_id,
            "decoding_config": config_name,
            "num_runs": len(summaries),
            "distinct_outputs": len(set(summaries)),
            "mean_pairwise_word_overlap": round(
                mean_pairwise_overlap(summaries), 3
            ),
            "mean_generation_seconds": round(
                group["generation_seconds"].mean(), 2
            ),
        })

    variability_df = pd.DataFrame(variability_rows)
    variability_path = OUTPUT_DIR / "decoding_variability_summary.csv"
    variability_df.to_csv(variability_path, index=False, encoding="utf-8")

    print("\n" + "=" * 60)
    print("DECODING EXPERIMENT COMPLETE")
    print("=" * 60)
    print(f"Total generations: {len(results)}")
    print(f"Total experiment time: {total_seconds:.2f} seconds")
    print(f"CSV results: {csv_path}")
    print(f"Variability summary: {variability_path}")
    print("\n" + variability_df.to_string(index=False))


if __name__ == "__main__":
    main()
