"""Offline tests for the application-level tool-calling workflow."""

from tool_calling.run_tool_calling import (
    TOOL_NAME,
    VALIDATION_NOTICE,
    build_final_response_messages,
    execute_tool_call,
    generate_final_response,
    parse_tool_request,
)


def test_valid_tool_request_executes():
    request = {
        "tool_name": TOOL_NAME,
        "arguments": {
            "output": {
                "summary": "They agreed to meet.",
                "key_points": ["They discussed meeting."],
                "decisions": ["They agreed to meet."],
                "action_items": [],
            }
        },
    }
    result = execute_tool_call(request)
    assert result["valid"] is True


def test_invalid_schema_is_reported():
    request = {
        "tool_name": TOOL_NAME,
        "arguments": {
            "output": {
                "summary": "A summary",
                "key_points": [],
                "decisions": [],
                "action_items": "invalid",
            }
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


def test_final_response_receives_tool_result(monkeypatch):
    request = {
        "tool_name": TOOL_NAME,
        "arguments": {
            "output": {
                "summary": "They agreed to meet.",
                "key_points": ["They discussed meeting."],
                "decisions": ["They agreed to meet."],
                "action_items": [],
            }
        },
    }
    tool_result = execute_tool_call(request)
    captured = {}

    def fake_generate_text(messages, tokenizer, model):
        captured["messages"] = messages
        return "Final response"

    monkeypatch.setattr(
        "tool_calling.run_tool_calling.generate_text",
        fake_generate_text,
    )
    final = generate_final_response(
        "A: Let's meet.\nB: Agreed.",
        '{"tool_name":"validate_summary_output"}',
        tool_result,
        None,
        None,
    )

    assert final.startswith("Final response")
    assert VALIDATION_NOTICE in final
    assert captured["messages"][1]["content"].endswith(
        "A: Let's meet.\nB: Agreed."
    )
    assert '"valid": true' in captured["messages"][-1]["content"]


def test_invalid_tool_result_blocks_final_response():
    invalid_result = {
        "tool": TOOL_NAME,
        "valid": False,
        "errors": ["Invalid payload"],
    }

    try:
        build_final_response_messages(
            "A: Hello",
            '{"tool_name":"validate_summary_output"}',
            invalid_result,
        )
    except ValueError as exc:
        assert "validation failed" in str(exc)
    else:
        raise AssertionError("Invalid tool results must block final response.")


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
    print(f"{len(tests)}/{len(tests)} local tool-calling checks passed.")


if __name__ == "__main__":
    main()
