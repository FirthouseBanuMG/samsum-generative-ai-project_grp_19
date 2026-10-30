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

for split, filename in FILES.items():
    path = DATA_DIR / filename

    print(f"\n{'=' * 55}")
    print(f"SPLIT: {split.upper()}")
    print(f"FILE: {filename}")

    if not path.exists():
        print("ERROR: File not found.")
        continue

    df = pd.read_csv(path, encoding="utf-8")

    print(f"Rows: {len(df):,}")
    print(f"Columns: {list(df.columns)}")
    print(f"Expected columns present: {EXPECTED_COLUMNS.issubset(df.columns)}")

    if not EXPECTED_COLUMNS.issubset(df.columns):
        print("ERROR: Required columns are missing; skipping further checks.")
        continue

    print("\nMissing values:")
    print(df[["id", "dialogue", "summary"]].isna().sum().to_string())

    print("\nBlank dialogue rows:", int(
        df["dialogue"].fillna("").astype(str).str.strip().eq("").sum()
    ))
    print("Blank summary rows:", int(
        df["summary"].fillna("").astype(str).str.strip().eq("").sum()
    ))
    print("Duplicate IDs:", int(df["id"].duplicated().sum()))

    lengths = df["dialogue"].dropna().astype(str).str.len()
    if not lengths.empty:
        print(f"Dialogue length (characters): min={lengths.min()}, "
              f"median={lengths.median():.0f}, max={lengths.max()}")

    print("\nFirst example:")
    print("ID:", df.iloc[0]["id"])
    print("Dialogue:", str(df.iloc[0]["dialogue"])[:350])
    print("Reference summary:", str(df.iloc[0]["summary"])[:250])

print(f"\n{'=' * 55}")
print("Dataset validation inspection complete.")
