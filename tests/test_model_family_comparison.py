
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


if __name__ == "__main__":
    unittest.main()
