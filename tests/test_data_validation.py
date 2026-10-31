"""Test that dataset validators fail explicitly on missing and invalid inputs."""

import pandas as pd
import pytest

from data_processing import validate_dataset
from data_processing import validate_processed_dataset


def test_raw_validation_fails_when_a_split_file_is_missing(tmp_path):
    with pytest.raises(ValueError, match="file not found"):
        validate_dataset.validate_raw_splits(tmp_path)


def test_raw_validation_fails_when_required_columns_are_missing(tmp_path):
    for filename in validate_dataset.FILES.values():
        pd.DataFrame({"id": ["1"], "dialogue": ["A: Hi"]}).to_csv(
            tmp_path / filename,
            index=False,
        )

    with pytest.raises(ValueError, match="missing required columns"):
        validate_dataset.validate_raw_splits(tmp_path)


def test_raw_validation_fails_on_missing_ids(tmp_path):
    for filename in validate_dataset.FILES.values():
        pd.DataFrame(
            {
                "id": ["1", "2", None],
                "dialogue": ["A: Hi", "B: Hello", "C: Hey"],
                "summary": ["Hi", "Hello", "Hey"],
            }
        ).to_csv(tmp_path / filename, index=False)

    with pytest.raises(ValueError, match="missing IDs"):
        validate_dataset.validate_raw_splits(tmp_path)


def test_raw_validation_fails_on_duplicate_ids(tmp_path):
    for filename in validate_dataset.FILES.values():
        pd.DataFrame(
            {
                "id": ["1", "1", "2"],
                "dialogue": ["A: Hi", "B: Hello", "C: Hey"],
                "summary": ["Hi", "Hello", "Hey"],
            }
        ).to_csv(tmp_path / filename, index=False)

    with pytest.raises(ValueError, match="duplicate IDs"):
        validate_dataset.validate_raw_splits(tmp_path)


def test_processed_validation_fails_when_a_split_file_is_missing(tmp_path):
    with pytest.raises(FileNotFoundError, match="Processed train split"):
        validate_processed_dataset.validate_processed_splits(tmp_path)


def test_processed_validation_fails_with_explicit_row_count_error(tmp_path):
    pd.DataFrame(
        [{"id": "1", "dialogue": "A: Hi", "summary": "Hello."}]
    ).to_csv(tmp_path / "samsum-train-processed.csv", index=False)

    with pytest.raises(ValueError, match="expected 14731 rows"):
        validate_processed_dataset.validate_processed_splits(tmp_path)
