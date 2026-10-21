"""
Fast checks for the structured-output schema and helpers (E4).

Runs without loading the model so the validation and extraction logic
can be verified quickly before any slow generation.
"""

from structured_schema import (
    validate_output,
    extract_json,
    parse_and_validate,
)


def test_valid_object_passes():
    obj = {
        "summary": "Amanda baked cookies and will bring some to Jerry tomorrow.",
        "action_items": [
            {"owner": "Amanda", "task": "Bring cookies to Jerry", "due": "tomorrow"},
        ],
    }

    is_valid, errors = validate_output(obj)

    assert is_valid, f"Expected valid object, got errors: {errors}"
    assert errors == []


def test_empty_action_items_passes():
    obj = {"summary": "They exchanged greetings.", "action_items": []}

    is_valid, errors = validate_output(obj)

    assert is_valid, f"Expected valid object, got errors: {errors}"


def test_missing_summary_fails():
    obj = {"action_items": []}

    is_valid, errors = validate_output(obj)

    assert not is_valid
    assert errors, "Expected validation errors for missing summary."


def test_wrong_action_items_type_fails():
    obj = {"summary": "A summary.", "action_items": "not-a-list"}

    is_valid, errors = validate_output(obj)

    assert not is_valid
    assert errors


def test_action_item_missing_owner_fails():
    obj = {
        "summary": "A summary.",
        "action_items": [{"task": "Do the thing"}],
    }

    is_valid, errors = validate_output(obj)

    assert not is_valid
    assert errors


def test_extract_json_from_fenced_block():
    raw = 'Here is the result:\n```json\n{"summary": "s", "action_items": []}\n```\nThanks!'

    extracted = extract_json(raw)

    assert extracted == '{"summary": "s", "action_items": []}'


def test_extract_json_from_surrounding_prose():
    raw = 'Sure! {"summary": "s", "action_items": []} Let me know if you need more.'

    extracted = extract_json(raw)

    assert extracted == '{"summary": "s", "action_items": []}'


def test_extract_json_returns_none_without_object():
    assert extract_json("no json here") is None
    assert extract_json("") is None


def test_parse_and_validate_malformed_json():
    result = parse_and_validate('{"summary": "s", "action_items": [}')

    assert result["parse_ok"] is False
    assert result["schema_valid"] is False
    assert result["errors"]


def test_parse_and_validate_valid_json():
    result = parse_and_validate('{"summary": "s", "action_items": []}')

    assert result["parse_ok"] is True
    assert result["schema_valid"] is True
    assert result["errors"] == []


def main():
    tests = [value for name, value in sorted(globals().items())
             if name.startswith("test_") and callable(value)]

    passed = 0
    for test in tests:
        test()
        print(f"PASS  {test.__name__}")
        passed += 1

    print(f"\n{passed}/{len(tests)} structured-schema tests passed.")


if __name__ == "__main__":
    main()
