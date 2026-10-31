"""Test validation and aggregation of independent blinded human ratings."""

import json

import pandas as pd
import pytest

from evaluation.summarize_human_reviews import (
    RATING_COLUMNS,
    summarize_reviews,
)


def _review_rows(score: int) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "sample_id": "sample-1",
                "blind_model": "Model A",
                "factual_support_1_to_5": score,
                "key_event_coverage_1_to_5": score,
                "speaker_attribution_1_to_5": score,
            }
        ]
    )


def test_summarize_reviews_reports_means_and_rater_agreement(tmp_path):
    reviewer_one = tmp_path / "reviewer_1.csv"
    reviewer_two = tmp_path / "reviewer_2.csv"
    key_path = tmp_path / "review_key.json"
    _review_rows(4).to_csv(reviewer_one, index=False)
    _review_rows(3).to_csv(reviewer_two, index=False)
    key_path.write_text(
        json.dumps({"Model A": "model-id"}),
        encoding="utf-8",
    )

    summary, agreement = summarize_reviews(
        reviewer_one,
        reviewer_two,
        key_path,
    )

    assert summary.loc[0, "model_name"] == "model-id"
    assert summary.loc[0, "review_rows"] == 2
    assert summary.loc[0, RATING_COLUMNS[0]] == 3.5
    assert agreement[RATING_COLUMNS[0]] == {
        "exact_agreement": 0.0,
        "mean_absolute_difference": 1.0,
    }


def test_summarize_reviews_rejects_missing_ratings(tmp_path):
    reviewer_one = tmp_path / "reviewer_1.csv"
    reviewer_two = tmp_path / "reviewer_2.csv"
    key_path = tmp_path / "review_key.json"
    rows = _review_rows(4)
    rows.loc[0, RATING_COLUMNS[0]] = None
    rows.to_csv(reviewer_one, index=False)
    _review_rows(4).to_csv(reviewer_two, index=False)
    key_path.write_text(json.dumps({"Model A": "model-id"}), encoding="utf-8")

    with pytest.raises(ValueError, match="incomplete or nonnumeric"):
        summarize_reviews(reviewer_one, reviewer_two, key_path)


def test_summarize_reviews_rejects_invalid_score_range(tmp_path):
    reviewer_one = tmp_path / "reviewer_1.csv"
    reviewer_two = tmp_path / "reviewer_2.csv"
    key_path = tmp_path / "review_key.json"
    _review_rows(6).to_csv(reviewer_one, index=False)
    _review_rows(4).to_csv(reviewer_two, index=False)
    key_path.write_text(json.dumps({"Model A": "model-id"}), encoding="utf-8")

    with pytest.raises(ValueError, match="must be from 1 to 5"):
        summarize_reviews(reviewer_one, reviewer_two, key_path)
