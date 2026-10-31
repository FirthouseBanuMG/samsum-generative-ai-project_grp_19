
"""Evaluate configured models on a seeded sample from the processed test split.

Run with ``python -m evaluation.run_model_family_comparison_50``; saves a sample
manifest, generations, ROUGE metrics, and aggregate results.
"""

import argparse
import gc
import json
from pathlib import Path

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
FINAL_EVALUATION_DIR = PROJECT_ROOT / "outputs" / "final_evaluation"


def select_samples(
    sample_size: int,
    seed: int = 42,
    excluded_ids: set[str] | None = None,
) -> list[dict]:
    """Select test examples excluding pilot and previously evaluated IDs."""
    df = pd.read_csv(TEST_FILE, dtype={"id": str})
    df = df.dropna(subset=["id", "dialogue", "summary"]).copy()
    df["id"] = df["id"].astype(str)

    excluded = PILOT_IDS | (excluded_ids or set())
    df = df[~df["id"].isin(excluded)]
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


def build_sample_manifest(
    samples: list[dict],
    seed: int = 42,
    excluded_ids: set[str] | None = None,
) -> dict:
    """Create the reproducibility record for a selected sample set."""
    manifest = {
        "seed": seed,
        "sample_count": len(samples),
        "dataset": TEST_FILE.relative_to(PROJECT_ROOT).as_posix(),
        "excluded_pilot_ids": sorted(PILOT_IDS),
        "sample_ids": [sample["sample_id"] for sample in samples],
    }
    if excluded_ids:
        manifest["excluded_prior_evaluation_ids"] = sorted(excluded_ids)
    return manifest


def load_excluded_ids(manifest_path: Path) -> set[str]:
    """Load sample IDs from a previous evaluation manifest."""
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected_dataset = TEST_FILE.relative_to(PROJECT_ROOT).as_posix()
    manifest_dataset = manifest.get("dataset")
    if not isinstance(manifest_dataset, str) or (
        manifest_dataset.replace("\\", "/") != expected_dataset
    ):
        raise ValueError(
            f"Manifest dataset must be {expected_dataset!r}: {manifest_path}"
        )
    sample_ids = manifest.get("sample_ids")
    if not isinstance(sample_ids, list) or not all(
        isinstance(sample_id, (str, int)) for sample_id in sample_ids
    ):
        raise ValueError(
            f"Evaluation manifest has no valid sample_ids list: {manifest_path}"
        )
    return {str(sample_id) for sample_id in sample_ids}


def create_human_review_templates(results: list[dict], output_dir: Path) -> None:
    """Write two independent blinded review CSVs and a separate model key."""
    model_names = sorted({row["model_name"] for row in results})
    aliases = {
        model_name: f"Model {chr(ord('A') + index)}"
        for index, model_name in enumerate(model_names)
    }
    review_rows = [
        {
            "sample_id": row["sample_id"],
            "blind_model": aliases[row["model_name"]],
            "dialogue": row["dialogue"],
            "generated_summary": row["generated_summary"],
            "factual_support_1_to_5": "",
            "key_event_coverage_1_to_5": "",
            "speaker_attribution_1_to_5": "",
            "reviewer_notes": "",
        }
        for row in results
    ]
    review = pd.DataFrame(review_rows).sample(
        frac=1,
        random_state=42,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    review.to_csv(
        output_dir / "human_review_reviewer_1.csv",
        index=False,
        encoding="utf-8",
    )
    review.to_csv(
        output_dir / "human_review_reviewer_2.csv",
        index=False,
        encoding="utf-8",
    )
    review_key = {alias: model_name for model_name, alias in aliases.items()}
    (output_dir / "review_key.json").write_text(
        json.dumps(review_key, indent=2),
        encoding="utf-8",
    )


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
    parser.add_argument(
        "--exclude-manifest",
        type=Path,
        help="Exclude sample IDs in this earlier evaluation manifest.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Output directory (reserved evaluation defaults to a new folder).",
    )
    args = parser.parse_args()

    if args.samples < 1 or args.samples > 50:
        raise ValueError("--samples must be between 1 and 50.")

    excluded_ids = (
        load_excluded_ids(args.exclude_manifest)
        if args.exclude_manifest is not None
        else set()
    )
    if args.exclude_manifest is not None and args.output_dir is None:
        output_dir = FINAL_EVALUATION_DIR
    else:
        output_dir = args.output_dir or OUTPUT_DIR
    if output_dir.resolve() == OUTPUT_DIR.resolve() and args.exclude_manifest:
        raise ValueError(
            "Choose a separate --output-dir for runs that exclude a prior manifest."
        )
    if args.exclude_manifest and output_dir.exists() and any(output_dir.iterdir()):
        raise FileExistsError(
            f"Reserved evaluation output directory is not empty: {output_dir}. "
            "Choose a new --output-dir to preserve prior results."
        )

    samples = select_samples(args.samples, args.seed, excluded_ids)
    results = []

    print(f"Selected {len(samples)} test samples.")
    if excluded_ids:
        print(f"Excluded {len(excluded_ids)} IDs from the earlier manifest.")
    print(f"Device: {'CUDA' if torch.cuda.is_available() else 'CPU'}")
    print(f"Output directory: {output_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)

    manifest = build_sample_manifest(samples, args.seed, excluded_ids)
    (output_dir / "sample_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )

    for config in MODEL_CONFIGS:
        print(f"\nLoading {config['model_name']}...")
        tokenizer, model = load_model(config)

        try:
            for index, sample in enumerate(samples, start=1):
                (
                    summary,
                    elapsed,
                    input_token_count,
                    input_truncated,
                ) = generate_summary(
                    model,
                    tokenizer,
                    sample["dialogue"],
                    config,
                )

                results.append({
                    "sample_id": sample["sample_id"],
                    "dialogue": sample["dialogue"],
                    "model_name": config["model_name"],
                    "model_family": config["family"],
                    "input_format": config["input_format"],
                    "reference_summary": sample["reference_summary"],
                    "generated_summary": summary,
                    "generation_seconds": round(elapsed, 3),
                    "input_token_count_before_truncation": input_token_count,
                    "input_truncated": input_truncated,
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
                    output_dir / "generations_in_progress.csv",
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
        output_dir / "model_family_comparison.csv",
        index=False,
        encoding="utf-8",
    )
    results_df.to_json(
        output_dir / "model_family_comparison.json",
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
        output_dir / "model_family_metrics.csv",
        index=False,
        encoding="utf-8",
    )
    if args.exclude_manifest is not None:
        create_human_review_templates(results, output_dir)

    print("\nEvaluation complete.")
    print(f"Total generations: {len(results)}")
    print(summary_df.to_string(index=False))
    print(f"\nResults saved to: {output_dir}")
    if args.exclude_manifest is not None:
        print("Blinded human-review templates and separate review key were created.")


if __name__ == "__main__":
    main()
