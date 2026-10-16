from pathlib import Path
import pandas as pd
from transformers import AutoTokenizer

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "raw"
MODEL = "Qwen/Qwen2.5-1.5B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(MODEL)

for split, filename in [
    ("train", "samsum-train.csv"),
    ("validation", "samsum-validation.csv"),
    ("test", "samsum-test.csv"),
]:
    df = pd.read_csv(DATA / filename, encoding="utf-8")
    print(f"\n=== {split.upper()} ===")

    for column in ["dialogue", "summary"]:
        texts = df[column].dropna().astype(str).tolist()
        lengths = [len(tokenizer.encode(text, add_special_tokens=False))
                   for text in texts]
        s = pd.Series(lengths)
        print(
            f"{column} tokens: n={len(s)}, min={s.min()}, "
            f"median={s.median():.0f}, p95={s.quantile(0.95):.0f}, "
            f"max={s.max()}"
        )

print("\nToken profiling complete. Raw CSV files were not modified.")
