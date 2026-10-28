from pathlib import Path
import json
import pandas as pd

from project_paths import PROJECT_ROOT

ROOT = PROJECT_ROOT
RAW_DIR = ROOT / "data" / "raw"
OUT_DIR = ROOT / "data" / "processed"
OUT_DIR.mkdir(parents=True, exist_ok=True)

FILES = {
    "train": "samsum-train.csv",
    "validation": "samsum-validation.csv",
    "test": "samsum-test.csv",
}
REQUIRED = ["id", "dialogue", "summary"]
exclusions = []
results = {}

for split, filename in FILES.items():
    source = RAW_DIR / filename
    if not source.exists():
        raise FileNotFoundError(f"Required source file missing: {source}")

    df = pd.read_csv(source, encoding="utf-8")

    missing_columns = set(REQUIRED) - set(df.columns)
    if missing_columns:
        raise ValueError(f"{filename}: missing columns {sorted(missing_columns)}")

    if df["id"].isna().any() or df["id"].duplicated().any():
        raise ValueError(f"{filename}: missing or duplicate IDs; investigate first")

    original_rows = len(df)
    invalid_dialogue = (
        df["dialogue"].isna()
        | df["dialogue"].astype("string").str.strip().eq("").fillna(True)
    )
    invalid_summary = (
        df["summary"].isna()
        | df["summary"].astype("string").str.strip().eq("").fillna(True)
    )

    for _, row in df[invalid_dialogue | invalid_summary].iterrows():
        reasons = []
        if pd.isna(row["dialogue"]) or not str(row["dialogue"]).strip():
            reasons.append("missing_or_blank_dialogue")
        if pd.isna(row["summary"]) or not str(row["summary"]).strip():
            reasons.append("missing_or_blank_summary")
        exclusions.append({
            "split": split,
            "id": str(row["id"]),
            "reason": ";".join(reasons),
        })

    keep = ~(invalid_dialogue | invalid_summary)
    processed = df.loc[keep, REQUIRED].copy()

    if processed["id"].duplicated().any():
        raise ValueError(f"{split}: duplicate IDs after preprocessing")
    if processed[["dialogue", "summary"]].isna().any().any():
        raise ValueError(f"{split}: missing dialogue/summary after preprocessing")
    if processed["dialogue"].astype(str).str.strip().eq("").any():
        raise ValueError(f"{split}: blank dialogue after preprocessing")
    if processed["summary"].astype(str).str.strip().eq("").any():
        raise ValueError(f"{split}: blank summary after preprocessing")

    output = OUT_DIR / f"samsum-{split}-processed.csv"
    processed.to_csv(output, index=False, encoding="utf-8")

    results[split] = {
        "source_file": f"data/raw/{filename}",
        "output_file": str(output.relative_to(ROOT)),
        "source_rows": original_rows,
        "processed_rows": len(processed),
        "excluded_rows": original_rows - len(processed),
    }

exclusion_file = OUT_DIR / "exclusions.json"
exclusion_file.write_text(
    json.dumps(exclusions, indent=2), encoding="utf-8"
)

metadata = {
    "required_columns": REQUIRED,
    "text_transformation": "none; original text preserved",
    "truncation": "none",
    "source_files_modified": False,
    "split_results": results,
    "exclusions_file": str(exclusion_file.relative_to(ROOT)),
}
metadata_file = OUT_DIR / "preprocessing_metadata.json"
metadata_file.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

print("PREPROCESSING COMPLETED AND VALIDATED")
for split, info in results.items():
    print(
        f"{split}: source={info['source_rows']}, "
        f"processed={info['processed_rows']}, "
        f"excluded={info['excluded_rows']}"
    )
print(f"Exclusion log: {exclusion_file.relative_to(ROOT)}")
print(f"Metadata: {metadata_file.relative_to(ROOT)}")
print("Original raw CSV files were not modified.")
