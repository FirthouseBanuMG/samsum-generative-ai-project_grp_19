"""
Structured-output schema and validation for the SAMSum project (E4).

Defines the machine-readable JSON schema the model is asked to produce
(a summary, key points, decisions, and action items) and the helpers used to
parse and validate model output, including recovery from model chatter
around the JSON object.
"""

import json
import re
from typing import Optional

from jsonschema import Draft202012Validator


# --------------------------------------------------
# SCHEMA
# --------------------------------------------------

# Machine-readable contract for a summarized conversation.
# A valid object has a summary, key points, decisions, and action items.
# Each action item names an owner and task; a due date is optional.
SUMMARY_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "properties": {
        "summary": {
            "type": "string",
            "minLength": 1,
        },
        "key_points": {
            "type": "array",
            "items": {"type": "string", "minLength": 1},
        },
        "decisions": {
            "type": "array",
            "items": {"type": "string", "minLength": 1},
        },
        "action_items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "owner": {"type": "string", "minLength": 1},
                    "task": {"type": "string", "minLength": 1},
                    "due": {"type": ["string", "null"]},
                },
                "required": ["owner", "task"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["summary", "key_points", "decisions", "action_items"],
    "additionalProperties": False,
}


_VALIDATOR = Draft202012Validator(SUMMARY_SCHEMA)


# --------------------------------------------------
# VALIDATION
# --------------------------------------------------

def validate_output(obj):
    """Validate a parsed object against SUMMARY_SCHEMA.

    Returns a tuple of (is_valid, error_messages). The error list is
    empty when the object is valid.
    """

    errors = sorted(_VALIDATOR.iter_errors(obj), key=lambda err: err.path)

    messages = []
    for error in errors:
        location = "/".join(str(part) for part in error.path) or "<root>"
        messages.append(f"{location}: {error.message}")

    return (len(messages) == 0), messages


# --------------------------------------------------
# JSON EXTRACTION
# --------------------------------------------------

# Matches a fenced code block such as ```json ... ``` or ``` ... ```.
_FENCE_PATTERN = re.compile(
    r"```(?:json)?\s*(?P<body>.*?)```",
    re.DOTALL | re.IGNORECASE,
)


def extract_json(raw_text: str) -> Optional[str]:
    """Extract the most likely JSON object from raw model output.

    Handles three common cases:
    1. Output wrapped in a ```json ... ``` fenced block.
    2. A JSON object preceded or followed by explanatory text.
    3. Clean JSON with no surrounding text.

    Returns the candidate JSON string, or None if no object-like span
    is found.
    """

    if not isinstance(raw_text, str) or not raw_text.strip():
        return None

    # Prefer the contents of a fenced code block when present.
    fence_match = _FENCE_PATTERN.search(raw_text)
    candidate = fence_match.group("body") if fence_match else raw_text

    # Grab the outermost {...} span so leading/trailing prose is dropped.
    start = candidate.find("{")
    end = candidate.rfind("}")

    if start == -1 or end == -1 or end < start:
        return None

    return candidate[start:end + 1].strip()


def parse_and_validate(raw_text: str):
    """Extract, parse and validate model output in one call.

    Returns a dict describing the outcome:
        extracted_json: the extracted JSON string (or None)
        parsed: the parsed Python object (or None)
        parse_ok: whether json.loads succeeded
        schema_valid: whether the parsed object matched the schema
        errors: list of parse/validation error messages
    """

    extracted = extract_json(raw_text)

    if extracted is None:
        return {
            "extracted_json": None,
            "parsed": None,
            "parse_ok": False,
            "schema_valid": False,
            "errors": ["No JSON object found in output."],
        }

    try:
        parsed = json.loads(extracted)
    except json.JSONDecodeError as error:
        return {
            "extracted_json": extracted,
            "parsed": None,
            "parse_ok": False,
            "schema_valid": False,
            "errors": [f"JSONDecodeError: {error}"],
        }

    schema_valid, messages = validate_output(parsed)

    return {
        "extracted_json": extracted,
        "parsed": parsed,
        "parse_ok": True,
        "schema_valid": schema_valid,
        "errors": messages,
    }
