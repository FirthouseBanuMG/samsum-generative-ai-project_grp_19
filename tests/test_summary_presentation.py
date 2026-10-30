import pytest

from integrated_demo.presentation import (
    format_final_response_for_review,
    format_summary_for_review,
)


def test_formats_summary_sections_and_action_item_details():
    formatted = format_summary_for_review(
        {
            "summary": "Amanda will bring cookies to Jerry tomorrow.",
            "key_points": ["Jerry accepted the offer."],
            "decisions": ["Amanda will bring cookies."],
            "action_items": [
                {
                    "owner": "Amanda",
                    "task": "Bring cookies to Jerry",
                    "due": "tomorrow",
                }
            ],
        },
        schema_valid=True,
        used_fallback=False,
    )

    assert "| Summary            | Amanda will bring cookies to Jerry tomorrow." in formatted
    assert "| Key points         | - Jerry accepted the offer." in formatted
    assert "| Decisions          | - Amanda will bring cookies." in formatted
    assert "| Action items       | 1. Bring cookies to Jerry" in formatted
    assert "|                    |    Owner: Amanda" in formatted
    assert "|                    |    Due: tomorrow" in formatted
    assert "JSON Schema validation passed." in formatted
    assert "Human review required" in formatted


def test_formats_empty_sections_and_coverage_warning():
    formatted = format_summary_for_review(
        {
            "summary": "The participants exchanged greetings.",
            "key_points": [],
            "decisions": [],
            "action_items": [],
        },
        schema_valid=True,
        used_fallback=False,
        coverage_flags=["A commitment may be missing."],
    )

    assert formatted.count("None identified.") == 3
    assert "Warning: A commitment may be missing." in formatted


def test_invalid_schema_does_not_present_unvalidated_summary_as_valid():
    formatted = format_summary_for_review(
        {"summary": "Untrusted output"},
        schema_valid=False,
        used_fallback=True,
        validation_errors=["action_items: required property is missing"],
    )

    assert "Not schema-valid. No validated summary is presented." in formatted
    assert "Saved for diagnostics; not shown as a validated summary." in formatted
    assert "Untrusted output" not in formatted
    assert "- action_items: required property is missing" in formatted


def test_schema_valid_but_mismatched_object_is_reported():
    with pytest.raises(ValueError, match="does not match the summary schema"):
        format_summary_for_review(
            {"summary": "A summary"},
            schema_valid=True,
            used_fallback=False,
        )


def test_formats_model_final_response_as_table():
    formatted = format_final_response_for_review(
        "Summary: Amanda baked cookies for Jerry.\n"
        "Key Points: \n"
        "- Amanda baked cookies\n"
        "- Jerry wants cookies\n\n"
        "Decisions: None identified\n\n"
        "Action Items: None identified\n\n"
        "Validation note: Structure was validated only.\n\n"
        'Completeness review required: Amanda said "I will bring cookies".'
    )

    assert "| Summary            | Amanda baked cookies for Jerry." in formatted
    assert "| Key points         | - Amanda baked cookies" in formatted
    assert "|                    | - Jerry wants cookies" in formatted
    assert "| Decisions          | None identified" in formatted
    assert "| Action items       | None identified" in formatted
    assert "| Validation         | Structure was validated only." in formatted
    assert "| Review warning     | Amanda said" in formatted


def test_preserves_unstructured_final_response_text():
    formatted = format_final_response_for_review("Here is the final answer.")

    assert "| Response           | Here is the final answer." in formatted
