from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT
    / "outputs"
    / "evaluation"
    / "prompt_evaluation.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "outputs"
    / "evaluation"
    / "prompt_strategy_comparison.csv"
)

SCORE_COLUMNS = [
    "relevance_score",
    "coverage_score",
    "factual_consistency_score",
    "output_reliability_score",
]


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Evaluation file not found: {INPUT_FILE}"
        )

    df = pd.read_csv(INPUT_FILE)

    required_columns = [
        "prompt_strategy",
        "generation_seconds",
        "output_nonempty",
        *SCORE_COLUMNS,
    ]

    missing = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing columns: {missing}"
        )

    # Ensure evaluation scores are numeric.
    for column in SCORE_COLUMNS:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce",
        )

    # Do not calculate averages if scores are missing.
    missing_scores = df[SCORE_COLUMNS].isna().sum()

    if missing_scores.any():
        print("Some evaluation scores are missing:")
        print(missing_scores[missing_scores > 0])
        raise ValueError(
            "Complete all four scores for every row before "
            "calculating the final comparison."
        )

    # Check that all scores fall within the 1-5 scale.
    invalid_scores = (
        (df[SCORE_COLUMNS] < 1)
        | (df[SCORE_COLUMNS] > 5)
    )

    if invalid_scores.any().any():
        raise ValueError(
            "Scores must be between 1 and 5."
        )

    df["generation_seconds"] = pd.to_numeric(
        df["generation_seconds"],
        errors="coerce",
    )

    comparison = (
        df.groupby("prompt_strategy")
        .agg(
            sample_count=("sample_id", "count"),
            average_relevance=(
                "relevance_score",
                "mean",
            ),
            average_coverage=(
                "coverage_score",
                "mean",
            ),
            average_factual_consistency=(
                "factual_consistency_score",
                "mean",
            ),
            average_output_reliability=(
                "output_reliability_score",
                "mean",
            ),
            average_generation_seconds=(
                "generation_seconds",
                "mean",
            ),
            nonempty_outputs=(
                "output_nonempty",
                lambda values: (
                    values.astype(str)
                    .str.strip()
                    .str.lower()
                    .eq("true")
                    .sum()
                ),
            ),
        )
        .round(2)
        .reset_index()
    )

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    comparison.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8",
    )

    print("\nPROMPT STRATEGY COMPARISON")
    print("=" * 70)
    print(comparison.to_string(index=False))
    print(f"\nSaved comparison to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
