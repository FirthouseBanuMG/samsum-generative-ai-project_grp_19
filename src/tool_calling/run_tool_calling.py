"""Validate structured summaries through an allowlisted application-level tool.

The model emits a JSON tool-call request. The application validates the
request, executes the named Python function, and records the result.

The module also supports a model-backed round trip; this JSON protocol is not
native model-specific tool calling. Run the demonstration with
``python -m tool_calling.run_tool_calling``.
"""

import json
import time

from project_paths import PROJECT_ROOT
from structured_output.schema import SUMMARY_SCHEMA, validate_output


BASELINE_PATH = PROJECT_ROOT / "outputs" / "baseline_smoke_test" / "baseline_outputs.json"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "tool_calling"
MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"
MAX_NEW_TOKENS = 256

TOOL_NAME = "validate_summary_output"
VALIDATION_NOTICE = (
    "Validation note: The output passed JSON Schema checks for structure "
    "only; this does not verify factual accuracy or completeness. Human "
    "review is required."
)

TOOL_SPEC = {
    "name": TOOL_NAME,
    "description": (
        "Validate a proposed conversation summary and its action items "
        "against the project's JSON schema."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "output": {
                **SUMMARY_SCHEMA,
                "description": (
                    "Proposed structured summary with summary, key_points, "
                    "decisions, and action_items."
                ),
            }
        },
        "required": ["output"],
        "additionalProperties": False,
    },
}


def validate_summary_output(output):
    """Callable tool: validate a summary object and return diagnostics."""
    valid, errors = validate_output(output)
    return {
        "tool": TOOL_NAME,
        "valid": valid,
        "errors": errors,
        "schema": SUMMARY_SCHEMA,
    }


def execute_tool_call(request):
    """Validate a model-requested tool call and execute only the allowlisted tool."""
    if not isinstance(request, dict):
        raise ValueError("Tool request must be a JSON object.")

    if request.get("tool_name") != TOOL_NAME:
        raise ValueError(f"Unknown tool name: {request.get('tool_name')!r}")

    arguments = request.get("arguments")
    if not isinstance(arguments, dict):
        raise ValueError("Tool arguments must be an object.")

    if set(arguments) != {"output"}:
        raise ValueError("Expected exactly one argument named 'output'.")

    output = arguments["output"]
    if not isinstance(output, dict):
        raise ValueError("'output' must be a JSON object.")

    return validate_summary_output(output)


def load_model():
    # Import ML dependencies only when a model run is requested.
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        dtype=torch.float32,
        low_cpu_mem_usage=True,
    )
    model.eval()
    return tokenizer, model


def generate_text(messages, tokenizer, model):
    import torch

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )
    inputs = tokenizer(prompt, return_tensors="pt")
    with torch.inference_mode():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=MAX_NEW_TOKENS,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )
    generated = output_ids[0, inputs["input_ids"].shape[1]:]
    return tokenizer.decode(generated, skip_special_tokens=True).strip()


def make_tool_request(dialogue, tokenizer, model):
    messages = [
        {
            "role": "system",
            "content": (
                "You are part of a conversation summarization application. "
                "You must request the validation tool. Return only one JSON "
                "object with exactly these fields: tool_name and arguments. "
                f"tool_name must be {TOOL_NAME!r}. arguments must contain "
                "one field, output. output must contain summary (string) "
                "and key_points and decisions (lists of strings). It must "
                "also have action_items (list of objects with owner, task, "
                "and optional due). Use only facts supported by the dialogue. "
                "If no action items are agreed, use an empty list. Do not "
                "invent commitments or deadlines. Do not use Markdown fences."
            ),
        },
        {
            "role": "user",
            "content": f"Conversation:\n{dialogue}\n\nTool specification:\n"
            + json.dumps(TOOL_SPEC, ensure_ascii=False),
        },
    ]
    return generate_text(messages, tokenizer, model)


def parse_tool_request(raw_text):
    """Parse a complete JSON tool request; do not execute extracted fragments."""
    try:
        request = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Model did not return valid JSON: {exc}") from exc

    if not isinstance(request, dict):
        raise ValueError("Tool request must be a JSON object.")

    if set(request) != {"tool_name", "arguments"}:
        raise ValueError("Tool request must contain exactly tool_name and arguments.")

    return request


