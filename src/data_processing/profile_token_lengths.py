"""Report tokenizer-based length statistics for raw SAMSum dialogues and summaries.

Run with ``python -m data_processing.profile_token_lengths``; requires model tokenizer files.
"""

import pandas as pd
from transformers import AutoTokenizer

from project_paths import PROJECT_ROOT

DATA = PROJECT_ROOT / "data" / "raw"
MODEL = "Qwen/Qwen2.5-1.5B-Instruct"


def main():
    """Load the tokenizer and report raw split token-length distributions."""
    tokenizer = AutoTokenizer.from_pretrained(MODEL)

    for split, filename in [
        ("train", "samsum-train.csv"),
        ("validation", "samsum-validation.csv"),
        ("test", "samsum-test.csv"),
    ]:
        path = DATA / filename
        if not path.is_file():
            raise FileNotFoundError(f"Raw {split} split not found: {path}")
        df = pd.read_csv(path, encoding="utf-8")
        missing = {"dialogue", "summary"} - set(df.columns)
        if missing:
            raise ValueError(
                f"{path.name}: missing required columns {sorted(missing)}"
            )
        print(f"\n=== {split.upper()} ===")

        for column in ["dialogue", "summary"]:
            texts = df[column].dropna().astype(str).tolist()
            lengths = [
                len(tokenizer.encode(text, add_special_tokens=False))
                for text in texts
            ]
            if not lengths:
                print(f"{column} tokens: no non-missing values")
                continue
            values = pd.Series(lengths)
            print(
                f"{column} tokens: n={len(values)}, min={values.min()}, "
                f"median={values.median():.0f}, "
                f"p95={values.quantile(0.95):.0f}, max={values.max()}"
            )

    print("\nToken profiling complete. Raw CSV files were not modified.")


if __name__ == "__main__":
    main()
