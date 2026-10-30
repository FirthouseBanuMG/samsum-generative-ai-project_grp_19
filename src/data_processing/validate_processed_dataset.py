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

for split, expected_rows in EXPECTED.items():
    path = DATA / f"samsum-{split}-processed.csv"
    df = pd.read_csv(path, encoding="utf-8")

    assert REQUIRED.issubset(df.columns), f"{split}: required columns missing"
    assert len(df) == expected_rows, f"{split}: unexpected row count"
    assert df["id"].notna().all(), f"{split}: missing IDs"
    assert df["id"].is_unique, f"{split}: duplicate IDs"
    assert df["dialogue"].notna().all(), f"{split}: missing dialogues"
    assert df["summary"].notna().all(), f"{split}: missing summaries"
    assert df["dialogue"].astype(str).str.strip().ne("").all(), (
        f"{split}: blank dialogues"
    )
    assert df["summary"].astype(str).str.strip().ne("").all(), (
        f"{split}: blank summaries"
    )

    print(
        f"{split}: PASS | rows={len(df)} | "
        f"columns={list(df.columns)} | IDs unique | text fields valid"
    )

print("\nALL PROCESSED SPLITS PASSED INDEPENDENT VALIDATION.")
