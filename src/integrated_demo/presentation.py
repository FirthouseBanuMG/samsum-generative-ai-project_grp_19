"""Human-readable presentation helpers for the integrated demo.

The functions in this module convert generated summaries and follow-up
responses into fixed-width console tables for easier human review.
"""

from collections.abc import Mapping, Sequence
import re
from textwrap import wrap


# Keep the table dimensions in one place so the console layout is easy to tune.
_FIELD_WIDTH = 18
_CONTENT_WIDTH = 72

# Recognize only the supported section headings. Any other response text is
# retained under the generic "Response" field rather than being discarded.
_FINAL_SECTION_PATTERN = re.compile(
    r"^(Summary|Key Points|Decisions|Action Items|Validation note|"
    r"Completeness review required):\\s*(.*)$",
    re.IGNORECASE,
)


def format_final_response_for_review(response: str) -> str:
    """Render a model follow-up as a table, preserving unrecognized text."""
    if not isinstance(response, str) or not response.strip():
        raise ValueError("Final response must be a non-empty string.")

    # Normalize recognized headings for display while preserving their content.
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
        """Store the accumulated text before moving to the next section."""
        if current_lines:
            # Copy the list so later clearing does not change the saved row.
            rows.append((current_field, current_lines.copy()))
            current_lines.clear()

    for line in response.splitlines():
        match = _FINAL_SECTION_PATTERN.match(line.strip())
        if match:
            # A recognized heading starts a new table section.
            save_current_section()
            current_field = section_names[match.group(1).casefold()]
            if match.group(2).strip():
                current_lines.append(match.group(2).strip())
            continue

        # Ignore blank lines, but preserve all non-empty unrecognized content.
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
        # Do not present an invalid or fallback generation as a validated
        # summary. Instead, show its status and any available diagnostics.
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

    # Read the expected fields only after schema validation has succeeded.
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

    # Convert each section into lines that can be displayed in the table.
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

        # Keep the task, owner, and optional due date grouped under one item.
        action_item_lines.extend(
            [
                f"{index}. {task}",
                f"   Owner: {owner}",
            ]
        )
        if due:
            action_item_lines.append(f"   Due: {due}")
    rows.append(("Action items", action_item_lines or ["None identified."]))

    # Schema validation checks structure, so the output still needs human review
    # for accuracy and completeness.
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
    """Format a list as bullet lines, including a message for an empty list."""
    if not items:
        return ["None identified."]
    return [f"- {item}" for item in items]


def _render_table(
    rows: list[tuple[str, list[str]]],
    *,
    title: str = "STRUCTURED SUMMARY FOR REVIEW",
) -> str:
    """Build a fixed-width text table and wrap long content to fit its columns."""
    field_width = _FIELD_WIDTH
    content_width = _CONTENT_WIDTH

    # Build a reusable horizontal border based on the configured column widths.
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
            # Escape vertical bars so content cannot be mistaken for a table
            # column separator. Preserve indentation for wrapped bullet items.
            wrapped_lines.extend(
                wrap(
                    content.replace("|", "\\\\|"),
                    width=content_width,
                    subsequent_indent="  " if content.startswith("- ") else "",
                    break_long_words=False,
                    break_on_hyphens=False,
                )
                or [""]
            )

        # Show the field name once, then leave its cells blank for continuation
        # lines belonging to the same field.
        for line_index, content in enumerate(wrapped_lines):
            label = field if line_index == 0 else ""
            rendered.append(
                f"| {label.ljust(field_width)} | "
                f"{content.ljust(content_width)} |"
            )
        rendered.append(border)

    return "\\n".join(rendered)
