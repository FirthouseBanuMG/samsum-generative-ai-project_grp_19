"""Test reproducibility metadata for the seeded test-split model comparison."""

from evaluation import run_model_family_comparison_50 as comparison


def test_sample_manifest_uses_repository_relative_processed_test_path():
    manifest = comparison.build_sample_manifest(
        [{"sample_id": "sample-1"}],
        seed=7,
    )

    assert manifest == {
        "seed": 7,
        "sample_count": 1,
        "dataset": "data/processed/samsum-test-processed.csv",
        "excluded_pilot_ids": [
            "13681000",
            "13728094",
            "13818513",
        ],
        "sample_ids": ["sample-1"],
    }
