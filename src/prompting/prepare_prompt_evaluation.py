import pandas as pd
from pathlib import Path


# Project paths
from project_paths import PROJECT_ROOT

INPUT_FILE = (
    PROJECT_ROOT
    / "outputs"
    / "prompt_experiments"
    / "prompt_comparison.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "outputs"
    / "evaluation"
    / "prompt_evaluation.csv"
)


def main():

    # Check that the experiment results exist
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Experiment CSV not found: {INPUT_FILE}"
        )

    # Load the existing experiment results
    df = pd.read_csv(INPUT_FILE)

    if df.empty:
        raise ValueError(
            "The prompt experiment CSV contains no records."
        )

    required_columns = [
        "sample_id",
        "prompt_strategy",
        "dialogue",
        "reference_summary",
        "generated_summary",
        "generation_seconds",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # Check for duplicate experiment records
    if df.duplicated(
        subset=["sample_id", "prompt_strategy"]
    ).any():
        raise ValueError(
            "Duplicate sample_id and prompt_strategy records found."
        )

    # Create the evaluation template
    evaluation_df = df[
        [
            "sample_id",
            "prompt_strategy",
            "dialogue",
            "reference_summary",
            "generated_summary",
            "generation_seconds",
        ]
    ].copy()

    # Calculate basic output information
    evaluation_df["summary_word_count"] = (
        evaluation_df["generated_summary"]
        .fillna("")
        .astype(str)
        .str.split()
        .str.len()
    )

    evaluation_df["output_nonempty"] = (
        evaluation_df["generated_summary"]
        .fillna("")
        .astype(str)
        .str.strip()
        .ne("")
    )

    # Columns for manual evaluation
    evaluation_df["relevance_score"] = pd.NA
    evaluation_df["coverage_score"] = pd.NA
    evaluation_df["factual_consistency_score"] = pd.NA
    evaluation_df["output_reliability_score"] = pd.NA

    evaluation_df["unsupported_claims"] = ""
    evaluation_df["missing_information"] = ""
    evaluation_df["comments"] = ""

    # Create the output directory
    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Protect an existing evaluation file
    if OUTPUT_FILE.exists():
        raise FileExistsError(
            f"Evaluation file already exists: {OUTPUT_FILE}\n"
            "Rename or back it up before creating a new template."
        )

    # Save the evaluation template
    evaluation_df.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8",
    )

    print("\nPrompt evaluation template created.")
    print(f"Input records: {len(df)}")
    print(f"Output file: {OUTPUT_FILE}")

    print("\nRecords per prompt strategy:")
    print(
        evaluation_df.groupby("prompt_strategy")
        .size()
        .to_string()
    )

    print("\nBasic output statistics:")
    print(
        evaluation_df.groupby("prompt_strategy")
        .agg(
            average_word_count=("summary_word_count", "mean"),
            nonempty_outputs=("output_nonempty", "sum"),
            average_generation_seconds=(
                "generation_seconds",
                "mean",
            ),
        )
        .round(2)
        .to_string()
    )


if __name__ == "__main__":
    main()
