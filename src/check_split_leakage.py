from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "raw"

FILES = {
    "train": "samsum-train.csv",
    "validation": "samsum-validation.csv",
    "test": "samsum-test.csv",
}

frames = {}
for split, filename in FILES.items():
    df = pd.read_csv(DATA / filename, encoding="utf-8")
    df["id"] = df["id"].astype("string")
    frames[split] = df

print("CROSS-SPLIT ID OVERLAP")
for left, right in [
    ("train", "validation"),
    ("train", "test"),
    ("validation", "test"),
]:
    overlap = set(frames[left]["id"].dropna()) & set(
        frames[right]["id"].dropna()
    )
    print(f"{left} vs {right}: {len(overlap)} shared IDs")

print("\nCROSS-SPLIT EXACT DIALOGUE-SUMMARY PAIRS")
for left, right in [
    ("train", "validation"),
    ("train", "test"),
    ("validation", "test"),
]:
    a = frames[left].dropna(subset=["dialogue", "summary"])
    b = frames[right].dropna(subset=["dialogue", "summary"])

    pairs_a = set(zip(a["dialogue"], a["summary"]))
    pairs_b = set(zip(b["dialogue"], b["summary"]))
    print(f"{left} vs {right}: {len(pairs_a & pairs_b)} shared pairs")

print("\nAudit complete. Source CSV files were not modified.")