def build_final_response_messages(dialogue, raw_request, tool_result):
    """Build the application-level follow-up after the tool has executed."""
    if not isinstance(dialogue, str) or not dialogue.strip():
        raise ValueError("Dialogue must be a non-empty string.")
    if not isinstance(raw_request, str) or not raw_request.strip():
        raise ValueError("Raw tool request must be a non-empty string.")
    if not isinstance(tool_result, dict) or tool_result.get("tool") != TOOL_NAME:
        raise ValueError("Tool result does not match the requested validation tool.")
    if tool_result.get("valid") is not True:
        raise ValueError("Final response is blocked because tool validation failed.")

    return [
        {
            "role": "system",
            "content": (
                "You are a conversation summarization assistant. Give the user "
                "a concise response based on the original conversation and the "
                "application tool result. Schema validation confirms structure "
                "only; it does not prove factual correctness. Do not claim "
                "semantic verification. Use the structured output from the "
                "preceding assistant message without adding, changing, or "
                "omitting claims. Describe empty lists as 'none identified', "
                "not as 'none needed'. State that the output passed structural "
                "validation only and still needs human review."
            ),
        },
        {"role": "user", "content": f"Original conversation:\n{dialogue}"},
        {"role": "assistant", "content": raw_request},
        {
            "role": "user",
            "content": (
                "The application executed the requested tool. Tool result:\n"
                f"{json.dumps(tool_result, ensure_ascii=False)}\n\n"
                "Now provide the final user-facing response using the exact "
                "summary, key_points, decisions, and action_items from the "
                "preceding assistant message. Do not introduce any new facts. "
                "The tool result validates structure only."
            ),
        },
    ]


def generate_final_response(dialogue, raw_request, tool_result, tokenizer, model):
    """Generate a final user-facing response only after successful validation."""
    messages = build_final_response_messages(dialogue, raw_request, tool_result)
    response = generate_text(messages, tokenizer, model)
    if not response.strip():
        raise ValueError("The model returned an empty final response.")
    return f"{response}\n\n{VALIDATION_NOTICE}"


def run_local_checks():
    """Fast checks run without loading the language model."""
    valid_request = {
        "tool_name": TOOL_NAME,
        "arguments": {
            "output": {
                "summary": "Amanda will bring cookies to Jerry tomorrow.",
                "key_points": [
                    "Jerry accepts Amanda's offer of cookies."
                ],
                "decisions": [
                    "Amanda will bring cookies to Jerry tomorrow."
                ],
                "action_items": [
                    {
                        "owner": "Amanda",
                        "task": "Bring cookies to Jerry",
                        "due": "tomorrow",
                    }
                ],
            }
        },
    }
    result = execute_tool_call(valid_request)
    assert result["valid"], result["errors"]

    invalid_schema_request = {
        "tool_name": TOOL_NAME,
        "arguments": {
            "output": {
                "summary": "A summary",
                "key_points": [],
                "decisions": [],
                "action_items": "not-a-list",
            }
        },
    }
    result = execute_tool_call(invalid_schema_request)
    assert not result["valid"]

    try:
        execute_tool_call({
            "tool_name": "unapproved_tool",
            "arguments": {"output": {}},
        })
    except ValueError:
        pass
    else:
        raise AssertionError("Unknown tools must be rejected.")

    try:
        parse_tool_request('{"tool_name": ')
    except ValueError:
        pass
    else:
        raise AssertionError("Malformed tool-call JSON must be rejected.")

    print("PASS: valid tool call executes and validates.")
    print("PASS: schema-invalid payload is rejected by the schema validator.")
    print("PASS: unknown tool names are rejected.")
    print("PASS: malformed tool-call JSON is rejected.")


def main():
    run_local_checks()

    records = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    if not isinstance(records, list) or not records:
        raise ValueError("Baseline outputs must contain a non-empty list.")

    # Use the first existing baseline example for a small demonstration.
    record = records[0]
    dialogue = record.get("dialogue")
    if not isinstance(dialogue, str) or not dialogue.strip():
        raise ValueError("Baseline example has no usable dialogue.")

    print(f"\nLoading {MODEL_NAME} on CPU...")
    tokenizer, model = load_model()

    start = time.time()
    raw_request = make_tool_request(dialogue, tokenizer, model)
    request = parse_tool_request(raw_request)
    tool_result = execute_tool_call(request)
    final_response = None
    final_response_status = "blocked_tool_validation_failed"
    if tool_result["valid"]:
        final_response = generate_final_response(
            dialogue,
            raw_request,
            tool_result,
            tokenizer,
            model,
        )
        final_response_status = "generated_after_valid_tool_result"

    evidence = {
        "experiment": "application_level_json_tool_calling",
        "model": MODEL_NAME,
        "sample_id": str(record.get("sample_id", "unknown")),
        "dataset_split": record.get("dataset_split", "train"),
        "protocol_note": (
            "Application-level JSON tool-call protocol; not native model-specific "
            "tool-call token parsing."
        ),
        "tool_specification": TOOL_SPEC,
        "dialogue": dialogue,
        "raw_model_tool_request": raw_request,
        "parsed_tool_request": request,
        "tool_execution_result": tool_result,
        "final_response_status": final_response_status,
        "final_response": final_response,
        "execution_seconds_including_generation": round(time.time() - start, 3),
        "human_review_required": True,
        "review_note": (
            "Schema validation checks structure only. "
            "Review the summary and action items for factual support "
            "against the original dialogue."
        ),
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / "tool_calling_demo.json"
    output_path.write_text(
        json.dumps(evidence, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("\n=== TOOL CALLING DEMONSTRATION ===")
    print("Requested tool:", request["tool_name"])
    print("Tool executed:", tool_result["tool"])
    print("Schema valid:", tool_result["valid"])
    print("Validation errors:", tool_result["errors"])
    print("Evidence saved:", output_path)


if __name__ == "__main__":
    main()
