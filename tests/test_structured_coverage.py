"""Test when the narrow commitment-coverage heuristic raises review warnings."""

from structured_output.coverage import find_unrepresented_commitments


def test_missing_explicit_commitment_is_flagged():
    dialogue = (
        "Amanda: I baked cookies. Do you want some?\n"
        "Jerry: Sure!\n"
        "Amanda: I'll bring you tomorrow :-)"
    )
    output = {"action_items": []}

    flags = find_unrepresented_commitments(dialogue, output)

    assert len(flags) == 1
    assert "Amanda" in flags[0]
    assert "I'll bring you tomorrow" in flags[0]


def test_matching_action_item_is_not_flagged():
    dialogue = "Amanda: I'll bring cookies tomorrow."
    output = {
        "action_items": [
            {"owner": "Amanda", "task": "Bring cookies to Jerry", "due": "tomorrow"}
        ]
    }

    assert find_unrepresented_commitments(dialogue, output) == []


def test_tentative_future_intention_is_not_flagged():
    dialogue = "Kim: Maybe I'll do that tomorrow."
    output = {"action_items": []}

    assert find_unrepresented_commitments(dialogue, output) == []


def test_non_commitment_and_unstructured_lines_are_ignored():
    dialogue = (
        "Amanda: I won't bring anything.\n"
        "Jerry: I will not bring anything.\n"
        "This line has no speaker."
    )
    output = {"action_items": []}

    assert find_unrepresented_commitments(dialogue, output) == []
