"""Inspect raw SAMSum splits for required columns, missing data, and basic quality.

Run with ``python -m data_processing.validate_dataset`` before preprocessing.
"""

from pathlib import Path
import pandas as pd

from project_paths import PROJECT_ROOT

ROOT = PROJECT_ROOT
DATA_DIR = ROOT / "data" / "raw"

FILES = {
    "train": "samsum-train.csv",
    "validation": "samsum-validation.csv",
    "test": "samsum-test.csv",
}

EXPECTED_COLUMNS = {"id", "dialogue", "summary"}


def validate_raw_splits(data_dir: Path = DATA_DIR):
    """Inspect all raw splits and raise when a file or required column is missing."""
    failures = []

    for split, filename in FILES.items():
        path = data_dir / filename

        print(f"\n{'=' * 55}")
        print(f"SPLIT: {split.upper()}")
        print(f"FILE: {filename}")

        if not path.is_file():
            failures.append(f"{split}: file not found: {path}")
            print(f"ERROR: File not found: {path}")
            continue

        df = pd.read_csv(path, encoding="utf-8")

        print(f"Rows: {len(df):,}")
        print(f"Columns: {list(df.columns)}")
        missing_columns = EXPECTED_COLUMNS - set(df.columns)
        print(f"Expected columns present: {not missing_columns}")

        if missing_columns:
            failures.append(
                f"{split}: missing required columns {sorted(missing_columns)}"
            )
            print(
                "ERROR: Required columns are missing; "
                "skipping further checks."
            )
            continue

        print("\nMissing values:")
        print(df[["id", "dialogue", "summary"]].isna().sum().to_string())

        print("\nBlank dialogue rows:", int(
            df["dialogue"].fillna("").astype(str).str.strip().eq("").sum()
        ))
        print("Blank summary rows:", int(
            df["summary"].fillna("").astype(str).str.strip().eq("").sum()
        ))
        duplicate_ids = df["id"].dropna().duplicated()
        print("Duplicate IDs:", int(duplicate_ids.sum()))
        if df["id"].isna().any():
            failures.append(f"{split}: missing IDs")
        if duplicate_ids.any():
            failures.append(f"{split}: duplicate IDs")

        lengths = df["dialogue"].dropna().astype(str).str.len()
        if not lengths.empty:
            print(f"Dialogue length (characters): min={lengths.min()}, "
                  f"median={lengths.median():.0f}, max={lengths.max()}")

        if not df.empty:
            print("\nFirst example:")
            print("ID:", df.iloc[0]["id"])
            print("Dialogue:", str(df.iloc[0]["dialogue"])[:350])
            print("Reference summary:", str(df.iloc[0]["summary"])[:250])

    print(f"\n{'=' * 55}")
    if failures:
        raise ValueError("Raw dataset validation failed:\n- " + "\n- ".join(failures))
    print("Dataset validation inspection complete.")


def main():
    validate_raw_splits()


if __name__ == "__main__":
    main()
