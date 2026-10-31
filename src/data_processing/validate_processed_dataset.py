"""Assert processed SAMSum splits match expected counts and required data constraints.

Run with ``python -m data_processing.validate_processed_dataset`` after preprocessing.
"""

from pathlib import Path
import pandas as pd

from project_paths import PROJECT_ROOT

ROOT = PROJECT_ROOT
DATA = ROOT / "data" / "processed"
EXPECTED = {
    "train": 14731,
    "validation": 818,
    "test": 819,
}
REQUIRED = {"id", "dialogue", "summary"}


def validate_processed_splits(data_dir: Path = DATA):
    """Check all processed splits and raise explicit errors on invalid data."""
    for split, expected_rows in EXPECTED.items():
        path = data_dir / f"samsum-{split}-processed.csv"
        if not path.is_file():
            raise FileNotFoundError(f"Processed {split} split not found: {path}")

        df = pd.read_csv(path, encoding="utf-8", dtype={"id": str})
        missing_columns = REQUIRED - set(df.columns)
        if missing_columns:
            raise ValueError(
                f"{split}: required columns missing: {sorted(missing_columns)}"
            )
        if len(df) != expected_rows:
            raise ValueError(
                f"{split}: expected {expected_rows} rows, found {len(df)}"
            )
        if df["id"].isna().any():
            raise ValueError(f"{split}: missing IDs")
        if not df["id"].is_unique:
            raise ValueError(f"{split}: duplicate IDs")
        for column in ("dialogue", "summary"):
            if df[column].isna().any():
                raise ValueError(f"{split}: missing {column}s")
            if not df[column].str.strip().ne("").all():
                raise ValueError(f"{split}: blank {column}s")

        print(
            f"{split}: PASS | rows={len(df)} | "
            f"columns={list(df.columns)} | IDs unique | text fields valid"
        )

    print("\nALL PROCESSED SPLITS PASSED INDEPENDENT VALIDATION.")


def main():
    validate_processed_splits()


if __name__ == "__main__":
    main()
