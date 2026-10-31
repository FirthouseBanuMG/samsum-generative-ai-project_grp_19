"""Test user-supplied dialogue validation and provenance in the integrated demo."""

import json

import pytest

from integrated_demo import run_integrated_demo as demo


def test_run_demo_rejects_empty_or_ambiguous_input():
    with pytest.raises(ValueError, match="non-empty"):
        demo.run_demo(dialogue=" ")
    with pytest.raises(ValueError, match="either sample_id or dialogue"):
        demo.run_demo(sample_id="13818513", dialogue="A: Hi")


def test_user_supplied_dialogue_is_recorded_and_runs_through_validation(
    tmp_path,
    monkeypatch,
):
    generation = {
        "commitment_coverage_flags": [],
        "schema_valid": True,
        "used_fallback": False,
        "final_object": {
            "summary": "They greeted each other.",
            "key_points": [],
            "decisions": [],
            "action_items": [],
        },
    }
    monkeypatch.setattr(demo, "load_model", lambda device="cpu": ("tokenizer", "model"))
    monkeypatch.setattr(
        demo,
        "generate_structured",
        lambda dialogue, tokenizer, model: generation,
    )
    monkeypatch.setattr(
        demo,
        "generate_final_response",
        lambda *args: "A reviewed response.",
    )
    output_file = tmp_path / "demo_result.json"
    monkeypatch.setattr(demo, "OUTPUT_FILE", output_file)

    result = demo.run_demo(dialogue="Alex: Hi\nSam: Hello.")

    assert result["sample_id"] is None
    assert result["dataset_split"] == "user_supplied"
    assert result["dialogue"] is None
    assert result["dialogue_sha256"]
    assert result["tool_result"]["valid"] is True
    saved = json.loads(output_file.read_text(encoding="utf-8"))
    assert saved["dataset_split"] == "user_supplied"
    assert saved["dialogue"] is None


def test_user_supplied_dialogue_can_be_saved_explicitly(tmp_path, monkeypatch):
    generation = {
        "commitment_coverage_flags": [],
        "schema_valid": False,
        "used_fallback": True,
        "validation_errors": ["invalid"],
        "final_object": {"summary": "invalid"},
    }
    monkeypatch.setattr(demo, "load_model", lambda device="cpu": ("tokenizer", "model"))
    monkeypatch.setattr(
        demo,
        "generate_structured",
        lambda dialogue, tokenizer, model: generation,
    )
    output_file = tmp_path / "demo_result.json"
    monkeypatch.setattr(demo, "OUTPUT_FILE", output_file)

    demo.run_demo(dialogue="Alex: Hi", save_input=True)

    saved = json.loads(output_file.read_text(encoding="utf-8"))
    assert saved["dialogue"] == "Alex: Hi"
