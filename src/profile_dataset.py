from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "raw"

for split, filename in [
    ("train", "samsum-train.csv"),
    ("validation", "samsum-validation.csv"),
    ("test", "samsum-test.csv"),
]:
    df = pd.read_csv(DATA / filename, encoding="utf-8")
    print(f"\n=== {split.upper()} ===")

    for column in ["dialogue", "summary"]:
        lengths = df[column].dropna().astype(str).str.len()
        if lengths.empty:
            continue
        print(
            f"{column} characters: "
            f"min={lengths.min()}, "
            f"median={lengths.median():.0f}, "
            f"p95={lengths.quantile(0.95):.0f}, "
            f"max={lengths.max()}"
        )

print("\nProfiling complete. Raw CSV files were not modified.")
