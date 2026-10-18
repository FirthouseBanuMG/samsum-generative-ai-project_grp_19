import json
from pathlib import Path

import pandas as pd


# --------------------------------------------------
# STEP 1: Define input and output file paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

BASELINE_FILE = (
    PROJECT_ROOT
    / "outputs"
    / "baseline_smoke_test"
    / "baseline_outputs.json"
)

EVALUATION_DIR = (
    PROJECT_ROOT
    / "outputs"
    / "evaluation"
)

EVALUATION_FILE = (
    EVALUATION_DIR
    / "baseline_evaluation.csv"
)


# --------------------------------------------------
# STEP 2: Read the existing baseline outputs
# --------------------------------------------------

def load_baseline_outputs(file_path):

    if not file_path.exists():
        raise FileNotFoundError(
            f"Baseline output file not found: {file_path}"
        )

    with file_path.open("r", encoding="utf-8") as file:
        records = json.load(file)

    if not isinstance(records, list):
        raise ValueError(
            "Expected baseline_outputs.json "
            "to contain a list of records."
        )

    if not records:
        raise ValueError(
            "The baseline output file contains no records."
        )

    required_fields = {
        "sample_id",
        "dialogue",
        "reference_summary",
        "generated_summary",
    }

    for index, record in enumerate(records):

        if not isinstance(record, dict):
            raise ValueError(
                f"Record {index} must be a JSON object."
            )

        missing_fields = required_fields - set(record.keys())

        if missing_fields:
            raise ValueError(
                f"Record {index} is missing fields: "
                f"{sorted(missing_fields)}"
            )

    return records


# --------------------------------------------------
# STEP 3: Prepare the evaluation records
# --------------------------------------------------

def prepare_evaluation_records(records):

    evaluation_records = []

    for record in records:

        dialogue = record["dialogue"]
        reference = record["reference_summary"]
        generated = record["generated_summary"]

        generated = generated or ""

        # Count the words in the generated summary.
        word_count = len(generated.split())

        # Basic automated output checks.
        is_nonempty = bool(generated.strip())

        # Preserve the existing generation time,
        # if it was recorded in the original output.
        generation_seconds = record.get(
            "generation_seconds"
        )

        evaluation_records.append({

            "sample_id": record["sample_id"],

            "dialogue": dialogue,

            "reference_summary": reference,

            "generated_summary": generated,

            "summary_word_count": word_count,

            "output_nonempty": is_nonempty,

            "generation_seconds": generation_seconds,

            # These scores will be filled in
            # after human evaluation.
            "relevance_score": None,

            "coverage_score": None,

            "factual_consistency_score": None,

            "output_reliability_score": None,

            # Record factual and coverage problems.
            "unsupported_claims": "",

            "missing_information": "",

            "comments": "",

        })

    return evaluation_records


# --------------------------------------------------
# STEP 4: Save the evaluation CSV
# --------------------------------------------------

def save_evaluation_csv(records, output_file):

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # Never overwrite an existing evaluation.
    # This protects any scores you have already entered.
    if output_file.exists():
        raise FileExistsError(
            f"Evaluation file already exists: {output_file}\n"
            "Rename or back up the existing file before "
            "creating a new evaluation template."
        )

    df = pd.DataFrame(records)

    df.to_csv(
        output_file,
        index=False,
        encoding="utf-8"
    )

    print("\nBaseline evaluation template created.")
    print(f"Output file: {output_file}")
    print(f"Number of records: {len(df)}")

    print("\nBasic output statistics:")

    print(
        df[
            [
                "sample_id",
                "summary_word_count",
                "output_nonempty",
                "generation_seconds",
            ]
        ].to_string(index=False)
    )

    print("\nNext, manually evaluate the four quality criteria.")


# --------------------------------------------------
# STEP 5: Run the complete workflow
# --------------------------------------------------

def main():

    print("Loading existing baseline outputs...")

    records = load_baseline_outputs(BASELINE_FILE)

    print(f"Loaded {len(records)} baseline records.")

    print("\nPreparing evaluation records...")

    evaluation_records = prepare_evaluation_records(
        records
    )

    print("\nSaving evaluation CSV...")

    save_evaluation_csv(
        evaluation_records,
        EVALUATION_FILE
    )


if __name__ == "__main__":
    main()