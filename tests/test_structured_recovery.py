"""Test structured-output parsing recovery, fallback behavior, and coverage flags."""

import sys
import types

import pytest

# Stub heavyweight model dependencies. These tests do not load a model.
torch_stub = types.ModuleType("torch")
torch_stub.float32 = "float32"
torch_stub.inference_mode = lambda: None
sys.modules.setdefault("torch", torch_stub)

pandas_stub = types.ModuleType("pandas")
sys.modules.setdefault("pandas", pandas_stub)

transformers_stub = types.ModuleType("transformers")
transformers_stub.AutoTokenizer = object
transformers_stub.AutoModelForCausalLM = object
sys.modules.setdefault("transformers", transformers_stub)

from structured_output import run_structured_output as structured


VALID_JSON = (
    '{"summary":"Meeting completed","key_points":[],'
    '"decisions":[],"action_items":[]}'
)
INVALID_JSON = (
    '{"summary":"Meeting completed","key_points":[],'
    '"decisions":[],"action_items":,}'
)


@pytest.fixture
def generator(monkeypatch):
    """Replace model generation with controlled responses."""
    responses = []

    def fake_generate(messages, tokenizer, model):
        if not responses:
            raise AssertionError("Unexpected extra generation attempt")
        return responses.pop(0)

    monkeypatch.setattr(structured, "generate", fake_generate)
    return responses


def test_valid_first_response_needs_no_repair(generator):
    generator.append(VALID_JSON)

    result = structured.generate_structured("Test dialogue", None, None)

    assert result["parse_ok"] is True
    assert result["schema_valid"] is True
    assert result["repair_attempted"] is False
    assert result["recovered"] is False
    assert result["used_fallback"] is False
    assert result["final_object"]["summary"] == "Meeting completed"
    assert result["commitment_coverage_flags"] == []
    assert generator == []


def test_invalid_first_response_recovers_on_retry(generator):
    generator.extend([INVALID_JSON, VALID_JSON])

    result = structured.generate_structured("Test dialogue", None, None)

    assert result["repair_attempted"] is True
    assert result["recovered"] is True
    assert result["used_fallback"] is False
    assert result["final_object"]["summary"] == "Meeting completed"
    assert generator == []


def test_invalid_responses_trigger_fallback(generator):
    generator.extend([INVALID_JSON, INVALID_JSON])

    result = structured.generate_structured("Test dialogue", None, None)

    assert result["repair_attempted"] is True
    assert result["recovered"] is False
    assert result["used_fallback"] is True
    assert result["final_object"]["_needs_review"] is True
    assert result["final_object"]["action_items"] == []
    assert result["commitment_coverage_flags"] == []
    assert generator == []


def test_missing_commitment_is_flagged_even_when_schema_is_valid(generator):
    generator.append(VALID_JSON)

    result = structured.generate_structured(
        "Amanda: I'll bring cookies tomorrow.",
        None,
        None,
    )

    assert result["schema_valid"] is True
    assert len(result["commitment_coverage_flags"]) == 1
    assert "Amanda" in result["commitment_coverage_flags"][0]


def test_schema_invalid_first_response_can_recover(generator):
    schema_invalid = (
        '{"summary":"Meeting completed","key_points":[],'
        '"decisions":[],"action_items":"none"}'
    )
    generator.extend([schema_invalid, VALID_JSON])

    result = structured.generate_structured("Test dialogue", None, None)

    assert result["parse_ok"] is True
    assert result["schema_valid"] is False
    assert result["repair_attempted"] is True
    assert result["recovered"] is True
    assert result["used_fallback"] is False
    assert generator == []
