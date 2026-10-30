"""Check processed dataset splits for shared IDs and exact dialogue-summary pairs.

Run with ``python -m data_processing.check_split_leakage`` after preprocessing.
"""

import pandas as pd

from project_paths import PROJECT_ROOT

DATA = PROJECT_ROOT / "data" / "processed"
FILES = {
    "train": "samsum-train-processed.csv",
    "validation": "samsum-validation-processed.csv",
    "test": "samsum-test-processed.csv",
}

frames = {}
for split, filename in FILES.items():
    path = DATA / filename
    if not path.is_file():
        raise FileNotFoundError(
            f"Processed {split} split not found: {path}. "
            "Run data_processing.preprocess_dataset first."
        )
    frame = pd.read_csv(path, encoding="utf-8", dtype={"id": str})
    required = {"id", "dialogue", "summary"}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"{path.name}: missing columns {sorted(missing)}")
    frames[split] = frame

overlap_found = False
for left, right in [
    ("train", "validation"),
    ("train", "test"),
    ("validation", "test"),
]:
    shared_ids = set(frames[left]["id"].dropna()) & set(
        frames[right]["id"].dropna()
    )
    left_valid = frames[left].dropna(subset=["dialogue", "summary"])
    right_valid = frames[right].dropna(subset=["dialogue", "summary"])
    left_pairs = set(zip(left_valid["dialogue"], left_valid["summary"]))
    right_pairs = set(zip(right_valid["dialogue"], right_valid["summary"]))
    shared_pairs = left_pairs & right_pairs

    print(
        f"{left} vs {right}: "
        f"{len(shared_ids)} shared IDs; "
        f"{len(shared_pairs)} shared exact dialogue-summary pairs"
    )
    overlap_found |= bool(shared_ids or shared_pairs)

if overlap_found:
    raise ValueError(
        "Cross-split leakage detected in processed data. "
        "Do not use these splits for experiments until investigated."
    )

print("Processed split leakage check passed.")
