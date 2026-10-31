
"""Test model-specific input formatting, architecture settings, and result validation."""

import unittest

from evaluation import run_model_family_comparison as comparison


class TestInputFormatting(unittest.TestCase):

    def test_constraint_based_format(self):
        dialogue = "Amanda: I baked cookies.\nJerry: Sure!"
        result = comparison.prepare_input(
            dialogue, "constraint_based"
        )
        self.assertIn(dialogue, result)
        self.assertIn(
            "Use only facts explicitly supported", result
        )

    def test_dialogue_only_format(self):
        dialogue = "Amanda: I baked cookies."
        self.assertEqual(
            comparison.prepare_input(dialogue, "dialogue_only"),
            dialogue,
        )

    def test_empty_dialogue_is_rejected(self):
        with self.assertRaises(ValueError):
            comparison.prepare_input("", "dialogue_only")

    def test_unknown_format_is_rejected(self):
        with self.assertRaises(ValueError):
            comparison.prepare_input("Hello", "unknown_format")


class TestModelArchitectureConfiguration(unittest.TestCase):

    def test_qwen_uses_causal_lm(self):
        self.assertEqual(
            comparison.MODEL_CONFIGS[0]["family"], "causal_lm"
        )

    def test_flan_t5_uses_seq2seq(self):
        self.assertEqual(
            comparison.MODEL_CONFIGS[1]["family"],
            "seq2seq_instruction",
        )

    def test_distilbart_uses_seq2seq(self):
        self.assertEqual(
            comparison.MODEL_CONFIGS[2]["family"],
            "seq2seq_summarization",
        )


class TestResultSaving(unittest.TestCase):

    def test_empty_results_are_rejected(self):
        with self.assertRaises(ValueError):
            comparison.save_results([])


def test_input_truncation_metadata_records_long_prompts():
    class FakeTokenizer:
        def __call__(self, prompt, *, add_special_tokens, truncation):
            assert add_special_tokens is True
            assert truncation is False
            return {"input_ids": list(range(comparison.MAX_INPUT_TOKENS + 1))}

    token_count, truncated = comparison.input_truncation_metadata(
        FakeTokenizer(),
        "long prompt",
    )

    assert token_count == comparison.MAX_INPUT_TOKENS + 1
    assert truncated is True


if __name__ == "__main__":
    unittest.main()
