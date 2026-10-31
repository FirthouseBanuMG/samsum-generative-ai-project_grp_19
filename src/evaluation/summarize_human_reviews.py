"""Summarize two independent human-rating CSVs and reveal model identities.

Run with ``python -m evaluation.summarize_human_reviews --reviewer-1 <csv>
--reviewer-2 <csv> --review-key <json>`` after both reviewers finish their
blinded ratings.
"""

import argparse
import json
from pathlib import Path

import pandas as pd


RATING_COLUMNS = [
    "factual_support_1_to_5",
    "key_event_coverage_1_to_5",
    "speaker_attribution_1_to_5",
]
KEY_COLUMNS = ["sample_id", "blind_model"]


def load_review(path: Path) -> pd.DataFrame:
    """Load a completed review file and validate keys and 1-5 ratings."""
    frame = pd.read_csv(path, dtype={"sample_id": str, "blind_model": str})
    required = set(KEY_COLUMNS + RATING_COLUMNS)
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"{path}: missing columns {sorted(missing)}")
    if frame.duplicated(KEY_COLUMNS).any():
        raise ValueError(f"{path}: duplicate sample/model review rows")

    for column in RATING_COLUMNS:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
        if frame[column].isna().any():
            raise ValueError(f"{path}: incomplete or nonnumeric ratings in {column}")
        if not frame[column].between(1, 5).all():
            raise ValueError(f"{path}: ratings in {column} must be from 1 to 5")
    return frame


def summarize_reviews(
    reviewer_one_path: Path,
    reviewer_two_path: Path,
    review_key_path: Path,
) -> tuple[pd.DataFrame, dict]:
    """Validate reviewer agreement and return per-model means and agreement."""
    reviewer_one = load_review(reviewer_one_path)
    reviewer_two = load_review(reviewer_two_path)
    keys_one = set(map(tuple, reviewer_one[KEY_COLUMNS].to_numpy()))
    keys_two = set(map(tuple, reviewer_two[KEY_COLUMNS].to_numpy()))
    if keys_one != keys_two:
        raise ValueError("Reviewer files do not contain the same sample/model rows.")

    joined = reviewer_one.merge(
        reviewer_two,
        on=KEY_COLUMNS,
        suffixes=("_r1", "_r2"),
        validate="one_to_one",
    )
    agreement = {}
    for column in RATING_COLUMNS:
        first = joined[f"{column}_r1"]
        second = joined[f"{column}_r2"]
        agreement[column] = {
            "exact_agreement": float(first.eq(second).mean()),
            "mean_absolute_difference": float((first - second).abs().mean()),
        }

    pooled = pd.concat([reviewer_one, reviewer_two], ignore_index=True)
    summary = (
        pooled.groupby("blind_model", as_index=False)
        .agg(
            review_rows=("sample_id", "count"),
            **{
                column: (column, "mean")
                for column in RATING_COLUMNS
            },
        )
    )
    key = json.loads(review_key_path.read_text(encoding="utf-8"))
    if not isinstance(key, dict) or set(summary["blind_model"]) - set(key):
        raise ValueError("Review key does not map every blinded model label.")
    summary["model_name"] = summary["blind_model"].map(key)
    return summary, agreement


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reviewer-1", type=Path, required=True)
    parser.add_argument("--reviewer-2", type=Path, required=True)
    parser.add_argument("--review-key", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("human_review_summary.csv"))
    args = parser.parse_args()

    summary, agreement = summarize_reviews(
        args.reviewer_1,
        args.reviewer_2,
        args.review_key,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(args.output, index=False, encoding="utf-8")
    print(summary.to_string(index=False))
    print("\nInter-rater agreement (descriptive; no chance-corrected statistic):")
    print(json.dumps(agreement, indent=2))
    print(f"\nSummary saved to: {args.output}")


if __name__ == "__main__":
    main()
