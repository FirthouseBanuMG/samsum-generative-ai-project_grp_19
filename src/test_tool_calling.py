"""Offline tests for the application-level tool-calling workflow."""

from run_tool_calling import (
    TOOL_NAME,
    execute_tool_call,
    parse_tool_request,
)


def test_valid_tool_request_executes():
    request = {
        "tool_name": TOOL_NAME,
        "arguments": {
            "output": {"summary": "They agreed to meet.", "action_items": []}
        },
    }
    result = execute_tool_call(request)
    assert result["valid"] is True


def test_invalid_schema_is_reported():
    request = {
        "tool_name": TOOL_NAME,
        "arguments": {
            "output": {"summary": "A summary", "action_items": "invalid"}
        },
    }
    result = execute_tool_call(request)
    assert result["valid"] is False


def test_unknown_tool_is_rejected():
    request = {"tool_name": "delete_files", "arguments": {"output": {}}}
    try:
        execute_tool_call(request)
    except ValueError:
        return
    raise AssertionError("Unknown tool should be rejected.")


def test_wrong_arguments_are_rejected():
    request = {"tool_name": TOOL_NAME, "arguments": {"unexpected": {}}}
    try:
        execute_tool_call(request)
    except ValueError:
        return
    raise AssertionError("Unexpected arguments should be rejected.")


def test_malformed_request_is_rejected():
    try:
        parse_tool_request('{"tool_name": ')
    except ValueError:
        return
    raise AssertionError("Malformed JSON should be rejected.")


def main():
    tests = [
        test_valid_tool_request_executes,
        test_invalid_schema_is_reported,
        test_unknown_tool_is_rejected,
        test_wrong_arguments_are_rejected,
        test_malformed_request_is_rejected,
    ]
    for test in tests:
        test()
        print("PASS", test.__name__)
    print(f"{len(tests)}/{len(tests)} tool-calling tests passed.")


if __name__ == "__main__":
    main()
