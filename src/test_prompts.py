from prompts import PROMPT_FUNCTIONS, build_prompt


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

    print("SUCCESS: All four prompt templates passed.")


if __name__ == "__main__":
    main()
