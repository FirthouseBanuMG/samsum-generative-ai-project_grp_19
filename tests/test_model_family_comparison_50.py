"""Test reproducibility metadata for the seeded test-split model comparison."""

import json

import pandas as pd

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


def test_sample_selection_excludes_previously_evaluated_ids(tmp_path, monkeypatch):
    test_file = tmp_path / "test.csv"
    pd.DataFrame(
        [
            {"id": f"id-{index}", "dialogue": f"A: {index}", "summary": "summary"}
            for index in range(10)
        ]
    ).to_csv(test_file, index=False)
    monkeypatch.setattr(comparison, "TEST_FILE", test_file)

    selected = comparison.select_samples(
        sample_size=5,
        seed=3,
        excluded_ids={"id-1", "id-2", "id-3", "id-4", "id-5"},
    )

    selected_ids = {sample["sample_id"] for sample in selected}
    assert len(selected_ids) == 5
    assert selected_ids.isdisjoint({"id-1", "id-2", "id-3", "id-4", "id-5"})


def test_load_excluded_ids_reads_manifest_sample_ids(tmp_path):
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "dataset": "data/processed/samsum-test-processed.csv",
                "sample_ids": ["a", 2],
            }
        ),
        encoding="utf-8",
    )

    assert comparison.load_excluded_ids(manifest_path) == {"a", "2"}


def test_load_excluded_ids_accepts_windows_manifest_paths(tmp_path):
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "dataset": "data\\processed\\samsum-test-processed.csv",
                "sample_ids": ["a"],
            }
        ),
        encoding="utf-8",
    )

    assert comparison.load_excluded_ids(manifest_path) == {"a"}


def test_human_review_templates_are_blinded_and_separate(tmp_path):
    comparison.create_human_review_templates(
        [
            {
                "sample_id": "id-1",
                "model_name": "model-z",
                "dialogue": "A: Hi",
                "generated_summary": "A greeting.",
            },
            {
                "sample_id": "id-1",
                "model_name": "model-a",
                "dialogue": "A: Hi",
                "generated_summary": "They said hello.",
            },
        ],
        tmp_path,
    )

    reviewer_one = pd.read_csv(tmp_path / "human_review_reviewer_1.csv")
    reviewer_two = pd.read_csv(tmp_path / "human_review_reviewer_2.csv")
    assert set(reviewer_one["blind_model"]) == {"Model A", "Model B"}
    assert "model_name" not in reviewer_one.columns
    assert reviewer_one.equals(reviewer_two)
    key = json.loads((tmp_path / "review_key.json").read_text(encoding="utf-8"))
    assert set(key) == {"Model A", "Model B"}
