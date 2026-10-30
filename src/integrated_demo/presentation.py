"""Human-readable presentation helpers for the integrated demo."""

from collections.abc import Mapping, Sequence
import re
from textwrap import wrap


_FIELD_WIDTH = 18
_CONTENT_WIDTH = 72
_FINAL_SECTION_PATTERN = re.compile(
    r"^(Summary|Key Points|Decisions|Action Items|Validation note|"
    r"Completeness review required):\s*(.*)$",
    re.IGNORECASE,
)


def format_final_response_for_review(response: str) -> str:
    """Render a model follow-up as a table, preserving unrecognized text."""
    if not isinstance(response, str) or not response.strip():
        raise ValueError("Final response must be a non-empty string.")

    section_names = {
        "summary": "Summary",
        "key points": "Key points",
        "decisions": "Decisions",
        "action items": "Action items",
        "validation note": "Validation",
        "completeness review required": "Review warning",
    }
    rows: list[tuple[str, list[str]]] = []
    current_field = "Response"
    current_lines: list[str] = []

    def save_current_section() -> None:
        if current_lines:
            rows.append((current_field, current_lines.copy()))
            current_lines.clear()

    for line in response.splitlines():
        match = _FINAL_SECTION_PATTERN.match(line.strip())
        if match:
            save_current_section()
            current_field = section_names[match.group(1).casefold()]
            if match.group(2).strip():
                current_lines.append(match.group(2).strip())
            continue

        if not line.strip():
            continue
        current_lines.append(line.strip())

    save_current_section()
    return _render_table(rows, title="FINAL RESPONSE")


def format_summary_for_review(
    output: Mapping[str, object],
    *,
    schema_valid: bool,
    used_fallback: bool,
    validation_errors: Sequence[str] = (),
    coverage_flags: Sequence[str] = (),
) -> str:
    """Render a structured generation as a readable console table."""
    rows: list[tuple[str, list[str]]] = []

    if not schema_valid:
        rows.append(
            (
                "Status",
                [
                    "Not schema-valid. No validated summary is presented.",
                    "Inspect the saved generation diagnostics.",
                ],
            )
        )
        if used_fallback:
            rows.append(
                (
                    "Fallback",
                    ["Saved for diagnostics; not shown as a validated summary."],
                )
            )
        if validation_errors:
            rows.append(
                ("Validation issues", [f"- {error}" for error in validation_errors])
            )
        return _render_table(rows)

    summary = output.get("summary")
    key_points = output.get("key_points")
    decisions = output.get("decisions")
    action_items = output.get("action_items")
    if (
        not isinstance(summary, str)
        or not isinstance(key_points, list)
        or not isinstance(decisions, list)
        or not isinstance(action_items, list)
    ):
        raise ValueError("Schema-valid output does not match the summary schema.")
    if not all(isinstance(item, str) for item in key_points + decisions):
        raise ValueError("Key points and decisions must contain only strings.")

    rows.append(("Summary", [summary]))
    rows.append(("Key points", _format_text_list(key_points)))
    rows.append(("Decisions", _format_text_list(decisions)))

    action_item_lines = []
    for index, item in enumerate(action_items, start=1):
        if not isinstance(item, Mapping):
            raise ValueError("Each action item must be an object.")
        owner = item.get("owner")
        task = item.get("task")
        due = item.get("due")
        if not isinstance(owner, str) or not isinstance(task, str):
            raise ValueError("Action items require string owner and task fields.")
        if due is not None and not isinstance(due, str):
            raise ValueError("Action item due values must be strings or null.")
        action_item_lines.extend(
            [
                f"{index}. {task}",
                f"   Owner: {owner}",
            ]
        )
        if due:
            action_item_lines.append(f"   Due: {due}")
    rows.append(("Action items", action_item_lines or ["None identified."]))

    review_notes = [
        "JSON Schema validation passed.",
        "Human review required; structural validity does not prove accuracy.",
    ]
    if used_fallback:
        review_notes.append("Fallback output was used; inspect generation diagnostics.")
    if coverage_flags:
        review_notes.extend(f"Warning: {flag}" for flag in coverage_flags)
    else:
        review_notes.append(
            "No commitment warning was detected; completeness is not guaranteed."
        )
    rows.append(("Review notes", review_notes))
    return _render_table(rows)


def _format_text_list(items: list[str]) -> list[str]:
    if not items:
        return ["None identified."]
    return [f"- {item}" for item in items]


def _render_table(
    rows: list[tuple[str, list[str]]],
    *,
    title: str = "STRUCTURED SUMMARY FOR REVIEW",
) -> str:
    field_width = _FIELD_WIDTH
    content_width = _CONTENT_WIDTH
    border = (
        f"+{'-' * (field_width + 2)}"
        f"+{'-' * (content_width + 2)}+"
    )
    rendered = [
        title,
        border,
        f"| {'Field'.ljust(field_width)} | "
        f"{'Details'.ljust(content_width)} |",
        border,
    ]
    for field, content_lines in rows:
        wrapped_lines = []
        for content in content_lines:
            wrapped_lines.extend(
                wrap(
                    content.replace("|", "\\|"),
                    width=content_width,
                    subsequent_indent="  " if content.startswith("- ") else "",
                    break_long_words=False,
                    break_on_hyphens=False,
                )
                or [""]
            )
        for line_index, content in enumerate(wrapped_lines):
            label = field if line_index == 0 else ""
            rendered.append(
                f"| {label.ljust(field_width)} | "
                f"{content.ljust(content_width)} |"
            )
        rendered.append(border)
    return "\n".join(rendered)
