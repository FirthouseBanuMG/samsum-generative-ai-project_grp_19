"""Test prompt templates, summary-detail variants, and explicit commitment guidance."""

import pytest

from prompting.prompts import (
    PROMPT_FUNCTIONS,
    build_prompt,
    build_summary_detail_prompt,
    structured_json_prompt,
)


def main():
    sample_dialogue = """
Sam: I need to finish my assignment.
Alex: You could work on it tonight.
Sam: Maybe. I will see how I feel after dinner.
"""

    print("Testing all prompt strategies...")
    print("-" * 40)

    for strategy in PROMPT_FUNCTIONS:
        prompt = build_prompt(
            strategy=strategy,
            dialogue=sample_dialogue
        )

        assert sample_dialogue.strip() in prompt
        assert len(prompt) > len(sample_dialogue)

        print(f"Strategy: {strategy}")
        print(f"Prompt length: {len(prompt)} characters")
        print("Test passed!")
        print()

    concise = build_summary_detail_prompt("concise", sample_dialogue)
    detailed = build_summary_detail_prompt("detailed", sample_dialogue)
    assert sample_dialogue.strip() in concise
    assert sample_dialogue.strip() in detailed
    assert "exactly one concise sentence" in concise
    assert "3-5 concise sentences" in detailed
    assert "Distinguish suggestions" in concise
    assert "Distinguish suggestions" in detailed
    print("Concise and detailed prompt templates passed.")

    print("SUCCESS: All four prompt templates passed.")


def test_summary_detail_prompt_validation():
    dialogue = "A: We will meet at noon.\nB: I agree."
    concise = build_summary_detail_prompt("concise", dialogue)
    detailed = build_summary_detail_prompt("detailed", dialogue)

    assert dialogue in concise
    assert dialogue in detailed
    assert "exactly one concise sentence" in concise
    assert "3-5 concise sentences" in detailed
    for shared_rule in (
        "Use only facts supported by the dialogue.",
        "Distinguish suggestions and",
        "Do not invent details.",
    ):
        assert shared_rule in concise
        assert shared_rule in detailed

    with pytest.raises(ValueError, match="Unknown summary detail style"):
        build_summary_detail_prompt("medium", "A: Hi")

    with pytest.raises(ValueError, match="non-empty"):
        build_summary_detail_prompt("concise", "  ")


def test_structured_prompt_requires_explicit_commitment_coverage():
    dialogue = (
        "Amanda: I baked cookies. Do you want some?\n"
        "Jerry: Sure!\n"
        "Amanda: I'll bring you tomorrow."
    )
    prompt = structured_json_prompt(dialogue)

    assert "Do not skip a short final turn." in prompt
    assert "Capture explicit future commitments" in prompt
    assert "Leave action_items empty only when no participant explicitly commits" in prompt
    assert dialogue in prompt


if __name__ == "__main__":
    main()
