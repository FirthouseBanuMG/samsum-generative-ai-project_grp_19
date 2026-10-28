
"""Run a reproducible SAMSum model-family comparison."""

import argparse
import gc
import json

import pandas as pd
import torch
from rouge_score import rouge_scorer

from evaluation.run_model_family_comparison import (
    MODEL_CONFIGS,
    generate_summary,
    load_model,
)
from project_paths import PROJECT_ROOT

TEST_FILE = PROJECT_ROOT / "data" / "processed" / "samsum-test-processed.csv"
PILOT_IDS = {"13818513", "13681000", "13728094"}
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "model_comparison_50_samples"


def select_samples(sample_size: int, seed: int = 42) -> list[dict]:
    """Select unique examples from the test split, excluding pilot IDs."""
    df = pd.read_csv(TEST_FILE, dtype={"id": str})
    df = df.dropna(subset=["id", "dialogue", "summary"]).copy()
    df["id"] = df["id"].astype(str)

    df = df[~df["id"].isin(PILOT_IDS)]
    df = df.drop_duplicates(subset=["id"])

    if len(df) < sample_size:
        raise ValueError(
            f"Requested {sample_size} samples, but only {len(df)} are available."
        )

    selected = df.sample(n=sample_size, random_state=seed)

    return [
        {
            "sample_id": row["id"],
            "dialogue": row["dialogue"],
            "reference_summary": row["summary"],
        }
        for _, row in selected.iterrows()
    ]


def build_sample_manifest(samples: list[dict], seed: int = 42) -> dict:
    """Create the reproducibility record for a selected sample set."""
    return {
        "seed": seed,
        "sample_count": len(samples),
        "dataset": TEST_FILE.relative_to(PROJECT_ROOT).as_posix(),
        "excluded_pilot_ids": sorted(PILOT_IDS),
        "sample_ids": [sample["sample_id"] for sample in samples],
    }


def calculate_metrics(results: list[dict]) -> list[dict]:
    """Calculate per-model ROUGE and generation-time metrics."""
    scorer = rouge_scorer.RougeScorer(
        ["rouge1", "rouge2", "rougeL"],
        use_stemmer=True,
    )

    for row in results:
        scores = scorer.score(
            row["reference_summary"],
            row["generated_summary"],
        )
        row["rouge1_f1"] = scores["rouge1"].fmeasure
        row["rouge2_f1"] = scores["rouge2"].fmeasure
        row["rougeL_f1"] = scores["rougeL"].fmeasure

    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=5)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    if args.samples < 1 or args.samples > 50:
        raise ValueError("--samples must be between 1 and 50.")

    samples = select_samples(args.samples, args.seed)
    results = []

    print(f"Selected {len(samples)} test samples.")
    print(f"Device: {'CUDA' if torch.cuda.is_available() else 'CPU'}")
    print(f"Output directory: {OUTPUT_DIR}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    manifest = build_sample_manifest(samples, args.seed)
    (OUTPUT_DIR / "sample_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )

    for config in MODEL_CONFIGS:
        print(f"\nLoading {config['model_name']}...")
        tokenizer, model = load_model(config)

        try:
            for index, sample in enumerate(samples, start=1):
                summary, elapsed = generate_summary(
                    model,
                    tokenizer,
                    sample["dialogue"],
                    config,
                )

                results.append({
                    "sample_id": sample["sample_id"],
                    "model_name": config["model_name"],
                    "model_family": config["family"],
                    "input_format": config["input_format"],
                    "reference_summary": sample["reference_summary"],
                    "generated_summary": summary,
                    "generation_seconds": round(elapsed, 3),
                    "max_new_tokens": 100,
                    "do_sample": False,
                    "num_beams": 1,
                })

                print(
                    f"[{index}/{len(samples)}] "
                    f"{sample['sample_id']} | {elapsed:.2f}s"
                )

                # Save progress after every generation.
                pd.DataFrame(results).to_csv(
                    OUTPUT_DIR / "generations_in_progress.csv",
                    index=False,
                    encoding="utf-8",
                )
        finally:
            del model, tokenizer
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()

    expected = len(samples) * len(MODEL_CONFIGS)
    if len(results) != expected:
        raise RuntimeError(
            f"Expected {expected} generations, got {len(results)}."
        )

    results = calculate_metrics(results)
    results_df = pd.DataFrame(results)

    results_df.to_csv(
        OUTPUT_DIR / "model_family_comparison.csv",
        index=False,
        encoding="utf-8",
    )
    results_df.to_json(
        OUTPUT_DIR / "model_family_comparison.json",
        orient="records",
        indent=2,
        force_ascii=False,
    )

    summary_df = (
        results_df.groupby("model_name", as_index=False)
        .agg(
            sample_count=("sample_id", "nunique"),
            rouge1_f1=("rouge1_f1", "mean"),
            rouge2_f1=("rouge2_f1", "mean"),
            rougeL_f1=("rougeL_f1", "mean"),
            avg_generation_seconds=("generation_seconds", "mean"),
        )
    )
    summary_df.to_csv(
        OUTPUT_DIR / "model_family_metrics.csv",
        index=False,
        encoding="utf-8",
    )

    print("\nEvaluation complete.")
    print(f"Total generations: {len(results)}")
    print(summary_df.to_string(index=False))
    print(f"\nResults saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
